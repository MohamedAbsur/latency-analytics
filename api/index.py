app.add_middleware(>
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def analytics(request: Request):
    data = await request.json()
    regions = data["regions"]
    threshold_ms = data["threshold_ms"]

    # MOCK TELEMETRY DATA - NO FILE NEEDED
    telemetry = [
        {"region": "apac", "latency_ms": 120, "uptime": 1.0},
        {"region": "apac", "latency_ms": 150, "uptime": 0.99},
        {"region": "apac", "latency_ms": 160, "uptime": 0.98},
        {"region": "amer", "latency_ms": 200, "uptime": 0.98},
        {"region": "amer", "latency_ms": 180, "uptime": 0.97},
        {"region": "amer", "latency_ms": 220, "uptime": 0.96},
        {"region": "amer", "latency_ms": 175, "uptime": 0.99},
    ]

    results = {}
    for region in regions:
        region_data = [r for r in telemetry if r["region"] == region]
        if not region_data:
            results[region] = {"error": "No data"}
            continue

        latencies = np.array([r["latency_ms"] for r in region_data])
        uptimes = [r["uptime"] for r in region_data]

        results[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": int(np.sum(latencies > threshold_ms))
        }
    return results
