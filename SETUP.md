# Setup Guide - Slack Clone

Complete guide for setting up and running the Slack Clone application.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Docker Setup (Recommended)](#docker-setup-recommended)
- [Manual Setup](#manual-setup)
- [Database Initialization](#database-initialization)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### For Docker Setup
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- Git

### For Manual Setup
- Node.js 18+ and npm
- Python 3.11+
- Git

## Docker Setup (Recommended)

This is the easiest way to get started. Docker will handle all dependencies and configuration.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/slack-rl-clone.git
cd slack-rl-clone
```

### Step 2: Build and Start Services

```bash
docker-compose up --build
```

**What this does:**
- Builds Docker images for frontend and backend
- Creates a SQLite database
- Seeds the database with sample data
- Starts both services

### Step 3: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Step 4: Stop the Application

Press `Ctrl+C` in the terminal, then run:

```bash
docker-compose down
```

### Step 5: Clean Up (Optional)

To remove all containers, networks, and volumes:

```bash
docker-compose down -v
```

## Manual Setup

If you prefer to run the services directly without Docker:

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database with sample data:**
   ```bash
   python seed.py
   ```

5. **Start the backend server:**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at http://localhost:8000

### Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file (optional):**
   ```bash
   # Create .env file in frontend directory
   echo "VITE_API_URL=http://localhost:8000" > .env
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

   The application will be available at http://localhost:5173

## Database Initialization

The application uses SQLite for data storage. Sample data is automatically created when you run the seed script.

### Sample Data Includes:

**Users:**
- Alice Johnson (alice@example.com)
- Bob Smith (bob@example.com)
- Charlie Brown (charlie@example.com)
- Diana Prince (diana@example.com)
- Eve Davis (eve@example.com)

**Channels:**
- #general - Main discussion channel
- #random - For off-topic conversations
- #development - Tech discussions

**Features:**
- Sample messages in each channel
- Direct message conversations
- Canvas documents for collaboration
- Starred items and favorites

### Resetting the Database

If you want to start fresh:

**With Docker:**
```bash
docker-compose down -v
docker-compose up --build
```

**Manual Setup:**
```bash
cd backend
rm slack.db  # Delete existing database
python seed.py  # Recreate with sample data
```

## Configuration

### Backend Configuration

Create a `.env` file in the `backend` directory:

```env
# Database
DATABASE_URL=sqlite:///./slack.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# CORS (optional)
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Configuration

Create a `.env` file in the `frontend` directory:

```env
# API URL
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Docker Issues

**Problem: Port already in use**
```
Error: bind: address already in use
```

**Solution:** Stop services using the ports or change ports in `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change external port
  frontend:
    ports:
      - "5174:5173"  # Change external port
```

**Problem: Docker daemon not running**
```
Error: Cannot connect to the Docker daemon
```

**Solution:** Start Docker Desktop or Docker service

---

**Problem: Build fails**
```
Error: failed to build
```

**Solution:** Clear Docker cache and rebuild:
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

### Backend Issues

**Problem: Module not found**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:** Activate virtual environment and reinstall:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

---

**Problem: Database locked**
```
sqlite3.OperationalError: database is locked
```

**Solution:** Close all applications accessing the database and restart

---

**Problem: Port 8000 already in use**
```
ERROR: [Errno 48] error while attempting to bind on address
```

**Solution:** Change port in uvicorn command:
```bash
uvicorn main:app --reload --port 8001
```

### Frontend Issues

**Problem: npm install fails**
```
npm ERR! code ERESOLVE
```

**Solution:** Use legacy peer dependencies:
```bash
npm install --legacy-peer-deps
```

---

**Problem: Vite dev server won't start**
```
Error: Failed to start dev server
```

**Solution:** Clear cache and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

**Problem: Cannot connect to backend**
```
Network Error or CORS error in console
```

**Solution:** 
1. Verify backend is running on http://localhost:8000
2. Check VITE_API_URL in `.env`
3. Verify CORS settings in backend `main.py`

### General Issues

**Problem: Changes not reflecting**

**Solution:**
- Hard refresh browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Clear browser cache
- Restart dev servers

---

**Problem: Sample data not showing**

**Solution:**
```bash
cd backend
python seed.py
```

---

**Problem: Images/files not loading**

**Solution:**
- Check uploads directory exists: `backend/uploads/`
- Verify file permissions
- Check CORS settings

## Development Tips

### Hot Reloading

Both services support hot reloading:
- **Backend**: Auto-reloads when Python files change
- **Frontend**: Auto-reloads when React components change

### API Testing

Use the built-in Swagger UI for API testing:
http://localhost:8000/docs

### Database Browser

To view/edit the SQLite database, use tools like:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [SQLite Viewer VS Code Extension](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)

### Debugging

**Backend:**
- Add print statements or use Python debugger
- Check logs in terminal running uvicorn
- Use FastAPI's `/docs` for request/response inspection

**Frontend:**
- Use React DevTools browser extension
- Check browser console for errors
- Use Network tab to inspect API calls

## Production Deployment

For production deployment, you should:

1. **Use PostgreSQL instead of SQLite**
   - Update DATABASE_URL in backend
   - Install psycopg2-binary

2. **Build frontend for production**
   ```bash
   cd frontend
   npm run build
   ```

3. **Use proper secrets**
   - Generate strong SECRET_KEY
   - Use environment variables
   - Don't commit .env files

4. **Enable authentication**
   - Uncomment auth routes in App.jsx
   - Implement JWT token validation
   - Add password hashing

5. **Use production web server**
   - Gunicorn or similar for backend
   - Nginx for frontend static files

6. **Add HTTPS**
   - Use Let's Encrypt certificates
   - Configure SSL/TLS

## Need Help?

- Check the [README.md](README.md) for features and architecture
- Review API documentation at http://localhost:8000/docs
- Open an issue on GitHub

---

**Happy coding! 🚀**
