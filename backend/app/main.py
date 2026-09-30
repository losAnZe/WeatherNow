import json
import os
from pathlib import Path
from math import sin
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .ml.inference_service import InferenceService
from .services.providers import PROVIDERS
from .services.alerts import severity_for

app = FastAPI(title="WeatherNow Prototype API", version="0.1.0", description="Simulated severe-weather nowcasting demonstration API")
configured_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5174", "http://127.0.0.1:5174", *configured_origins], allow_methods=["*"], allow_headers=["*"])
engine = InferenceService()
EVENTS = json.loads((Path(__file__).resolve().parents[2] / 'data' / 'demo' / 'scenarios.json').read_text(encoding='utf-8'))['events']
ALERTS = [{"id":"alt-01","eventType":"Severe Thunderstorm","severity":"Warning","location":"Central India","probability":82,"forecastWindow":"+2h to +4h","message":"Increasing convective risk in the central region. Monitor the affected area and prepare response resources according to local authority protocols.","generatedAt":"16:42 IST","status":"Active"},{"id":"alt-02","eventType":"Cloudburst","severity":"Severe Warning","location":"Western Ghats","probability":74,"forecastWindow":"+3h to +5h","message":"High-intensity rainfall scenario detected over elevated terrain. Continue monitoring through local authority protocols.","generatedAt":"16:39 IST","status":"Active"}]
class InferenceRequest(BaseModel):
    atmospheric_grid: list[dict[str, float]] = Field(default_factory=list, max_length=10000)
    terrain_grid: list[dict[str, float]] = Field(default_factory=list, max_length=10000)

@app.get("/api/health")
def health(): return {"status":"online","mode":"PROTOTYPE","dataSource":"SIMULATED_DEMO"}
@app.get("/api/events")
def events(): return {"items":EVENTS,"dataSource":"SIMULATED_DEMO"}
@app.get("/api/events/{event_id}")
def event_detail(event_id: str):
    for item in EVENTS:
        if item["id"] == event_id: return item
    raise HTTPException(404, "Event not found")
@app.get("/api/forecast")
def forecast(): return {"hours":[{"hour":i,"thunderstorm":v[0],"cloudburst":v[1],"flashFlood":v[2],"rainfall":v[3]} for i,v in enumerate([(48,35,25,18),(64,49,34,34),(82,67,53,57),(91,74,61,76),(78,58,49,82),(61,46,37,65),(46,34,29,43)])],"dataSource":"SIMULATED_DEMO"}
@app.get("/api/risk-map")
def risk_map():
    atmospheric: list[dict[str, float]] = []
    terrain: list[dict[str, float]] = []
    locations: list[tuple[float, float]] = []
    for row in range(6):
        for column in range(9):
            index = row * 9 + column
            dx, dy = (column - 4) * 1.18, (row - 2.7) * 1.02
            core = max(0.0, 1.0 - (((dx - .1) ** 2 + (dy + .1) ** 2) ** .5) / 4.5)
            oscillation = (1.0 + sin(index * 2.13)) * 4
            atmospheric.append({"iwv": 26 + core * 18, "cape": 490 + core * 1760, "cin": 105 - core * 68, "convergence": 25 + core * 65, "shear": 14 + core * 18, "ctt_cooling": core * 9, "rainfall": 9 + core * 67 + oscillation})
            terrain.append({"elevation": 220 + max(0, 3-row)*185 + max(0, 4-column)*42 + core*150, "slope": 3 + core*24 + (4 if row > 3 else 0), "drainage": min(.95, .22 + core*.42 + (.12 if row > 3 else 0))})
            locations.append((78.2 + dx, 20.6 + dy))
    predictions = engine.model.predict(atmospheric, terrain)
    features = []
    for index, ((longitude, latitude), values, prediction) in enumerate(zip(locations, atmospheric, predictions)):
        features.append({"type":"Feature","id":f"grid-{index}","geometry":{"type":"Point","coordinates":[round(longitude, 4), round(latitude, 4)]},"properties":{"dataSource":"SIMULATED_DEMO","forecastHour":2,"thunderstormProbability":prediction["thunderstorm"],"cloudburstProbability":prediction["cloudburst"],"flashFloodProbability":prediction["flash_flood"],"rainfallIntensity":round(values["rainfall"], 1),"iwv":round(values["iwv"], 1),"cape":round(values["cape"]),"cin":round(values["cin"]),"cttCooling":round(values["ctt_cooling"], 1)}})
    return {"type":"FeatureCollection","dataSource":"SIMULATED_DEMO","features":features}
@app.get("/api/alerts")
def alerts(): return {"items":ALERTS,"dataSource":"SIMULATED_DEMO"}
@app.get("/api/alerts/{alert_id}")
def alert_detail(alert_id: str):
    for item in ALERTS:
        if item["id"] == alert_id: return item
    raise HTTPException(404,"Alert not found")
@app.get("/api/insights")
def insights(): return {"model":"WeatherNow Multi-Task Nowcasting","mode":"PROTOTYPE","dataSource":"SIMULATED_DEMO","heads":["Thunderstorm","Cloudburst","Flash Flood"],"architecture":["Satellite adapter","IMDAA adapter","QPE adapter","DEM adapter","Data fusion","Feature pipeline","Spatiotemporal encoder","Multi-task heads","Risk maps"]}
@app.get("/api/system-status")
def system_status(): return {"providers":[provider.status() for provider in PROVIDERS],"services":[{"name":n,"status":"ONLINE"} for n in ("AI Inference Engine","Risk Engine","Alert Engine","Map Service","API")],"dataSource":"SIMULATED_DEMO"}
@app.post("/api/inference/run")
def run_inference(request: InferenceRequest): return engine.run(request.atmospheric_grid, request.terrain_grid)
