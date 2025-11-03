#!/bin/sh

# Startup script for Slack Clone Backend

echo "Starting Slack Clone Backend..."

# Create necessary directories
mkdir -p /app/uploads
mkdir -p /app/data

# Check if database exists, if not create it
if [ ! -f "/app/slack.db" ]; then
    echo "Database not found. Initializing with sample data..."
    python seed.py
    echo "Database initialized successfully!"
else
    echo "Database already exists. Skipping initialization."
fi

# Start the application
echo "Starting Uvicorn server..."
# Use PORT environment variable from Render, default to 8000
PORT=${PORT:-8000}
exec uvicorn main:app --host 0.0.0.0 --port $PORT
