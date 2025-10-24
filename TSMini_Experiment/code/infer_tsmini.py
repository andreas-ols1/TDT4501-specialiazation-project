import torch
import sys
import numpy as np
from scipy.spatial.distance import euclidean, directed_hausdorff

sys.path.append("./TSMini")
from model.tsmini import TSMini

torch.manual_seed(42)
np.random.seed(42)

# Load model
model_path = "exp/snapshots/porto_20200_trajsimi_TSMini_frechet_best.pt"
checkpoint = torch.load(model_path, map_location=torch.device("cpu"))
model = TSMini()
model.load_state_dict(checkpoint["encoder"])
model.eval()

# Load Porto dataset (placeholder, replace with actual data)
def load_porto_data():
    # Dummy data: [batch_size, seq_len, 7 features]
    trajs = torch.randn(2, 100, 7)  # 2 trajectories, 100 timesteps, 7 features
    trajs_len = torch.tensor([100, 90])  # Variable lengths
    return trajs, trajs_len

# Get trajectories
trajs, trajs_len = load_porto_data()
print("Input trajs shape:", trajs.shape)  # Should be [2, 100, 7]

# Normalize trajectories (lon, lat) to [0, 1] for Hausdorff
trajs_norm = trajs.clone()
trajs_norm[:, :, :2] = (trajs[:, :, :2] - trajs[:, :, :2].min()) / (trajs[:, :, :2].max() - trajs[:, :, :2].min() + 1e-8)

# Get embeddings
try:
    with torch.no_grad():
        embeddings = model(trajs, trajs_len)
    print("Embeddings shape:", embeddings.shape)  # Expected: [2, 128]
    print("Sample embedding (first 5 dims):", embeddings[0, :5])

    # Compute learned similarity (Euclidean distance on embeddings)
    embedding_dist = euclidean(embeddings[0].numpy(), embeddings[1].numpy())
    print("Euclidean distance (embeddings):", embedding_dist)

# Non-learned similarity (Hausdorff on normalized lon, lat)
    traj1 = trajs_norm[0, :trajs_len[0], :2].numpy()
    traj2 = trajs_norm[1, :trajs_len[1], :2].numpy()
    hausdorff_dist = max(directed_hausdorff(traj1, traj2)[0], directed_hausdorff(traj2, traj1)[0])
    print("Hausdorff distance (normalized trajectories):", hausdorff_dist)  # ~[0, 1]

    # Compare (normalize for qualitative comparison)
    print("Comparison: Learned (Euclidean) vs. Non-learned (Hausdorff)")
    print(f"Ratio (Euclidean/Hausdorff): {embedding_dist / hausdorff_dist if hausdorff_dist != 0 else 'N/A'}")
except RuntimeError as e:
    print("Error during forward pass:", e)
    print("Check input shape or model/embeder.py forward method")