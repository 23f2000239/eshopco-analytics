from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open(os.path.join(os.path.dirname(__file__), "../data/telemetry.json")) as f:
    TELEMETRY = json.load(f)

class Request(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.post("/api")
def analyze(req: Request):
    result = {}
    for region in req.regions:
        records = TELEMETRY.get(region, [])
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 4),
            "p95_latency": round(float(np.percentile(latencies, 95)), 4),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > req.threshold_ms))
        }
    return result
