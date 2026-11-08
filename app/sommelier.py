"""Curated enological database and multi-vector sommelier pairing engine."""

import math

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
        sensory=SensoryRadar(
            body=7.8, acidity=7.0, tannins=7.5, fruit=8.0, oak=8.5
        ),
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
        sensory=SensoryRadar(
            body=8.8, acidity=6.5, tannins=8.5, fruit=8.5, oak=8.0
        ),
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
        sensory=SensoryRadar(
            body=6.5, acidity=8.8, tannins=1.5, fruit=8.2, oak=2.0
        ),
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
        sensory=SensoryRadar(
            body=7.2, acidity=7.5, tannins=2.0, fruit=7.6, oak=6.5
        ),
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
        sensory=SensoryRadar(
            body=8.5, acidity=7.5, tannins=8.0, fruit=8.2, oak=7.5
        ),
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
        sensory=SensoryRadar(
            body=5.2, acidity=8.2, tannins=1.2, fruit=5.5, oak=3.5
        ),
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
        sensory=SensoryRadar(
            body=9.5, acidity=6.0, tannins=9.0, fruit=8.5, oak=8.5
        ),
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
        sensory=SensoryRadar(
            body=6.5, acidity=7.5, tannins=5.8, fruit=8.5, oak=5.2
        ),
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
        sensory=SensoryRadar(
            body=6.0, acidity=8.6, tannins=1.4, fruit=7.2, oak=4.0
        ),
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
        sensory=SensoryRadar(
            body=6.2, acidity=6.5, tannins=6.0, fruit=7.5, oak=6.5
        ),
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
        sensory=SensoryRadar(
            body=5.0, acidity=8.2, tannins=1.0, fruit=8.0, oak=1.0
        ),
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
        sensory=SensoryRadar(
            body=7.8, acidity=7.0, tannins=3.0, fruit=5.0, oak=8.2
        ),
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


class SommelierEngine:
    """Core mathematical pairing engine and enological knowledge catalog."""

    # Maximum possible distance in 5D space bounded within [1.0, 10.0]: sqrt(5 * 9^2) ≈ 20.12461
    MAX_EUCLIDEAN_DISTANCE: float = math.sqrt(5 * (9.0**2))

    def __init__(
        self,
        wines: Optional[list[WineProfile]] = None,
        dishes: Optional[list[Dish]] = None,
    ) -> None:
        """Initialize engine with curated catalogs or custom datasets."""
        self._wines: list[WineProfile] = list(wines or CURATED_WINES)
        self._dishes: list[Dish] = list(dishes or CURATED_DISHES)
        self._dish_index: dict[str, Dish] = {d.id: d for d in self._dishes}
        self._wine_index: dict[str, WineProfile] = {w.id: w for w in self._wines}

    def get_wines(
        self,
        appellation: str | None = None,
        wine_type: WineType | None = None,
        max_price: float | None = None,
    ) -> list[WineProfile]:
        """Filter wines by designation of origin, wine type, or maximum budget."""
        results: list[WineProfile] = []
        for wine in self._wines:
            if (
                appellation
                and appellation.lower() not in wine.appellation.lower()
            ):
                continue
            if wine_type and wine.wine_type != wine_type:
                continue
            if max_price is not None and wine.price_eur > max_price:
                continue
            results.append(wine)
        return results

    def get_wine_by_id(self, wine_id: str) -> WineProfile | None:
        """Fetch a single wine by its unique slug identifier."""
        return self._wine_index.get(wine_id)

    def get_dishes(self) -> list[Dish]:
        """Return all cataloged dishes."""
        return list(self._dishes)

    def get_dish_by_id(self, dish_id: str) -> Dish | None:
        """Fetch a single dish by its unique slug identifier."""
        return self._dish_index.get(dish_id)

    def get_regions(self) -> list[RegionSummary]:
        """Aggregate wine catalog by Designation of Origin (appellation)."""
        counts: dict[str, int] = {}
        for wine in self._wines:
            counts[wine.appellation] = counts.get(wine.appellation, 0) + 1

        climate_map = {
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

        summaries: list[RegionSummary] = []
        for app, count in counts.items():
            climate = climate_map.get(
                app, "Mediterráneo continental característico"
            )
            summaries.append(
                RegionSummary(
                    appellation=app, wine_count=count, climate_type=climate
                )
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

    def recommend_pairing(
        self, request: DishPairingRequest
    ) -> PairingRecommendation:
        """Calculate optimal wine pairing using multi-vector sensory distance."""
        dish = self.get_dish_by_id(request.dish_id)
        if not dish:
            raise ValueError(f"Dish with id '{request.dish_id}' not found.")

        # Candidate pool matching budget and optional preferred wine type
        candidates: list[WineProfile] = []
        for wine in self._wines:
            if wine.price_eur > request.max_budget_eur:
                continue
            if (
                request.preferred_type
                and wine.wine_type != request.preferred_type
            ):
                continue
            candidates.append(wine)

        # Fallback: If no wines fit budget with the preferred type, relax type filter
        if not candidates and request.preferred_type:
            candidates = [
                w for w in self._wines if w.price_eur <= request.max_budget_eur
            ]

        if not candidates:
            raise ValueError(
                f"No wines found in cellar catalog within budget of {request.max_budget_eur:.2f} €."
            )

        # Rank candidates by compatibility score descending, then by price ascending
        scored_wines = [
            (
                wine,
                self.compute_compatibility_score(
                    dish.target_sensory, wine.sensory
                ),
            )
            for wine in candidates
        ]
        scored_wines.sort(key=lambda item: (-item[1], item[0].price_eur))

        top_wine, top_score = scored_wines[0]
        alternatives = [wine for wine, _ in scored_wines[1:3]]

        explanation = self._generate_explanation(dish, top_wine, top_score)

        return PairingRecommendation(
            dish_name=dish.name,
            compatibility_score=top_score,
            primary_wine=top_wine,
            alternative_wines=alternatives,
            target_sensory=dish.target_sensory,
            sommelier_explanation=explanation,
        )

    def _generate_explanation(
        self, dish: Dish, wine: WineProfile, score: float
    ) -> str:
        """Generate enological rationale for harmony between dish and wine."""
        return (
            f"Maridaje de alta afinidad ({score:.1f}% de afinidad sensorial). "
            f"Para el plato '{dish.name}', la estructura de '{wine.name}' ({wine.appellation}) "
            f"proporciona un equilibrio sobresaliente: sus {wine.sensory.body:.1f}/10 de cuerpo "
            f"y {wine.sensory.tannins:.1f}/10 de taninos envuelven la textura del plato, "
            f"mientras que su acidez de {wine.sensory.acidity:.1f}/10 limpia el paladar. "
            f"Servir a {wine.serving_temp_c:.0f}°C en copa {wine.glass_type}"
            f"{f' tras {wine.decant_minutes} min de decantación' if wine.decant_minutes > 0 else ''}."
        )
