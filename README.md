# Layoff Notice Match Tool

A deterministic, evidence-first tool for exploring how facilities and job titles relate to published layoff notices.

The project combines:
- an interactive, client-rendered map for spatial exploration
- a reproducible Python CLI for facility- and role-specific risk analysis

This tool does **not** predict individual layoff likelihood.
It only matches user-selected inputs to explicitly published notice data and shows the supporting evidence and nearby context.

---

## Quickstart (Map)

From repo root:

### Option A (PowerShell)
1) Build + serve the map:
   - `powershell -ExecutionPolicy Bypass -File scripts\run_map.ps1`
2) Open:
   - `http://localhost:8000`

### Option B (BAT)
1) Build + serve the map:
   - `scripts\run_map.bat`
2) Open:
   - `http://localhost:8000`

The map is a static Leaflet application served locally.  
Facilities are labeled directly on the map and colored by impact severity.

---

## Quickstart (CLI)

Direct usage:
```powershell
python tools\risk_assessment.py --facility SEA93 --title "Product Manager III"

powershell -ExecutionPolicy Bypass -File scripts\risk.ps1 -Facility SEA93 -Title "Product Manager III"

The map includes a Copy CLI button in each facility popup that generates a ready-to-run command for deeper analysis.

What this is

An evidence-first matching tool against official layoff notices

A deterministic, testable system (no ML, no prediction)

A client-rendered map for exploration + a local CLI for analysis

A way to reason about facility, role, and geographic proximity using published data

What this is not

Not a prediction model

Not a probability calculator

Not an HR system

Not a claim about any individual’s likelihood of being laid off

How it works (high level)

Layoff notices are normalized into a canonical dataset

Facilities are geocoded and rolled up by impact

The map visualizes facilities, impact magnitude, and top affected roles

Users can explore spatial clusters and copy a reproducible CLI command

The CLI performs a deterministic match and explains the supporting evidence

All logic is deterministic and inspectable.

Repository structure
docs/       Product specs, decisions, scoring rules, UI wireframes
data/       Source notices, normalized datasets, aliases, geocodes
tools/      Python data pipelines and CLI risk assessment
scripts/    One-command wrappers and build helpers
app/        Static Leaflet map (HTML/JS) and generated GeoJSON

Documentation (start here)

docs/SPEC.md – source-of-truth product specification

docs/DATA_SCHEMA.md – normalized data model

docs/SCORING.md – tiering and explainability rules

docs/UI_WIREFRAME.md – UI structure and intent

Development status

Initial viable prototype (v1).

Current focus:

Data correctness and geocoding accuracy

Scoring and explainability validation

Packaging and internal distribution workflows

Privacy and safety

Map UI is client-rendered

No user input leaves the local machine

No personal employee data is stored or displayed

All outputs are derived from published notice data

License

MIT License. See LICENSE.txt.