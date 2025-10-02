import requests

# Uncomment this block to use hardcoded coordinates for testing
start_lat, start_lon = 42.5075, 1.5218  # Example: Carrer de la Grau
end_lat, end_lon = 42.5063, 1.5211      # Example: Avinguda Prat de la Creu

# # Uncomment this block to use address input and geocoding
# def geocode(address):
#     url = "https://nominatim.openstreetmap.org/search"
#     params = {
#         "q": address,
#         "format": "json",
#         "limit": 1
#     }
#     headers = {
#         "User-Agent": "AndorraValhallaScript/1.0 (your_email@example.com)"
#     }
#     response = requests.get(url, params=params, headers=headers)
#     if response.status_code != 200:
#         raise Exception(f"Geocoding failed for '{address}'. Status code: {response.status_code}")
#     try:
#         results = response.json()
#     except Exception:
#         raise Exception(f"Geocoding response not valid JSON for '{address}'. Response: {response.text}")
#     if results:
#         lat = float(results[0]["lat"])
#         lon = float(results[0]["lon"])
#         return lat, lon
#     else:
#         raise ValueError(f"Address not found: {address}")
#
# start_address = input("Enter start address: ")
# end_address = input("Enter end address: ")
# start_lat, start_lon = geocode(start_address)
# end_lat, end_lon = geocode(end_address)

# Valhalla server URL
url = "http://localhost:8002/route"

# Request payload using coordinates
payload = {
    "locations": [
        {"lat": start_lat, "lon": start_lon},
        {"lat": end_lat, "lon": end_lon}
    ],
    "costing": "pedestrian"
}

response = requests.post(url, json=payload)
data = response.json()

leg = data["trip"]["legs"][0]
distance = leg["summary"]["length"]
duration = leg["summary"]["time"]

print(f"Distance: {distance} km")
print(f"Duration: {duration/60:.1f} minutes\n")

print("Turn-by-turn instructions:")
for maneuver in leg["maneuvers"]:
    instruction = maneuver["instruction"]
    maneuver_type = maneuver["type"]
    maneuver_distance = maneuver["length"]
    print(f"- [{maneuver_type}] {instruction} ({maneuver_distance} km)")