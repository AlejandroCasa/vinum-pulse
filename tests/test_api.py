"""Integration tests for Vinum Pulse FastAPI endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Verify /healthz returns 200 OK for Kubernetes probes."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_wines_endpoint() -> None:
    """Verify /api/v1/wines returns full wine list."""
    response = client.get("/api/v1/wines")
    assert response.status_code == 200
    wines = response.json()
    assert isinstance(wines, list)
    assert len(wines) >= 10
    sample = wines[0]
    assert "id" in sample
    assert "name" in sample
    assert "sensory" in sample


def test_list_wines_with_query_params() -> None:
    """Verify /api/v1/wines respects query filters."""
    response = client.get(
        "/api/v1/wines",
        params={"appellation": "Rioja", "wine_type": "Red", "max_price": 40.0},
    )
    assert response.status_code == 200
    wines = response.json()
    assert len(wines) >= 1
    for w in wines:
        assert "Rioja" in w["appellation"]
        assert w["wine_type"] == "Red"
        assert w["price_eur"] <= 40.0


def test_list_dishes_endpoint() -> None:
    """Verify /api/v1/dishes returns gastronomic catalog with 5D targets."""
    response = client.get("/api/v1/dishes")
    assert response.status_code == 200
    dishes = response.json()
    assert len(dishes) >= 6
    sample = dishes[0]
    assert "id" in sample
    assert "target_sensory" in sample
    assert "body" in sample["target_sensory"]


def test_list_regions_endpoint() -> None:
    """Verify /api/v1/regions returns aggregated D.O. summaries."""
    response = client.get("/api/v1/regions")
    assert response.status_code == 200
    regions = response.json()
    assert len(regions) >= 5
    sample = regions[0]
    assert "appellation" in sample
    assert "wine_count" in sample
    assert "climate_type" in sample


def test_recommend_pairing_endpoint_success() -> None:
    """Verify POST /api/v1/pairings/recommend returns valid pairing recommendation."""
    payload = {
        "dish_id": "chuleton-brasa",
        "max_budget_eur": 50.0,
        "preferred_type": "Red",
    }
    response = client.post("/api/v1/pairings/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["dish_name"] == "Chuletón de vaca vieja a la brasa"
    assert data["compatibility_score"] > 80.0
    assert "primary_wine" in data
    assert data["primary_wine"]["price_eur"] <= 50.0
    assert "sommelier_explanation" in data
    assert len(data["sommelier_explanation"]) > 20


def test_recommend_pairing_endpoint_not_found_dish() -> None:
    """Verify 404 response when querying invalid dish ID."""
    payload = {
        "dish_id": "non-existent-paella",
        "max_budget_eur": 50.0,
    }
    response = client.post("/api/v1/pairings/recommend", json=payload)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_recommend_pairing_endpoint_budget_too_low() -> None:
    """Verify 404 response when budget is below any available wine."""
    payload = {
        "dish_id": "chuleton-brasa",
        "max_budget_eur": 2.0,
    }
    response = client.post("/api/v1/pairings/recommend", json=payload)
    assert response.status_code == 404
    assert "No wines found" in response.json()["detail"]


def test_get_dashboard_serves_html() -> None:
    """Verify GET / returns interactive HTML single page dashboard."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html = response.text
    assert "Vinum Pulse" in html
    assert "Radar de Cata" in html
    assert "radarChart" in html
    assert "budget-slider" in html


def test_list_wines_pagination_and_search() -> None:
    """Verify /api/v1/wines supports limit, offset, and text search q."""
    p1 = client.get("/api/v1/wines", params={"limit": 2, "offset": 0})
    p2 = client.get("/api/v1/wines", params={"limit": 2, "offset": 2})
    assert p1.status_code == 200
    assert p2.status_code == 200
    assert len(p1.json()) == 2
    assert len(p2.json()) == 2
    assert p1.json()[0]["id"] != p2.json()[0]["id"]

    search = client.get("/api/v1/wines", params={"q": "Belondrade"})
    assert search.status_code == 200
    assert len(search.json()) == 1
    assert search.json()[0]["id"] == "belondrade-lurton"


def test_list_dishes_pagination_and_search() -> None:
    """Verify /api/v1/dishes supports category, q, limit, and offset."""
    p1 = client.get("/api/v1/dishes", params={"limit": 2, "offset": 0})
    assert p1.status_code == 200
    assert len(p1.json()) == 2

    search = client.get(
        "/api/v1/dishes", params={"category": "Carnes", "q": "Cochinillo"}
    )
    assert search.status_code == 200
    assert len(search.json()) == 1
    assert search.json()[0]["id"] == "cochinillo-asado"
