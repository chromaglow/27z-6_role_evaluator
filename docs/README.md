\## Risk assessment CLI



This repo builds normalized WARN notice data and provides a CLI to query layoff impact risk by facility and job title.



\### Inputs

\- data/exports/impacts\_by\_facility.csv (row-level impacts)

\- data/exports/facility\_rollup.csv (facility totals, impact-driven)

\- data/normalized/facility\_geocodes.csv (facility lat/lon)



\### Run

From repo root:



```powershell

python tools\\risk\_assessment.py --facility SEA40 --title "Program Manager III" --nearest 8 --radius\_km 30



