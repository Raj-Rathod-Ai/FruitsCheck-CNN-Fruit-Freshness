# ============================================================
# FruitCheck — Hugging Face Spaces Dockerfile (FastAPI Backend)
#
# Hugging Face Spaces runs containers on port 7860.
# The internal $SPACE_PORT env var is automatically set to 7860.
# ============================================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY main.py .

# Copy model — stored in the backend/models/ folder
COPY models/ ./models/

# Hugging Face Spaces ALWAYS uses port 7860
EXPOSE 7860

# Single-worker Uvicorn to keep one model copy in memory
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
