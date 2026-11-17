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
    """Verify /api/v1/dishes returns gastronomic catalog across 9 sections."""
    response = client.get("/api/v1/dishes")
    assert response.status_code == 200
    dishes = response.json()
    assert len(dishes) == 22
    sample = dishes[0]
    assert "id" in sample
    assert "target_sensory" in sample
    assert "body" in sample["target_sensory"]
    categories = {d["category"] for d in dishes}
    assert len(categories) == 9


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


def test_atlas_geojson_endpoint_wineries() -> None:
    """Verify /api/v1/atlas/geojson returns valid GeoJSON for 36 wineries."""
    response = client.get("/api/v1/atlas/geojson")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    features = data["features"]
    assert len(features) == 36

    # Verify all 12 D.O.s are represented
    appellations = {f["properties"]["appellation"] for f in features}
    assert len(appellations) == 12
    assert "D.O.Ca. Rioja" in appellations
    assert "D.O. Ribera del Duero" in appellations
    assert "D.O.Q. Priorat" in appellations
    assert "D.O. Rías Baixas" in appellations

    # Validate GeoJSON schema, coordinates and terroir properties
    for feat in features:
        assert feat["type"] == "Feature"
        assert feat["geometry"]["type"] == "Point"
        coords = feat["geometry"]["coordinates"]
        assert len(coords) == 2
        lon, lat = coords
        assert -10.0 <= lon <= 5.0
        assert 35.0 <= lat <= 45.0
        p = feat["properties"]
        assert p["feature_type"] == "winery"
        assert "winery" in p
        assert "name" in p
        assert "appellation" in p
        assert "autonomous_community" in p
        assert "climate" in p
        assert "soil" in p
        assert "altitude_m" in p
        assert "signature_grape" in p
        assert "winery_catalog_summary" in p
        assert "sensory" in p


def test_atlas_geojson_endpoint_layers() -> None:
    """Verify /api/v1/atlas/geojson layers param (regions and all)."""
    # Regions layer
    reg_res = client.get("/api/v1/atlas/geojson", params={"layer": "regions"})
    assert reg_res.status_code == 200
    reg_data = reg_res.json()
    assert reg_data["type"] == "FeatureCollection"
    assert len(reg_data["features"]) == 12
    for feat in reg_data["features"]:
        assert feat["properties"]["feature_type"] == "region"
        assert "wineries" in feat["properties"]
        assert "winery_count" in feat["properties"]

    # All layer
    all_res = client.get("/api/v1/atlas/geojson", params={"layer": "all"})
    assert all_res.status_code == 200
    all_data = all_res.json()
    assert len(all_data["features"]) == 48


def test_dashboard_ui_atlas_integration() -> None:
    """Verify GET / dashboard embeds Leaflet and Atlas cartographic elements."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "leaflet.css" in html
    assert "leaflet.js" in html
    assert "Atlas Cartográfico de Terroirs" in html
    assert 'id="atlas-map"' in html
    assert 'id="atlas-svg-fallback"' in html
    assert 'id="terroir-card"' in html
    assert 'id="do-pills-bar"' in html
    assert "/api/v1/atlas/geojson" in html


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


# --- Evening Menu Planner & W47 UX Tests ---


def test_plan_evening_menu_endpoint_success() -> None:
    """Verify POST /api/v1/pairings/menu-plan returns 3-course sommelier progression."""
    payload = {
        "occasion": "Cena Romántica",
        "starter_dish_id": "salmorejo-cordobes",
        "main_dish_id": "chuleton-brasa",
        "dessert_dish_id": "tarta-queso-idiazabal",
        "total_budget_eur": 120.0,
    }
    response = client.post("/api/v1/pairings/menu-plan", json=payload)
    assert response.status_code == 200
    plan = response.json()
    assert plan["occasion"] == "Cena Romántica"
    assert plan["total_budget_eur"] == 120.0
    assert plan["total_price_eur"] <= 120.0
    assert len(plan["courses"]) == 3
    wine_ids = {c["wine"]["id"] for c in plan["courses"]}
    assert len(wine_ids) == 3
    for course in plan["courses"]:
        assert "fridge_tip" in course
        assert "uncork_tip" in course
        assert course["vintage_semaphore"] in ("green", "amber", "gold")
        assert len(course["vintage_status_label"]) > 5


def test_plan_evening_menu_endpoint_errors() -> None:
    """Verify POST /api/v1/pairings/menu-plan returns 404 on invalid input."""
    bad_dish_payload = {
        "occasion": "Barbacoa con Amigos",
        "starter_dish_id": "plato-inexistente",
        "main_dish_id": "chuleton-brasa",
        "dessert_dish_id": "queso-manchego",
        "total_budget_eur": 100.0,
    }
    res_dish = client.post("/api/v1/pairings/menu-plan", json=bad_dish_payload)
    assert res_dish.status_code == 404
    assert "not found" in res_dish.json()["detail"]

    low_budget_payload = {
        "occasion": "Barbacoa con Amigos",
        "starter_dish_id": "salmorejo-cordobes",
        "main_dish_id": "chuleton-brasa",
        "dessert_dish_id": "queso-manchego",
        "total_budget_eur": 10.0,
    }
    res_budget = client.post("/api/v1/pairings/menu-plan", json=low_budget_payload)
    assert res_budget.status_code == 404
    assert "insufficient" in res_budget.json()["detail"].lower()


def test_dashboard_ui_w47_components() -> None:
    """Verify GET / embeds accordion, bottle SVG, tagline, and evening planner."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert 'id="active-dish-chip"' in html
    assert 'id="res-tagline"' in html
    assert 'id="btn-toggle-tasting-notes"' in html
    assert 'id="res-bottle-visual"' in html
    assert 'id="res-bottle-svg-container"' in html
    assert 'id="evening-planner-section"' in html
    assert 'id="printable-menu-card"' in html
    assert "@media print" in html
    assert "/api/v1/pairings/menu-plan" in html


def test_dashboard_ui_tabbed_workspace_navigation() -> None:
    """Verify GET / renders sticky header KPIs and 4-tab SPA workspace."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    assert 'id="app-header"' in html
    assert 'id="global-kpis"' in html
    assert 'id="kpi-wines-count"' in html
    assert 'id="kpi-regions-count"' in html
    assert 'id="kpi-cellar-pill"' in html

    assert 'id="workspace-tablist"' in html
    assert 'role="tablist"' in html
    for tab_id in ("atlas", "carte", "veladas", "bodega"):
        assert f'id="tab-btn-{tab_id}"' in html
        assert f'aria-controls="panel-{tab_id}"' in html
        assert f'id="panel-{tab_id}"' in html
        assert f'aria-labelledby="tab-btn-{tab_id}"' in html
    assert html.count('role="tab"') >= 4
    assert html.count('role="tabpanel"') == 4


def test_dashboard_ui_deep_linking_and_canvas_lifecycle() -> None:
    """Verify URL hash deep linking, keyboard nav, and map/radar resize lifecycle."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    assert 'const VALID_TABS = ["atlas", "carte", "veladas", "bodega"]' in html
    assert "function switchTab(tabId, updateHash = true)" in html
    assert 'window.addEventListener("hashchange"' in html
    assert "resolveTabFromHash" in html
    assert "atlasMap.invalidateSize()" in html
    assert "radarChart.resize()" in html
    assert "ArrowRight" in html
    assert "ArrowLeft" in html


def test_dashboard_ui_contextual_bridges_and_cellar_workspace() -> None:
    """Verify contextual cross-tab bridges, catalog filters, toast, and cellar UI."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # Atlas layer toggles & integrated 5D radar
    assert 'id="atlas-layer-bar"' in html
    assert 'data-layer="wineries"' in html
    assert 'data-layer="regions"' in html
    assert 'data-layer="all"' in html
    assert 'id="atlas-radar-panel"' in html
    assert 'id="atlasRadarChart"' in html

    # Contextual bridges across Atlas, La Carte, Veladas, and Mi Bodega
    assert 'id="btn-atlas-to-carte"' in html
    assert 'id="btn-atlas-to-bodega"' in html
    assert 'id="btn-pairing-add-cellar"' in html
    assert 'id="btn-pairing-plan-velada"' in html
    assert 'id="btn-pairing-view-atlas"' in html
    assert 'id="btn-add-trio-cellar"' in html

    # Searchable catalog, progression curve, cellar analytics/CRUD & toast container
    assert 'id="catalog-search-input"' in html
    assert 'id="catalog-do-filter"' in html
    assert 'id="catalog-wines-grid"' in html
    assert 'id="progressionChart"' in html
    assert 'id="cellar-analytics-grid"' in html
    assert 'id="cellar-add-form"' in html
    assert 'id="cellar-inventory-list"' in html
    assert 'id="toast-container"' in html
    assert "showToast(" in html
