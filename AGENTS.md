# Vinum Pulse — Repository Engineering Rules

Inherits global CTO governance from `c:/Workspace/AGENTS.md`.

## 1. Repository Architecture & Scope
- **Service**: **Vinum Pulse** — Real-Time Sommelier Radar, Dynamic Geo-Atlas, Gastronomic Pairing Engine, Evening Menu Planner, and Cellar Analytics Platform (`FastAPI` + `Pydantic v2` + `SQLite/SQLAlchemy` + interactive HTML5/Tailwind/Chart.js/Leaflet.js frontend served at `/`).
- **Audience & Product Goal**: Deliver an immediately intuitive, visually striking interactive web experience for non-technical users (interactive map of Spanish wine regions/wineries, 5-axis sensory radar charts, 3-course evening sommelier planner with printable tasting cards, and persistent personal cellar) backed by 100% strict Python 3.12 engineering standards.
- **Source Layout**:
  - `app/database.py` & `app/models.py`: SQLite persistence engine (`SQLAlchemy 2.0` / `SQLModel`) and seeded Spanish D.O. catalog (+35 wines, 12 geolocated regions, dishes, and `cellar_items`).
  - `app/schemas.py`: Pydantic v2 data contracts (`WineProfile`, `SensoryRadar`, `DishPairingRequest`, `PairingRecommendation`, `EveningMenuRequest`, `EveningMenuPlan`, `CellarBottle`).
  - `app/sommelier.py` & `app/planner.py`: Deterministic multi-vector sensory pairing engine, vintage peak window calculator, and 3-course evening progression planner.
  - `app/main.py`: FastAPI REST endpoints (`GET /api/v1/wines`, `GET /api/v1/regions`, `GET /api/v1/dishes`, `POST /api/v1/pairings/recommend`, `POST /api/v1/pairings/menu-plan`, `CRUD /api/v1/cellar`, `GET /healthz`) and interactive visual dashboard (`GET /`).
  - `tests/`: Comprehensive integration and unit test suite (`pytest` + `httpx`).

## 2. Mandatory Quality Gates & CI/CD Standard (WSL 2 Ubuntu & `.github/workflows/ci.yml`)
Always execute from `c:/Workspace/vinum-pulse` via `wsl bash -lc`:
1. **Sync / Lock Dependencies**: `wsl bash -lc "uv lock && uv sync"`
2. **Formatting, Import Sorting & Linting (`black` + `isort` + `ruff`)**:
   `wsl bash -lc "uv run black --check . && uv run isort --check-only --profile black . && uv run ruff check ."`
3. **Static Type Check (`mypy --strict`)**:
   `wsl bash -lc "uv run mypy app tests"`
4. **Code Complexity & Maintainability (`radon` + `xenon`)**:
   `wsl bash -lc "uv run radon cc app/ -a -nb && uv run xenon --max-absolute B --max-modules A --max-average A app/"`
5. **Security SAST & Dependency Audit (`bandit` + `pip-audit`)**:
   `wsl bash -lc "uv run bandit -c pyproject.toml -r app/ && uv run pip-audit"`
6. **Test Suite & Coverage (`>= 85%`, `0` warnings)**:
   `wsl bash -lc "uv run pytest -v --cov=app --cov-report=term-missing --cov-fail-under=85"`
7. **Container Build**:
   `wsl bash -lc "docker build -t vinum-pulse:latest ."`

## 3. Obsidian Knowledge Links
- **Project Hub**: `c:/Workspace/docs/Proyectos/Vinum-Pulse.md` (`[[Vinum-Pulse]]`)
- **Functional Spec**: `c:/Workspace/docs/Proyectos/Vinum-Pulse-Spec.md` (`[[Vinum-Pulse-Spec]]`)
