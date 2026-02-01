app.add_middleware(>
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def analytics(request: Request):
    body = await request.body()
    data = json.loads(body)
    regions = data["regions"]
    threshold = data["threshold_ms"]

    telemetry = [
        {"region": "apac", "latency_ms": 120, "uptime": 1.0},
        {"region": "apac", "latency_ms": 150, "uptime": 0.99},
        {"region": "apac", "latency_ms": 160, "uptime": 0.98},
        {"region": "amer", "latency_ms": 200, "uptime": 0.98},
        {"region": "amer", "latency_ms": 180, "uptime": 0.97},
        {"region": "amer", "latency_ms": 220, "uptime": 0.96},
    ]

    result = {}
    for r in regions:
        region_data = [x for x in telemetry if x["region"] == r]
        if not region_data:
            result[r] = {"error": "No data"}
            continue
        latencies = np.array([x["latency_ms"] for x in region_data])
        uptimes = [x["uptime"] for x in region_data]
        result[r] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": int(np.sum(latencies > threshold))
        }
    return result
