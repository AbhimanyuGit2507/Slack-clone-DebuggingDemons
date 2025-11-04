#!/bin/sh

# Startup script for Slack Clone Backend

echo "Starting Slack Clone Backend..."

# Create necessary directories
mkdir -p /app/uploads
mkdir -p /app/data

# Determine DB path used by the app (matches backend/database.py default)
DB_FILE=/app/data/slack_rl.db
if [ ! -f "$DB_FILE" ]; then
    echo "Database not found at $DB_FILE. Initializing tables..."
    # run seeder from repository root
    python backend/seed.py
    echo "Database initialized successfully!"
else
    echo "Database already exists at $DB_FILE. Skipping initialization."
fi

# Start the application
echo "Starting Uvicorn server..."
# Use PORT environment variable from Render, default to 8000
PORT=${PORT:-8000}
# Run uvicorn with the package module path so relative imports work
exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT
