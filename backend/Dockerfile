FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/uploads

# Initialize database with sample data (optional, will run on first startup if needed)
RUN python seed.py || echo "Database seeding skipped or failed - will retry on startup"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/docs || exit 1

# Run the application directly with uvicorn
CMD ["sh", "-c", "python seed.py || true && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
