# ==============================================================================
# TrustChain-AI FastAPI Backend Dockerfile
# Base: Python 3.12-slim (Secure, minimal footprint)
# ==============================================================================

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOST=0.0.0.0 \
    APP_PORT=8050

WORKDIR /app

# Install system packages (curl for container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application source and initialization scripts
COPY akta/ /app/akta/
COPY scripts/ /app/scripts/
COPY pyproject.toml /app/pyproject.toml
COPY .env.example /app/.env.example

# Create storage directory for SQLite persistence
RUN mkdir -p /app/data && chown -R 1000:1000 /app

USER 1000:1000

EXPOSE 8050

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8050/health || exit 1

CMD ["python", "-m", "uvicorn", "akta.server:app", "--host", "0.0.0.0", "--port", "8050"]
