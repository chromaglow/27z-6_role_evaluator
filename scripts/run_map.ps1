# Run from repo root
$ErrorActionPreference = "Stop"

Write-Host "Building map data..." -ForegroundColor Cyan
& "$PSScriptRoot\build_map_data.bat"

Write-Host "Starting local web server for map..." -ForegroundColor Cyan
Push-Location "app\public"

# Try to open the browser automatically
Start-Process "http://localhost:8000" | Out-Null

Write-Host ""
Write-Host "Map is serving at http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow
Write-Host ""

python -m http.server 8000

Pop-Location
