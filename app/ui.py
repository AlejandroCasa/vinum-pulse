"""UI templates and interactive HTML views for Vinum Pulse."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vinum Pulse — Radar de Cata y Maridaje Sensorial</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .wine-gradient { background: linear-gradient(135deg, #4A0E17 0%, #1A0508 100%); }
        .card-active { border-color: #E11D48; background-color: #2D0B12; }
    </style>
</head>
<body class="bg-stone-950 text-stone-100 min-h-screen font-sans antialiased">
    <!-- Navbar -->
    <header class="border-b border-stone-800 bg-stone-900/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl wine-gradient border border-rose-500/30 flex items-center justify-center text-rose-400 text-xl font-bold shadow-lg shadow-rose-950/50">
                    <i class="fa-solid fa-wine-glass"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                        Vinum Pulse <span class="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-medium">Sommelier Radar v0.1</span>
                    </h1>
                    <p class="text-xs text-stone-400">Inteligencia Enológica & Maridaje Sensorial Multivectorial</p>
                </div>
            </div>
            <div class="flex items-center gap-3 text-xs">
                <span class="px-3 py-1 rounded-full bg-stone-800 border border-stone-700 text-stone-300 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Motor Activo
                </span>
                <span class="px-3 py-1 rounded-full bg-stone-800 border border-stone-700 text-stone-300">
                    <i class="fa-solid fa-layer-group text-rose-400 mr-1"></i> 9 D.O. Españolas
                </span>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8 space-y-8">
        <!-- Hero Section -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
                Maridaje Perfecto sin Jerga Enológica
            </h2>
            <p class="text-stone-400 text-sm sm:text-base">
                Selecciona tu plato gastronómico, ajusta tu presupuesto y visualiza cómo el perfil tánico, ácido y frutal del vino abraza la estructura del plato en un radar sensorial interactivo.
            </p>
        </section>

        <!-- Selector de Platos -->
        <section class="space-y-4">
            <div class="flex justify-between items-center">
                <h3 class="text-lg font-semibold text-stone-200 flex items-center gap-2">
                    <i class="fa-solid fa-utensils text-rose-400"></i> 1. Selecciona tu Plato Gastronómico
                </h3>
                <span class="text-xs text-stone-400" id="dish-counter">Cargando platos...</span>
            </div>
            <div id="dish-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Platos inyectados vía JS -->
            </div>
        </section>

        <!-- Filtros y Presupuesto -->
        <section class="bg-stone-900 border border-stone-800 rounded-2xl p-6 shadow-xl space-y-6">
            <h3 class="text-lg font-semibold text-stone-200 flex items-center gap-2">
                <i class="fa-solid fa-sliders text-rose-400"></i> 2. Ajustes de Maridaje & Presupuesto
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                <!-- Presupuesto -->
                <div class="space-y-3">
                    <div class="flex justify-between items-center">
                        <label for="budget-slider" class="text-sm font-medium text-stone-300">Presupuesto Máximo por Botella</label>
                        <span id="budget-value" class="text-xl font-bold text-rose-400">50 €</span>
                    </div>
                    <input id="budget-slider" type="range" min="15" max="80" step="5" value="50"
                           class="w-full h-2 bg-stone-700 rounded-lg appearance-none cursor-pointer accent-rose-500">
                    <div class="flex justify-between text-xs text-stone-500">
                        <span>15 € (Accesible)</span>
                        <span>45 € (Premium)</span>
                        <span>80 € (Colección)</span>
                    </div>
                </div>

                <!-- Tipo de Vino -->
                <div class="space-y-3">
                    <label class="text-sm font-medium text-stone-300">Preferencia Enológica</label>
                    <div class="grid grid-cols-3 sm:grid-cols-5 gap-2" id="type-selector">
                        <button type="button" data-type="" class="type-btn px-3 py-2 rounded-xl text-xs font-semibold border border-rose-500 bg-rose-500/20 text-rose-300 text-center transition">Todos</button>
                        <button type="button" data-type="Red" class="type-btn px-3 py-2 rounded-xl text-xs font-semibold border border-stone-700 bg-stone-800 text-stone-300 text-center hover:border-stone-600 transition">Tinto</button>
                        <button type="button" data-type="White" class="type-btn px-3 py-2 rounded-xl text-xs font-semibold border border-stone-700 bg-stone-800 text-stone-300 text-center hover:border-stone-600 transition">Blanco</button>
                        <button type="button" data-type="Sparkling" class="type-btn px-3 py-2 rounded-xl text-xs font-semibold border border-stone-700 bg-stone-800 text-stone-300 text-center hover:border-stone-600 transition">Espumoso</button>
                        <button type="button" data-type="Fortified" class="type-btn px-3 py-2 rounded-xl text-xs font-semibold border border-stone-700 bg-stone-800 text-stone-300 text-center hover:border-stone-600 transition">Generoso</button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Resultados: Vino Recomendado + Gráfico Radar -->
        <section id="results-section" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Ficha Enológica Recomendada (7 cols) -->
            <div class="lg:col-span-7 bg-stone-900 border border-stone-800 rounded-2xl p-6 shadow-xl space-y-6">
                <div class="flex flex-wrap justify-between items-start gap-4 border-b border-stone-800 pb-4">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span id="res-appellation" class="px-2.5 py-1 rounded-md text-xs font-bold uppercase tracking-wider bg-rose-950 text-rose-400 border border-rose-800">D.O.Ca. Rioja</span>
                            <span id="res-vintage" class="text-xs text-stone-400 font-mono">Añada 2017</span>
                        </div>
                        <h4 id="res-name" class="text-2xl font-bold text-white tracking-tight">Viña Ardanza Reserva</h4>
                        <p id="res-winery" class="text-sm text-stone-400">La Rioja Alta, S.A.</p>
                    </div>
                    <div class="text-right">
                        <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 font-bold text-sm">
                            <i class="fa-solid fa-circle-check"></i> <span id="res-score">96.5%</span> Afinidad
                        </div>
                        <div class="text-xl font-extrabold text-stone-100 mt-2" id="res-price">34.00 €</div>
                    </div>
                </div>

                <!-- Termómetro de Servicio & Cristalería -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 bg-stone-950/60 border border-stone-800/80 rounded-xl p-4">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 text-lg">
                            <i class="fa-solid fa-temperature-half"></i>
                        </div>
                        <div>
                            <div class="text-[11px] text-stone-400 uppercase tracking-wide">Temp. Servicio</div>
                            <div class="text-sm font-bold text-white" id="res-temp">17 °C</div>
                        </div>
                    </div>
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 text-lg">
                            <i class="fa-solid fa-hourglass-half"></i>
                        </div>
                        <div>
                            <div class="text-[11px] text-stone-400 uppercase tracking-wide">Decantación</div>
                            <div class="text-sm font-bold text-white" id="res-decant">30 min</div>
                        </div>
                    </div>
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 text-lg">
                            <i class="fa-solid fa-wine-glass-empty"></i>
                        </div>
                        <div>
                            <div class="text-[11px] text-stone-400 uppercase tracking-wide">Copa Óptima</div>
                            <div class="text-sm font-bold text-white" id="res-glass">Burdeos</div>
                        </div>
                    </div>
                </div>

                <!-- Explicación del Sommelier -->
                <div class="space-y-2">
                    <div class="text-xs uppercase tracking-wider text-rose-400 font-bold flex items-center gap-1.5">
                        <i class="fa-solid fa-comment-dots"></i> Veredicto del Sommelier
                    </div>
                    <p id="res-explanation" class="text-sm text-stone-300 leading-relaxed bg-stone-950/40 p-4 rounded-xl border border-stone-800/60">
                        Cargando análisis sensorial...
                    </p>
                </div>

                <!-- Notas de Cata -->
                <div class="space-y-2">
                    <div class="text-xs uppercase tracking-wider text-stone-400 font-bold">Notas de Cata</div>
                    <p id="res-notes" class="text-xs text-stone-400 italic">
                        Cargando descriptores organolépticos...
                    </p>
                </div>

                <!-- Alternativas -->
                <div class="space-y-3 pt-2 border-t border-stone-800">
                    <div class="text-xs uppercase tracking-wider text-stone-400 font-bold">Alternativas en Bodega</div>
                    <div id="res-alternatives" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <!-- Alternativas vía JS -->
                    </div>
                </div>
            </div>

            <!-- Radar Sensorial de 5 Ejes (5 cols) -->
            <div class="lg:col-span-5 bg-stone-900 border border-stone-800 rounded-2xl p-6 shadow-xl space-y-4">
                <div class="flex justify-between items-center border-b border-stone-800 pb-3">
                    <h4 class="text-base font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-chart-radar text-rose-400"></i> Radar Sensorial (5 Ejes)
                    </h4>
                    <span class="text-xs font-mono text-stone-400">Escala 1–10</span>
                </div>
                <div class="relative w-full aspect-square max-w-sm mx-auto">
                    <canvas id="radarChart"></canvas>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs pt-2">
                    <div class="flex items-center gap-2 p-2 rounded-lg bg-stone-950 border border-stone-800">
                        <span class="w-3 h-3 rounded-full bg-rose-500"></span>
                        <span class="text-stone-300 font-medium">Vino Recomendado</span>
                    </div>
                    <div class="flex items-center gap-2 p-2 rounded-lg bg-stone-950 border border-stone-800">
                        <span class="w-3 h-3 rounded-full bg-amber-400"></span>
                        <span class="text-stone-300 font-medium">Demanda del Plato</span>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-stone-800 mt-16 py-8 text-center text-xs text-stone-500 space-y-2">
        <p>Vinum Pulse &copy; 2026 — Plataforma de Arquitectura Limpia en FastAPI, Pydantic v2 y Python 3.12</p>
        <p class="text-stone-600">Gobernanza CTO & Calidad de Código Certificada</p>
    </footer>

    <script>
        let allDishes = [];
        let selectedDishId = "chuleton-brasa";
        let preferredType = null;
        let radarChartInstance = null;

        const dishIcons = {
            "chuleton-brasa": "fa-drumstick-bite",
            "pulpo-feira": "fa-shrimp",
            "arroz-bogavante": "fa-bowl-rice",
            "jamon-bellota": "fa-bacon",
            "queso-manchego": "fa-cheese",
            "cochinillo-asado": "fa-fire"
        };

        async function init() {
            try {
                const res = await fetch("/api/v1/dishes");
                allDishes = await res.json();
                renderDishes();
                setupEventListeners();
                fetchRecommendation();
            } catch (err) {
                console.error("Error al inicializar:", err);
            }
        }

        function renderDishes() {
            const grid = document.getElementById("dish-grid");
            document.getElementById("dish-counter").textContent = `${allDishes.length} platos disponibles`;
            grid.innerHTML = allDishes.map(dish => {
                const isActive = dish.id === selectedDishId;
                const icon = dishIcons[dish.id] || "fa-utensils";
                return `
                    <div data-dish-id="${dish.id}" class="dish-card cursor-pointer p-4 rounded-xl border transition-all ${isActive ? 'card-active border-rose-500 shadow-lg shadow-rose-950/40' : 'border-stone-800 bg-stone-900/60 hover:border-stone-700'}">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs px-2 py-0.5 rounded-full bg-stone-800 text-stone-400 font-medium">${dish.category}</span>
                            <i class="fa-solid ${icon} text-rose-400 text-lg"></i>
                        </div>
                        <h4 class="text-sm font-bold text-white mb-1">${dish.name}</h4>
                        <p class="text-xs text-stone-400 line-clamp-2">${dish.description}</p>
                    </div>
                `;
            }).join("");

            document.querySelectorAll(".dish-card").forEach(el => {
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

            document.querySelectorAll(".type-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    document.querySelectorAll(".type-btn").forEach(b => {
                        b.classList.remove("border-rose-500", "bg-rose-500/20", "text-rose-300");
                        b.classList.add("border-stone-700", "bg-stone-800", "text-stone-300");
                    });
                    btn.classList.add("border-rose-500", "bg-rose-500/20", "text-rose-300");
                    btn.classList.remove("border-stone-700", "bg-stone-800", "text-stone-300");
                    preferredType = btn.getAttribute("data-type") || null;
                    fetchRecommendation();
                });
            });
        }

        async function fetchRecommendation() {
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
                    alert(err.detail || "Error en la recomendación");
                    return;
                }
                const data = await res.json();
                updateUI(data);
            } catch (err) {
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
            document.getElementById("res-decant").textContent = wine.decant_minutes > 0 ? `${wine.decant_minutes} min` : "No requerida";
            document.getElementById("res-glass").textContent = wine.glass_type;
            document.getElementById("res-explanation").textContent = rec.sommelier_explanation;
            document.getElementById("res-notes").textContent = `"${wine.tasting_notes}"`;

            // Alternativas
            const altGrid = document.getElementById("res-alternatives");
            if (rec.alternative_wines && rec.alternative_wines.length > 0) {
                altGrid.innerHTML = rec.alternative_wines.map(alt => `
                    <div class="p-3 rounded-xl bg-stone-950/80 border border-stone-800 flex justify-between items-center text-xs">
                        <div>
                            <div class="font-bold text-white">${alt.name}</div>
                            <div class="text-stone-400 text-[11px]">${alt.appellation} (${alt.wine_type})</div>
                        </div>
                        <div class="text-stone-300 font-mono font-bold">${alt.price_eur.toFixed(2)} €</div>
                    </div>
                `).join("");
            } else {
                altGrid.innerHTML = `<div class="col-span-2 text-xs text-stone-500 italic">No hay alternativas adicionales bajo este presupuesto.</div>`;
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
                            backgroundColor: 'rgba(244, 63, 94, 0.25)',
                            borderColor: '#F43F5E',
                            pointBackgroundColor: '#F43F5E',
                            pointBorderColor: '#fff',
                            borderWidth: 2
                        },
                        {
                            label: 'Demanda del Plato',
                            data: targetData,
                            backgroundColor: 'rgba(251, 191, 36, 0.2)',
                            borderColor: '#FBBF24',
                            pointBackgroundColor: '#FBBF24',
                            pointBorderColor: '#fff',
                            borderWidth: 2,
                            borderDash: [4, 4]
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            pointLabels: {
                                color: '#D6D3D1',
                                font: { size: 11, weight: 'bold' }
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