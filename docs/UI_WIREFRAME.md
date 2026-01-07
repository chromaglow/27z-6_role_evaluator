\# UI Wireframe and Component Structure



This document defines the high-level UI layout, pages, and components for the Layoff Notice Match Tool. It describes structure and behavior, not visual styling.



The goal of the UI is clarity, explainability, and conservative presentation of evidence.



---



\## Design principles



\- Evidence-first: explanations and evidence are always visible or easily accessible

\- Conservative language: no implied likelihood or predictions

\- Guided input: minimize free text, prefer selection and confirmation

\- Progressive disclosure: show more detail only when useful

\- Accessibility-aware: readable, scannable, and keyboard-friendly



---



\## Page structure overview



The application consists of two primary pages:



1\. Home (input collection)

2\. Results (tier, explanation, evidence, and context)



Navigation between pages is linear and state-driven.



---



\## Home page



\### Purpose

Collect validated user inputs in a guided, low-friction manner.



\### Components



\#### Header

\- App title

\- One-line description clarifying non-predictive nature



\#### Facility selector

\- Searchable dropdown of known facilities

\- Display label includes facility code and city/state

\- Helper text for users unsure of their facility code



\#### Job title selector

\- Searchable dropdown of canonical job titles

\- Optional free-text input with guided suggestions

\- Confidence indicator shown when selection is ambiguous



\#### Remote status toggle

\- Boolean toggle: Remote or On-site



\#### Conditional remote fields

\- State of residence dropdown

\- Helper text explaining why state is required for remote selection



\#### Submit button

\- Disabled until required inputs are valid

\- Proceeds to Results page



---



\## Results page



\### Purpose

Present the computed tier with clear explanations and supporting evidence, plus illustrative context.



\### Components



\#### Summary panel

\- Tier badge (High / Medium / Low / Unknown)

\- One-line summary explaining what the tier means

\- Reminder that this is not a prediction



\#### Reasons panel

\- Bullet list of plain-language reasons for the tier

\- Each reason corresponds to evidence shown elsewhere



\#### Evidence drawer

\- Expandable section listing evidence items

\- Each item shows:

&nbsp; - Notice identifier

&nbsp; - Facility name

&nbsp; - Job title (raw text)

&nbsp; - Affected counts or approximate counts

&nbsp; - Relevant dates when available



\#### Similar roles panel

\- Shown when no exact job-title match exists

\- Lists top K similar canonical titles

\- Displays confidence indicators and affected counts



---



\## Map and nearby context



\### Map panel

\- Interactive map centered on selected facility

\- Pins for facilities listed in notices

\- Pin size scaled by total affected count

\- User marker at selected facility



\### Map popovers

\- Facility name and code

\- Total affected count

\- Top affected job titles



\### Nearby facilities sidebar

\- List of nearest affected facilities

\- Distance from selected facility

\- Summary of impact at each location



---



\## Download and transparency



\### Download report

\- Button to download a JSON report containing:

&nbsp; - User inputs

&nbsp; - Assigned tier

&nbsp; - Reasons

&nbsp; - Evidence references



\### Disclaimers

\- Visible reminder that outputs are derived from published notices

\- Explicit statement that the tool does not assess individual likelihood



---



\## Error and empty states



\- No matches found: clear explanation and `Unknown` tier

\- Missing geocode data: map panel hidden with explanatory note

\- Incomplete input: inline validation and guidance



---



\## Component organization (suggested)



\- `pages/`

&nbsp; - `Home.tsx`

&nbsp; - `Results.tsx`

\- `components/`

&nbsp; - `FacilitySelector.tsx`

&nbsp; - `JobTitleSelector.tsx`

&nbsp; - `RemoteToggle.tsx`

&nbsp; - `TierBadge.tsx`

&nbsp; - `ReasonsList.tsx`

&nbsp; - `EvidenceDrawer.tsx`

&nbsp; - `SimilarRolesList.tsx`

\- `map/`

&nbsp; - `FacilityMap.tsx`

&nbsp; - `MapPopover.tsx`



---



\## Out of scope (v1)



\- User accounts or persistence

\- Browser geolocation

\- Editable visual themes

\- Any form of predictive or probabilistic UI



