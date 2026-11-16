"""Curated enological database and multi-vector sommelier pairing engine."""

import heapq
import math
import uuid
from typing import Any

from sqlalchemy import Engine, func, inspect, or_, select, text
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.models import CellarItemModel, DishModel, WineModel
from app.schemas import (
    CellarCreateRequest,
    CellarItem,
    Dish,
    DishPairingRequest,
    GeoJsonFeature,
    GeoJsonFeatureCollection,
    GeoJsonGeometry,
    PairingRecommendation,
    RegionSummary,
    SensoryRadar,
    WineProfile,
    WineType,
)

# Curated reference catalog of premier Spanish wines across 12 major D.O.s (36 authentic wines)
CURATED_WINES: list[WineProfile] = [
    # 1. D.O.Ca. Rioja
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
        latitude=42.5735,
        longitude=-2.8521,
        altitude_m=580,
        soil_type="Arcilloso-calcáreo",
        climate="Continental templado con influencia atlántica",
        aging_potential_years=15,
        tagline="Elegancia clásica riojana de taninos sedosos y crianza pausada en roble americano.",
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
        latitude=42.5621,
        longitude=-2.8502,
        altitude_m=520,
        soil_type="Arcilloso",
        climate="Continental templado",
        aging_potential_years=6,
        tagline="Fruta roja vibrante, vainilla balsámica y trago envolvente.",
    ),
    WineProfile(
        id="castillo-ygay-gran-reserva",
        name="Castillo Ygay Gran Reserva Especial",
        winery="Marqués de Murrieta",
        appellation="D.O.Ca. Rioja",
        wine_type=WineType.RED,
        vintage=2012,
        price_eur=220.0,
        serving_temp_c=18.0,
        decant_minutes=60,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=8.5, acidity=7.8, tannins=8.2, fruit=8.0, oak=9.2),
        tasting_notes="Icono mundial. Ensamblaje magistral de Tempranillo y Mazuelo con décadas de potencial. Trufa negra, ebanistería y ciruela pasa.",
        latitude=42.4412,
        longitude=-2.3985,
        altitude_m=485,
        soil_type="Arcilloso-calcáreo con cantos",
        climate="Continental templado",
        aging_potential_years=30,
        tagline="Icono universal de elegancia aristocrática, trufa negra y persistencia sin fin.",
    ),
    # 2. D.O. Ribera del Duero
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
        latitude=41.5976,
        longitude=-4.1165,
        altitude_m=850,
        soil_type="Calizo y margas",
        climate="Mediterráneo continental extremo",
        aging_potential_years=12,
        tagline="Potencia envolvente con tanino dulce y madurez voluptuosa de fruta negra.",
    ),
    WineProfile(
        id="vega-sicilia-unico",
        name="Vega Sicilia Único",
        winery="Bodegas Vega Sicilia",
        appellation="D.O. Ribera del Duero",
        wine_type=WineType.RED,
        vintage=2014,
        price_eur=495.0,
        serving_temp_c=18.0,
        decant_minutes=60,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=9.2, acidity=8.0, tannins=8.8, fruit=8.6, oak=9.0),
        tasting_notes="Mito enológico. Crianza legendaria de casi 10 años en madera y botella. Finura inigualable, notas de cedro, tabaco habano y grosella.",
        latitude=41.6142,
        longitude=-4.2635,
        altitude_m=750,
        soil_type="Aluvial calcáreo",
        climate="Mediterráneo continental extremo",
        aging_potential_years=40,
        tagline="La leyenda viva del vino español, finura infinita y complejidad intemporal.",
    ),
    WineProfile(
        id="pesquera-crianza",
        name="Tinto Pesquera Crianza",
        winery="Familia Fernández Rivera",
        appellation="D.O. Ribera del Duero",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=24.0,
        serving_temp_c=16.0,
        decant_minutes=20,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=7.5, acidity=6.8, tannins=7.5, fruit=8.2, oak=7.2),
        tasting_notes="El pionero del estilo moderno ribereño. 100% Tempranillo con fruta negra, regaliz balsámico y roble americano especiado.",
        latitude=41.6425,
        longitude=-4.0950,
        altitude_m=800,
        soil_type="Pardo-calizo arcilloso",
        climate="Mediterráneo continental extremo",
        aging_potential_years=8,
        tagline="Pionero del renacer ribereño, fruta madura y tostados nobles.",
    ),
    # 3. D.O.Q. Priorat
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
        latitude=41.1895,
        longitude=0.8145,
        altitude_m=450,
        soil_type="Pizarra licorella",
        climate="Mediterráneo de montaña sobre pizarra licorella",
        aging_potential_years=10,
        tagline="Mineralidad telúrica de bancales escarpados y garnachas centenarias.",
    ),
    WineProfile(
        id="clos-mogador",
        name="Clos Mogador",
        winery="Clos Mogador",
        appellation="D.O.Q. Priorat",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=95.0,
        serving_temp_c=17.0,
        decant_minutes=60,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=9.0, acidity=7.6, tannins=8.5, fruit=8.5, oak=8.2),
        tasting_notes="El renacimiento del Priorat creado por René Barbier. Profundo, denso, balsámico, con flores azules, romero y mineralidad volcánica.",
        latitude=41.1925,
        longitude=0.8220,
        altitude_m=400,
        soil_type="Pizarra licorella pura",
        climate="Mediterráneo de montaña sobre pizarra licorella",
        aging_potential_years=25,
        tagline="Profundidad colosal, fruta balsámica y el alma renacida del Priorat.",
    ),
    WineProfile(
        id="vall-llach-idits",
        name="Idits de Vall Llach",
        winery="Celler Vall Llach",
        appellation="D.O.Q. Priorat",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=29.0,
        serving_temp_c=16.0,
        decant_minutes=30,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=7.8, acidity=7.2, tannins=7.5, fruit=8.0, oak=6.8),
        tasting_notes="Expresión fresca y directa de Porrera. Predominio de Cariñena de viñedos en pendiente, pimienta negra y frutos silvestres.",
        latitude=41.1960,
        longitude=0.8425,
        altitude_m=520,
        soil_type="Licorella desmenuzada",
        climate="Mediterráneo de montaña",
        aging_potential_years=8,
        tagline="Cariñenas y garnachas vibrantes con frescura especiada.",
    ),
    # 4. D.O. Rías Baixas
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
        latitude=42.5412,
        longitude=-8.6985,
        altitude_m=50,
        soil_type="Xabre granítico",
        climate="Atlántico húmedo y salino",
        aging_potential_years=15,
        tagline="El albariño de guarda más laureado con 30 meses de lías y noble hidrocarburo.",
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
        latitude=42.5025,
        longitude=-8.7845,
        altitude_m=35,
        soil_type="Granítico arenoso",
        climate="Atlántico húmedo y salino",
        aging_potential_years=4,
        tagline="Frescura atlántica cristalina con pomelo, manzana verde y notas salinas.",
    ),
    WineProfile(
        id="do-ferreiro-cepas-vellas",
        name="Do Ferreiro Cepas Vellas",
        winery="Bodegas Gerardo Méndez",
        appellation="D.O. Rías Baixas",
        wine_type=WineType.WHITE,
        vintage=2022,
        price_eur=38.0,
        serving_temp_c=11.0,
        decant_minutes=15,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.8, acidity=9.0, tannins=1.8, fruit=8.4, oak=2.5),
        tasting_notes="Cepas bicentenarias de pie franco en el valle de Salnés. Tensión eléctrica, notas ahumadas, salmuera y melocotón de viña.",
        latitude=42.5250,
        longitude=-8.7420,
        altitude_m=60,
        soil_type="Granito descompuesto",
        climate="Atlántico salino",
        aging_potential_years=18,
        tagline="Cepas bicentenarias de pie franco con acidez vertical y mineralidad profunda.",
    ),
    # 5. D.O. Bierzo
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
        latitude=42.6120,
        longitude=-6.8245,
        altitude_m=650,
        soil_type="Pizarra descompuesta",
        climate="Microclima de transición atlántico-continental",
        aging_potential_years=6,
        tagline="Fragancia de violetas, frambuesa fresca y fluidez atlántica de Mencía.",
    ),
    WineProfile(
        id="corullon-mencia",
        name="Villa de Corullón",
        winery="Descendientes de J. Palacios",
        appellation="D.O. Bierzo",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=48.0,
        serving_temp_c=16.0,
        decant_minutes=30,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=7.5, acidity=7.8, tannins=7.0, fruit=8.0, oak=6.5),
        tasting_notes="Pizarra escarpada en Corullón. Mencía de gran profundidad con notas ferruginosas, regaliz y hierba de montaña.",
        latitude=42.5780,
        longitude=-6.8210,
        altitude_m=720,
        soil_type="Pizarra ferrosa",
        climate="Atlántico-continental",
        aging_potential_years=15,
        tagline="El gran Cru berciano: austeridad mineral, tanino eléctrico y elegancia.",
    ),
    WineProfile(
        id="ultreia-saint-jacques",
        name="Ultreia Saint Jacques",
        winery="Raúl Pérez",
        appellation="D.O. Bierzo",
        wine_type=WineType.RED,
        vintage=2022,
        price_eur=14.5,
        serving_temp_c=15.0,
        decant_minutes=10,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.2, acidity=7.2, tannins=5.5, fruit=8.2, oak=4.5),
        tasting_notes="La magia de Raúl Pérez. Mencía, Bastardo y Garnacha Tintorera en roble usado. Terroso, jugoso y aromático.",
        latitude=42.5535,
        longitude=-6.7420,
        altitude_m=550,
        soil_type="Arcilla con canto y arena",
        climate="Atlántico-continental",
        aging_potential_years=7,
        tagline="El genio de Valtuille expresado en fruta roja directa, terrosa y envolvente.",
    ),
    # 6. D.O. Toro
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
        latitude=41.4820,
        longitude=-5.4120,
        altitude_m=750,
        soil_type="Arenoso-pedregoso sobre arcilla",
        climate="Continental árido de alta insolación",
        aging_potential_years=14,
        tagline="Poderío tánico domesticado con fruta negra opulenta y maderas balsámicas.",
    ),
    WineProfile(
        id="pintia-toro",
        name="Pintia",
        winery="Bodegas Pintia / Vega Sicilia",
        appellation="D.O. Toro",
        wine_type=WineType.RED,
        vintage=2018,
        price_eur=65.0,
        serving_temp_c=17.0,
        decant_minutes=45,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=9.2, acidity=6.5, tannins=8.8, fruit=8.6, oak=8.5),
        tasting_notes="Interpretación sublime de Toro por Vega Sicilia. Concentración refinada, moras silvestres, café tostado y textura aterciopelada.",
        latitude=41.5140,
        longitude=-5.3950,
        altitude_m=700,
        soil_type="Canto rodado aluvial",
        climate="Continental árido",
        aging_potential_years=16,
        tagline="La elegancia contemporánea de Toro: redondez, moras y final especiado.",
    ),
    WineProfile(
        id="numanthia",
        name="Numanthia",
        winery="Bodega Numanthia",
        appellation="D.O. Toro",
        wine_type=WineType.RED,
        vintage=2017,
        price_eur=55.0,
        serving_temp_c=17.0,
        decant_minutes=45,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=9.6, acidity=6.2, tannins=9.2, fruit=8.4, oak=8.8),
        tasting_notes="Viñas francas de más de 100 años. Fuerza colosal, cacao amargo, ciruela negra macerada y taninos densos y nobles.",
        latitude=41.5230,
        longitude=-5.3620,
        altitude_m=720,
        soil_type="Arcilla y grava",
        climate="Continental árido",
        aging_potential_years=20,
        tagline="Concentración legendaria de viñedos centenarios resistentes a la filoxera.",
    ),
    # 7. D.O. Jerez-Xérès-Sherry
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
        latitude=36.6850,
        longitude=-6.1420,
        altitude_m=45,
        soil_type="Albariza deslumbrante",
        climate="Mediterráneo cálido con albariza oceánica",
        aging_potential_years=3,
        tagline="Velo de flor sin filtrar: salinidad punzante, almendra verde y levadura viva.",
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
        latitude=36.6820,
        longitude=-6.1360,
        altitude_m=50,
        soil_type="Albariza pura",
        climate="Mediterráneo cálido con albariza oceánica",
        aging_potential_years=20,
        tagline="Oxidación aristocrática: ebanistería noble, nuez tostada y final seco infinito.",
    ),
    WineProfile(
        id="valdespino-inocente-fino",
        name="Valdespino Fino Inocente",
        winery="Valdespino",
        appellation="D.O. Jerez-Xérès-Sherry",
        wine_type=WineType.FORTIFIED,
        vintage=2023,
        price_eur=18.0,
        serving_temp_c=8.0,
        decant_minutes=0,
        glass_type="Copita",
        sensory=SensoryRadar(body=5.4, acidity=8.4, tannins=1.3, fruit=5.2, oak=4.0),
        tasting_notes="El único fino fermentado en bota de roble y con 10 criaderas en Macharnudo Alto. Complejidad mineral insuperable.",
        latitude=36.6910,
        longitude=-6.1280,
        altitude_m=60,
        soil_type="Albariza de Macharnudo Alto",
        climate="Mediterráneo oceánico",
        aging_potential_years=5,
        tagline="El único fino fermentado en bota de roble americano por el sistema de 10 criaderas.",
    ),
    # 8. D.O. Rueda
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
        latitude=41.3850,
        longitude=-4.9540,
        altitude_m=750,
        soil_type="Canto rodado sobre arcilla",
        climate="Continental de meseta",
        aging_potential_years=10,
        tagline="El Verdejo de guarda por antonomasia: untuosidad bordelesa y flor blanca.",
    ),
    WineProfile(
        id="jose-pariente-verdejo",
        name="José Pariente Verdejo",
        winery="Bodegas José Pariente",
        appellation="D.O. Rueda",
        wine_type=WineType.WHITE,
        vintage=2023,
        price_eur=11.0,
        serving_temp_c=9.0,
        decant_minutes=0,
        glass_type="Tulipa",
        sensory=SensoryRadar(body=5.2, acidity=8.0, tannins=1.2, fruit=8.2, oak=1.0),
        tasting_notes="Expresión varietal pura: hierba fresca, anís, hinojo y pomelo con paso crujiente y agradable amargor varietal.",
        latitude=41.4020,
        longitude=-4.9720,
        altitude_m=730,
        soil_type="Cascajoso pedregoso",
        climate="Continental de meseta",
        aging_potential_years=3,
        tagline="Expresión clásica de hierba fresca recién cortada, hinojo y fruta de hueso.",
    ),
    WineProfile(
        id="ossian-vinas-viejas",
        name="Ossian Viñas Viejas",
        winery="Ossian Vides y Vinos",
        appellation="D.O. Rueda",
        wine_type=WineType.WHITE,
        vintage=2021,
        price_eur=32.0,
        serving_temp_c=12.0,
        decant_minutes=20,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=7.0, acidity=7.8, tannins=1.8, fruit=7.8, oak=6.0),
        tasting_notes="Verdejo prefiloxérico en Nieva sobre arenas puras. Complejidad aromática, salinidad, cítricos maduros y gran textura grasa.",
        latitude=41.1240,
        longitude=-4.5120,
        altitude_m=880,
        soil_type="Arenas silíceas prefiloxéricas",
        climate="Continental extremo",
        aging_potential_years=12,
        tagline="Verdejo centenario segoviano fermentado en barrica con sapidez y cuerpo.",
    ),
    # 9. D.O. Cava / Corpinnat
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
        latitude=41.4285,
        longitude=1.7890,
        altitude_m=220,
        soil_type="Arcillo-calcáreo con limo",
        climate="Mediterráneo marítimo templado",
        aging_potential_years=8,
        tagline="Más de 50 meses de rima: burbuja cremosa, brioche y acidez gastronómica.",
    ),
    WineProfile(
        id="recaredo-terrers-brut-nature",
        name="Recaredo Terrers Brut Nature",
        winery="Recaredo",
        appellation="D.O. Corpinnat / Penedès",
        wine_type=WineType.SPARKLING,
        vintage=2019,
        price_eur=32.0,
        serving_temp_c=9.0,
        decant_minutes=0,
        glass_type="Tulipa",
        sensory=SensoryRadar(body=6.2, acidity=8.8, tannins=1.5, fruit=7.0, oak=3.5),
        tasting_notes="Biodinámica pura y crianza con tapón de corcho natural. Tensión mineral, hierbas secas, burbuja microscópica y final seco.",
        latitude=41.4240,
        longitude=1.7820,
        altitude_m=250,
        soil_type="Calcáreo limoso",
        climate="Mediterráneo marítimo templado",
        aging_potential_years=10,
        tagline="Biodinámica rigurosa, tapón de corcho en rima y sequedad salina insuperable.",
    ),
    WineProfile(
        id="llopart-leopardi",
        name="Llopart Leopardi Brut Nature",
        winery="Cava Llopart",
        appellation="D.O. Corpinnat / Penedès",
        wine_type=WineType.SPARKLING,
        vintage=2017,
        price_eur=25.0,
        serving_temp_c=8.0,
        decant_minutes=0,
        glass_type="Tulipa",
        sensory=SensoryRadar(body=5.8, acidity=8.5, tannins=1.3, fruit=7.4, oak=3.8),
        tasting_notes="Viñedos de montaña en Subirats. Crianza larga con recuerdos a frutos secos, mantequilla fresca y burbuja integrada.",
        latitude=41.4080,
        longitude=1.8120,
        altitude_m=340,
        soil_type="Calizo fósil de montaña",
        climate="Mediterráneo",
        aging_potential_years=8,
        tagline="Elegancia centenaria con finas notas tostadas y crema pastelera.",
    ),
    # 10. D.O. Ribeira Sacra
    WineProfile(
        id="guimaro-finca-meixeman",
        name="Guímaro Finca Meixemán",
        winery="Adega Guímaro",
        appellation="D.O. Ribeira Sacra",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=28.0,
        serving_temp_c=15.0,
        decant_minutes=20,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.8, acidity=7.8, tannins=6.2, fruit=8.2, oak=5.5),
        tasting_notes="Viticultura heroica en los cañones del Sil. Mencía y uvas autóctonas en bancales de pizarra. Fruta silvestre, grafito y pimienta.",
        latitude=42.4280,
        longitude=-7.4850,
        altitude_m=420,
        soil_type="Pizarra y esquisto en bancales",
        climate="Atlántico-continental",
        aging_potential_years=10,
        tagline="Viticultura heroica de cañones del Sil: notas minerales, grosella y frescor.",
    ),
    WineProfile(
        id="ponte-da-boga-bancales",
        name="Ponte da Boga Bancales Ya Hablados",
        winery="Adega Ponte da Boga",
        appellation="D.O. Ribeira Sacra",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=22.0,
        serving_temp_c=15.0,
        decant_minutes=15,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.5, acidity=7.6, tannins=6.0, fruit=8.0, oak=5.0),
        tasting_notes="Laderas abruptas sobre el río Bibei. Mencía fluida con recuerdos a hojas secas, frambuesa y frescura atlántica.",
        latitude=42.3920,
        longitude=-7.3150,
        altitude_m=500,
        soil_type="Pizarra y granito en pendiente",
        climate="Atlántico-continental",
        aging_potential_years=8,
        tagline="Mencía de vértigo con aromas balsámicos y trago sedoso de montaña.",
    ),
    WineProfile(
        id="lalama-dominio-do-bibei",
        name="Lalama",
        winery="Dominio do Bibei",
        appellation="D.O. Ribeira Sacra",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=24.0,
        serving_temp_c=16.0,
        decant_minutes=20,
        glass_type="Borgoña",
        sensory=SensoryRadar(body=6.7, acidity=7.9, tannins=6.2, fruit=8.3, oak=5.2),
        tasting_notes="Arquitectura y viñedo integrados. Mencía con Brancellao y Mouratón en barricas y tinos usados. Finura atlántica sublime.",
        latitude=42.3680,
        longitude=-7.2180,
        altitude_m=600,
        soil_type="Granito y arcilla esquistosa",
        climate="Atlántico-continental",
        aging_potential_years=12,
        tagline="Finura casi borgoñona con especias silvestres y acidez vibrante.",
    ),
    # 11. D.O. Somontano
    WineProfile(
        id="blecua-somontano",
        name="Blecua",
        winery="Viñas del Vero / Blecua",
        appellation="D.O. Somontano",
        wine_type=WineType.RED,
        vintage=2017,
        price_eur=98.0,
        serving_temp_c=17.0,
        decant_minutes=45,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=8.8, acidity=6.8, tannins=8.5, fruit=8.2, oak=8.8),
        tasting_notes="El gran vino de autor del Somontano. Coupage bordelés y mediterráneo. Taninos maduros, chocolate negro, ciruela y tabaco rubio.",
        latitude=42.0350,
        longitude=0.1280,
        altitude_m=550,
        soil_type="Aluvial franco-arenoso",
        climate="Continental prepirenaico",
        aging_potential_years=20,
        tagline="El vino de culto del Somontano: ensamblaje magistral, tanino maduro y cacao.",
    ),
    WineProfile(
        id="enate-cabernet-merlot",
        name="Enate Cabernet Sauvignon-Merlot",
        winery="Bodegas Enate",
        appellation="D.O. Somontano",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=10.5,
        serving_temp_c=16.0,
        decant_minutes=15,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=7.0, acidity=6.6, tannins=7.0, fruit=7.8, oak=6.5),
        tasting_notes="Equilibrio aromático del pie de los Pirineos. Pimiento rojo asado, grosella negra, tofe y paso amplio y sedoso.",
        latitude=42.0620,
        longitude=0.1740,
        altitude_m=600,
        soil_type="Calizo y pedregoso",
        climate="Continental prepirenaico",
        aging_potential_years=8,
        tagline="Perfil atlántico-pirenaico con pimiento asado, ciruela negra y especias dulces.",
    ),
    WineProfile(
        id="vinas-del-vero-gran-vos",
        name="Viñas del Vero Gran Vos Reserva",
        winery="Viñas del Vero",
        appellation="D.O. Somontano",
        wine_type=WineType.RED,
        vintage=2018,
        price_eur=18.5,
        serving_temp_c=16.0,
        decant_minutes=20,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=7.6, acidity=6.7, tannins=7.5, fruit=8.0, oak=7.2),
        tasting_notes="Reserva elaborado con las mejores uvas tintas de la bodega. Notas de zarzamora, torrefacto, vainilla y final largo.",
        latitude=42.0410,
        longitude=0.1350,
        altitude_m=520,
        soil_type="Franco-calizo",
        climate="Continental prepirenaico",
        aging_potential_years=10,
        tagline="Reserva aromático con mora confitada, cedro y cuerpo equilibrado.",
    ),
    # 12. D.O. Jumilla
    WineProfile(
        id="clio-jumilla",
        name="Clio",
        winery="Bodegas El Nido",
        appellation="D.O. Jumilla",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=48.0,
        serving_temp_c=17.0,
        decant_minutes=45,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=9.4, acidity=6.2, tannins=8.8, fruit=8.8, oak=8.5),
        tasting_notes="70% Monastrell de viñas viejas y 30% Cabernet Sauvignon. Poder colosal, arándano maduro, moca, regaliz y textura suntuosa.",
        latitude=38.4750,
        longitude=-1.3280,
        altitude_m=800,
        soil_type="Calizo pedregoso sobre tosca",
        climate="Mediterráneo seco y soleado",
        aging_potential_years=15,
        tagline="Monastrell y Cabernet de opulencia arrolladora, torrefacto y arándanos maduros.",
    ),
    WineProfile(
        id="el-nido-jumilla",
        name="El Nido",
        winery="Bodegas El Nido",
        appellation="D.O. Jumilla",
        wine_type=WineType.RED,
        vintage=2020,
        price_eur=140.0,
        serving_temp_c=17.0,
        decant_minutes=60,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=9.7, acidity=6.4, tannins=9.0, fruit=9.0, oak=9.0),
        tasting_notes="La cúspide del sureste español. 70% Cabernet Sauvignon y 30% Monastrell. Intensidad abrumadora de fruta negra, cacao y especias nobles.",
        latitude=38.4760,
        longitude=-1.3290,
        altitude_m=820,
        soil_type="Caliza superficial extrema",
        climate="Mediterráneo seco",
        aging_potential_years=20,
        tagline="La joya de la corona del Levante: terciopelo concentrado y estela interminable.",
    ),
    WineProfile(
        id="juan-gil-etiqueta-plata",
        name="Juan Gil Etiqueta Plata",
        winery="Bodegas Juan Gil",
        appellation="D.O. Jumilla",
        wine_type=WineType.RED,
        vintage=2021,
        price_eur=14.5,
        serving_temp_c=16.0,
        decant_minutes=15,
        glass_type="Burdeos",
        sensory=SensoryRadar(body=8.2, acidity=6.0, tannins=7.8, fruit=8.5, oak=7.5),
        tasting_notes="100% Monastrell de cepas viejas. Gran concentración de fruta madura, grosella roja, recuerdos a torrefacto y trago envolvente.",
        latitude=38.5620,
        longitude=-1.3050,
        altitude_m=750,
        soil_type="Franco-arenoso calizo",
        climate="Mediterráneo seco",
        aging_potential_years=6,
        tagline="Monastrell goloso de viñas viejas con notas de ciruela pasa y roble tostado.",
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
    Dish(
        id="rodaballo-brasa",
        name="Rodaballo salvaje a la brasa con refrito de ajos",
        category="Pescados y Mariscos",
        description="Pescado plano atlántico asado entero a la parrilla con su piel gelatinosa, emulsión de colágeno y vinagre de sidra.",
        target_sensory=SensoryRadar(
            body=6.8, acidity=8.0, tannins=1.8, fruit=7.5, oak=5.5
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="paella-valenciana",
        name="Paella valenciana tradicional a leña de naranjo",
        category="Arroces",
        description="Arroz seco en paella con pollo de corral, conejo, garrofó, judía ferradura y socarrat aromático de romero.",
        target_sensory=SensoryRadar(
            body=6.0, acidity=7.5, tannins=3.0, fruit=7.8, oak=2.5
        ),
        suggested_wine_type=WineType.ROSE,
    ),
    Dish(
        id="carrilleras-ibericas",
        name="Carrilleras ibéricas estofadas al vino tinto",
        category="Carnes",
        description="Cocción lenta de carrillera de cerdo ibérico en reducción de vino, chalotas y cacao amargo con textura melosa.",
        target_sensory=SensoryRadar(
            body=8.5, acidity=7.0, tannins=7.8, fruit=8.0, oak=7.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="rabo-toro",
        name="Rabo de toro estofado a la cordobesa",
        category="Carnes",
        description="Guiso tradicional de larga cocción con vino oloroso, verduras pochadas y salsa gelatinosa de gran intensidad.",
        target_sensory=SensoryRadar(
            body=9.2, acidity=6.8, tannins=8.2, fruit=7.5, oak=8.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="salmorejo-cordobes",
        name="Salmorejo cordobés con virutas de jamón ibérico",
        category="Entrantes y Cuchara",
        description="Crema fría emulsionada de tomate maduro, pan de telera y aceite de oliva virgen extra picual.",
        target_sensory=SensoryRadar(
            body=5.8, acidity=8.2, tannins=1.5, fruit=8.0, oak=2.0
        ),
        suggested_wine_type=WineType.SPARKLING,
    ),
    Dish(
        id="ostras-gallegas",
        name="Ostras planas de la Ría de Arousa al natural",
        category="Pescados y Mariscos",
        description="Ostra rizada fresca servida sobre hielo picado con salitre oceánico y acidez marina cortante.",
        target_sensory=SensoryRadar(
            body=4.0, acidity=9.5, tannins=1.0, fruit=7.0, oak=1.0
        ),
        suggested_wine_type=WineType.WHITE,
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
    "D.O. Ribeira Sacra": "Atlántico de transición en cañones fluviales",
    "D.O. Somontano": "Continental prepirenaico de alta luminosidad",
    "D.O. Jumilla": "Mediterráneo seco y semiárido de altiplano",
}

DO_METADATA: dict[str, dict[str, Any]] = {
    "D.O.Ca. Rioja": {
        "appellation": "D.O.Ca. Rioja",
        "autonomous_community": "La Rioja / País Vasco / Navarra",
        "climate": "Continental templado con influencia atlántica",
        "soil": "Arcilloso-calcáreo, arcillo-ferroso y aluvial",
        "altitude_range_m": "450 - 700 m",
        "signature_grape": "Tempranillo, Garnacha, Graciano, Mazuelo",
        "center": [-2.6000, 42.4500],
        "description": "Cuna histórica del roble y la elegancia clásica de guarda española.",
    },
    "D.O. Ribera del Duero": {
        "appellation": "D.O. Ribera del Duero",
        "autonomous_community": "Castilla y León",
        "climate": "Mediterráneo continental extremo",
        "soil": "Calizo, margas y terrazas aluviales",
        "altitude_range_m": "750 - 850 m",
        "signature_grape": "Tempranillo (Tinta del País / Tinto Fino)",
        "center": [-4.1000, 41.6200],
        "description": "Terruño de meseta de oscilación térmica extrema y taninos colosales.",
    },
    "D.O.Q. Priorat": {
        "appellation": "D.O.Q. Priorat",
        "autonomous_community": "Cataluña",
        "climate": "Mediterráneo de montaña sobre pizarra licorella",
        "soil": "Pizarra licorella desmenuzada y escarpada",
        "altitude_range_m": "400 - 520 m",
        "signature_grape": "Garnacha Tinta, Cariñena (Mazuelo)",
        "center": [0.8250, 41.1920],
        "description": "Bancales heroicos de mineralidad telúrica y concentración casi mística.",
    },
    "D.O. Rías Baixas": {
        "appellation": "D.O. Rías Baixas",
        "autonomous_community": "Galicia",
        "climate": "Atlántico húmedo y salino",
        "soil": "Xabre granítico descompuesto y arenoso",
        "altitude_range_m": "35 - 60 m",
        "signature_grape": "Albariño",
        "center": [-8.7400, 42.5200],
        "description": "Salinidad oceánica, acidez eléctrica y albariños de longevidad insospechada.",
    },
    "D.O. Bierzo": {
        "appellation": "D.O. Bierzo",
        "autonomous_community": "Castilla y León",
        "climate": "Microclima de transición atlántico-continental",
        "soil": "Pizarra ferrosa y laderas de cuarcita",
        "altitude_range_m": "550 - 720 m",
        "signature_grape": "Mencía, Godello",
        "center": [-6.7800, 42.5800],
        "description": "Fragancia de violetas, frescura silvestre y finura atlántica.",
    },
    "D.O. Toro": {
        "appellation": "D.O. Toro",
        "autonomous_community": "Castilla y León",
        "climate": "Continental árido de alta insolación",
        "soil": "Arenoso-pedregoso sobre arcilla profunda",
        "altitude_range_m": "700 - 750 m",
        "signature_grape": "Tinta de Toro (Tempranillo autóctono)",
        "center": [-5.3900, 41.5000],
        "description": "Viñedos centenarios prefiloxéricos de potencia tánica y fruta negra.",
    },
    "D.O. Jerez-Xérès-Sherry": {
        "appellation": "D.O. Jerez-Xérès-Sherry",
        "autonomous_community": "Andalucía",
        "climate": "Mediterráneo cálido con albariza oceánica",
        "soil": "Albariza blanca deslumbrante rica en carbonato cálcico",
        "altitude_range_m": "45 - 60 m",
        "signature_grape": "Palomino Fino, Pedro Ximénez",
        "center": [-6.1350, 36.6850],
        "description": "Crianza biológica bajo velo de flor y soleras centenarias de oxidación noble.",
    },
    "D.O. Rueda": {
        "appellation": "D.O. Rueda",
        "autonomous_community": "Castilla y León",
        "climate": "Continental de meseta",
        "soil": "Cascajoso pedregoso con canto rodado sobre arcilla",
        "altitude_range_m": "730 - 880 m",
        "signature_grape": "Verdejo",
        "center": [-4.9500, 41.3850],
        "description": "Aromas herbáceos, hinojo silvestre y verdejos de guarda con barrica.",
    },
    "D.O. Corpinnat / Penedès": {
        "appellation": "D.O. Corpinnat / Penedès",
        "autonomous_community": "Cataluña",
        "climate": "Mediterráneo marítimo templado",
        "soil": "Arcillo-calcáreo con limo y calizo fósil",
        "altitude_range_m": "220 - 340 m",
        "signature_grape": "Xarel·lo, Macabeo, Parellada",
        "center": [1.7900, 41.4200],
        "description": "Espumosos gastronómicos de larguísima rima y viticultura ecológica rigurosa.",
    },
    "D.O. Ribeira Sacra": {
        "appellation": "D.O. Ribeira Sacra",
        "autonomous_community": "Galicia",
        "climate": "Atlántico de transición en cañones fluviales",
        "soil": "Pizarra, esquisto y granito en bancales de vértigo",
        "altitude_range_m": "420 - 600 m",
        "signature_grape": "Mencía, Brancellao, Merenzao",
        "center": [-7.3500, 42.4000],
        "description": "Viticultura heroica en pendientes imposibles sobre los ríos Sil y Miño.",
    },
    "D.O. Somontano": {
        "appellation": "D.O. Somontano",
        "autonomous_community": "Aragón",
        "climate": "Continental prepirenaico de alta luminosidad",
        "soil": "Franco-calizo, arenisca y terrazas aluviales",
        "altitude_range_m": "520 - 600 m",
        "signature_grape": "Cabernet Sauvignon, Merlot, Tempranillo, Moristel",
        "center": [0.1450, 42.0450],
        "description": "Ensamblajes de autor al abrigo de las cumbres pirenaicas.",
    },
    "D.O. Jumilla": {
        "appellation": "D.O. Jumilla",
        "autonomous_community": "Región de Murcia",
        "climate": "Mediterráneo seco y semiárido de altiplano",
        "soil": "Calizo pedregoso sobre tosca dura",
        "altitude_range_m": "750 - 820 m",
        "signature_grape": "Monastrell",
        "center": [-1.3250, 38.5000],
        "description": "Reino absoluto de la Monastrell sobre suelos áridos de altitud y sol implacable.",
    },
}


def _build_winery_feature(wine: WineProfile) -> GeoJsonFeature:
    """Build a GeoJSON Point feature for a curated winery label."""
    do_meta = DO_METADATA.get(wine.appellation, {})
    community = str(do_meta.get("autonomous_community", "España"))
    grape = str(do_meta.get("signature_grape", "Varietal autóctono"))
    summary = (
        f"{wine.winery} ({wine.appellation}) — {wine.name} ({wine.vintage}), "
        f"{wine.price_eur:.2f} €. {wine.tagline}"
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
            "sensory": wine.sensory.model_dump(),
        },
    )


def _build_region_feature(
    do_name: str, meta: dict[str, Any], wines: list[WineProfile]
) -> GeoJsonFeature:
    """Build a GeoJSON Point feature for a Designation of Origin centroid."""
    avg_alt = int(sum(w.altitude_m for w in wines) / len(wines)) if wines else 500
    bodegas = sorted(list(dict.fromkeys(w.winery for w in wines)))
    summary = (
        f"{do_name} ({len(wines)} vinos catalogados, {len(bodegas)} bodegas): "
        f"{', '.join(bodegas)}"
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
            "autonomous_community": str(meta.get("autonomous_community", "España")),
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


_WINE_MIGRATION_COLUMNS: tuple[tuple[str, str], ...] = (
    ("latitude", "FLOAT DEFAULT 40.4168"),
    ("longitude", "FLOAT DEFAULT -3.7038"),
    ("altitude_m", "INTEGER DEFAULT 500"),
    ("soil_type", "VARCHAR(128) DEFAULT 'Arcilloso-calcáreo'"),
    ("climate", "VARCHAR(128) DEFAULT 'Continental'"),
    ("aging_potential_years", "INTEGER DEFAULT 5"),
    ("tagline", "VARCHAR(256) DEFAULT ''"),
)


def _ensure_wine_terroir_columns(db_engine: Engine) -> None:
    """Add new terroir columns to existing SQLite wines table if missing."""
    inspector = inspect(db_engine)
    if "wines" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("wines")}
    with db_engine.begin() as conn:
        for col_name, col_def in _WINE_MIGRATION_COLUMNS:
            if col_name not in existing:
                stmt_sql = f"ALTER TABLE wines ADD COLUMN {col_name} {col_def}"
                conn.execute(text(stmt_sql))  # nosec B608


def init_db(db_engine: Engine, session_factory: sessionmaker[Session]) -> None:
    """Create database tables and seed missing curated wines and dishes."""
    Base.metadata.create_all(bind=db_engine)
    _ensure_wine_terroir_columns(db_engine)
    with session_factory() as session:
        existing_wines = set(session.scalars(select(WineModel.id)).all())
        missing_wines = [
            WineModel.from_schema(w)
            for w in CURATED_WINES
            if w.id not in existing_wines
        ]
        if missing_wines:
            session.add_all(missing_wines)

        existing_dishes = set(session.scalars(select(DishModel.id)).all())
        missing_dishes = [
            DishModel.from_schema(d)
            for d in CURATED_DISHES
            if d.id not in existing_dishes
        ]
        if missing_dishes:
            session.add_all(missing_dishes)
        session.commit()


class SommelierEngine:
    """Core mathematical pairing engine and enological knowledge catalog."""

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
            search = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    WineModel.name.ilike(search),
                    WineModel.winery.ilike(search),
                    WineModel.appellation.ilike(search),
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
            return self._get_dishes_db(
                self._session_factory,
                category=category,
                q=q,
                limit=limit,
                offset=offset,
            )

        query = q.lower().strip() if q else None
        results = [
            dish
            for dish in self._dishes
            if (not category or dish.category.lower() == category.lower())
            and (
                not query
                or query in dish.name.lower()
                or query in dish.description.lower()
            )
        ]
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
        if self._session_factory is not None:
            with self._session_factory() as session:
                row = session.get(DishModel, dish_id)
                return row.to_schema() if row else None
        return self._dish_index.get(dish_id)

    def get_regions(self) -> list[RegionSummary]:
        """Return summary of all Appellations and their wine representation count."""
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
                        autonomous_community=DO_METADATA.get(app, {}).get(
                            "autonomous_community"
                        ),
                        signature_grape=DO_METADATA.get(app, {}).get("signature_grape"),
                        soil=DO_METADATA.get(app, {}).get("soil"),
                        coordinates=DO_METADATA.get(app, {}).get("center"),
                    )
                    for app, count in rows
                ]

        counts: dict[str, int] = {}
        for wine in self._wines:
            counts[wine.appellation] = counts.get(wine.appellation, 0) + 1

        summaries: list[RegionSummary] = []
        for app, count in counts.items():
            climate = CLIMATE_MAP.get(app, "Mediterráneo continental característico")
            meta = DO_METADATA.get(app, {})
            summaries.append(
                RegionSummary(
                    appellation=app,
                    wine_count=count,
                    climate_type=climate,
                    autonomous_community=meta.get("autonomous_community"),
                    signature_grape=meta.get("signature_grape"),
                    soil=meta.get("soil"),
                    coordinates=meta.get("center"),
                )
            )
        return sorted(summaries, key=lambda r: r.wine_count, reverse=True)

    def get_atlas_geojson(self, layer: str = "wineries") -> GeoJsonFeatureCollection:
        """Return GeoJSON FeatureCollection of Spanish wine regions and/or wineries."""
        features: list[GeoJsonFeature] = []
        wines = self.get_wines(limit=100)

        if layer in ("wineries", "all"):
            for wine in wines:
                features.append(_build_winery_feature(wine))

        if layer in ("regions", "all"):
            for do_name, meta in DO_METADATA.items():
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
        )

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
