@echo off
echo ========================================
echo  Slack RL Clone - Backend Setup
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking for .env file...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file if you need custom settings
    echo.
)

echo [2/3] Installing backend dependencies...
pip install -r requirements.txt

echo [3/3] Starting backend server...
echo.
echo ========================================
echo Backend is running on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo ========================================
echo.
echo Press CTRL+C to stop the server
echo.
python -m uvicorn backend.main:app --reload --port 8000
