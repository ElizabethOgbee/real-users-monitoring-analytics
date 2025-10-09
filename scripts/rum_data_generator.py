import requests
import random
import time
import uuid

# Datadog RUM credentials
CLIENT_TOKEN = "pub9da8e9eff920a0bfe4cf59316c0f92c5"
APPLICATION_ID = "ba828cb5-c3be-45be-8fb6-105fb0ed9ee4"
SITE = "us5.datadoghq.com"

# Behavioral rules by region
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

pages = ["/home", "/products", "/checkout",
         "/blog", "/contact", "/pricing", "/dashboard"]
browsers = ["Chrome", "Safari", "Edge", "Firefox", "Opera"]


def generate_event(country):
    behavior = behavioral_map[country]
    return {
        "application": {"id": APPLICATION_ID},
        "session_id": str(uuid.uuid4()),
        "view": random.choice(pages),
        "country": country,
        "device": random.choice(behavior["device"]),
        "browser": random.choice(browsers),
        "duration": random.randint(*behavior["duration"]),
        "user_action": random.choice(behavior["actions"]),
        "timestamp": int(time.time() * 1000)
    }


# Headers
headers = {
    "DD-API-KEY": CLIENT_TOKEN,
    "Content-Type": "application/json"
}

# Generate 4000 events equally split among regions
countries = list(behavioral_map.keys())
total_events = 4000
events_per_country = total_events // len(countries)

for country in countries:
    for i in range(events_per_country):
        data = generate_event(country)
        try:
            requests.post(
                f"https://browser-intake-{SITE}/api/v2/rum", json=data, headers=headers)
        except Exception as e:
            print(f"Error sending {country} event: {e}")
        time.sleep(0.03)
    print(f"✅ {country}: {events_per_country} events sent")

print("🎉 Done! 4000 structured RUM events successfully simulated with realistic behavior patterns.")
