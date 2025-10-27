import json
import csv
import random
import uuid
from datetime import datetime, timedelta
import os

# --- Ensure data folder exists ---
os.makedirs("data", exist_ok=True)

# --- Settings ---
TARGET_EVENTS = 10000       # Total events to generate
NUM_USERS = 3000           # Unique users
MAX_ACTIONS_PER_SESSION = 6
START_DATE = datetime.now() - timedelta(days=180)  # 6 months back
COUNTRIES = ["Nigeria", "Ghana", "Egypt", "South Africa", "USA", "UK"]

# --- Possible actions ---
ACTIONS_FLOW = ["visit home", "subscribed to Basic plans", "subscribed to pro plans", "subscribed to elite plans", "join_plan", "viewed alex johnson profile",
                "viewed mia carter profile", "visit liam smith trainers", "visit contact", "sent message"]

events = []

while len(events) < TARGET_EVENTS:
    user_id = random.randint(1000, 9999)
    country = random.choice(COUNTRIES)

    # Each user can have 1-2 sessions
    num_sessions = random.choice([1, 2])
    for _ in range(num_sessions):
        session_id = str(uuid.uuid4())  # unique session ID
        base_time = START_DATE + timedelta(days=random.randint(0, 180))
        num_actions = random.randint(2, MAX_ACTIONS_PER_SESSION)

        # Generate realistic actions per session
        user_actions = ["visit home"]
        if random.random() < 0.8:
            user_actions.append("visit plans")
            if random.random() < 0.3:
                user_actions.append("join_plan")
        if random.random() < 0.5:
            user_actions.append("visit trainers")
        if random.random() < 0.4:
            user_actions.append("visit contact")
            if random.random() < 0.2:
                user_actions.append("sent message")

        # Shuffle for randomness and limit to num_actions
        random.shuffle(user_actions)
        user_actions = user_actions[:num_actions]

        # Generate events with realistic time spacing
        for i, action in enumerate(user_actions):
            timestamp = base_time + timedelta(
                minutes=random.randint(5, 180) * i,
                seconds=random.randint(0, 59)
            )
            event = {
                "user_id": user_id,
                "session_id": session_id,
                "country": country,
                "user_action": action,
                "timestamp": int(timestamp.timestamp() * 1000),  # UNIX ms
                "readable_timestamp": timestamp.strftime("%y-%m-%d %I:%M:%S %p")

            }
            events.append(event)
            if len(events) >= TARGET_EVENTS:
                break
        if len(events) >= TARGET_EVENTS:
            break

# Shuffle events for realism
random.shuffle(events)

# --- Save to JSON ---
json_path = "data/rum_generated.json"
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(events, json_file, indent=4)

# --- Save to CSV ---
csv_path = "data/rum_generated.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=events[0].keys())
    writer.writeheader()
    writer.writerows(events)

print(
    f"✅ Successfully generated {len(events)} realistic user events with session IDs!")
print("📁 Files saved to: data/rum_generated.json and data/rum_generated.csv")
