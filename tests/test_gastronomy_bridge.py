"""Unit tests for the Vinum Pulse <-> Mise en Place MD PostgreSQL bridge."""

from __future__ import annotations

from app.catalog import CURATED_DISHES, CURATED_WINES
from app.gastronomy_bridge import GastronomyPostgresBridge, build_recipe_url
from app.schemas import DishPairingRequest
from app.sommelier import SommelierEngine


class _StubBridge(GastronomyPostgresBridge):
    """In-memory stub returning deterministic dish-to-recipe links."""

    def __init__(self, links: dict[str, str], base_url: str) -> None:
        super().__init__(pg_url=None, mise_en_place_base_url=base_url)
        self._links = links

    @property
    def enabled(self) -> bool:
        return True

    def fetch_dish_recipe_links(self) -> dict[str, str]:
        return dict(self._links)


def test_build_recipe_url() -> None:
    """Deep-link URL composes cleanly without double slashes."""
    assert (
        build_recipe_url("http://127.0.0.1:8001/", "arroz-meloso-carrillera-setas")
        == "http://127.0.0.1:8001/recipes/arroz-meloso-carrillera-setas"
    )
    assert build_recipe_url("http://127.0.0.1:8001", None) is None


def test_disabled_bridge_is_noop() -> None:
    """Unconfigured bridge does not fail and returns empty link maps."""
    bridge = GastronomyPostgresBridge(
        pg_url=None,
        mise_en_place_base_url="http://127.0.0.1:8001",
    )
    assert bridge.enabled is False
    assert bridge.sync_catalog(CURATED_WINES[:1], CURATED_DISHES[:1]) == 0
    assert bridge.fetch_dish_recipe_links() == {}


def test_sommelier_attaches_recipe_links_to_dishes_and_recommendations() -> None:
    """Dishes and pairing recommendations include Mise en Place MD deep links."""
    sample_dish = CURATED_DISHES[0]
    bridge = _StubBridge(
        links={sample_dish.id: "arroz-meloso-carrillera-setas"},
        base_url="http://127.0.0.1:8001",
    )
    engine = SommelierEngine(
        wines=CURATED_WINES,
        dishes=CURATED_DISHES,
        gastronomy_bridge=bridge,
    )

    fetched = engine.get_dish_by_id(sample_dish.id)
    assert fetched is not None
    assert fetched.recipe_slug == "arroz-meloso-carrillera-setas"
    assert (
        fetched.recipe_url
        == "http://127.0.0.1:8001/recipes/arroz-meloso-carrillera-setas"
    )

    dishes = engine.get_dishes(limit=100)
    matched = [d for d in dishes if d.id == sample_dish.id]
    assert len(matched) == 1
    assert matched[0].recipe_slug == "arroz-meloso-carrillera-setas"

    rec = engine.recommend_pairing(
        DishPairingRequest(dish_id=sample_dish.id, max_budget_eur=80.0)
    )
    assert rec.dish_recipe_slug == "arroz-meloso-carrillera-setas"
    assert (
        rec.dish_recipe_url
        == "http://127.0.0.1:8001/recipes/arroz-meloso-carrillera-setas"
    )
