\# Layoff Notice Match Tool – Product Specification



\## Status

Draft v1



\## Goal

Build a static, client-only web application that helps users understand how their selected facility and job title relate to published layoff notices, plus an illustrative view of nearby facility impact and similar affected roles.



The system is evidence-first, deterministic, and explainable.



\## Non-goals

\- This is not a prediction model

\- This does not estimate an individual’s likelihood of layoff

\- This does not infer information beyond what is explicitly published in notices

\- This does not integrate with internal HR or personnel systems



---



\## Data sources

\- Official layoff notice PDFs

\- Facility lists, job-title tables, and remote Washington clauses explicitly present in those notices

\- All source documents or references are stored under `data/notices/`



---



\## Users and primary use cases



\### Primary user

Someone seeking an evidence-first understanding of whether their selected facility and job title appear in published notices, and what nearby facilities show impact.



\### Use cases

1\. Select a facility and job title and see if there is a direct match in the notices

2\. If no exact job-title match exists, see closest listed roles with confidence indicators

3\. View nearby affected facilities with total counts and top affected roles

4\. Download a structured report of inputs, tier, and evidence



---



\## Inputs



\### Required

\- Facility (selected from known facility list)

\- Job title (selected from known titles or guided free text)

\- Remote status (boolean)



\### Conditional

\- State of residence, if remote is true

&nbsp; - Washington is treated as a special case when explicitly referenced in notices



\### Validation rules

\- Facility must resolve to a known facilityId

\- Job title must resolve to a canonical title or produce selectable suggestions



---



\## Outputs



\### A) Risk tier

One of:

\- \*\*High\*\*: facility match and job-title match in at least one notice

\- \*\*Medium\*\*: facility match but job title not listed, or low-confidence title match

\- \*\*Low\*\*: no direct facility match, but proximity or loose title similarity

\- \*\*Unknown\*\*: no meaningful matches in scope of provided notices



\### B) Explanation

Always shown:

\- Plain-language reasons

\- Evidence items citing notice, facility, job title, counts, and dates where applicable



\### C) Nearby facility context

\- Nearest N affected facilities

\- For each: total affected and top affected job titles



\### D) Similar role context

\- Top K closest job titles from notice dataset

\- Confidence indicators and affected counts



\### E) Download

\- JSON report of inputs, tier, reasons, and evidence references



---



\## Job title normalization



\### Purpose

Allow common variants and abbreviations to resolve to canonical job titles used in notices.



\### Pipeline

1\. Canonicalization (trim, lowercase, punctuation normalization)

2\. Alias mapping

3\. Fuzzy matching for suggestions

4\. User confirmation when confidence is not high



\### Confidence levels

\- High: exact or alias match

\- Medium: fuzzy match above threshold

\- Low: weak fuzzy match shown as suggestion only



---



\## Map visualization



\### Purpose

Illustrative display of affected facilities and relative impact. Not a personal risk map.



\### Features

\- Facility pins sized by affected counts

\- User marker at selected facility

\- Pin popovers showing totals and top roles

\- Sidebar listing nearest affected facilities



\### Geolocation rules

\- No browser geolocation

\- User marker derived from selected facility only



---



\## Privacy and safety

\- Client-only execution

\- No user data leaves the browser

\- No personal identities stored or displayed

\- All outputs derived from published notice data



---



\## Acceptance criteria (v1)

\- End-to-end flow works using selection-based inputs

\- Tier and explanation always shown

\- Evidence displayed for High and Medium tiers

\- Map renders affected facilities correctly

\- App deploys successfully to GitHub Pages



---



\## Out of scope (v1)

\- Probability estimates

\- Predictive language

\- Inference beyond notice data

\- Internal system integrations



