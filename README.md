# Vinum Pulse 🍷📡

**Real-Time Sommelier Radar, Gastronomic Pairing Engine, and Cellar Analytics Platform** built with **Python 3.12**, **FastAPI**, **Pydantic v2**, and an interactive visual analytics UI.

**Vinum Pulse** combines a multi-vector sensory pairing engine on the backend with an intuitive, zero-jargon interactive dashboard featuring **5-Axis Sensory Radar Charts**, **Appellation (D.O.) Intelligence**, **Serving Temperature & Decanting Gauges**, and **Cellar Aging Curves**.

---

## ✨ Key Capabilities

- **Interactive Visual Sommelier Radar (`GET /`)**:
  - Select gastronomic dishes (*Chuletón a la brasa*, *Pulpo a feira*, *Arroz con bogavante*, *Jamón Ibérico de Bellota*, *Queso Manchego Curado*, *Cochinillo asado*), tune budget sliders (`10 € – 80 €`), and visualize real-time pairing scores.
  - **5-Axis Sensory Radar Chart**: Overlays the dish's target sensory vector against the recommended wine across *Body*, *Acidity*, *Tannins*, *Fruit Intensity*, and *Oak Aging*.
  - **Thermodynamics & Serving Telemetry**: Visual thermometer (`°C`), decanting oxygenation timer, and stemware geometry guide.
- **REST API Endpoints**:
  - `GET /api/v1/wines`: Query and filter curated wines across premier Iberian appellations (*Rioja*, *Ribera del Duero*, *Priorat*, *Rías Baixas*, *Jerez*, *Toro*, *Bierzo*, *Rueda*).
  - `POST /api/v1/pairings/recommend`: Vector-distance sommelier engine returning compatibility scores (`0–100%`) and sensory harmony breakdowns.
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
uv run ruff check .
uv run ruff format --check .
uv run mypy app tests
uv run pytest -v --cov=app --cov-report=term-missing --cov-fail-under=85
```
