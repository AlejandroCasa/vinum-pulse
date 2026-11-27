"""Tests for application-layer perimeter security middlewares and DB settings."""

from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from app.database import Settings, create_db_engine
from app.main import app, rate_limiter
from app.security import MAX_BODY_BYTES, TokenBucketRateLimiter
from app.sommelier import SommelierEngine, init_db

client = TestClient(app)


def test_security_headers_present_on_api_and_ui_responses() -> None:
    """Verify every HTTP response includes hardened security headers."""
    for path in ("/healthz", "/api/v1/wines?limit=1", "/"):
        res = client.get(path)
        assert res.status_code == 200
        assert "content-security-policy" in res.headers
        assert "default-src 'self'" in res.headers["content-security-policy"]
        assert "frame-ancestors 'none'" in res.headers["content-security-policy"]
        assert "strict-transport-security" in res.headers
        assert res.headers["x-content-type-options"] == "nosniff"
        assert res.headers["x-frame-options"] == "DENY"
        assert res.headers["referrer-policy"] == "strict-origin-when-cross-origin"
        assert "permissions-policy" in res.headers


def test_body_size_limit_rejects_oversized_payload_with_413() -> None:
    """Verify payloads exceeding MAX_BODY_BYTES return HTTP 413."""
    oversized_notes = "x" * (MAX_BODY_BYTES + 2048)
    payload = {
        "wine_id": "vina-ardanza-reserva",
        "quantity": 1,
        "notes": oversized_notes,
    }
    res = client.post("/api/v1/cellar", json=payload)
    assert res.status_code == 413
    assert "exceeds maximum allowed size" in res.json()["detail"]
    assert res.headers["x-content-type-options"] == "nosniff"


def test_rate_limiter_enforces_429_with_retry_after() -> None:
    """Verify token-bucket rate limiter returns 429 and Retry-After when exhausted."""
    orig_capacity = rate_limiter.capacity
    orig_refill = rate_limiter.refill_per_sec
    orig_enabled = rate_limiter.enabled
    try:
        rate_limiter.configure(capacity=2, refill_per_sec=0.05, enabled=True)
        headers = {"X-Forwarded-For": "203.0.113.42"}
        payload = {
            "dish_id": "chuleton-brasa",
            "max_budget_eur": 50.0,
            "preferred_type": "Red",
        }
        r1 = client.post("/api/v1/pairings/recommend", json=payload, headers=headers)
        r2 = client.post("/api/v1/pairings/recommend", json=payload, headers=headers)
        r3 = client.post("/api/v1/pairings/recommend", json=payload, headers=headers)

        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r3.status_code == 429
        assert int(r3.headers["retry-after"]) >= 1
        assert "rate limit" in r3.json()["detail"].lower()

        # Non-limited GET endpoints remain accessible even when bucket is empty
        health = client.get("/healthz", headers=headers)
        assert health.status_code == 200
    finally:
        rate_limiter.configure(
            capacity=orig_capacity,
            refill_per_sec=orig_refill,
            enabled=orig_enabled,
        )


def test_token_bucket_unit_refill_and_disable() -> None:
    """Verify TokenBucketRateLimiter refill math, reset, and disable switch."""
    limiter = TokenBucketRateLimiter(capacity=1, refill_per_sec=0.5, enabled=True)
    ok1, retry1 = limiter.consume("10.0.0.1", now=100.0)
    assert ok1 is True
    assert retry1 == 0

    ok2, retry2 = limiter.consume("10.0.0.1", now=100.5)
    assert ok2 is False
    assert retry2 >= 1

    ok3, retry3 = limiter.consume("10.0.0.1", now=103.0)
    assert ok3 is True
    assert retry3 == 0

    limiter.reset()
    limiter.configure(enabled=False)
    ok4, retry4 = limiter.consume("10.0.0.1", now=103.0)
    assert ok4 is True
    assert retry4 == 0


def test_settings_db_path_resolution() -> None:
    """Verify VINUM_DB_PATH resolves to an absolute SQLite URL for serverless/K8s."""
    default_settings = Settings()
    assert default_settings.effective_database_url.startswith("sqlite:///")

    lambda_settings = Settings(db_path="/tmp/vinum_pulse.db")
    assert lambda_settings.effective_database_url == "sqlite:////tmp/vinum_pulse.db"


def test_sqlite_schema_evolution_from_legacy_wines_table() -> None:
    """Verify init_db migrates a legacy SQLite schema lacking country/classification."""
    db_engine = create_db_engine("sqlite:///:memory:")
    with db_engine.begin() as conn:
        conn.execute(text("""
                CREATE TABLE wines (
                    id VARCHAR(128) PRIMARY KEY,
                    name VARCHAR(256),
                    winery VARCHAR(256),
                    appellation VARCHAR(128),
                    wine_type VARCHAR(32),
                    vintage INTEGER,
                    price_eur FLOAT,
                    serving_temp_c FLOAT,
                    decant_minutes INTEGER,
                    glass_type VARCHAR(64),
                    body FLOAT,
                    acidity FLOAT,
                    tannins FLOAT,
                    fruit FLOAT,
                    oak FLOAT,
                    tasting_notes TEXT
                )
                """))
        conn.execute(text("""
                INSERT INTO wines VALUES (
                    'vina-ardanza-reserva',
                    'Viña Ardanza Reserva',
                    'La Rioja Alta, S.A.',
                    'D.O.Ca. Rioja', 'Red', 2017, 34.0, 17.0, 30, 'Burdeos',
                    7.8, 7.0, 7.5, 8.0, 8.5, 'Legacy row'
                )
                """))

    factory = sessionmaker(
        bind=db_engine, autoflush=False, expire_on_commit=False, class_=Session
    )
    init_db(db_engine, factory)
    engine = SommelierEngine(session_factory=factory)

    all_wines = engine.get_wines(limit=300)
    assert len(all_wines) == 225
    ardanza = engine.get_wine_by_id("vina-ardanza-reserva")
    assert ardanza is not None
    assert ardanza.country == "España"
    assert ardanza.classification == "D.O.Ca."
    assert len(engine.get_dishes()) == 50
