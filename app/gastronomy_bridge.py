"""PostgreSQL shared-ecosystem bridge syncing Vinum Pulse with Mise en Place MD."""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, text

from app.schemas import Dish, WineProfile

_UPSERT_WINE_SQL = text("""
    INSERT INTO enology.wines (
        slug, name, winery, appellation, country, classification, wine_type,
        vintage, price_eur, serving_temp_c, decant_minutes, glass_type,
        body, acidity, tannins, fruit, oak, tasting_notes,
        latitude, longitude, altitude_m, soil_type, climate,
        aging_potential_years, tagline, image_url
    ) VALUES (
        :slug, :name, :winery, :appellation, :country, :classification, :wine_type,
        :vintage, :price_eur, :serving_temp_c, :decant_minutes, :glass_type,
        :body, :acidity, :tannins, :fruit, :oak, :tasting_notes,
        :latitude, :longitude, :altitude_m, :soil_type, :climate,
        :aging_potential_years, :tagline, :image_url
    )
    ON CONFLICT (slug) DO UPDATE SET
        name = EXCLUDED.name,
        winery = EXCLUDED.winery,
        appellation = EXCLUDED.appellation,
        country = EXCLUDED.country,
        classification = EXCLUDED.classification,
        wine_type = EXCLUDED.wine_type,
        vintage = EXCLUDED.vintage,
        price_eur = EXCLUDED.price_eur,
        serving_temp_c = EXCLUDED.serving_temp_c,
        decant_minutes = EXCLUDED.decant_minutes,
        glass_type = EXCLUDED.glass_type,
        body = EXCLUDED.body,
        acidity = EXCLUDED.acidity,
        tannins = EXCLUDED.tannins,
        fruit = EXCLUDED.fruit,
        oak = EXCLUDED.oak,
        tasting_notes = EXCLUDED.tasting_notes,
        tagline = EXCLUDED.tagline,
        image_url = EXCLUDED.image_url
    """)

_UPSERT_DISH_SQL = text("""
    INSERT INTO enology.dishes (
        slug, name, category, description,
        body, acidity, tannins, fruit, oak, suggested_wine_type
    ) VALUES (
        :slug, :name, :category, :description,
        :body, :acidity, :tannins, :fruit, :oak, :suggested_wine_type
    )
    ON CONFLICT (slug) DO UPDATE SET
        name = EXCLUDED.name,
        category = EXCLUDED.category,
        description = EXCLUDED.description,
        body = EXCLUDED.body,
        acidity = EXCLUDED.acidity,
        tannins = EXCLUDED.tannins,
        fruit = EXCLUDED.fruit,
        oak = EXCLUDED.oak,
        suggested_wine_type = EXCLUDED.suggested_wine_type
    """)

_FETCH_RECIPE_LINKS_SQL = text("""
    SELECT dish_slug, recipe_slug
    FROM pairing.v_dish_with_recipe
    WHERE recipe_slug IS NOT NULL
    """)


def build_recipe_url(base_url: str, recipe_slug: str | None) -> str | None:
    """Compose a deep-link URL to Mise en Place MD without hardcoding hosts in DB."""
    if not recipe_slug:
        return None
    return f"{base_url.rstrip('/')}/recipes/{recipe_slug}"


class GastronomyPostgresBridge:
    """Syncs Vinum Pulse catalog into PostgreSQL and resolves recipe deep-links."""

    def __init__(
        self,
        pg_url: str | None,
        mise_en_place_base_url: str,
        pg_engine: Engine | None = None,
    ) -> None:
        self._mise_base_url = mise_en_place_base_url.rstrip("/")
        if pg_engine is not None:
            self._engine: Engine | None = pg_engine
        elif pg_url:
            self._engine = create_engine(pg_url, pool_pre_ping=True)
        else:
            self._engine = None

    @property
    def enabled(self) -> bool:
        """Return whether the shared PostgreSQL bridge is configured."""
        return self._engine is not None

    def sync_catalog(self, wines: list[WineProfile], dishes: list[Dish]) -> int:
        """Idempotently upsert wines and dishes into PostgreSQL enology schema."""
        if self._engine is None:
            return 0

        wine_params = [
            {
                "slug": w.id,
                "name": w.name,
                "winery": w.winery,
                "appellation": w.appellation,
                "country": w.country,
                "classification": w.classification,
                "wine_type": str(w.wine_type),
                "vintage": w.vintage,
                "price_eur": w.price_eur,
                "serving_temp_c": w.serving_temp_c,
                "decant_minutes": w.decant_minutes,
                "glass_type": w.glass_type,
                "body": w.sensory.body,
                "acidity": w.sensory.acidity,
                "tannins": w.sensory.tannins,
                "fruit": w.sensory.fruit,
                "oak": w.sensory.oak,
                "tasting_notes": w.tasting_notes,
                "latitude": w.latitude,
                "longitude": w.longitude,
                "altitude_m": w.altitude_m,
                "soil_type": w.soil_type,
                "climate": w.climate,
                "aging_potential_years": w.aging_potential_years,
                "tagline": w.tagline,
                "image_url": w.image_url,
            }
            for w in wines
        ]
        dish_params = [
            {
                "slug": d.id,
                "name": d.name,
                "category": d.category,
                "description": d.description,
                "body": d.target_sensory.body,
                "acidity": d.target_sensory.acidity,
                "tannins": d.target_sensory.tannins,
                "fruit": d.target_sensory.fruit,
                "oak": d.target_sensory.oak,
                "suggested_wine_type": (
                    str(d.suggested_wine_type)
                    if d.suggested_wine_type is not None
                    else None
                ),
            }
            for d in dishes
        ]

        with self._engine.begin() as conn:
            if wine_params:
                conn.execute(_UPSERT_WINE_SQL, wine_params)
            if dish_params:
                conn.execute(_UPSERT_DISH_SQL, dish_params)
        return len(wine_params) + len(dish_params)

    def fetch_dish_recipe_links(self) -> dict[str, str]:
        """Return mapping {dish_slug: recipe_slug} from pairing.v_dish_with_recipe."""
        if self._engine is None:
            return {}
        with self._engine.connect() as conn:
            rows = conn.execute(_FETCH_RECIPE_LINKS_SQL).all()
        return {str(dish_slug): str(recipe_slug) for dish_slug, recipe_slug in rows}

    def attach_recipe_link(self, dish: Dish, links: dict[str, str]) -> Dish:
        """Return Dish enriched with recipe_slug and deep-link URL when linked."""
        slug = links.get(dish.id)
        if not slug:
            return dish
        return dish.model_copy(
            update={
                "recipe_slug": slug,
                "recipe_url": build_recipe_url(self._mise_base_url, slug),
            }
        )
