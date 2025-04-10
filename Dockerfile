FROM python:3.12-slim

# Install system dependencies early to leverage Docker layer caching
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first to cache the layer
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Default to 4 workers but allow override at runtime
ENV WORKERS=4

# Launch Gunicorn with Uvicorn workers
CMD ["sh", "-c", "gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w $(nproc) --keep-alive 120 --bind 0.0.0.0:8000"]
