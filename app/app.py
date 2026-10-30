import os
import socket

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # expose /metrics

VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def index():
    return jsonify(message="Hello DevSecOps", version=VERSION, pod=socket.gethostname())


@app.get("/health")
@metrics.do_not_track()
def health():
    return jsonify(status="ok")
