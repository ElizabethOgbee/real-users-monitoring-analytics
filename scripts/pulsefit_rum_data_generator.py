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
    "visit_home": 1.52,
    "visit_plans": 0.50,
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
    user_start = START_DATE + \
        timedelta(days=random.randint(0, 150))  # between June–Oct

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


# --- Ensure data folder exists ---
os.makedirs("data", exist_ok=True)

# --- SETTINGS ---
NUM_EVENTS = 9000
START_DATE = datetime(2025, 6, 1)  # start from June 2025
COUNTRIES = ["Nigeria", "South Africa", "Egypt", "Ghana", "Kenya", "Tanzania"]
TRAINERS = ["Alex Johnson", "Mia Carter", "Liam Smith"]

# Weighted probabilities for user actions
USER_ACTIONS = [
    ("visit_home", 1.40),
    ("visit_plans", 0.20),
    ("visit_trainers", 0.15),
    ("view_plan", 0.07),
    ("subscribed_basic", 0.03),
    ("subscribed_pro", 0.01),
    ("subscribed_elite", 0.009),
    ("sent_message", 0.04),
]

# Weighted probabilities for countries
COUNTRY_WEIGHTS = {
    "Nigeria": 0.32,
    "South Africa": 0.27,
    "Egypt": 0.18,
    "Ghana": 0.13,
    "Kenya": 0.06,
    "Tanzania": 0.04,
}


def weighted_choice(choices):
    total = sum(weight for _, weight in choices)
    r = random.uniform(0, total)
    upto = 0
    for choice, weight in choices:
        if upto + weight >= r:
            return choice
        upto += weight


def weighted_country(countries):
    total = sum(COUNTRY_WEIGHTS.values())
    r = random.uniform(0, total)
    upto = 0
    for country, weight in COUNTRY_WEIGHTS.items():
        if upto + weight >= r:
            return country
        upto += weight


# --- GENERATE DATA ---
events = []
for _ in range(NUM_EVENTS):
    user_id = random.randint(1000, 9999)
    country = weighted_country(COUNTRIES)
    action = weighted_choice(USER_ACTIONS)
    timestamp = START_DATE + timedelta(
        days=random.randint(0, (datetime.now() - START_DATE).days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )

    # Add trainer name only for "visit_trainers"
    trainer_name = random.choice(
        TRAINERS) if action == "visit_trainers" else ""

    event = {
        "user_id": user_id,
        "country": country,
        "user_action": action,
        "trainer_name": trainer_name,
        "timestamp": int(timestamp.timestamp() * 1000),
        "readable_timestamp": timestamp.strftime("%Y-%m-%d %I:%M:%S %p"),
    }
    events.append(event)

# --- SAVE JSON ---
json_path = "data/rum_generated.json"
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(events, json_file, indent=4)

# --- SAVE CSV ---
csv_path = "data/rum_generated.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=events[0].keys())
    writer.writeheader()
    writer.writerows(events)

print(f"✅ Successfully generated {NUM_EVENTS} realistic user events!")
print("📁 Files saved to: data/rum_generated.json and data/rum_generated.csv")
