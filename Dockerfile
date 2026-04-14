# ============================================================
# Dockerfile — trending-repos CLI tool
# ============================================================
# Build:  docker build -t trending-repos .
# Run:    docker run --rm trending-repos
#         docker run --rm trending-repos --duration day --limit 5
#         docker run --rm trending-repos --duration week --language python
# ============================================================

# --- Stage 1: Base image ---
# Use a slim Python 3.11 image to keep the final image small
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="Your Name"
LABEL description="A CLI tool to discover trending GitHub repositories"
LABEL version="1.0.0"

# --- Environment setup ---
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to terminal (no buffering)
ENV PYTHONUNBUFFERED=1

# --- Working directory ---
WORKDIR /app

# --- Install dependencies ---
# Copy requirements first to leverage Docker layer caching.
# This layer only re-builds when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- Copy project files ---
COPY setup.py .
COPY trending_repos/ ./trending_repos/

# --- Install the package as a CLI command ---
# This registers the 'trending-repos' entry point defined in setup.py
RUN pip install --no-cache-dir -e .

# --- Default command ---
# Running the container with no extra args executes:
#   trending-repos --duration week --limit 10
# You can override by appending flags after the image name.
ENTRYPOINT ["trending-repos"]
CMD ["--duration", "week", "--limit", "10"]
