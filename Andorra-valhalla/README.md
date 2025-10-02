# Andorra_valhalla: Trajectory Generation and Testing with Valhalla

This folder contains a module for generating and analyzing pedestrian trajectories in Andorra using Valhalla, an open-source routing engine, as part of a broader master's thesis project on trajectory similarity measurement.

## Overview
- **Purpose**: Generate road-constrained trajectories using Valhalla's Docker setup, compute similarities (e.g., DTW, Hausdorff) with TrajSimiMeasures, and visualize results. This serves as a testbed for the paper "Trajectory Similarity Measurement: An Efficiency Perspective" (2024).
- **Key Components**:
  - Valhalla Docker for routing.
  - Python scripts in `src/` for trajectory generation, similarity computation, and mapping.
  - Data and configs in `data/` and `custom_files/`.

## Prerequisites
- Docker (for Valhalla server).
- Python 3.9+ with pip.
- NVIDIA GPU with CUDA (optional for GPU-accelerated DTW; falls back to CPU).
- Download Andorra OSM data: [andorra-latest.osm.pbf](https://download.geofabrik.de/europe/andorra-latest.osm.pbf) (~3.1 MB). Place in `custom_files/` (excluded from git; see `.gitignore`).

## Setup Instructions
1. **Clone the Repository**:
- git clone https://github.com/andreas-ols1/TDT4501-specialiazation-project.git
- cd TDT4501-specialiazation-project
- git submodule update --init --recursive  # Initialize TrajSimiMeasures submodule

2. **Set Up Valhalla Docker**:
- Ensure `custom_files/valhalla.json` is present and updated (e.g., paths).
- Run Valhalla Docker from the root:
- docker run -dt --name valhalla_andorra -p 8002:8002 
- v "$(pwd)/Andorra_valhalla/custom_files:/custom_files"
- ghcr.io/gis-ops/valhalla:latest 
- valhalla_run_map -c /custom_files/valhalla.json
- Verify: `curl http://localhost:8002/status` should respond.

3. **Install Python Dependencies**:
- pip install requests folium polyline numpy matplotlib numba scipy cython
- Install TrajSimiMeasures (from root submodule):
- cd ../TrajSimiMeasures
- pip install -e .
- cd ../Andorra_valhalla

## Usage
1. **Generate Trajectories**:
- Run:
- python src/generate_trajectories.py

- Outputs: `data/andorra_trajectories.json` with points, distances, durations.

2. **Compute Similarities**:
- Run:
- python src/compute_similarity.py
- Outputs: DTW/Hausdorff distances printed; relative plot shown/saved as PNG.

3. **Test Valhalla Routing**:
- Run:
- python src/valhalla_test.py
- Outputs: Distance, duration, and turn-by-turn instructions.

4. **Generate Maps**:
- `src/route_map.py`: Creates `route_map.html`.
- `src/isochrone_map.py`: Creates `isochrone_map.html`.
- Run each with: `python src/<script_name>.py`.

## Testing with Valhalla
- **Verification**: Use `src/valhalla_test.py` to confirm routing works (e.g., auto mode from 42.5075, 1.5218 to 42.5063, 1.5211).
- **Debugging**: Check Docker logs (`docker logs valhalla_andorra`) if `localhost:8002` fails.
- **Expand**: Add more points to `src/generate_trajectories.py` or switch costing (e.g., "auto") in scripts.

## References
- Paper: "Trajectory Similarity Measurement: An Efficiency Perspective" (arXiv:2311.00960v3, 2024). See `docs/trajectory_paper_page1.pdf` for intro.
- Valhalla: https://github.com/valhalla/valhalla
- TrajSimiMeasures: https://github.com/changyanchuan/TrajSimiMeasures (root submodule)

## License
MIT License

If issues, open a GitHub issue in the root repository!