# Technical Backlog & Architecture Roadmap — Vinum Pulse

This file tracks prioritized engineering improvements, features, and completed milestones for **Vinum Pulse**.

## 🎯 Prioritized Backlog

### P0 — Core Sensory Pairing Engine & Interactive Visual Dashboard (MVP)
- [ ] **[ui/viz]** Interactive Vinum Pulse Visual Dashboard (`GET /`): Build a sleek, zero-jargon visual web interface with interactive dish selector cards, budget slider, live 5-axis Sensory Radar Chart (Body, Acidity, Tannins, Fruit, Oak), D.O. appellation badges, and serving thermometer visual (Impact: 5/5 | Effort: M)
- [ ] **[docker]** Multi-Stage Production Dockerfile: Package `vinum-pulse:latest` using `uv` cache mounts, non-root `appuser` (`UID 10001`), and native `HEALTHCHECK` on `/healthz` (Impact: 4/5 | Effort: S)

### P1 — Cellar Analytics & Vintage Aging Simulator
- [ ] **[cellar]** Cellar Valuation & Vintage Peak Window Simulator (`/api/v1/cellar`): Interactive cellar tracker showing bottle aging curves, optimal uncorking windows by vintage, and total cellar valuation charts (Impact: 4/5 | Effort: M)

### P2 — Sommelier Menu Builder & Export
- [ ] **[export]** Interactive Multi-Course Dinner Pairing Card: Generate a visual printable tasting sheet matching starter, main course, and dessert with optimal wine flight progression (Impact: 3/5 | Effort: S)

---

## ✅ Completed Milestones
- [x] **[core/api]** Multi-Vector Sensory Engine & FastAPI Endpoints: Implemented `app/schemas.py` (`WineProfile`, `SensoryRadar`, `DishPairingRequest`, `PairingRecommendation`), `app/sommelier.py` with curated D.O. wines and Euclidean sensory similarity algorithm, and endpoints (`GET /api/v1/wines`, `GET /api/v1/dishes`, `POST /api/v1/pairings/recommend`, `GET /api/v1/regions`, `GET /healthz`, and interactive dashboard `GET /`) (`[[ADR-0004-sommelier-vector-pairing-engine]]`) — Branch: `feat/sommelier-core-api` (`2026-11-01`)
- [x] **[core]** Repository scaffolding, `pyproject.toml` with strict QA gates, and Obsidian specification — (`2026-11-01`)
