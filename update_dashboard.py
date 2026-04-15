import requests
import json

dashboard = {
    "dashboard": {
        "id": None,
        "uid": "fastapi-mlops",
        "title": "FastAPI MLOps Monitoring",
        "tags": ["fastapi", "mlops", "premium"],
        "panels": [
            {
                "id": 1,
                "title": "Total requests in server",
                "type": "piechart",
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 0},
                "targets": [
                    {"expr": "sum(http_requests_total) by (handler)", "refId": "A"}
                ],
                "options": {"pieType": "donut", "displayLabels": ["percent"]},
                "datasource": {"type": "prometheus", "uid": "dfihy5f0yd2ioe"}
            },
            {
                "id": 2,
                "title": "Requests created",
                "type": "timeseries",
                "gridPos": {"h": 10, "w": 12, "x": 12, "y": 0},
                "targets": [
                    {"expr": "sum(http_requests_total) by (handler)", "refId": "A"}
                ],
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "drawStyle": "line",
                            "fillOpacity": 30,
                            "stacking": {"mode": "normal"}
                        }
                    }
                },
                "datasource": {"type": "prometheus", "uid": "dfihy5f0yd2ioe"}
            },
            {
                "id": 3,
                "title": "batch prediction calls",
                "type": "gauge",
                "gridPos": {"h": 10, "w": 12, "x": 0, "y": 10},
                "targets": [
                    {"expr": 'sum(http_requests_total{handler="/batch_prediction"})', "refId": "A"}
                ],
                "fieldConfig": {
                    "defaults": {
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": 0},
                                {"color": "#EAB839", "value": 5},
                                {"color": "red", "value": 10}
                            ]
                        }
                    }
                },
                "datasource": {"type": "prometheus", "uid": "dfihy5f0yd2ioe"}
            },
            {
                "id": 4,
                "title": "Latency",
                "type": "timeseries",
                "gridPos": {"h": 10, "w": 12, "x": 12, "y": 10},
                "targets": [
                    {"expr": "http_request_duration_highr_seconds_sum / http_request_duration_highr_seconds_count", "refId": "A"}
                ],
                "fieldConfig": {"defaults": {"unit": "s"}},
                "datasource": {"type": "prometheus", "uid": "dfihy5f0yd2ioe"}
            }
        ],
        "schemaVersion": 39,
        "timezone": "browser"
    },
    "overwrite": True
}

# Use the actual Prometheus datasource UID if possible, otherwise 'prometheus' or 'default' often work
try:
    auth = ("admin", "admin")
    url = "http://localhost:3001/api/dashboards/db"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=dashboard, auth=auth, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
