import json
import os

def handler(event, context):
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body
        
        regions = data.get('regions', [])
        threshold = data.get('threshold_ms', 177)
        
        telemetry = [
            {'region': 'apac', 'latency_ms': 120, 'uptime': 1.0},
            {'region': 'apac', 'latency_ms': 150, 'uptime': 0.99},
            {'region': 'apac', 'latency_ms': 160, 'uptime': 0.98},
            {'region': 'amer', 'latency_ms': 200, 'uptime': 0.98},
            {'region': 'amer', 'latency_ms': 180, 'uptime': 0.97},
            {'region': 'amer', 'latency_ms': 220, 'uptime': 0.96}
        ]
        
        result = {}
        for region in regions:
            region_data = [r for r in telemetry if r['region'] == region]
            if region_data:
                latencies = [r['latency_ms'] for r in region_data]
                uptimes = [r['uptime'] for r in region_data]
                result[region] = {
                    'avg_latency': round(sum(latencies)/len(latencies), 2),
                    'p95_latency': round(sorted(latencies)[-1], 2),
                    'avg_uptime': round(sum(uptimes)/len(uptimes), 3),
                    'breaches': sum(1 for x in latencies if x > threshold)
                }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
