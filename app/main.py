"""FastAPI web service, Sommelier API, and interactive sensory dashboard."""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import HTMLResponse

from app.schemas import (
    Dish,
    DishPairingRequest,
    PairingRecommendation,
    RegionSummary,
    WineProfile,
    WineType,
)
from app.sommelier import SommelierEngine
from app.ui import DASHBOARD_HTML

app = FastAPI(
    title="Vinum Pulse",
    description=(
        "Real-Time Sommelier Radar, Gastronomic Pairing Engine, and "
        "Cellar Analytics Platform."
    ),
    version="0.1.0",
)

sommelier = SommelierEngine()


@app.get("/healthz", tags=["Health"])
def health_check() -> dict[str, str]:
    """Health check endpoint for Kubernetes liveness and readiness probes."""
    return {"status": "ok"}


@app.get("/api/v1/wines", response_model=list[WineProfile], tags=["Catalog"])
def list_wines(
    appellation: str | None = Query(
        default=None, description="Filter by Designation of Origin"
    ),
    wine_type: WineType | None = Query(
        default=None, description="Filter by wine type (Red, White, etc.)"
    ),
    max_price: float | None = Query(
        default=None, gt=0, description="Maximum bottle price in EUR"
    ),
) -> list[WineProfile]:
    """Return cataloged wines with optional filtering."""
    return sommelier.get_wines(
        appellation=appellation, wine_type=wine_type, max_price=max_price
    )


@app.get("/api/v1/dishes", response_model=list[Dish], tags=["Catalog"])
def list_dishes() -> list[Dish]:
    """Return all cataloged dishes and their 5D target sensory profiles."""
    return sommelier.get_dishes()


@app.get("/api/v1/regions", response_model=list[RegionSummary], tags=["Catalog"])
def list_regions() -> list[RegionSummary]:
    """Return list of featured Spanish wine regions and wine counts."""
    return sommelier.get_regions()


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


@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def get_dashboard() -> HTMLResponse:
    """Serve the interactive single-page sommelier dashboard."""
    return HTMLResponse(content=DASHBOARD_HTML)
