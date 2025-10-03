import networkx as nx
import osmnx as ox
import matplotlib

matplotlib.use('Agg')  # Non-interactive backend

ox.settings.use_cache = True

# Download Andorra street network
place = "Andorra"
G = ox.graph_from_place(place, network_type="drive")

# Add edge speeds and travel times
G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

# Generate sample trajectory (shortest path between random nodes)
nodes = list(G.nodes)
source, target = nodes[0], nodes[10]  # Adjust indices as needed
trajectory = nx.shortest_path(G, source, target, weight='travel_time')
print(f"Sample trajectory: {trajectory}")

# Multiple Trajectories
trajectory2 = nx.shortest_path(G, nodes[5], nodes[15], weight='travel_time')
traj2_points = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in trajectory2]

# Convert to DiGraph for centrality calculation
D = ox.convert.to_digraph(G, weight="travel_time")
bc = nx.betweenness_centrality(D, weight="travel_time", normalized=True)
nx.set_node_attributes(G, values=bc, name="bc")

# Plot 1: Network with trajectories highlighted
nc = ['gray'] * len(G.nodes)  # Default gray color if no attribute used directly
fig, ax = ox.plot_graph(
    G, bgcolor="k", node_color=nc, node_size=30, edge_linewidth=1, edge_color="#333333"
)
trajectory_points = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in trajectory]
ax.plot(*zip(*trajectory_points), color="r", linewidth=2, label="Trajectory 1")
ax.plot(*zip(*traj2_points), color="b", linewidth=2, label="Trajectory 2")

# Add Node Labels or Key Locations
important_nodes = [nodes[0], nodes[10]]  # Example, adjust with real data (e.g., towns)
for node in important_nodes:
    x, y = G.nodes[node]['x'], G.nodes[node]['y']
    ax.text(x, y, str(node), color="w", fontsize=8)

ax.legend()
fig.savefig("andorra_network_with_trajectories.png", dpi=300, bbox_inches="tight")

# Plot 2: Network colored by betweenness centrality
nc_bc = ox.plot.get_node_colors_by_attr(G, attr="bc", cmap="plasma")
fig_bc, ax_bc = ox.plot_graph(
    G, bgcolor="k", node_color=nc_bc, node_size=50, edge_linewidth=2, edge_color="#333333"
)
ax_bc.plot(*zip(*trajectory_points), color="r", linewidth=2, label="Trajectory 1")
ax_bc.plot(*zip(*traj2_points), color="b", linewidth=2, label="Trajectory 2")

# Add Node Labels or Key Locations for second plot
for node in important_nodes:
    x, y = G.nodes[node]['x'], G.nodes[node]['y']
    ax_bc.text(x, y, str(node), color="w", fontsize=8)

ax_bc.legend()
fig_bc.savefig("andorra_centrality_with_trajectories.png", dpi=300, bbox_inches="tight")

# Similarity Visualization
def hausdorff_distance(T1, T2):
    max_dist = 0
    for p1 in T1:
        min_dist = min(((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5 for p2 in T2)
        max_dist = max(max_dist, min_dist)
    for p2 in T2:
        min_dist = min(((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5 for p1 in T1)
        max_dist = max(max_dist, min_dist)
    return max_dist

dist = hausdorff_distance(trajectory_points, traj2_points)
print(f"Hausdorff distance between Trajectory 1 and Trajectory 2: {dist}")
# Placeholder for bar chart (expand later with multiple distances and a plotting library)

# Save graph
ox.save_graph_geopackage(G, filepath="andorra_graph.gpkg")
print("Graphs and graph file saved.")