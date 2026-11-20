# Vinum Pulse 🍷📡

**European Real-Time Sommelier Radar, Dynamic Cartographic Atlas, Gastronomic Pairing Engine, 3-Course Evening Menu Planner, and Cellar Analytics Platform** built with **Python 3.12**, **FastAPI**, **Pydantic v2**, **SQLAlchemy 2.0 / SQLite**, application-layer perimeter security, and an interactive Parisian Bistro visual studio.

---

## ✨ Key Capabilities

- **European Cartographic Atlas & 200-Wine Multi-Country Catalog (`GET /`)**:
  - **200 Curated Geolocated Wines across 4 Countries & 32 Appellations**:
    - **Spain (65 wines / 12 D.O.s)**: Rioja, Ribera del Duero, Priorat, Rías Baixas, Jerez-Xérès-Sherry, Corpinnat/Penedès, Bierzo, Rueda, Toro, Somontano, Ribeira Sacra, Jumilla.
    - **France (55 wines / 8 AOCs)**: Bordeaux, Bourgogne, Champagne, Vallée du Rhône, Loire, Alsace, Provence, Languedoc.
    - **Italy (55 wines / 8 DOC/DOCGs)**: Piemonte, Toscana, Veneto, Sicilia, Alto Adige, Friuli, Puglia, Campania.
    - **England (25 wines / 4 PDOs)**: Sussex, Kent, Hampshire, Surrey.
  - **Zero-Key Multi-Provider Open-Source Cartography**: Interactive **Leaflet.js** map with European Country Quick-Select pills (`Todos (Europa)`, `España`, `Francia`, `Italia`, `Inglaterra`), dynamic `flyToBounds` camera reframing, OpenStreetMap Editorial + IGN España WMTS switcher, and deterministic offline SVG fallback.
  - **"La Carte" 9-Section Collapsible Accordion (45 European Dishes)**: Browse 45 curated Spanish, French, Italian, and British dishes across 9 gastronomic sections with auto-collapse into a compact active dish chip, Country + Appellation catalog filters, editorial SVG bottle silhouettes, and 1-sentence sensory taglines.
  - **Interactive 3-Course Evening Sommelier Planner & Printable Menu Card**: Optimal light-to-full wine progression within a global budget, plain-language fridge/uncorking tips, vintage peak semaphore, and `@media print` guest menu sheet.
- **Application-Layer Perimeter Security & Serverless Readiness (`app/security.py`, `Dockerfile`)**:
  - **HTTP Security Headers Middleware**: Enforces `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, and `Permissions-Policy`.
  - **Zero-Dependency Token-Bucket Rate Limiter**: Per-IP rate limiting on mutation (`POST`/`DELETE /api/v1/cellar`) and compute (`POST /api/v1/pairings/*`) endpoints returning HTTP `429 Too Many Requests` with `Retry-After`.
  - **Strict Payload Limit**: Enforces `MAX_BODY_BYTES = 32768`, returning HTTP `413 Content Too Large` for oversized payloads.
  - **Cloud-Native Multi-Stage Container**: Non-root `UID 10001`, native `HEALTHCHECK`, configurable `VINUM_DB_PATH` (`/tmp/vinum_pulse.db` default in container for `readOnlyRootFilesystem`), and AWS Lambda Web Adapter (`/opt/extensions/lambda-adapter`).
- **REST API Endpoints**:
  - `GET /api/v1/wines`: Query and filter 200 European wines (`?country=`, `?appellation=`, `?wine_type=`, `?max_price=`, `?q=`, pagination).
  - `GET /api/v1/dishes`: Query 45 curated European dishes across 9 culinary categories.
  - `GET /api/v1/regions`: Regional summaries across 32 appellations (`?country=`).
  - `GET /api/v1/atlas/geojson`: RFC 7946 GeoJSON FeatureCollection (`?layer=wineries|regions|all`, `?country=`).
  - `POST /api/v1/pairings/recommend`: Multi-vector Euclidean sensory pairing engine.
  - `POST /api/v1/pairings/menu-plan`: 3-course evening progression planner within a global budget.
  - `GET/POST/DELETE /api/v1/cellar`: Personal cellar inventory management backed by SQLite (`VINUM_DATABASE_URL` / `VINUM_DB_PATH`).
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
docker build -t vinum-pulse:latest .
```
