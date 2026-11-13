"""Pydantic data models and enums for Vinum Pulse sommelier pairing engine."""

from enum import StrEnum

from pydantic import BaseModel, Field


class WineType(StrEnum):
    """Enumeration of wine types."""

    RED = "Red"
    WHITE = "White"
    SPARKLING = "Sparkling"
    FORTIFIED = "Fortified"
    ROSE = "Rose"


class SensoryRadar(BaseModel):
    """5-axis sensory taste profile scaled from 1.0 (subtle) to 10.0 (intense)."""

    body: float = Field(
        ...,
        ge=1.0,
        le=10.0,
        description="Body and texture density on palate (1.0 to 10.0).",
    )
    acidity: float = Field(
        ...,
        ge=1.0,
        le=10.0,
        description="Acidity, tartness, and freshness (1.0 to 10.0).",
    )
    tannins: float = Field(
        ...,
        ge=1.0,
        le=10.0,
        description="Tannic grip and astringency structure (1.0 to 10.0).",
    )
    fruit: float = Field(
        ...,
        ge=1.0,
        le=10.0,
        description="Primary and secondary fruit expression (1.0 to 10.0).",
    )
    oak: float = Field(
        ...,
        ge=1.0,
        le=10.0,
        description="Oak maturation, vanilla, and toast character (1.0 to 10.0).",
    )


class WineProfile(BaseModel):
    """Complete profile of a curated wine in the cellar catalog."""

    id: str = Field(
        ...,
        min_length=1,
        description="Unique URL-friendly wine identifier slug.",
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Commercial label name of the wine.",
    )
    winery: str = Field(
        ...,
        min_length=1,
        description="Name of the producing winery or bodega.",
    )
    appellation: str = Field(
        ...,
        min_length=1,
        description="Official Protected Designation of Origin (D.O. / D.O.Ca. / D.O.Q.).",
    )
    wine_type: WineType = Field(
        ...,
        description="Enological wine category.",
    )
    vintage: int = Field(
        ...,
        ge=1900,
        le=2100,
        description="Harvest vintage year.",
    )
    price_eur: float = Field(
        ...,
        gt=0.0,
        description="Current market price in euros.",
    )
    serving_temp_c: float = Field(
        ...,
        ge=4.0,
        le=22.0,
        description="Optimal serving temperature in degrees Celsius.",
    )
    decant_minutes: int = Field(
        default=0,
        ge=0,
        description="Recommended decanting or aeration time in minutes.",
    )
    glass_type: str = Field(
        ...,
        min_length=1,
        description="Recommended glassware geometry (e.g. Burdeos, Borgoña, Tulipa).",
    )
    sensory: SensoryRadar = Field(
        ...,
        description="5-dimensional sensory radar profile.",
    )
    tasting_notes: str = Field(
        ...,
        min_length=1,
        description="Sommelier tasting notes and aromatic descriptors.",
    )


class Dish(BaseModel):
    """Gastronomic dish with culinary attributes and target sensory requirement."""

    id: str = Field(
        ...,
        min_length=1,
        description="Unique dish identifier slug.",
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Traditional gastronomic name of the dish.",
    )
    category: str = Field(
        ...,
        min_length=1,
        description="Culinary category (e.g. Carnes, Arroces, Pescados, Embutidos).",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Culinary elaboration and sensory highlights.",
    )
    target_sensory: SensoryRadar = Field(
        ...,
        description="Ideal sensory profile required in wine to complement the dish.",
    )
    suggested_wine_type: WineType | None = Field(
        default=None,
        description="Recommended default wine category for this dish.",
    )


class DishPairingRequest(BaseModel):
    """Incoming request to recommend an optimal wine pairing for a dish."""

    dish_id: str = Field(
        ...,
        min_length=1,
        description="Identifier of the target dish from the catalog.",
    )
    max_budget_eur: float = Field(
        ...,
        gt=0.0,
        description="Maximum allowed bottle budget in euros.",
    )
    preferred_type: WineType | None = Field(
        default=None,
        description="Optional wine type preference filter.",
    )


class PairingRecommendation(BaseModel):
    """Algorithmic sommelier recommendation containing primary and alternative wines."""

    dish_name: str = Field(
        ...,
        description="Name of the evaluated gastronomic dish.",
    )
    compatibility_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Sensory affinity compatibility index from 0.0 to 100.0%.",
    )
    primary_wine: WineProfile = Field(
        ...,
        description="Top-ranked wine matching sensory profile within budget.",
    )
    alternative_wines: list[WineProfile] = Field(
        default_factory=list,
        description="Alternative pairing options within budget.",
    )
    target_sensory: SensoryRadar = Field(
        ...,
        description="Sensory profile demanded by the dish.",
    )
    sommelier_explanation: str = Field(
        ...,
        description="Expert sommelier rationale detailing taste and structural harmony.",
    )


class RegionSummary(BaseModel):
    """Summary of a wine region and its representation in the catalog."""

    appellation: str = Field(..., description="Name of the Appellation / D.O.")
    wine_count: int = Field(..., ge=0, description="Number of cataloged wines.")
    climate_type: str = Field(..., description="Regional climate classification.")
