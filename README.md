# Layoff Notice Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

I built this tool after getting anxious about layoffs at work. Wanted to see which facilities and job titles were actually mentioned in published WARN notices instead of relying on rumors.

**What it does:** Matches facilities and job titles against official layoff notices. Shows you the data, not predictions.

**What it doesn't do:** It won't tell you if YOU specifically are getting laid off. It just shows what's in the public notices.

---

## Quick Start

**Not technical?** Check out [GETTING_STARTED.md](GETTING_STARTED.md) - I wrote it for my non-tech friends.

**Know Python?** Here's the fast version:

```bash
# Install
pip install -r requirements.txt

# Run the map
scripts\run_map.bat

# Or check a specific facility
python tools\risk_assessment.py --facility SEA40 --title "Program Manager"
```

---

## The Map

The interactive map shows all the facilities mentioned in layoff notices. Bigger circles = more people affected.

**Features:**
- Click any facility to see details
- Search for specific facility codes
- Filter to show only impacted facilities
- Retro terminal UI (because why not)
- Background music auto-plays on first click (Blade Runner vibes)

**Easter eggs:**
- Loading screen quotes are from Alien and Starship Troopers
- Press any key to skip the loading screen (I got impatient during testing)
- The terminal is called NOSTROMO because of course it is

To launch the map:
```bash
scripts\run_map.bat
```

Then open your browser to `http://localhost:8000`

---

## Command Line Tool

If you want to dig deeper into a specific facility and job title:

```bash
python tools\risk_assessment.py --facility SEA93 --title "Product Manager III"
```

This will show you:
- Exact matches in the notices
- Nearby facilities with similar impacts
- The actual notice text (so you can verify it yourself)

**Pro tip:** The map has a "Copy CLI" button in each facility popup that generates the command for you.

---

## How It Works

1. I grabbed the WARN notices (public layoff announcements)
2. Parsed them to extract facility codes and job titles
3. Geocoded the facilities so they can be mapped
4. Built a map to visualize it all
5. Added a CLI tool for detailed analysis

Everything is deterministic - no ML, no predictions, just matching what you ask for against what's in the notices.

---

## Project Structure

```
27z-6_role_evaluator/
├── app/                    # The map (HTML/JS)
│   └── public/
│       ├── index.html      # Map interface
│       └── facilities.geojson
├── data/                   # All the notice data
│   ├── raw/                # Original PDFs
│   ├── normalized/         # Cleaned up data
│   └── exports/            # CSV files for analysis
├── docs/                   # Detailed specs (if you're curious)
├── scripts/                # Helper scripts to run things
└── tools/                  # Python scripts for data processing
```

---

## Installation

**Prerequisites:**
- Python 3.8 or higher
- A web browser

**Steps:**
```bash
# Clone or download this repo
cd 27z-6_role_evaluator

# Install dependencies
pip install -r requirements.txt

# That's it!
```

For more detailed instructions, see [INSTALL.md](INSTALL.md).

---

## Documentation

If you want to dive deeper:

| Document | What's in it |
|----------|--------------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Step-by-step for non-tech folks |
| [INSTALL.md](INSTALL.md) | Detailed installation help |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and fixes |
| [docs/SPEC.md](docs/SPEC.md) | Full technical specification |
| [docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md) | How the data is structured |

---

## Known Issues

- Geocoding sometimes gets confused by weird facility codes (working on it)
- The map can be slow if you load all facilities at once
- Volume slider looks a bit janky on Firefox

---

## Privacy & Safety

- Everything runs locally on your machine
- No data gets sent anywhere
- No personal employee information is stored
- All data comes from public WARN notices

---

## Development

Want to contribute or modify something?

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black tools/

# Rebuild the map data
scripts\build_map_data.bat
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## Tech Stack

- **Map:** Leaflet.js (client-side, no server needed)
- **Data processing:** Python with pandas
- **PDF parsing:** pdfplumber
- **Geocoding:** geopy + OpenStreetMap

---

## Why I Built This

I was tired of hearing rumors and speculation about layoffs. Wanted to see the actual data from official sources. Figured others might find it useful too.

This tool doesn't predict anything - it just shows you what's already public. Think of it as a search engine for layoff notices.

---

## License

MIT License - do whatever you want with it. See [LICENSE.txt](LICENSE.txt).

---

## Questions?

1. Check [GETTING_STARTED.md](GETTING_STARTED.md) or [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Look through the [docs/](docs/) folder
3. Open an issue if something's broken

---

**Built out of anxiety, powered by public data** 🗺️
