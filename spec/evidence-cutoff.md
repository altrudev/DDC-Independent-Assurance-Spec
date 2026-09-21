# Evidence cutoff

The cutoff record defines what evidence may be treated as available for the evaluated decision/action.

It MUST include:
- case ID/revision;
- cutoff time;
- timezone/UTC normalization;
- clock source if known;
- known clock skew or uncertainty;
- evidence items included;
- evidence items known to exist but unavailable at the action boundary, when relevant;
- later evidence/reconstruction classification;
- frozen record hash.

Evidence existence, reachability, discoverability, accessibility/authorization, freshness/timeliness, trustworthiness and actual consultation are distinct properties and MUST NOT be collapsed when material to the result.
