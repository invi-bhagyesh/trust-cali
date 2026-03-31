"""Generate sample output data to demonstrate the logging format."""

import json
import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

PRODUCTS = [
    "Sony WH-1000XM5",
    "Kindle Paperwhite",
    "Anker PowerCore 26800",
    "Logitech MX Master 3S",
    "Samsung T7 Shield 1TB",
]

logs = []
base_time = datetime(2026, 3, 31, 14, 0, 0)

for p in range(6):
    pid = str(uuid.uuid4())[:8]
    condition = "A" if p % 2 == 0 else "B"
    t = base_time + timedelta(minutes=p * 5)

    for trial_num, product in enumerate(PRODUCTS, 1):
        latency = random.randint(800, 4500)
        # condition A (warm "Aria") tends to get more accepts
        accept_prob = 0.7 if condition == "A" else 0.5
        decision = "accept" if random.random() < accept_prob else "reject"

        t += timedelta(seconds=latency / 1000 + random.uniform(1, 3))

        logs.append({
            "participant_id": pid,
            "condition": condition,
            "trial": trial_num,
            "product": product,
            "decision": decision,
            "timestamp": t.isoformat(),
            "latency_ms": latency,
        })

# save JSON
with open(OUT_DIR / "experiment_log.json", "w") as f:
    json.dump(logs, f, indent=2)

# save CSV
with open(OUT_DIR / "experiment_log.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=logs[0].keys())
    writer.writeheader()
    writer.writerows(logs)

print(f"Generated {len(logs)} trial logs for {6} participants")
print(f"Saved to {OUT_DIR}/experiment_log.json and experiment_log.csv")
