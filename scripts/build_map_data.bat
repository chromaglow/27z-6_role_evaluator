@echo off
REM Build Map Data - Generates and syncs facilities.geojson
setlocal

echo ========================================
echo Building Map Data
echo ========================================
echo.

echo [1/2] Exporting facilities.geojson...
python tools\export_facilities_geojson.py
if errorlevel 1 (
    echo ERROR: Export failed.
    exit /b 1
)

echo.
echo [2/2] Syncing to app\public...
copy /Y data\exports\facilities.geojson app\public\facilities.geojson >nul
if errorlevel 1 (
    echo ERROR: Copy failed.
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: Map data updated!
echo ========================================
echo File: app\public\facilities.geojson
echo.

endlocal
