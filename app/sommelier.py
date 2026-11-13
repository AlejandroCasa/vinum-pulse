"""Curated enological database and multi-vector sommelier pairing engine."""

import heapq
import math

from sqlalchemy import Engine, func, or_, select
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.models import DishModel, WineModel
from app.schemas import (
    Dish,
    DishPairingRequest,
    PairingRecommendation,
    RegionSummary,
    SensoryRadar,
    WineProfile,
    WineType,
)

# Curated reference catalog of premier Spanish wines across major D.O.s
CURATED_WINES: list[WineProfile] = [
    WineProfile(
        id="vina-ardanza-reserva",
        name="Viña Ardanza Reserva",
        winery="La Rioja Alta, S.A.",
        appellation="D.O.Ca. Rioja",
        wine_type=WineType.RED,
        vintage=2017,
        price_eur=34.0,
        serving_temp_c=17.0,
        decant_minutes=30,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=7.8, acidity=7.0, tannins=7.5, fruit=8.0, oak=8.5),
        tasting_notes="Clásico coupage riojano (Tempranillo y Garnacha). Aromas a cedro, tabaco dulce, vainilla y cereza madura con taninos sedosos.",
    ),
    WineProfile(
        id="pago-carraovejas",
        name="Pago de Carraovejas",
        winery="Bodega Pago de Carraovejas",
        appellation="D.O. Ribera del Duero",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=48.0,
        serving_temp_c=16.0,
        decant_minutes=30,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=8.8, acidity=6.5, tannins=8.5, fruit=8.5, oak=8.0),
        tasting_notes="Potente y envolvente. Fruta negra madura, especias tostadas y estructura tánica cremosa que llena el paladar.",
    ),
    WineProfile(
        id="pazo-senorans-seleccion",
        name="Pazo Señorans Selección de Añada",
        winery="Pazo de Señorans",
        appellation="D.O. Rías Baixas",
        wine_type=WineType.WHITE,
        vintage=2014,
        price_eur=46.0,
        serving_temp_c=11.0,
        decant_minutes=0,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.5, acidity=8.8, tannins=1.5, fruit=8.2, oak=2.0),
        tasting_notes="Albariño mítico de guarda criado sobre lías en acero durante más de 30 meses. Alta mineralidad atlántica, hidrocarburos y cítricos nobles.",
    ),
    WineProfile(
        id="belondrade-lurton",
        name="Belondrade y Lurton",
        winery="Belondrade",
        appellation="D.O. Rueda",
        wine_type=WineType.WHITE,
        vintage=2022,
        price_eur=39.0,
        serving_temp_c=12.0,
        decant_minutes=15,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=7.2, acidity=7.5, tannins=2.0, fruit=7.6, oak=6.5),
        tasting_notes="Pionero Verdejo fermentado y criado en barrica de roble francés. Textura untuosa, flor blanca, hinojo silvestre y humo elegante.",
    ),
    WineProfile(
        id="les-terrasses",
        name="Les Terrasses Velles Vinyes",
        winery="Álvaro Palacios",
        appellation="D.O.Q. Priorat",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=39.5,
        serving_temp_c=16.0,
        decant_minutes=45,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=8.5, acidity=7.5, tannins=8.0, fruit=8.2, oak=7.5),
        tasting_notes="Suelo escarpado de pizarra licorella. Garnacha y Cariñena concentradas, grafito, hierbas mediterráneas y fruta roja licorosa.",
    ),
    WineProfile(
        id="tio-pepe-en-rama",
        name="Tío Pepe en Rama Fino",
        winery="González Byass",
        appellation="D.O. Jerez-Xérès-Sherry",
        wine_type=WineType.FORTIFIED,
        vintage=2023,
        price_eur=19.5,
        serving_temp_c=8.0,
        decant_minutes=0,
        glass_type="Copita",
        sensory=SensoryRadar(body=5.2, acidity=8.2, tannins=1.2, fruit=5.5, oak=3.5),
        tasting_notes="Crianza biológica bajo velo de flor sin filtrar ni clarificar. Aromas punzantes a levadura, almendra cruda y una salinidad yodada arrolladora.",
    ),
    WineProfile(
        id="san-roman",
        name="San Román",
        winery="Bodegas Maurodos",
        appellation="D.O. Toro",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=36.0,
        serving_temp_c=17.0,
        decant_minutes=45,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=9.5, acidity=6.0, tannins=9.0, fruit=8.5, oak=8.5),
        tasting_notes="Tinta de Toro de viñas viejas prefiloxéricas. Opulencia tánica, regaliz negro, maderas balsámicas y una concentración colosal.",
    ),
    WineProfile(
        id="petalos-del-bierzo",
        name="Pétalos del Bierzo",
        winery="Descendientes de J. Palacios",
        appellation="D.O. Bierzo",
        wine_type=WineType.RED,
        vintage=2022,
        price_eur=21.5,
        serving_temp_c=15.0,
        decant_minutes=15,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.5, acidity=7.5, tannins=5.8, fruit=8.5, oak=5.2),
        tasting_notes="Mencía atlántica de ladera. Perfil fragante a violetas, frambuesa ácida y frescura mineral con trago directo y seductor.",
    ),
    WineProfile(
        id="gramona-imperial",
        name="Gramona Imperial Brut Nature",
        winery="Gramona",
        appellation="D.O. Corpinnat / Penedès",
        wine_type=WineType.SPARKLING,
        vintage=2018,
        price_eur=26.0,
        serving_temp_c=8.0,
        decant_minutes=0,
        glass_type="Tulipa",
        sensory=SensoryRadar(body=6.0, acidity=8.6, tannins=1.4, fruit=7.2, oak=4.0),
        tasting_notes="Crianza en rima superior a 50 meses. Burbuja fundida, notas de brioche, manzana asada y una frescura vibrante que limpia el paladar.",
    ),
    WineProfile(
        id="ramon-bilbao-crianza",
        name="Ramón Bilbao Crianza",
        winery="Bodegas Ramón Bilbao",
        appellation="D.O.Ca. Rioja",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=11.5,
        serving_temp_c=16.0,
        decant_minutes=0,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=6.2, acidity=6.5, tannins=6.0, fruit=7.5, oak=6.5),
        tasting_notes="Tempranillo accesible y versátil con crianza equilibrada en barrica de roble americano. Notas de vainilla, mora y coco.",
    ),
    WineProfile(
        id="martin-codax-albarino",
        name="Martín Códax Albariño",
        winery="Bodegas Martín Códax",
        appellation="D.O. Rías Baixas",
        wine_type=WineType.WHITE,
        vintage=2023,
        price_eur=13.5,
        serving_temp_c=10.0,
        decant_minutes=0,
        glass_type="Tulipa",
        sensory=SensoryRadar(body=5.0, acidity=8.2, tannins=1.0, fruit=8.0, oak=1.0),
        tasting_notes="Joven y fresco. Flores blancas, manzana verde, pomelo y salinidad marina limpia y refrescante.",
    ),
    WineProfile(
        id="lustau-oloroso-don-nuno",
        name="Lustau Oloroso Don Nuño",
        winery="Emilio Lustau",
        appellation="D.O. Jerez-Xérès-Sherry",
        wine_type=WineType.FORTIFIED,
        vintage=2022,
        price_eur=24.5,
        serving_temp_c=13.0,
        decant_minutes=0,
        glass_type="Copita",
        sensory=SensoryRadar(body=7.8, acidity=7.0, tannins=3.0, fruit=5.0, oak=8.2),
        tasting_notes="Envejecimiento oxidativo en solera centenaria. Nuez tostada, ebanistería noble, cuero y humo con un final seco interminable.",
    ),
]

# Gastronomic catalog of iconic Spanish dishes
CURATED_DISHES: list[Dish] = [
    Dish(
        id="chuleton-brasa",
        name="Chuletón de vaca vieja a la brasa",
        category="Carnes",
        description="Corte de lomo alto madurado 45 días asado con leña de encina y cristales de sal marina.",
        target_sensory=SensoryRadar(
            body=9.0, acidity=6.5, tannins=8.5, fruit=7.5, oak=8.0
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="pulpo-feira",
        name="Pulpo á feira con pimentón de la Vera y patatas",
        category="Pescados y Mariscos",
        description="Pulpo gallego cocido en cobre, pimentón agridulce, aceite virgen extra arbequina y patata kennebec.",
        target_sensory=SensoryRadar(
            body=5.0, acidity=8.5, tannins=1.5, fruit=8.0, oak=1.5
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="arroz-bogavante",
        name="Arroz meloso con bogavante gallego",
        category="Arroces",
        description="Fondo marino intenso de roca, sofrito caramelizado y bogavante azul del Cantábrico con arroz bomba.",
        target_sensory=SensoryRadar(
            body=7.0, acidity=7.5, tannins=2.0, fruit=7.5, oak=5.0
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="jamon-bellota",
        name="Jamón Ibérico de Bellota 100%",
        category="Embutidos y Quesos",
        description="Curación natural en bodega de Jabugo superior a 36 meses. Grasa infiltrada insaturada y umami profundo.",
        target_sensory=SensoryRadar(
            body=5.5, acidity=8.2, tannins=2.0, fruit=6.0, oak=3.5
        ),
        suggested_wine_type=WineType.FORTIFIED,
    ),
    Dish(
        id="queso-manchego",
        name="Queso Manchego Curado de oveja",
        category="Embutidos y Quesos",
        description="Leche cruda de oveja manchega curado en cueva 12 meses. Textura mantecosa, acidez láctica y notas picantes.",
        target_sensory=SensoryRadar(
            body=8.0, acidity=6.5, tannins=7.5, fruit=6.5, oak=7.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="cochinillo-asado",
        name="Cochinillo asado tradicional segoviano",
        category="Carnes",
        description="Asado lentamente en horno de leña de encina con piel ultra crujiente y carne melosa confitada.",
        target_sensory=SensoryRadar(
            body=7.5, acidity=7.5, tannins=7.0, fruit=7.5, oak=7.5
        ),
        suggested_wine_type=WineType.RED,
    ),
]


CLIMATE_MAP: dict[str, str] = {
    "D.O.Ca. Rioja": "Continental templado con influencia atlántica",
    "D.O. Ribera del Duero": "Mediterráneo continental extremo",
    "D.O. Rías Baixas": "Atlántico húmedo y salino",
    "D.O. Rueda": "Continental de meseta",
    "D.O.Q. Priorat": "Mediterráneo de montaña sobre pizarra licorella",
    "D.O. Jerez-Xérès-Sherry": "Mediterráneo cálido con albariza oceánica",
    "D.O. Toro": "Continental árido de alta insolación",
    "D.O. Bierzo": "Microclima de transición atlántico-continental",
    "D.O. Corpinnat / Penedès": "Mediterráneo marítimo templado",
}


def init_db(db_engine: Engine, session_factory: sessionmaker[Session]) -> None:
    """Create database tables and seed curated wines and dishes if empty."""
    Base.metadata.create_all(bind=db_engine)
    with session_factory() as session:
        wine_count = session.scalar(select(func.count()).select_from(WineModel)) or 0
        if wine_count == 0:
            session.add_all([WineModel.from_schema(w) for w in CURATED_WINES])
        dish_count = session.scalar(select(func.count()).select_from(DishModel)) or 0
        if dish_count == 0:
            session.add_all([DishModel.from_schema(d) for d in CURATED_DISHES])
        session.commit()


class SommelierEngine:
    """Core mathematical pairing engine and enological knowledge catalog."""

    # Maximum possible distance in 5D space bounded within [1.0, 10.0]: sqrt(5 * 9^2) ≈ 20.12461
    MAX_EUCLIDEAN_DISTANCE: float = math.sqrt(5 * (9.0**2))

    def __init__(
        self,
        wines: list[WineProfile] | None = None,
        dishes: list[Dish] | None = None,
        session_factory: sessionmaker[Session] | None = None,
    ) -> None:
        """Initialize engine with curated catalogs, custom datasets, or DB session."""
        self._session_factory: sessionmaker[Session] | None = session_factory
        self._wines: list[WineProfile] = list(wines or CURATED_WINES)
        self._dishes: list[Dish] = list(dishes or CURATED_DISHES)
        self._dish_index: dict[str, Dish] = {d.id: d for d in self._dishes}
        self._wine_index: dict[str, WineProfile] = {w.id: w for w in self._wines}

    def get_wines(
        self,
        appellation: str | None = None,
        wine_type: WineType | None = None,
        max_price: float | None = None,
        q: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[WineProfile]:
        """Filter and paginate wines by appellation, type, budget, and search query."""
        if self._session_factory is not None:
            return self._get_wines_db(
                self._session_factory,
                appellation=appellation,
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
        wine_type: WineType | None,
        max_price: float | None,
        query: str | None,
    ) -> bool:
        """Check whether an in-memory wine satisfies all optional filters."""
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
        )

    def _get_wines_db(
        self,
        session_factory: sessionmaker[Session],
        appellation: str | None,
        wine_type: WineType | None,
        max_price: float | None,
        q: str | None,
        limit: int,
        offset: int,
    ) -> list[WineProfile]:
        """Query paginated and filtered wines from SQLAlchemy."""
        stmt = select(WineModel)
        if appellation:
            stmt = stmt.where(WineModel.appellation.ilike(f"%{appellation}%"))
        if wine_type:
            stmt = stmt.where(WineModel.wine_type == str(wine_type))
        if max_price is not None:
            stmt = stmt.where(WineModel.price_eur <= max_price)
        if q:
            pattern = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    WineModel.name.ilike(pattern),
                    WineModel.winery.ilike(pattern),
                    WineModel.appellation.ilike(pattern),
                )
            )
        stmt = stmt.offset(offset).limit(limit)
        with session_factory() as session:
            rows = session.scalars(stmt).all()
            return [row.to_schema() for row in rows]

    def get_wine_by_id(self, wine_id: str) -> WineProfile | None:
        """Fetch a single wine by its unique slug identifier."""
        if self._session_factory is not None:
            with self._session_factory() as session:
                row = session.get(WineModel, wine_id)
                return row.to_schema() if row is not None else None
        return self._wine_index.get(wine_id)

    def get_dishes(
        self,
        category: str | None = None,
        q: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Dish]:
        """Return paginated dishes with optional category and search filtering."""
        if self._session_factory is not None:
            return self._get_dishes_db(
                self._session_factory,
                category=category,
                q=q,
                limit=limit,
                offset=offset,
            )

        query = q.lower().strip() if q else None
        results: list[Dish] = []
        for dish in self._dishes:
            if category and category.lower() not in dish.category.lower():
                continue
            if query and (
                query not in dish.name.lower() and query not in dish.description.lower()
            ):
                continue
            results.append(dish)
        return results[offset : offset + limit]

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
            pattern = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    DishModel.name.ilike(pattern),
                    DishModel.description.ilike(pattern),
                )
            )
        stmt = stmt.offset(offset).limit(limit)
        with session_factory() as session:
            rows = session.scalars(stmt).all()
            return [row.to_schema() for row in rows]

    def get_dish_by_id(self, dish_id: str) -> Dish | None:
        """Fetch a single dish by its unique slug identifier."""
        if self._session_factory is not None:
            with self._session_factory() as session:
                row = session.get(DishModel, dish_id)
                return row.to_schema() if row is not None else None
        return self._dish_index.get(dish_id)

    def get_regions(self) -> list[RegionSummary]:
        """Aggregate wine catalog by Designation of Origin (appellation)."""
        if self._session_factory is not None:
            with self._session_factory() as session:
                stmt = (
                    select(WineModel.appellation, func.count(WineModel.id))
                    .group_by(WineModel.appellation)
                    .order_by(func.count(WineModel.id).desc())
                )
                rows = session.execute(stmt).all()
                return [
                    RegionSummary(
                        appellation=app,
                        wine_count=int(count),
                        climate_type=CLIMATE_MAP.get(
                            app, "Mediterráneo continental característico"
                        ),
                    )
                    for app, count in rows
                ]

        counts: dict[str, int] = {}
        for wine in self._wines:
            counts[wine.appellation] = counts.get(wine.appellation, 0) + 1

        summaries: list[RegionSummary] = []
        for app, count in counts.items():
            climate = CLIMATE_MAP.get(app, "Mediterráneo continental característico")
            summaries.append(
                RegionSummary(appellation=app, wine_count=count, climate_type=climate)
            )
        return sorted(summaries, key=lambda r: r.wine_count, reverse=True)

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

    @classmethod
    def _score_from_coords(
        cls,
        target: SensoryRadar,
        body: float,
        acidity: float,
        tannins: float,
        fruit: float,
        oak: float,
    ) -> float:
        """Compute compatibility score directly from raw 5D coordinates."""
        squared_diffs = (
            (target.body - body) ** 2
            + (target.acidity - acidity) ** 2
            + (target.tannins - tannins) ** 2
            + (target.fruit - fruit) ** 2
            + (target.oak - oak) ** 2
        )
        ratio = math.sqrt(squared_diffs) / cls.MAX_EUCLIDEAN_DISTANCE
        score = max(0.0, min(100.0, 100.0 * (1.0 - ratio)))
        return round(score, 1)

    def _top_wines_db(
        self,
        session_factory: sessionmaker[Session],
        dish: Dish,
        request: DishPairingRequest,
    ) -> list[tuple[WineProfile, float]]:
        """Pre-filter candidates in SQL and hydrate only the top 3 matches."""
        cols = (
            WineModel.id,
            WineModel.price_eur,
            WineModel.body,
            WineModel.acidity,
            WineModel.tannins,
            WineModel.fruit,
            WineModel.oak,
        )
        with session_factory() as session:
            base_stmt = select(*cols).where(
                WineModel.price_eur <= request.max_budget_eur
            )
            rows = (
                session.execute(
                    base_stmt.where(WineModel.wine_type == str(request.preferred_type))
                ).all()
                if request.preferred_type
                else []
            )
            if not rows:
                rows = session.execute(base_stmt).all()
            if not rows:
                raise ValueError(
                    f"No wines found in cellar catalog within budget of "
                    f"{request.max_budget_eur:.2f} €."
                )

            ranked = heapq.nsmallest(
                3,
                (
                    (
                        -self._score_from_coords(
                            dish.target_sensory,
                            row.body,
                            row.acidity,
                            row.tannins,
                            row.fruit,
                            row.oak,
                        ),
                        row.price_eur,
                        row.id,
                    )
                    for row in rows
                ),
            )
            top_ids = [wine_id for _, _, wine_id in ranked]
            hydrated = {
                w.id: w.to_schema()
                for w in session.scalars(
                    select(WineModel).where(WineModel.id.in_(top_ids))
                ).all()
            }
            return [(hydrated[wine_id], -neg_score) for neg_score, _, wine_id in ranked]

    def _select_candidates(self, request: DishPairingRequest) -> list[WineProfile]:
        """Select candidate wines within budget, relaxing type filter if empty."""
        within_budget = [
            w for w in self._wines if w.price_eur <= request.max_budget_eur
        ]
        if request.preferred_type:
            typed = [w for w in within_budget if w.wine_type == request.preferred_type]
            if typed:
                return typed
        if not within_budget:
            raise ValueError(
                f"No wines found in cellar catalog within budget of "
                f"{request.max_budget_eur:.2f} €."
            )
        return within_budget

    def recommend_pairing(self, request: DishPairingRequest) -> PairingRecommendation:
        """Calculate optimal wine pairing using multi-vector sensory distance."""
        dish = self.get_dish_by_id(request.dish_id)
        if not dish:
            raise ValueError(f"Dish with id '{request.dish_id}' not found.")

        if self._session_factory is not None:
            top_matches = self._top_wines_db(self._session_factory, dish, request)
        else:
            candidates = self._select_candidates(request)
            top_matches = heapq.nsmallest(
                3,
                (
                    (
                        wine,
                        self.compute_compatibility_score(
                            dish.target_sensory, wine.sensory
                        ),
                    )
                    for wine in candidates
                ),
                key=lambda item: (-item[1], item[0].price_eur),
            )

        top_wine, top_score = top_matches[0]
        alternatives = [wine for wine, _ in top_matches[1:3]]

        explanation = self._generate_explanation(dish, top_wine, top_score)

        return PairingRecommendation(
            dish_name=dish.name,
            compatibility_score=top_score,
            primary_wine=top_wine,
            alternative_wines=alternatives,
            target_sensory=dish.target_sensory,
            sommelier_explanation=explanation,
        )

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
