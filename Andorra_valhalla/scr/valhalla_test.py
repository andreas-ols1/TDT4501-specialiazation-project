import requests
import json

# Valhalla server URL
url = "http://localhost:8002/route"

# Request payload: two locations in Andorra
payload = {
    "locations": [
        {"lat": 42.5075, "lon": 1.5218},
        {"lat": 42.5063, "lon": 1.5211}
    ],
    "costing": "auto"
}

# Send POST request
response = requests.post(url, json=payload)
data = response.json()

# Extract and print distance and duration
leg = data["trip"]["legs"][0]
distance = leg["summary"]["length"]  # in kilometers
duration = leg["summary"]["time"]    # in seconds

print(f"Distance: {distance} km")
print(f"Duration: {duration/60:.1f} minutes\n")

# Print turn-by-turn instructions
print("Turn-by-turn instructions:")
for maneuver in leg["maneuvers"]:
    instruction = maneuver["instruction"]
    maneuver_type = maneuver["type"]
    maneuver_distance = maneuver["length"]  # in kilometers
    print(f"- [{maneuver_type}] {instruction} ({maneuver_distance} km)")