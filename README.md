# WeatherNow

**Hyper-Local Severe Weather Intelligence** — a Smart India Hackathon demonstration prototype for visualizing a simulated 2–6 hour severe-weather nowcasting workflow.

> **Prototype notice:** WeatherNow currently uses deterministic simulated inputs and transparent demo scoring rules. It is not an operational warning service, does not use live INSAT/IMDAA/QPE data, and does not provide official forecasts or scientifically validated predictions.

## Overview

WeatherNow demonstrates data fusion through alert generation: scenario inputs → feature normalization → multi-hazard risk scoring → illustrative risk grid → event selection → feature-contribution explanation → terrain/impact context → threshold-based alerts.

## Features

- Responsive operational dashboard with stylized interactive India overview and clickable simulated risk grid.
- Layer selection for thunderstorm, cloudburst, flash flood, rainfall, moisture, wind, and elevation concepts. Layers show scenario values on illustrative geography, not official boundaries.
- Six-hour deterministic forecast trend, event list, indicator bars, impact context, and transparent explanation.
- Event filtering, supported-region search, alert acknowledgement, historical replay, AI architecture, and provider/service status.
- Run demonstration action, pipeline sequence, local inference API call when reachable, and graceful UI fallback.
- FastAPI API with health, events, forecast, risk map, alerts, insights, system status, and inference endpoints.
- Demo/future provider interfaces, feature normalization, model contract, prototype risk rules, and alert thresholds.

## Architecture

```text
frontend/                         React + TypeScript + Vite dashboard
  src/pages/App.tsx               Navigation and operational workflows
  src/data/demo.ts                Coherent simulated scenarios
  src/services/api.ts             API client and fallback
  src/types/                      Shared UI domain types
  src/styles.css                  Dark meteorological design system
backend/app/
  main.py                         FastAPI endpoints and validation
  ml/model_interface.py           Replaceable model contract
  ml/demo_model.py                Deterministic prototype scoring
  ml/feature_pipeline.py          Feature aliases and normalization
  ml/inference_service.py         Inference service
  services/providers.py           Demo and future provider interfaces
  services/alerts.py              Configurable thresholds
data/demo/                        Reserved for versioned scenario data
data/schemas/                     Reserved for provider/model contracts
docs/                             Integration notes and limitations
models/                           Reserved for trained weights
```

## Technology stack

- Frontend: React, TypeScript, Vite, Lucide, Recharts.
- Map: responsive custom SVG map and demo grid; no tile service dependency. MapLibre is included as an optional dependency for a future tile-backed map.
- Backend: Python 3.10+, FastAPI, Pydantic, Uvicorn.
- Persistence: in-memory demonstration fixtures; no database setup required.

## Installation

Requirements: Node.js 20+ with npm; Python 3.10+ with pip.

### Run the frontend

From the repository root:

```powershell
npm install
npm run dev
```

Open [http://localhost:5174](http://localhost:5174). Without an API connection, the UI uses its bundled labeled demo data.

### Run the backend

In a second terminal, from the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs). Set `VITE_API_URL` before starting Vite to use another API origin (default in local development: `http://localhost:8000/api`).

### Demo mode

No account is required. Click **Run demonstration** for ingestion, alignment, feature extraction, inference, risk, impact, and alert sequence. Select an event, click a map cell, change forecast hour, switch atmosphere/impact or layers, open **Why this prediction?**, and inspect **Alerts**. With the API online, the action submits a sample to `/api/inference/run`.

## Publish with GitHub, Netlify, and Render

Netlify hosts the React/Vite website. The Python FastAPI service runs separately on Render; a static Netlify site cannot run this Python API process. Both deployment configuration files are included in this repository.

### 1. Upload the project to GitHub

Copy the project files to your GitHub repository folder, keeping the repository root layout intact. Include `frontend/`, `backend/`, `data/`, `docs/`, `models/`, `package.json`, `package-lock.json`, `index.html`, `vite.config.ts`, `netlify.toml`, and `render.yaml`. Do not upload `node_modules/`, `dist/`, `.venv/`, `.uv-cache/`, or `.env`.

From PowerShell in the repository folder, review and push the files:

```powershell
git status
git add .
git commit -m "Prepare WeatherNow prototype for deployment"
git push
```

### 2. Deploy the API on Render

1. Sign in to Render and choose **New → Blueprint**.
2. Connect the GitHub repository containing WeatherNow. Render reads `render.yaml` and creates the `weathernow-api` web service.
3. After deployment, open the service URL (for example, `https://weathernow-api.onrender.com`) and confirm `/api/health` returns JSON with `"status":"online"`.

### 3. Deploy the frontend on Netlify

1. In Netlify choose **Add new site → Import an existing project** and connect the same GitHub repository.
2. Keep the repository root as the base directory. `netlify.toml` sets build command `npm run build` and publish directory `dist`.
3. In Netlify **Site configuration → Environment variables**, add `VITE_API_URL` with the API URL ending in `/api`, such as `https://weathernow-api.onrender.com/api`.
4. Copy the deployed Netlify site origin (such as `https://your-site.netlify.app`). In Render's `weathernow-api` service environment, set `CORS_ORIGINS` to that origin only (no trailing slash), save, and redeploy the service.
5. Trigger a Netlify redeploy so the frontend is rebuilt with `VITE_API_URL`. Open the site and run **Run demonstration**; the system status should show API connectivity when the Render service is awake.

If you add a custom domain, add its exact `https://` origin to Render's comma-separated `CORS_ORIGINS` value as well. Free API instances may sleep while idle, so the first request after inactivity can take longer.

### Deployment configuration

- `netlify.toml`: Vite build/publish settings and single-page application route fallback.
- `render.yaml`: FastAPI service blueprint. The backend allows local development origins plus the origins listed in `CORS_ORIGINS`.
- `.env.example`: documents the frontend API URL variable; set production values in Netlify's environment settings rather than committing secrets.

The deployment remains a simulated prototype. Hosting it does not connect live INSAT, IMDAA, QPE, or official warning feeds.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | API and prototype status |
| GET | `/api/events` | Simulated active events |
| GET | `/api/events/{id}` | Event details |
| GET | `/api/forecast` | Six-hour risk series |
| GET | `/api/risk-map` | Simulated 54-cell GeoJSON FeatureCollection |
| GET | `/api/alerts` | Simulated active alerts |
| GET | `/api/alerts/{id}` | Alert details |
| GET | `/api/insights` | Model mode and pipeline |
| GET | `/api/system-status` | Provider and service status |
| POST | `/api/inference/run` | Deterministic scoring for validated grids |

## AI architecture

`NowcastingModel` accepts atmospheric and terrain grids. `DemoModel` applies bounded feature normalization and deterministic weighted rules for thunderstorm, cloudburst, and flash flood scores; negative CIN weight lowers thunderstorm risk as CIN increases. Weights are centralized in `demo_model.py`. They are illustrative and uncalibrated. Alert levels are threshold-based and configured separately in `services/alerts.py`.

Future pipeline: multi-modal adapters → provenance/QC and spatial-temporal alignment → feature engineering → shared spatiotemporal encoder → thunderstorm/cloudburst/flash-flood heads → probability grids → impact analysis → alert workflow. A PyTorch-compatible trained implementation can satisfy the model contract. Any training, evaluation and operational claims require real datasets and validation.

## Data sources and future integration

All records use `SIMULATED_DEMO` provenance. No operational feed is queried. Provider interfaces are in `backend/app/services/providers.py`; add authenticated adapters with licensing, timestamps, coordinate/unit conversion, data quality, provenance, freshness and error state. Connect INSAT imagery, IMDAA fields, QPE precipitation products and licensed DEM through those adapters. Authoritative geography, population and infrastructure layers are not included.

## Prototype limitations

- Scoring is deterministic demonstration logic, not a trained, calibrated, scientifically validated model.
- All events, atmospheric values, forecasts, alerts, and terrain examples are simulated.
- The map is illustrative; its grid is synthetic and not an authoritative boundary or observed risk footprint.
- UI and API have separate small bundled fixtures; this is for interaction demos, not persistence/provider synchronization.
- Risk-map API returns synthetic grid values, not connected authoritative raster/vector data.

See [docs/real-data-integration.md](docs/real-data-integration.md) for an onboarding checklist.
