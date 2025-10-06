# syntax=docker/dockerfile:1

# Python Docker deployment best practices with uv package manager
# Multi-stage build for minimal image size and security

# Stage 1: Builder - Install dependencies
FROM python:3.12-slim AS builder

# Install uv - fast Python package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv sync
# --frozen: use exact versions from uv.lock (reproducible builds)
# --no-dev: exclude dev dependencies for production
RUN uv sync --frozen --no-dev

# Stage 2: Runtime - Minimal production image
FROM python:3.12-slim

# Install security updates and clean up in one layer
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r ddgs && \
    useradd -r -g ddgs -u 1000 -m -s /bin/bash ddgs

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=ddgs:ddgs /app/.venv /app/.venv

# Copy application code
COPY --chown=ddgs:ddgs app ./app

# Switch to non-root user
USER ddgs

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # FastAPI defaults
    HOST=0.0.0.0 \
    PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz').read()"

# Run FastAPI application with uvicorn
# Use uvicorn instead of fastapi dev for production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
