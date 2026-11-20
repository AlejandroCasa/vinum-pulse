"""Helper builder for converting compact wine seed specs into WineProfile models."""

from typing import NamedTuple

from app.schemas import SensoryRadar, WineProfile, WineType


class WineSpec(NamedTuple):
    """Compact typed tuple representing a curated wine catalog entry."""

    id: str
    name: str
    winery: str
    appellation: str
    country: str
    classification: str
    wine_type: WineType
    vintage: int
    price_eur: float
    serving_temp_c: float
    decant_minutes: int
    glass_type: str
    sensory: tuple[float, float, float, float, float]
    tasting_notes: str
    latitude: float
    longitude: float
    altitude_m: int
    soil_type: str
    climate: str
    aging_potential_years: int
    tagline: str


def build_wines(specs: tuple[WineSpec, ...]) -> list[WineProfile]:
    """Convert a tuple of WineSpec records into validated WineProfile objects."""
    return [
        WineProfile(
            id=spec.id,
            name=spec.name,
            winery=spec.winery,
            appellation=spec.appellation,
            country=spec.country,
            classification=spec.classification,
            wine_type=spec.wine_type,
            vintage=spec.vintage,
            price_eur=spec.price_eur,
            serving_temp_c=spec.serving_temp_c,
            decant_minutes=spec.decant_minutes,
            glass_type=spec.glass_type,
            sensory=SensoryRadar(
                body=spec.sensory[0],
                acidity=spec.sensory[1],
                tannins=spec.sensory[2],
                fruit=spec.sensory[3],
                oak=spec.sensory[4],
            ),
            tasting_notes=spec.tasting_notes,
            latitude=spec.latitude,
            longitude=spec.longitude,
            altitude_m=spec.altitude_m,
            soil_type=spec.soil_type,
            climate=spec.climate,
            aging_potential_years=spec.aging_potential_years,
            tagline=spec.tagline,
        )
        for spec in specs
    ]
