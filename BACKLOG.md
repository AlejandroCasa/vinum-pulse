# Technical Backlog & Architecture Roadmap — Vinum Pulse

This file tracks prioritized engineering improvements, features, and completed milestones for **Vinum Pulse**.

## 🎯 Prioritized Backlog (Sprint 2026-W46)

### P0 — Database Persistence & Dynamic Geo-Map
- [ ] **[database]** SQLite Persistence Engine & Expanded Enological Seed (`app/database.py` + `app/models.py`): Migrate static arrays to persistent SQLite database (via `SQLAlchemy 2.0` / `SQLModel`) seeded with **35+ authentic Spanish wines across 12 D.O. regions**, geolocated wineries (`lat`, `lon`), terroir/soil/altitude profiles, regional dishes, and persistent **"Mi Bodega Personal" (`CRUD /api/v1/cellar`)** (Impact: 5/5 | Effort: M)
- [ ] **[dynamic-map]** Interactive Cartographic Atlas of Spanish Wine Regions & Wineries (`GET /` + Leaflet.js / GeoJSON): Build an interactive map of Spain displaying D.O. zones and winery markers; clicking a region or winery reveals its Terroir Card (climate, soil, altitude, signature grape) and dynamically filters the catalog and 5D Sensory Radar (Impact: 5/5 | Effort: M)

### P1 — Flagship Non-Technical User Experience & Sommelier Planner
- [ ] **[event-planner]** Interactive Evening & 3-Course Menu Sommelier Planner (`POST /api/v1/pairings/menu-plan`): Let any user select an occasion (*Cena Romántica*, *Barbacoa con Amigos*, *Comida Familiar*, *Tapas Gourmet*) and a 3-course menu (*Entrante + Principal + Postre/Queso*) within a target budget. Automatically compute optimal wine serving progression (light-to-full structure), plain-language serving tips (*"45 min in fridge before serving"*, *"Uncork 30 min early"*), vintage peak status semaphore, and a **Printable Sommelier Menu Card** for guests (Impact: 5/5 | Effort: M)

### P2 — Kubernetes Orchestration & Weighted Algorithms
- [ ] **[k8s]** Declarative Kubernetes Manifests (`k8s/`): Create `deployment.yaml` and `service.yaml` with hardened `securityContext` (`runAsNonRoot: true`, `UID 10001`, `readOnlyRootFilesystem: true`, probes on `/healthz`) for local `k3s` (Impact: 4/5 | Effort: S)

---

## ✅ Completed Milestones
- [x] **[cicd/qa]** Full CI/CD & Quality Gate Suite: Integrated `black`, `isort`, `ruff`, `mypy` (strict), `bandit` (SAST), `pip-audit` (SCA), `radon` & `xenon` (complexity rank `A`), and `pytest-cov` (`>=85%`) with modular UI decoupling (`app/ui.py`) and automated GitHub Actions pipeline (`.github/workflows/ci.yml`) (`[[ADR-0010-vinum-pulse-cicd-devsecops-suite]]`) — Branch: `feat/cicd-devsecops-pipeline` (`2026-11-08`)
- [x] **[docker]** Multi-Stage Production Dockerfile: Packaged `vinum-pulse:latest` using `uv` cache mounts, non-root `appuser` (`UID 10001`), `.dockerignore`, and native `HEALTHCHECK` on `/healthz` (`[[ADR-0006-vinum-pulse-docker-multistage-uv]]`) — Branch: `feat/docker-multistage-uv` (`2026-11-04`)
- [x] **[ui/viz]** Interactive Vinum Pulse Visual Dashboard (`GET /`): Built sleek visual web interface with interactive dish selector cards, budget slider, live 5-axis Sensory Radar Chart (Body, Acidity, Tannins, Fruit, Oak), D.O. appellation badges, and serving thermometer visual — Branch: `feat/sommelier-core-api` (`2026-11-01`)
- [x] **[core/api]** Multi-Vector Sensory Engine & FastAPI Endpoints: Implemented `app/schemas.py` (`WineProfile`, `SensoryRadar`, `DishPairingRequest`, `PairingRecommendation`), `app/sommelier.py` with curated D.O. wines and Euclidean sensory similarity algorithm, and endpoints (`GET /api/v1/wines`, `GET /api/v1/dishes`, `POST /api/v1/pairings/recommend`, `GET /api/v1/regions`, `GET /healthz`, and interactive dashboard `GET /`) (`[[ADR-0004-sommelier-vector-pairing-engine]]`) — Branch: `feat/sommelier-core-api` (`2026-11-01`)
- [x] **[core]** Repository scaffolding, `pyproject.toml` with strict QA gates, and Obsidian specification — (`2026-11-01`)
