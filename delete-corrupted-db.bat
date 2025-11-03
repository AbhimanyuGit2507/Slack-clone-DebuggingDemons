@echo off
echo ========================================
echo  Deleting Corrupted Database
echo ========================================
echo.

cd /d "%~dp0"

if exist "data\slack_rl.db" (
    echo Found corrupted database...
    del /F "data\slack_rl.db"
    echo ✓ Database deleted successfully!
) else (
    echo ✓ No database file found (already deleted)
)

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo To create a fresh database, do ONE of these:
echo.
echo 1. Double-click on: start-backend.bat
echo    (This will create the database and start the server)
echo.
echo 2. OR ask the Live Share host to run:
echo    python -m uvicorn backend.main:app --reload --port 8000
echo.
echo The database will be automatically created with 15 demo users!
echo.
pause
