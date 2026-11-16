# Vinum Pulse 🍷📡

**Real-Time Sommelier Radar, Dynamic Cartographic Atlas, Gastronomic Pairing Engine, 3-Course Evening Menu Planner, and Cellar Analytics Platform** built with **Python 3.12**, **FastAPI**, **Pydantic v2**, **SQLAlchemy 2.0 / SQLite**, and an interactive Parisian Bistro visual studio.

---

## ✨ Key Capabilities

- **Interactive Visual Sommelier Radar & Cartographic Atlas (`GET /`)**:
  - **"La Carte" 9-Section Collapsible Accordion**: Browse 22 curated Spanish dishes across 9 gastronomic sections (*Entrantes y Cuchara*, *Ensaladas y Huerta*, *Tapas y Pintxos*, *Embutidos y Quesos*, *Pescados y Mariscos*, *Arroces*, *Carnes y Caza*, *Postres y Dulces*, *Platos Vegetarianos y Setas*) with auto-collapse into a compact active dish chip.
  - **Editorial Bottle & Label SVG Visuals + Consumer Tagline**: Dynamic vector bottle silhouettes (*Bordelesa*, *Borgoña*, *Jerezana*, *Espumosa*) with typographic D.O. labels, 1-sentence sensory hooks (`tagline`), and expandable sommelier tasting notes.
  - **Dynamic Cartographic Atlas of Spain**: Interactive map of 12 Denominations of Origin and 36 georeferenced wineries powered by **Leaflet.js** (`CartoDB Positron`) with an automatic **deterministic offline SVG fallback**, interactive *Terroir & Climate* cards, and one-click projection onto the **5-Axis Sensory Radar Chart**.
  - **Interactive 3-Course Evening Sommelier Planner & Printable Menu Card**: Select an occasion (*Cena Romántica*, *Barbacoa con Amigos*, *Comida Familiar de Domingo*, *Tardeo & Tapas Gourmet*), configure a 3-course menu within a target total budget, and receive an optimal light-to-full wine progression, plain-language refrigerator/uncorking tips, vintage peak semaphore, and a `@media print` guest menu sheet.
- **SQLite + SQLAlchemy 2.0 Persistence & REST API Endpoints**:
  - `GET /api/v1/wines`: Query and filter 36 curated wines across 12 premier Spanish appellations.
  - `GET /api/v1/dishes`: Query 22 curated Spanish dishes across 9 culinary categories.
  - `GET /api/v1/regions`: Regional summaries with climate, soil, signature grape, and centroid coordinates.
  - `GET /api/v1/atlas/geojson`: RFC 7946 GeoJSON FeatureCollection for wineries and appellation centroids (`?layer=wineries|regions|all`).
  - `POST /api/v1/pairings/recommend`: Multi-vector Euclidean sensory pairing engine.
  - `POST /api/v1/pairings/menu-plan`: 3-course evening progression planner within a global budget.
  - `GET/POST/DELETE /api/v1/cellar`: Personal cellar inventory management backed by SQLite (`VINUM_DATABASE_URL`).
  - `GET /healthz`: Container and Kubernetes readiness probe.

---

## 🚀 Quick Start

```bash
uv run uvicorn app.main:app --reload --port 8080
```

Open `http://localhost:8080` in your browser to launch the **Vinum Pulse Visual Studio**, or `http://localhost:8080/docs` for the interactive OpenAPI documentation.

---

## 🧪 Quality Gates

```bash
uv run black --check .
uv run isort --check-only --profile black .
uv run ruff check .
uv run mypy app tests
uv run radon cc app/ -a -nb && uv run xenon --max-absolute B --max-modules A --max-average A app/
uv run bandit -c pyproject.toml -r app/ && uv run pip-audit
uv run pytest -v --cov=app --cov-report=term-missing --cov-fail-under=85
```
