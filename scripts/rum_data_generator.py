import os
import json
import random
import uuid
from datetime import datetime, timedelta

# -----------------------------
# 1️⃣ Ensure 'data' folder exists
# -----------------------------
os.makedirs("data", exist_ok=True)

# -----------------------------
# 2️⃣ Define behavioral rules by region
# -----------------------------
behavioral_map = {
    "Nigeria": {"device": ["mobile"] * 6 + ["desktop"] * 2 + ["tablet"] * 2,
                "actions": ["click", "scroll", "navigate"],
                "duration": (1000, 12000)},
    "Ghana": {"device": ["mobile", "desktop"],
              "actions": ["scroll", "click"],
              "duration": (4000, 18000)},
    "Egypt": {"device": ["desktop"] * 7 + ["mobile"] * 3,
              "actions": ["navigate", "scroll", "click"],
              "duration": (10000, 30000)},
    "South Africa": {"device": ["mobile", "desktop"],
                     "actions": ["form_submit", "click", "navigate"],
                     "duration": (6000, 20000)},
    "Kenya": {"device": ["mobile"] * 8 + ["desktop"] * 2,
              "actions": ["scroll", "click"],
              "duration": (1500, 10000)},
    "United Kingdom": {"device": ["desktop"] * 8 + ["tablet"] * 2,
                       "actions": ["navigate", "scroll"],
                       "duration": (12000, 40000)},
    "United States": {"device": ["desktop", "tablet"],
                      "actions": ["navigate", "click", "scroll"],
                      "duration": (10000, 30000)},
    "Japan": {"device": ["desktop"] * 9 + ["mobile"],
              "actions": ["form_submit", "navigate"],
              "duration": (15000, 35000)},
}

# -----------------------------
# 3️⃣ Define pages and browsers
# -----------------------------
pages = ["/home", "/products", "/checkout",
         "/blog", "/contact", "/pricing", "/dashboard"]
browsers = ["Chrome", "Safari", "Edge", "Firefox", "Opera"]

# -----------------------------
# 4️⃣ Define timestamps (6 months)
# -----------------------------
start_date = datetime.now() - timedelta(days=180)  # 6 months ago
end_date = datetime.now()


def random_timestamp(start, end):
    """Generate a random timestamp (ms) and human-readable timestamp between start and end"""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    random_time = start + timedelta(seconds=random_seconds)
    timestamp_ms = int(random_time.timestamp() * 1000)
    timestamp_readable = random_time.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp_ms, timestamp_readable

# -----------------------------
# 5️⃣ Generate a single event
# -----------------------------


def generate_event(country):
    """Generate a single synthetic RUM event"""
    behavior = behavioral_map[country]
    ts_ms, ts_readable = random_timestamp(start_date, end_date)
    return {
        "session_id": str(uuid.uuid4()),
        "view": random.choice(pages),
        "country": country,
        "device": random.choice(behavior["device"]),
        "browser": random.choice(browsers),
        "duration": random.randint(*behavior["duration"]),
        "user_action": random.choice(behavior["actions"]),
        "timestamp": ts_ms,
        "timestamp_readable": ts_readable
    }


# -----------------------------
# 6️⃣ Generate all events (4,000)
# -----------------------------
events = []
countries = list(behavioral_map.keys())
total_events = 4000
events_per_country = total_events // len(countries)

for country in countries:
    for _ in range(events_per_country):
        events.append(generate_event(country))

# -----------------------------
# 7️⃣ Shuffle events for randomness
# -----------------------------
random.shuffle(events)

# -----------------------------
# 8️⃣ Save events to JSON
# -----------------------------
with open("data/rum_generated.json", "w") as f:
    json.dump(events, f, indent=2)

print("✅ 4,000 synthetic RUM events saved locally with 6-month randomized timestamps and country order!")
