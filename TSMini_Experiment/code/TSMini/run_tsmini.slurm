#!/bin/bash
#SBATCH --job-name=tsmini_train
#SBATCH --account=share-ie-idi  # Replace with your NTNU project ID (e.g., nnXXXXk)
#SBATCH --partition=GPUQ  # Use GPUQ for GPUs; CPUQ for CPU-only
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8  # Adjust as needed
#SBATCH --mem=32GB  # Adjust RAM
#SBATCH --gpus=1  # Request 1 GPU (e.g., add :a100 for specific type if needed)
#SBATCH --time=24:00:00  # Max time (adjust based on job size)
#SBATCH --output=tsmini_%j.out
#SBATCH --error=tsmini_%j.err

# Load modules
module purge
module load Python/3.11.3-GCCcore-12.3.0  # Match what you used earlier
module load CUDA/12.1.0  # If using GPUs

# Activate venv
source ~/tsmini_env/bin/activate

# Run the code (data is already in ./data)
python train_trajsimi.py --dataset porto --trajsimi_measure_fn_name frechet

