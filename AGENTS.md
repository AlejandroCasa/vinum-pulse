# Vinum Pulse — Repository Engineering Rules

Inherits global CTO governance from `C:/Users/acasa/.gemini/config/AGENTS.md` and `c:/Workspace/AGENTS.md`.

## 1. Repository Architecture & Scope
- **Service**: **Vinum Pulse** — Real-Time Sommelier Radar, Gastronomic Pairing Engine, and Cellar Analytics Platform (`FastAPI` + `Pydantic v2` + interactive visual HTML5/Tailwind/Chart.js frontend served at `/`).
- **Audience & Product Goal**: Deliver an immediately intuitive, visually striking interactive web experience (5-axis sensory radar charts, appellation explorer, serving temperature gauges, and instant dish-to-wine pairing simulator) backed by 100% strict Python 3.12 engineering standards.
- **Source Layout**:
  - `app/schemas.py`: Pydantic v2 data contracts (`WineProfile`, `SensoryRadar`, `DishPairingRequest`, `PairingRecommendation`, `CellarBottle`).
  - `app/sommelier.py`: Deterministic multi-vector sensory pairing engine and curated appellation catalog (*Rioja*, *Ribera del Duero*, *Priorat*, *Rías Baixas*, *Jerez*, *Toro*, *Bierzo*, *Rueda*).
  - `app/main.py`: FastAPI REST endpoints (`GET /api/v1/wines`, `POST /api/v1/pairings/recommend`, `GET /api/v1/regions`, `GET /healthz`) and interactive visual dashboard (`GET /`).
  - `tests/`: Comprehensive integration test suite (`pytest` + `httpx`).

## 2. Verified Execution Commands (WSL 2 Ubuntu)
Always execute from `c:/Workspace/vinum-pulse` via `wsl bash -lc`:
- **Sync / Lock Dependencies**: `wsl bash -lc "uv lock && uv sync"`
- **Linter & Formatter**: `wsl bash -lc "uv run ruff check . && uv run ruff format --check ."`
- **Static Type Check**: `wsl bash -lc "uv run mypy app tests"`
- **Test Suite & Coverage (`>= 85%`, `0` warnings)**: `wsl bash -lc "uv run pytest -v --cov=app --cov-report=term-missing --cov-fail-under=85"`
- **Container Build**: `wsl bash -lc "docker build -t vinum-pulse:latest ."`

## 3. Obsidian Knowledge Links
- **Project Hub**: `c:/Workspace/docs/Proyectos/Vinum-Pulse.md` (`[[Vinum-Pulse]]`)
- **Functional Spec**: `c:/Workspace/docs/Proyectos/Vinum-Pulse-Spec.md` (`[[Vinum-Pulse-Spec]]`)
