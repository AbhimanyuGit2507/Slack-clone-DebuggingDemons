# Fix corrupted database and reseed with demo data
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Fixing Corrupted Database" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$dbPath = "data\slack_rl.db"

Write-Host "[1/2] Deleting corrupted database..." -ForegroundColor Yellow
if (Test-Path $dbPath) {
    Remove-Item $dbPath -Force
    Write-Host "✓ Corrupted database deleted" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No database found at: $dbPath" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[2/2] Running seed script..." -ForegroundColor Yellow
python test_seed.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Database Fixed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Database location: data\slack_rl.db" -ForegroundColor White
Write-Host ""
Write-Host "You can now:" -ForegroundColor White
Write-Host "  1. Right-click on data\slack_rl.db → Open with SQLite Viewer" -ForegroundColor Gray
Write-Host "  2. Start backend: .\start-backend.bat" -ForegroundColor Gray
Write-Host ""
