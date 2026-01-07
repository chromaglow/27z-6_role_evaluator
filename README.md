\# Layoff Notice Match Tool (Client-only)



A static, client-only web application that helps users understand how their selected facility and job title relate to published layoff notices, using evidence-first matching and explainability.



This tool does \*\*not\*\* predict individual layoff likelihood. It only matches user-selected inputs to explicitly published notice data and presents the supporting evidence and nearby context.



---



\## What this is

\- An evidence-first matching tool against official layoff notices

\- A deterministic, testable system (no ML, no prediction)

\- A client-only React + TypeScript app hosted on GitHub Pages

\- A way to explore affected facilities, roles, and nearby context using published data



\## What this is not

\- Not a prediction model

\- Not a probability calculator

\- Not an HR system

\- Not a claim about any individual’s likelihood of being laid off



---



\## How it works (high level)

1\. User selects a facility, job title, and remote status

2\. Inputs are normalized and matched against published notice data

3\. The app computes a tier (High / Medium / Low / Unknown) using explicit rules

4\. The app explains \*why\* by quoting the matched notice entries

5\. The app shows nearby affected facilities and similar affected roles for context



All logic is deterministic and testable.



---

## Repository structure


docs/ Product specs, decisions, scoring rules, UI wireframes
data/ Source notices, normalized datasets, aliases, geocodes
app/ React + TypeScript frontend
scripts/ Optional helpers for data validation and generation

--- ## Documentation Start here: 
- docs/SPEC.md – source-of-truth product specification 
- docs/DATA_SCHEMA.md – normalized JSON data model 
- docs/SCORING.md – tiering and explainability rules 
- docs/UI_WIREFRAME.md – UI structure and components --- 

## Development status
 Early foundation phase. Current focus:
- Finalizing product spec 
- Normalizing notice data into versioned JSON 
- Building a pure matching and scoring engine with unit tests 

--- 

## Privacy and safety 
- Client-only. No user input leaves the browser. 
- No personal data or employee identities are stored or displayed. 
- All outputs are derived from published notice data. 

--- 


## License MIT License. See LICENSE.

