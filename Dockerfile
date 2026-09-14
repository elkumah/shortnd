# ============================================================
# Stage 1: Builder
# ============================================================
FROM python:3.14-slim AS builder

WORKDIR /build

# Copy dependency definition first for better Docker caching
COPY api/requirements.txt .

# Install Python dependencies into a separate directory.
# They will be copied into the runtime image later.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================================================
# Stage 2: Runtime
# ============================================================
FROM python:3.14-slim AS runtime

WORKDIR /app

# Copy only the installed Python dependencies
# from the builder stage.
COPY --from=builder /install /usr/local

# Copy only the application source code
COPY api/app ./app

# Create a non-root user for running the application
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

# Run the application as a non-root user
USER appuser

# FastAPI/Uvicorn listens on port 8000
EXPOSE 8000

# Start the Shortnd API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]