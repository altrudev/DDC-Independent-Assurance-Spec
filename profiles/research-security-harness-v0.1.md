# DDC Research & Security Harness Assurance Profile v0.1

Status: Draft profile

Applies to research harnesses, security test suites, exploit and reproducer collections, cryptographic evaluation harnesses, smart-contract audit harnesses, protocol conformance systems, and similar evidence-producing technical systems.

## 1. Purpose

This profile defines how an assurance system should preserve the evidence chain from an external source artifact to a published technical finding.

It does not define how a researcher must discover findings. It defines what must remain knowable afterward.

Central requirement: evidence-channel closure.

> A published finding should be traceable to the exact source artifact, transformation path, execution environment, witness, controls, adjudication state, and publication revision that support it.

A finding may still be valid when closure is incomplete. In that case, missing links must remain explicit rather than being silently inferred.

## 2. Core invariants

1. Source identity is not source integrity. A URL, project name, or archive filename does not establish the bytes evaluated.
2. Download is not verification. A fetched artifact remains unverified until its expected identity is checked.
3. Extraction is an authority boundary. An evidence package must not gain filesystem or execution authority merely because it is being inspected.
4. Retained source is not automatically identical to submitted source. Curation, normalization, patches, translation, generated adapters, and derived data are transitions.
5. Build success is not semantic equivalence. Harness-side fixes that enable compilation require provenance and scope.
6. A witness is not a universal claim. Runtime evidence establishes what happened under the recorded environment and inputs.
7. A control is not full falsification. Controls test stated alternatives but do not prove the reproducer is free of shared blind spots.
8. Observation is not exploitation. Structural defects, proof gaps, implementation divergences, and demonstrated exploits are separate evidence classes.
9. Discovery provenance is separate from technical validity. Human, AI-assisted, automated, and externally suggested findings may all be valid, but their origins should not be conflated.
10. Later evidence must not rewrite earlier evidence. Revisions, retries, patches, reruns, or publication updates must not contaminate the record of what earlier evidence established.
11. External reproduction is revision-specific. Reproduction of revision A does not validate revision B unless continuity or a new rerun is evidenced.
12. Chronology is not causality.

## 3. Required evidence objects

### SourceArtifact
Identifies the externally supplied source under review.
Required: source identifier, acquisition reference, acquisition time, byte length when available, cryptographic digest, expected-digest source if one exists, and verification result.

### ExtractionRecord
Records how an archive or package became a working tree.
Required: input SourceArtifact, extractor and version, extraction policy, rejected unsafe entries, retained-member mapping or manifest, and output-tree or manifest digest.

### TransformationRecord
Records every researcher or harness-controlled change before evaluation.
Examples include compile-fix patches, generated adapters, normalized test vectors, source rewrites, wrappers, shims, parameter extraction, and private-to-public transformations.
Required: input artifact, transformation description, exact patch or tool identity, output artifact, reason, and claimed semantic effect.

### BuildRecord
Binds executable evaluation inputs to an environment.
Required: source or tree identity, compiler or interpreter, version, flags, linked dependencies and versions, platform or ABI, build result, and executable or library digest where practical.

### WitnessRecord
Records a positive, negative, mutation-control, or indeterminate observation.
Required: finding ID, evaluator or reproducer identity, target build identity, inputs, environment, observed result, output digest, and witness class.

### ClaimRecord
Separates observation from assertion.
Required: finding ID, layer, status, claim text, evidence references, assumptions, unresolved alternatives, and scope limitations.

### ReviewRecord
Captures adjudication and discovery provenance.
Required: review state, reviewer role or pseudonymous identifier where appropriate, discovery provenance, technical validation path, and unresolved disagreements.

### PublicationRecord
Binds a public report to the evidence state that existed when it was published.
Required: report URI, publication time, report revision, repository commit or immutable content identity, included finding IDs, evidence cutoff, and supersession relation.

### ExternalReproductionRecord
Records third-party reproduction without broadening it.
Required: external actor or reference, exact artifact or commit reproduced, environment if known, findings reproduced, result, source of the statement, and later revisions not covered.

## 4. Evidence-channel closure dispositions

CLOSED — every material transition from acquisition through publication is bound to inspectable evidence and no unresolved gap can change the stated claim.

CONDITIONALLY_CLOSED — the finding is strongly substantiated, but one or more declared assumptions or environment dependencies remain material to scope.

OPEN — one or more material provenance, transformation, environment, witness, or publication bindings are missing.

CONTRADICTED — trusted evidence conflicts with a material claim or provenance relation.

These dispositions assess the evidence channel, not whether the underlying software is secure.

## 5. Mandatory gates

A conforming assurance run must fail closed when a material finding depends on any of the following:

1. an expected source digest exists but was not checked;
2. extracted source cannot be bound to evaluated source;
3. an undocumented harness-side patch affected evaluated code;
4. the evaluated build cannot be distinguished from a materially different build;
5. a runtime claim is generalized beyond its recorded environment without supporting evidence;
6. a report cites a finding but cannot identify the evidence revision supporting publication;
7. an external reproduction claim does not identify the revision reproduced;
8. later evidence has overwritten or obscured the original finding state.

## 6. Strongly recommended controls

- pre-extraction validation of path traversal, absolute paths, symlinks, hard links, and special entries;
- per-member archive-to-retained-source manifest;
- hermetic or pinned build environment;
- result artifact hashing;
- positive and negative controls;
- mutation or falsification controls for the reproducer itself;
- machine-readable finding lifecycle;
- explicit AI, human, automated, or external discovery provenance;
- environment-matrix testing for undefined-behaviour or memory-layout-sensitive findings;
- public reconstruction of derived datasets where disclosure permits;
- branch-preserving lineage when alternate reproducer paths exist.

## 7. Finding lifecycle

OBSERVED -> HYPOTHESIS -> WITNESS_CREATED -> CONTROLLED -> ADJUDICATED -> PUBLISHED -> EXTERNALLY_REPRODUCED (optional) -> FIXED | SUPERSEDED | RETRACTED | STILL_OPEN

Each transition earns its own certainty. A later state must not automatically inherit certainty from an earlier one.

## 8. Minimal machine-readable envelope

Required top-level fields:
- schema
- finding_id
- source
- extraction
- transformations
- build
- witnesses
- claim
- review
- publication
- external_reproduction
- evidence_channel

Recommended schema identifier: ddc-research-harness-assurance/0.1

## 9. Non-goals

This profile does not decide vulnerability severity, decide whether cryptographic assumptions are sound, replace domain experts, require disclosure of proprietary reasoning, require disclosure of sensitive exploit material, equate reproducibility with correctness, or equate AI assistance with either weakness or authority.

## 10. Relationship to DDC Independent Assurance

This profile is a domain-specific application of DDC Independent Assurance principles.

Two evaluators may use different internal methods while still exchanging the same frozen evidence objects and closure claims. The profile standardizes evidence boundaries and comparison surfaces, not proprietary evaluator reasoning.