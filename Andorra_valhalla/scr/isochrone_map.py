import requests
import folium
import polyline

center_lat, center_lon = 42.5561, 1.5331  # Ordino

url = "http://localhost:8002/isochrone"
payload = {
    "locations": [{"lat": center_lat, "lon": center_lon}],
    "costing": "pedestrian",
    "contours": [{"time": 120, "color": "ff0000"}],  # 10 minutes, red
    "polygons": True
}

response = requests.post(url, json=payload)
data = response.json()

# Get the polygon coordinates (first contour)
coords = data["features"][0]["geometry"]["coordinates"][0]
# Folium expects [lat, lon], so swap each pair
polygon = [[lat, lon] for lon, lat in coords]

# Create map centered on the point
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
folium.Marker([center_lat, center_lon], popup="Center", icon=folium.Icon(color="green")).add_to(m)
folium.Polygon(polygon, color="red", fill=True, fill_opacity=0.4).add_to(m)

m.save("../data/isochrone_map.html")
print("Isochrone map saved as ../data/isochrone_map.html")