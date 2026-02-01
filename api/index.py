import json

def handler(request):
    try:
        body = request['body']
        data = json.loads(body)
        regions = data["regions"]
        threshold = data["threshold_ms"]
        
        # Mock data
        telemetry = [
            {"region": "apac", "latency_ms": 120, "uptime": 1.0},
            {"region": "apac", "latency_ms": 150, "uptime": 0.99},
            {"region": "apac", "latency_ms": 160, "uptime": 0.98},
            {"region": "amer", "latency_ms": 200, "uptime": 0.98},
            {"region": "amer", "latency_ms": 180, "uptime": 0.97},
            {"region": "amer", "latency_ms": 220, "uptime": 0.96},
        ]
        
        result = {}
        for region in regions:
            region_data = [r for r in telemetry if r["region"] == region]
            if not region_data:
                result[region] = {"error": "No data"}
                continue
                
            latencies = [r["latency_ms"] for r in region_data]
            uptimes = [r["uptime"] for r in region_data]
            
            # Pure Python stats (no numpy)
            avg_latency = sum(latencies) / len(latencies)
            avg_uptime = sum(uptimes) / len(uptimes)
            p95_latency = sorted(latencies)[int(0.95 * len(latencies))]
            breaches = sum(1 for x in latencies if x > threshold)
            
            result[region] = {
                "avg_latency": round(float(avg_latency), 2),
                "p95_latency": round(float(p95_latency), 2),
                "avg_uptime": round(float(avg_uptime), 3),
                "breaches": int(breaches)
            }
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
