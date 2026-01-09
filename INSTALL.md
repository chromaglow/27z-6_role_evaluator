# Installation Guide

## Prerequisites

- **Python 3.8+** (check with `python --version`)
- **Git** (for cloning the repository)
- **pip** (Python package installer)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/chromaglow/27z-6_role_evaluator.git
cd 27z-6_role_evaluator
```

### 2. Create a Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

**Production (minimal):**
```bash
pip install -r requirements.txt
```

**Development (includes testing and linting tools):**
```bash
pip install -r requirements-dev.txt
```

**Editable install (for development):**
```bash
pip install -e .
```

This allows you to run `risk-assessment` from anywhere after installation.

## Verify Installation

Test that everything works:

```bash
# Test the CLI
python tools/risk_assessment.py --help

# Run the map (PowerShell)
powershell -ExecutionPolicy Bypass -File scripts/run_map.ps1

# Or use the BAT file
scripts\run_map.bat
```

## Troubleshooting

### Issue: `pip` not found
**Solution:** Make sure Python is in your PATH, or use `python -m pip` instead of `pip`.

### Issue: Permission denied when activating virtual environment
**Solution (Windows):** Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Module not found errors
**Solution:** Make sure you're in the virtual environment and have installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Geocoding fails or times out
**Solution:** The geocoding script uses Nominatim (OpenStreetMap). If you get rate-limited:
1. Increase `SLEEP_SECONDS` in `tools/geocode_refresh_from_addresses.py`
2. Run the script again (it will skip already-geocoded facilities)

## Updating Dependencies

To update all packages to their latest compatible versions:

```bash
pip install --upgrade -r requirements.txt
```

To freeze current versions (for reproducibility):

```bash
pip freeze > requirements-lock.txt
```

## Uninstall

To remove the virtual environment:

```bash
# Deactivate first
deactivate

# Then remove the directory
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

## Next Steps

- Read the [README.md](README.md) for project overview
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Explore the [docs/](docs/) folder for detailed specifications
