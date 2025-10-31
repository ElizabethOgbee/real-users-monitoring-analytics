import csv
import json
import random
from datetime import datetime, timedelta

# ----- Constants -----
PLANS = ["Basic", "Pro", "Elite"]
TRAINERS = ["Alex Johnson", "Mia Carter", "Liam Smith"]
PAGES = ["Home", "Plans", "Trainers", "Contact"]

ACTIONS = [
    *[f"Visited {page}" for page in PAGES],
    *[f"Viewed Trainer: {t}" for t in TRAINERS],
    *[f"Viewed Plan: {p}" for p in PLANS]
]

COUNTRIES = ["Nigeria", "Kenya", "Egypt", "South Africa", "USA", "UK"]

# ----- Timestamp helper -----


def get_timestamp(base_time, offset_minutes):
    t = base_time + timedelta(minutes=offset_minutes)
    return t.strftime("%m/%d/%Y, %I:%M %p")

# ----- Generate realistic user sessions -----


def generate_rum_data(target_events=10000, num_users=3000):
    events = []
    base_date = datetime.now() - timedelta(days=90)

    while len(events) < target_events:
        user_id = random.randint(10000, 99999)
        country = random.choices(COUNTRIES, weights=[0.6, 0.15, 0.3, 0.1, 0.20, 0.15])[
            0]  # Nigeria more common

        # each user may have 1–3 sessions
        for _ in range(random.randint(1, 3)):
            session_id = random.randint(1000, 9999)
            start_time = base_date + timedelta(days=random.randint(0, 90))
            num_actions = random.randint(2, 6)

            chosen_actions = random.sample(ACTIONS, num_actions)
            for i, act in enumerate(chosen_actions):
                timestamp = get_timestamp(
                    start_time, i * random.randint(2, 15))
                events.append({
                    "session_id": session_id,
                    "user_id": user_id,
                    "country": country,
                    "user_action": act,
                    "timestamp": timestamp
                })

                if len(events) >= target_events:
                    break
            if len(events) >= target_events:
                break
    return events


# ----- Save Files -----
if __name__ == "__main__":
    rum_data = generate_rum_data(10000, 3000)

    with open("pulsefit_rum_data_generated.json", "w", encoding="utf-8") as f:
        json.dump(rum_data, f, indent=2)

    with open("pulsefit_rum_data_generated.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rum_data[0].keys())
        writer.writeheader()
        writer.writerows(rum_data)

    print("✅ 10,000 RUM data points saved to 'pulsefit_rum_data_generated.json' and 'pulsefit_rum_data_generated.csv'")
