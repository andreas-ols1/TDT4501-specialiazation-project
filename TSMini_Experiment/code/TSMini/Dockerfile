FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Install NVIDIA libraries (for pynvml, if GPU is available)
RUN pip install nvidia-ml-py

# Set working directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run TSMini
CMD ["python3", "train_trajsimi.py", "--dataset", "porto", "--trajsimi_measure_fn_name", "frechet"]