# Start from NVIDIA's CUDA image (Debian-based, includes cuDNN & repo)
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Optional: Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Python manually
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3-pip python3-dev python3-venv wget curl python-is-python3

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"
