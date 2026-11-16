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
    """Verify /api/v1/wines returns full wine list with terroir metadata."""
    response = client.get("/api/v1/wines")
    assert response.status_code == 200
    wines = response.json()
    assert isinstance(wines, list)
    assert len(wines) >= 35
    sample = wines[0]
    assert "id" in sample
    assert "name" in sample
    assert "sensory" in sample
    assert "latitude" in sample
    assert "longitude" in sample
    assert "altitude_m" in sample
    assert "soil_type" in sample
    assert "climate" in sample
    assert "tagline" in sample


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
    assert len(dishes) == 12
    sample = dishes[0]
    assert "id" in sample
    assert "target_sensory" in sample
    assert "body" in sample["target_sensory"]


def test_list_regions_endpoint() -> None:
    """Verify /api/v1/regions returns D.O. summaries across all 12 regions."""
    response = client.get("/api/v1/regions")
    assert response.status_code == 200
    regions = response.json()
    assert len(regions) >= 12
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
        "preferred_type": "Red",
    }
    response = client.post("/api/v1/pairings/recommend", json=payload)
    assert response.status_code == 404
    assert "budget" in response.json()["detail"].lower()


def test_dashboard_ui_endpoint() -> None:
    """Verify GET / returns HTML dashboard with UTF-8 encoding."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Vinum Pulse" in response.text


# --- Personal Cellar Tests ---


def test_cellar_lifecycle_crud() -> None:
    """Verify adding, listing, and deleting bottles from personal cellar."""
    # 1. Add bottle to cellar
    payload = {
        "wine_id": "vina-ardanza-reserva",
        "quantity": 3,
        "purchase_price_eur": 32.5,
        "storage_location": "Armario Climatizado Balda 2",
        "notes": "Compradas en avanzada para descorchar en 2028.",
    }
    create_res = client.post("/api/v1/cellar", json=payload)
    assert create_res.status_code == 200
    item = create_res.json()
    assert item["wine_id"] == "vina-ardanza-reserva"
    assert item["quantity"] == 3
    assert item["purchase_price_eur"] == 32.5
    assert item["wine"] is not None
    assert item["wine"]["name"] == "Viña Ardanza Reserva"
    item_id = item["id"]

    # 2. List cellar
    list_res = client.get("/api/v1/cellar")
    assert list_res.status_code == 200
    items = list_res.json()
    assert any(i["id"] == item_id for i in items)

    # 3. Decrement quantity (remove 1 bottle)
    dec_res = client.delete(f"/api/v1/cellar/{item_id}?quantity=1")
    assert dec_res.status_code == 200
    assert dec_res.json()["remaining"] == 2

    # 4. Remove remaining bottles (delete)
    del_res = client.delete(f"/api/v1/cellar/{item_id}?quantity=2")
    assert del_res.status_code == 200
    assert del_res.json()["remaining"] == 0

    # 5. Delete non-existent item returns 404
    err_res = client.delete(f"/api/v1/cellar/{item_id}")
    assert err_res.status_code == 404


def test_cellar_add_invalid_wine_returns_404() -> None:
    """Verify adding non-existent wine to cellar returns 404 error."""
    payload = {
        "wine_id": "vino-inexistente-123",
        "quantity": 1,
    }
    response = client.post("/api/v1/cellar", json=payload)
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]
