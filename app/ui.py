"""UI templates and interactive HTML views for Vinum Pulse."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vinum Pulse — Radar de Cata y Maridaje Sensorial</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        serif: ['"Instrument Serif"', 'Georgia', 'serif'],
                        sans: ['"Work Sans"', 'system-ui', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        cream: '#F7F2E8',
                        butter: '#EFE7D6',
                        espresso: '#231B16',
                        walnut: '#6A5A4F',
                        bordeaux: '#6B1D28',
                        brass: '#9C6F38',
                        sage: '#4F5D47',
                    }
                }
            }
        }
    </script>
    <style>
        :root {
            color-scheme: light;
            --ease-bistro: cubic-bezier(0.22, 1, 0.36, 1);
        }
        ::selection { background-color: #6B1D28; color: #F7F2E8; }
        body {
            background-color: #F7F2E8;
            color: #231B16;
        }
        ::-webkit-scrollbar { width: 7px; }
        ::-webkit-scrollbar-track { background: #EFE7D6; }
        ::-webkit-scrollbar-thumb { background: rgba(107, 29, 40, 0.25); border-radius: 4px; }

        .menu-frame {
            border-top: 1px solid rgba(35, 27, 22, 0.16);
            border-bottom: 1px solid rgba(35, 27, 22, 0.16);
        }
        .dish-row {
            transition: background-color 200ms var(--ease-bistro), padding-left 200ms var(--ease-bistro);
        }
        .dish-row:hover {
            background-color: rgba(239, 231, 214, 0.55);
        }
        .dish-row.is-active {
            background-color: #EFE7D6;
            padding-left: 0.75rem;
        }
        .style-tab {
            transition: color 180ms var(--ease-bistro), border-color 180ms var(--ease-bistro);
        }
        .do-pill {
            transition: all 180ms var(--ease-bistro);
            border: 1px solid rgba(35, 27, 22, 0.14);
            background-color: #EFE7D6;
            color: #6A5A4F;
        }
        .do-pill:hover {
            border-color: #6B1D28;
            color: #231B16;
        }
        .do-pill.is-active {
            background-color: #6B1D28;
            border-color: #6B1D28;
            color: #F7F2E8;
            font-weight: 500;
        }
        .occasion-btn {
            transition: all 200ms var(--ease-bistro);
        }
        .occasion-btn.is-active {
            border-color: #6B1D28;
            background-color: #EFE7D6;
            box-shadow: 0 1px 4px rgba(107, 29, 40, 0.12);
        }
        input[type="range"] {
            -webkit-appearance: none;
            appearance: none;
            background: rgba(35, 27, 22, 0.16);
            height: 2px;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 999px;
            background: #6B1D28;
            border: 2px solid #F7F2E8;
            box-shadow: 0 1px 3px rgba(35, 27, 22, 0.25);
            cursor: pointer;
        }
        :focus-visible {
            outline: 2px solid #6B1D28;
            outline-offset: 3px;
        }
        .tabular-nums { font-variant-numeric: tabular-nums; }

        /* Leaflet custom styling */
        .leaflet-container {
            background: #FAF6EE !important;
            font-family: "Work Sans", sans-serif;
        }
        .leaflet-popup-content-wrapper {
            background: #FAF6EE !important;
            color: #231B16 !important;
            border: 1px solid rgba(107, 29, 40, 0.3) !important;
            border-radius: 4px !important;
            box-shadow: 0 4px 12px rgba(35, 27, 22, 0.15) !important;
            padding: 2px !important;
        }
        .leaflet-popup-tip {
            background: #FAF6EE !important;
        }
        .custom-pin {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #6B1D28;
            border: 2px solid #FAF6EE;
            box-shadow: 0 2px 6px rgba(35, 27, 22, 0.35);
            cursor: pointer;
            transition: transform 150ms ease;
        }
        .custom-pin:hover {
            transform: scale(1.25);
            background: #9C6F38;
        }
        .custom-pin-inner {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #F7F2E8;
        }

        /* Print Media Styles for Printable Menu Card */
        @media print {
            body {
                background-color: #FAF6EE !important;
                color: #231B16 !important;
            }
            .no-print, header, footer, #atlas-section, .menu-frame, #error-banner, #occasion-selector, #plan-inputs-container, #btn-generate-menu-plan, #btn-print-menu, #menu-plan-results > div:not(#printable-menu-card) {
                display: none !important;
            }
            #evening-planner-section {
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            #printable-menu-card {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 auto !important;
                border: 2px solid #231B16 !important;
                box-shadow: none !important;
                padding: 2.5rem !important;
                page-break-inside: avoid;
            }
        }
    </style>
</head>
<body class="min-h-screen font-sans antialiased text-espresso">
    <!-- Parisian Bistro Masthead -->
    <header class="max-w-5xl mx-auto px-6 sm:px-10 pt-10 pb-6 text-center space-y-2 no-print">
        <div class="flex items-center justify-center gap-3 text-bordeaux">
            <span class="h-px w-8 bg-espresso/20"></span>
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M8 22h8M12 15v7M6 3h12l-1.2 6.5a5 5 0 0 1-9.6 0L6 3Z"/>
            </svg>
            <span class="h-px w-8 bg-espresso/20"></span>
        </div>
        <h1 class="font-serif text-4xl sm:text-5xl tracking-tight text-espresso">Vinum Pulse</h1>
        <p class="font-serif italic text-lg text-walnut">
            Cave &amp; Table — Maridaje de mesa, sin jerga enológica
        </p>
    </header>

    <main class="max-w-5xl mx-auto px-6 sm:px-10 pb-16 space-y-12">
        <!-- Inline Error Banner -->
        <div id="error-banner" role="alert" class="hidden border border-bordeaux/30 bg-butter px-4 py-3 text-bordeaux text-sm flex items-center justify-between gap-4 no-print">
            <span id="error-message">No hay vinos disponibles con estos filtros.</span>
            <button type="button" onclick="document.getElementById('error-banner').classList.add('hidden')" class="text-xs font-mono underline underline-offset-4">Cerrar</button>
        </div>

        <!-- Atlas Cartográfico de Terroirs & Bodegas D.O. -->
        <section id="atlas-section" class="border-t border-espresso/15 pt-8 space-y-6 no-print">
            <div class="flex flex-wrap items-baseline justify-between gap-4 border-b border-espresso/15 pb-4">
                <div class="space-y-1">
                    <div class="text-xs font-mono text-bordeaux uppercase tracking-wider flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-bordeaux"></span>
                        Geografía &amp; Terroir Peninsular
                    </div>
                    <h2 class="font-serif text-3xl sm:text-4xl text-espresso tracking-tight">
                        Atlas Cartográfico de Terroirs &amp; Bodegas D.O.
                    </h2>
                    <p class="font-serif italic text-base text-walnut">
                        12 Denominaciones de Origen y 36 bodegas emblemáticas de España
                    </p>
                </div>
                <div class="flex items-center gap-3">
                    <span id="atlas-status-badge" class="px-3 py-1 text-xs font-mono rounded-full bg-butter text-bordeaux border border-bordeaux/20 tabular-nums">
                        12 D.O. · 36 Bodegas
                    </span>
                </div>
            </div>

            <!-- D.O. Quick-Select Pill Bar -->
            <div class="space-y-2">
                <div class="flex justify-between items-center text-xs font-mono text-walnut">
                    <span>Filtro por Denominación de Origen</span>
                    <span id="atlas-selected-do-label" class="text-bordeaux font-medium">Todas las regiones</span>
                </div>
                <div id="do-pills-bar" class="flex flex-wrap gap-2 text-xs font-mono">
                    <button type="button" data-do="" class="do-pill px-3 py-1.5 rounded-sm is-active">Todas (12 D.O.)</button>
                    <!-- Remaining D.O. pills populated via JS -->
                </div>
            </div>

            <!-- Map and Ficha Layout -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                <!-- Map Column (7 cols) -->
                <div class="lg:col-span-7 space-y-3">
                    <div class="relative w-full h-[460px] rounded border border-espresso/15 overflow-hidden bg-[#FAF6EE] shadow-xs">
                        <div id="atlas-map" class="w-full h-full z-10"></div>
                        <!-- Deterministic SVG Fallback -->
                        <div id="atlas-svg-fallback" class="hidden absolute inset-0 w-full h-full bg-[#FAF6EE] p-4 flex flex-col justify-between z-20 overflow-hidden">
                            <div class="flex justify-between items-center text-xs font-mono text-walnut border-b border-espresso/10 pb-2">
                                <span class="flex items-center gap-1.5">
                                    <span class="w-2 h-2 rounded-full bg-sage"></span>
                                    Atlas Cartográfico Vectorial (Modo Determinista)
                                </span>
                                <span class="text-bordeaux font-medium">12 D.O. / 36 Bodegas</span>
                            </div>
                            <div id="svg-map-canvas" class="w-full h-[380px] flex items-center justify-center">
                                <!-- SVG map rendered here -->
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-wrap justify-between items-center text-[11px] font-mono text-walnut px-1 gap-2">
                        <span>Haga clic en un marcador para cargar su Ficha de Terroir y sincronizar el Radar Sensorial.</span>
                        <span id="map-engine-label" class="text-sage">Cartografía: Leaflet.js</span>
                    </div>
                </div>

                <!-- Ficha de Terroir & Clima (5 cols) -->
                <aside id="terroir-card" class="lg:col-span-5 bg-butter/60 border border-espresso/12 rounded p-6 space-y-5">
                    <div class="border-b border-espresso/15 pb-4 space-y-1.5">
                        <div class="flex justify-between items-baseline">
                            <span id="terroir-community" class="text-xs font-mono text-bordeaux uppercase tracking-wider">La Rioja</span>
                            <span id="terroir-altitude" class="text-xs font-mono text-walnut tabular-nums">580 m altitud</span>
                        </div>
                        <h3 id="terroir-do-name" class="font-serif text-2xl sm:text-3xl text-espresso leading-tight">D.O.Ca. Rioja</h3>
                        <p id="terroir-tagline" class="text-xs text-walnut leading-relaxed italic">
                            Cuna histórica del roble y la elegancia clásica de guarda española.
                        </p>
                    </div>

                    <dl class="space-y-2.5 text-xs">
                        <div class="flex justify-between items-baseline border-b border-espresso/8 pb-1.5">
                            <dt class="font-mono text-walnut">Clima</dt>
                            <dd id="terroir-climate" class="font-medium text-espresso text-right max-w-[65%]">Continental templado</dd>
                        </div>
                        <div class="flex justify-between items-baseline border-b border-espresso/8 pb-1.5">
                            <dt class="font-mono text-walnut">Suelo</dt>
                            <dd id="terroir-soil" class="font-medium text-espresso text-right max-w-[65%]">Arcilloso-calcáreo</dd>
                        </div>
                        <div class="flex justify-between items-baseline border-b border-espresso/8 pb-1.5">
                            <dt class="font-mono text-walnut">Uva Emblema</dt>
                            <dd id="terroir-grape" class="font-medium text-bordeaux text-right max-w-[65%]">Tempranillo, Garnacha</dd>
                        </div>
                        <div class="flex justify-between items-baseline border-b border-espresso/8 pb-1.5">
                            <dt class="font-mono text-walnut">Bodega Activa</dt>
                            <dd id="terroir-winery" class="font-medium text-espresso text-right max-w-[65%]">La Rioja Alta, S.A.</dd>
                        </div>
                        <div class="flex justify-between items-baseline border-b border-espresso/8 pb-1.5">
                            <dt class="font-mono text-walnut">Vino Destacado</dt>
                            <dd id="terroir-wine-name" class="font-serif text-sm text-espresso text-right max-w-[65%]">Viña Ardanza Reserva</dd>
                        </div>
                    </dl>

                    <div class="space-y-2 pt-1">
                        <div class="flex justify-between items-baseline">
                            <h4 class="font-serif italic text-sm text-walnut">Bodegas en esta D.O.</h4>
                            <span id="terroir-winery-count" class="text-[11px] font-mono text-walnut">3 bodegas</span>
                        </div>
                        <div id="terroir-wineries-list" class="space-y-1.5 max-h-[150px] overflow-y-auto pr-1">
                            <!-- Winery chips rendered via JS -->
                        </div>
                    </div>

                    <button type="button" id="btn-sync-radar" class="w-full py-2.5 px-4 bg-bordeaux text-cream text-xs font-mono uppercase tracking-wider rounded hover:bg-bordeaux/90 transition shadow-xs cursor-pointer">
                        Proyectar Perfil en Radar 5D
                    </button>
                </aside>
            </div>
        </section>

        <!-- Menu Sheet Layout -->
        <div class="menu-frame py-10 grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-start no-print">
            <!-- Left: La Carte & Cellar Preferences (5 cols) -->
            <aside class="lg:col-span-5 space-y-8">
                <!-- La Carte Collapsible Section -->
                <section class="space-y-4">
                    <div class="flex justify-between items-baseline border-b border-espresso/15 pb-2.5">
                        <h2 class="font-serif text-2xl text-espresso">La Carte</h2>
                        <span id="dish-counter" class="text-xs font-serif italic text-walnut">Cargando carta...</span>
                    </div>

                    <!-- Active Dish Summary Chip -->
                    <div id="active-dish-chip" class="bg-butter/70 border border-espresso/12 rounded p-3.5 space-y-2 transition-all">
                        <div class="flex items-center justify-between gap-2">
                            <div class="flex items-center gap-2">
                                <span class="inline-block w-2 h-2 rounded-full bg-bordeaux"></span>
                                <span class="text-[10px] font-mono uppercase tracking-wider text-bordeaux font-semibold">Plato seleccionado</span>
                                <span id="active-dish-category" class="text-[10px] font-mono px-2 py-0.5 rounded bg-cream border border-espresso/10 text-walnut">Carnes</span>
                            </div>
                            <button type="button" id="btn-expand-carte" class="text-xs font-mono text-bordeaux hover:underline flex items-center gap-1 cursor-pointer">
                                <span>Cambiar plato</span> <span id="btn-expand-carte-chevron">▾</span>
                            </button>
                        </div>
                        <div class="flex items-baseline justify-between gap-3">
                            <h3 id="active-dish-name" class="font-serif text-lg text-bordeaux font-medium">Chuletón de vaca vieja a la brasa</h3>
                        </div>
                        <p id="active-dish-desc" class="text-xs text-walnut/90 line-clamp-1 italic">Corte de lomo alto madurado 45 días asado con leña de encina.</p>
                    </div>

                    <!-- Accordion container for dishes (#dish-grid) -->
                    <div id="dish-grid" class="space-y-2">
                        <!-- Collapsible sections rendered via JS -->
                    </div>
                </section>

                <!-- En Bodega: Budget and Style Filters -->
                <section class="space-y-6 pt-2">
                    <h2 class="font-serif text-2xl text-espresso border-b border-espresso/15 pb-2.5">En Bodega</h2>

                    <div class="space-y-3">
                        <div class="flex justify-between items-baseline">
                            <label for="budget-slider" class="text-sm text-walnut">Presupuesto por botella</label>
                            <span id="budget-value" class="font-mono text-base text-bordeaux tabular-nums">50 €</span>
                        </div>
                        <input id="budget-slider" type="range" min="15" max="80" step="5" value="50" class="w-full cursor-pointer">
                        <div class="flex justify-between text-[11px] font-mono text-walnut/80">
                            <span>15 €</span>
                            <span>45 €</span>
                            <span>80 €</span>
                        </div>
                    </div>

                    <div class="space-y-2.5">
                        <span class="block text-sm text-walnut">Estilo</span>
                        <div class="flex flex-wrap gap-x-5 gap-y-2 border-b border-espresso/10 pb-1" id="type-selector">
                            <button type="button" data-type="" class="style-tab pb-1.5 text-sm font-medium border-b-2 border-bordeaux text-bordeaux">Todos</button>
                            <button type="button" data-type="Red" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso">Tinto</button>
                            <button type="button" data-type="White" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso">Blanco</button>
                            <button type="button" data-type="Sparkling" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso">Espumoso</button>
                            <button type="button" data-type="Fortified" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso">Generoso</button>
                        </div>
                    </div>
                </section>
            </aside>

            <!-- Right: Le Choix du Sommelier (7 cols) -->
            <section id="results-section" class="lg:col-span-7 lg:border-l lg:border-espresso/12 lg:pl-12 space-y-8">
                <!-- Wine Header -->
                <div class="flex flex-wrap justify-between items-baseline gap-4 border-b border-espresso/15 pb-6">
                    <div class="space-y-1">
                        <div class="text-xs font-mono text-walnut flex items-center gap-2">
                            <span id="res-appellation" class="text-bordeaux uppercase tracking-wider">D.O.Ca. Rioja</span>
                            <span aria-hidden="true">·</span>
                            <span id="res-vintage" class="tabular-nums">Añada 2017</span>
                        </div>
                        <h3 id="res-name" class="font-serif text-3xl sm:text-4xl text-espresso leading-tight">Viña Ardanza Reserva</h3>
                        <p id="res-winery" class="font-serif italic text-lg text-walnut">La Rioja Alta, S.A.</p>
                    </div>
                    <div class="text-right space-y-1">
                        <div id="res-price" class="font-mono text-2xl text-espresso tabular-nums">34.00 €</div>
                        <div class="text-xs font-mono text-sage tabular-nums">
                            <span id="res-score">96.5%</span> afinidad
                        </div>
                    </div>
                </div>

                <!-- Quiet Service Ritual Line -->
                <div class="flex flex-wrap items-center gap-x-8 gap-y-2 text-sm text-walnut border-b border-espresso/10 pb-5">
                    <span>Servicio <strong id="res-temp" class="font-medium text-espresso tabular-nums">17 °C</strong></span>
                    <span>Decantación <strong id="res-decant" class="font-medium text-espresso tabular-nums">30 min</strong></span>
                    <span>Copa <strong id="res-glass" class="font-medium text-espresso">Burdeos</strong></span>
                </div>

                <!-- Editorial Bottle Visual, Wine Hook & Radar (3-part responsive grid) -->
                <div class="grid grid-cols-1 sm:grid-cols-12 gap-6 items-center">
                    <!-- Col 1: Editorial Bottle & Label Visual (#res-bottle-visual) -->
                    <div class="sm:col-span-3 flex flex-col items-center justify-center">
                        <div id="res-bottle-visual" class="relative w-full max-w-[130px] flex flex-col items-center">
                            <img id="res-bottle-img" src="" alt="Botella de vino" class="hidden max-h-[220px] object-contain drop-shadow">
                            <div id="res-bottle-svg-container" class="w-full flex justify-center">
                                <!-- Dynamic high-craft SVG bottle rendered here -->
                            </div>
                            <span id="res-bottle-badge" class="mt-2 text-[10px] font-mono px-2 py-0.5 rounded bg-butter border border-espresso/15 text-bordeaux font-medium text-center">
                                Botella Bordelesa
                            </span>
                        </div>
                    </div>

                    <!-- Col 2: Wine Hook, Explanation & Tasting Notes Expansion (5 cols) -->
                    <div class="sm:col-span-5 space-y-4">
                        <p id="res-tagline" class="font-serif italic text-xl text-bordeaux leading-snug">
                            Elegancia clásica riojana de taninos sedosos y crianza pausada en roble americano.
                        </p>
                        <p id="res-explanation" class="text-xs sm:text-sm text-espresso/90 leading-relaxed">
                            Cargando análisis sensorial...
                        </p>
                        <div class="pt-1">
                            <button type="button" id="btn-toggle-tasting-notes" aria-expanded="false" class="group inline-flex items-center gap-1.5 text-xs font-mono text-walnut hover:text-bordeaux py-1.5 px-3 rounded bg-butter/60 hover:bg-butter border border-espresso/10 transition cursor-pointer">
                                <span id="btn-toggle-tasting-notes-label">Ver notas de cata completas del sumiller</span>
                                <span id="btn-toggle-tasting-notes-icon" class="text-bordeaux transition-transform duration-200">▾</span>
                            </button>
                            <blockquote id="res-notes-panel" class="hidden mt-2.5 border-l-2 border-bordeaux pl-3 py-1.5 bg-butter/30 rounded-r transition-all duration-300">
                                <p id="res-notes" class="font-serif italic text-sm sm:text-base text-walnut leading-relaxed">
                                    Cargando descriptores...
                                </p>
                            </blockquote>
                        </div>
                    </div>

                    <!-- Col 3: 5D Radar Chart (4 cols) -->
                    <div class="sm:col-span-4 space-y-2">
                        <div class="relative w-full aspect-square max-w-[220px] mx-auto">
                            <canvas id="radarChart"></canvas>
                        </div>
                        <div class="flex justify-center gap-4 text-[10px] font-mono text-walnut">
                            <span class="flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-bordeaux"></span> Vino
                            </span>
                            <span class="flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-brass"></span> Plato
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Cellar Alternatives -->
                <div class="space-y-3 pt-4 border-t border-espresso/12">
                    <h4 class="font-serif italic text-lg text-walnut">Otras botellas de la cava</h4>
                    <div id="res-alternatives" class="divide-y divide-espresso/10">
                        <!-- Alternativas vía JS -->
                    </div>
                </div>
            </section>
        </div>

        <!-- Section: Interactive Evening & 3-Course Menu Sommelier Planner + Printable Menu Card -->
        <section id="evening-planner-section" class="border-t border-espresso/15 pt-12 space-y-10">
            <div class="text-center max-w-2xl mx-auto space-y-2 no-print">
                <div class="flex items-center justify-center gap-3 text-bordeaux">
                    <span class="h-px w-8 bg-espresso/20"></span>
                    <span class="text-xs font-mono uppercase tracking-wider text-bordeaux">Progresión Enológica</span>
                    <span class="h-px w-8 bg-espresso/20"></span>
                </div>
                <h2 class="font-serif text-3xl sm:text-4xl text-espresso tracking-tight">
                    Diseñador Interactivo de Veladas &amp; Carta de Sumiller Imprimible
                </h2>
                <p class="font-serif italic text-base text-walnut">
                    Planifica un menú de 3 pases con progresión enológica óptima, guía de nevera/descorche sin tecnicismos y carta lista para tus invitados
                </p>
            </div>

            <!-- Paso 1: Elegir la Ocasión (#occasion-selector) -->
            <div class="space-y-3 no-print">
                <div class="flex items-center justify-between text-xs font-mono text-walnut border-b border-espresso/10 pb-2">
                    <span>Paso 1 · Elige la Ocasión</span>
                    <span id="selected-occasion-label" class="text-bordeaux font-medium">Cena Romántica</span>
                </div>
                <div id="occasion-selector" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                    <button type="button" data-occasion="Cena Romántica" class="occasion-btn is-active text-left p-4 rounded border border-bordeaux bg-butter/90 hover:bg-butter transition cursor-pointer">
                        <div class="text-lg mb-1">🕯️</div>
                        <div class="font-serif text-lg text-espresso font-medium">Cena Romántica</div>
                        <p class="text-xs text-walnut mt-1">Elegancia, sutiles matices y conversación pausada.</p>
                    </button>
                    <button type="button" data-occasion="Barbacoa con Amigos" class="occasion-btn text-left p-4 rounded border border-espresso/12 bg-cream hover:bg-butter transition cursor-pointer">
                        <div class="text-lg mb-1">🥩</div>
                        <div class="font-serif text-lg text-espresso font-medium">Barbacoa con Amigos</div>
                        <p class="text-xs text-walnut mt-1">Taninos nobles, fruta madura y brasa intensa.</p>
                    </button>
                    <button type="button" data-occasion="Comida Familiar de Domingo" class="occasion-btn text-left p-4 rounded border border-espresso/12 bg-cream hover:bg-butter transition cursor-pointer">
                        <div class="text-lg mb-1">🥘</div>
                        <div class="font-serif text-lg text-espresso font-medium">Comida Familiar de Domingo</div>
                        <p class="text-xs text-walnut mt-1">Tradición de cuchara, generosidad y sobremesa.</p>
                    </button>
                    <button type="button" data-occasion="Tardeo & Tapas Gourmet" class="occasion-btn text-left p-4 rounded border border-espresso/12 bg-cream hover:bg-butter transition cursor-pointer">
                        <div class="text-lg mb-1">🍷</div>
                        <div class="font-serif text-lg text-espresso font-medium">Tardeo &amp; Tapas Gourmet</div>
                        <p class="text-xs text-walnut mt-1">Burbujas vivas, frescura marina y picoteo selecto.</p>
                    </button>
                </div>
            </div>

            <!-- Paso 2: Configurar el Menú de 3 Pases y Presupuesto Total -->
            <div id="plan-inputs-container" class="bg-butter/40 border border-espresso/12 rounded p-6 space-y-6 no-print">
                <div class="flex items-center justify-between text-xs font-mono text-walnut border-b border-espresso/10 pb-2">
                    <span>Paso 2 · Configura el Menú de 3 Pases y Presupuesto Total</span>
                    <span class="text-bordeaux font-medium">3 Vinos Maridados</span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- 1.º Pase Select -->
                    <div class="space-y-2">
                        <label for="plan-starter-select" class="block text-xs font-mono text-walnut uppercase tracking-wide">
                            1.º Pase · Entrante / Aperitivo
                        </label>
                        <select id="plan-starter-select" class="w-full bg-cream border border-espresso/20 rounded p-2.5 text-sm font-serif text-espresso focus:border-bordeaux focus:ring-0">
                            <!-- Populated via JS -->
                        </select>
                    </div>

                    <!-- 2.º Pase Select -->
                    <div class="space-y-2">
                        <label for="plan-main-select" class="block text-xs font-mono text-walnut uppercase tracking-wide">
                            2.º Pase · Plato Principal
                        </label>
                        <select id="plan-main-select" class="w-full bg-cream border border-espresso/20 rounded p-2.5 text-sm font-serif text-espresso focus:border-bordeaux focus:ring-0">
                            <!-- Populated via JS -->
                        </select>
                    </div>

                    <!-- 3.º Pase Select -->
                    <div class="space-y-2">
                        <label for="plan-dessert-select" class="block text-xs font-mono text-walnut uppercase tracking-wide">
                            3.º Pase · Quesos o Postre
                        </label>
                        <select id="plan-dessert-select" class="w-full bg-cream border border-espresso/20 rounded p-2.5 text-sm font-serif text-espresso focus:border-bordeaux focus:ring-0">
                            <!-- Populated via JS -->
                        </select>
                    </div>
                </div>

                <!-- Total Budget Slider & Action Button -->
                <div class="pt-2 border-t border-espresso/10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                    <div class="space-y-2 flex-1 max-w-md">
                        <div class="flex justify-between items-baseline text-xs font-mono text-walnut">
                            <label for="plan-budget-slider">Presupuesto total de la velada (3 botellas)</label>
                            <span id="plan-budget-value" class="text-base text-bordeaux font-medium tabular-nums">110 €</span>
                        </div>
                        <input id="plan-budget-slider" type="range" min="45" max="250" step="5" value="110" class="w-full cursor-pointer">
                        <div class="flex justify-between text-[10px] font-mono text-walnut/70">
                            <span>45 €</span>
                            <span>110 €</span>
                            <span>250 €</span>
                        </div>
                    </div>

                    <button type="button" id="btn-generate-menu-plan" class="py-3 px-6 bg-bordeaux text-cream text-xs font-mono uppercase tracking-wider rounded hover:bg-bordeaux/90 transition shadow-sm self-start md:self-auto cursor-pointer">
                        Diseñar Velada de 3 Pases
                    </button>
                </div>
            </div>

            <!-- Paso 3: Progresión de los 3 Vinos & Semáforo Cotidiano (#menu-plan-results) -->
            <div id="menu-plan-results" class="space-y-8">
                <!-- Summary Bar -->
                <div class="bg-butter/70 border border-espresso/15 rounded p-5 space-y-3 no-print">
                    <div class="flex flex-wrap items-baseline justify-between gap-4 border-b border-espresso/10 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="text-xs font-mono text-bordeaux uppercase tracking-wider font-semibold">Balance de Velada</span>
                            <span class="h-3 w-px bg-espresso/20"></span>
                            <span id="plan-ambience-tip" class="text-xs font-serif italic text-walnut">
                                Ambiente sugerido: Iluminación cálida y música suave.
                            </span>
                        </div>
                        <div class="flex items-center gap-4 text-xs font-mono">
                            <span>Inversión total: <strong id="plan-total-price" class="text-sm text-espresso font-semibold tabular-nums">85.00 €</strong></span>
                            <span class="text-sage">Afinidad media: <strong id="plan-avg-score" class="text-sm font-semibold tabular-nums">95.4%</strong></span>
                        </div>
                    </div>
                    <p id="plan-progression-summary" class="text-xs sm:text-sm text-espresso/90 leading-relaxed font-sans">
                        Cargando progresión sommelier...
                    </p>
                </div>

                <!-- 3 Courses Grid (#plan-courses-grid) -->
                <div id="plan-courses-grid" class="grid grid-cols-1 md:grid-cols-3 gap-6 no-print">
                    <!-- Course cards populated via JS -->
                </div>

                <!-- Carta de Velada Imprimible para Invitados (#printable-menu-card) -->
                <div id="printable-menu-card" class="bg-[#FAF6EE] border-2 border-espresso/30 rounded p-8 sm:p-12 space-y-8 shadow-xs max-w-3xl mx-auto my-6">
                    <div class="text-center space-y-2 border-b border-espresso/15 pb-6">
                        <div class="flex items-center justify-center gap-3 text-bordeaux">
                            <span class="h-px w-10 bg-espresso/25"></span>
                            <span class="text-[11px] font-mono uppercase tracking-widest text-bordeaux font-medium">Carte des Vins &amp; Menu</span>
                            <span class="h-px w-10 bg-espresso/25"></span>
                        </div>
                        <h3 id="print-card-title" class="font-serif text-3xl sm:text-4xl text-espresso tracking-tight">Cena Romántica</h3>
                        <p class="font-serif italic text-sm text-walnut">Maridaje enológico de tres pases preparado por el Sumiller de Vinum Pulse</p>
                    </div>

                    <div id="print-courses-list" class="space-y-6 divide-y divide-espresso/10">
                        <!-- Courses list for print populated via JS -->
                    </div>

                    <div class="text-center pt-6 border-t border-espresso/15 text-xs font-serif italic text-walnut space-y-1">
                        <p>Vinum Pulse · Caviste &amp; Table · Bodega y Gastronomía Española</p>
                        <p class="text-[10px] font-mono text-walnut/70 uppercase tracking-widest">Salud y buen provecho</p>
                    </div>

                    <div class="text-center pt-2 no-print">
                        <button type="button" id="btn-print-menu" onclick="window.print()" class="inline-flex items-center gap-2 py-2.5 px-6 bg-bordeaux text-cream text-xs font-mono uppercase tracking-wider rounded hover:bg-bordeaux/90 transition shadow-sm cursor-pointer">
                            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            Imprimir Carta para Invitados
                        </button>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="max-w-5xl mx-auto px-6 sm:px-10 pb-10 text-center text-xs font-serif italic text-walnut no-print">
        Vinum Pulse · Radar de Cata y Maridaje Sensorial · Atlas Cartográfico de Terroirs
    </footer>

    <script>
        let allDishes = [];
        let atlasFeatures = [];
        let selectedDishId = "chuleton-brasa";
        let selectedDo = "";
        let activeAtlasFeature = null;
        let preferredType = null;
        let radarChartInstance = null;
        let leafletMap = null;
        let mapMarkers = [];
        let expandedCategory = null;
        let selectedOccasion = "Cena Romántica";

        const CANONICAL_CATEGORIES = [
            "Entrantes y Cuchara",
            "Ensaladas y Huerta",
            "Tapas y Pintxos",
            "Embutidos y Quesos",
            "Pescados y Mariscos",
            "Arroces",
            "Carnes y Caza",
            "Postres y Dulces",
            "Platos Vegetarianos y Setas"
        ];

        function getCategoryForDish(dish) {
            if (!dish || !dish.category) return "Entrantes y Cuchara";
            const cat = dish.category.trim();
            if (cat === "Carnes" || cat === "Caza" || cat.includes("Carne")) return "Carnes y Caza";
            if (cat.includes("Entrante") || cat.includes("Cuchara")) return "Entrantes y Cuchara";
            if (cat.includes("Ensalada") || cat.includes("Huerta")) return "Ensaladas y Huerta";
            if (cat.includes("Tapa") || cat.includes("Pintxo")) return "Tapas y Pintxos";
            if (cat.includes("Embutido") || cat.includes("Queso")) return "Embutidos y Quesos";
            if (cat.includes("Pescado") || cat.includes("Marisco")) return "Pescados y Mariscos";
            if (cat.includes("Arroz") || cat.includes("Arroces")) return "Arroces";
            if (cat.includes("Postre") || cat.includes("Dulce")) return "Postres y Dulces";
            if (cat.includes("Vegetariano") || cat.includes("Seta")) return "Platos Vegetarianos y Setas";
            return cat;
        }

        async function init() {
            try {
                const resDishes = await fetch("/api/v1/dishes");
                allDishes = await resDishes.json();
                renderActiveDishChip();
                renderDishes();
                setupEventListeners();
                fetchRecommendation();
                populatePlannerSelects();
                generateMenuPlan();
                await initAtlas();
            } catch (err) {
                showError("No se pudo inicializar la aplicación.");
                console.error("Error al inicializar:", err);
            }
        }

        function showError(msg) {
            const banner = document.getElementById("error-banner");
            document.getElementById("error-message").textContent = msg;
            banner.classList.remove("hidden");
        }

        function hideError() {
            document.getElementById("error-banner").classList.add("hidden");
        }

        function renderActiveDishChip() {
            const cur = allDishes.find(d => d.id === selectedDishId);
            if (!cur) return;
            const cat = getCategoryForDish(cur);
            document.getElementById("active-dish-category").textContent = cat;
            document.getElementById("active-dish-name").textContent = cur.name;
            document.getElementById("active-dish-desc").textContent = cur.description || "";
        }

        function renderDishes() {
            const grid = document.getElementById("dish-grid");
            document.getElementById("dish-counter").textContent = `${allDishes.length} platos`;

            // Group dishes by canonical categories
            const grouped = {};
            CANONICAL_CATEGORIES.forEach(cat => { grouped[cat] = []; });
            allDishes.forEach(dish => {
                const cat = getCategoryForDish(dish);
                if (!grouped[cat]) grouped[cat] = [];
                grouped[cat].push(dish);
            });

            grid.innerHTML = CANONICAL_CATEGORIES.filter(cat => grouped[cat] && grouped[cat].length > 0).map(catName => {
                const dishes = grouped[catName];
                const isExpanded = expandedCategory === catName;
                return `
                    <div class="carte-section rounded border border-espresso/12 overflow-hidden bg-cream/60 transition">
                        <button type="button" class="carte-section-header w-full flex items-center justify-between py-2.5 px-3 bg-butter/40 hover:bg-butter/80 transition text-left cursor-pointer" data-category="${catName}">
                            <div class="flex items-center gap-2">
                                <span class="font-serif text-base text-espresso">${catName}</span>
                                <span class="text-[10px] font-mono text-walnut tabular-nums">(${dishes.length})</span>
                            </div>
                            <span class="text-xs font-mono text-bordeaux transform transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}">▾</span>
                        </button>
                        <div class="carte-section-body ${isExpanded ? 'block' : 'hidden'} divide-y divide-espresso/10 border-t border-espresso/10 bg-cream">
                            ${dishes.map(dish => {
                                const isActive = dish.id === selectedDishId;
                                return `
                                    <button type="button" data-dish-id="${dish.id}" class="dish-row w-full text-left py-2.5 px-3 rounded-none ${isActive ? 'is-active bg-butter/80' : 'hover:bg-butter/40'}">
                                        <div class="flex items-baseline justify-between gap-2">
                                            <span class="font-serif text-lg ${isActive ? 'text-bordeaux font-medium' : 'text-espresso'}">${dish.name}</span>
                                            <span class="text-[10px] font-mono text-walnut shrink-0">${dish.suggested_wine_type || ''}</span>
                                        </div>
                                        <p class="text-xs text-walnut line-clamp-1 mt-0.5">${dish.description}</p>
                                    </button>
                                `;
                            }).join("")}
                        </div>
                    </div>
                `;
            }).join("");

            // Wire accordion header click
            grid.querySelectorAll(".carte-section-header").forEach(header => {
                header.addEventListener("click", () => {
                    const cat = header.getAttribute("data-category");
                    expandedCategory = (expandedCategory === cat) ? null : cat;
                    renderDishes();
                });
            });

            // Wire dish row click: updates selectedDishId, auto-collapses all accordion sections, updates chip and triggers fetchRecommendation
            grid.querySelectorAll(".dish-row").forEach(el => {
                el.addEventListener("click", () => {
                    selectedDishId = el.getAttribute("data-dish-id");
                    expandedCategory = null;
                    renderActiveDishChip();
                    renderDishes();
                    fetchRecommendation();
                });
            });
        }

        function toggleTastingNotes() {
            const panel = document.getElementById("res-notes-panel");
            const btn = document.getElementById("btn-toggle-tasting-notes");
            const label = document.getElementById("btn-toggle-tasting-notes-label");
            const icon = document.getElementById("btn-toggle-tasting-notes-icon");
            if (!panel || !btn) return;

            const isExpanded = btn.getAttribute("aria-expanded") === "true";
            if (isExpanded) {
                panel.classList.add("hidden");
                btn.setAttribute("aria-expanded", "false");
                label.textContent = "Ver notas de cata completas del sumiller";
                icon.textContent = "▾";
            } else {
                panel.classList.remove("hidden");
                btn.setAttribute("aria-expanded", "true");
                label.textContent = "Ocultar notas de cata del sumiller";
                icon.textContent = "▴";
            }
        }

        function setupEventListeners() {
            const slider = document.getElementById("budget-slider");
            const valLabel = document.getElementById("budget-value");
            slider.addEventListener("input", (e) => {
                valLabel.textContent = `${e.target.value} €`;
            });
            slider.addEventListener("change", () => {
                fetchRecommendation();
            });

            const activeClasses = ["border-bordeaux", "text-bordeaux", "font-medium"];
            const idleClasses = ["border-transparent", "text-walnut"];

            document.querySelectorAll(".style-tab").forEach(btn => {
                btn.addEventListener("click", () => {
                    document.querySelectorAll(".style-tab").forEach(b => {
                        b.classList.remove(...activeClasses);
                        b.classList.add(...idleClasses);
                    });
                    btn.classList.add(...activeClasses);
                    btn.classList.remove(...idleClasses);
                    preferredType = btn.getAttribute("data-type") || null;
                    fetchRecommendation();
                });
            });

            // Expand carte from summary chip
            const btnExpandCarte = document.getElementById("btn-expand-carte");
            if (btnExpandCarte) {
                btnExpandCarte.addEventListener("click", () => {
                    const cur = allDishes.find(d => d.id === selectedDishId);
                    const cat = getCategoryForDish(cur);
                    expandedCategory = (expandedCategory === cat) ? null : cat;
                    renderDishes();
                });
            }

            // Tasting notes expansion toggle button
            const btnNotes = document.getElementById("btn-toggle-tasting-notes");
            if (btnNotes) {
                btnNotes.addEventListener("click", toggleTastingNotes);
            }

            // Atlas sync button
            const btnSync = document.getElementById("btn-sync-radar");
            if (btnSync) {
                btnSync.addEventListener("click", () => {
                    if (activeAtlasFeature) {
                        applyAtlasWineToRadar(activeAtlasFeature);
                        document.getElementById("results-section").scrollIntoView({ behavior: "smooth" });
                    }
                });
            }

            // Evening Planner: Occasion buttons
            document.querySelectorAll(".occasion-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    document.querySelectorAll(".occasion-btn").forEach(b => {
                        b.classList.remove("is-active", "border-bordeaux", "bg-butter/90");
                        b.classList.add("border-espresso/12", "bg-cream");
                    });
                    btn.classList.add("is-active", "border-bordeaux", "bg-butter/90");
                    btn.classList.remove("border-espresso/12", "bg-cream");
                    selectedOccasion = btn.getAttribute("data-occasion");
                    document.getElementById("selected-occasion-label").textContent = selectedOccasion;
                    document.getElementById("print-card-title").textContent = selectedOccasion;
                    generateMenuPlan();
                });
            });

            // Evening Planner: Budget slider
            const planSlider = document.getElementById("plan-budget-slider");
            const planValLabel = document.getElementById("plan-budget-value");
            if (planSlider && planValLabel) {
                planSlider.addEventListener("input", (e) => {
                    planValLabel.textContent = `${e.target.value} €`;
                });
                planSlider.addEventListener("change", () => {
                    generateMenuPlan();
                });
            }

            // Evening Planner: Selects
            ["plan-starter-select", "plan-main-select", "plan-dessert-select"].forEach(id => {
                const el = document.getElementById(id);
                if (el) {
                    el.addEventListener("change", () => {
                        generateMenuPlan();
                    });
                }
            });

            // Evening Planner: Action button
            const btnGeneratePlan = document.getElementById("btn-generate-menu-plan");
            if (btnGeneratePlan) {
                btnGeneratePlan.addEventListener("click", () => {
                    generateMenuPlan();
                });
            }
        }

        async function fetchRecommendation() {
            hideError();
            const budget = parseFloat(document.getElementById("budget-slider").value);
            const payload = {
                dish_id: selectedDishId,
                max_budget_eur: budget,
                preferred_type: preferredType
            };

            try {
                const res = await fetch("/api/v1/pairings/recommend", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                if (!res.ok) {
                    const err = await res.json();
                    showError(err.detail || "No hay vinos disponibles para esta selección.");
                    return;
                }
                const data = await res.json();
                updateUI(data);
            } catch (err) {
                showError("Error de conexión con el motor de maridaje.");
                console.error("Error fetching recommendation:", err);
            }
        }

        function getBottleSilhouette(wine) {
            if (wine.bottle_silhouette) return wine.bottle_silhouette;
            const type = (wine.wine_type || "").toLowerCase();
            const glass = (wine.glass_type || "").toLowerCase();
            const app = (wine.appellation || "").toLowerCase();

            if (type === "sparkling" || app.includes("cava") || app.includes("corpinnat")) {
                return "Espumosa";
            }
            if (type === "fortified" || app.includes("jerez") || glass.includes("jerez")) {
                return "Jerezana";
            }
            if (glass.includes("borgoña") || app.includes("bierzo") || app.includes("priorat") || app.includes("ribeira")) {
                return "Borgoña";
            }
            return "Bordelesa";
        }

        function renderBottleVisual(wine) {
            const container = document.getElementById("res-bottle-svg-container");
            const img = document.getElementById("res-bottle-img");
            const badge = document.getElementById("res-bottle-badge");
            if (!container || !wine) return;

            if (wine.image_url) {
                img.src = wine.image_url;
                img.alt = wine.name;
                img.classList.remove("hidden");
                container.classList.add("hidden");
                img.onerror = () => {
                    img.classList.add("hidden");
                    container.classList.remove("hidden");
                };
            } else {
                img.classList.add("hidden");
                container.classList.remove("hidden");
            }

            const silhouette = getBottleSilhouette(wine);
            badge.textContent = `Botella ${silhouette}`;

            let glassColor = "#3B0F17";
            let capsuleColor = "#9C6F38";
            let bodyPath = "";
            let capsulePath = "";
            let labelY = 115;
            let labelHeight = 72;
            let labelWidth = 44;
            let labelX = 28;

            if (silhouette === "Bordelesa") {
                glassColor = "#3B0F17";
                capsuleColor = "#9C6F38";
                bodyPath = "M 26 245 C 26 248 74 248 74 245 L 74 105 C 73 90 57 82 57 38 L 59 38 L 59 30 L 41 30 L 41 38 L 43 38 C 43 82 27 90 26 105 Z";
                capsulePath = "M 41 30 L 59 30 L 59 62 L 41 62 Z";
                labelY = 115;
                labelHeight = 72;
                labelWidth = 44;
                labelX = 28;
            } else if (silhouette === "Borgoña") {
                glassColor = "#521822";
                capsuleColor = "#D4AF37";
                bodyPath = "M 20 245 C 20 249 80 249 80 245 L 79 160 C 76 115 57 80 57 38 L 59 38 L 59 30 L 41 30 L 41 38 L 43 38 C 43 80 24 115 21 160 Z";
                capsulePath = "M 41 30 L 59 30 L 59 62 L 41 62 Z";
                labelY = 135;
                labelHeight = 65;
                labelWidth = 48;
                labelX = 26;
            } else if (silhouette === "Jerezana") {
                glassColor = "#2A1E17";
                capsuleColor = "#8A2B1D";
                bodyPath = "M 26 245 C 26 248 74 248 74 245 L 74 105 C 73 92 57 82 57 66 C 60 58 57 50 57 38 L 59 38 L 59 30 L 41 30 L 41 38 L 43 38 C 43 50 40 58 43 66 C 43 82 27 92 26 105 Z";
                capsulePath = "M 41 30 L 59 30 L 59 58 L 41 58 Z";
                labelY = 115;
                labelHeight = 72;
                labelWidth = 44;
                labelX = 28;
            } else if (silhouette === "Espumosa") {
                glassColor = "#354230";
                capsuleColor = "#D4AF37";
                bodyPath = "M 21 245 C 21 249 79 249 79 245 L 78 155 C 75 110 58 78 58 38 L 60 38 L 60 28 L 40 28 L 40 38 L 42 38 C 42 78 25 110 22 155 Z";
                capsulePath = "M 40 28 L 60 28 L 60 68 C 55 70 45 70 40 68 Z";
                labelY = 130;
                labelHeight = 65;
                labelWidth = 46;
                labelX = 27;
            }

            const rawApp = (wine.appellation || "Vino de España").replace("D.O.Ca. ", "").replace("D.O.Q. ", "").replace("D.O. ", "").toUpperCase();
            const appText = rawApp.length > 14 ? rawApp.substring(0, 12) + "…" : rawApp;

            const wineWords = (wine.name || "").split(" ");
            let line1 = wine.name || "";
            let line2 = "";
            if (wineWords.length > 2) {
                line1 = wineWords.slice(0, 2).join(" ");
                line2 = wineWords.slice(2, 5).join(" ");
            }
            if (line1.length > 13) line1 = line1.substring(0, 11) + "…";
            if (line2.length > 13) line2 = line2.substring(0, 11) + "…";

            const wineryText = (wine.winery || "").length > 14 ? (wine.winery || "").substring(0, 12) + "…" : (wine.winery || "");

            const svg = `
                <svg viewBox="0 0 100 260" class="w-24 sm:w-28 h-auto select-none drop-shadow-sm" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="glassGrad-${silhouette}" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="${glassColor}" stop-opacity="0.95" />
                            <stop offset="25%" stop-color="${glassColor}" stop-opacity="0.75" />
                            <stop offset="65%" stop-color="${glassColor}" stop-opacity="0.9" />
                            <stop offset="100%" stop-color="${glassColor}" stop-opacity="1" />
                        </linearGradient>
                        <linearGradient id="capsuleGrad-${silhouette}" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="${capsuleColor}" />
                            <stop offset="50%" stop-color="#FAF6EE" stop-opacity="0.6" />
                            <stop offset="100%" stop-color="${capsuleColor}" />
                        </linearGradient>
                    </defs>

                    <ellipse cx="50" cy="249" rx="28" ry="5" fill="rgba(35, 27, 22, 0.18)" />
                    <path d="${bodyPath}" fill="url(#glassGrad-${silhouette})" stroke="rgba(35, 27, 22, 0.4)" stroke-width="1.2" />
                    <path d="M 30 110 L 30 235" stroke="rgba(255, 255, 255, 0.22)" stroke-width="2.5" stroke-linecap="round" />
                    <path d="${capsulePath}" fill="url(#capsuleGrad-${silhouette})" stroke="rgba(35, 27, 22, 0.3)" stroke-width="0.8" />
                    <line x1="40" y1="38" x2="60" y2="38" stroke="rgba(35, 27, 22, 0.3)" stroke-width="0.8" />

                    <g transform="translate(${labelX}, ${labelY})">
                        <rect x="0" y="0" width="${labelWidth}" height="${labelHeight}" rx="2" fill="#FAF6EE" stroke="#9C6F38" stroke-width="0.7" />
                        <rect x="2" y="2" width="${labelWidth - 4}" height="${labelHeight - 4}" rx="1" fill="none" stroke="rgba(35, 27, 22, 0.12)" stroke-width="0.4" />

                        <text x="${labelWidth / 2}" y="9" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="3.2" fill="#6B1D28" font-weight="600" letter-spacing="0.4">${appText}</text>
                        <line x1="${labelWidth / 2 - 8}" y1="12" x2="${labelWidth / 2 + 8}" y2="12" stroke="#9C6F38" stroke-width="0.4" />

                        <text x="${labelWidth / 2}" y="20" text-anchor="middle" font-family="'Instrument Serif', Georgia, serif" font-size="5.2" fill="#231B16" font-weight="bold">${line1}</text>
                        ${line2 ? `<text x="${labelWidth / 2}" y="26" text-anchor="middle" font-family="'Instrument Serif', Georgia, serif" font-size="4.6" fill="#231B16">${line2}</text>` : ''}

                        <text x="${labelWidth / 2}" y="${line2 ? 34 : 30}" text-anchor="middle" font-family="'Instrument Serif', Georgia, serif" font-size="3.8" font-style="italic" fill="#6A5A4F">${wineryText}</text>

                        <text x="${labelWidth / 2}" y="${labelHeight - 12}" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="3.6" fill="#231B16" font-weight="500">AÑADA ${wine.vintage}</text>
                        <text x="${labelWidth / 2}" y="${labelHeight - 4}" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="2.6" fill="#9C6F38" letter-spacing="0.2">${silhouette.toUpperCase()}</text>
                    </g>
                </svg>
            `;

            container.innerHTML = svg;
        }

        function updateUI(rec) {
            const wine = rec.primary_wine;
            document.getElementById("res-name").textContent = wine.name;
            document.getElementById("res-winery").textContent = wine.winery;
            document.getElementById("res-appellation").textContent = wine.appellation;
            document.getElementById("res-vintage").textContent = `Añada ${wine.vintage}`;
            document.getElementById("res-price").textContent = `${wine.price_eur.toFixed(2)} €`;
            document.getElementById("res-score").textContent = `${rec.compatibility_score.toFixed(1)}%`;
            document.getElementById("res-temp").textContent = `${wine.serving_temp_c.toFixed(0)} °C`;
            document.getElementById("res-decant").textContent = wine.decant_minutes > 0 ? `${wine.decant_minutes} min` : "Directo";
            document.getElementById("res-glass").textContent = wine.glass_type;
            document.getElementById("res-tagline").textContent = wine.tagline || (wine.winery + " · " + wine.appellation);
            document.getElementById("res-explanation").textContent = rec.sommelier_explanation;
            document.getElementById("res-notes").textContent = `«${wine.tasting_notes}»`;

            renderBottleVisual(wine);

            const altGrid = document.getElementById("res-alternatives");
            if (rec.alternative_wines && rec.alternative_wines.length > 0) {
                altGrid.innerHTML = rec.alternative_wines.map(alt => `
                    <div class="py-2.5 flex justify-between items-baseline gap-4 text-sm">
                        <div>
                            <span class="font-serif text-lg text-espresso">${alt.name}</span>
                            <span class="text-xs text-walnut ml-2">${alt.appellation}</span>
                        </div>
                        <span class="font-mono text-xs text-espresso tabular-nums shrink-0">${alt.price_eur.toFixed(2)} €</span>
                    </div>
                `).join("");
            } else {
                altGrid.innerHTML = `<p class="py-2 text-xs text-walnut italic">Sin alternativas adicionales bajo este presupuesto.</p>`;
            }

            renderRadarChart(rec.target_sensory, wine.sensory);
        }

        function renderRadarChart(target, wineSensory) {
            const ctx = document.getElementById('radarChart').getContext('2d');
            const labels = ['Cuerpo', 'Acidez', 'Taninos', 'Fruta', 'Madera'];
            const targetData = [target.body, target.acidity, target.tannins, target.fruit, target.oak];
            const wineData = [wineSensory.body, wineSensory.acidity, wineSensory.tannins, wineSensory.fruit, wineSensory.oak];

            if (radarChartInstance) {
                radarChartInstance.destroy();
            }

            radarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Vino Seleccionado',
                            data: wineData,
                            backgroundColor: 'rgba(107, 29, 40, 0.14)',
                            borderColor: '#6B1D28',
                            pointBackgroundColor: '#6B1D28',
                            pointBorderColor: '#F7F2E8',
                            borderWidth: 2
                        },
                        {
                            label: 'Demanda del Plato',
                            data: targetData,
                            backgroundColor: 'rgba(156, 111, 56, 0.12)',
                            borderColor: '#9C6F38',
                            pointBackgroundColor: '#9C6F38',
                            pointBorderColor: '#F7F2E8',
                            borderWidth: 1.5,
                            borderDash: [4, 3]
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(35, 27, 22, 0.1)' },
                            grid: { color: 'rgba(35, 27, 22, 0.1)' },
                            pointLabels: {
                                color: '#6A5A4F',
                                font: { family: '"Work Sans", sans-serif', size: 11, weight: '500' }
                            },
                            ticks: {
                                display: false,
                                min: 0,
                                max: 10,
                                stepSize: 2
                            },
                            suggestedMin: 0,
                            suggestedMax: 10
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }

        /* --- Atlas Cartográfico de Terroirs & Bodegas D.O. --- */

        async function initAtlas() {
            try {
                const res = await fetch("/api/v1/atlas/geojson?layer=wineries");
                if (!res.ok) throw new Error("Fallo al obtener GeoJSON del Atlas.");
                const data = await res.json();
                atlasFeatures = data.features || [];

                populateDoPills();

                if (atlasFeatures.length > 0) {
                    selectAtlasFeature(atlasFeatures[0]);
                }

                if (typeof L !== "undefined" && typeof L.map === "function") {
                    initLeafletAtlas();
                } else {
                    initSvgFallbackAtlas();
                }
            } catch (err) {
                console.warn("Leaflet offline o error GeoJSON, activando fallback SVG:", err);
                initSvgFallbackAtlas();
            }
        }

        function populateDoPills() {
            const container = document.getElementById("do-pills-bar");
            const dos = [...new Set(atlasFeatures.map(f => f.properties.appellation))].sort();

            dos.forEach(doName => {
                const btn = document.createElement("button");
                btn.type = "button";
                btn.setAttribute("data-do", doName);
                btn.className = "do-pill px-3 py-1.5 rounded-sm";
                btn.textContent = doName.replace("D.O.Ca. ", "").replace("D.O.Q. ", "").replace("D.O. ", "");
                btn.addEventListener("click", () => filterAtlasByDo(doName, btn));
                container.appendChild(btn);
            });

            const allBtn = container.querySelector('button[data-do=""]');
            if (allBtn) {
                allBtn.addEventListener("click", () => filterAtlasByDo("", allBtn));
            }
        }

        function filterAtlasByDo(doName, activeBtn) {
            selectedDo = doName;
            document.querySelectorAll(".do-pill").forEach(b => b.classList.remove("is-active"));
            if (activeBtn) activeBtn.classList.add("is-active");

            document.getElementById("atlas-selected-do-label").textContent = doName || "Todas las regiones (12 D.O.)";

            const matching = doName ? atlasFeatures.filter(f => f.properties.appellation === doName) : atlasFeatures;
            if (matching.length > 0) {
                selectAtlasFeature(matching[0]);
            }

            if (leafletMap) {
                if (doName && matching.length > 0) {
                    const first = matching[0];
                    leafletMap.setView([first.geometry.coordinates[1], first.geometry.coordinates[0]], 8, { animate: true });
                } else {
                    leafletMap.setView([40.2, -3.7], 6, { animate: true });
                }
            }

            highlightSvgMarkers(doName);
        }

        function selectAtlasFeature(feature) {
            activeAtlasFeature = feature;
            const p = feature.properties;

            document.getElementById("terroir-community").textContent = p.autonomous_community || "España";
            document.getElementById("terroir-altitude").textContent = `${p.altitude_m || 500} m altitud`;
            document.getElementById("terroir-do-name").textContent = p.appellation;
            document.getElementById("terroir-tagline").textContent = p.tagline || p.winery_catalog_summary || "";
            document.getElementById("terroir-climate").textContent = p.climate;
            document.getElementById("terroir-soil").textContent = p.soil;
            document.getElementById("terroir-grape").textContent = p.signature_grape;
            document.getElementById("terroir-winery").textContent = p.winery;
            document.getElementById("terroir-wine-name").textContent = `${p.name} (${p.vintage})`;

            const listEl = document.getElementById("terroir-wineries-list");
            const sameDoFeatures = atlasFeatures.filter(f => f.properties.appellation === p.appellation);
            document.getElementById("terroir-winery-count").textContent = `${sameDoFeatures.length} bodegas`;

            listEl.innerHTML = sameDoFeatures.map(f => {
                const isCur = f.id === feature.id;
                return `
                    <button type="button" data-feat-id="${f.id}" class="w-full text-left p-2 rounded flex items-center justify-between gap-2 text-xs transition ${isCur ? 'bg-bordeaux text-cream font-medium' : 'bg-cream hover:bg-butter text-espresso'}">
                        <span class="truncate">${f.properties.winery} · ${f.properties.name}</span>
                        <span class="font-mono text-[11px] shrink-0">${f.properties.price_eur.toFixed(2)} €</span>
                    </button>
                `;
            }).join("");

            listEl.querySelectorAll("button").forEach(btn => {
                btn.addEventListener("click", () => {
                    const fid = btn.getAttribute("data-feat-id");
                    const found = atlasFeatures.find(f => f.id === fid);
                    if (found) {
                        selectAtlasFeature(found);
                        if (leafletMap) {
                            leafletMap.setView([found.geometry.coordinates[1], found.geometry.coordinates[0]], 8, { animate: true });
                        }
                    }
                });
            });
        }

        function applyAtlasWineToRadar(feature) {
            const p = feature.properties;
            document.getElementById("res-name").textContent = p.name;
            document.getElementById("res-winery").textContent = p.winery;
            document.getElementById("res-appellation").textContent = p.appellation;
            document.getElementById("res-vintage").textContent = `Añada ${p.vintage}`;
            document.getElementById("res-price").textContent = `${p.price_eur.toFixed(2)} €`;
            document.getElementById("res-score").textContent = "98.0%";
            document.getElementById("res-temp").textContent = `${p.serving_temp_c || 16} °C`;
            document.getElementById("res-decant").textContent = (p.decant_minutes && p.decant_minutes > 0) ? `${p.decant_minutes} min` : "Directo";
            document.getElementById("res-glass").textContent = p.glass_type || "Burdeos";
            document.getElementById("res-tagline").textContent = p.tagline || p.winery_catalog_summary || (p.winery + " · " + p.appellation);
            document.getElementById("res-explanation").textContent = `Selección directa desde el Atlas de Terroirs: ${p.winery_catalog_summary}`;
            document.getElementById("res-notes").textContent = `«${p.tasting_notes}»`;

            renderBottleVisual(p);

            const currentDish = allDishes.find(d => d.id === selectedDishId);
            const targetSensory = currentDish ? currentDish.target_sensory : { body: 7.0, acidity: 7.0, tannins: 7.0, fruit: 7.0, oak: 7.0 };
            renderRadarChart(targetSensory, p.sensory);
        }

        function initLeafletAtlas() {
            try {
                const mapEl = document.getElementById("atlas-map");
                if (!mapEl) return;

                leafletMap = L.map("atlas-map", {
                    center: [40.2, -3.7],
                    zoom: 6,
                    zoomControl: true,
                    attributionControl: false
                });

                L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
                    maxZoom: 18,
                    subdomains: "abcd"
                }).addTo(leafletMap);

                const icon = L.divIcon({
                    className: "custom-pin",
                    html: '<div class="custom-pin-inner"></div>',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });

                atlasFeatures.forEach(feat => {
                    const coords = feat.geometry.coordinates;
                    const marker = L.marker([coords[1], coords[0]], { icon: icon }).addTo(leafletMap);
                    marker.bindTooltip(`<strong>${feat.properties.winery}</strong><br><span style="font-size:11px;color:#6A5A4F">${feat.properties.appellation} · ${feat.properties.name}</span>`, {
                        direction: "top",
                        offset: [0, -8]
                    });
                    marker.on("click", () => {
                        selectAtlasFeature(feat);
                    });
                    mapMarkers.push({ marker, feature: feat });
                });

                document.getElementById("map-engine-label").textContent = "Cartografía: Leaflet.js (CartoDB Positron)";
            } catch (err) {
                console.error("Leaflet init error, switching to SVG fallback:", err);
                initSvgFallbackAtlas();
            }
        }

        function initSvgFallbackAtlas() {
            const mapDiv = document.getElementById("atlas-map");
            const fallbackDiv = document.getElementById("atlas-svg-fallback");
            const canvas = document.getElementById("svg-map-canvas");
            if (mapDiv) mapDiv.classList.add("hidden");
            if (fallbackDiv) fallbackDiv.classList.remove("hidden");
            document.getElementById("map-engine-label").textContent = "Cartografía: SVG Determinista (Modo Offline)";

            const svgW = 680;
            const svgH = 340;

            function lonToX(lon) {
                return ((lon - (-9.5)) / (3.5 - (-9.5))) * (svgW - 80) + 40;
            }
            function latToY(lat) {
                return ((44.0 - lat) / (44.0 - 36.0)) * (svgH - 60) + 30;
            }

            let svgContent = `
                <svg viewBox="0 0 ${svgW} ${svgH}" class="w-full h-full select-none" xmlns="http://www.w3.org/2000/svg">
                    <!-- Stylized Iberian Peninsula Boundary -->
                    <path d="M 60 70 Q 180 40 320 50 Q 500 50 560 90 L 590 140 Q 580 200 540 260 Q 480 320 380 330 Q 280 330 180 320 Q 90 300 70 230 Q 50 150 60 70 Z" fill="#EFE7D6" stroke="rgba(35, 27, 22, 0.2)" stroke-width="1.5" stroke-dasharray="3 3"/>
                    <path d="M 120 70 Q 280 80 500 100" fill="none" stroke="rgba(107, 29, 40, 0.12)" stroke-width="1"/>
                    <path d="M 100 160 Q 300 170 540 180" fill="none" stroke="rgba(107, 29, 40, 0.12)" stroke-width="1"/>
            `;

            atlasFeatures.forEach(feat => {
                const coords = feat.geometry.coordinates;
                const x = lonToX(coords[0]);
                const y = latToY(coords[1]);
                svgContent += `
                    <g class="svg-pin cursor-pointer group" data-feat-id="${feat.id}" data-do="${feat.properties.appellation}" transform="translate(${x}, ${y})">
                        <circle r="7" fill="#6B1D28" stroke="#FAF6EE" stroke-width="1.5" class="transition-all duration-150 hover:r-9 hover:fill-[#9C6F38]"/>
                        <circle r="2" fill="#FAF6EE"/>
                        <title>${feat.properties.winery} (${feat.properties.appellation}) — ${feat.properties.name}</title>
                    </g>
                `;
            });

            svgContent += `</svg>`;
            canvas.innerHTML = svgContent;

            canvas.querySelectorAll(".svg-pin").forEach(pin => {
                pin.addEventListener("click", () => {
                    const fid = pin.getAttribute("data-feat-id");
                    const found = atlasFeatures.find(f => f.id === fid);
                    if (found) selectAtlasFeature(found);
                });
            });
        }

        function highlightSvgMarkers(doName) {
            const canvas = document.getElementById("svg-map-canvas");
            if (!canvas) return;
            canvas.querySelectorAll(".svg-pin").forEach(pin => {
                const pinDo = pin.getAttribute("data-do");
                const circle = pin.querySelector("circle");
                if (!circle) return;
                if (!doName || pinDo === doName) {
                    circle.setAttribute("fill", "#6B1D28");
                    circle.setAttribute("opacity", "1.0");
                } else {
                    circle.setAttribute("fill", "#6A5A4F");
                    circle.setAttribute("opacity", "0.35");
                }
            });
        }

        /* --- Evening & 3-Course Menu Sommelier Planner --- */

        function populatePlannerSelects() {
            const starterSelect = document.getElementById("plan-starter-select");
            const mainSelect = document.getElementById("plan-main-select");
            const dessertSelect = document.getElementById("plan-dessert-select");
            if (!starterSelect || !mainSelect || !dessertSelect || allDishes.length === 0) return;

            const starters = allDishes.filter(d => {
                const cat = getCategoryForDish(d);
                return cat === "Entrantes y Cuchara" || cat === "Tapas y Pintxos" || cat === "Ensaladas y Huerta";
            });
            const mains = allDishes.filter(d => {
                const cat = getCategoryForDish(d);
                return cat === "Carnes y Caza" || cat === "Pescados y Mariscos" || cat === "Arroces";
            });
            const desserts = allDishes.filter(d => {
                const cat = getCategoryForDish(d);
                return cat === "Embutidos y Quesos" || cat === "Postres y Dulces";
            });

            const fillSelect = (selectEl, list, defaultId) => {
                selectEl.innerHTML = list.map(d => `
                    <option value="${d.id}" ${d.id === defaultId ? 'selected' : ''}>
                        ${d.name} (${d.category})
                    </option>
                `).join("");
            };

            fillSelect(starterSelect, starters.length ? starters : allDishes, "salmorejo-cordobes");
            fillSelect(mainSelect, mains.length ? mains : allDishes, "chuleton-brasa");
            fillSelect(dessertSelect, desserts.length ? desserts : allDishes, "queso-manchego");
        }

        async function generateMenuPlan() {
            const starterId = document.getElementById("plan-starter-select")?.value || "salmorejo-cordobes";
            const mainId = document.getElementById("plan-main-select")?.value || "chuleton-brasa";
            const dessertId = document.getElementById("plan-dessert-select")?.value || "queso-manchego";
            const budget = parseFloat(document.getElementById("plan-budget-slider")?.value || "110");

            const payload = {
                occasion: selectedOccasion,
                starter_dish_id: starterId,
                main_dish_id: mainId,
                dessert_dish_id: dessertId,
                total_budget_eur: budget
            };

            try {
                const res = await fetch("/api/v1/pairings/menu-plan", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    const data = await res.json();
                    renderMenuPlanResults(data);
                    return;
                }
            } catch (err) {
                console.warn("Endpoint /api/v1/pairings/menu-plan no disponible aún, usando cálculo local de cata:", err);
            }

            const fallbackData = buildLocalMenuPlan(selectedOccasion, starterId, mainId, dessertId, budget);
            renderMenuPlanResults(fallbackData);
        }

        function buildLocalMenuPlan(occasion, starterId, mainId, dessertId, budget) {
            const starterDish = allDishes.find(d => d.id === starterId) || { name: "Salmorejo cordobés", description: "Crema fría de tomate y jamón ibérico" };
            const mainDish = allDishes.find(d => d.id === mainId) || { name: "Chuletón de vaca vieja", description: "Corte madurado a la brasa" };
            const dessertDish = allDishes.find(d => d.id === dessertId) || { name: "Queso Manchego Curado", description: "Leche cruda de oveja en cueva" };

            const occasionDetails = {
                "Cena Romántica": {
                    ambience: "Luz de velas tenue, copas finas de cristal y servicio pausado entre pases.",
                    rationale: "Progresión ascendente de sutil armonía: apertura cítrica y brioche de burbuja larga, corazón tánico elegante de roble riojano y cierre aristocrático de frutos secos con amontillado.",
                    wines: [
                        { name: "Gramona Imperial Brut Nature", winery: "Gramona", appellation: "Corpinnat", vintage: 2017, price_eur: 24.50, tagline: "Más de 50 meses de rima: burbuja cremosa, brioche y acidez gastronómica.", bottle_silhouette: "Espumosa", vintage_label: "En su cumbre hoy · 2021-2030", vintage_color: "green", fridge: "2 horas en nevera (servir a 8 °C)", uncork: "Descorche directo al servir; preservar burbuja fina", note: "La acidez cortante y la efervescencia fina desengrasan y potencian la frescura del entrante." },
                        { name: "Viña Ardanza Reserva", winery: "La Rioja Alta, S.A.", appellation: "D.O.Ca. Rioja", vintage: 2017, price_eur: 34.00, tagline: "Elegancia clásica riojana de taninos sedosos y crianza pausada en roble americano.", bottle_silhouette: "Bordelesa", vintage_label: "Plenitud de guarda · 2020-2035", vintage_color: "gold", fridge: "20 minutos de refresco en puerta de nevera (16 °C)", uncork: "Decantar 30 minutos antes para oxigenar aromas nobles", note: "El nervio tánico y la vainilla especiada abrazan la intensidad cárnica del plato fuerte." },
                        { name: "Fino La Panesa Especial", winery: "Emilio Hidalgo", appellation: "D.O. Jerez-Xérès-Sherry", vintage: 2018, price_eur: 32.00, tagline: "El único fino fermentado en bota de roble americano por el sistema de 10 criaderas.", bottle_silhouette: "Jerezana", vintage_label: "Solera viva centenaria", vintage_color: "gold", fridge: "40 minutos en nevera (servir fresco a 12-13 °C)", uncork: "Descorche directo en copa amplia de vino blanco", note: "La salinidad y la almendra verde realzan la curación láctica y la textura grasa del queso." }
                    ]
                },
                "Barbacoa con Amigos": {
                    ambience: "Mesa rústica al aire libre, brasas de sarmiento y copas amplias para compartir sin prisa.",
                    rationale: "Carácter directo y festivo: notas frescas y salinas para abrir boca, potencia estructurada frente al humo de la brasa y final goloso y expresivo.",
                    wines: [
                        { name: "Pazo Señorans Selección de Añada", winery: "Pazo de Señorans", appellation: "D.O. Rías Baixas", vintage: 2013, price_eur: 42.00, tagline: "El albariño de guarda más laureado con 30 meses de lías y noble hidrocarburo.", bottle_silhouette: "Borgoña", vintage_label: "En su cumbre hoy · 2019-2032", vintage_color: "green", fridge: "1 hora en nevera (servir a 10 °C)", uncork: "Descorchar 10 minutos antes", note: "La salinidad atlántica limpia el paladar con precisión milimétrica." },
                        { name: "Pago de Carraovejas", winery: "Pago de Carraovejas", appellation: "D.O. Ribera del Duero", vintage: 2021, price_eur: 46.00, tagline: "Potencia envolvente con tanino dulce y madurez voluptuosa de fruta negra.", bottle_silhouette: "Bordelesa", vintage_label: "En su cumbre hoy · 2023-2034", vintage_color: "green", fridge: "15 minutos de refresco (16 °C)", uncork: "Descorchar 20 minutos antes", note: "Volumen, tanino goloso y fruta madura impecables para el fuego de la parrilla." },
                        { name: "Pintia Toro", winery: "Bodegas y Viñedos Pintia", appellation: "D.O. Toro", vintage: 2018, price_eur: 48.00, tagline: "La elegancia contemporánea de Toro: redondez, moras y final especiado.", bottle_silhouette: "Bordelesa", vintage_label: "Plenitud de guarda · 2022-2035", vintage_color: "gold", fridge: "20 minutos de refresco (16 °C)", uncork: "Decantar 20 minutos", note: "Poderío tánico refinado que resiste la salinidad de los quesos más intensos." }
                    ]
                },
                "Comida Familiar de Domingo": {
                    ambience: "Sobremesa pausada, mantel de hilo largo y copas clásicas de cata.",
                    rationale: "Tradición y diálogo enológico: clasicismo aromático de guarda, armonía estructurada para platos de fuego lento y despedida señorial.",
                    wines: [
                        { name: "Terras Gauda O Rosal", winery: "Bodegas Terras Gauda", appellation: "D.O. Rías Baixas", vintage: 2023, price_eur: 16.50, tagline: "Frescura atlántica cristalina con pomelo, manzana verde y notas salinas.", bottle_silhouette: "Borgoña", vintage_label: "Joven y radiante · 2024-2028", vintage_color: "green", fridge: "2 horas en nevera (servir a 9 °C)", uncork: "Descorche directo al servir", note: "Apertura viva y aromática que despierta el apetito de toda la mesa." },
                        { name: "Viña Tondonia Reserva Tinto", winery: "R. López de Heredia", appellation: "D.O.Ca. Rioja", vintage: 2011, price_eur: 42.00, tagline: "Icono universal de elegancia aristocrática, trufa negra y persistencia sin fin.", bottle_silhouette: "Bordelesa", vintage_label: "Gran Reserva Maduro · 2018-2036", vintage_color: "gold", fridge: "Temperatura ambiente de bodega (17 °C)", uncork: "Decantar 40 minutos para despertar terciarios", note: "Un clásico monumental con notas de cuero noble, tabaco y tanino aterciopelado." },
                        { name: "Amontillado Tradición VOS", winery: "Bodegas Tradición", appellation: "D.O. Jerez-Xérès-Sherry", vintage: 2010, price_eur: 52.00, tagline: "Oxidación aristocrática: ebanistería noble, nuez tostada y final seco infinito.", bottle_silhouette: "Jerezana", vintage_label: "Solera VOS > 20 años", vintage_color: "gold", fridge: "45 minutos en nevera (servir a 13 °C)", uncork: "Descorchar directo en copa amplia", note: "Sobremesa sublime con notas de madera vieja y avellanas tostadas." }
                    ]
                },
                "Tardeo & Tapas Gourmet": {
                    ambience: "Música ambiental chic, picoteo selecto al centro y copas de pie esbelto.",
                    rationale: "Secuencia ágil y gastronómica: burbujas biodinámicas vivas, fruta roja atlántica fluida y cierre mineral con garnachas viejas.",
                    wines: [
                        { name: "Recaredo Terrers Brut Nature", winery: "Recaredo", appellation: "Corpinnat", vintage: 2019, price_eur: 26.00, tagline: "Biodinámica rigurosa, tapón de corcho en rima y sequedad salina insuperable.", bottle_silhouette: "Espumosa", vintage_label: "En su cumbre hoy · 2022-2030", vintage_color: "green", fridge: "2 horas en nevera (servir a 8 °C)", uncork: "Descorchar con cuidado al momento", note: "Sequedad salina rigurosa que eleva cada bocado del aperitivo." },
                        { name: "Ultreia Saint Jacques", winery: "Raúl Pérez Viticultor", appellation: "D.O. Bierzo", vintage: 2021, price_eur: 14.50, tagline: "Fragancia de violetas, frambuesa fresca y fluidez atlántica de Mencía.", bottle_silhouette: "Borgoña", vintage_label: "En su cumbre hoy · 2023-2029", vintage_color: "green", fridge: "20 minutos en nevera (servir a 14 °C)", uncork: "Descorche directo", note: "Mencía sedosa y fresca que marida con fluidez sin saturar el paladar." },
                        { name: "La Bruja de Rozas", winery: "Comando G", appellation: "D.O. Vinos de Madrid", vintage: 2021, price_eur: 19.50, tagline: "Finura casi borgoñona con especias silvestres y acidez vibrante.", bottle_silhouette: "Borgoña", vintage_label: "En su cumbre hoy · 2023-2030", vintage_color: "green", fridge: "20 minutos de refresco (15 °C)", uncork: "Servir en copa Borgoña", note: "Garnacha de altura con violetas y granito que redondea el pase final." }
                    ]
                }
            };

            const occ = occasionDetails[occasion] || occasionDetails["Cena Romántica"];
            const rawWines = occ.wines;
            const courses = [
                {
                    course_number: 1,
                    course_title: "1.º Pase · Entrante / Aperitivo",
                    dish_name: starterDish.name,
                    dish_description: starterDish.description,
                    wine: rawWines[0],
                    vintage_status_label: rawWines[0].vintage_label,
                    vintage_color: rawWines[0].vintage_color,
                    fridge_tip: rawWines[0].fridge,
                    uncork_tip: rawWines[0].uncork,
                    sommelier_note: rawWines[0].note
                },
                {
                    course_number: 2,
                    course_title: "2.º Pase · Plato Principal",
                    dish_name: mainDish.name,
                    dish_description: mainDish.description,
                    wine: rawWines[1],
                    vintage_status_label: rawWines[1].vintage_label,
                    vintage_color: rawWines[1].vintage_color,
                    fridge_tip: rawWines[1].fridge,
                    uncork_tip: rawWines[1].uncork,
                    sommelier_note: rawWines[1].note
                },
                {
                    course_number: 3,
                    course_title: "3.º Pase · Quesos o Postre",
                    dish_name: dessertDish.name,
                    dish_description: dessertDish.description,
                    wine: rawWines[2],
                    vintage_status_label: rawWines[2].vintage_label,
                    vintage_color: rawWines[2].vintage_color,
                    fridge_tip: rawWines[2].fridge,
                    uncork_tip: rawWines[2].uncork,
                    sommelier_note: rawWines[2].note
                }
            ];

            const total = courses.reduce((acc, c) => acc + c.wine.price_eur, 0);

            return {
                occasion: occasion,
                total_price_eur: total,
                average_compatibility_score: 95.8,
                ambience_tip: occ.ambience,
                progression_rationale: occ.rationale,
                courses: courses
            };
        }

        function renderMenuPlanResults(data) {
            const totalPrice = data.total_price_eur || data.total_price || 0;
            const avgScore = data.average_compatibility_score || data.average_score || data.avg_score || 95.0;
            const ambienceTip = data.occasion_ambience_tip || data.ambience_tip || data.occasion_tip || "Iluminación cálida y conversación sosegada.";
            const progressionSummary = data.progression_summary || data.progression_rationale || data.rationale || "Progresión enológica armónica.";
            const courses = data.courses || [];

            document.getElementById("plan-total-price").textContent = `${totalPrice.toFixed(2)} €`;
            document.getElementById("plan-avg-score").textContent = `${avgScore.toFixed(1)}%`;
            document.getElementById("plan-ambience-tip").textContent = `Ambiente: ${ambienceTip}`;
            document.getElementById("plan-progression-summary").textContent = progressionSummary;

            // Render 3 Course Cards in grid
            const coursesGrid = document.getElementById("plan-courses-grid");
            coursesGrid.innerHTML = courses.map((course, idx) => {
                const wine = course.wine || {};
                const courseTitle = course.course_title || `${idx + 1}.º Pase`;
                const dishName = (course.dish && course.dish.name) || course.dish_name || "Plato seleccionado";
                const dishDesc = (course.dish && course.dish.description) || course.dish_description || "";
                const vintageLabel = course.vintage_status_label || course.vintage_status || "En su cumbre hoy";
                const semaphore = course.vintage_semaphore || course.vintage_color || "green";

                let badgeColorClass = "bg-sage/15 text-sage border-sage/30";
                if (semaphore === "gold" || vintageLabel.includes("Plenitud") || vintageLabel.includes("óptima") || vintageLabel.includes("Solera")) {
                    badgeColorClass = "bg-brass/15 text-brass border-brass/30";
                } else if (semaphore === "amber" || vintageLabel.includes("Maduro") || vintageLabel.includes("Gran Reserva")) {
                    badgeColorClass = "bg-amber-100 text-amber-900 border-amber-300";
                }

                return `
                    <div class="bg-cream border border-espresso/15 rounded p-5 space-y-4 flex flex-col justify-between shadow-2xs">
                        <div class="space-y-3">
                            <div class="flex items-center justify-between gap-2 border-b border-espresso/10 pb-2">
                                <span class="text-xs font-mono text-bordeaux uppercase tracking-wider font-semibold">${courseTitle}</span>
                                <span class="text-[10px] font-mono px-2 py-0.5 rounded border ${badgeColorClass} font-medium">
                                    ${vintageLabel}
                                </span>
                            </div>

                            <div class="space-y-1">
                                <h4 class="font-serif text-xl text-espresso font-normal leading-tight">${dishName}</h4>
                                <div class="text-xs font-serif italic text-walnut">${dishDesc}</div>
                            </div>

                            <div class="pt-2 border-t border-espresso/8 space-y-1">
                                <div class="flex justify-between items-baseline gap-2">
                                    <span class="font-serif text-lg text-bordeaux font-medium">${wine.name || ''}</span>
                                    <span class="font-mono text-xs text-espresso font-semibold tabular-nums shrink-0">${(wine.price_eur || 0).toFixed(2)} €</span>
                                </div>
                                <div class="text-xs font-mono text-walnut">
                                    ${wine.winery || ''} · ${wine.appellation || ''} (Añada ${wine.vintage || ''})
                                </div>
                                <p class="text-xs font-serif italic text-walnut/90 line-clamp-2 mt-1">«${wine.tagline || wine.tasting_notes || ''}»</p>
                            </div>
                        </div>

                        <div class="space-y-2 pt-3 border-t border-espresso/10 text-xs">
                            <div class="bg-butter/60 rounded p-2.5 space-y-1.5 font-sans">
                                <div class="text-[11px] text-espresso/90 flex items-start gap-1.5">
                                    <span class="shrink-0">❄️</span>
                                    <span><strong>Nevera:</strong> ${course.fridge_tip || 'Temperatura recomendada'}</span>
                                </div>
                                <div class="text-[11px] text-espresso/90 flex items-start gap-1.5">
                                    <span class="shrink-0">🍾</span>
                                    <span><strong>Descorche:</strong> ${course.uncork_tip || 'Servicio directo'}</span>
                                </div>
                            </div>
                            <p class="text-[11px] text-walnut italic leading-relaxed pt-1">
                                ${course.sommelier_note || ''}
                            </p>
                        </div>
                    </div>
                `;
            }).join("");

            // Render Printable Guest Menu Card
            const printList = document.getElementById("print-courses-list");
            document.getElementById("print-card-title").textContent = data.printable_card_title || data.occasion || selectedOccasion;
            printList.innerHTML = courses.map((course, idx) => {
                const wine = course.wine || {};
                const courseTitle = course.course_title || `${idx + 1}.º Pase`;
                const dishName = (course.dish && course.dish.name) || course.dish_name || "Plato seleccionado";
                return `
                    <div class="pt-4 first:pt-0 space-y-2">
                        <div class="flex items-baseline justify-between text-xs font-mono text-bordeaux uppercase tracking-wider">
                            <span class="font-semibold">${courseTitle}</span>
                            <span class="text-walnut">${wine.appellation || ''} · Añada ${wine.vintage || ''}</span>
                        </div>
                        <div class="flex flex-wrap items-baseline justify-between gap-3">
                            <h4 class="font-serif text-2xl text-espresso">${dishName}</h4>
                            <span class="font-serif text-xl text-bordeaux font-normal">${wine.name || ''}</span>
                        </div>
                        <div class="flex justify-between items-baseline text-xs font-mono text-walnut">
                            <span>Bodega: ${wine.winery || ''}</span>
                            <span class="tabular-nums font-medium text-espresso">${(wine.price_eur || 0).toFixed(2)} €</span>
                        </div>
                        <p class="font-serif italic text-sm text-walnut/90">«${wine.tagline || wine.tasting_notes || ''}»</p>
                    </div>
                `;
            }).join("");
        }

        window.addEventListener("DOMContentLoaded", init);
    </script>
</body>
</html>"""
