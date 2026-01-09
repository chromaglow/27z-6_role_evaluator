@echo off
REM Run Map - Batch Script
REM Builds map data and starts local server

echo ========================================
echo Layoff Notice Map - Starting Server
echo ========================================
echo.

REM Step 1: Build map data
echo [1/3] Building map data...
call scripts\build_map_data.bat
if errorlevel 1 (
    echo ERROR: Failed to build map data
    pause
    exit /b 1
)

echo.
echo [2/3] Starting local web server...
echo.
echo The map will open in your browser at:
echo http://localhost:8000
echo.
echo Press Ctrl+C to stop the server when done.
echo.

REM Step 2: Start server and open browser
cd app\public
start http://localhost:8000
python -m http.server 8000

REM Step 3: Cleanup (runs when server stops)
echo.
echo Server stopped.
pause
