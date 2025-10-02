import requests
import random

# Valhalla server URL
url = "http://localhost:8002/route"

# Define a small grid of points in Andorra for sampling (adjust as needed)
andorra_points = [
    {"lat": 42.5075, "lon": 1.5218},  # Carrer de la Grau
    {"lat": 42.5063, "lon": 1.5211},  # Avinguda Prat de la Creu
    {"lat": 42.5080, "lon": 1.5230},  # Nearby point 1
    {"lat": 42.5050, "lon": 1.5200}   # Nearby point 2
]

# Function to generate a trajectory between two random points
def generate_trajectory(start_idx, end_idx):
    start_point = andorra_points[start_idx]
    end_point = andorra_points[end_idx]
    
    payload = {
        "locations": [
            {"lat": start_point["lat"], "lon": start_point["lon"]},
            {"lat": end_point["lat"], "lon": end_point["lon"]}
        ],
        "costing": "pedestrian",
        "directions_options": {"units": "kilometers"}
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Routing failed. Status code: {response.status_code}")
    data = response.json()

    leg = data["trip"]["legs"][0]
    trajectory = []
    for maneuver in leg["maneuvers"]:
        # Approximate points along the route (simplified; use shape for precision)
        trajectory.append({
            "lat": maneuver["begin_shape_index_lat"] if "begin_shape_index_lat" in maneuver else start_point["lat"],
            "lon": maneuver["begin_shape_index_lon"] if "begin_shape_index_lon" in maneuver else start_point["lon"]
        })
    return trajectory, leg["summary"]["length"], leg["summary"]["time"]

# Generate a few sample trajectories
num_trajectories = 3
trajectories = []
for _ in range(num_trajectories):
    start_idx = random.randint(0, len(andorra_points) - 2)
    end_idx = random.randint(start_idx + 1, len(andorra_points) - 1)
    traj, dist, dur = generate_trajectory(start_idx, end_idx)
    trajectories.append({"points": traj, "distance": dist, "duration": dur})
    print(f"Trajectory {_ + 1}: Distance = {dist} km, Duration = {dur/60:.1f} minutes")
    for i, point in enumerate(traj):
        print(f"  Point {i}: lat={point['lat']}, lon={point['lon']}")

# Save trajectories for later analysis (e.g., CSV or JSON)
import json
with open("andorra_trajectories.json", "w") as f:
    json.dump(trajectories, f)