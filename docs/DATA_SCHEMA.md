\# Data Schema (Normalized JSON)



This document is the single source of truth for the normalized JSON dataset consumed by the client-only app.



It is designed to support:

\- facility selection

\- job-title selection and normalization

\- scoring and explainability

\- map visualization and nearby-facility context



---



\## Files and their roles



\### Source notices

\- `data/notices/`

&nbsp; - Contains the original PDFs (or reference notes/links if PDFs are not committed).



\### Normalized notice datasets

\- `data/normalized/notice\_1.json`

\- `data/normalized/notice\_2.json`



Each file contains a normalized representation of one official notice:

\- notice metadata

\- facility impacts (facility list + approximate affected counts)

\- job-title impacts by facility (title rows + counts)



\### Combined canonical dataset

\- `data/normalized/combined.json`



Merged dataset used by the app. It:

\- includes both notices

\- deduplicates facilities

\- provides convenience indexes for UI dropdowns and engine lookup



\### Alias map

\- `data/aliases/job\_title\_aliases.json`



Maps common user-entered variants and abbreviations to canonical job titles.



\### Facility geocodes

\- `data/facilities/facility\_geocodes.json`



Adds latitude/longitude for facilities so the app can render a map.



---



\## Entity definitions



\### Notice

A `Notice` describes one official notice and its scope.



Required fields:

\- `noticeId` (string): stable unique identifier (e.g., `"notice\_1"`)

\- `source` (object):

&nbsp; - `filename` (string): filename in `data/notices/` or a reference label

&nbsp; - `receivedDate` (string, optional): ISO date (`YYYY-MM-DD`)

&nbsp; - `letterDate` (string, optional): ISO date (`YYYY-MM-DD`)

\- `jurisdiction` (string): e.g., `"WA"`

\- `remoteClauses` (array): clauses describing remote worker scope (may be empty)

\- `separationDates` (array): ISO dates if explicitly listed (may be empty)

\- `facilities` (FacilityImpact\[])

\- `jobTitleImpacts` (JobTitleImpact\[])



Remote clause format (recommended):

\- `type` (string): `"REMOTE\_RESIDENCE\_STATE"`

\- `state` (string): e.g., `"WA"`

\- `notes` (string, optional)



---



\### Facility

A `Facility` represents a facility/location referenced in notices.



Required fields:

\- `facilityId` (string): stable id, typically a facility code (e.g., `"SEA40"`)

\- `label` (string): display label (e.g., `"SEA40 - Seattle, WA"`)

\- `address` (object):

&nbsp; - `line1` (string)

&nbsp; - `city` (string)

&nbsp; - `state` (string)

&nbsp; - `postalCode` (string, optional)



Notes:

\- The notices may not provide full addresses. If full addresses are not present, `line1` may be a best-effort label (or empty string) but `city` and `state` should be present when known.

\- Geolocation is stored separately (see `facility\_geocodes.json`).



---



\### FacilityImpact

A `FacilityImpact` represents impacts for one facility within one notice.



Required fields:

\- `noticeId` (string)

\- `facilityId` (string)

\- `affectedApprox` (number or null): approximate count if provided, else null

\- `notes` (string, optional): any clarifying text



Optional fields:

\- `scopeFlags` (object, optional): notice- or row-level scope flags if needed

&nbsp; - `includesRemoteWA` (boolean, optional)



Guidance:

\- If the notice states remote WA scope at the notice level, prefer representing it in `Notice.remoteClauses`, not per-facility.



---



\### JobTitleImpact

A `JobTitleImpact` is a job-title row tied to a facility within a notice.



Required fields:

\- `noticeId` (string)

\- `facilityId` (string)

\- `jobTitleRaw` (string): exactly as written in the notice enclosure/table

\- `jobTitleCanonical` (string): normalized casing/spacing version used by the app

\- `affectedCount` (number): non-negative integer



Notes:

\- `jobTitleCanonical` is used for matching, indexing, and alias validation.

\- `jobTitleRaw` is preserved for evidence display and traceability.



---



\## JSON file specifications



\### `data/normalized/notice\_1.json` and `data/normalized/notice\_2.json`



Top-level shape:

\- `version` (string): dataset version for that notice (e.g., `"1.0.0"`)

\- `generatedAt` (string): ISO datetime (`YYYY-MM-DDTHH:mm:ssZ`)

\- `notice` (Notice): the notice object



Constraints:

\- `notice.noticeId` must match the intended file identity (e.g., `"notice\_1"`).



---



\### `data/normalized/combined.json`



Top-level shape:

\- `version` (string): combined dataset version (e.g., `"1.0.0"`)

\- `generatedAt` (string): ISO datetime

\- `notices` (Notice\[]): the merged notices (as normalized)

\- `facilities` (Facility\[]): deduplicated facility definitions

\- `jobTitles` (object): convenience indexes

&nbsp; - `canonicalTitles` (string\[]): unique canonical titles across all notices

&nbsp; - `byFacility` (object): mapping `facilityId` -> string\[] of canonical titles present at that facility



Rules:

\- Every `FacilityImpact.facilityId` and `JobTitleImpact.facilityId` must exist in `facilities\[]`.

\- Every `JobTitleImpact.jobTitleCanonical` must exist in `jobTitles.canonicalTitles`.

\- `jobTitles.byFacility\[facilityId]` should contain only canonical titles that exist in `jobTitles.canonicalTitles`.



---



\### `data/aliases/job\_title\_aliases.json`



Top-level shape:

\- `version` (string): alias dataset version (e.g., `"1.0.0"`)

\- `aliases` (array):

&nbsp; - `input` (string): user-entered variant, stored lowercase and trimmed (e.g., `"sde2"`)

&nbsp; - `canonical` (string): must match a value in `combined.json` `jobTitles.canonicalTitles`

&nbsp; - `notes` (string, optional)



Rules:

\- Store `input` values lowercase and trimmed.

\- Do not include punctuation-only variants unless they are common in practice.

\- The alias map is additive and must not override the preserved `jobTitleRaw` strings from notices.



---



\### `data/facilities/facility\_geocodes.json`



Top-level shape:

\- `version` (string): geocode dataset version (e.g., `"1.0.0"`)

\- `geos` (array):

&nbsp; - `facilityId` (string): must exist in `combined.json` `facilities\[]`

&nbsp; - `lat` (number): decimal degrees

&nbsp; - `lon` (number): decimal degrees

&nbsp; - `confidence` (string): `"exact"` or `"approx"`

&nbsp; - `source` (string): e.g., `"manual"`, `"geocoder"`, `"reference\_lookup"`



Notes:

\- Geocodes are not provided by the notices. They must be added from external lookup or manual entry.

\- The app can run without geocodes, but map features require them.



---



\## Validation checks (recommended)



A validation script (optional) should enforce:



Referential integrity:

\- Every `facilityId` referenced in `FacilityImpact` and `JobTitleImpact` exists in `combined.json` `facilities\[]`.

\- Every `noticeId` referenced in impacts matches a notice present in the dataset.



Title integrity:

\- Every `jobTitleCanonical` exists in `combined.json` `jobTitles.canonicalTitles`.

\- Every alias `canonical` exists in `combined.json` `jobTitles.canonicalTitles`.



Value constraints:

\- `affectedCount` is a non-negative integer.

\- `affectedApprox` is null or a non-negative number.

\- `lat` is within \[-90, 90] and `lon` within \[-180, 180].



Consistency:

\- `jobTitles.byFacility` contains only canonical titles that exist in `jobTitles.canonicalTitles`.

\- `jobTitles.byFacility` keys refer to known `facilityId` values.



---



\## Versioning guidance



\- Bump `version` when normalized data changes (new notice, corrected parsing, new facilities, updated aliases, updated geocodes).

\- Keep `generatedAt` updated to the time the dataset was generated.

\- Prefer additive changes and keep prior notice files stable when possible.



