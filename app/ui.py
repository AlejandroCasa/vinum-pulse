"""UI templates and interactive HTML views for Vinum Pulse."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vinum Pulse — Radar de Cata y Maridaje Sensorial</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
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
    </style>
</head>
<body class="min-h-screen font-sans antialiased text-espresso">
    <!-- Parisian Bistro Masthead -->
    <header class="max-w-5xl mx-auto px-6 sm:px-10 pt-10 pb-6 text-center space-y-2">
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
        <div id="error-banner" role="alert" class="hidden border border-bordeaux/30 bg-butter px-4 py-3 text-bordeaux text-sm flex items-center justify-between gap-4">
            <span id="error-message">No hay vinos disponibles con estos filtros.</span>
            <button type="button" onclick="document.getElementById('error-banner').classList.add('hidden')" class="text-xs font-mono underline underline-offset-4">Cerrar</button>
        </div>

        <!-- Atlas Cartográfico de Terroirs & Bodegas D.O. -->
        <section id="atlas-section" class="border-t border-espresso/15 pt-8 space-y-6">
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

                    <button type="button" id="btn-sync-radar" class="w-full py-2.5 px-4 bg-bordeaux text-cream text-xs font-mono uppercase tracking-wider rounded hover:bg-bordeaux/90 transition shadow-xs">
                        Proyectar Perfil en Radar 5D
                    </button>
                </aside>
            </div>
        </section>

        <!-- Menu Sheet Layout -->
        <div class="menu-frame py-10 grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-start">
            <!-- Left: La Carte & Cellar Preferences (5 cols) -->
            <aside class="lg:col-span-5 space-y-10">
                <section class="space-y-4">
                    <div class="flex justify-between items-baseline border-b border-espresso/15 pb-2.5">
                        <h2 class="font-serif text-2xl text-espresso">La Carte</h2>
                        <span id="dish-counter" class="text-xs font-serif italic text-walnut">Cargando carta...</span>
                    </div>
                    <div id="dish-grid" class="divide-y divide-espresso/10">
                        <!-- Dishes rendered via JS -->
                    </div>
                </section>

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

                <!-- Tasting Quote & Radar -->
                <div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
                    <div class="md:col-span-6 space-y-5">
                        <p id="res-explanation" class="text-sm text-espresso/90 leading-relaxed">
                            Cargando análisis sensorial...
                        </p>
                        <blockquote class="border-l border-bordeaux/50 pl-4">
                            <p id="res-notes" class="font-serif italic text-xl text-walnut leading-snug">
                                Cargando descriptores...
                            </p>
                        </blockquote>
                    </div>

                    <div class="md:col-span-6 space-y-2">
                        <div class="relative w-full aspect-square max-w-[260px] mx-auto">
                            <canvas id="radarChart"></canvas>
                        </div>
                        <div class="flex justify-center gap-5 text-[11px] font-mono text-walnut">
                            <span class="flex items-center gap-1.5">
                                <span class="w-2 h-2 rounded-full bg-bordeaux"></span> Vino
                            </span>
                            <span class="flex items-center gap-1.5">
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
    </main>

    <footer class="max-w-5xl mx-auto px-6 sm:px-10 pb-10 text-center text-xs font-serif italic text-walnut">
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

        async function init() {
            try {
                const resDishes = await fetch("/api/v1/dishes");
                allDishes = await resDishes.json();
                renderDishes();
                setupEventListeners();
                fetchRecommendation();
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

        function renderDishes() {
            const grid = document.getElementById("dish-grid");
            document.getElementById("dish-counter").textContent = `${allDishes.length} platos`;
            grid.innerHTML = allDishes.map(dish => {
                const isActive = dish.id === selectedDishId;
                return `
                    <button type="button" data-dish-id="${dish.id}" class="dish-row w-full text-left py-3 pr-2 rounded-sm ${isActive ? 'is-active' : ''}">
                        <div class="flex items-baseline justify-between gap-2">
                            <span class="font-serif text-xl text-espresso ${isActive ? 'text-bordeaux' : ''}">${dish.name}</span>
                            <span class="text-[11px] font-mono text-walnut shrink-0">${dish.category}</span>
                        </div>
                        <p class="text-xs text-walnut line-clamp-1 mt-0.5">${dish.description}</p>
                    </button>
                `;
            }).join("");

            document.querySelectorAll(".dish-row").forEach(el => {
                el.addEventListener("click", () => {
                    selectedDishId = el.getAttribute("data-dish-id");
                    renderDishes();
                    fetchRecommendation();
                });
            });
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

            const btnSync = document.getElementById("btn-sync-radar");
            if (btnSync) {
                btnSync.addEventListener("click", () => {
                    if (activeAtlasFeature) {
                        applyAtlasWineToRadar(activeAtlasFeature);
                        document.getElementById("results-section").scrollIntoView({ behavior: "smooth" });
                    }
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
            document.getElementById("res-explanation").textContent = rec.sommelier_explanation;
            document.getElementById("res-notes").textContent = `«${wine.tasting_notes}»`;

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

                // Select default first feature
                if (atlasFeatures.length > 0) {
                    selectAtlasFeature(atlasFeatures[0]);
                }

                // Check Leaflet availability
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

            // If a specific D.O. is selected, focus its first winery
            const matching = doName ? atlasFeatures.filter(f => f.properties.appellation === doName) : atlasFeatures;
            if (matching.length > 0) {
                selectAtlasFeature(matching[0]);
            }

            // Update Leaflet map view & markers
            if (leafletMap) {
                if (doName && matching.length > 0) {
                    const first = matching[0];
                    leafletMap.setView([first.geometry.coordinates[1], first.geometry.coordinates[0]], 8, { animate: true });
                } else {
                    leafletMap.setView([40.2, -3.7], 6, { animate: true });
                }
            }

            // Update SVG fallback markers
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

            // Populate wineries list for this D.O.
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
            document.getElementById("res-explanation").textContent = `Selección directa desde el Atlas de Terroirs: ${p.winery_catalog_summary}`;
            document.getElementById("res-notes").textContent = `«${p.tasting_notes}»`;

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

            // Build deterministic SVG canvas for Spain
            // Lon range: [-9.5, 3.5] -> width 680
            // Lat range: [36.0, 44.0] -> height 360
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
                    <!-- Regional Reference Lines -->
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

        window.addEventListener("DOMContentLoaded", init);
    </script>
</body>
</html>"""
