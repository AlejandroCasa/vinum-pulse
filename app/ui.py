"""UI templates and interactive 4-tab SPA workspace for Vinum Pulse."""

_DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vinum Pulse — Atlas, Sumiller, Veladas &amp; Bodega</title>
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
        ::-webkit-scrollbar { width: 7px; height: 7px; }
        ::-webkit-scrollbar-track { background: #EFE7D6; }
        ::-webkit-scrollbar-thumb { background: rgba(107, 29, 40, 0.25); border-radius: 4px; }

        .menu-frame {
            border-top: 1px solid rgba(35, 27, 22, 0.14);
            border-bottom: 1px solid rgba(35, 27, 22, 0.14);
        }
        .workspace-tab {
            transition: background-color 180ms var(--ease-bistro), color 180ms var(--ease-bistro), box-shadow 180ms var(--ease-bistro);
        }
        .workspace-tab.is-active {
            background-color: #6B1D28;
            color: #F7F2E8;
            box-shadow: 0 1px 4px rgba(35, 27, 22, 0.18);
        }
        .tab-panel {
            animation: panelReveal 220ms var(--ease-bistro);
        }
        @keyframes panelReveal {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
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
        .style-tab, .catalog-type-pill, .atlas-layer-btn, .atlas-basemap-btn, .cellar-filter-btn {
            transition: all 180ms var(--ease-bistro);
        }
        .atlas-layer-btn.is-active, .atlas-basemap-btn.is-active, .catalog-type-pill.is-active, .cellar-filter-btn.is-active {
            background-color: #6B1D28;
            border-color: #6B1D28;
            color: #F7F2E8;
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
        .toast-item {
            animation: toastSlideIn 220ms var(--ease-bistro);
        }
        @keyframes toastSlideIn {
            from { opacity: 0; transform: translateY(10px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
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
            outline-offset: 2px;
        }
        .tabular-nums { font-variant-numeric: tabular-nums; }

        /* Leaflet custom styling */
        .leaflet-container {
            background: #FAF6EE !important;
            font-family: "Work Sans", sans-serif;
        }
        .vinum-editorial-tiles {
            filter: sepia(24%) saturate(52%) contrast(93%) brightness(103%);
        }
        .leaflet-control-attribution {
            background: rgba(247, 242, 232, 0.88) !important;
            color: #6A5A4F !important;
            font-family: "JetBrains Mono", monospace !important;
            font-size: 9px !important;
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
            transform: scale(1.22);
            background: #9C6F38;
        }
        .custom-pin-inner {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #F7F2E8;
        }
        .custom-region-pin {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: rgba(156, 111, 56, 0.92);
            border: 2px solid #231B16;
            box-shadow: 0 2px 8px rgba(35, 27, 22, 0.3);
            cursor: pointer;
            transition: transform 150ms ease;
        }
        .custom-region-pin:hover {
            transform: scale(1.18);
            background: #6B1D28;
        }
        .custom-region-pin-inner {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #FAF6EE;
        }

        /* Print Media Styles for Printable Menu Card */
        @media print {
            body {
                background-color: #FAF6EE !important;
                color: #231B16 !important;
            }
            .no-print, #app-header, header, footer, #toast-container, #error-banner,
            #panel-atlas, #panel-carte, #panel-bodega,
            #occasion-selector, #plan-inputs-container, #btn-generate-menu-plan,
            #btn-print-menu, #progression-chart-panel,
            #menu-plan-results > div:not(#printable-menu-card) {
                display: none !important;
            }
            #panel-veladas {
                display: block !important;
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
<body class="min-h-screen font-sans antialiased text-espresso flex flex-col">
    <!-- Sticky Editorial App-Shell Header -->
    <header id="app-header" class="sticky top-0 z-40 bg-cream/95 backdrop-blur-md border-b border-espresso/15 no-print">
        <div class="max-w-6xl mx-auto px-4 sm:px-8 py-3 space-y-3">
            <!-- Brand Identity & Global KPI Pills -->
            <div class="flex flex-wrap items-center justify-between gap-3">
                <a href="#atlas" onclick="switchTab('atlas'); return false;" class="flex items-center gap-3 group focus:outline-none">
                    <span class="w-9 h-9 rounded-full bg-bordeaux text-cream flex items-center justify-center shadow-xs group-hover:bg-espresso transition">
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                            <path d="M8 22h8M12 15v7M6 3h12l-1.2 6.5a5 5 0 0 1-9.6 0L6 3Z"/>
                        </svg>
                    </span>
                    <div>
                        <div class="flex items-baseline gap-2.5">
                            <h1 class="font-serif text-2xl sm:text-3xl tracking-tight text-espresso leading-none">Vinum Pulse</h1>
                            <span class="hidden sm:inline text-xs font-serif italic text-walnut">Cave &amp; Table</span>
                        </div>
                        <p class="text-[11px] font-mono text-walnut/85 hidden md:block">
                            Atlas Cartográfico, Sumiller Sensorial, Veladas &amp; Bodega Personal
                        </p>
                    </div>
                </a>

                <!-- Global KPI Pills -->
                <div id="global-kpis" class="flex flex-wrap items-center gap-2 text-[11px] font-mono">
                    <span id="kpi-wines-count" class="px-2.5 py-1 rounded bg-butter border border-espresso/12 text-espresso tabular-nums">
                        __KPI_WINES_COUNT__ Vinos
                    </span>
                    <span id="kpi-regions-count" class="px-2.5 py-1 rounded bg-butter border border-espresso/12 text-bordeaux tabular-nums">
                        __KPI_REGIONS_COUNT__ D.O.
                    </span>
                    <button type="button" id="kpi-cellar-pill" onclick="switchTab('bodega')" class="px-2.5 py-1 rounded bg-cream hover:bg-butter border border-bordeaux/25 text-espresso transition cursor-pointer tabular-nums flex items-center gap-1.5">
                        <span class="w-1.5 h-1.5 rounded-full bg-sage"></span>
                        <span>Bodega: <strong id="kpi-cellar-bottles">0</strong> bot. · <strong id="kpi-cellar-value">0 €</strong></span>
                    </button>
                </div>
            </div>

            <!-- 4-Tab Segmented Workspace Navigation Bar -->
            <nav id="workspace-tablist" role="tablist" aria-label="Espacios de trabajo de Vinum Pulse" class="flex items-center gap-1.5 p-1 rounded bg-butter/85 border border-espresso/12 overflow-x-auto">
                <button type="button" role="tab" id="tab-btn-atlas" data-tab="atlas" aria-controls="panel-atlas" aria-selected="true" tabindex="0" class="workspace-tab is-active flex-1 min-w-[140px] py-2 px-3.5 rounded-sm text-xs font-mono uppercase tracking-wider flex items-center justify-center gap-2 cursor-pointer whitespace-nowrap">
                    <span aria-hidden="true">🗺️</span>
                    <span>Atlas &amp; Terroir</span>
                </button>
                <button type="button" role="tab" id="tab-btn-carte" data-tab="carte" aria-controls="panel-carte" aria-selected="false" tabindex="-1" class="workspace-tab text-walnut hover:text-espresso flex-1 min-w-[160px] py-2 px-3.5 rounded-sm text-xs font-mono uppercase tracking-wider flex items-center justify-center gap-2 cursor-pointer whitespace-nowrap">
                    <span aria-hidden="true">🍷</span>
                    <span>La Carte &amp; Sommelier</span>
                </button>
                <button type="button" role="tab" id="tab-btn-veladas" data-tab="veladas" aria-controls="panel-veladas" aria-selected="false" tabindex="-1" class="workspace-tab text-walnut hover:text-espresso flex-1 min-w-[160px] py-2 px-3.5 rounded-sm text-xs font-mono uppercase tracking-wider flex items-center justify-center gap-2 cursor-pointer whitespace-nowrap">
                    <span aria-hidden="true">🕯️</span>
                    <span>Diseñador de Veladas</span>
                </button>
                <button type="button" role="tab" id="tab-btn-bodega" data-tab="bodega" aria-controls="panel-bodega" aria-selected="false" tabindex="-1" class="workspace-tab text-walnut hover:text-espresso flex-1 min-w-[140px] py-2 px-3.5 rounded-sm text-xs font-mono uppercase tracking-wider flex items-center justify-center gap-2 cursor-pointer whitespace-nowrap">
                    <span aria-hidden="true">🍾</span>
                    <span>Mi Bodega</span>
                    <span id="tab-badge-bodega" class="px-1.5 py-0.5 text-[10px] rounded-full bg-cream/85 text-bordeaux font-semibold tabular-nums">0</span>
                </button>
            </nav>
        </div>
    </header>

    <main class="max-w-6xl w-full mx-auto px-4 sm:px-8 py-6 sm:py-8 flex-1 space-y-6">
        <!-- Inline Error Banner -->
        <div id="error-banner" role="alert" class="hidden border border-bordeaux/30 bg-butter px-4 py-3 rounded text-bordeaux text-sm flex items-center justify-between gap-4 no-print">
            <span id="error-message">No hay vinos disponibles con estos filtros.</span>
            <button type="button" onclick="hideError()" class="text-xs font-mono underline underline-offset-4 cursor-pointer">Cerrar</button>
        </div>

        <!-- ================================================================== -->
        <!-- TAB 1: ATLAS & TERROIR (#atlas)                                    -->
        <!-- ================================================================== -->
        <section id="panel-atlas" role="tabpanel" aria-labelledby="tab-btn-atlas" class="tab-panel space-y-8 no-print">
            <div id="atlas-section" class="space-y-6">
                <!-- Section Title & Layer Toggles -->
                <div class="flex flex-wrap items-end justify-between gap-4 border-b border-espresso/15 pb-4">
                    <div class="space-y-1">
                        <div class="text-xs font-mono text-bordeaux uppercase tracking-wider flex items-center gap-2">
                            <span class="inline-block w-2 h-2 rounded-full bg-bordeaux"></span>
                            Geografía &amp; Terroir Peninsular
                        </div>
                        <h2 class="font-serif text-3xl sm:text-4xl text-espresso tracking-tight">
                            Atlas Cartográfico de Terroirs &amp; Bodegas D.O.
                        </h2>
                        <p class="font-serif italic text-base text-walnut">
                            __KPI_REGIONS_COUNT__ Denominaciones de Origen y __KPI_WINES_COUNT__ bodegas emblemáticas en __KPI_COUNTRIES_COUNT__ países
                        </p>
                    </div>

                    <div class="flex flex-wrap items-center gap-2">
                        <!-- Layer Toggles (wineries / regions / all) -->
                        <div id="atlas-layer-bar" role="group" aria-label="Capas del mapa" class="inline-flex rounded border border-espresso/15 bg-butter/60 p-0.5 text-[11px] font-mono">
                            <button type="button" data-layer="wineries" class="atlas-layer-btn is-active px-2.5 py-1 rounded-xs cursor-pointer">Bodegas</button>
                            <button type="button" data-layer="regions" class="atlas-layer-btn px-2.5 py-1 rounded-xs text-walnut hover:text-espresso cursor-pointer">Regiones D.O.</button>
                            <button type="button" data-layer="all" class="atlas-layer-btn px-2.5 py-1 rounded-xs text-walnut hover:text-espresso cursor-pointer">Todo</button>
                        </div>
                        <span id="atlas-status-badge" class="px-3 py-1.5 text-xs font-mono rounded bg-butter text-bordeaux border border-bordeaux/20 tabular-nums">
                            __KPI_REGIONS_COUNT__ Regiones · __KPI_WINES_COUNT__ Bodegas
                        </span>
                    </div>
                </div>

                <!-- Country Quick-Select Pill Bar (European Atlas) -->
                <div class="space-y-2">
                    <div class="flex justify-between items-center text-xs font-mono text-walnut">
                        <span>Atlas Vitivinícola Europeo · Selección de País</span>
                        <span id="atlas-selected-country-label" class="text-bordeaux font-medium">Europa (__KPI_COUNTRIES_COUNT__ Países)</span>
                    </div>
                    <div id="country-pills-bar" role="group" aria-label="Filtro de país del atlas" class="flex flex-wrap gap-2 text-xs font-mono">
                        <button type="button" data-country="" class="country-pill do-pill px-3 py-1.5 rounded-sm is-active cursor-pointer">Todos (Europa)</button>
                        <button type="button" data-country="España" class="country-pill do-pill px-3 py-1.5 rounded-sm cursor-pointer">España</button>
                        <button type="button" data-country="Francia" class="country-pill do-pill px-3 py-1.5 rounded-sm cursor-pointer">Francia</button>
                        <button type="button" data-country="Italia" class="country-pill do-pill px-3 py-1.5 rounded-sm cursor-pointer">Italia</button>
                        <button type="button" data-country="Inglaterra" class="country-pill do-pill px-3 py-1.5 rounded-sm cursor-pointer">Inglaterra</button>
                    </div>
                </div>

                <!-- D.O. Quick-Select Pill Bar -->
                <div class="space-y-2">
                    <div class="flex justify-between items-center text-xs font-mono text-walnut">
                        <span>Filtro por Denominación / AOC / DOCG / PDO</span>
                        <span id="atlas-selected-do-label" class="text-bordeaux font-medium">Todas las regiones</span>
                    </div>
                    <div id="do-pills-bar" class="flex flex-wrap gap-2 text-xs font-mono">
                        <button type="button" data-do="" class="do-pill px-3 py-1.5 rounded-sm is-active cursor-pointer">Todas (32 Regiones)</button>
                    </div>
                </div>

                <!-- Asymmetric Map (7 cols) & Terroir Inspector (5 cols) -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                    <!-- Map Column -->
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
                                    <span id="svg-fallback-counter" class="text-bordeaux font-medium">__KPI_REGIONS_COUNT__ D.O. / __KPI_WINES_COUNT__ Bodegas</span>
                                </div>
                                <div id="svg-map-canvas" class="w-full h-[380px] flex items-center justify-center"></div>
                            </div>
                        </div>
                        <div class="flex flex-wrap justify-between items-center text-[11px] font-mono text-walnut px-1 gap-2">
                            <div id="atlas-basemap-bar" role="group" aria-label="Proveedor cartográfico" class="inline-flex rounded border border-espresso/15 bg-butter/60 p-0.5 text-[10px] font-mono">
                                <button type="button" data-basemap="osm-editorial" class="atlas-basemap-btn is-active px-2 py-0.5 rounded-xs cursor-pointer">OSM Editorial</button>
                                <button type="button" data-basemap="ign-espana" class="atlas-basemap-btn px-2 py-0.5 rounded-xs text-walnut hover:text-espresso cursor-pointer">IGN España</button>
                                <button type="button" data-basemap="svg-offline" class="atlas-basemap-btn px-2 py-0.5 rounded-xs text-walnut hover:text-espresso cursor-pointer">SVG Offline</button>
                            </div>
                            <span id="map-engine-label" class="text-sage">Cartografía: OpenStreetMap Editorial (Zero-Key Open Source)</span>
                        </div>
                        <p class="text-[11px] font-mono text-walnut/80 px-1">
                            Haz clic en un marcador para inspeccionar el terroir y actualizar el Radar Sensorial 5D.
                        </p>
                    </div>

                    <!-- Terroir & Climate Inspector -->
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
                            <div id="terroir-wineries-list" class="space-y-1.5 max-h-[140px] overflow-y-auto pr-1"></div>
                        </div>

                        <!-- Contextual Bridges from Atlas -->
                        <div class="pt-2 border-t border-espresso/12 space-y-2.5">
                            <button type="button" id="btn-sync-radar" class="w-full py-2.5 px-4 bg-bordeaux text-cream text-xs font-mono uppercase tracking-wider rounded hover:bg-bordeaux/90 transition shadow-xs cursor-pointer">
                                Proyectar Perfil en Radar 5D
                            </button>
                            <div class="grid grid-cols-2 gap-2.5">
                                <button type="button" id="btn-atlas-to-carte" class="py-2 px-3 bg-cream hover:bg-butter text-espresso border border-espresso/20 text-xs font-mono rounded transition cursor-pointer flex items-center justify-center gap-1">
                                    <span>Ver en La Carte →</span>
                                </button>
                                <button type="button" id="btn-atlas-to-bodega" class="py-2 px-3 bg-cream hover:bg-butter text-bordeaux border border-bordeaux/30 text-xs font-mono rounded transition cursor-pointer flex items-center justify-center gap-1 font-medium">
                                    <span>+ Bodega</span>
                                </button>
                            </div>
                        </div>
                    </aside>
                </div>

                <!-- 5-Axis Sensory Radar Comparison Panel (Integrated in Tab 1) -->
                <div id="atlas-radar-panel" class="bg-butter/45 border border-espresso/15 rounded p-6 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                    <div class="lg:col-span-5 space-y-3">
                        <div class="flex items-center justify-between gap-2">
                            <span class="text-xs font-mono text-bordeaux uppercase tracking-wider">Radar Sensorial 5D · Comparativa Terroir</span>
                            <span id="atlas-radar-score" class="px-2.5 py-0.5 text-xs font-mono rounded bg-sage/15 text-sage border border-sage/30 tabular-nums font-medium">
                                92.0% afinidad
                            </span>
                        </div>
                        <h3 id="atlas-radar-title" class="font-serif text-2xl sm:text-3xl text-espresso leading-tight">
                            Viña Ardanza Reserva
                        </h3>
                        <p id="atlas-radar-subtitle" class="text-xs font-mono text-walnut">
                            La Rioja Alta, S.A. · D.O.Ca. Rioja · 34.00 €
                        </p>
                        <p id="atlas-radar-notes" class="font-serif italic text-sm text-walnut leading-relaxed">
                            Selecciona una bodega o región en el mapa para comparar su huella de Cuerpo, Acidez, Taninos, Fruta y Madera frente al plato de referencia.
                        </p>

                        <!-- Reference Dish selector for live radar overlay -->
                        <div class="pt-2 space-y-1.5">
                            <label for="atlas-radar-dish-select" class="block text-[11px] font-mono text-walnut uppercase tracking-wide">
                                Comparar contra plato de La Carte
                            </label>
                            <select id="atlas-radar-dish-select" class="w-full bg-cream border border-espresso/20 rounded p-2 text-xs font-sans text-espresso focus:border-bordeaux focus:ring-0">
                            </select>
                        </div>

                        <!-- 5-Axis Numeric Strip -->
                        <div id="atlas-sensory-bars" class="grid grid-cols-5 gap-2 pt-2 text-center font-mono">
                            <div class="bg-cream border border-espresso/10 rounded py-1.5 px-1">
                                <div class="text-[10px] text-walnut">Cuerpo</div>
                                <div id="atlas-val-body" class="text-xs font-semibold text-espresso tabular-nums">7.5</div>
                            </div>
                            <div class="bg-cream border border-espresso/10 rounded py-1.5 px-1">
                                <div class="text-[10px] text-walnut">Acidez</div>
                                <div id="atlas-val-acidity" class="text-xs font-semibold text-espresso tabular-nums">7.0</div>
                            </div>
                            <div class="bg-cream border border-espresso/10 rounded py-1.5 px-1">
                                <div class="text-[10px] text-walnut">Taninos</div>
                                <div id="atlas-val-tannins" class="text-xs font-semibold text-espresso tabular-nums">7.5</div>
                            </div>
                            <div class="bg-cream border border-espresso/10 rounded py-1.5 px-1">
                                <div class="text-[10px] text-walnut">Fruta</div>
                                <div id="atlas-val-fruit" class="text-xs font-semibold text-espresso tabular-nums">7.5</div>
                            </div>
                            <div class="bg-cream border border-espresso/10 rounded py-1.5 px-1">
                                <div class="text-[10px] text-walnut">Madera</div>
                                <div id="atlas-val-oak" class="text-xs font-semibold text-espresso tabular-nums">8.0</div>
                            </div>
                        </div>
                    </div>

                    <div class="lg:col-span-7 flex flex-col items-center justify-center space-y-2">
                        <div class="relative w-full max-w-[300px] aspect-square">
                            <canvas id="atlasRadarChart"></canvas>
                        </div>
                        <div class="flex justify-center gap-5 text-[11px] font-mono text-walnut">
                            <span class="flex items-center gap-1.5">
                                <span class="w-2.5 h-2.5 rounded-full bg-bordeaux"></span> Terroir / Vino Activo
                            </span>
                            <span class="flex items-center gap-1.5">
                                <span class="w-2.5 h-2.5 rounded-full bg-brass"></span> Demanda del Plato
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================================================================== -->
        <!-- TAB 2: LA CARTE & SOMMELIER (#carte)                               -->
        <!-- ================================================================== -->
        <section id="panel-carte" role="tabpanel" aria-labelledby="tab-btn-carte" class="tab-panel hidden space-y-12 no-print">
            <!-- Instant Dish-to-Wine Pairing Workbench -->
            <div class="menu-frame py-8 grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-start">
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
                                    <span id="active-dish-category" class="text-[10px] font-mono px-2 py-0.5 rounded bg-cream border border-espresso/10 text-walnut">Carnes y Caza</span>
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
                        <div id="dish-grid" class="space-y-2"></div>
                    </section>

                    <!-- En Bodega: Budget and Style Filters -->
                    <section class="space-y-6 pt-2">
                        <h2 class="font-serif text-2xl text-espresso border-b border-espresso/15 pb-2.5">Preferencias de Maridaje</h2>

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
                                <button type="button" data-type="" class="style-tab pb-1.5 text-sm font-medium border-b-2 border-bordeaux text-bordeaux cursor-pointer">Todos</button>
                                <button type="button" data-type="Red" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso cursor-pointer">Tinto</button>
                                <button type="button" data-type="White" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso cursor-pointer">Blanco</button>
                                <button type="button" data-type="Sparkling" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso cursor-pointer">Espumoso</button>
                                <button type="button" data-type="Fortified" class="style-tab pb-1.5 text-sm border-b-2 border-transparent text-walnut hover:text-espresso cursor-pointer">Generoso</button>
                            </div>
                        </div>
                    </section>
                </aside>

                <!-- Right: Le Choix du Sommelier (7 cols) -->
                <section id="results-section" class="lg:col-span-7 lg:border-l lg:border-espresso/12 lg:pl-10 space-y-6">
                    <!-- Wine Header -->
                    <div class="flex flex-wrap justify-between items-baseline gap-4 border-b border-espresso/15 pb-5">
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

                    <!-- Contextual Bridge Action Bar on Pairing Recommendation -->
                    <div class="flex flex-wrap items-center justify-between gap-3 bg-butter/55 border border-espresso/12 rounded px-4 py-2.5">
                        <div class="flex flex-wrap items-center gap-x-6 gap-y-1 text-xs text-walnut">
                            <span>Servicio <strong id="res-temp" class="font-medium text-espresso tabular-nums">17 °C</strong></span>
                            <span>Decantación <strong id="res-decant" class="font-medium text-espresso tabular-nums">30 min</strong></span>
                            <span>Copa <strong id="res-glass" class="font-medium text-espresso">Burdeos</strong></span>
                        </div>
                        <div class="flex flex-wrap items-center gap-2">
                            <button type="button" id="btn-pairing-add-cellar" class="px-3 py-1.5 bg-bordeaux text-cream text-[11px] font-mono rounded hover:bg-bordeaux/90 transition cursor-pointer">
                                + Añadir a Bodega
                            </button>
                            <button type="button" id="btn-pairing-plan-velada" class="px-3 py-1.5 bg-cream hover:bg-butter text-espresso border border-espresso/20 text-[11px] font-mono rounded transition cursor-pointer">
                                Planificar Velada →
                            </button>
                            <button type="button" id="btn-pairing-view-atlas" class="px-2.5 py-1.5 bg-transparent hover:bg-butter text-walnut hover:text-espresso border border-espresso/15 text-[11px] font-mono rounded transition cursor-pointer">
                                Ver en Atlas
                            </button>
                        </div>
                    </div>

                    <!-- Editorial Bottle Visual, Wine Hook & Radar (3-part responsive grid) -->
                    <div class="grid grid-cols-1 sm:grid-cols-12 gap-6 items-center">
                        <!-- Col 1: Editorial Bottle & Label Visual -->
                        <div class="sm:col-span-3 flex flex-col items-center justify-center">
                            <div id="res-bottle-visual" class="relative w-full max-w-[130px] flex flex-col items-center">
                                <img id="res-bottle-img" src="" alt="Botella de vino" class="hidden max-h-[220px] object-contain drop-shadow">
                                <div id="res-bottle-svg-container" class="w-full flex justify-center"></div>
                                <span id="res-bottle-badge" class="mt-2 text-[10px] font-mono px-2 py-0.5 rounded bg-butter border border-espresso/15 text-bordeaux font-medium text-center">
                                    Botella Bordelesa
                                </span>
                            </div>
                        </div>

                        <!-- Col 2: Wine Hook, Explanation & Tasting Notes Expansion -->
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

                        <!-- Col 3: 5D Radar Chart -->
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
                        <h4 class="font-serif italic text-lg text-walnut">Otras botellas recomendadas</h4>
                        <div id="res-alternatives" class="divide-y divide-espresso/10"></div>
                    </div>
                </section>
            </div>

            <!-- Full Searchable & Filterable Spanish D.O. Wine Catalog -->
            <section id="catalog-section" class="space-y-6">
                <div class="flex flex-wrap items-end justify-between gap-4 border-b border-espresso/15 pb-4">
                    <div class="space-y-1">
                        <div class="text-xs font-mono text-bordeaux uppercase tracking-wider">Catálogo Completo · __KPI_REGIONS_COUNT__ D.O.</div>
                        <h2 class="font-serif text-3xl text-espresso tracking-tight">Bodega Española de Referencia</h2>
                        <p class="font-serif italic text-sm text-walnut">
                            Explora, filtra por Denominación de Origen o estilo, y añade etiquetas directamente a tu bodega personal
                        </p>
                    </div>
                    <div class="flex items-center gap-3">
                        <span id="catalog-count-label" class="text-xs font-mono text-walnut tabular-nums">200 vinos</span>
                        <button type="button" id="btn-catalog-reset" class="hidden text-xs font-mono text-bordeaux underline underline-offset-4 cursor-pointer">
                            Limpiar filtros
                        </button>
                    </div>
                </div>

                <!-- Search & Filter Toolbar -->
                <div class="bg-butter/50 border border-espresso/12 rounded p-4 space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-12 gap-3">
                        <div class="md:col-span-4">
                            <label for="catalog-search-input" class="sr-only">Buscar vino o bodega</label>
                            <input id="catalog-search-input" type="search" placeholder="Buscar vino, bodega, país o nota de cata..." class="w-full bg-cream border border-espresso/20 rounded px-3 py-2 text-sm text-espresso placeholder:text-walnut/60 focus:border-bordeaux focus:ring-0">
                        </div>
                        <div class="md:col-span-2">
                            <label for="catalog-country-filter" class="sr-only">Filtrar por País</label>
                            <select id="catalog-country-filter" class="w-full bg-cream border border-espresso/20 rounded px-3 py-2 text-sm font-sans text-espresso focus:border-bordeaux focus:ring-0">
                                <option value="">Todos los países (__KPI_COUNTRIES_COUNT__)</option>
                                <option value="España">España</option>
                                <option value="Francia">Francia</option>
                                <option value="Italia">Italia</option>
                                <option value="Inglaterra">Inglaterra</option>
                            </select>
                        </div>
                        <div class="md:col-span-3">
                            <label for="catalog-do-filter" class="sr-only">Filtrar por Denominación de Origen</label>
                            <select id="catalog-do-filter" class="w-full bg-cream border border-espresso/20 rounded px-3 py-2 text-sm font-sans text-espresso focus:border-bordeaux focus:ring-0">
                                <option value="">Todas las Denominaciones (__KPI_REGIONS_COUNT__)</option>
                            </select>
                        </div>
                        <div class="md:col-span-3">
                            <label for="catalog-sort-select" class="sr-only">Ordenar catálogo</label>
                            <select id="catalog-sort-select" class="w-full bg-cream border border-espresso/20 rounded px-3 py-2 text-sm font-sans text-espresso focus:border-bordeaux focus:ring-0">
                                <option value="price-asc">Precio: menor a mayor</option>
                                <option value="price-desc">Precio: mayor a menor</option>
                                <option value="vintage-desc">Añada más reciente</option>
                                <option value="name-asc">Nombre (A-Z)</option>
                            </select>
                        </div>
                    </div>

                    <div id="catalog-type-filter" class="flex flex-wrap gap-2 text-xs font-mono">
                        <button type="button" data-type="" class="catalog-type-pill is-active px-3 py-1 rounded border border-espresso/15 cursor-pointer">Todos</button>
                        <button type="button" data-type="Red" class="catalog-type-pill px-3 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">Tinto</button>
                        <button type="button" data-type="White" class="catalog-type-pill px-3 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">Blanco</button>
                        <button type="button" data-type="Sparkling" class="catalog-type-pill px-3 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">Espumoso</button>
                        <button type="button" data-type="Rose" class="catalog-type-pill px-3 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">Rosado</button>
                        <button type="button" data-type="Fortified" class="catalog-type-pill px-3 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">Generoso</button>
                    </div>
                </div>

                <!-- Tasting Cards Grid -->
                <div id="catalog-wines-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"></div>
            </section>
        </section>

        <!-- ================================================================== -->
        <!-- TAB 3: DISEÑADOR DE VELADAS (#veladas)                             -->
        <!-- ================================================================== -->
        <section id="panel-veladas" role="tabpanel" aria-labelledby="tab-btn-veladas" class="tab-panel hidden space-y-8">
            <div id="evening-planner-section" class="space-y-8">
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
                        <div class="space-y-2">
                            <label for="plan-starter-select" class="block text-xs font-mono text-walnut uppercase tracking-wide">
                                1.º Pase · Entrante / Aperitivo
                            </label>
                            <select id="plan-starter-select" class="w-full bg-cream border border-espresso/20 rounded p-2.5 text-sm font-serif text-espresso focus:border-bordeaux focus:ring-0"></select>
                        </div>

                        <div class="space-y-2">
                            <label for="plan-main-select" class="block text-xs font-mono text-walnut uppercase tracking-wide">
                                2.º Pase · Plato Principal
                            </label>
                            <select id="plan-main-select" class="w-full bg-cream border border-espresso/20 rounded p-2.5 text-sm font-serif text-espresso focus:border-bordeaux focus:ring-0"></select>
                        </div>

                        <div class="space-y-2">
                            <label for="plan-dessert-select" class="block text-xs font-mono text-walnut uppercase tracking-wide">
                                3.º Pase · Quesos o Postre
                            </label>
                            <select id="plan-dessert-select" class="w-full bg-cream border border-espresso/20 rounded p-2.5 text-sm font-serif text-espresso focus:border-bordeaux focus:ring-0"></select>
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

                <!-- Paso 3: Progresión de los 3 Vinos & Curva Sensorial (#menu-plan-results) -->
                <div id="menu-plan-results" class="space-y-8">
                    <!-- Summary Bar -->
                    <div class="bg-butter/70 border border-espresso/15 rounded p-5 space-y-3 no-print">
                        <div class="flex flex-wrap items-baseline justify-between gap-4 border-b border-espresso/10 pb-3">
                            <div class="flex flex-wrap items-center gap-3">
                                <span class="text-xs font-mono text-bordeaux uppercase tracking-wider font-semibold">Balance de Velada</span>
                                <span class="h-3 w-px bg-espresso/20"></span>
                                <span id="plan-ambience-tip" class="text-xs font-serif italic text-walnut">
                                    Ambiente sugerido: Iluminación cálida y música suave.
                                </span>
                            </div>
                            <div class="flex flex-wrap items-center gap-4 text-xs font-mono">
                                <span>Inversión total: <strong id="plan-total-price" class="text-sm text-espresso font-semibold tabular-nums">85.00 €</strong></span>
                                <span class="text-sage">Afinidad media: <strong id="plan-avg-score" class="text-sm font-semibold tabular-nums">95.4%</strong></span>
                                <button type="button" id="btn-add-trio-cellar" class="px-3 py-1 bg-bordeaux text-cream text-[11px] rounded hover:bg-bordeaux/90 transition cursor-pointer">
                                    + Añadir 3 botellas a Bodega
                                </button>
                            </div>
                        </div>
                        <p id="plan-progression-summary" class="text-xs sm:text-sm text-espresso/90 leading-relaxed font-sans">
                            Cargando progresión sommelier...
                        </p>
                    </div>

                    <!-- Sensory Progression Curve Panel -->
                    <div id="progression-chart-panel" class="bg-cream border border-espresso/15 rounded p-5 space-y-3 no-print">
                        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-espresso/10 pb-2">
                            <div>
                                <h3 class="font-serif text-xl text-espresso">Curva de Progresión Sensorial en Tres Tiempos</h3>
                                <p class="text-xs text-walnut">Evolución equilibrada de cuerpo, acidez, estructura tánica y crianza del 1.º al 3.º pase</p>
                            </div>
                            <span id="plan-progression-badge" class="text-[11px] font-mono px-2.5 py-1 rounded bg-sage/15 text-sage border border-sage/30">
                                Progresión Validada
                            </span>
                        </div>
                        <div class="relative w-full h-[220px]">
                            <canvas id="progressionChart"></canvas>
                        </div>
                    </div>

                    <!-- 3 Courses Grid (#plan-courses-grid) -->
                    <div id="plan-courses-grid" class="grid grid-cols-1 md:grid-cols-3 gap-6 no-print"></div>

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

                        <div id="print-courses-list" class="space-y-6 divide-y divide-espresso/10"></div>

                        <div class="text-center pt-6 border-t border-espresso/15 text-xs font-serif italic text-walnut space-y-1">
                            <p>Vinum Pulse · Caviste &amp; Table · Bodega y Gastronomía Española</p>
                            <p class="text-[10px] font-mono text-walnut/70 uppercase tracking-widest">Salud y buen provecho</p>
                        </div>

                        <div class="text-center pt-2 no-print">
                            <button type="button" id="btn-print-menu" onclick="window.print()" class="inline-flex items-center gap-2 py-2.5 px-6 bg-bordeaux text-cream text-xs font-mono uppercase tracking-wider rounded hover:bg-bordeaux/90 transition shadow-sm cursor-pointer">
                                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                    <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                                    <rect x="6" y="14" width="12" height="8"></rect>
                                </svg>
                                Imprimir Carta para Invitados
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================================================================== -->
        <!-- TAB 4: MI BODEGA (#bodega)                                         -->
        <!-- ================================================================== -->
        <section id="panel-bodega" role="tabpanel" aria-labelledby="tab-btn-bodega" class="tab-panel hidden space-y-8 no-print">
            <div class="flex flex-wrap items-end justify-between gap-4 border-b border-espresso/15 pb-4">
                <div class="space-y-1">
                    <div class="text-xs font-mono text-bordeaux uppercase tracking-wider">Inventario SQLite &amp; Ventanas de Guarda</div>
                    <h2 class="font-serif text-3xl sm:text-4xl text-espresso tracking-tight">
                        Mi Bodega Personal &amp; Analítica de Madurez
                    </h2>
                    <p class="font-serif italic text-base text-walnut">
                        Gestiona tus botellas reales, controla la valoración de tu cava y detecta añadas en su momento óptimo de descorche
                    </p>
                </div>
            </div>

            <!-- Cellar Analytics KPI Bento Strip -->
            <div id="cellar-analytics-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-butter/60 border border-espresso/12 rounded p-4 space-y-1">
                    <div class="text-[11px] font-mono text-walnut uppercase tracking-wider">Stock en Cava</div>
                    <div class="flex items-baseline gap-2">
                        <span id="cellar-kpi-bottles" class="font-serif text-3xl text-espresso tabular-nums">0</span>
                        <span class="text-xs font-mono text-walnut">botellas</span>
                    </div>
                    <div id="cellar-kpi-refs" class="text-xs font-mono text-bordeaux tabular-nums">0 etiquetas distintas</div>
                </div>

                <div class="bg-butter/60 border border-espresso/12 rounded p-4 space-y-1">
                    <div class="text-[11px] font-mono text-walnut uppercase tracking-wider">Valoración Total</div>
                    <div id="cellar-kpi-valuation" class="font-serif text-3xl text-espresso tabular-nums">0.00 €</div>
                    <div id="cellar-kpi-avg-price" class="text-xs font-mono text-walnut tabular-nums">Media: 0.00 € / bot.</div>
                </div>

                <div class="bg-butter/60 border border-espresso/12 rounded p-4 space-y-1">
                    <div class="text-[11px] font-mono text-walnut uppercase tracking-wider">Diversificación D.O.</div>
                    <div class="flex items-baseline gap-2">
                        <span id="cellar-kpi-regions" class="font-serif text-3xl text-espresso tabular-nums">0</span>
                        <span class="text-xs font-mono text-walnut">regiones</span>
                    </div>
                    <div id="cellar-style-breakdown" class="text-xs font-mono text-walnut truncate">Sin estilos registrados</div>
                </div>

                <div class="bg-butter/60 border border-espresso/12 rounded p-4 space-y-1">
                    <div class="text-[11px] font-mono text-walnut uppercase tracking-wider">Ventana de Consumo</div>
                    <div id="cellar-kpi-peak" class="font-serif text-3xl text-sage tabular-nums">0 listas</div>
                    <div id="cellar-kpi-peak-detail" class="text-xs font-mono text-walnut">0 prioritarias · 0 en guarda</div>
                </div>
            </div>

            <!-- Asymmetric Cellar Workspace: Add Form (4 cols) + Inventory (8 cols) -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                <!-- Left: Add Bottle Form -->
                <form id="cellar-add-form" class="lg:col-span-4 bg-butter/50 border border-espresso/15 rounded p-6 space-y-4">
                    <div class="border-b border-espresso/12 pb-3">
                        <h3 class="font-serif text-2xl text-espresso">Registrar Nueva Botella</h3>
                        <p class="text-xs text-walnut">Añade existencias a la persistencia SQLite de tu cava</p>
                    </div>

                    <div class="space-y-1.5">
                        <label for="cellar-wine-select" class="block text-xs font-mono text-walnut uppercase">Vino del Catálogo</label>
                        <select id="cellar-wine-select" required class="w-full bg-cream border border-espresso/20 rounded p-2.5 text-sm font-sans text-espresso focus:border-bordeaux focus:ring-0"></select>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <div class="space-y-1.5">
                            <label for="cellar-qty-input" class="block text-xs font-mono text-walnut uppercase">Cantidad</label>
                            <input id="cellar-qty-input" type="number" min="1" max="240" value="1" required class="w-full bg-cream border border-espresso/20 rounded p-2 text-sm font-mono text-espresso tabular-nums focus:border-bordeaux focus:ring-0">
                        </div>
                        <div class="space-y-1.5">
                            <label for="cellar-price-input" class="block text-xs font-mono text-walnut uppercase">Precio (€)</label>
                            <input id="cellar-price-input" type="number" min="0" step="0.5" value="25.00" class="w-full bg-cream border border-espresso/20 rounded p-2 text-sm font-mono text-espresso tabular-nums focus:border-bordeaux focus:ring-0">
                        </div>
                    </div>

                    <div class="space-y-1.5">
                        <label for="cellar-location-input" class="block text-xs font-mono text-walnut uppercase">Ubicación en Cava</label>
                        <input id="cellar-location-input" type="text" list="cellar-location-suggestions" value="Bodega Principal" class="w-full bg-cream border border-espresso/20 rounded p-2 text-sm text-espresso focus:border-bordeaux focus:ring-0">
                        <datalist id="cellar-location-suggestions">
                            <option value="Bodega Principal"></option>
                            <option value="Armario Climatizado Balda 1"></option>
                            <option value="Armario Climatizado Balda 2"></option>
                            <option value="Botellero Salón"></option>
                            <option value="Cava Subterránea"></option>
                        </datalist>
                    </div>

                    <div class="space-y-1.5">
                        <label for="cellar-notes-input" class="block text-xs font-mono text-walnut uppercase">Notas de Guarda / Ocasión</label>
                        <textarea id="cellar-notes-input" rows="2" placeholder="Ej. Regalo aniversario, descorchar en invierno..." class="w-full bg-cream border border-espresso/20 rounded p-2 text-sm text-espresso placeholder:text-walnut/50 focus:border-bordeaux focus:ring-0"></textarea>
                    </div>

                    <button type="submit" id="btn-cellar-add" class="w-full py-2.5 px-4 bg-bordeaux text-cream text-xs font-mono uppercase tracking-wider rounded hover:bg-bordeaux/90 transition shadow-xs cursor-pointer">
                        Guardar en Mi Bodega
                    </button>
                </form>

                <!-- Right: Inventory List & Window Filters -->
                <div id="cellar-inventory-panel" class="lg:col-span-8 space-y-4">
                    <div class="flex flex-wrap items-center justify-between gap-3 bg-butter/40 border border-espresso/12 rounded p-3">
                        <input id="cellar-search-input" type="search" placeholder="Filtrar mi bodega por vino, D.O. o balda..." class="flex-1 min-w-[200px] bg-cream border border-espresso/20 rounded px-3 py-1.5 text-xs text-espresso focus:border-bordeaux focus:ring-0">
                        <div id="cellar-window-filter" class="flex flex-wrap gap-1.5 text-[11px] font-mono">
                            <button type="button" data-window="all" class="cellar-filter-btn is-active px-2.5 py-1 rounded border border-espresso/15 cursor-pointer">Todas</button>
                            <button type="button" data-window="ready" class="cellar-filter-btn px-2.5 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">En Cumbre</button>
                            <button type="button" data-window="priority" class="cellar-filter-btn px-2.5 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">Prioritario</button>
                            <button type="button" data-window="aging" class="cellar-filter-btn px-2.5 py-1 rounded border border-espresso/15 bg-cream text-walnut hover:text-espresso cursor-pointer">Guarda</button>
                        </div>
                    </div>

                    <div id="cellar-inventory-list" class="space-y-3"></div>
                </div>
            </div>
        </section>
    </main>

    <!-- Non-intrusive Toast Notification Container -->
    <div id="toast-container" aria-live="polite" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-[calc(100%-2.5rem)] pointer-events-none no-print"></div>

    <footer class="max-w-6xl w-full mx-auto px-4 sm:px-8 pb-8 pt-4 border-t border-espresso/10 text-center text-xs font-serif italic text-walnut no-print">
        Vinum Pulse · Atlas Cartográfico de Terroirs · Radar de Cata 5D · Diseñador de Veladas &amp; Bodega SQLite
    </footer>

    <script>
        const VALID_TABS = ["atlas", "carte", "veladas", "bodega"];
        let activeTab = "atlas";

        let allDishes = [];
        let allWines = [];
        let allRegions = [];
        let cellarItems = [];
        let atlasFeatures = [];

        let selectedDishId = "chuleton-brasa";
        let selectedCountry = "";
        let selectedDo = "";
        let activeAtlasLayer = "wineries";
        let activeAtlasFeature = null;
        let preferredType = null;
        let currentPairingRec = null;

        const EUROPE_DEFAULT_VIEW = { center: [45.5, 2.5], zoom: 4.5 };
        const COUNTRY_BOUNDS = {
            "": [[36.0, -9.5], [52.0, 18.5]],
            "España": [[36.0, -9.5], [43.5, 3.2]],
            "Francia": [[42.3, -2.5], [50.2, 8.2]],
            "Italia": [[36.6, 7.0], [47.0, 18.5]],
            "Inglaterra": [[50.4, -2.2], [51.8, 1.8]]
        };

        let radarChartInstance = null;
        let radarChart = null; // Atlas 5D Sensory Comparison Radar
        let progressionChart = null; // Veladas 3-Course Progression Curve

        let leafletMap = null;
        let atlasMap = null; // Alias for lifecycle invalidation
        let activeTileLayer = null;
        let activeBasemapId = "osm-editorial";
        let consecutiveTileErrors = 0;
        const MAX_CONSECUTIVE_TILE_ERRORS = 4;
        let mapMarkers = [];
        let atlasNeedsInitialCenter = false;

        const BASEMAP_PROVIDERS = {
            "osm-editorial": {
                url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                options: {
                    maxZoom: 18,
                    className: "vinum-editorial-tiles",
                    attribution: "&copy; OpenStreetMap contributors"
                },
                label: "Cartografía: OpenStreetMap Editorial (Zero-Key Open Source)",
                nextFallback: "ign-espana"
            },
            "ign-espana": {
                url: "https://www.ign.es/wmts/ign-base?layer=IGNBaseTodo&style=default&tilematrixset=GoogleMapsCompatible&Service=WMTS&Request=GetTile&Version=1.0.0&Format=image/jpeg&TileMatrix={z}&TileCol={x}&TileRow={y}",
                options: {
                    maxZoom: 18,
                    attribution: "&copy; Instituto Geográfico Nacional de España (CC-BY 4.0)"
                },
                label: "Cartografía: IGN España (CC-BY 4.0 Open Source)",
                nextFallback: "svg-offline"
            }
        };

        let expandedCategory = null;
        let selectedOccasion = "Cena Romántica";
        let catalogSearchQuery = "";
        let catalogCountryFilter = "";
        let catalogDoFilter = "";
        let catalogTypeFilter = "";
        let catalogSortOrder = "price-asc";
        let highlightedCatalogWineId = "";
        let cellarSearchQuery = "";
        let cellarWindowFilter = "all";

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

        function escapeHtml(value) {
            if (value === null || value === undefined) return "";
            return String(value)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#39;");
        }

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

        /* --- 4-Tab SPA Navigation & URL Hash Deep Linking --- */

        function resolveTabFromHash(hashValue) {
            const cleaned = (hashValue || "").replace(/^#/, "").trim().toLowerCase();
            return VALID_TABS.includes(cleaned) ? cleaned : "atlas";
        }

        function switchTab(tabId, updateHash = true) {
            const targetTab = VALID_TABS.includes(tabId) ? tabId : "atlas";
            activeTab = targetTab;

            document.querySelectorAll('#workspace-tablist [role="tab"]').forEach(btn => {
                const isTarget = btn.getAttribute("data-tab") === targetTab;
                btn.setAttribute("aria-selected", isTarget ? "true" : "false");
                btn.setAttribute("tabindex", isTarget ? "0" : "-1");
                btn.classList.toggle("is-active", isTarget);
                btn.classList.toggle("text-walnut", !isTarget);
            });

            VALID_TABS.forEach(id => {
                const panel = document.getElementById(`panel-${id}`);
                if (panel) {
                    panel.classList.toggle("hidden", id !== targetTab);
                }
            });

            if (updateHash) {
                const desiredHash = `#${targetTab}`;
                if (window.location.hash !== desiredHash) {
                    window.location.hash = desiredHash;
                }
            }

            if (targetTab === "atlas") {
                setTimeout(() => {
                    if (atlasMap) {
                        atlasMap.invalidateSize();
                        if (atlasNeedsInitialCenter) {
                            atlasMap.setView(EUROPE_DEFAULT_VIEW.center, EUROPE_DEFAULT_VIEW.zoom, { animate: false });
                            atlasNeedsInitialCenter = false;
                        }
                    }
                    if (radarChart) radarChart.resize();
                }, 60);
            } else if (targetTab === "carte") {
                setTimeout(() => {
                    if (radarChartInstance) radarChartInstance.resize();
                }, 60);
            } else if (targetTab === "veladas") {
                setTimeout(() => {
                    if (progressionChart) progressionChart.resize();
                }, 60);
            }
        }

        function setupTabKeyboardNavigation() {
            const tablist = document.getElementById("workspace-tablist");
            if (!tablist) return;
            tablist.querySelectorAll('[role="tab"]').forEach((tab, idx, tabs) => {
                tab.addEventListener("click", () => {
                    switchTab(tab.getAttribute("data-tab"), true);
                });
                tab.addEventListener("keydown", (e) => {
                    let nextIdx = idx;
                    if (e.key === "ArrowRight") nextIdx = (idx + 1) % tabs.length;
                    else if (e.key === "ArrowLeft") nextIdx = (idx - 1 + tabs.length) % tabs.length;
                    else if (e.key === "Home") nextIdx = 0;
                    else if (e.key === "End") nextIdx = tabs.length - 1;
                    else return;
                    e.preventDefault();
                    const nextTab = tabs[nextIdx];
                    nextTab.focus();
                    switchTab(nextTab.getAttribute("data-tab"), true);
                });
            });
        }

        /* --- Non-intrusive Toast Notification System --- */

        function showToast(message, options = {}) {
            const container = document.getElementById("toast-container");
            if (!container) return;

            const toast = document.createElement("div");
            const variant = options.variant || "success";
            const accentClass = variant === "warning" ? "border-brass bg-[#FAF6EE]" : "border-bordeaux/35 bg-[#FAF6EE]";
            const dotColor = variant === "warning" ? "bg-brass" : "bg-bordeaux";

            toast.className = `toast-item pointer-events-auto border ${accentClass} rounded shadow-md px-4 py-3 flex items-start justify-between gap-3 text-xs text-espresso`;

            const bodyWrap = document.createElement("div");
            bodyWrap.className = "flex items-start gap-2.5 flex-1";

            const dot = document.createElement("span");
            dot.className = `mt-1 w-2 h-2 rounded-full ${dotColor} shrink-0`;
            bodyWrap.appendChild(dot);

            const textCol = document.createElement("div");
            textCol.className = "space-y-1";

            const msgEl = document.createElement("p");
            msgEl.className = "font-sans text-xs text-espresso leading-snug";
            msgEl.textContent = message;
            textCol.appendChild(msgEl);

            if (options.actionLabel && typeof options.onAction === "function") {
                const actionBtn = document.createElement("button");
                actionBtn.type = "button";
                actionBtn.className = "font-mono text-[11px] text-bordeaux underline underline-offset-4 hover:text-espresso cursor-pointer";
                actionBtn.textContent = options.actionLabel;
                actionBtn.addEventListener("click", () => {
                    options.onAction();
                    toast.remove();
                });
                textCol.appendChild(actionBtn);
            }

            bodyWrap.appendChild(textCol);
            toast.appendChild(bodyWrap);

            const closeBtn = document.createElement("button");
            closeBtn.type = "button";
            closeBtn.setAttribute("aria-label", "Cerrar notificación");
            closeBtn.className = "text-walnut hover:text-espresso font-mono text-xs px-1 cursor-pointer";
            closeBtn.innerHTML = "&times;";
            closeBtn.addEventListener("click", () => toast.remove());
            toast.appendChild(closeBtn);

            container.appendChild(toast);

            setTimeout(() => {
                if (toast.isConnected) toast.remove();
            }, options.durationMs || 4200);
        }

        /* --- Initialization --- */

        async function init() {
            setupTabKeyboardNavigation();
            window.addEventListener("hashchange", () => {
                switchTab(resolveTabFromHash(window.location.hash), false);
            });

            const initialTab = resolveTabFromHash(window.location.hash);
            switchTab(initialTab, false);

            try {
                const [resDishes, resWines, resRegions] = await Promise.all([
                    fetch("/api/v1/dishes"),
                    fetch("/api/v1/wines?limit=250"),
                    fetch("/api/v1/regions")
                ]);
                allDishes = await resDishes.json();
                allWines = await resWines.json();
                allRegions = await resRegions.json();

                updateCatalogGlobalKpis();
                populateAtlasDishSelect();
                populateCatalogFilters();
                renderWineCatalog();

                renderActiveDishChip();
                renderDishes();
                setupEventListeners();
                fetchRecommendation();

                populatePlannerSelects();
                generateMenuPlan();

                populateCellarWineSelect();
                await loadCellar();
                await initAtlas();
            } catch (err) {
                showError("No se pudo inicializar la aplicación.");
                console.error("Error al inicializar:", err);
            }
        }

        function updateCatalogGlobalKpis() {
            const winesEl = document.getElementById("kpi-wines-count");
            const regionsEl = document.getElementById("kpi-regions-count");
            const badgeEl = document.getElementById("atlas-status-badge");
            if (winesEl) winesEl.textContent = `${allWines.length} Vinos`;
            if (regionsEl) regionsEl.textContent = `${allRegions.length} D.O.`;
            if (badgeEl && !atlasCountryFilter) {
                badgeEl.textContent = `${allRegions.length} Regiones · ${allWines.length} Bodegas`;
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

        /* --- La Carte & Pairing Engine --- */

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
                        <button type="button" class="carte-section-header w-full flex items-center justify-between py-2.5 px-3 bg-butter/40 hover:bg-butter/80 transition text-left cursor-pointer" data-category="${escapeHtml(catName)}">
                            <div class="flex items-center gap-2">
                                <span class="font-serif text-base text-espresso">${escapeHtml(catName)}</span>
                                <span class="text-[10px] font-mono text-walnut tabular-nums">(${dishes.length})</span>
                            </div>
                            <span class="text-xs font-mono text-bordeaux transform transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}">▾</span>
                        </button>
                        <div class="carte-section-body ${isExpanded ? 'block' : 'hidden'} divide-y divide-espresso/10 border-t border-espresso/10 bg-cream">
                            ${dishes.map(dish => {
                                const isActive = dish.id === selectedDishId;
                                return `
                                    <button type="button" data-dish-id="${escapeHtml(dish.id)}" class="dish-row w-full text-left py-2.5 px-3 rounded-none cursor-pointer ${isActive ? 'is-active bg-butter/80' : 'hover:bg-butter/40'}">
                                        <div class="flex items-baseline justify-between gap-2">
                                            <span class="font-serif text-lg ${isActive ? 'text-bordeaux font-medium' : 'text-espresso'}">${escapeHtml(dish.name)}</span>
                                            <span class="text-[10px] font-mono text-walnut shrink-0">${escapeHtml(dish.suggested_wine_type || '')}</span>
                                        </div>
                                        <p class="text-xs text-walnut line-clamp-1 mt-0.5">${escapeHtml(dish.description)}</p>
                                    </button>
                                `;
                            }).join("")}
                        </div>
                    </div>
                `;
            }).join("");

            grid.querySelectorAll(".carte-section-header").forEach(header => {
                header.addEventListener("click", () => {
                    const cat = header.getAttribute("data-category");
                    expandedCategory = (expandedCategory === cat) ? null : cat;
                    renderDishes();
                });
            });

            grid.querySelectorAll(".dish-row").forEach(el => {
                el.addEventListener("click", () => {
                    selectedDishId = el.getAttribute("data-dish-id");
                    expandedCategory = null;
                    renderActiveDishChip();
                    renderDishes();
                    fetchRecommendation();
                    const atlasDishSel = document.getElementById("atlas-radar-dish-select");
                    if (atlasDishSel) {
                        atlasDishSel.value = selectedDishId;
                        if (activeAtlasFeature) updateAtlasRadar(activeAtlasFeature);
                    }
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
            slider.addEventListener("change", () => fetchRecommendation());

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

            document.getElementById("btn-expand-carte")?.addEventListener("click", () => {
                const cur = allDishes.find(d => d.id === selectedDishId);
                const cat = getCategoryForDish(cur);
                expandedCategory = (expandedCategory === cat) ? null : cat;
                renderDishes();
            });

            document.getElementById("btn-toggle-tasting-notes")?.addEventListener("click", toggleTastingNotes);

            // Atlas layer toggles
            document.querySelectorAll(".atlas-layer-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    const layer = btn.getAttribute("data-layer") || "wineries";
                    if (layer === activeAtlasLayer) return;
                    activeAtlasLayer = layer;
                    document.querySelectorAll(".atlas-layer-btn").forEach(b => {
                        b.classList.toggle("is-active", b === btn);
                        b.classList.toggle("text-walnut", b !== btn);
                    });
                    loadAtlasLayer(layer);
                });
            });

            // Atlas zero-key basemap provider switcher
            document.querySelectorAll(".atlas-basemap-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    const providerId = btn.getAttribute("data-basemap") || "osm-editorial";
                    switchBasemapProvider(providerId);
                });
            });

            // Atlas radar sync & dish comparison selector
            document.getElementById("btn-sync-radar")?.addEventListener("click", () => {
                if (activeAtlasFeature) {
                    updateAtlasRadar(activeAtlasFeature);
                    document.getElementById("atlas-radar-panel")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
                    showToast(`Perfil 5D de ${activeAtlasFeature.properties.name} proyectado en el Radar`);
                }
            });

            document.getElementById("atlas-radar-dish-select")?.addEventListener("change", () => {
                if (activeAtlasFeature) updateAtlasRadar(activeAtlasFeature);
            });

            // Contextual Bridges: Atlas -> La Carte / Mi Bodega
            document.getElementById("btn-atlas-to-carte")?.addEventListener("click", () => {
                if (activeAtlasFeature) bridgeAtlasToCarte(activeAtlasFeature);
            });

            document.getElementById("btn-atlas-to-bodega")?.addEventListener("click", () => {
                if (activeAtlasFeature) bridgeAtlasToBodega(activeAtlasFeature);
            });

            // Contextual Bridges: Pairing Result -> Mi Bodega / Veladas / Atlas
            document.getElementById("btn-pairing-add-cellar")?.addEventListener("click", () => {
                if (currentPairingRec && currentPairingRec.primary_wine) {
                    quickAddWineToCellar(currentPairingRec.primary_wine.id, "La Carte");
                }
            });

            document.getElementById("btn-pairing-plan-velada")?.addEventListener("click", () => {
                bridgePairingToVeladas();
            });

            document.getElementById("btn-pairing-view-atlas")?.addEventListener("click", () => {
                if (currentPairingRec && currentPairingRec.primary_wine) {
                    bridgeWineToAtlas(currentPairingRec.primary_wine.id);
                }
            });

            // Country Quick-Select Pills (European Atlas)
            document.querySelectorAll(".country-pill").forEach(btn => {
                btn.addEventListener("click", () => {
                    const country = btn.getAttribute("data-country") || "";
                    filterAtlasByCountry(country, btn);
                });
            });

            // Wine Catalog Search & Filters
            document.getElementById("catalog-search-input")?.addEventListener("input", (e) => {
                catalogSearchQuery = e.target.value.trim();
                renderWineCatalog();
            });
            document.getElementById("catalog-country-filter")?.addEventListener("change", (e) => {
                catalogCountryFilter = e.target.value;
                catalogDoFilter = "";
                populateCatalogFilters();
                renderWineCatalog();
            });
            document.getElementById("catalog-do-filter")?.addEventListener("change", (e) => {
                catalogDoFilter = e.target.value;
                renderWineCatalog();
            });
            document.getElementById("catalog-sort-select")?.addEventListener("change", (e) => {
                catalogSortOrder = e.target.value;
                renderWineCatalog();
            });
            document.querySelectorAll(".catalog-type-pill").forEach(btn => {
                btn.addEventListener("click", () => {
                    catalogTypeFilter = btn.getAttribute("data-type") || "";
                    document.querySelectorAll(".catalog-type-pill").forEach(b => {
                        const isMatch = b === btn;
                        b.classList.toggle("is-active", isMatch);
                        b.classList.toggle("bg-cream", !isMatch);
                        b.classList.toggle("text-walnut", !isMatch);
                    });
                    renderWineCatalog();
                });
            });
            document.getElementById("btn-catalog-reset")?.addEventListener("click", () => {
                resetCatalogFilters();
            });

            // Evening Planner listeners
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

            const planSlider = document.getElementById("plan-budget-slider");
            const planValLabel = document.getElementById("plan-budget-value");
            if (planSlider && planValLabel) {
                planSlider.addEventListener("input", (e) => {
                    planValLabel.textContent = `${e.target.value} €`;
                });
                planSlider.addEventListener("change", () => generateMenuPlan());
            }

            ["plan-starter-select", "plan-main-select", "plan-dessert-select"].forEach(id => {
                document.getElementById(id)?.addEventListener("change", () => generateMenuPlan());
            });

            document.getElementById("btn-generate-menu-plan")?.addEventListener("click", () => generateMenuPlan());

            document.getElementById("btn-add-trio-cellar")?.addEventListener("click", async () => {
                await addCurrentMenuTrioToCellar();
            });

            // Cellar Form & Filter listeners
            document.getElementById("cellar-wine-select")?.addEventListener("change", (e) => {
                const w = allWines.find(x => x.id === e.target.value);
                if (w) {
                    const priceInput = document.getElementById("cellar-price-input");
                    if (priceInput) priceInput.value = w.price_eur.toFixed(2);
                }
            });

            document.getElementById("cellar-add-form")?.addEventListener("submit", async (e) => {
                e.preventDefault();
                await handleCellarFormSubmit();
            });

            document.getElementById("cellar-search-input")?.addEventListener("input", (e) => {
                cellarSearchQuery = e.target.value.trim().toLowerCase();
                renderCellar();
            });

            document.querySelectorAll(".cellar-filter-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    cellarWindowFilter = btn.getAttribute("data-window") || "all";
                    document.querySelectorAll(".cellar-filter-btn").forEach(b => {
                        const isMatch = b === btn;
                        b.classList.toggle("is-active", isMatch);
                        b.classList.toggle("bg-cream", !isMatch);
                        b.classList.toggle("text-walnut", !isMatch);
                    });
                    renderCellar();
                });
            });
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
                currentPairingRec = data;
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
            const appText = escapeHtml(rawApp.length > 14 ? rawApp.substring(0, 12) + "…" : rawApp);

            const wineWords = (wine.name || "").split(" ");
            let line1 = wine.name || "";
            let line2 = "";
            if (wineWords.length > 2) {
                line1 = wineWords.slice(0, 2).join(" ");
                line2 = wineWords.slice(2, 5).join(" ");
            }
            if (line1.length > 13) line1 = line1.substring(0, 11) + "…";
            if (line2.length > 13) line2 = line2.substring(0, 11) + "…";

            const wineryRaw = wine.winery || "";
            const wineryText = escapeHtml(wineryRaw.length > 14 ? wineryRaw.substring(0, 12) + "…" : wineryRaw);

            container.innerHTML = `
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

                        <text x="${labelWidth / 2}" y="20" text-anchor="middle" font-family="'Instrument Serif', Georgia, serif" font-size="5.2" fill="#231B16" font-weight="bold">${escapeHtml(line1)}</text>
                        ${line2 ? `<text x="${labelWidth / 2}" y="26" text-anchor="middle" font-family="'Instrument Serif', Georgia, serif" font-size="4.6" fill="#231B16">${escapeHtml(line2)}</text>` : ''}

                        <text x="${labelWidth / 2}" y="${line2 ? 34 : 30}" text-anchor="middle" font-family="'Instrument Serif', Georgia, serif" font-size="3.8" font-style="italic" fill="#6A5A4F">${wineryText}</text>

                        <text x="${labelWidth / 2}" y="${labelHeight - 12}" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="3.6" fill="#231B16" font-weight="500">AÑADA ${escapeHtml(wine.vintage)}</text>
                        <text x="${labelWidth / 2}" y="${labelHeight - 4}" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="2.6" fill="#9C6F38" letter-spacing="0.2">${escapeHtml(silhouette.toUpperCase())}</text>
                    </g>
                </svg>
            `;
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
                    <div class="py-2.5 flex flex-wrap justify-between items-center gap-3 text-sm">
                        <div>
                            <span class="font-serif text-lg text-espresso">${escapeHtml(alt.name)}</span>
                            <span class="text-xs text-walnut ml-2">${escapeHtml(alt.appellation)}</span>
                        </div>
                        <div class="flex items-center gap-3 shrink-0">
                            <span class="font-mono text-xs text-espresso tabular-nums">${alt.price_eur.toFixed(2)} €</span>
                            <button type="button" data-alt-wine-id="${escapeHtml(alt.id)}" class="btn-alt-add-cellar px-2 py-1 text-[10px] font-mono rounded border border-bordeaux/30 text-bordeaux hover:bg-bordeaux hover:text-cream transition cursor-pointer">
                                + Bodega
                            </button>
                        </div>
                    </div>
                `).join("");
                altGrid.querySelectorAll(".btn-alt-add-cellar").forEach(btn => {
                    btn.addEventListener("click", () => {
                        const wid = btn.getAttribute("data-alt-wine-id");
                        if (wid) quickAddWineToCellar(wid, "La Carte");
                    });
                });
            } else {
                altGrid.innerHTML = `<p class="py-2 text-xs text-walnut italic">Sin alternativas adicionales bajo este presupuesto.</p>`;
            }

            renderRadarChart(rec.target_sensory, wine.sensory);
        }

        function buildRadarConfig(target, wineSensory, wineLabel, targetLabel) {
            const labels = ['Cuerpo', 'Acidez', 'Taninos', 'Fruta', 'Madera'];
            const targetData = [target.body, target.acidity, target.tannins, target.fruit, target.oak];
            const wineData = [wineSensory.body, wineSensory.acidity, wineSensory.tannins, wineSensory.fruit, wineSensory.oak];

            return {
                type: 'radar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: wineLabel,
                            data: wineData,
                            backgroundColor: 'rgba(107, 29, 40, 0.14)',
                            borderColor: '#6B1D28',
                            pointBackgroundColor: '#6B1D28',
                            pointBorderColor: '#F7F2E8',
                            borderWidth: 2
                        },
                        {
                            label: targetLabel,
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
            };
        }

        function renderRadarChart(target, wineSensory) {
            const canvas = document.getElementById('radarChart');
            if (!canvas || typeof Chart === "undefined") return;
            const ctx = canvas.getContext('2d');
            if (radarChartInstance) radarChartInstance.destroy();
            radarChartInstance = new Chart(ctx, buildRadarConfig(target, wineSensory, 'Vino Seleccionado', 'Demanda del Plato'));
        }

        /* --- Full Searchable & Filterable Spanish D.O. Wine Catalog (Tab 2) --- */

        function populateCatalogFilters() {
            const select = document.getElementById("catalog-do-filter");
            if (!select) return;
            const pool = catalogCountryFilter
                ? allWines.filter(w => w.country === catalogCountryFilter)
                : allWines;
            const dos = [...new Set(pool.map(w => w.appellation))].sort();
            select.innerHTML = `<option value="">Todas las Denominaciones (${dos.length})</option>` +
                dos.map(d => `<option value="${escapeHtml(d)}">${escapeHtml(d)}</option>`).join("");
            select.value = catalogDoFilter;
        }

        function resetCatalogFilters() {
            catalogSearchQuery = "";
            catalogCountryFilter = "";
            catalogDoFilter = "";
            catalogTypeFilter = "";
            highlightedCatalogWineId = "";
            const searchEl = document.getElementById("catalog-search-input");
            const countryEl = document.getElementById("catalog-country-filter");
            const doEl = document.getElementById("catalog-do-filter");
            if (searchEl) searchEl.value = "";
            if (countryEl) countryEl.value = "";
            populateCatalogFilters();
            if (doEl) doEl.value = "";
            document.querySelectorAll(".catalog-type-pill").forEach(b => {
                const isAll = b.getAttribute("data-type") === "";
                b.classList.toggle("is-active", isAll);
                b.classList.toggle("bg-cream", !isAll);
                b.classList.toggle("text-walnut", !isAll);
            });
            renderWineCatalog();
        }

        function translateWineType(t) {
            const map = { Red: "Tinto", White: "Blanco", Sparkling: "Espumoso", Fortified: "Generoso", Rose: "Rosado" };
            return map[t] || t;
        }

        function renderWineCatalog() {
            const grid = document.getElementById("catalog-wines-grid");
            const countEl = document.getElementById("catalog-count-label");
            const resetBtn = document.getElementById("btn-catalog-reset");
            if (!grid) return;

            const q = catalogSearchQuery.toLowerCase();
            let filtered = allWines.filter(w => {
                if (catalogCountryFilter && w.country !== catalogCountryFilter) return false;
                if (catalogDoFilter && w.appellation !== catalogDoFilter) return false;
                if (catalogTypeFilter && w.wine_type !== catalogTypeFilter) return false;
                if (q) {
                    const haystack = `${w.name} ${w.winery} ${w.appellation} ${w.country || ""} ${w.classification || ""} ${w.tagline || ""} ${w.tasting_notes || ""}`.toLowerCase();
                    if (!haystack.includes(q)) return false;
                }
                return true;
            });

            filtered = [...filtered].sort((a, b) => {
                if (catalogSortOrder === "price-desc") return b.price_eur - a.price_eur;
                if (catalogSortOrder === "vintage-desc") return b.vintage - a.vintage;
                if (catalogSortOrder === "name-asc") return a.name.localeCompare(b.name);
                return a.price_eur - b.price_eur;
            });

            if (countEl) {
                countEl.textContent = `Mostrando ${filtered.length} de ${allWines.length} vinos`;
            }
            if (resetBtn) {
                const hasFilter = Boolean(catalogSearchQuery || catalogCountryFilter || catalogDoFilter || catalogTypeFilter || highlightedCatalogWineId);
                resetBtn.classList.toggle("hidden", !hasFilter);
            }

            if (filtered.length === 0) {
                grid.innerHTML = `
                    <div class="col-span-full bg-butter/50 border border-espresso/15 rounded p-8 text-center space-y-3">
                        <p class="font-serif text-xl text-espresso">No encontramos etiquetas con estos filtros</p>
                        <p class="text-xs text-walnut">Prueba limpiando la búsqueda o seleccionando otra Denominación de Origen.</p>
                        <button type="button" onclick="resetCatalogFilters()" class="px-4 py-2 bg-bordeaux text-cream text-xs font-mono rounded cursor-pointer">
                            Restablecer Catálogo
                        </button>
                    </div>
                `;
                return;
            }

            grid.innerHTML = filtered.map(w => {
                const isHighlighted = highlightedCatalogWineId && w.id === highlightedCatalogWineId;
                const s = w.sensory || { body: 5, acidity: 5, tannins: 5 };
                return `
                    <article data-catalog-wine-id="${escapeHtml(w.id)}" class="bg-cream border ${isHighlighted ? 'border-2 border-bordeaux ring-2 ring-bordeaux/20' : 'border-espresso/15'} rounded p-5 flex flex-col justify-between gap-4 shadow-2xs hover:border-bordeaux/45 transition">
                        <div class="space-y-2.5">
                            <div class="flex items-center justify-between gap-2 text-[10px] font-mono">
                                <span class="text-bordeaux uppercase tracking-wider font-semibold truncate">${escapeHtml(w.appellation)}</span>
                                <span class="px-2 py-0.5 rounded bg-butter border border-espresso/10 text-walnut shrink-0">${escapeHtml(translateWineType(w.wine_type))} · ${escapeHtml(w.vintage)}</span>
                            </div>
                            <div class="flex justify-between items-baseline gap-2">
                                <h3 class="font-serif text-xl text-espresso leading-snug">${escapeHtml(w.name)}</h3>
                                <span class="font-mono text-sm font-semibold text-espresso tabular-nums shrink-0">${w.price_eur.toFixed(2)} €</span>
                            </div>
                            <p class="text-xs font-mono text-walnut">${escapeHtml(w.winery)}</p>
                            <p class="font-serif italic text-sm text-bordeaux/90 leading-snug">«${escapeHtml(w.tagline || w.tasting_notes)}»</p>
                            <p class="text-xs text-walnut line-clamp-2">${escapeHtml(w.tasting_notes)}</p>
                        </div>

                        <div class="space-y-3 pt-3 border-t border-espresso/10">
                            <div class="flex items-center justify-between text-[10px] font-mono text-walnut tabular-nums">
                                <span>Cuerpo ${s.body.toFixed(1)} · Acidez ${s.acidity.toFixed(1)} · Taninos ${s.tannins.toFixed(1)}</span>
                                <span>${w.serving_temp_c.toFixed(0)} °C</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <button type="button" data-action="add-cellar" data-wine-id="${escapeHtml(w.id)}" class="flex-1 py-1.5 px-3 bg-bordeaux text-cream text-[11px] font-mono rounded hover:bg-bordeaux/90 transition cursor-pointer">
                                    + Añadir a Bodega
                                </button>
                                <button type="button" data-action="view-atlas" data-wine-id="${escapeHtml(w.id)}" class="py-1.5 px-2.5 bg-butter hover:bg-butter/80 text-espresso border border-espresso/15 text-[11px] font-mono rounded transition cursor-pointer">
                                    Ver en Atlas →
                                </button>
                            </div>
                        </div>
                    </article>
                `;
            }).join("");

            grid.querySelectorAll('button[data-action="add-cellar"]').forEach(btn => {
                btn.addEventListener("click", () => {
                    quickAddWineToCellar(btn.getAttribute("data-wine-id"), "Catálogo");
                });
            });
            grid.querySelectorAll('button[data-action="view-atlas"]').forEach(btn => {
                btn.addEventListener("click", () => {
                    bridgeWineToAtlas(btn.getAttribute("data-wine-id"));
                });
            });
        }

        /* --- Atlas Cartográfico de Terroirs & Bodegas D.O. (Tab 1) --- */

        function populateAtlasDishSelect() {
            const select = document.getElementById("atlas-radar-dish-select");
            if (!select || allDishes.length === 0) return;
            select.innerHTML = allDishes.map(d =>
                `<option value="${escapeHtml(d.id)}" ${d.id === selectedDishId ? 'selected' : ''}>${escapeHtml(d.name)} (${escapeHtml(d.category)})</option>`
            ).join("");
        }

        async function initAtlas() {
            await loadAtlasLayer(activeAtlasLayer);
        }

        async function filterAtlasByCountry(country, activeBtn) {
            selectedCountry = country;
            selectedDo = "";
            document.querySelectorAll(".country-pill").forEach(b => b.classList.remove("is-active"));
            if (activeBtn) activeBtn.classList.add("is-active");

            const labelEl = document.getElementById("atlas-selected-country-label");
            if (labelEl) {
                labelEl.textContent = country ? `${country} · Atlas Regional` : "Europa (4 Países)";
            }

            await loadAtlasLayer(activeAtlasLayer);

            if (leafletMap) {
                if (country && COUNTRY_BOUNDS[country]) {
                    leafletMap.flyToBounds(COUNTRY_BOUNDS[country], { padding: [24, 24], duration: 0.75 });
                } else {
                    leafletMap.setView(EUROPE_DEFAULT_VIEW.center, EUROPE_DEFAULT_VIEW.zoom, { animate: true });
                }
            }
        }

        async function loadAtlasLayer(layer) {
            try {
                const countryQuery = selectedCountry ? `&country=${encodeURIComponent(selectedCountry)}` : "";
                const res = await fetch(`/api/v1/atlas/geojson?layer=${encodeURIComponent(layer)}${countryQuery}`);
                if (!res.ok) throw new Error("Fallo al obtener GeoJSON del Atlas.");
                const data = await res.json();
                atlasFeatures = data.features || [];

                const badge = document.getElementById("atlas-status-badge");
                if (badge) {
                    const wineriesCount = atlasFeatures.filter(f => f.properties.feature_type === "winery").length;
                    const regionsCount = atlasFeatures.filter(f => f.properties.feature_type === "region").length;
                    const uniqueDos = new Set(atlasFeatures.map(f => f.properties.appellation)).size;
                    if (layer === "regions") badge.textContent = `${regionsCount} Regiones`;
                    else if (layer === "all") badge.textContent = `${regionsCount} Regiones · ${wineriesCount} Bodegas`;
                    else badge.textContent = `${uniqueDos} Regiones · ${wineriesCount} Bodegas`;
                }

                populateDoPills();

                if (atlasFeatures.length > 0) {
                    const matchingDo = selectedDo ? atlasFeatures.find(f => f.properties.appellation === selectedDo) : null;
                    selectAtlasFeature(matchingDo || atlasFeatures[0]);
                }

                if (activeBasemapId !== "svg-offline" && typeof L !== "undefined" && typeof L.map === "function") {
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
            if (!container) return;
            const dos = [...new Set(atlasFeatures.map(f => f.properties.appellation))].sort();

            container.innerHTML = `<button type="button" data-do="" class="do-pill px-3 py-1.5 rounded-sm ${selectedDo === "" ? "is-active" : ""} cursor-pointer">Todas (${dos.length} D.O.)</button>`;

            dos.forEach(doName => {
                const btn = document.createElement("button");
                btn.type = "button";
                btn.setAttribute("data-do", doName);
                btn.className = `do-pill px-3 py-1.5 rounded-sm cursor-pointer ${selectedDo === doName ? "is-active" : ""}`;
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

            document.getElementById("atlas-selected-do-label").textContent = doName || `Todas las regiones (${allRegions.length} D.O.)`;

            const matching = doName ? atlasFeatures.filter(f => f.properties.appellation === doName) : atlasFeatures;
            if (matching.length > 0) {
                selectAtlasFeature(matching[0]);
            }

            if (leafletMap) {
                if (doName && matching.length > 0) {
                    const first = matching[0];
                    leafletMap.setView([first.geometry.coordinates[1], first.geometry.coordinates[0]], 8, { animate: true });
                } else if (selectedCountry && COUNTRY_BOUNDS[selectedCountry]) {
                    leafletMap.flyToBounds(COUNTRY_BOUNDS[selectedCountry], { padding: [24, 24], duration: 0.75 });
                } else {
                    leafletMap.setView(EUROPE_DEFAULT_VIEW.center, EUROPE_DEFAULT_VIEW.zoom, { animate: true });
                }
            }

            highlightSvgMarkers(doName);
        }

        function resolveSensoryForAtlasFeature(feature) {
            const p = feature.properties;
            if (p.sensory) return { sensory: p.sensory, wine: p };
            const doWines = allWines.filter(w => w.appellation === p.appellation);
            if (doWines.length === 0) {
                return {
                    sensory: { body: 6.5, acidity: 6.5, tannins: 6.0, fruit: 7.0, oak: 6.0 },
                    wine: { name: p.appellation, winery: `${p.winery_count || 3} bodegas`, appellation: p.appellation, price_eur: 28, tasting_notes: p.description || p.winery_catalog_summary || "" }
                };
            }
            const avg = (key) => Number((doWines.reduce((s, w) => s + w.sensory[key], 0) / doWines.length).toFixed(1));
            return {
                sensory: {
                    body: avg("body"),
                    acidity: avg("acidity"),
                    tannins: avg("tannins"),
                    fruit: avg("fruit"),
                    oak: avg("oak")
                },
                wine: {
                    id: doWines[0].id,
                    name: `${p.appellation} (Perfil Medio)`,
                    winery: `${doWines.length} bodegas catalogadas`,
                    appellation: p.appellation,
                    price_eur: Number((doWines.reduce((s, w) => s + w.price_eur, 0) / doWines.length).toFixed(2)),
                    tasting_notes: p.description || doWines[0].tagline || ""
                }
            };
        }

        function computeClientCompatibility(a, b) {
            const sq = (a.body - b.body) ** 2 + (a.acidity - b.acidity) ** 2 + (a.tannins - b.tannins) ** 2 + (a.fruit - b.fruit) ** 2 + (a.oak - b.oak) ** 2;
            const maxDist = Math.sqrt(5 * 81);
            return Math.max(0, Math.min(100, 100 * (1 - Math.sqrt(sq) / maxDist)));
        }

        function updateAtlasRadar(feature) {
            const resolved = resolveSensoryForAtlasFeature(feature);
            const wineSensory = resolved.sensory;
            const info = resolved.wine;

            const dishSelect = document.getElementById("atlas-radar-dish-select");
            const refDishId = (dishSelect && dishSelect.value) ? dishSelect.value : selectedDishId;
            const dish = allDishes.find(d => d.id === refDishId) || { name: "Plato de referencia", target_sensory: { body: 7, acidity: 7, tannins: 7, fruit: 7, oak: 7 } };
            const target = dish.target_sensory;

            const score = computeClientCompatibility(target, wineSensory);
            document.getElementById("atlas-radar-score").textContent = `${score.toFixed(1)}% afinidad`;
            document.getElementById("atlas-radar-title").textContent = info.name;
            document.getElementById("atlas-radar-subtitle").textContent = `${info.winery} · ${info.appellation} · ${(info.price_eur || 0).toFixed(2)} €`;
            document.getElementById("atlas-radar-notes").textContent = info.tagline || info.tasting_notes || "";

            document.getElementById("atlas-val-body").textContent = wineSensory.body.toFixed(1);
            document.getElementById("atlas-val-acidity").textContent = wineSensory.acidity.toFixed(1);
            document.getElementById("atlas-val-tannins").textContent = wineSensory.tannins.toFixed(1);
            document.getElementById("atlas-val-fruit").textContent = wineSensory.fruit.toFixed(1);
            document.getElementById("atlas-val-oak").textContent = wineSensory.oak.toFixed(1);

            const canvas = document.getElementById("atlasRadarChart");
            if (canvas && typeof Chart !== "undefined") {
                const ctx = canvas.getContext("2d");
                if (radarChart) radarChart.destroy();
                radarChart = new Chart(ctx, buildRadarConfig(target, wineSensory, info.name, dish.name));
            }
        }

        function selectAtlasFeature(feature) {
            activeAtlasFeature = feature;
            const p = feature.properties;

            document.getElementById("terroir-community").textContent = p.autonomous_community || "España";
            document.getElementById("terroir-altitude").textContent = p.altitude_range_m ? `${p.altitude_range_m}` : `${p.altitude_m || 500} m altitud`;
            document.getElementById("terroir-do-name").textContent = p.appellation;
            document.getElementById("terroir-tagline").textContent = p.tagline || p.description || p.winery_catalog_summary || "";
            document.getElementById("terroir-climate").textContent = p.climate;
            document.getElementById("terroir-soil").textContent = p.soil;
            document.getElementById("terroir-grape").textContent = p.signature_grape;

            const isRegion = p.feature_type === "region";
            const doWines = allWines.filter(w => w.appellation === p.appellation);
            document.getElementById("terroir-winery").textContent = isRegion ? `${p.winery_count || doWines.length} bodegas en D.O.` : p.winery;
            document.getElementById("terroir-wine-name").textContent = isRegion ? (doWines[0] ? `${doWines[0].name} (${doWines[0].vintage})` : p.name) : `${p.name} (${p.vintage})`;

            const listEl = document.getElementById("terroir-wineries-list");
            const sameDoWineries = doWines.length > 0 ? doWines : atlasFeatures.filter(f => f.properties.appellation === p.appellation && f.properties.feature_type === "winery").map(f => f.properties);
            document.getElementById("terroir-winery-count").textContent = `${sameDoWineries.length} bodegas`;

            listEl.innerHTML = sameDoWineries.map(w => {
                const isCur = !isRegion && w.id === feature.id;
                return `
                    <button type="button" data-wine-id="${escapeHtml(w.id)}" class="w-full text-left p-2 rounded flex items-center justify-between gap-2 text-xs transition cursor-pointer ${isCur ? 'bg-bordeaux text-cream font-medium' : 'bg-cream hover:bg-butter text-espresso'}">
                        <span class="truncate">${escapeHtml(w.winery)} · ${escapeHtml(w.name)}</span>
                        <span class="font-mono text-[11px] shrink-0">${(w.price_eur || 0).toFixed(2)} €</span>
                    </button>
                `;
            }).join("");

            listEl.querySelectorAll("button").forEach(btn => {
                btn.addEventListener("click", () => {
                    const wid = btn.getAttribute("data-wine-id");
                    const foundFeature = atlasFeatures.find(f => f.id === wid);
                    if (foundFeature) {
                        selectAtlasFeature(foundFeature);
                        if (leafletMap) {
                            leafletMap.setView([foundFeature.geometry.coordinates[1], foundFeature.geometry.coordinates[0]], 8, { animate: true });
                        }
                    } else {
                        const foundWine = allWines.find(w => w.id === wid);
                        if (foundWine) {
                            selectAtlasFeature({
                                id: foundWine.id,
                                geometry: { coordinates: [foundWine.longitude, foundWine.latitude] },
                                properties: { ...foundWine, feature_type: "winery", soil: foundWine.soil_type, signature_grape: p.signature_grape, autonomous_community: p.autonomous_community }
                            });
                        }
                    }
                });
            });

            updateAtlasRadar(feature);
        }

        function syncBasemapButtons(providerId) {
            document.querySelectorAll(".atlas-basemap-btn").forEach(btn => {
                const isActive = btn.getAttribute("data-basemap") === providerId;
                btn.classList.toggle("is-active", isActive);
                btn.classList.toggle("text-walnut", !isActive);
            });
        }

        function switchBasemapProvider(providerId) {
            if (providerId === "svg-offline") {
                initSvgFallbackAtlas();
                return;
            }
            if (typeof L === "undefined" || typeof L.map !== "function") {
                initSvgFallbackAtlas();
                showToast("Leaflet.js no disponible sin conexión; manteniendo Atlas SVG.", { variant: "warning" });
                return;
            }
            activeBasemapId = BASEMAP_PROVIDERS[providerId] ? providerId : "osm-editorial";
            initLeafletAtlas();
            setTimeout(() => {
                if (atlasMap) atlasMap.invalidateSize();
            }, 60);
        }

        function applyLeafletBasemap(providerId) {
            if (!leafletMap) return;
            const resolvedId = BASEMAP_PROVIDERS[providerId] ? providerId : "osm-editorial";
            const cfg = BASEMAP_PROVIDERS[resolvedId];
            activeBasemapId = resolvedId;
            syncBasemapButtons(resolvedId);

            const mapDiv = document.getElementById("atlas-map");
            const fallbackDiv = document.getElementById("atlas-svg-fallback");
            if (mapDiv) mapDiv.classList.remove("hidden");
            if (fallbackDiv) fallbackDiv.classList.add("hidden");

            if (activeTileLayer) {
                leafletMap.removeLayer(activeTileLayer);
                activeTileLayer = null;
            }
            consecutiveTileErrors = 0;

            const tileLayer = L.tileLayer(cfg.url, cfg.options);
            tileLayer.on("tileload", () => {
                consecutiveTileErrors = 0;
            });
            tileLayer.on("tileerror", () => {
                if (activeTileLayer !== tileLayer) return;
                consecutiveTileErrors += 1;
                if (consecutiveTileErrors >= MAX_CONSECUTIVE_TILE_ERRORS) {
                    const fallbackTarget = cfg.nextFallback;
                    console.warn(`Basemap '${resolvedId}' tileerror threshold reached; failing over to '${fallbackTarget}'.`);
                    if (fallbackTarget && BASEMAP_PROVIDERS[fallbackTarget]) {
                        applyLeafletBasemap(fallbackTarget);
                        showToast("Conmutado a mapa IGN España (CC-BY 4.0) por indisponibilidad de teselas.", { variant: "warning" });
                    } else {
                        initSvgFallbackAtlas();
                        showToast("Activado Atlas Vectorial SVG Offline (sin conexión a teselas).", { variant: "warning" });
                    }
                }
            });

            activeTileLayer = tileLayer.addTo(leafletMap);
            const labelEl = document.getElementById("map-engine-label");
            if (labelEl) labelEl.textContent = cfg.label;
        }

        function initLeafletAtlas() {
            try {
                if (activeBasemapId === "svg-offline") {
                    initSvgFallbackAtlas();
                    return;
                }
                const mapEl = document.getElementById("atlas-map");
                const fallbackDiv = document.getElementById("atlas-svg-fallback");
                if (!mapEl) return;
                mapEl.classList.remove("hidden");
                if (fallbackDiv) fallbackDiv.classList.add("hidden");

                if (!leafletMap) {
                    leafletMap = L.map("atlas-map", {
                        center: EUROPE_DEFAULT_VIEW.center,
                        zoom: EUROPE_DEFAULT_VIEW.zoom,
                        zoomControl: true,
                        attributionControl: true
                    });
                    if (leafletMap.attributionControl) {
                        leafletMap.attributionControl.setPrefix(false);
                    }
                    atlasMap = leafletMap;
                }

                applyLeafletBasemap(activeBasemapId);

                if (activeTab !== "atlas") {
                    atlasNeedsInitialCenter = true;
                }

                mapMarkers.forEach(m => leafletMap.removeLayer(m.marker));
                mapMarkers = [];

                const wineryIcon = L.divIcon({
                    className: "custom-pin",
                    html: '<div class="custom-pin-inner"></div>',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });
                const regionIcon = L.divIcon({
                    className: "custom-region-pin",
                    html: '<div class="custom-region-pin-inner"></div>',
                    iconSize: [26, 26],
                    iconAnchor: [13, 13]
                });

                atlasFeatures.forEach(feat => {
                    const coords = feat.geometry.coordinates;
                    const isRegion = feat.properties.feature_type === "region";
                    const marker = L.marker([coords[1], coords[0]], { icon: isRegion ? regionIcon : wineryIcon }).addTo(leafletMap);
                    const tooltipHtml = isRegion
                        ? `<strong>${escapeHtml(feat.properties.appellation)}</strong><br><span style="font-size:11px;color:#6A5A4F">${feat.properties.winery_count || 3} bodegas · ${escapeHtml(feat.properties.autonomous_community)}</span>`
                        : `<strong>${escapeHtml(feat.properties.winery)}</strong><br><span style="font-size:11px;color:#6A5A4F">${escapeHtml(feat.properties.appellation)} · ${escapeHtml(feat.properties.name)}</span>`;
                    marker.bindTooltip(tooltipHtml, { direction: "top", offset: [0, -8] });
                    marker.on("click", () => selectAtlasFeature(feat));
                    mapMarkers.push({ marker, feature: feat });
                });
            } catch (err) {
                console.error("Leaflet init error, switching to SVG fallback:", err);
                initSvgFallbackAtlas();
            }
        }

        function initSvgFallbackAtlas() {
            activeBasemapId = "svg-offline";
            syncBasemapButtons("svg-offline");
            const mapDiv = document.getElementById("atlas-map");
            const fallbackDiv = document.getElementById("atlas-svg-fallback");
            const canvas = document.getElementById("svg-map-canvas");
            if (mapDiv) mapDiv.classList.add("hidden");
            if (fallbackDiv) fallbackDiv.classList.remove("hidden");
            const labelEl = document.getElementById("map-engine-label");
            if (labelEl) labelEl.textContent = "Cartografía: SVG Determinista (Modo Offline)";

            const svgW = 680;
            const svgH = 340;
            const lonToX = (lon) => ((lon - (-9.5)) / (3.5 - (-9.5))) * (svgW - 80) + 40;
            const latToY = (lat) => ((44.0 - lat) / (44.0 - 36.0)) * (svgH - 60) + 30;

            let svgContent = `
                <svg viewBox="0 0 ${svgW} ${svgH}" class="w-full h-full select-none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M 60 70 Q 180 40 320 50 Q 500 50 560 90 L 590 140 Q 580 200 540 260 Q 480 320 380 330 Q 280 330 180 320 Q 90 300 70 230 Q 50 150 60 70 Z" fill="#EFE7D6" stroke="rgba(35, 27, 22, 0.2)" stroke-width="1.5" stroke-dasharray="3 3"/>
                    <path d="M 120 70 Q 280 80 500 100" fill="none" stroke="rgba(107, 29, 40, 0.12)" stroke-width="1"/>
                    <path d="M 100 160 Q 300 170 540 180" fill="none" stroke="rgba(107, 29, 40, 0.12)" stroke-width="1"/>
            `;

            atlasFeatures.forEach(feat => {
                const coords = feat.geometry.coordinates;
                const x = lonToX(coords[0]);
                const y = latToY(coords[1]);
                const isRegion = feat.properties.feature_type === "region";
                const r = isRegion ? 9 : 7;
                const fill = isRegion ? "#9C6F38" : "#6B1D28";
                svgContent += `
                    <g class="svg-pin cursor-pointer group" data-feat-id="${escapeHtml(feat.id)}" data-do="${escapeHtml(feat.properties.appellation)}" transform="translate(${x}, ${y})">
                        <circle r="${r}" fill="${fill}" stroke="#FAF6EE" stroke-width="1.5" />
                        <circle r="2.2" fill="#FAF6EE"/>
                        <title>${escapeHtml(feat.properties.winery || feat.properties.name)} (${escapeHtml(feat.properties.appellation)})</title>
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
                    circle.setAttribute("opacity", "1.0");
                } else {
                    circle.setAttribute("opacity", "0.3");
                }
            });
        }

        /* --- Contextual Cross-Tab Bridges --- */

        function bridgeAtlasToCarte(feature) {
            const p = feature.properties;
            catalogDoFilter = p.appellation || "";
            catalogSearchQuery = "";
            catalogTypeFilter = "";
            highlightedCatalogWineId = p.feature_type === "winery" ? p.id : "";

            const doSelect = document.getElementById("catalog-do-filter");
            const searchInput = document.getElementById("catalog-search-input");
            if (doSelect) doSelect.value = catalogDoFilter;
            if (searchInput) searchInput.value = "";
            document.querySelectorAll(".catalog-type-pill").forEach(b => {
                const isAll = b.getAttribute("data-type") === "";
                b.classList.toggle("is-active", isAll);
                b.classList.toggle("bg-cream", !isAll);
                b.classList.toggle("text-walnut", !isAll);
            });

            renderWineCatalog();
            switchTab("carte", true);

            setTimeout(() => {
                const targetEl = highlightedCatalogWineId
                    ? Array.from(document.querySelectorAll("[data-catalog-wine-id]"))
                        .find(el => el.getAttribute("data-catalog-wine-id") === highlightedCatalogWineId)
                    : document.getElementById("catalog-section");
                if (targetEl) targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
            }, 120);

            showToast(`Filtrando La Carte por ${p.appellation}`);
        }

        function bridgeAtlasToBodega(feature) {
            const p = feature.properties;
            let wineId = p.feature_type === "winery" ? p.id : "";
            if (!wineId) {
                const firstInDo = allWines.find(w => w.appellation === p.appellation);
                wineId = firstInDo ? firstInDo.id : (allWines[0] ? allWines[0].id : "");
            }
            const wine = allWines.find(w => w.id === wineId);
            const sel = document.getElementById("cellar-wine-select");
            const priceInput = document.getElementById("cellar-price-input");
            if (sel && wineId) {
                sel.value = wineId;
            }
            if (priceInput && wine) {
                priceInput.value = wine.price_eur.toFixed(2);
            }

            switchTab("bodega", true);
            setTimeout(() => {
                document.getElementById("cellar-qty-input")?.focus();
            }, 100);

            showToast(`${wine ? wine.name : p.name} preseleccionado en Mi Bodega`);
        }

        function bridgeWineToAtlas(wineId) {
            const wine = allWines.find(w => w.id === wineId);
            if (!wine) return;

            selectedDo = wine.appellation;
            switchTab("atlas", true);

            const doBtn = Array.from(document.querySelectorAll(".do-pill"))
                .find(b => b.getAttribute("data-do") === wine.appellation);
            document.querySelectorAll(".do-pill").forEach(b => b.classList.remove("is-active"));
            if (doBtn) doBtn.classList.add("is-active");
            document.getElementById("atlas-selected-do-label").textContent = wine.appellation;

            const feat = atlasFeatures.find(f => f.id === wine.id) || {
                id: wine.id,
                geometry: { coordinates: [wine.longitude, wine.latitude] },
                properties: {
                    ...wine,
                    feature_type: "winery",
                    soil: wine.soil_type,
                    signature_grape: "Varietal de la D.O.",
                    autonomous_community: "España"
                }
            };
            selectAtlasFeature(feat);
            setTimeout(() => {
                if (atlasMap) {
                    atlasMap.invalidateSize();
                    atlasMap.setView([wine.latitude, wine.longitude], 8, { animate: true });
                }
            }, 90);
            showToast(`Mostrando ${wine.winery} en el Atlas de Terroirs`);
        }

        function bridgePairingToVeladas() {
            const dish = allDishes.find(d => d.id === selectedDishId);
            if (!dish) return;
            const cat = getCategoryForDish(dish);

            let targetSelectId = "plan-main-select";
            if (cat === "Entrantes y Cuchara" || cat === "Ensaladas y Huerta" || cat === "Tapas y Pintxos" || cat === "Platos Vegetarianos y Setas") {
                targetSelectId = "plan-starter-select";
            } else if (cat === "Embutidos y Quesos" || cat === "Postres y Dulces") {
                targetSelectId = "plan-dessert-select";
            }

            const selectEl = document.getElementById(targetSelectId);
            if (selectEl) {
                selectEl.value = dish.id;
            }

            const singleBudget = parseFloat(document.getElementById("budget-slider")?.value || "50");
            const smartTotalBudget = Math.min(250, Math.max(45, Math.round((singleBudget * 2.4) / 5) * 5));
            const planSlider = document.getElementById("plan-budget-slider");
            const planVal = document.getElementById("plan-budget-value");
            if (planSlider && planVal) {
                planSlider.value = smartTotalBudget;
                planVal.textContent = `${smartTotalBudget} €`;
            }

            switchTab("veladas", true);
            generateMenuPlan();
            showToast(`Velada adaptada con "${dish.name}" (${smartTotalBudget} € total)`);
        }

        /* --- Evening & 3-Course Menu Sommelier Planner (Tab 3) --- */

        function populatePlannerSelects() {
            const starterSelect = document.getElementById("plan-starter-select");
            const mainSelect = document.getElementById("plan-main-select");
            const dessertSelect = document.getElementById("plan-dessert-select");
            if (!starterSelect || !mainSelect || !dessertSelect || allDishes.length === 0) return;

            const starterCats = new Set(["Entrantes y Cuchara", "Tapas y Pintxos", "Ensaladas y Huerta"]);
            const mainCats = new Set(["Carnes y Caza", "Pescados y Mariscos", "Arroces", "Platos Vegetarianos y Setas"]);
            const dessertCats = new Set(["Embutidos y Quesos", "Postres y Dulces"]);

            const buildGroupedOptions = (preferredSet, defaultId) => {
                const preferred = allDishes.filter(d => preferredSet.has(getCategoryForDish(d)));
                const others = allDishes.filter(d => !preferredSet.has(getCategoryForDish(d)));
                const optHtml = (list) => list.map(d =>
                    `<option value="${escapeHtml(d.id)}" ${d.id === defaultId ? 'selected' : ''}>${escapeHtml(d.name)} (${escapeHtml(d.category)})</option>`
                ).join("");
                return `<optgroup label="Recomendados para este pase">${optHtml(preferred)}</optgroup>` +
                    `<optgroup label="Toda La Carte">${optHtml(others)}</optgroup>`;
            };

            starterSelect.innerHTML = buildGroupedOptions(starterCats, "salmorejo-cordobes");
            mainSelect.innerHTML = buildGroupedOptions(mainCats, "chuleton-brasa");
            dessertSelect.innerHTML = buildGroupedOptions(dessertCats, "queso-manchego");
        }

        let lastGeneratedMenuPlan = null;

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
                    lastGeneratedMenuPlan = data;
                    renderMenuPlanResults(data);
                    return;
                }
            } catch (err) {
                console.warn("Endpoint /api/v1/pairings/menu-plan no disponible:", err);
            }

            const fallbackData = buildLocalMenuPlan(selectedOccasion, starterId, mainId, dessertId);
            lastGeneratedMenuPlan = fallbackData;
            renderMenuPlanResults(fallbackData);
        }

        function buildLocalMenuPlan(occasion, starterId, mainId, dessertId) {
            const starterDish = allDishes.find(d => d.id === starterId) || { name: "Salmorejo cordobés", description: "Crema fría de tomate y jamón ibérico" };
            const mainDish = allDishes.find(d => d.id === mainId) || { name: "Chuletón de vaca vieja", description: "Corte madurado a la brasa" };
            const dessertDish = allDishes.find(d => d.id === dessertId) || { name: "Queso Manchego Curado", description: "Leche cruda de oveja en cueva" };

            const defaultWines = [
                { id: "gramona-imperial", name: "Gramona Imperial Brut Nature", winery: "Gramona", appellation: "Corpinnat", vintage: 2017, price_eur: 24.50, tagline: "Burbuja cremosa y acidez gastronómica.", sensory: { body: 5.5, acidity: 8.5, tannins: 1.5, fruit: 7.0, oak: 4.5 }, vintage_label: "En su cumbre hoy", vintage_color: "green", fridge: "2 horas en nevera (8 °C)", uncork: "Descorche directo", note: "Acidez viva que limpia el paladar." },
                { id: "vina-ardanza-reserva", name: "Viña Ardanza Reserva", winery: "La Rioja Alta, S.A.", appellation: "D.O.Ca. Rioja", vintage: 2017, price_eur: 34.00, tagline: "Elegancia clásica riojana de taninos sedosos.", sensory: { body: 7.5, acidity: 7.0, tannins: 7.5, fruit: 7.5, oak: 8.0 }, vintage_label: "Plenitud de guarda", vintage_color: "gold", fridge: "20 min en nevera (16 °C)", uncork: "Decantar 30 min", note: "Nervio tánico elegante para el plato principal." },
                { id: "la-panesa-fino", name: "Fino La Panesa Especial", winery: "Emilio Hidalgo", appellation: "D.O. Jerez-Xérès-Sherry", vintage: 2018, price_eur: 32.00, tagline: "Salinidad y almendra verde en bota.", sensory: { body: 6.5, acidity: 7.5, tannins: 2.0, fruit: 4.5, oak: 8.5 }, vintage_label: "Solera viva", vintage_color: "gold", fridge: "40 min en nevera (12 °C)", uncork: "Copa amplia", note: "Salinidad noble para quesos curados y cierre." }
            ];

            return {
                occasion: occasion,
                total_price_eur: 90.50,
                average_compatibility_score: 95.2,
                progression_valid: true,
                occasion_ambience_tip: "Copas finas preparadas por comensal y servicio pausado entre pases.",
                progression_summary: "Progresión armónica ascendente en tres tiempos.",
                courses: [
                    { course_number: 1, course_title: "1.º Pase · Entrante", dish: starterDish, wine: defaultWines[0], vintage_status_label: defaultWines[0].vintage_label, vintage_semaphore: "green", fridge_tip: defaultWines[0].fridge, uncork_tip: defaultWines[0].uncork, sommelier_note: defaultWines[0].note },
                    { course_number: 2, course_title: "2.º Pase · Principal", dish: mainDish, wine: defaultWines[1], vintage_status_label: defaultWines[1].vintage_label, vintage_semaphore: "gold", fridge_tip: defaultWines[1].fridge, uncork_tip: defaultWines[1].uncork, sommelier_note: defaultWines[1].note },
                    { course_number: 3, course_title: "3.º Pase · Cierre", dish: dessertDish, wine: defaultWines[2], vintage_status_label: defaultWines[2].vintage_label, vintage_semaphore: "gold", fridge_tip: defaultWines[2].fridge, uncork_tip: defaultWines[2].uncork, sommelier_note: defaultWines[2].note }
                ]
            };
        }

        function renderProgressionChart(courses, isValid) {
            const badge = document.getElementById("plan-progression-badge");
            if (badge) {
                badge.textContent = isValid !== false ? "Progresión Ascendente Óptima" : "Progresión de Contraste";
            }
            const canvas = document.getElementById("progressionChart");
            if (!canvas || typeof Chart === "undefined" || !courses || courses.length === 0) return;

            const labels = courses.map((c, idx) => `${idx + 1}.º ${(c.wine && c.wine.name) ? c.wine.name.split(" ").slice(0, 2).join(" ") : "Pase"}`);
            const extract = (key) => courses.map(c => (c.wine && c.wine.sensory) ? c.wine.sensory[key] : 5.0);

            if (progressionChart) progressionChart.destroy();
            progressionChart = new Chart(canvas.getContext("2d"), {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [
                        { label: "Cuerpo", data: extract("body"), borderColor: "#6B1D28", backgroundColor: "rgba(107, 29, 40, 0.1)", tension: 0.35, borderWidth: 2.5, pointRadius: 4 },
                        { label: "Acidez", data: extract("acidity"), borderColor: "#4F5D47", backgroundColor: "rgba(79, 93, 71, 0.1)", tension: 0.35, borderWidth: 2, pointRadius: 4 },
                        { label: "Taninos", data: extract("tannins"), borderColor: "#231B16", borderDash: [4, 3], tension: 0.35, borderWidth: 1.8, pointRadius: 3.5 },
                        { label: "Madera", data: extract("oak"), borderColor: "#9C6F38", tension: 0.35, borderWidth: 1.8, pointRadius: 3.5 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { min: 0, max: 10, ticks: { stepSize: 2, color: "#6A5A4F", font: { family: '"JetBrains Mono"', size: 10 } }, grid: { color: "rgba(35, 27, 22, 0.08)" } },
                        x: { ticks: { color: "#231B16", font: { family: '"Work Sans"', size: 11 } }, grid: { display: false } }
                    },
                    plugins: {
                        legend: {
                            position: "bottom",
                            labels: { boxWidth: 10, color: "#6A5A4F", font: { family: '"JetBrains Mono"', size: 10 } }
                        }
                    }
                }
            });
        }

        function renderMenuPlanResults(data) {
            const totalPrice = data.total_price_eur || 0;
            const avgScore = data.average_compatibility_score || 95.0;
            const ambienceTip = data.occasion_ambience_tip || "Iluminación cálida y conversación sosegada.";
            const progressionSummary = data.progression_summary || "Progresión enológica armónica.";
            const courses = data.courses || [];

            document.getElementById("plan-total-price").textContent = `${totalPrice.toFixed(2)} €`;
            document.getElementById("plan-avg-score").textContent = `${avgScore.toFixed(1)}%`;
            document.getElementById("plan-ambience-tip").textContent = `Ambiente: ${ambienceTip}`;
            document.getElementById("plan-progression-summary").textContent = progressionSummary;

            renderProgressionChart(courses, data.progression_valid);

            const coursesGrid = document.getElementById("plan-courses-grid");
            coursesGrid.innerHTML = courses.map((course, idx) => {
                const wine = course.wine || {};
                const courseTitle = course.course_title || `${idx + 1}.º Pase`;
                const dishName = (course.dish && course.dish.name) || course.dish_name || "Plato seleccionado";
                const dishDesc = (course.dish && course.dish.description) || course.dish_description || "";
                const vintageLabel = course.vintage_status_label || "En su cumbre hoy";
                const semaphore = course.vintage_semaphore || "green";

                let badgeColorClass = "bg-sage/15 text-sage border-sage/30";
                if (semaphore === "gold") badgeColorClass = "bg-brass/15 text-brass border-brass/30";
                else if (semaphore === "amber") badgeColorClass = "bg-amber-100 text-amber-900 border-amber-300";

                return `
                    <div class="bg-cream border border-espresso/15 rounded p-5 space-y-4 flex flex-col justify-between shadow-2xs">
                        <div class="space-y-3">
                            <div class="flex items-center justify-between gap-2 border-b border-espresso/10 pb-2">
                                <span class="text-xs font-mono text-bordeaux uppercase tracking-wider font-semibold">${escapeHtml(courseTitle)}</span>
                                <span class="text-[10px] font-mono px-2 py-0.5 rounded border ${badgeColorClass} font-medium">
                                    ${escapeHtml(vintageLabel)}
                                </span>
                            </div>
                            <div class="space-y-1">
                                <h4 class="font-serif text-xl text-espresso font-normal leading-tight">${escapeHtml(dishName)}</h4>
                                <div class="text-xs font-serif italic text-walnut">${escapeHtml(dishDesc)}</div>
                            </div>
                            <div class="pt-2 border-t border-espresso/8 space-y-1">
                                <div class="flex justify-between items-baseline gap-2">
                                    <span class="font-serif text-lg text-bordeaux font-medium">${escapeHtml(wine.name || '')}</span>
                                    <span class="font-mono text-xs text-espresso font-semibold tabular-nums shrink-0">${(wine.price_eur || 0).toFixed(2)} €</span>
                                </div>
                                <div class="text-xs font-mono text-walnut">
                                    ${escapeHtml(wine.winery || '')} · ${escapeHtml(wine.appellation || '')} (${escapeHtml(wine.vintage || '')})
                                </div>
                                <p class="text-xs font-serif italic text-walnut/90 line-clamp-2 mt-1">«${escapeHtml(wine.tagline || wine.tasting_notes || '')}»</p>
                            </div>
                        </div>

                        <div class="space-y-2.5 pt-3 border-t border-espresso/10 text-xs">
                            <div class="bg-butter/60 rounded p-2.5 space-y-1.5 font-sans">
                                <div class="text-[11px] text-espresso/90 flex items-start gap-1.5">
                                    <span class="shrink-0">❄️</span>
                                    <span><strong>Nevera:</strong> ${escapeHtml(course.fridge_tip || 'Temperatura recomendada')}</span>
                                </div>
                                <div class="text-[11px] text-espresso/90 flex items-start gap-1.5">
                                    <span class="shrink-0">🍾</span>
                                    <span><strong>Descorche:</strong> ${escapeHtml(course.uncork_tip || 'Servicio directo')}</span>
                                </div>
                            </div>
                            <div class="flex items-center justify-between gap-2 pt-1">
                                <p class="text-[11px] text-walnut italic leading-relaxed line-clamp-2">${escapeHtml(course.sommelier_note || '')}</p>
                                ${wine.id ? `<button type="button" data-course-wine-id="${escapeHtml(wine.id)}" class="btn-course-add-cellar shrink-0 px-2 py-1 text-[10px] font-mono rounded border border-bordeaux/30 text-bordeaux hover:bg-bordeaux hover:text-cream transition cursor-pointer">+ Bodega</button>` : ''}
                            </div>
                        </div>
                    </div>
                `;
            }).join("");

            coursesGrid.querySelectorAll(".btn-course-add-cellar").forEach(btn => {
                btn.addEventListener("click", () => {
                    quickAddWineToCellar(btn.getAttribute("data-course-wine-id"), "Velada");
                });
            });

            const printList = document.getElementById("print-courses-list");
            document.getElementById("print-card-title").textContent = data.printable_card_title || data.occasion || selectedOccasion;
            printList.innerHTML = courses.map((course, idx) => {
                const wine = course.wine || {};
                const courseTitle = course.course_title || `${idx + 1}.º Pase`;
                const dishName = (course.dish && course.dish.name) || course.dish_name || "Plato seleccionado";
                return `
                    <div class="pt-4 first:pt-0 space-y-2">
                        <div class="flex items-baseline justify-between text-xs font-mono text-bordeaux uppercase tracking-wider">
                            <span class="font-semibold">${escapeHtml(courseTitle)}</span>
                            <span class="text-walnut">${escapeHtml(wine.appellation || '')} · Añada ${escapeHtml(wine.vintage || '')}</span>
                        </div>
                        <div class="flex flex-wrap items-baseline justify-between gap-3">
                            <h4 class="font-serif text-2xl text-espresso">${escapeHtml(dishName)}</h4>
                            <span class="font-serif text-xl text-bordeaux font-normal">${escapeHtml(wine.name || '')}</span>
                        </div>
                        <div class="flex justify-between items-baseline text-xs font-mono text-walnut">
                            <span>Bodega: ${escapeHtml(wine.winery || '')}</span>
                            <span class="tabular-nums font-medium text-espresso">${(wine.price_eur || 0).toFixed(2)} €</span>
                        </div>
                        <p class="font-serif italic text-sm text-walnut/90">«${escapeHtml(wine.tagline || wine.tasting_notes || '')}»</p>
                    </div>
                `;
            }).join("");
        }

        async function addCurrentMenuTrioToCellar() {
            if (!lastGeneratedMenuPlan || !lastGeneratedMenuPlan.courses) return;
            let added = 0;
            for (const c of lastGeneratedMenuPlan.courses) {
                if (c.wine && c.wine.id) {
                    const ok = await postCellarAddition(c.wine.id, 1, c.wine.price_eur || 0, "Bodega Principal", `Velada: ${lastGeneratedMenuPlan.occasion}`, false);
                    if (ok) added += 1;
                }
            }
            if (added > 0) {
                await loadCellar();
                showToast(`${added} botellas de la velada añadidas a Mi Bodega`, {
                    actionLabel: "Ir a Mi Bodega →",
                    onAction: () => switchTab("bodega")
                });
            }
        }

        /* --- Mi Bodega Personal & Analytics (Tab 4) --- */

        function populateCellarWineSelect() {
            const sel = document.getElementById("cellar-wine-select");
            if (!sel || allWines.length === 0) return;
            const sorted = [...allWines].sort((a, b) => a.name.localeCompare(b.name));
            sel.innerHTML = sorted.map(w =>
                `<option value="${escapeHtml(w.id)}">${escapeHtml(w.name)} — ${escapeHtml(w.appellation)} (${w.price_eur.toFixed(2)} €)</option>`
            ).join("");
            const priceInput = document.getElementById("cellar-price-input");
            if (priceInput && sorted[0]) priceInput.value = sorted[0].price_eur.toFixed(2);
        }

        function computeCellarVintageWindow(wine) {
            if (!wine) return { status: "ready", label: "Listo para disfrutar", badgeClass: "bg-sage/15 text-sage border-sage/30" };
            const currentYear = 2026;
            const peakEnd = (wine.vintage || 2020) + (wine.aging_potential_years || 6);
            if (currentYear >= peakEnd - 1) {
                return { status: "priority", label: `Consumo prioritario (≤${peakEnd})`, badgeClass: "bg-amber-100 text-amber-900 border-amber-300" };
            }
            if ((wine.aging_potential_years || 5) >= 12 && currentYear - (wine.vintage || 2020) < 4) {
                return { status: "aging", label: `Potencial de guarda (${wine.vintage}-${peakEnd})`, badgeClass: "bg-brass/15 text-brass border-brass/30" };
            }
            return { status: "ready", label: `En su cumbre hoy (${wine.vintage}-${peakEnd})`, badgeClass: "bg-sage/15 text-sage border-sage/30" };
        }

        async function loadCellar() {
            try {
                const res = await fetch("/api/v1/cellar");
                if (!res.ok) return;
                cellarItems = await res.json();
                renderCellar();
            } catch (err) {
                console.warn("No se pudo cargar Mi Bodega:", err);
            }
        }

        function updateCellarAnalyticsAndHeader() {
            let totalBottles = 0;
            let totalValue = 0;
            const regions = new Set();
            const styleCounts = {};
            let readyCount = 0;
            let priorityCount = 0;
            let agingCount = 0;

            cellarItems.forEach(item => {
                const qty = item.quantity || 0;
                const w = item.wine;
                const unitPrice = (item.purchase_price_eur && item.purchase_price_eur > 0) ? item.purchase_price_eur : (w ? w.price_eur : 0);
                totalBottles += qty;
                totalValue += qty * unitPrice;
                if (w) {
                    regions.add(w.appellation);
                    const tLabel = translateWineType(w.wine_type);
                    styleCounts[tLabel] = (styleCounts[tLabel] || 0) + qty;
                }
                const win = computeCellarVintageWindow(w);
                if (win.status === "priority") priorityCount += qty;
                else if (win.status === "aging") agingCount += qty;
                else readyCount += qty;
            });

            // Header KPIs & Tab Badge
            document.getElementById("kpi-cellar-bottles").textContent = String(totalBottles);
            document.getElementById("kpi-cellar-value").textContent = `${totalValue.toFixed(0)} €`;
            document.getElementById("tab-badge-bodega").textContent = String(totalBottles);

            // Bodega Tab KPIs
            document.getElementById("cellar-kpi-bottles").textContent = String(totalBottles);
            document.getElementById("cellar-kpi-refs").textContent = `${cellarItems.length} etiquetas distintas`;
            document.getElementById("cellar-kpi-valuation").textContent = `${totalValue.toFixed(2)} €`;
            const avgPrice = totalBottles > 0 ? totalValue / totalBottles : 0;
            document.getElementById("cellar-kpi-avg-price").textContent = `Media: ${avgPrice.toFixed(2)} € / bot.`;
            document.getElementById("cellar-kpi-regions").textContent = String(regions.size);
            const breakdownText = Object.entries(styleCounts).map(([k, v]) => `${k}: ${v}`).join(" · ");
            document.getElementById("cellar-style-breakdown").textContent = breakdownText || "Sin estilos registrados";
            document.getElementById("cellar-kpi-peak").textContent = `${readyCount} listas`;
            document.getElementById("cellar-kpi-peak-detail").textContent = `${priorityCount} prioritarias · ${agingCount} en guarda`;
        }

        function renderCellar() {
            updateCellarAnalyticsAndHeader();
            const listEl = document.getElementById("cellar-inventory-list");
            if (!listEl) return;

            const filtered = cellarItems.filter(item => {
                const w = item.wine || {};
                const win = computeCellarVintageWindow(item.wine);
                if (cellarWindowFilter !== "all" && win.status !== cellarWindowFilter) return false;
                if (cellarSearchQuery) {
                    const hay = `${w.name || item.wine_id} ${w.winery || ""} ${w.appellation || ""} ${item.storage_location || ""} ${item.notes || ""}`.toLowerCase();
                    if (!hay.includes(cellarSearchQuery)) return false;
                }
                return true;
            });

            if (cellarItems.length === 0) {
                listEl.innerHTML = `
                    <div class="bg-butter/40 border border-espresso/15 rounded p-8 text-center space-y-3">
                        <p class="font-serif text-2xl text-espresso">Tu bodega personal está vacía</p>
                        <p class="text-xs text-walnut max-w-md mx-auto">
                            Añade tu primera botella desde el formulario lateral o explora el Atlas y La Carte usando los botones "+ Añadir a Bodega".
                        </p>
                        <div class="flex justify-center gap-3 pt-1">
                            <button type="button" onclick="switchTab('carte')" class="px-4 py-2 bg-bordeaux text-cream text-xs font-mono rounded cursor-pointer">Explorar La Carte →</button>
                            <button type="button" onclick="switchTab('atlas')" class="px-4 py-2 bg-cream border border-espresso/20 text-espresso text-xs font-mono rounded cursor-pointer">Ir al Atlas →</button>
                        </div>
                    </div>
                `;
                return;
            }

            if (filtered.length === 0) {
                listEl.innerHTML = `<div class="bg-butter/40 border border-espresso/12 rounded p-6 text-center text-xs text-walnut">No hay botellas en tu bodega que coincidan con el filtro seleccionado.</div>`;
                return;
            }

            listEl.innerHTML = filtered.map(item => {
                const w = item.wine || { id: item.wine_id, name: item.wine_id, winery: "", appellation: "", vintage: "", price_eur: item.purchase_price_eur || 0 };
                const win = computeCellarVintageWindow(item.wine);
                const unitPrice = item.purchase_price_eur > 0 ? item.purchase_price_eur : (w.price_eur || 0);
                const subtotal = unitPrice * item.quantity;

                return `
                    <article class="bg-cream border border-espresso/15 rounded p-5 flex flex-col sm:flex-row justify-between gap-4 shadow-2xs">
                        <div class="space-y-2 flex-1">
                            <div class="flex flex-wrap items-center gap-2 text-[10px] font-mono">
                                <span class="text-bordeaux uppercase font-semibold">${escapeHtml(w.appellation)}</span>
                                <span class="px-2 py-0.5 rounded border ${win.badgeClass}">${escapeHtml(win.label)}</span>
                                <span class="px-2 py-0.5 rounded bg-butter border border-espresso/10 text-walnut">${escapeHtml(item.storage_location || "Bodega Principal")}</span>
                            </div>
                            <div>
                                <h4 class="font-serif text-2xl text-espresso leading-tight">${escapeHtml(w.name)} <span class="text-base font-mono text-walnut">(${escapeHtml(w.vintage || "")})</span></h4>
                                <p class="text-xs font-mono text-walnut">${escapeHtml(w.winery)}</p>
                            </div>
                            ${item.notes ? `<p class="text-xs italic text-walnut bg-butter/45 px-2.5 py-1.5 rounded border-l-2 border-brass">${escapeHtml(item.notes)}</p>` : ''}
                            <div class="flex flex-wrap items-center gap-3 pt-1 text-[11px] font-mono">
                                <button type="button" data-bridge-atlas="${escapeHtml(item.wine_id)}" class="btn-cellar-atlas text-bordeaux hover:underline cursor-pointer">Ver en Atlas →</button>
                                <span class="text-espresso/25">|</span>
                                <button type="button" data-bridge-carte="${escapeHtml(w.appellation)}" data-wine-id="${escapeHtml(item.wine_id)}" class="btn-cellar-carte text-walnut hover:text-espresso hover:underline cursor-pointer">Explorar en La Carte →</button>
                            </div>
                        </div>

                        <div class="flex sm:flex-col items-center sm:items-end justify-between gap-3 shrink-0 border-t sm:border-t-0 pt-3 sm:pt-0 border-espresso/10">
                            <div class="text-left sm:text-right">
                                <div class="font-mono text-lg font-semibold text-espresso tabular-nums">${subtotal.toFixed(2)} €</div>
                                <div class="text-[11px] font-mono text-walnut tabular-nums">${unitPrice.toFixed(2)} € / bot.</div>
                            </div>
                            <div class="flex items-center gap-1.5">
                                <button type="button" data-item-id="${escapeHtml(item.id)}" class="btn-cellar-dec w-7 h-7 rounded border border-espresso/20 bg-butter hover:bg-bordeaux hover:text-cream font-mono text-sm transition cursor-pointer" title="Descorchar 1 botella">-1</button>
                                <span class="px-2.5 font-mono text-sm font-semibold tabular-nums">${item.quantity}</span>
                                <button type="button" data-wine-id="${escapeHtml(item.wine_id)}" data-price="${unitPrice}" data-loc="${escapeHtml(item.storage_location || "Bodega Principal")}" class="btn-cellar-inc w-7 h-7 rounded border border-espresso/20 bg-butter hover:bg-bordeaux hover:text-cream font-mono text-sm transition cursor-pointer" title="Añadir 1 botella">+1</button>
                                <button type="button" data-item-id="${escapeHtml(item.id)}" data-qty="${item.quantity}" class="btn-cellar-del ml-1 px-2 h-7 rounded border border-bordeaux/30 text-bordeaux hover:bg-bordeaux hover:text-cream font-mono text-[10px] transition cursor-pointer" title="Eliminar registro">Vaciar</button>
                            </div>
                        </div>
                    </article>
                `;
            }).join("");

            listEl.querySelectorAll(".btn-cellar-dec").forEach(btn => {
                btn.addEventListener("click", () => decrementCellarItem(btn.getAttribute("data-item-id"), 1));
            });
            listEl.querySelectorAll(".btn-cellar-del").forEach(btn => {
                btn.addEventListener("click", () => decrementCellarItem(btn.getAttribute("data-item-id"), parseInt(btn.getAttribute("data-qty") || "1", 10)));
            });
            listEl.querySelectorAll(".btn-cellar-inc").forEach(btn => {
                btn.addEventListener("click", async () => {
                    const wid = btn.getAttribute("data-wine-id");
                    const price = parseFloat(btn.getAttribute("data-price") || "0");
                    const loc = btn.getAttribute("data-loc") || "Bodega Principal";
                    await postCellarAddition(wid, 1, price, loc, "", true);
                });
            });
            listEl.querySelectorAll(".btn-cellar-atlas").forEach(btn => {
                btn.addEventListener("click", () => bridgeWineToAtlas(btn.getAttribute("data-bridge-atlas")));
            });
            listEl.querySelectorAll(".btn-cellar-carte").forEach(btn => {
                btn.addEventListener("click", () => {
                    const app = btn.getAttribute("data-bridge-carte") || "";
                    const wid = btn.getAttribute("data-wine-id") || "";
                    catalogDoFilter = app;
                    highlightedCatalogWineId = wid;
                    const doEl = document.getElementById("catalog-do-filter");
                    if (doEl) doEl.value = app;
                    renderWineCatalog();
                    switchTab("carte", true);
                    setTimeout(() => document.getElementById("catalog-section")?.scrollIntoView({ behavior: "smooth" }), 100);
                });
            });
        }

        async function postCellarAddition(wineId, quantity, priceEur, location, notes, showFeedback = true) {
            try {
                const res = await fetch("/api/v1/cellar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        wine_id: wineId,
                        quantity: quantity,
                        purchase_price_eur: priceEur,
                        storage_location: location || "Bodega Principal",
                        notes: notes || ""
                    })
                });
                if (!res.ok) {
                    showError("No se pudo guardar la botella en Mi Bodega.");
                    return false;
                }
                const saved = await res.json();
                await loadCellar();
                if (showFeedback) {
                    const name = (saved.wine && saved.wine.name) ? saved.wine.name : wineId;
                    showToast(`${name} (+${quantity}) guardado en Mi Bodega`, {
                        actionLabel: activeTab !== "bodega" ? "Ver Bodega →" : null,
                        onAction: () => switchTab("bodega")
                    });
                }
                return true;
            } catch (err) {
                console.error("Error adding to cellar:", err);
                showError("Error de red al guardar en Mi Bodega.");
                return false;
            }
        }

        async function quickAddWineToCellar(wineId, sourceLabel) {
            const wine = allWines.find(w => w.id === wineId);
            const price = wine ? wine.price_eur : 0;
            const note = sourceLabel ? `Añadido desde ${sourceLabel}` : "";
            await postCellarAddition(wineId, 1, price, "Bodega Principal", note, true);
        }

        async function handleCellarFormSubmit() {
            const wineId = document.getElementById("cellar-wine-select")?.value;
            const qty = parseInt(document.getElementById("cellar-qty-input")?.value || "1", 10);
            const price = parseFloat(document.getElementById("cellar-price-input")?.value || "0");
            const location = document.getElementById("cellar-location-input")?.value || "Bodega Principal";
            const notes = document.getElementById("cellar-notes-input")?.value || "";
            if (!wineId) return;
            const ok = await postCellarAddition(wineId, Math.max(1, qty), Math.max(0, price), location, notes, true);
            if (ok) {
                const notesEl = document.getElementById("cellar-notes-input");
                if (notesEl) notesEl.value = "";
            }
        }

        async function decrementCellarItem(itemId, quantity) {
            try {
                const res = await fetch(`/api/v1/cellar/${encodeURIComponent(itemId)}?quantity=${quantity}`, {
                    method: "DELETE"
                });
                if (!res.ok) return;
                await loadCellar();
                showToast(quantity > 1 ? "Registro retirado de Mi Bodega" : "1 botella descorchada de Mi Bodega", { variant: "warning" });
            } catch (err) {
                console.error("Error updating cellar:", err);
            }
        }

        window.addEventListener("DOMContentLoaded", init);
    </script>
</body>
</html>"""


def render_dashboard_html(
    wine_count: int = 200,
    region_count: int = 32,
    country_count: int = 4,
) -> str:
    """Render the dashboard HTML with live database KPI counters."""
    return (
        _DASHBOARD_TEMPLATE.replace("__KPI_WINES_COUNT__", str(wine_count))
        .replace("__KPI_REGIONS_COUNT__", str(region_count))
        .replace("__KPI_COUNTRIES_COUNT__", str(country_count))
    )


DASHBOARD_HTML: str = render_dashboard_html()
