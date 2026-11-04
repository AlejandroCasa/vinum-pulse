# Technical Backlog & Architecture Roadmap — Vinum Pulse

This file tracks prioritized engineering improvements, features, and completed milestones for **Vinum Pulse**.

## 🎯 Prioritized Backlog

### P0 — Kubernetes Deployment & Local Orchestration
- [ ] **[k8s]** Declarative Kubernetes Manifests (`k8s/`): Create `deployment.yaml` and `service.yaml` with hardened `securityContext` (`runAsNonRoot: true`, `UID 10001`, `readOnlyRootFilesystem: true`, probes on `/healthz`) for local `k3s` (Impact: 4/5 | Effort: S)

### P1 — Cellar Analytics & Vintage Aging Simulator
- [ ] **[cellar]** Cellar Valuation & Vintage Peak Window Simulator (`/api/v1/cellar`): Interactive cellar tracker showing bottle aging curves, optimal uncorking windows by vintage, and total cellar valuation charts (Impact: 4/5 | Effort: M)

### P2 — Sommelier Menu Builder & Export
- [ ] **[export]** Interactive Multi-Course Dinner Pairing Card: Generate a visual printable tasting sheet matching starter, main course, and dessert with optimal wine flight progression (Impact: 3/5 | Effort: S)

---

## ✅ Completed Milestones
- [x] **[docker]** Multi-Stage Production Dockerfile: Packaged `vinum-pulse:latest` using `uv` cache mounts, non-root `appuser` (`UID 10001`), `.dockerignore`, and native `HEALTHCHECK` on `/healthz` (`[[ADR-0006-vinum-pulse-docker-multistage-uv]]`) — Branch: `feat/docker-multistage-uv` (`2026-11-04`)
- [x] **[ui/viz]** Interactive Vinum Pulse Visual Dashboard (`GET /`): Built sleek visual web interface with interactive dish selector cards, budget slider, live 5-axis Sensory Radar Chart (Body, Acidity, Tannins, Fruit, Oak), D.O. appellation badges, and serving thermometer visual — Branch: `feat/sommelier-core-api` (`2026-11-01`)
- [x] **[core/api]** Multi-Vector Sensory Engine & FastAPI Endpoints: Implemented `app/schemas.py` (`WineProfile`, `SensoryRadar`, `DishPairingRequest`, `PairingRecommendation`), `app/sommelier.py` with curated D.O. wines and Euclidean sensory similarity algorithm, and endpoints (`GET /api/v1/wines`, `GET /api/v1/dishes`, `POST /api/v1/pairings/recommend`, `GET /api/v1/regions`, `GET /healthz`, and interactive dashboard `GET /`) (`[[ADR-0004-sommelier-vector-pairing-engine]]`) — Branch: `feat/sommelier-core-api` (`2026-11-01`)
- [x] **[core]** Repository scaffolding, `pyproject.toml` with strict QA gates, and Obsidian specification — (`2026-11-01`)
