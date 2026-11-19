"""Curated European gastronomic catalog of 45 dishes across 9 culinary sections."""

from app.schemas import Dish, SensoryRadar, WineType

CURATED_DISHES: list[Dish] = [
    # --- 1. Entrantes y Cuchara (4 dishes) ---
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
        id="fabada-asturiana",
        name="Fabada asturiana con compango ahumado",
        category="Entrantes y Cuchara",
        description="Fabas de la Granja con chorizo asturiano, morcilla y lacón curado al humo de roble.",
        target_sensory=SensoryRadar(
            body=8.5, acidity=6.5, tannins=7.0, fruit=7.0, oak=6.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="soupe-a-loignon",
        name="Soupe à l'Oignon gratinée con queso Gruyère",
        category="Entrantes y Cuchara",
        description="Clásica sopa francesa de cebolla caramelizada lentamente en caldo de buey, pan tostado y costra gratinada de Gruyère.",
        target_sensory=SensoryRadar(
            body=6.8, acidity=7.8, tannins=2.5, fruit=7.2, oak=5.0
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="bouillabaisse-marsella",
        name="Bouillabaisse de Marsella con rouille y azafrán",
        category="Entrantes y Cuchara",
        description="Sopa provenzal de pescados de roca del Mediterráneo con hinojo, azafrán, piel de naranja y salsa rouille sobre picatostes.",
        target_sensory=SensoryRadar(
            body=6.4, acidity=8.2, tannins=1.8, fruit=8.0, oak=2.5
        ),
        suggested_wine_type=WineType.ROSE,
    ),
    # --- 2. Ensaladas y Huerta (4 dishes) ---
    Dish(
        id="escalivada-catalana",
        name="Escalivada tibia a la brasa con ventresca",
        category="Ensaladas y Huerta",
        description="Pimientos, berenjenas y cebollas asadas a la brasa de sarmiento con ventresca de bonito del norte y AOVE.",
        target_sensory=SensoryRadar(
            body=5.5, acidity=7.5, tannins=3.0, fruit=7.5, oak=3.0
        ),
        suggested_wine_type=WineType.ROSE,
    ),
    Dish(
        id="menestra-tudela",
        name="Menestra de verduras de la Ribera de Tudela",
        category="Ensaladas y Huerta",
        description="Alcachofas, espárragos blancos, guisantes lágrima y habitas tiernas estofadas con jamón serrano.",
        target_sensory=SensoryRadar(
            body=5.0, acidity=8.5, tannins=2.0, fruit=7.0, oak=2.0
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="burrata-pugliese",
        name="Burrata Pugliese con tomates confitados y albahaca",
        category="Ensaladas y Huerta",
        description="Burrata artesanal de Apulia de corazón cremoso de stracciatella con tomates datterini asados, albahaca fresca y aceite virgen extra.",
        target_sensory=SensoryRadar(
            body=5.4, acidity=8.4, tannins=1.4, fruit=8.3, oak=1.4
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="salade-nicoise",
        name="Salade Niçoise tradicional de la Costa Azul",
        category="Ensaladas y Huerta",
        description="Atún fresco sellado, aceitunas negras de Niza, anchoas, judías verdes crujientes, huevo mollet y vinagreta provenzal.",
        target_sensory=SensoryRadar(
            body=5.2, acidity=8.3, tannins=1.5, fruit=8.2, oak=1.2
        ),
        suggested_wine_type=WineType.ROSE,
    ),
    # --- 3. Tapas y Pintxos (4 dishes) ---
    Dish(
        id="gilda-antxoa-piparra",
        name="Gilda donostiarra de anchoa del Cantábrico y piparra",
        category="Tapas y Pintxos",
        description="Pintxo clásico con aceituna manzanilla, piparra en vinagre de Ibarra y anchoa del Cantábrico en salazón.",
        target_sensory=SensoryRadar(
            body=3.5, acidity=9.5, tannins=1.0, fruit=6.0, oak=1.0
        ),
        suggested_wine_type=WineType.FORTIFIED,
    ),
    Dish(
        id="croquetas-jamon-iberico",
        name="Croquetas cremosas de jamón ibérico de bellota",
        category="Tapas y Pintxos",
        description="Bechamel fluida infusionada con hueso de jamón ibérico, crujiente rebozado en panko y virutas de bellota.",
        target_sensory=SensoryRadar(
            body=6.5, acidity=7.5, tannins=3.0, fruit=6.5, oak=3.5
        ),
        suggested_wine_type=WineType.SPARKLING,
    ),
    Dish(
        id="tartare-de-boeuf",
        name="Tartare de Boeuf francés cortado al cuchillo",
        category="Tapas y Pintxos",
        description="Solomillo de ternera picado a cuchillo con chalota, alcaparras, pepinillo, mostaza de Dijon, salsa Perrins y yema fresca.",
        target_sensory=SensoryRadar(
            body=6.6, acidity=8.0, tannins=5.8, fruit=8.4, oak=4.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="arancini-sicilianos",
        name="Arancini sicilianos de azafrán, ragú y scamorza",
        category="Tapas y Pintxos",
        description="Crujientes esferas doradas de arroz al azafrán rellenas de ragú lento, guisantes y queso fundente al estilo de Catania.",
        target_sensory=SensoryRadar(
            body=6.5, acidity=8.0, tannins=5.5, fruit=8.2, oak=3.8
        ),
        suggested_wine_type=WineType.RED,
    ),
    # --- 4. Embutidos y Quesos (4 dishes) ---
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
        id="plateau-comte-brie",
        name="Plateau de Comté 24 meses & Brie de Meaux",
        category="Embutidos y Quesos",
        description="Selección afinada de Comté alpino con cristales de tirosina y Brie de Meaux cremoso de leche cruda con nueces.",
        target_sensory=SensoryRadar(
            body=7.0, acidity=8.6, tannins=1.6, fruit=7.8, oak=5.2
        ),
        suggested_wine_type=WineType.SPARKLING,
    ),
    Dish(
        id="stilton-aged-cheddar",
        name="Stilton azul & Aged Somerset Cheddar británico",
        category="Embutidos y Quesos",
        description="Tabla clásica inglesa de Stilton azul cremoso y Cheddar madurado en tela 24 meses con chutney de higos y nueces.",
        target_sensory=SensoryRadar(
            body=8.8, acidity=7.2, tannins=2.5, fruit=8.8, oak=7.2
        ),
        suggested_wine_type=WineType.FORTIFIED,
    ),
    # --- 5. Pescados y Mariscos (5 dishes) ---
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
        id="ostras-gallegas",
        name="Ostras planas de la Ría de Arousa al natural",
        category="Pescados y Mariscos",
        description="Ostra rizada fresca servida sobre hielo picado con salitre oceánico y acidez marina cortante.",
        target_sensory=SensoryRadar(
            body=4.0, acidity=9.5, tannins=1.0, fruit=7.0, oak=1.0
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="cornish-oysters-dover-sole",
        name="Cornish Oysters & Dover Sole a la meunière",
        category="Pescados y Mariscos",
        description="Ostras nativas de Cornualles seguidas de lenguado Dover Sole dorado en mantequilla avellana, limón y perejil fresco.",
        target_sensory=SensoryRadar(
            body=6.2, acidity=9.0, tannins=1.3, fruit=7.6, oak=4.0
        ),
        suggested_wine_type=WineType.SPARKLING,
    ),
    Dish(
        id="bacalao-pil-pil",
        name="Bacalao al pil-pil donostiarra con guindilla",
        category="Pescados y Mariscos",
        description="Lomos de bacalao skrei confitados a baja temperatura con su gelatina emulsionada en aceite de oliva y láminas de ajo.",
        target_sensory=SensoryRadar(
            body=6.6, acidity=8.4, tannins=1.5, fruit=7.8, oak=3.8
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    # --- 6. Arroces (4 dishes) ---
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
        id="risotto-funghi-porcini",
        name="Risotto ai Funghi Porcini e Parmigiano",
        category="Arroces",
        description="Arroz Carnaroli mantecado con boletus porcini de montaña, caldo de setas, mantequilla alpina y Parmigiano Reggiano 30 meses.",
        target_sensory=SensoryRadar(
            body=7.4, acidity=7.9, tannins=6.2, fruit=8.0, oak=5.8
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="arroz-negro-chipirones",
        name="Arroz negro mediterráneo con chipirones y alioli",
        category="Arroces",
        description="Arroz bomba cocinado en fumet de sepia y tinta natural con chipirones a la plancha y emulsión suave de ajo.",
        target_sensory=SensoryRadar(
            body=6.2, acidity=8.4, tannins=1.6, fruit=8.0, oak=2.0
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    # --- 7. Carnes y Caza (10 dishes) ---
    Dish(
        id="chuleton-brasa",
        name="Chuletón de vaca vieja a la brasa",
        category="Carnes y Caza",
        description="Corte de lomo alto madurado 45 días asado con leña de encina y cristales de sal marina.",
        target_sensory=SensoryRadar(
            body=9.0, acidity=6.5, tannins=8.5, fruit=7.5, oak=8.0
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="cochinillo-asado",
        name="Cochinillo asado tradicional segoviano",
        category="Carnes y Caza",
        description="Asado lentamente en horno de leña de encina con piel ultra crujiente y carne melosa confitada.",
        target_sensory=SensoryRadar(
            body=7.5, acidity=7.5, tannins=7.0, fruit=7.5, oak=7.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="carrilleras-ibericas",
        name="Carrilleras ibéricas estofadas al vino tinto",
        category="Carnes y Caza",
        description="Cocción lenta de carrillera de cerdo ibérico en reducción de vino, chalotas y cacao amargo con textura melosa.",
        target_sensory=SensoryRadar(
            body=8.5, acidity=7.0, tannins=7.8, fruit=8.0, oak=7.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="rabo-toro",
        name="Rabo de toro estofado a la cordobesa",
        category="Carnes y Caza",
        description="Guiso tradicional de larga cocción con vino oloroso, verduras pochadas y salsa gelatinosa de gran intensidad.",
        target_sensory=SensoryRadar(
            body=9.2, acidity=6.8, tannins=8.2, fruit=7.5, oak=8.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="perdiz-toledana",
        name="Perdiz roja estofada a la toledana",
        category="Carnes y Caza",
        description="Perdiz de campo estofada a fuego lento con cebolla pochada, vino blanco de guarda, vinagre y laurel.",
        target_sensory=SensoryRadar(
            body=8.0, acidity=7.5, tannins=7.5, fruit=7.5, oak=7.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="boeuf-bourguignon",
        name="Boeuf Bourguignon al vino tinto de Borgoña",
        category="Carnes y Caza",
        description="Morcillo de vaca estofado lentamente en Pinot Noir con panceta ahumada, cebollitas glaseadas y champiñones salteados.",
        target_sensory=SensoryRadar(
            body=7.8, acidity=7.8, tannins=7.0, fruit=8.3, oak=6.6
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="magret-de-canard",
        name="Magret de Canard asado con salsa de frutos rojos",
        category="Carnes y Caza",
        description="Pechuga de pato de las Landas sellada al punto rosado con piel crujiente y reducción de cerezas y pimienta negra.",
        target_sensory=SensoryRadar(
            body=8.0, acidity=7.8, tannins=7.2, fruit=8.6, oak=6.5
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="ossobuco-alla-milanese",
        name="Ossobuco alla Milanese con gremolata cítrica",
        category="Carnes y Caza",
        description="Jarrete de ternera blanca braseado lentamente con vino blanco, tuétano meloso y gremolata fresca de ralladura de limón y perejil.",
        target_sensory=SensoryRadar(
            body=8.4, acidity=8.1, tannins=8.0, fruit=8.4, oak=7.2
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="bistecca-alla-fiorentina",
        name="Bistecca alla Fiorentina a la brasa de roble",
        category="Carnes y Caza",
        description="Corte monumental de vaca Chianina en T-bone asado a fuego vivo, servido al punto sangrante con aceite toscano y romero.",
        target_sensory=SensoryRadar(
            body=8.8, acidity=8.0, tannins=8.4, fruit=8.5, oak=7.6
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="beef-wellington",
        name="Beef Wellington en hojaldre con duxelles de setas",
        category="Carnes y Caza",
        description="Solomillo británico envuelto en duxelles de champiñones trufados, jamón curado y hojaldre dorado de mantequilla.",
        target_sensory=SensoryRadar(
            body=8.7, acidity=7.4, tannins=8.2, fruit=8.4, oak=8.2
        ),
        suggested_wine_type=WineType.RED,
    ),
    # --- 8. Postres y Dulces (5 dishes) ---
    Dish(
        id="tarta-queso-idiazabal",
        name="Tarta fluida de queso Idiazábal ahumado",
        category="Postres y Dulces",
        description="Tarta horneada al estilo donostiarra con corazón cremoso de queso Idiazábal D.O. ahumado con madera de haya.",
        target_sensory=SensoryRadar(
            body=7.5, acidity=7.0, tannins=3.5, fruit=6.5, oak=5.0
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="torrija-brioche-px",
        name="Torrija caramelizada de brioche al Pedro Ximénez",
        category="Postres y Dulces",
        description="Pan brioche empapado en leche aromatizada con canela y cítricos, caramelizado con soplete y reducción de Pedro Ximénez.",
        target_sensory=SensoryRadar(
            body=8.5, acidity=5.5, tannins=2.0, fruit=9.0, oak=6.5
        ),
        suggested_wine_type=WineType.FORTIFIED,
    ),
    Dish(
        id="creme-brulee-bourbon",
        name="Crème Brûlée de vainilla Bourbon caramelizada",
        category="Postres y Dulces",
        description="Crema francesa sedosa infusionada con vaina natural de vainilla de Madagascar bajo una lámina crujiente de caramelo.",
        target_sensory=SensoryRadar(
            body=8.6, acidity=7.6, tannins=1.5, fruit=9.2, oak=6.8
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="tiramisu-clasico",
        name="Tiramisù clásico de mascarpone, espresso y cacao",
        category="Postres y Dulces",
        description="Capas de bizcocho savoiardi empapado en café espresso italiano, crema aireada de mascarpone y cacao amargo puro.",
        target_sensory=SensoryRadar(
            body=8.4, acidity=6.2, tannins=2.2, fruit=8.6, oak=7.2
        ),
        suggested_wine_type=WineType.FORTIFIED,
    ),
    Dish(
        id="sticky-toffee-pudding",
        name="Sticky Toffee Pudding británico con salsa de dátiles",
        category="Postres y Dulces",
        description="Bizcocho tibio húmedo de dátiles bañado en salsa de toffee de mantequilla salada y nata espesa de Cornualles.",
        target_sensory=SensoryRadar(
            body=9.0, acidity=5.8, tannins=1.8, fruit=9.2, oak=7.5
        ),
        suggested_wine_type=WineType.FORTIFIED,
    ),
    # --- 9. Platos Vegetarianos y Setas (5 dishes) ---
    Dish(
        id="hongos-boletus-yema",
        name="Boletus edulis salteados al sarmiento con yema campera",
        category="Platos Vegetarianos y Setas",
        description="Setas silvestres boletus edulis salteadas a fuego vivo con ajo tierno y yema de huevo campera trufada.",
        target_sensory=SensoryRadar(
            body=7.0, acidity=6.8, tannins=5.5, fruit=6.5, oak=6.0
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="alcachofas-confitadas-trufa",
        name="Alcachofas de Tudela confitadas con lascas de trufa negra",
        category="Platos Vegetarianos y Setas",
        description="Corazones de alcachofa confitados a baja temperatura en aceite virgen extra y terminados a la brasa con trufa negra melanosporum.",
        target_sensory=SensoryRadar(
            body=6.0, acidity=7.8, tannins=3.0, fruit=6.0, oak=4.5
        ),
        suggested_wine_type=WineType.WHITE,
    ),
    Dish(
        id="tagliatelle-al-tartufo",
        name="Tagliatelle freschi al Tartufo Bianco d'Alba",
        category="Platos Vegetarianos y Setas",
        description="Pasta fresca al huevo mantecada con mantequilla de montaña piamontesa, Parmigiano y finas láminas de trufa blanca de Alba.",
        target_sensory=SensoryRadar(
            body=7.5, acidity=8.3, tannins=7.2, fruit=8.2, oak=6.2
        ),
        suggested_wine_type=WineType.RED,
    ),
    Dish(
        id="ratatouille-provenzal",
        name="Ratatouille provenzal confitada al tomillo",
        category="Platos Vegetarianos y Setas",
        description="Hortalizas de verano del Midi (berenjena, calabacín, pimiento y tomate) confitadas lentamente con hierbas de Provenza.",
        target_sensory=SensoryRadar(
            body=6.2, acidity=8.0, tannins=2.2, fruit=8.3, oak=1.8
        ),
        suggested_wine_type=WineType.ROSE,
    ),
    Dish(
        id="melanzane-alla-parmigiana",
        name="Melanzane alla Parmigiana gratinadas",
        category="Platos Vegetarianos y Setas",
        description="Capas de berenjena asada con salsa de tomate San Marzano, albahaca fresca, mozzarella fior di latte y Parmigiano horneado.",
        target_sensory=SensoryRadar(
            body=7.4, acidity=8.1, tannins=6.6, fruit=8.4, oak=5.2
        ),
        suggested_wine_type=WineType.RED,
    ),
]
