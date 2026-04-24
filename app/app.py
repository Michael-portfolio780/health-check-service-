import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Endpoints to monitor
ENDPOINTS = {
    "service_a": "https://example.com/api/a",
    "service_b": "https://example.com/api/b",
    "service_c": "https://example.com/api/c",
}

TIMEOUT = 3  # seconds


def check_endpoint(name, url):
    start = time.time()
    try:
        response = requests.get(url, timeout=TIMEOUT)
        latency = round((time.time() - start) * 1000, 2)  # ms

        return {
            "name": name,
            "url": url,
            "status": "UP" if response.status_code == 200 else "DOWN",
            "status_code": response.status_code,
            "latency_ms": latency,
        }

    except requests.exceptions.RequestException:
        latency = round((time.time() - start) * 1000, 2)
        return {
            "name": name,
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "latency_ms": latency,
        }


@app.route("/health", methods=["GET"])
def health():
    results = []
    overall_status = "UP"

    for name, url in ENDPOINTS.items():
        result = check_endpoint(name, url)
        results.append(result)

        if result["status"] == "DOWN":
            overall_status = "DEGRADED"

    return jsonify({
        "status": overall_status,
        "timestamp": time.time(),
        "services": results
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)