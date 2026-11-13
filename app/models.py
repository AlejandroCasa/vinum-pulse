"""SQLAlchemy ORM models for persistent wines and gastronomic dishes."""

from sqlalchemy import Float, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.schemas import Dish, SensoryRadar, WineProfile, WineType


class WineModel(Base):
    """Persistent catalog entry for a curated wine."""

    __tablename__ = "wines"
    __table_args__ = (
        Index("ix_wines_type_price", "wine_type", "price_eur"),
        Index("ix_wines_appellation_price", "appellation", "price_eur"),
    )

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), index=True)
    winery: Mapped[str] = mapped_column(String(256), index=True)
    appellation: Mapped[str] = mapped_column(String(128), index=True)
    wine_type: Mapped[str] = mapped_column(String(32), index=True)
    vintage: Mapped[int] = mapped_column(Integer)
    price_eur: Mapped[float] = mapped_column(Float, index=True)
    serving_temp_c: Mapped[float] = mapped_column(Float)
    decant_minutes: Mapped[int] = mapped_column(Integer, default=0)
    glass_type: Mapped[str] = mapped_column(String(64))
    body: Mapped[float] = mapped_column(Float)
    acidity: Mapped[float] = mapped_column(Float)
    tannins: Mapped[float] = mapped_column(Float)
    fruit: Mapped[float] = mapped_column(Float)
    oak: Mapped[float] = mapped_column(Float)
    tasting_notes: Mapped[str] = mapped_column(Text)

    def to_schema(self) -> WineProfile:
        """Convert ORM row into a Pydantic WineProfile contract."""
        return WineProfile(
            id=self.id,
            name=self.name,
            winery=self.winery,
            appellation=self.appellation,
            wine_type=WineType(self.wine_type),
            vintage=self.vintage,
            price_eur=self.price_eur,
            serving_temp_c=self.serving_temp_c,
            decant_minutes=self.decant_minutes,
            glass_type=self.glass_type,
            sensory=SensoryRadar(
                body=self.body,
                acidity=self.acidity,
                tannins=self.tannins,
                fruit=self.fruit,
                oak=self.oak,
            ),
            tasting_notes=self.tasting_notes,
        )

    @classmethod
    def from_schema(cls, wine: WineProfile) -> "WineModel":
        """Build a WineModel instance from a Pydantic WineProfile."""
        return cls(
            id=wine.id,
            name=wine.name,
            winery=wine.winery,
            appellation=wine.appellation,
            wine_type=str(wine.wine_type),
            vintage=wine.vintage,
            price_eur=wine.price_eur,
            serving_temp_c=wine.serving_temp_c,
            decant_minutes=wine.decant_minutes,
            glass_type=wine.glass_type,
            body=wine.sensory.body,
            acidity=wine.sensory.acidity,
            tannins=wine.sensory.tannins,
            fruit=wine.sensory.fruit,
            oak=wine.sensory.oak,
            tasting_notes=wine.tasting_notes,
        )


class DishModel(Base):
    """Persistent catalog entry for a gastronomic dish."""

    __tablename__ = "dishes"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    description: Mapped[str] = mapped_column(Text)
    body: Mapped[float] = mapped_column(Float)
    acidity: Mapped[float] = mapped_column(Float)
    tannins: Mapped[float] = mapped_column(Float)
    fruit: Mapped[float] = mapped_column(Float)
    oak: Mapped[float] = mapped_column(Float)
    suggested_wine_type: Mapped[str | None] = mapped_column(String(32), nullable=True)

    def to_schema(self) -> Dish:
        """Convert ORM row into a Pydantic Dish contract."""
        return Dish(
            id=self.id,
            name=self.name,
            category=self.category,
            description=self.description,
            target_sensory=SensoryRadar(
                body=self.body,
                acidity=self.acidity,
                tannins=self.tannins,
                fruit=self.fruit,
                oak=self.oak,
            ),
            suggested_wine_type=(
                WineType(self.suggested_wine_type)
                if self.suggested_wine_type is not None
                else None
            ),
        )

    @classmethod
    def from_schema(cls, dish: Dish) -> "DishModel":
        """Build a DishModel instance from a Pydantic Dish."""
        return cls(
            id=dish.id,
            name=dish.name,
            category=dish.category,
            description=dish.description,
            body=dish.target_sensory.body,
            acidity=dish.target_sensory.acidity,
            tannins=dish.target_sensory.tannins,
            fruit=dish.target_sensory.fruit,
            oak=dish.target_sensory.oak,
            suggested_wine_type=(
                str(dish.suggested_wine_type)
                if dish.suggested_wine_type is not None
                else None
            ),
        )
