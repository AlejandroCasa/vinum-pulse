"""Unit tests for SommelierEngine multi-vector pairing and enological catalog."""

import pytest

from app.planner import (
    compute_ambience_tip,
    compute_fridge_tip,
    compute_uncork_tip,
    compute_vintage_status,
)
from app.schemas import (
    DishPairingRequest,
    EveningMenuRequest,
    SensoryRadar,
    WineProfile,
    WineType,
)
from app.sommelier import CURATED_DISHES, CURATED_WINES, SommelierEngine


@pytest.fixture
def engine() -> SommelierEngine:
    """Fixture providing a fresh instance of SommelierEngine."""
    return SommelierEngine()


def test_catalog_initialization(engine: SommelierEngine) -> None:
    """Verify default catalog contains curated Spanish wines and dishes."""
    wines = engine.get_wines()
    dishes = engine.get_dishes()

    assert len(wines) == len(CURATED_WINES)
    assert len(dishes) == len(CURATED_DISHES)
    assert len(wines) >= 10
    assert len(dishes) == 22


def test_get_wine_by_id(engine: SommelierEngine) -> None:
    """Verify fetching existing and non-existing wines by slug."""
    wine = engine.get_wine_by_id("vina-ardanza-reserva")
    assert wine is not None
    assert wine.name == "Viña Ardanza Reserva"
    assert wine.appellation == "D.O.Ca. Rioja"
    assert wine.wine_type == WineType.RED

    non_existent = engine.get_wine_by_id("unknown-wine-slug")
    assert non_existent is None


def test_get_dish_by_id(engine: SommelierEngine) -> None:
    """Verify fetching existing and non-existing dishes by slug."""
    dish = engine.get_dish_by_id("chuleton-brasa")
    assert dish is not None
    assert dish.name == "Chuletón de vaca vieja a la brasa"
    assert dish.category == "Carnes y Caza"

    non_existent = engine.get_dish_by_id("non-existent-dish")
    assert non_existent is None


def test_filter_wines_by_appellation(engine: SommelierEngine) -> None:
    """Verify filtering wines by Designation of Origin."""
    rioja_wines = engine.get_wines(appellation="Rioja")
    assert len(rioja_wines) >= 2
    for w in rioja_wines:
        assert "Rioja" in w.appellation


def test_filter_wines_by_type(engine: SommelierEngine) -> None:
    """Verify filtering wines by enological type."""
    white_wines = engine.get_wines(wine_type=WineType.WHITE)
    assert len(white_wines) >= 2
    for w in white_wines:
        assert w.wine_type == WineType.WHITE


def test_filter_wines_by_max_price(engine: SommelierEngine) -> None:
    """Verify filtering wines strictly by price ceiling."""
    max_price = 25.0
    affordable = engine.get_wines(max_price=max_price)
    assert len(affordable) > 0
    for w in affordable:
        assert w.price_eur <= max_price


def test_get_regions_summary(engine: SommelierEngine) -> None:
    """Verify region aggregation returns sorted list of D.O. summaries."""
    regions = engine.get_regions()
    assert len(regions) > 0
    # Must be sorted descending by wine count
    counts = [r.wine_count for r in regions]
    assert counts == sorted(counts, reverse=True)
    # Check climate metadata
    for r in regions:
        assert len(r.climate_type) > 0
        assert r.wine_count > 0


def test_euclidean_distance_identical_profiles(engine: SommelierEngine) -> None:
    """Verify identical sensory profiles produce 0 distance and 100% compatibility."""
    profile = SensoryRadar(body=5.0, acidity=5.0, tannins=5.0, fruit=5.0, oak=5.0)
    dist = engine.compute_distance(profile, profile)
    score = engine.compute_compatibility_score(profile, profile)

    assert dist == pytest.approx(0.0)
    assert score == pytest.approx(100.0)


def test_euclidean_distance_maximum_divergence(engine: SommelierEngine) -> None:
    """Verify maximum opposite sensory profiles produce maximum distance and 0% score."""
    p1 = SensoryRadar(body=1.0, acidity=1.0, tannins=1.0, fruit=1.0, oak=1.0)
    p2 = SensoryRadar(body=10.0, acidity=10.0, tannins=10.0, fruit=10.0, oak=10.0)

    dist = engine.compute_distance(p1, p2)
    score = engine.compute_compatibility_score(p1, p2)

    assert dist == pytest.approx(engine.MAX_EUCLIDEAN_DISTANCE)
    assert score == pytest.approx(0.0)


def test_recommend_pairing_chuleton_success(engine: SommelierEngine) -> None:
    """Verify pairing recommendation for Chuletón selects a full-bodied red."""
    req = DishPairingRequest(
        dish_id="chuleton-brasa", max_budget_eur=60.0, preferred_type=WineType.RED
    )
    recommendation = engine.recommend_pairing(req)

    assert recommendation.dish_name == "Chuletón de vaca vieja a la brasa"
    assert recommendation.compatibility_score >= 80.0
    assert recommendation.primary_wine.wine_type == WineType.RED
    assert recommendation.primary_wine.price_eur <= 60.0
    explanation = recommendation.sommelier_explanation
    assert "%" not in explanation
    assert "/10" not in explanation
    assert "¿Por qué funciona?" in explanation
    assert "Consejo de servicio:" in explanation
    assert len(recommendation.alternative_wines) <= 2


def test_explanation_is_educational_and_omits_tannins_for_whites(
    engine: SommelierEngine,
) -> None:
    """Verify explanation avoids numeric scores and omits tannins for low-tannin whites."""
    req = DishPairingRequest(
        dish_id="cochinillo-asado", max_budget_eur=50.0, preferred_type=WineType.WHITE
    )
    rec = engine.recommend_pairing(req)
    explanation = rec.sommelier_explanation

    assert "%" not in explanation
    assert "/10" not in explanation
    assert "taninos" not in explanation.lower()
    assert "Consejo de servicio:" in explanation


def test_recommend_pairing_pulpo_recommends_white(
    engine: SommelierEngine,
) -> None:
    """Verify pairing recommendation for Pulpo á feira selects high-acidity white."""
    req = DishPairingRequest(
        dish_id="pulpo-feira", max_budget_eur=50.0, preferred_type=WineType.WHITE
    )
    rec = engine.recommend_pairing(req)

    assert rec.primary_wine.wine_type == WineType.WHITE
    assert rec.primary_wine.sensory.acidity >= 7.5
    assert rec.compatibility_score > 75.0


def test_recommend_pairing_unknown_dish_raises_value_error(
    engine: SommelierEngine,
) -> None:
    """Verify invalid dish ID raises descriptive ValueError."""
    req = DishPairingRequest(dish_id="unknown-dish-id", max_budget_eur=50.0)
    with pytest.raises(ValueError, match="not found"):
        engine.recommend_pairing(req)


def test_recommend_pairing_budget_too_low_raises_value_error(
    engine: SommelierEngine,
) -> None:
    """Verify budget lower than cheapest wine raises ValueError."""
    req = DishPairingRequest(dish_id="chuleton-brasa", max_budget_eur=5.0)
    with pytest.raises(ValueError, match="No wines found in cellar catalog"):
        engine.recommend_pairing(req)


def test_recommend_pairing_relaxes_type_filter_when_none_match(
    engine: SommelierEngine,
) -> None:
    """Verify that when no wines of preferred type fit budget, type constraint relaxes."""
    # Let's create an engine with a cheap white and expensive red
    cheap_white = WineProfile(
        id="cheap-white",
        name="Cheap White",
        winery="Test Winery",
        appellation="D.O. Rueda",
        wine_type=WineType.WHITE,
        vintage=2023,
        price_eur=10.0,
        serving_temp_c=10.0,
        decant_minutes=0,
        glass_type="Tulipa",
        sensory=SensoryRadar(body=4.0, acidity=7.0, tannins=1.0, fruit=7.0, oak=1.0),
        tasting_notes="Fresh",
    )
    expensive_red = WineProfile(
        id="expensive-red",
        name="Expensive Red",
        winery="Test Winery",
        appellation="D.O.Ca. Rioja",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=50.0,
        serving_temp_c=16.0,
        decant_minutes=15,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=8.0, acidity=6.0, tannins=8.0, fruit=8.0, oak=7.0),
        tasting_notes="Rich",
    )
    custom_engine = SommelierEngine(
        wines=[cheap_white, expensive_red], dishes=CURATED_DISHES
    )

    # Ask for RED with budget of 15 EUR (no red exists under 15 EUR, but white does)
    req = DishPairingRequest(
        dish_id="chuleton-brasa",
        max_budget_eur=15.0,
        preferred_type=WineType.RED,
    )
    rec = custom_engine.recommend_pairing(req)

    assert rec.primary_wine.id == "cheap-white"
    assert rec.primary_wine.price_eur <= 15.0


def test_db_backed_engine_pagination_search_and_pairing() -> None:
    """Verify SQLAlchemy-backed SommelierEngine seeding, pagination, search, and pairing."""
    from sqlalchemy.orm import Session, sessionmaker

    from app.database import create_db_engine
    from app.sommelier import init_db

    db_engine = create_db_engine("sqlite:///:memory:")
    factory = sessionmaker(
        bind=db_engine, autoflush=False, expire_on_commit=False, class_=Session
    )
    init_db(db_engine, factory)
    init_db(db_engine, factory)  # Verify idempotent seeding

    db_sommelier = SommelierEngine(session_factory=factory)

    page1 = db_sommelier.get_wines(limit=3, offset=0)
    page2 = db_sommelier.get_wines(limit=3, offset=3)
    assert len(page1) == 3
    assert len(page2) == 3
    assert {w.id for w in page1}.isdisjoint({w.id for w in page2})

    searched_wines = db_sommelier.get_wines(q="Ardanza")
    assert len(searched_wines) == 1
    assert searched_wines[0].id == "vina-ardanza-reserva"

    searched_dishes = db_sommelier.get_dishes(category="Carnes", q="Cochinillo")
    assert len(searched_dishes) == 1
    assert searched_dishes[0].id == "cochinillo-asado"

    assert db_sommelier.get_wine_by_id("vina-ardanza-reserva") is not None
    assert db_sommelier.get_wine_by_id("missing-wine") is None
    assert len(db_sommelier.get_regions()) >= 5

    rec = db_sommelier.recommend_pairing(
        DishPairingRequest(
            dish_id="chuleton-brasa", max_budget_eur=60.0, preferred_type=WineType.RED
        )
    )
    assert rec.primary_wine.wine_type == WineType.RED
    assert len(rec.alternative_wines) == 2

    with pytest.raises(ValueError, match="No wines found"):
        db_sommelier.recommend_pairing(
            DishPairingRequest(dish_id="chuleton-brasa", max_budget_eur=1.0)
        )


def test_atlas_geojson_generation() -> None:
    """Verify SommelierEngine.get_atlas_geojson produces valid RFC 7946 GeoJSON collections."""
    engine = SommelierEngine()

    # Wineries layer
    wineries_fc = engine.get_atlas_geojson(layer="wineries")
    assert wineries_fc.type == "FeatureCollection"
    assert len(wineries_fc.features) == 36
    all_appellations = {f.properties["appellation"] for f in wineries_fc.features}
    assert len(all_appellations) == 12

    # Regions layer
    regions_fc = engine.get_atlas_geojson(layer="regions")
    assert regions_fc.type == "FeatureCollection"
    assert len(regions_fc.features) == 12
    for feat in regions_fc.features:
        assert feat.properties["feature_type"] == "region"
        assert feat.properties["winery_count"] >= 1

    # All layer
    all_fc = engine.get_atlas_geojson(layer="all")
    assert len(all_fc.features) == 48


def test_gastronomic_sections_coverage() -> None:
    """Verify all 9 required gastronomic sections are present in catalog."""
    expected_sections = [
        "Entrantes y Cuchara",
        "Ensaladas y Huerta",
        "Tapas y Pintxos",
        "Embutidos y Quesos",
        "Pescados y Mariscos",
        "Arroces",
        "Carnes y Caza",
        "Postres y Dulces",
        "Platos Vegetarianos y Setas",
    ]
    catalog_categories = {d.category for d in CURATED_DISHES}
    for section in expected_sections:
        assert section in catalog_categories
        matching = [d for d in CURATED_DISHES if d.category == section]
        assert len(matching) >= 2


def test_wine_profile_bottle_silhouette_detection() -> None:
    """Verify automatic bottle silhouette deduction based on wine type and terroir."""
    w_fortified = WineProfile(
        id="t-jerez",
        name="Tío Pepe",
        winery="González Byass",
        appellation="D.O. Jerez-Xérès-Sherry",
        wine_type=WineType.FORTIFIED,
        vintage=2020,
        price_eur=12.0,
        serving_temp_c=8.0,
        glass_type="Copita",
        sensory=SensoryRadar(body=5.0, acidity=7.0, tannins=1.0, fruit=5.0, oak=6.0),
        tasting_notes="Salino y almendrado.",
    )
    assert w_fortified.bottle_silhouette == "Jerezana"

    w_sparkling = WineProfile(
        id="t-cava",
        name="Cava Brut",
        winery="Gramona",
        appellation="D.O. Corpinnat / Penedès",
        wine_type=WineType.SPARKLING,
        vintage=2019,
        price_eur=25.0,
        serving_temp_c=8.0,
        glass_type="Tulipa",
        sensory=SensoryRadar(body=5.0, acidity=8.0, tannins=1.0, fruit=6.0, oak=4.0),
        tasting_notes="Burbuja fina y notas de levadura.",
    )
    assert w_sparkling.bottle_silhouette == "Espumosa"

    w_bierzo = WineProfile(
        id="t-bierzo",
        name="Pétalos del Bierzo",
        winery="Descendientes de J. Palacios",
        appellation="D.O. Bierzo",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=20.0,
        serving_temp_c=15.0,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.5, acidity=7.0, tannins=6.0, fruit=8.0, oak=5.0),
        tasting_notes="Fragancia de violetas y pizarra.",
    )
    assert w_bierzo.bottle_silhouette == "Borgoña"

    w_rioja = WineProfile(
        id="t-rioja",
        name="Rioja Crianza",
        winery="Bodega Riojana",
        appellation="D.O.Ca. Rioja",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=15.0,
        serving_temp_c=16.0,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=7.0, acidity=6.5, tannins=7.0, fruit=7.5, oak=6.5),
        tasting_notes="Vainilla y fruta madura.",
    )
    assert w_rioja.bottle_silhouette == "Bordelesa"

    w_custom = WineProfile(
        id="t-custom",
        name="Custom Label",
        winery="Bodega Custom",
        appellation="D.O.Ca. Rioja",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=15.0,
        serving_temp_c=16.0,
        glass_type="Burdeos",
        bottle_silhouette="Jerezana",
        sensory=SensoryRadar(body=7.0, acidity=6.5, tannins=7.0, fruit=7.5, oak=6.5),
        tasting_notes="Personalizado.",
    )
    assert w_custom.bottle_silhouette == "Jerezana"


def test_plan_evening_menu_success(engine: SommelierEngine) -> None:
    """Verify evening menu plan produces 3 distinct wines within budget."""
    req = EveningMenuRequest(
        occasion="Cena Romántica",
        starter_dish_id="salmorejo-cordobes",
        main_dish_id="chuleton-brasa",
        dessert_dish_id="tarta-queso-idiazabal",
        total_budget_eur=120.0,
    )
    plan = engine.plan_evening_menu(req)

    assert plan.occasion == "Cena Romántica"
    assert len(plan.courses) == 3
    assert plan.total_price_eur <= 120.0
    assert len({c.wine.id for c in plan.courses}) == 3
    assert plan.printable_card_title == "Menú Maridaje Sommelier · Cena Romántica"
    assert len(plan.occasion_ambience_tip) > 10
    assert len(plan.progression_summary) > 10
    assert plan.average_compatibility_score > 0.0

    for i, course in enumerate(plan.courses, start=1):
        assert course.course_number == i
        assert len(course.course_title) > 0
        assert len(course.fridge_tip) > 5
        assert len(course.uncork_tip) > 5
        assert course.vintage_semaphore in ("green", "amber", "gold")
        assert len(course.vintage_status_label) > 5
        assert len(course.sommelier_note) > 5


def test_plan_evening_menu_unknown_dish_raises(engine: SommelierEngine) -> None:
    """Verify unknown dish slug raises descriptive ValueError."""
    req = EveningMenuRequest(
        starter_dish_id="unknown-dish-slug",
        main_dish_id="chuleton-brasa",
        dessert_dish_id="tarta-queso-idiazabal",
    )
    with pytest.raises(ValueError, match="not found in gastronomic catalog"):
        engine.plan_evening_menu(req)


def test_plan_evening_menu_insufficient_budget_raises(
    engine: SommelierEngine,
) -> None:
    """Verify insufficient budget raises descriptive ValueError."""
    req = EveningMenuRequest(
        starter_dish_id="salmorejo-cordobes",
        main_dish_id="chuleton-brasa",
        dessert_dish_id="tarta-queso-idiazabal",
        total_budget_eur=10.0,
    )
    with pytest.raises(
        ValueError, match="insufficient for a 3-bottle evening menu plan"
    ):
        engine.plan_evening_menu(req)


def test_planner_helper_functions() -> None:
    """Verify fridge, uncork, vintage semaphore, and ambience helper logic."""
    test_wine = WineProfile(
        id="t-wine",
        name="Vino Test",
        winery="Bodega Test",
        appellation="D.O.Ca. Rioja",
        wine_type=WineType.RED,
        vintage=2024,
        price_eur=18.0,
        serving_temp_c=8.0,
        decant_minutes=60,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=7.0, acidity=7.0, tannins=7.0, fruit=7.0, oak=7.0),
        tasting_notes="Prueba",
        aging_potential_years=4,
    )

    # Fridge tip branches
    tip_cold = compute_fridge_tip(test_wine)
    assert "90 min" in tip_cold

    test_wine.serving_temp_c = 12.0
    assert "45 min" in compute_fridge_tip(test_wine)

    test_wine.serving_temp_c = 15.0
    assert "20 min" in compute_fridge_tip(test_wine)

    test_wine.serving_temp_c = 18.0
    assert "15 min" in compute_fridge_tip(test_wine)

    # Uncork tip branches
    test_wine.decant_minutes = 45
    assert "decantar 45 min" in compute_uncork_tip(test_wine)

    test_wine.decant_minutes = 15
    assert "Descorchar 15 min" in compute_uncork_tip(test_wine)

    test_wine.decant_minutes = 0
    test_wine.wine_type = WineType.SPARKLING
    assert "burbuja fina" in compute_uncork_tip(test_wine)

    test_wine.wine_type = WineType.RED
    assert "directamente al momento" in compute_uncork_tip(test_wine)

    # Vintage status branches
    test_wine.vintage = 2020
    test_wine.aging_potential_years = 20
    sem_gold, label_gold = compute_vintage_status(test_wine, current_year=2026)
    assert sem_gold == "gold"
    assert "Gran Reserva" in label_gold

    test_wine.vintage = 2025
    test_wine.aging_potential_years = 4
    sem_young, label_young = compute_vintage_status(test_wine, current_year=2026)
    assert sem_young == "green"
    assert "Joven y vibrante" in label_young

    test_wine.vintage = 2020
    test_wine.aging_potential_years = 8
    sem_peak, label_peak = compute_vintage_status(test_wine, current_year=2026)
    assert sem_peak == "green"
    assert "En su cumbre" in label_peak

    test_wine.vintage = 2010
    test_wine.aging_potential_years = 5
    sem_amber, label_amber = compute_vintage_status(test_wine, current_year=2026)
    assert sem_amber == "amber"
    assert "evolucionado" in label_amber

    # Ambience tip branches
    tip_romantic = compute_ambience_tip("Cena Romántica")
    assert "romántica" in tip_romantic.lower() or "copas" in tip_romantic
    assert "cubitera" in compute_ambience_tip("Barbacoa con amigos")
    assert "mantel de lino" in compute_ambience_tip("Comida Familiar de Domingo")
    assert "pintxos" in compute_ambience_tip("Tardeo & Tapas Gourmet")
    assert "Ambiente relajado" in compute_ambience_tip("Evento Especial")
    assert "pintxos" in compute_ambience_tip("Tardeo & Tapas Gourmet")
    assert "Ambiente relajado" in compute_ambience_tip("Evento Especial")
