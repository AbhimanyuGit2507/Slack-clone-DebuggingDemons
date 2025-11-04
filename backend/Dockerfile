FROM python:3.11-slim

# Work in the repository root so the backend package is available at /app/backend
WORKDIR /app

# Install system deps required for some Python packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential gcc libpq-dev curl \
  && rm -rf /var/lib/apt/lists/*

# Copy backend sources and data
COPY backend/ ./backend/
COPY data/ ./data/

# Install Python deps (use backend requirements file)
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r backend/requirements.txt

# Set PYTHONPATH to ensure modules are discoverable
ENV PYTHONPATH=/app

# Ensure directories exist for runtime
RUN mkdir -p /app/data /app/uploads

# Try to initialize the DB at build time; if it fails we'll seed on startup
RUN python backend/seed.py || echo "Database seeding skipped (will run at container startup)"

ENV PORT=8000
EXPOSE 8000

# use startup script so database seeding runs at container start and PORT env is honored
CMD ["sh","-c","chmod +x ./backend/start.sh && sed -i 's/\\r$//' ./backend/start.sh || true && ./backend/start.sh"]
