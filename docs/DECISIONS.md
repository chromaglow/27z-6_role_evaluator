\# Architectural Decisions



This document records the key architectural and product decisions for the Layoff Notice Match Tool, along with the rationale behind each choice. The goal is to make tradeoffs explicit and reduce future ambiguity.



---



\## Client-only architecture



\*\*Decision:\*\*  

The application is implemented as a static, client-only web app.



\*\*Rationale:\*\*  

\- No user input leaves the browser

\- No backend infrastructure to operate or secure

\- Reduced risk of misinterpretation or misuse of personal data

\- Simpler deployment via GitHub Pages



\*\*Implications:\*\*  

\- All data must be shipped as static JSON

\- All matching, scoring, and explainability logic must run in the browser

\- Dataset size must remain reasonable for client load time



---



\## Evidence-first design



\*\*Decision:\*\*  

Every output tier must be accompanied by explicit reasons and evidence derived directly from published notice data.



\*\*Rationale:\*\*  

\- Prevents implied or speculative claims

\- Makes the system auditable and explainable

\- Allows users to see exactly what data was matched



\*\*Implications:\*\*  

\- Raw notice language is preserved alongside normalized fields

\- Scoring logic must emit structured evidence references

\- UI must surface evidence, not just a summary label



---



\## Deterministic scoring (no prediction)



\*\*Decision:\*\*  

The system uses deterministic rules and tiers, not probabilities or predictive models.



\*\*Rationale:\*\*  

\- Published notices are sparse and categorical, not predictive

\- Probabilistic outputs would imply knowledge the data does not support

\- Deterministic logic is testable and reviewable



\*\*Implications:\*\*  

\- Scoring rules are explicitly documented in `SCORING.md`

\- Changes to scoring require versioned updates and tests

\- No machine learning or statistical inference is used



---



\## Tiered output instead of numeric scores



\*\*Decision:\*\*  

Outputs are expressed as tiers (High / Medium / Low / Unknown), not numeric scores.



\*\*Rationale:\*\*  

\- Tiers align better with the qualitative nature of the data

\- Avoids false precision

\- Easier for users to interpret correctly



\*\*Implications:\*\*  

\- UI focuses on explanation rather than optimization

\- Edge cases are explicitly handled as `Unknown`



---



\## Normalized data with preserved raw text



\*\*Decision:\*\*  

Job titles and facilities are normalized for matching, but raw notice text is preserved.



\*\*Rationale:\*\*  

\- Normalization improves usability and matching accuracy

\- Preserving raw text maintains traceability to source documents



\*\*Implications:\*\*  

\- Data schema includes both `jobTitleRaw` and `jobTitleCanonical`

\- Alias maps are additive and never overwrite raw values



---



\## Explicit handling of remote scope



\*\*Decision:\*\*  

Remote employee scope is represented explicitly when mentioned in notices, rather than inferred.



\*\*Rationale:\*\*  

\- Notices may include specific clauses (e.g., remote employees residing in Washington)

\- Inferring remote scope would introduce unsupported assumptions



\*\*Implications:\*\*  

\- Remote clauses are stored as structured data

\- UI treats remote status as a conditional input with clear rules



---



\## Map as illustrative context, not prediction



\*\*Decision:\*\*  

The map visualization is explicitly illustrative and contextual.



\*\*Rationale:\*\*  

\- Geographic proximity does not imply individual impact

\- Map provides situational awareness, not likelihood



\*\*Implications:\*\*  

\- Map UI includes clear disclaimers

\- Pins represent published facility impacts only

\- User location is derived from selected facility, not GPS



---



\## Versioned data artifacts



\*\*Decision:\*\*  

All normalized datasets, aliases, and geocodes are versioned.



\*\*Rationale:\*\*  

\- Notice data may change or be corrected

\- Versioning supports reproducibility and review



\*\*Implications:\*\*  

\- Each JSON dataset includes `version` and `generatedAt`

\- Breaking changes require version bumps



---



\## Testing focus on pure functions



\*\*Decision:\*\*  

Core logic is implemented as pure functions with unit tests.



\*\*Rationale:\*\*  

\- Deterministic behavior is easy to test and reason about

\- Reduces UI-driven bugs

\- Supports future refactoring without behavioral drift



\*\*Implications:\*\*  

\- Matching and scoring logic lives outside UI components

\- Tests validate normalization, scoring, and explainability outputs



---



\## Deferred backend and integrations



\*\*Decision:\*\*  

No backend services or integrations are included in v1.



\*\*Rationale:\*\*  

\- Keeps scope aligned with evidence-first goals

\- Avoids premature infrastructure complexity



\*\*Implications:\*\*  

\- Any future backend work requires explicit re-evaluation

\- Current architecture is intentionally limited and conservative



