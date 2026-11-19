"""FastAPI web service, Sommelier API, and interactive sensory dashboard."""

from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import HTMLResponse

from app.database import SessionLocal, engine, settings
from app.schemas import (
    CellarCreateRequest,
    CellarItem,
    Dish,
    DishPairingRequest,
    EveningMenuPlan,
    EveningMenuRequest,
    GeoJsonFeatureCollection,
    PairingRecommendation,
    RegionSummary,
    WineProfile,
    WineType,
)
from app.security import (
    BodySizeLimitMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    TokenBucketRateLimiter,
)
from app.sommelier import SommelierEngine, init_db
from app.ui import DASHBOARD_HTML

app = FastAPI(
    title="Vinum Pulse",
    description=(
        "European Real-Time Sommelier Radar, Dynamic Geo-Atlas (200 Wines, "
        "4 Countries), Gastronomic Pairing Engine, and Cellar Analytics Platform."
    ),
    version="0.3.0",
)

rate_limiter = TokenBucketRateLimiter(
    capacity=settings.rate_limit_capacity,
    refill_per_sec=settings.rate_limit_refill_per_sec,
    enabled=settings.rate_limit_enabled,
)

# Register perimeter security middlewares (outermost runs first)
app.add_middleware(RateLimitMiddleware, limiter=rate_limiter)
app.add_middleware(BodySizeLimitMiddleware, max_body_bytes=settings.max_body_bytes)
app.add_middleware(SecurityHeadersMiddleware)

init_db(engine, SessionLocal)
sommelier = SommelierEngine(session_factory=SessionLocal)


@app.get("/healthz", tags=["Health"])
def health_check() -> dict[str, str]:
    """Health check endpoint for Kubernetes liveness and readiness probes."""
    return {"status": "ok"}


@app.get("/api/v1/wines", response_model=list[WineProfile], tags=["Catalog"])
def list_wines(
    appellation: str | None = Query(
        default=None, description="Filter by Designation of Origin"
    ),
    country: str | None = Query(
        default=None,
        description="Filter by country (España, Francia, Italia, Inglaterra)",
    ),
    wine_type: WineType | None = Query(
        default=None, description="Filter by wine type (Red, White, etc.)"
    ),
    max_price: float | None = Query(
        default=None, gt=0, description="Maximum bottle price in EUR"
    ),
    q: str | None = Query(
        default=None,
        description="Search by wine name, winery, appellation, or country",
    ),
    limit: int = Query(
        default=250, ge=1, le=500, description="Maximum number of items to return"
    ),
    offset: int = Query(
        default=0, ge=0, description="Number of items to skip for pagination"
    ),
) -> list[WineProfile]:
    """Return cataloged wines with optional filtering and pagination."""
    return sommelier.get_wines(
        appellation=appellation,
        country=country,
        wine_type=wine_type,
        max_price=max_price,
        q=q,
        limit=limit,
        offset=offset,
    )


@app.get("/api/v1/dishes", response_model=list[Dish], tags=["Catalog"])
def list_dishes(
    category: str | None = Query(
        default=None, description="Filter by culinary category"
    ),
    q: str | None = Query(
        default=None, description="Search by dish name or description"
    ),
    limit: int = Query(
        default=100, ge=1, le=500, description="Maximum number of items to return"
    ),
    offset: int = Query(
        default=0, ge=0, description="Number of items to skip for pagination"
    ),
) -> list[Dish]:
    """Return cataloged dishes with optional filtering and pagination."""
    return sommelier.get_dishes(category=category, q=q, limit=limit, offset=offset)


@app.get("/api/v1/regions", response_model=list[RegionSummary], tags=["Catalog"])
def list_regions(
    country: str | None = Query(
        default=None,
        description="Optional country filter (España, Francia, Italia, Inglaterra)",
    ),
) -> list[RegionSummary]:
    """Return list of featured European wine regions and wine counts."""
    return sommelier.get_regions(country=country)


@app.get(
    "/api/v1/atlas/geojson",
    response_model=GeoJsonFeatureCollection,
    tags=["Atlas"],
)
def get_atlas_geojson(
    layer: str = Query(
        default="wineries",
        description=(
            "Feature layer: 'wineries' (200 curated wineries across 32 appellations), "
            "'regions' (32 European region centroids), or 'all' (both)."
        ),
    ),
    country: str | None = Query(
        default=None,
        description="Optional country filter (España, Francia, Italia, Inglaterra)",
    ),
) -> GeoJsonFeatureCollection:
    """Return deterministic GeoJSON FeatureCollection of wine regions/wineries."""
    return sommelier.get_atlas_geojson(layer=layer, country=country)


@app.post(
    "/api/v1/pairings/recommend",
    response_model=PairingRecommendation,
    tags=["Pairing Engine"],
)
def recommend_pairing(request: DishPairingRequest) -> PairingRecommendation:
    """Evaluate multi-vector sensory similarity and recommend optimal pairings."""
    dish = sommelier.get_dish_by_id(request.dish_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish '{request.dish_id}' not found in gastronomic catalog.",
        )
    try:
        return sommelier.recommend_pairing(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@app.post(
    "/api/v1/pairings/menu-plan",
    response_model=EveningMenuPlan,
    tags=["Pairing Engine"],
)
def plan_evening_menu(request: EveningMenuRequest) -> EveningMenuPlan:
    """Design a 3-course evening wine progression within a global budget."""
    try:
        return sommelier.plan_evening_menu(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# --- Personal Cellar Endpoints ---


@app.get("/api/v1/cellar", response_model=list[CellarItem], tags=["Cellar"])
def list_cellar(user_id: str = "sommelier") -> list[CellarItem]:
    """Retrieve all bottles stored in user's personal cellar."""
    return sommelier.get_cellar(user_id=user_id)


@app.post("/api/v1/cellar", response_model=CellarItem, tags=["Cellar"])
def add_to_cellar(
    payload: CellarCreateRequest, user_id: str = "sommelier"
) -> CellarItem:
    """Add or increment wine bottles in personal cellar."""
    try:
        return sommelier.add_to_cellar(payload=payload, user_id=user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@app.delete("/api/v1/cellar/{item_id}", tags=["Cellar"])
def remove_from_cellar(
    item_id: str,
    quantity: int = Query(default=1, ge=1),
    user_id: str = "sommelier",
) -> dict[str, Any]:
    """Decrement stock or delete bottle record from personal cellar."""
    try:
        return sommelier.remove_from_cellar(
            item_id=item_id, user_id=user_id, quantity=quantity
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def get_dashboard() -> HTMLResponse:
    """Serve the interactive single-page sommelier dashboard."""
    return HTMLResponse(content=DASHBOARD_HTML)
