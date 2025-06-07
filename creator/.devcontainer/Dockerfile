# .devcontainer/Dockerfile
FROM python:3.10-slim

# System packages
RUN apt-get update && apt-get install -y \
    curl git build-essential && \
    apt-get clean

# Install Ollama CLI (if you want to use it inside the container)
RUN curl -fsSL https://ollama.com/install.sh | sh || true

# Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

WORKDIR /workspace
