"""Unit tests for SommelierEngine multi-vector pairing and enological catalog."""

import pytest

from app.schemas import (
    DishPairingRequest,
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
    assert len(dishes) >= 6


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
    assert dish.category == "Carnes"

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
