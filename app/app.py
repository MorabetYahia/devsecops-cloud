import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # expose /metrics

VERSION = os.getenv("APP_VERSION", "dev")
STARTED_AT = datetime.now(timezone.utc)

CHECKS = [
    ("pytest", "Le code fait bien ce qu'il promet"),
    ("Gitleaks", "Aucun secret oublié dans l'historique Git"),
    ("Semgrep", "Aucune faille connue dans le code"),
    ("Checkov", "Infrastructure Terraform et Kubernetes analysée"),
    ("Trivy", "Aucune CVE critique dans le conteneur"),
]


def info():
    return {
        "owner": "Yahia Morabet",
        "message": "Hello DevSecOps",
        "pod": socket.gethostname(),
        "version": VERSION,
        "uptime_seconds": int((datetime.now(timezone.utc) - STARTED_AT).total_seconds()),
    }


@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = (
        "default-src 'none'; style-src 'unsafe-inline'; "
        "base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    )
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    return resp


@app.get("/")
def index():
    return render_template("index.html", checks=CHECKS, **info())


@app.get("/api/info")
def api_info():
    return jsonify(info())


@app.get("/health")
@metrics.do_not_track()
def health():
    return jsonify(status="ok")
