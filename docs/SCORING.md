\# Scoring and Explainability Rules



This document defines the deterministic scoring rules used by the Layoff Notice Match Tool and the requirements for explainability. It is the authoritative reference for how tiers are computed and why a given result is shown.



The system does not predict outcomes. It classifies explicit matches and near-matches to published notice data.



---



\## Core principles



\- Deterministic: the same inputs always produce the same output

\- Evidence-first: every tier must be explainable using notice data

\- Conservative: no inference beyond what is explicitly published

\- Testable: rules are implementable as pure functions with unit tests



---



\## Inputs to scoring



The scoring engine receives the following normalized inputs:



\- `facilityId` (string)

\- `jobTitleCanonical` (string or null)

\- `jobTitleConfidence` (High | Medium | Low | None)

\- `isRemote` (boolean)

\- `remoteState` (string or null)

\- `dataset` (combined normalized dataset)



---



\## Evidence model



Evidence is structured data emitted by the scoring engine and displayed to the user.



Each evidence item includes:

\- `noticeId`

\- `facilityId` (if applicable)

\- `jobTitleRaw` (if applicable)

\- `jobTitleCanonical` (if applicable)

\- `affectedCount` or `affectedApprox`

\- `notes` (optional)



Evidence must reference data that exists in the normalized dataset.



---



\## Tier definitions



\### High

Returned when:

\- The selected facility appears in at least one notice, and

\- The selected job title appears for that facility in the same notice, and

\- The job-title match confidence is High



Evidence requirements:

\- At least one JobTitleImpact row matching both facility and job title

\- Notice metadata identifying the source



---



\### Medium

Returned when any of the following conditions are met:

\- Facility appears in a notice, but job title does not appear for that facility

\- Job title appears for the facility only via Medium-confidence fuzzy match

\- Job title appears in the notice but not tied to a specific facility



Evidence requirements:

\- Facility-level impact evidence, or

\- Job-title evidence with reduced confidence indicator



---



\### Low

Returned when:

\- No direct facility match exists, but

\- One or more affected facilities exist within the same metro area or nearby region, or

\- Only Low-confidence job-title similarity matches exist



Evidence requirements:

\- Nearby facility evidence, or

\- Similar job-title evidence with low confidence explicitly labeled



---



\### Unknown

Returned when:

\- No meaningful facility, job-title, or proximity matches exist within the dataset



Evidence requirements:

\- Explanation stating that no relevant matches were found



---



\## Scoring order of operations



1\. Resolve facility match

2\. Resolve job-title match and confidence

3\. Evaluate direct facility + job-title matches

4\. Evaluate facility-only matches

5\. Evaluate proximity and similarity context

6\. Assign tier

7\. Emit reasons and evidence



The first satisfied tier condition in priority order is applied.



Priority order:

1\. High

2\. Medium

3\. Low

4\. Unknown



---



\## Explainability requirements



For every result, the engine must emit:



\### Reasons

\- Plain-language bullet points explaining why the tier was assigned

\- Each reason must correspond to one or more evidence items



\### Evidence

\- Structured references to notice data

\- Raw notice text preserved where applicable

\- Counts and dates included when available



If no evidence exists, the result must be `Unknown`.



---



\## Similar role logic



When no High-confidence job-title match exists:

\- Compute similarity against canonical titles in the dataset

\- Return top K closest titles (default K = 5)

\- Include confidence indicators and affected counts when available



Similar roles must never elevate a result to High.



---



\## Nearby facility logic



Nearby facilities are computed using facility geocodes when available.



Rules:

\- Default N = 3 nearest affected facilities

\- Distance is computed between facility coordinates

\- Only facilities explicitly listed in notices are included



Nearby facilities provide context only and must not imply individual impact.



---



\## Remote scope handling



If `isRemote` is true:

\- Check for explicit remote clauses in notices

\- Only apply remote scope when the notice explicitly mentions the selected state

\- Remote scope alone cannot produce a High tier without job-title evidence



Remote handling must be explicit and conservative.



---



\## Edge cases



\- Missing job title: scoring proceeds with facility-only logic

\- Missing facility: scoring proceeds with job-title-only similarity logic

\- Missing geocodes: skip proximity logic gracefully

\- Conflicting notice data: emit evidence from all applicable notices



---



\## Versioning and changes



\- Any change to scoring logic requires an update to this document

\- Behavioral changes must be accompanied by unit tests

\- Dataset changes alone do not require scoring changes unless behavior changes



---



\## Non-goals



\- Probability estimates

\- Predictive modeling

\- Ranking individuals or teams

\- Inferring impact beyond published notice data



