"""Application-layer perimeter security middlewares for Vinum Pulse."""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass

from starlette.types import ASGIApp, Message, Receive, Scope, Send

MAX_BODY_BYTES: int = 32768

CSP_POLICY: str = "; ".join(
    [
        "default-src 'self'",
        (
            "script-src 'self' 'unsafe-inline' "
            "https://cdn.tailwindcss.com https://unpkg.com https://cdn.jsdelivr.net"
        ),
        (
            "style-src 'self' 'unsafe-inline' "
            "https://unpkg.com https://fonts.googleapis.com"
        ),
        "font-src 'self' data: https://fonts.gstatic.com",
        (
            "img-src 'self' data: blob: "
            "https://tile.openstreetmap.org https://www.ign.es https://unpkg.com"
        ),
        "connect-src 'self' https://tile.openstreetmap.org https://www.ign.es",
        "object-src 'none'",
        "base-uri 'self'",
        "frame-ancestors 'none'",
    ]
)

SECURITY_HEADERS: tuple[tuple[bytes, bytes], ...] = (
    (b"content-security-policy", CSP_POLICY.encode("ascii")),
    (
        b"strict-transport-security",
        b"max-age=63072000; includeSubDomains; preload",
    ),
    (b"x-content-type-options", b"nosniff"),
    (b"x-frame-options", b"DENY"),
    (b"referrer-policy", b"strict-origin-when-cross-origin"),
    (b"permissions-policy", b"geolocation=(), microphone=(), camera=()"),
)


async def _send_json_error(
    send: Send,
    status_code: int,
    detail: str,
    extra_headers: list[tuple[bytes, bytes]] | None = None,
) -> None:
    """Send a minimal JSON error response with mandatory security headers."""
    body = json.dumps({"detail": detail}).encode("utf-8")
    headers: list[tuple[bytes, bytes]] = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode("ascii")),
        *SECURITY_HEADERS,
    ]
    if extra_headers:
        headers.extend(extra_headers)
    await send(
        {"type": "http.response.start", "status": status_code, "headers": headers}
    )
    await send({"type": "http.response.body", "body": body, "more_body": False})


def _extract_header(scope: Scope, name: bytes) -> str | None:
    """Extract a single ASCII header value from an ASGI scope."""
    for raw_key, raw_val in scope.get("headers", ()):
        if raw_key.lower() == name:
            decoded: str = raw_val.decode("latin-1")
            return decoded.strip()
    return None


def _resolve_client_ip(scope: Scope) -> str:
    """Resolve client IP from X-Forwarded-For or ASGI client tuple."""
    forwarded = _extract_header(scope, b"x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    client = scope.get("client")
    if client and isinstance(client, (list, tuple)) and client[0]:
        return str(client[0])
    return "127.0.0.1"


def _is_rate_limited_endpoint(method: str, path: str) -> bool:
    """Return True for mutation and compute endpoints subject to rate limiting."""
    if method in ("POST", "DELETE") and path.startswith("/api/v1/cellar"):
        return True
    return method == "POST" and path.startswith("/api/v1/pairings/")


class SecurityHeadersMiddleware:
    """Attach hardened HTTP security headers to every HTTP response."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize middleware wrapping an ASGI application."""
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Inject security headers on http.response.start events."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", ()))
                existing = {k.lower() for k, _ in headers}
                for key, val in SECURITY_HEADERS:
                    if key not in existing:
                        headers.append((key, val))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)


class _BodyTooLargeError(Exception):
    """Internal signal raised when streamed request body exceeds limit."""


class BodySizeLimitMiddleware:
    """Reject HTTP requests whose payload exceeds MAX_BODY_BYTES with 413."""

    def __init__(self, app: ASGIApp, max_body_bytes: int = MAX_BODY_BYTES) -> None:
        """Initialize middleware with maximum allowed request body size in bytes."""
        self.app = app
        self.max_body_bytes = max_body_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Validate Content-Length header and streamed request body size."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        content_length = _extract_header(scope, b"content-length")
        if (
            content_length
            and content_length.isdigit()
            and int(content_length) > self.max_body_bytes
        ):
            await _send_json_error(
                send,
                413,
                f"Request body exceeds maximum allowed size of "
                f"{self.max_body_bytes} bytes.",
            )
            return

        bytes_seen = 0
        response_started = False

        async def limited_receive() -> Message:
            nonlocal bytes_seen
            message = await receive()
            if message["type"] == "http.request":
                bytes_seen += len(message.get("body", b""))
                if bytes_seen > self.max_body_bytes:
                    raise _BodyTooLargeError
            return message

        async def tracked_send(message: Message) -> None:
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        try:
            await self.app(scope, limited_receive, tracked_send)
        except _BodyTooLargeError:
            if not response_started:
                await _send_json_error(
                    send,
                    413,
                    f"Request body exceeds maximum allowed size of "
                    f"{self.max_body_bytes} bytes.",
                )


@dataclass
class _BucketState:
    """Per-IP token bucket state."""

    tokens: float
    last_refill: float


class TokenBucketRateLimiter:
    """Zero-dependency in-memory per-IP token bucket rate limiter."""

    def __init__(
        self,
        capacity: int = 60,
        refill_per_sec: float = 1.0,
        enabled: bool = True,
    ) -> None:
        """Initialize token bucket parameters and empty IP state map."""
        self.capacity = max(1, capacity)
        self.refill_per_sec = max(0.001, refill_per_sec)
        self.enabled = enabled
        self._buckets: dict[str, _BucketState] = {}

    def reset(self) -> None:
        """Clear all tracked client buckets (primarily for test isolation)."""
        self._buckets.clear()

    def configure(
        self,
        *,
        capacity: int | None = None,
        refill_per_sec: float | None = None,
        enabled: bool | None = None,
    ) -> None:
        """Dynamically reconfigure limiter parameters and reset buckets."""
        if capacity is not None:
            self.capacity = max(1, capacity)
        if refill_per_sec is not None:
            self.refill_per_sec = max(0.001, refill_per_sec)
        if enabled is not None:
            self.enabled = enabled
        self._buckets.clear()

    def consume(self, client_ip: str, now: float | None = None) -> tuple[bool, int]:
        """Attempt to consume 1 token; return (allowed, retry_after_seconds)."""
        if not self.enabled:
            return True, 0

        ts = time.monotonic() if now is None else now
        bucket = self._buckets.get(client_ip)
        if bucket is None:
            bucket = _BucketState(tokens=float(self.capacity), last_refill=ts)
            self._buckets[client_ip] = bucket
        else:
            elapsed = max(0.0, ts - bucket.last_refill)
            bucket.tokens = min(
                float(self.capacity),
                bucket.tokens + elapsed * self.refill_per_sec,
            )
            bucket.last_refill = ts

        if bucket.tokens >= 1.0:
            bucket.tokens -= 1.0
            return True, 0

        needed = 1.0 - bucket.tokens
        retry_after = max(1, math.ceil(needed / self.refill_per_sec))
        return False, retry_after


class RateLimitMiddleware:
    """Enforce per-IP token-bucket rate limits on mutation and compute routes."""

    def __init__(self, app: ASGIApp, limiter: TokenBucketRateLimiter) -> None:
        """Initialize rate limiting middleware with a shared limiter instance."""
        self.app = app
        self.limiter = limiter

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Check rate limit for protected mutation and compute endpoints."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = str(scope.get("method", "GET")).upper()
        path = str(scope.get("path", ""))
        if not _is_rate_limited_endpoint(method, path):
            await self.app(scope, receive, send)
            return

        client_ip = _resolve_client_ip(scope)
        allowed, retry_after = self.limiter.consume(client_ip)
        if not allowed:
            await _send_json_error(
                send,
                429,
                "Rate limit exceeded. Please retry later.",
                extra_headers=[(b"retry-after", str(retry_after).encode("ascii"))],
            )
            return

        await self.app(scope, receive, send)
