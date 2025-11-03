@echo off
echo ========================================
echo  Slack RL Clone - Frontend Setup
echo ========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo [1/2] Installing npm dependencies...
    call npm install
) else (
    echo [1/2] Dependencies already installed, skipping...
)

echo [2/2] Starting frontend dev server...
echo.
echo Frontend will run on: http://localhost:5173
echo Press CTRL+C to stop the server
echo.
call npm run dev
