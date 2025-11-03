@echo off
echo ========================================
echo  Fixing Corrupted Database
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Deleting corrupted database...
if exist "data\slack_rl.db" (
    del "data\slack_rl.db"
    echo ✓ Corrupted database deleted
) else (
    echo ✓ No database found
)

echo.
echo [2/2] Running seed script to create fresh database...
python test_seed.py

echo.
echo ========================================
echo Database has been recreated!
echo ========================================
echo.
echo You can now:
echo 1. View the database using SQLite Viewer
echo 2. Start the backend server with: start-backend.bat
echo.
pause
