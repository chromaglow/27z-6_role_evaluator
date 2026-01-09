@echo off
setlocal

echo Exporting facilities.geojson...
python tools\export_facilities_geojson.py
if errorlevel 1 (
  echo Export failed.
  exit /b 1
)

echo Syncing to app\public...
copy /Y data\exports\facilities.geojson app\public\facilities.geojson >nul
if errorlevel 1 (
  echo Copy failed.
  exit /b 1
)

echo Done: app\public\facilities.geojson updated.
endlocal



geocode_refresh_from_addresses.py

python tools\geocode_refresh_from_addresses.py
