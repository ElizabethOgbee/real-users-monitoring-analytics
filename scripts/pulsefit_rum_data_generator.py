import json
import csv
import random
from datetime import datetime, timedelta
import os

# === Ensure "data" folder exists ===
os.makedirs("data", exist_ok=True)

# === SETTINGS ===
NUM_EVENTS = 9000
START_DATE = datetime(2025, 6, 1)
COUNTRIES = ["Nigeria", "Ghana", "Egypt", "South Africa", "USA", "UK"]

# Probabilities for each action (should total ≈ 1)
USER_ACTIONS = {
    "visit_home": 0.52,
    "visit_plans": 0.20,
    "visit_trainers": 0.15,
    "join_plan": 0.10,
    "subscribed_basic": 0.07,
    "subscribed_pro": 0.05,
    "subscribed_elite": 0.03,
    "sent_message": 0.05
}

# Pre-calculate cumulative probabilities
ACTIONS, WEIGHTS = list(USER_ACTIONS.keys()), list(USER_ACTIONS.values())

# === GENERATE REALISTIC USER JOURNEYS ===
events = []
unique_users = random.randint(1000, 1200)  # ~1K users
user_ids = [random.randint(1000, 9999) for _ in range(unique_users)]

for user_id in user_ids:
    num_actions = random.randint(1, 7)  # each user performs 1–7 actions
    country = random.choice(COUNTRIES)
    user_start = START_DATE + timedelta(days=random.randint(0, 150))  # between June–Oct

    for i in range(num_actions):
        action = random.choices(ACTIONS, WEIGHTS, k=1)[0]
        timestamp = user_start + timedelta(
            hours=random.randint(0, 24),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        event = {
            "user_id": user_id,
            "country": country,
            "user_action": action,
            "timestamp": int(timestamp.timestamp() * 1000),  # Unix ms
            "readable_timestamp": timestamp.strftime("%Y-%m-%d %I:%M:%S %p")
        }
        events.append(event)

# Trim if we go slightly over
events = events[:NUM_EVENTS]

# === SAVE AS JSON ===
json_path = "data/rum_generated.json"
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(events, json_file, indent=4)

# === SAVE AS CSV ===
csv_path = "data/rum_generated.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=events[0].keys())
    writer.writeheader()
    writer.writerows(events)

print(f"✅ Successfully generated {len(events)} realistic user events!")
print(f"📁 Files saved to: {json_path} and {csv_path}")

