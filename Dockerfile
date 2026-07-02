# ========================================================
# Stage 1 - Build Dependencies
# ========================================================
FROM python:3.12-slim-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
        gcc \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install Python packages
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ========================================================
# Stage 2 - Production
# ========================================================
FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Runtime dependency only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd --system appgroup && \
    useradd --system \
    --gid appgroup \
    --create-home \
    --home-dir /home/appuser \
    appuser

# Create required directories
RUN mkdir -p /app/logs

# Copy source
COPY ./app ./app

# Permissions
RUN chown -R appuser:appgroup /app

USER appuser

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]