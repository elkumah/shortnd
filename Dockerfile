# ============================================================
# Stage 1: Builder
# ============================================================
FROM python:3.14-slim AS builder

WORKDIR /build

# Copy dependency definition first for better Docker caching
COPY api/requirements.txt .

# Install application dependencies into a separate directory.
# pip remains available only in the builder stage.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================================================
# Stage 2: Runtime
# ============================================================
FROM python:3.14-slim AS runtime

# Update OS packages and clean apt cache
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only application dependencies from the builder.
COPY --from=builder /install /usr/local

# Remove pip and its metadata from the runtime image.
# pip is only required during the build stage.
RUN rm -rf \
    /usr/local/lib/python3.14/site-packages/pip \
    /usr/local/lib/python3.14/site-packages/pip-*.dist-info \
    /usr/local/bin/pip \
    /usr/local/bin/pip3 \
    /usr/local/bin/pip3.14

# Copy application source code
COPY api/app ./app

# Create a non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

# Run as non-root user
USER appuser

# FastAPI/Uvicorn listens on port 8000
EXPOSE 8000

# Start the Shortnd API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]