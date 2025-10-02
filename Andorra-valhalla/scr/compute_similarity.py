import json
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("C:/Andorra_valhalla/TrajSimiMeasures")
sys.path.append("C:/Andorra_valhalla/TrajSimiMeasures/core")

from core.dtw import dtw
from core.hausdorff import hausdorff

# Add the TrajSimiMeasures directory to the Python path
sys.path.append("C:/Andorra_valhalla/TrajSimiMeasures")

# Load trajectories
with open("C:/Andorra_valhalla/andorra_trajectories.json", "r") as f:
    trajectories = json.load(f)

# Extract points as NumPy arrays for the first two trajectories
traj1_points = np.array([(p["lat"], p["lon"]) for p in trajectories[0]["points"]])
traj2_points = np.array([(p["lat"], p["lon"]) for p in trajectories[1]["points"]])

print(f"Trajectory 1: {len(traj1_points)} points, Distance: {trajectories[0]['distance']} km")
print(f"Trajectory 2: {len(traj2_points)} points, Distance: {trajectories[1]['distance']} km")

# Compute DTW and Hausdorff distances
# Remove length arguments; let the function infer sizes
distance_dtw = dtw(traj1_points, traj2_points)
distance_hausdorff = hausdorff(traj1_points, traj2_points)
print(f"DTW Distance (Euclidean): {distance_dtw}")
print(f"Hausdorff Distance (Euclidean): {distance_hausdorff}")

# Visualize trajectories
fig, ax = plt.subplots(figsize=(8, 6))
base_lat, base_lon = traj1_points[0]
ax.plot([p[0] - base_lat for p in traj1_points], [p[1] - base_lon for p in traj1_points], 'b-o', label='Trajectory 1', markersize=4)
ax.plot([p[0] - base_lat for p in traj2_points], [p[1] - base_lon for p in traj2_points], 'r-s', label='Trajectory 2', markersize=4)
ax.set_xlabel('Latitude Offset (degrees)')
ax.set_ylabel('Longitude Offset (degrees)')
ax.set_title('Andorra Trajectories (Relative)')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.show()