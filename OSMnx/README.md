# OSMnx Project Folder

This folder contains scripts and data for working with OSMnx, a Python package for downloading, modeling, analyzing, and visualizing street networks from OpenStreetMap. The focus is on generating Andorra's road network, creating trajectories, and visualizing them to support a trajectory similarity efficiency study, inspired by the paper "Trajectory Similarity Measurement: An Efficiency Perspective" (arXiv:2311.00960v3).

## What is Being Done
- **Network Modeling**: Downloads and models Andorra's street network using OSMnx.
- **Trajectory Generation**: Computes shortest paths (trajectories) on the network based on travel time.
- **Visualization**: Creates graphs showing the network with trajectories highlighted, including centrality-based coloring and node labels.
- **Similarity Analysis**: Implements a basic Hausdorff distance measure to quantify similarity between trajectories, aligning with the paper's non-learned measures.

## How to Run
1. **Prerequisites**:
   - Install Docker: Follow instructions at https://docs.docker.com/get-docker/.
   - Ensure Docker is running (`docker --version` to verify).

2. **Run the Script**:
   - Open a terminal in VSCode within this `OSMnx` folder (`C:\TDT4501-specialization\TDT4501-specialiazation-project\OSMnx`).
   - Execute the following command in PowerShell:
   - docker run --rm -it -v "${PWD}:/home/jovyan/work" -w /home/jovyan/work gboeing/osmnx python osmnx_test.py

   - **Notes**:
- This pulls the `gboeing/osmnx` Docker image (if not already present) and runs the `osmnx_test.py` script.
- The `-v "${PWD}:/home/jovyan/work"` mounts the local folder to the container, and `-w` sets the working directory.
- If `${PWD}` doesn’t work, use `$(Get-Location)` instead:
- docker run --rm -it -v "$(Get-Location):/home/jovyan/work" -w /home/jovyan/work gboeing/osmnx python osmnx_test.py

3. **Output**:
   - Generated files will appear in the `OSMnx` folder:
     - `andorra_network_with_trajectories.png`: A network plot of Andorra's street system, visualized as a graph where nodes represent intersections or endpoints, and edges represent road segments. This image highlights two trajectories:
       - **Trajectory 1** (red line): A shortest path computed between two randomly selected nodes (e.g., node indices 0 and 10) based on travel time, representing a sequence of timestamped or spatial point locations (as defined in the paper, Section 2, Table 1). This trajectory captures a potential movement path, such as a route from one town to another.
       - **Trajectory 2** (blue line): A second shortest path (e.g., between node indices 5 and 15), providing a comparative route to assess similarity or divergence. The overlap or separation of these paths visually suggests potential similarity, which can be quantified (see Hausdorff distance below).
       - The plot includes labeled nodes (e.g., start/end points) in white text, enhancing interpretability by marking key locations.
     - `andorra_centrality_with_trajectories.png`: An enhanced network plot where nodes are colored according to betweenness centrality (using a plasma colormap), a measure of a node's importance in the network based on the number of shortest paths passing through it (relevant to kNN queries in the paper, Section 3). The same red and blue trajectories are overlaid, allowing you to see how critical paths align with network structure. Node labels are included for key points.
     - `andorra_graph.gpkg`: A GeoPackage file containing the complete Andorra street network as a MultiDiGraph, including node coordinates (x, y) and edge attributes like travel times. This file can be used for further analysis or integration with tools like Valhalla.
   - **Console Output**:
     - Displays the node sequences of the sample trajectories (e.g., `[625030, 3699555986, ...]`), representing the ordered list of nodes traversed, as per the paper's trajectory definition (Section 2).
     - Includes the **Hausdorff distance** between Trajectory 1 and Trajectory 2, a non-learned similarity measure (paper, Fig. 1) that calculates the maximum perpendicular distance between any point on one trajectory to the nearest point on the other. This value (e.g., in meters) indicates how dissimilar the trajectories are, with lower values suggesting greater similarity. The paper notes this measure’s quadratic time complexity (O(n²)), making it a baseline for efficiency comparisons with learned measures.
   - **What is Being Plotted**:
     - The graphs visualize the spatial structure of Andorra’s road network, derived from OpenStreetMap data via OSMnx. Trajectories are plotted as polylines connecting node coordinates, reflecting movement paths that could represent vehicle or pedestrian routes.
     - Betweenness centrality coloring highlights network hubs, which could influence trajectory similarity queries (e.g., kNN, Section 3 of the paper).
     - The inclusion of multiple trajectories and their Hausdorff distance ties directly to the paper’s focus on quantifying trajectory similarity, providing a visual and numerical foundation for your efficiency analysis in the thesis.


4. **Customization**:
- Edit `osmnx_test.py` to adjust `place` (e.g., change to another region), `network_type` (e.g., "walk"), or node indices for trajectories.
- Update `important_nodes` with specific Andorra town IDs if known.

## Notes
- **Dependencies**: All required packages (OSMnx, NetworkX, Matplotlib) are included in the `gboeing/osmnx` Docker image.
- **Internet Access**: Required for initial OSM data download (cached afterward).
- **Troubleshooting**:
- If "invalid reference format" occurs, ensure the path is correct or use the `Get-Location` alternative.
- Check Docker logs or add `--debug` to the command for more details if errors persist.

## Future Work
- Integrate with the `andorra_valhalla` folder to use Valhalla-generated trajectories.
- Expand similarity analysis with learned measures (e.g., T3S) and visualize runtime/accuracy comparisons.
- Enhance graphs with additional metrics or interactive plotting.
