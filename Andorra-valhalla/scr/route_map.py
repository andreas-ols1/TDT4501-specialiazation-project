import requests
import folium
import polyline

start_lat, start_lon = 42.5561, 1.5331  # Ordino
end_lat, end_lon = 42.4634, 1.4917      # Sant Julià de Lòria

url = "http://localhost:8002/route"
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

# --- Visualization ---
# Decode the route geometry (polyline)
route_coords = polyline.decode(leg["shape"])

# Center map on the midpoint of the route
mid_lat = (start_lat + end_lat) / 2
mid_lon = (start_lon + end_lon) / 2
m = folium.Map(location=[mid_lat, mid_lon], zoom_start=18)

# Draw the route as a blue line
folium.PolyLine(route_coords, color="blue", weight=8, opacity=0.9).add_to(m)

# Mark start and end points
folium.Marker([start_lat, start_lon], popup="Start", icon=folium.Icon(color="green")).add_to(m)
folium.Marker([end_lat, end_lon], popup="End", icon=folium.Icon(color="red")).add_to(m)

# Add circle markers for each route point
for lat, lon in route_coords:
    folium.CircleMarker([lat, lon], radius=3, color="blue", fill=True, fill_color="blue").add_to(m)

# Save map to HTML
m.save("route_map.html")
print("Route map saved as route_map.html")
