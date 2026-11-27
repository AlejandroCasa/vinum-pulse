"""European curated wine, region, and gastronomic dish catalogs."""

from app.catalog.dishes import CURATED_DISHES
from app.catalog.england import ENGLAND_WINES
from app.catalog.france import FRANCE_WINES
from app.catalog.italy import ITALY_WINES
from app.catalog.regions import CLIMATE_MAP, DO_METADATA
from app.catalog.spain import SPAIN_WINES
from app.catalog.vermouths import SPANISH_VERMOUTHS
from app.schemas import WineProfile

CURATED_WINES: list[WineProfile] = [
    *SPAIN_WINES,
    *SPANISH_VERMOUTHS,
    *FRANCE_WINES,
    *ITALY_WINES,
    *ENGLAND_WINES,
]

__all__ = [
    "CLIMATE_MAP",
    "CURATED_DISHES",
    "CURATED_WINES",
    "DO_METADATA",
    "ENGLAND_WINES",
    "FRANCE_WINES",
    "ITALY_WINES",
    "SPAIN_WINES",
    "SPANISH_VERMOUTHS",
]
