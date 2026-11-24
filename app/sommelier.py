"""Curated enological database and multi-vector sommelier pairing engine."""

import heapq
import math
import uuid
from typing import Any

from sqlalchemy import Engine, TextClause, func, inspect, or_, select, text
from sqlalchemy.orm import Session, sessionmaker

from app.catalog import CLIMATE_MAP as CLIMATE_MAP
from app.catalog import CURATED_DISHES as CURATED_DISHES
from app.catalog import CURATED_WINES as CURATED_WINES
from app.catalog import DO_METADATA as DO_METADATA
from app.database import Base
from app.gastronomy_bridge import GastronomyPostgresBridge
from app.models import CellarItemModel, DishModel, WineModel
from app.schemas import (
    CellarCreateRequest,
    CellarItem,
    Dish,
    DishPairingRequest,
    EveningMenuPlan,
    EveningMenuRequest,
    GeoJsonFeature,
    GeoJsonFeatureCollection,
    GeoJsonGeometry,
    PairingRecommendation,
    RegionSummary,
    SensoryRadar,
    WineProfile,
    WineType,
)


def _build_winery_feature(wine: WineProfile) -> GeoJsonFeature:
    """Build a GeoJSON Point feature for a curated winery label."""
    do_meta = DO_METADATA.get(wine.appellation, {})
    community = str(do_meta.get("autonomous_community", wine.country))
    grape = str(do_meta.get("signature_grape", "Varietal autóctono"))
    summary = (
        f"{wine.winery} ({wine.appellation}, {wine.country}) — "
        f"{wine.name} ({wine.vintage}), {wine.price_eur:.2f} €. {wine.tagline}"
    )
    return GeoJsonFeature(
        id=wine.id,
        geometry=GeoJsonGeometry(coordinates=[wine.longitude, wine.latitude]),
        properties={
            "feature_type": "winery",
            "id": wine.id,
            "name": wine.name,
            "winery": wine.winery,
            "appellation": wine.appellation,
            "country": wine.country,
            "classification": wine.classification,
            "autonomous_community": community,
            "climate": wine.climate,
            "soil": wine.soil_type,
            "altitude_m": wine.altitude_m,
            "signature_grape": grape,
            "winery_catalog_summary": summary,
            "price_eur": wine.price_eur,
            "vintage": wine.vintage,
            "wine_type": str(wine.wine_type.value),
            "serving_temp_c": wine.serving_temp_c,
            "decant_minutes": wine.decant_minutes,
            "glass_type": wine.glass_type,
            "tasting_notes": wine.tasting_notes,
            "tagline": wine.tagline,
            "bottle_silhouette": wine.bottle_silhouette,
            "image_url": wine.image_url,
            "sensory": wine.sensory.model_dump(),
        },
    )


def _build_region_feature(
    do_name: str, meta: dict[str, Any], wines: list[WineProfile]
) -> GeoJsonFeature:
    """Build a GeoJSON Point feature for a Designation of Origin centroid."""
    avg_alt = int(sum(w.altitude_m for w in wines) / len(wines)) if wines else 500
    bodegas = sorted(list(dict.fromkeys(w.winery for w in wines)))
    country = str(meta.get("country", "España"))
    classification = str(meta.get("classification", "D.O."))
    summary = (
        f"{do_name} ({country}, {len(wines)} vinos catalogados, "
        f"{len(bodegas)} bodegas): {', '.join(bodegas)}"
    )
    slug = do_name.lower().replace(" ", "-").replace(".", "").replace("/", "-").strip()
    center: list[float] = list(meta.get("center", [-3.7, 40.4]))
    return GeoJsonFeature(
        id=f"region-{slug}",
        geometry=GeoJsonGeometry(coordinates=[center[0], center[1]]),
        properties={
            "feature_type": "region",
            "id": f"region-{slug}",
            "name": do_name,
            "appellation": do_name,
            "country": country,
            "classification": classification,
            "autonomous_community": str(meta.get("autonomous_community", country)),
            "climate": str(meta.get("climate", "Mediterráneo continental")),
            "soil": str(meta.get("soil", "Calizo y arcilloso")),
            "altitude_m": avg_alt,
            "altitude_range_m": str(meta.get("altitude_range_m", "400 - 800 m")),
            "signature_grape": str(meta.get("signature_grape", "Varietal autóctono")),
            "description": str(meta.get("description", "")),
            "winery_count": len(bodegas),
            "wineries": bodegas,
            "winery_catalog_summary": summary,
        },
    )


_WINE_MIGRATION_STMTS: tuple[tuple[str, TextClause], ...] = (
    (
        "country",
        text("ALTER TABLE wines ADD COLUMN country VARCHAR(64) DEFAULT 'España'"),
    ),
    (
        "classification",
        text("ALTER TABLE wines ADD COLUMN classification VARCHAR(32) DEFAULT 'D.O.'"),
    ),
    ("latitude", text("ALTER TABLE wines ADD COLUMN latitude FLOAT DEFAULT 40.4168")),
    ("longitude", text("ALTER TABLE wines ADD COLUMN longitude FLOAT DEFAULT -3.7038")),
    ("altitude_m", text("ALTER TABLE wines ADD COLUMN altitude_m INTEGER DEFAULT 500")),
    (
        "soil_type",
        text(
            "ALTER TABLE wines ADD COLUMN soil_type VARCHAR(128) DEFAULT 'Arcilloso-calcáreo'"
        ),
    ),
    (
        "climate",
        text("ALTER TABLE wines ADD COLUMN climate VARCHAR(128) DEFAULT 'Continental'"),
    ),
    (
        "aging_potential_years",
        text("ALTER TABLE wines ADD COLUMN aging_potential_years INTEGER DEFAULT 5"),
    ),
    ("tagline", text("ALTER TABLE wines ADD COLUMN tagline VARCHAR(256) DEFAULT ''")),
    (
        "image_url",
        text("ALTER TABLE wines ADD COLUMN image_url VARCHAR(512) DEFAULT NULL"),
    ),
)


def _ensure_wine_terroir_columns(db_engine: Engine) -> None:
    """Add new terroir and multi-country columns to existing SQLite wines table."""
    inspector = inspect(db_engine)
    if "wines" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("wines")}
    with db_engine.begin() as conn:
        for col_name, stmt in _WINE_MIGRATION_STMTS:
            if col_name not in existing:
                conn.execute(stmt)


def _sync_wines(session: Session) -> None:
    """Seed missing wines and update country/classification on migrated rows."""
    existing_rows = {row.id: row for row in session.scalars(select(WineModel)).all()}
    missing: list[WineModel] = []
    for wine in CURATED_WINES:
        row = existing_rows.get(wine.id)
        if row is None:
            missing.append(WineModel.from_schema(wine))
        else:
            if row.country != wine.country:
                row.country = wine.country
            if row.classification != wine.classification:
                row.classification = wine.classification
    if missing:
        session.add_all(missing)


def _sync_dishes(session: Session) -> None:
    """Seed missing dishes and synchronize categories on existing rows."""
    dish_map = {d.id: d for d in session.scalars(select(DishModel)).all()}
    missing_dishes: list[DishModel] = []
    for dish in CURATED_DISHES:
        existing = dish_map.get(dish.id)
        if existing is None:
            missing_dishes.append(DishModel.from_schema(dish))
        elif existing.category != dish.category:
            existing.category = dish.category
    if missing_dishes:
        session.add_all(missing_dishes)


def init_db(db_engine: Engine, session_factory: sessionmaker[Session]) -> None:
    """Create database tables, evolve schema, and seed curated wines and dishes."""
    Base.metadata.create_all(bind=db_engine)
    _ensure_wine_terroir_columns(db_engine)
    with session_factory() as session:
        _sync_wines(session)
        _sync_dishes(session)
        session.commit()


def _matches_country(value: str, country_filter: str | None) -> bool:
    """Case-insensitive country match helper."""
    if not country_filter:
        return True
    return value.strip().lower() == country_filter.strip().lower()


class SommelierEngine:
    """Core mathematical pairing engine and enological knowledge catalog."""

    MAX_EUCLIDEAN_DISTANCE: float = math.sqrt(5 * (9.0**2))

    def __init__(
        self,
        wines: list[WineProfile] | None = None,
        dishes: list[Dish] | None = None,
        session_factory: sessionmaker[Session] | None = None,
        gastronomy_bridge: GastronomyPostgresBridge | None = None,
    ) -> None:
        """Initialize engine with curated catalogs, custom datasets, or DB session."""
        self._session_factory: sessionmaker[Session] | None = session_factory
        self._gastronomy_bridge: GastronomyPostgresBridge | None = gastronomy_bridge
        self._wines: list[WineProfile] = list(wines or CURATED_WINES)
        self._dishes: list[Dish] = list(dishes or CURATED_DISHES)
        self._dish_index: dict[str, Dish] = {d.id: d for d in self._dishes}
        self._wine_index: dict[str, WineProfile] = {w.id: w for w in self._wines}

    def _enrich_dishes_with_recipes(self, dishes: list[Dish]) -> list[Dish]:
        """Attach Mise en Place MD recipe links when the PostgreSQL bridge is active."""
        if self._gastronomy_bridge is None or not self._gastronomy_bridge.enabled:
            return dishes
        links = self._gastronomy_bridge.fetch_dish_recipe_links()
        if not links:
            return dishes
        return [
            self._gastronomy_bridge.attach_recipe_link(dish, links) for dish in dishes
        ]

    def get_wines(
        self,
        appellation: str | None = None,
        country: str | None = None,
        wine_type: WineType | None = None,
        max_price: float | None = None,
        q: str | None = None,
        limit: int = 250,
        offset: int = 0,
    ) -> list[WineProfile]:
        """Filter and paginate wines by country, appellation, type, budget, search."""
        if self._session_factory is not None:
            return self._get_wines_db(
                self._session_factory,
                appellation=appellation,
                country=country,
                wine_type=wine_type,
                max_price=max_price,
                q=q,
                limit=limit,
                offset=offset,
            )

        query = q.lower().strip() if q else None
        results = [
            wine
            for wine in self._wines
            if self._wine_matches_filters(
                wine,
                appellation=appellation,
                country=country,
                wine_type=wine_type,
                max_price=max_price,
                query=query,
            )
        ]
        return results[offset : offset + limit]

    @classmethod
    def _wine_matches_filters(
        cls,
        wine: WineProfile,
        appellation: str | None,
        country: str | None,
        wine_type: WineType | None,
        max_price: float | None,
        query: str | None,
    ) -> bool:
        """Check whether an in-memory wine satisfies all optional filters."""
        if not _matches_country(wine.country, country):
            return False
        if appellation and appellation.lower() not in wine.appellation.lower():
            return False
        if wine_type and wine.wine_type != wine_type:
            return False
        if max_price is not None and wine.price_eur > max_price:
            return False
        return not (query and not cls._matches_wine_query(wine, query))

    @staticmethod
    def _matches_wine_query(wine: WineProfile, query: str) -> bool:
        """Check whether a wine matches a lowercase search term."""
        return (
            query in wine.name.lower()
            or query in wine.winery.lower()
            or query in wine.appellation.lower()
            or query in wine.country.lower()
        )

    def _get_wines_db(
        self,
        session_factory: sessionmaker[Session],
        appellation: str | None,
        country: str | None,
        wine_type: WineType | None,
        max_price: float | None,
        q: str | None,
        limit: int,
        offset: int,
    ) -> list[WineProfile]:
        """Query paginated and filtered wines from SQLAlchemy."""
        stmt = select(WineModel)
        if country:
            stmt = stmt.where(func.lower(WineModel.country) == country.strip().lower())
        if appellation:
            stmt = stmt.where(WineModel.appellation.ilike(f"%{appellation}%"))
        if wine_type:
            stmt = stmt.where(WineModel.wine_type == str(wine_type))
        if max_price is not None:
            stmt = stmt.where(WineModel.price_eur <= max_price)
        if q:
            search = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    WineModel.name.ilike(search),
                    WineModel.winery.ilike(search),
                    WineModel.appellation.ilike(search),
                    WineModel.country.ilike(search),
                )
            )
        stmt = stmt.order_by(WineModel.price_eur.asc()).offset(offset).limit(limit)

        with session_factory() as session:
            rows = session.scalars(stmt).all()
            return [row.to_schema() for row in rows]

    def get_dishes(
        self,
        category: str | None = None,
        q: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Dish]:
        """Return cataloged dishes with optional category filtering and search."""
        if self._session_factory is not None:
            return self._enrich_dishes_with_recipes(
                self._get_dishes_db(
                    self._session_factory,
                    category=category,
                    q=q,
                    limit=limit,
                    offset=offset,
                )
            )

        query = q.lower().strip() if q else None
        results = [
            dish
            for dish in self._dishes
            if (not category or category.lower() in dish.category.lower())
            and (
                not query
                or query in dish.name.lower()
                or query in dish.description.lower()
            )
        ]
        return self._enrich_dishes_with_recipes(results[offset : offset + limit])

    def _get_dishes_db(
        self,
        session_factory: sessionmaker[Session],
        category: str | None,
        q: str | None,
        limit: int,
        offset: int,
    ) -> list[Dish]:
        """Query paginated and filtered dishes from SQLAlchemy."""
        stmt = select(DishModel)
        if category:
            stmt = stmt.where(DishModel.category.ilike(f"%{category}%"))
        if q:
            search = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    DishModel.name.ilike(search),
                    DishModel.description.ilike(search),
                )
            )
        stmt = stmt.order_by(DishModel.name.asc()).offset(offset).limit(limit)

        with session_factory() as session:
            rows = session.scalars(stmt).all()
            return [row.to_schema() for row in rows]

    def get_wine_by_id(self, wine_id: str) -> WineProfile | None:
        """Look up a wine profile by its unique identifier slug."""
        if self._session_factory is not None:
            with self._session_factory() as session:
                row = session.get(WineModel, wine_id)
                return row.to_schema() if row else None
        return self._wine_index.get(wine_id)

    def get_dish_by_id(self, dish_id: str) -> Dish | None:
        """Look up a dish by its unique identifier slug."""
        dish: Dish | None
        if self._session_factory is not None:
            with self._session_factory() as session:
                row = session.get(DishModel, dish_id)
                dish = row.to_schema() if row else None
        else:
            dish = self._dish_index.get(dish_id)
        if dish is None:
            return None
        return self._enrich_dishes_with_recipes([dish])[0]

    @staticmethod
    def _build_region_summary(app_name: str, count: int) -> RegionSummary:
        """Build a RegionSummary from appellation name, count, and metadata."""
        meta = DO_METADATA.get(app_name, {})
        climate = CLIMATE_MAP.get(app_name, "Mediterráneo continental característico")
        return RegionSummary(
            appellation=app_name,
            country=str(meta.get("country", "España")),
            classification=str(meta.get("classification", "D.O.")),
            wine_count=count,
            climate_type=climate,
            autonomous_community=meta.get("autonomous_community"),
            signature_grape=meta.get("signature_grape"),
            soil=meta.get("soil"),
            coordinates=meta.get("center"),
        )

    def get_regions(self, country: str | None = None) -> list[RegionSummary]:
        """Return summary of all Appellations optionally filtered by country."""
        if self._session_factory is not None:
            with self._session_factory() as session:
                stmt = select(WineModel.appellation, func.count(WineModel.id))
                if country:
                    stmt = stmt.where(
                        func.lower(WineModel.country) == country.strip().lower()
                    )
                stmt = stmt.group_by(WineModel.appellation).order_by(
                    func.count(WineModel.id).desc()
                )
                rows = session.execute(stmt).all()
                return [
                    self._build_region_summary(app, int(count)) for app, count in rows
                ]

        counts: dict[str, int] = {}
        for wine in self._wines:
            if _matches_country(wine.country, country):
                counts[wine.appellation] = counts.get(wine.appellation, 0) + 1

        summaries = [
            self._build_region_summary(app, count) for app, count in counts.items()
        ]
        return sorted(summaries, key=lambda r: r.wine_count, reverse=True)

    def get_atlas_geojson(
        self, layer: str = "wineries", country: str | None = None
    ) -> GeoJsonFeatureCollection:
        """Return GeoJSON FeatureCollection of European wine regions and wineries."""
        features: list[GeoJsonFeature] = []
        wines = self.get_wines(country=country, limit=500)

        if layer in ("wineries", "all"):
            for wine in wines:
                features.append(_build_winery_feature(wine))

        if layer in ("regions", "all"):
            for do_name, meta in DO_METADATA.items():
                meta_country = str(meta.get("country", "España"))
                if not _matches_country(meta_country, country):
                    continue
                do_wines = [w for w in wines if w.appellation == do_name]
                features.append(_build_region_feature(do_name, meta, do_wines))

        return GeoJsonFeatureCollection(features=features)

    @classmethod
    def compute_distance(cls, a: SensoryRadar, b: SensoryRadar) -> float:
        """Compute the Euclidean metric across the 5 sensory dimensions."""
        squared_diffs = (
            (a.body - b.body) ** 2
            + (a.acidity - b.acidity) ** 2
            + (a.tannins - b.tannins) ** 2
            + (a.fruit - b.fruit) ** 2
            + (a.oak - b.oak) ** 2
        )
        return math.sqrt(squared_diffs)

    @classmethod
    def compute_compatibility_score(
        cls, target: SensoryRadar, candidate: SensoryRadar
    ) -> float:
        """Convert Euclidean distance to a 0.0 to 100.0% compatibility score."""
        dist = cls.compute_distance(target, candidate)
        ratio = dist / cls.MAX_EUCLIDEAN_DISTANCE
        score = max(0.0, min(100.0, 100.0 * (1.0 - ratio)))
        return round(score, 1)

    @staticmethod
    def _describe_affinity_opening(score: float) -> str:
        """Return a qualitative, non-numeric opening phrase for pairing affinity."""
        if score >= 85.0:
            return "Armonía excepcional"
        if score >= 70.0:
            return "Maridaje muy equilibrado"
        return "Propuesta de contraste interesante"

    @staticmethod
    def _describe_sensory_lesson(wine: WineProfile) -> str:
        """Build an educational explanation of how the wine's sensory traits interact."""
        parts: list[str] = []

        if wine.sensory.body >= 7.5:
            parts.append(
                "su cuerpo amplio aporta el peso necesario para sostener platos de "
                "intensidad marcada sin quedar opacado"
            )
        elif wine.sensory.body >= 5.5:
            parts.append(
                "su volumen medio en boca acompaña la textura del plato con equilibrio"
            )
        else:
            parts.append(
                "su perfil ligero y ágil respeta los matices más delicados sin saturar"
            )

        if wine.sensory.tannins >= 7.0:
            parts.append(
                "sus taninos estructurados se suavizan al interactuar con las proteínas "
                "y grasas del plato, creando una sensación aterciopelada"
            )
        elif wine.wine_type == WineType.RED and wine.sensory.tannins >= 4.5:
            parts.append(
                "sus taninos finos enmarcan el bocado sin resultar astringentes"
            )

        if wine.sensory.acidity >= 7.5:
            parts.append(
                "su acidez vibrante actúa como limpiador natural del paladar, "
                "aligerando la untuosidad entre bocados"
            )
        elif wine.sensory.acidity >= 6.0:
            parts.append("su frescura equilibrada realza los sabores principales")

        if wine.sensory.oak >= 6.5:
            parts.append(
                "la crianza en barrica aporta notas tostadas y especiadas que "
                "conectan por similitud aromática con los matices de elaboración del plato"
            )
        elif wine.sensory.fruit >= 7.8:
            parts.append(
                "su expresión frutal nítida aporta vivacidad aromática al conjunto"
            )

        return "; ".join(parts)

    @staticmethod
    def _describe_service_lesson(wine: WineProfile) -> str:
        """Explain the enological reason behind temperature, glass, and decanting."""
        glass_reasons = {
            "Borgoña": "su cáliz ancho concentra aromas complejos y guía el vino con suavidad",
            "Burdeos": "su copa alta y amplia permite que el vino respire y redondee su estructura",
            "Copita": "su forma estrecha canaliza aromas intensos y punzantes",
            "Tulipa": "preserva la burbuja fina y dirige los aromas hacia la nariz",
            "Flauta": "mantiene la efervescencia vertical y la frescura",
            "Vaso bajo": "permite servirlo con hielo grueso y twist cítrico liberando sus botánicos",
        }
        glass_note = glass_reasons.get(
            wine.glass_type, "favorece una correcta expresión aromática"
        )

        if wine.serving_temp_c <= 10.0:
            temp_note = "frío para preservar su frescura y tensión aromática"
        elif wine.serving_temp_c <= 14.0:
            temp_note = (
                "fresco (sin enfriar en exceso) para que despliegue sus matices "
                "sin perder vivacidad"
            )
        else:
            temp_note = (
                "a temperatura de bodega para suavizar su estructura y liberar "
                "aromas complejos"
            )

        decant_note = (
            f" Conviene decantarlo {wine.decant_minutes} minutos antes para "
            "oxigenarlo y abrir su bouquet."
            if wine.decant_minutes > 0
            else ""
        )

        return (
            f"Consejo de servicio: sírvelo a {wine.serving_temp_c:.0f}°C ({temp_note}) "
            f"en copa {wine.glass_type}, ya que {glass_note}.{decant_note}"
        )

    def _generate_explanation(self, dish: Dish, wine: WineProfile, score: float) -> str:
        """Generate educational enological rationale without numeric scores."""
        opening = self._describe_affinity_opening(score)
        sensory_lesson = self._describe_sensory_lesson(wine)
        service_lesson = self._describe_service_lesson(wine)
        return (
            f"{opening} para '{dish.name}' con '{wine.name}' "
            f"({wine.appellation}, {wine.winery}). "
            f"¿Por qué funciona? Porque {sensory_lesson}. "
            f"{service_lesson}"
        )

    def recommend_pairing(self, request: DishPairingRequest) -> PairingRecommendation:
        """Calculate sensory compatibility and return top-ranked pairings."""
        dish = self.get_dish_by_id(request.dish_id)
        if not dish:
            raise ValueError(
                f"Dish '{request.dish_id}' not found in gastronomic catalog."
            )

        candidate_wines = self.get_wines(
            wine_type=request.preferred_type,
            max_price=request.max_budget_eur,
            limit=500,
        )

        if not candidate_wines and request.preferred_type is not None:
            candidate_wines = self.get_wines(
                max_price=request.max_budget_eur,
                limit=500,
            )

        if not candidate_wines:
            raise ValueError(
                f"No wines found in cellar catalog within the budget of "
                f"{request.max_budget_eur:.2f} EUR."
            )

        scored_wines: list[tuple[float, WineProfile]] = []
        for wine in candidate_wines:
            score = self.compute_compatibility_score(dish.target_sensory, wine.sensory)
            scored_wines.append((score, wine))

        top_candidates = heapq.nlargest(3, scored_wines, key=lambda item: item[0])
        best_score, best_wine = top_candidates[0]
        alternatives = [wine for _, wine in top_candidates[1:]]

        explanation = self._generate_explanation(
            dish=dish,
            wine=best_wine,
            score=best_score,
        )

        return PairingRecommendation(
            dish_name=dish.name,
            compatibility_score=best_score,
            primary_wine=best_wine,
            alternative_wines=alternatives,
            target_sensory=dish.target_sensory,
            sommelier_explanation=explanation,
            dish_recipe_slug=dish.recipe_slug,
            dish_recipe_url=dish.recipe_url,
        )

    def plan_evening_menu(self, request: EveningMenuRequest) -> EveningMenuPlan:
        """Design a 3-course evening wine progression within a global budget."""
        from app.planner import build_evening_menu_plan

        return build_evening_menu_plan(self, request)

    # --- Personal Cellar CRUD Operations ---

    def add_to_cellar(
        self, payload: CellarCreateRequest, user_id: str = "sommelier"
    ) -> CellarItem:
        """Add bottles of a wine to the personal cellar."""
        if self._session_factory is None:
            raise RuntimeError(
                "Database session factory required for cellar operations."
            )

        wine = self.get_wine_by_id(payload.wine_id)
        if not wine:
            raise ValueError(f"Wine '{payload.wine_id}' does not exist in catalog.")

        with self._session_factory() as session:
            stmt = select(CellarItemModel).where(
                CellarItemModel.user_id == user_id,
                CellarItemModel.wine_id == payload.wine_id,
            )
            existing = session.scalars(stmt).first()

            if existing:
                existing.quantity += payload.quantity
                if payload.purchase_price_eur > 0:
                    existing.purchase_price_eur = payload.purchase_price_eur
                if payload.storage_location:
                    existing.storage_location = payload.storage_location
                if payload.notes:
                    existing.notes = payload.notes
                session.commit()
                return existing.to_schema(wine_profile=wine)

            new_item = CellarItemModel(
                id=str(uuid.uuid4())[:8],
                wine_id=payload.wine_id,
                user_id=user_id,
                quantity=payload.quantity,
                purchase_price_eur=payload.purchase_price_eur or wine.price_eur,
                storage_location=payload.storage_location,
                notes=payload.notes,
            )
            session.add(new_item)
            session.commit()
            return new_item.to_schema(wine_profile=wine)

    def get_cellar(self, user_id: str = "sommelier") -> list[CellarItem]:
        """Return all bottles stored in user's personal cellar."""
        if self._session_factory is None:
            return []

        with self._session_factory() as session:
            stmt = select(CellarItemModel).where(CellarItemModel.user_id == user_id)
            rows = session.scalars(stmt).all()
            results: list[CellarItem] = []
            for row in rows:
                wine = self.get_wine_by_id(row.wine_id)
                results.append(row.to_schema(wine_profile=wine))
            return results

    def get_catalog_stats(self) -> tuple[int, int, int]:
        """Return live catalog totals as (wines, appellations, countries)."""
        if self._session_factory is not None:
            with self._session_factory() as session:
                wine_count = int(session.scalar(select(func.count(WineModel.id))) or 0)
                region_count = int(
                    session.scalar(
                        select(func.count(func.distinct(WineModel.appellation)))
                    )
                    or 0
                )
                country_count = int(
                    session.scalar(select(func.count(func.distinct(WineModel.country))))
                    or 0
                )
                return wine_count, region_count, country_count

        return (
            len(self._wines),
            len({wine.appellation for wine in self._wines}),
            len({wine.country for wine in self._wines}),
        )

    def remove_from_cellar(
        self, item_id: str, user_id: str = "sommelier", quantity: int = 1
    ) -> dict[str, Any]:
        """Decrement bottle count or remove cellar record if empty."""
        if self._session_factory is None:
            raise RuntimeError(
                "Database session factory required for cellar operations."
            )

        with self._session_factory() as session:
            row = session.get(CellarItemModel, item_id)
            if not row or row.user_id != user_id:
                raise ValueError(f"Cellar record '{item_id}' not found.")

            if row.quantity <= quantity:
                session.delete(row)
                session.commit()
                return {"status": "deleted", "item_id": item_id, "remaining": 0}

            row.quantity -= quantity
            session.commit()
            return {
                "status": "decremented",
                "item_id": item_id,
                "remaining": row.quantity,
            }
