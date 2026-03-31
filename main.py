"""
Screening Task: Minimal A/B trust experiment prototype.

Two conditions differ in agent name + tone:
  Condition A: "Aria" (warm, conversational)
  Condition B: "System" (formal, neutral)

Task: 5 product recommendations. Participant accepts or rejects each.
Logs: participant_id, condition, trial, decision, timestamp, latency_ms

Run: python main.py
Then open http://localhost:5000 in browser.
"""

import os
import json
import csv
import uuid
import random
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, template_folder="static")

OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

# pre-generated product recommendations
PRODUCTS = [
    {"name": "Sony WH-1000XM5", "category": "Headphones", "price": "$348"},
    {"name": "Kindle Paperwhite", "category": "E-Reader", "price": "$140"},
    {"name": "Anker PowerCore 26800", "category": "Power Bank", "price": "$66"},
    {"name": "Logitech MX Master 3S", "category": "Mouse", "price": "$99"},
    {"name": "Samsung T7 Shield 1TB", "category": "External SSD", "price": "$110"},
]

# condition configs
CONDITIONS = {
    "A": {
        "agent_name": "Aria",
        "tone": "warm",
        "rec_template": "Hey! I think you'd really enjoy the {product}. It's a great {category} and well worth it at {price}. What do you think?",
        "style": {"bg": "#f0f4ff", "accent": "#4a6cf7", "avatar": "friendly"},
    },
    "B": {
        "agent_name": "System",
        "tone": "formal",
        "rec_template": "Recommendation: {product}. Category: {category}. Price: {price}. Based on analysis, this item has a high relevance score. Accept or reject.",
        "style": {"bg": "#f5f5f5", "accent": "#666", "avatar": "neutral"},
    },
}

trial_logs = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start_session():
    pid = str(uuid.uuid4())[:8]
    condition = random.choice(["A", "B"])
    config = CONDITIONS[condition]

    trials = []
    for i, product in enumerate(PRODUCTS):
        rec_text = config["rec_template"].format(
            product=product["name"],
            category=product["category"],
            price=product["price"],
        )
        trials.append({
            "trial": i + 1,
            "product": product["name"],
            "category": product["category"],
            "price": product["price"],
            "recommendation": rec_text,
        })

    return jsonify({
        "participant_id": pid,
        "condition": condition,
        "agent_name": config["agent_name"],
        "tone": config["tone"],
        "style": config["style"],
        "trials": trials,
    })


@app.route("/api/log", methods=["POST"])
def log_trial():
    data = request.json
    entry = {
        "participant_id": data["participant_id"],
        "condition": data["condition"],
        "trial": data["trial"],
        "product": data["product"],
        "decision": data["decision"],
        "timestamp": data["timestamp"],
        "latency_ms": data["latency_ms"],
    }
    trial_logs.append(entry)
    _save_logs()
    return jsonify({"status": "ok"})


@app.route("/api/export")
def export():
    return jsonify(trial_logs)


def _save_logs():
    # JSON
    with open(OUT_DIR / "experiment_log.json", "w") as f:
        json.dump(trial_logs, f, indent=2)

    # CSV
    if trial_logs:
        with open(OUT_DIR / "experiment_log.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=trial_logs[0].keys())
            writer.writeheader()
            writer.writerows(trial_logs)


if __name__ == "__main__":
    print("Trust Experiment Server")
    print("Open http://localhost:5001 in your browser")
    print(f"Logs will be saved to {OUT_DIR}/")
    app.run(debug=True, port=5001)
