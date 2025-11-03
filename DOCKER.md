# Docker Setup Guide

## Prerequisites
- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. Build and Start Containers
```bash
docker-compose up --build
```

### 2. Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 3. Stop Containers
```bash
docker-compose down
```

## Common Issues and Solutions

### Issue 1: Backend Container Fails with "no such file or directory"
**Cause:** Windows line endings (CRLF) in shell scripts

**Solution:**
The Dockerfile now runs the application directly without shell scripts. If you still encounter issues:

1. Ensure Docker Desktop is using Linux containers (not Windows containers)
2. Rebuild without cache:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```

### Issue 2: "Container is unhealthy"
**Cause:** Backend takes time to start

**Solution:**
Wait 30-60 seconds for the health check to pass. The backend needs to:
- Initialize the database
- Run seed data
- Start the uvicorn server

### Issue 3: Database Not Persisting
**Cause:** Volume not properly mounted

**Solution:**
Check volumes in docker-compose.yml:
```yaml
volumes:
  - backend-data:/app
```

To reset the database:
```bash
docker-compose down -v  # Removes volumes
docker-compose up --build
```

### Issue 4: Port Already in Use
**Cause:** Ports 5173 or 8000 are occupied

**Solution:**
Either stop the conflicting service or change ports in docker-compose.yml:
```yaml
ports:
  - "3000:5173"  # Use port 3000 instead
  - "8080:8000"  # Use port 8080 instead
```

## Development Mode

To run with hot reload for development:

### Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Production Deployment

### Using Docker
```bash
docker-compose -f docker-compose.yml up -d
```

### Using Render (recommended)
See main README.md for Render deployment instructions.

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./slack.db
SECRET_KEY=your-secret-key-here
PORT=8000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## Troubleshooting Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart backend

# Enter container shell
docker exec -it slack-backend sh
docker exec -it slack-frontend sh

# Remove all containers and volumes
docker-compose down -v --remove-orphans
```

## Health Checks

The backend includes a health check that:
- Runs every 30 seconds
- Checks if the API documentation is accessible
- Marks container as healthy after successful checks

Frontend waits for backend to be healthy before starting.
