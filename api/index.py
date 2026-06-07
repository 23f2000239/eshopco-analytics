from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = [{"region":"apac","latency_ms":208.33,"uptime_pct":98.078},{"region":"apac","latency_ms":125.37,"uptime_pct":98.852},{"region":"apac","latency_ms":214.09,"uptime_pct":99.193},{"region":"apac","latency_ms":153.76,"uptime_pct":98.098},{"region":"apac","latency_ms":227.48,"uptime_pct":97.311},{"region":"apac","latency_ms":140.86,"uptime_pct":97.635},{"region":"apac","latency_ms":220.66,"uptime_pct":99.133},{"region":"apac","latency_ms":157.65,"uptime_pct":97.6},{"region":"apac","latency_ms":125.62,"uptime_pct":99.174},{"region":"apac","latency_ms":154.14,"uptime_pct":98.879},{"region":"apac","latency_ms":133.36,"uptime_pct":99.123},{"region":"apac","latency_ms":148.3,"uptime_pct":99.075},{"region":"emea","latency_ms":186.78,"uptime_pct":97.443},{"region":"emea","latency_ms":130.03,"uptime_pct":99.407},{"region":"emea","latency_ms":152.87,"uptime_pct":97.647},{"region":"emea","latency_ms":191.46,"uptime_pct":98.744},{"region":"emea","latency_ms":165.08,"uptime_pct":99.473},{"region":"emea","latency_ms":164.41,"uptime_pct":98.642},{"region":"emea","latency_ms":123.53,"uptime_pct":97.595},{"region":"emea","latency_ms":197.92,"uptime_pct":98.25},{"region":"emea","latency_ms":142.27,"uptime_pct":99.287},{"region":"emea","latency_ms":193.6,"uptime_pct":98.289},{"region":"emea","latency_ms":220.73,"uptime_pct":99.438},{"region":"emea","latency_ms":123.56,"uptime_pct":99.493},{"region":"amer","latency_ms":136.74,"uptime_pct":98.223},{"region":"amer","latency_ms":182.99,"uptime_pct":97.357},{"region":"amer","latency_ms":131.49,"uptime_pct":99.378},{"region":"amer","latency_ms":165.17,"uptime_pct":97.484},{"region":"amer","latency_ms":228.64,"uptime_pct":98.877},{"region":"amer","latency_ms":113.02,"uptime_pct":97.326},{"region":"amer","latency_ms":137.9,"uptime_pct":98.793},{"region":"amer","latency_ms":139.01,"uptime_pct":99.122},{"region":"amer","latency_ms":186.34,"uptime_pct":99.159},{"region":"amer","latency_ms":140.93,"uptime_pct":97.293},{"region":"amer","latency_ms":161.52,"uptime_pct":98.18},{"region":"amer","latency_ms":181.01,"uptime_pct":97.181}]

class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.options("/")
async def options_handler():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.post("/")
def analyze(req: AnalyticsRequest):
    result = {}
    for region in req.regions:
        records = [r for r in DATA if r["region"] == region]
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 4),
            "p95_latency": round(float(np.percentile(latencies, 95)), 4),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > req.threshold_ms))
        }
    return JSONResponse(
        content=result,
        headers={"Access-Control-Allow-Origin": "*"}
    )
