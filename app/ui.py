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

    <main class="max-w-5xl mx-auto px-6 sm:px-10 pb-16 space-y-10">
        <!-- Inline Error Banner -->
        <div id="error-banner" role="alert" class="hidden border border-bordeaux/30 bg-butter px-4 py-3 text-bordeaux text-sm flex items-center justify-between gap-4">
            <span id="error-message">No hay vinos disponibles con estos filtros.</span>
            <button type="button" onclick="document.getElementById('error-banner').classList.add('hidden')" class="text-xs font-mono underline underline-offset-4">Cerrar</button>
        </div>

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
        Vinum Pulse · Radar de Cata y Maridaje Sensorial
    </footer>

    <script>
        let allDishes = [];
        let selectedDishId = "chuleton-brasa";
        let preferredType = null;
        let radarChartInstance = null;

        async function init() {
            try {
                const res = await fetch("/api/v1/dishes");
                allDishes = await res.json();
                renderDishes();
                setupEventListeners();
                fetchRecommendation();
            } catch (err) {
                showError("No se pudo cargar la carta de platos.");
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
                            label: 'Vino Recomendado',
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

        window.addEventListener("DOMContentLoaded", init);
    </script>
</body>
</html>"""
