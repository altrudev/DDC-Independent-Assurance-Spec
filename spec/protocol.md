# DDC Independent Assurance Protocol — draft 0.1

## 1. Purpose

This protocol coordinates multiple assurance evaluators without allowing one evaluator's reasoning to influence another before each has frozen its own determination.

## 2. Required lifecycle

A conforming implementation MUST enforce:

DRAFT → INTAKE_COMPLETE → EVIDENCE_CUTOFF_FROZEN → BUNDLE_FROZEN → INDEPENDENT_REVIEW → EVALUATOR_RESULTS_FROZEN → REVEAL_ALLOWED → COMPARISON_DRAFT → REPRESENTATION_CONFIRMED → JOINT_ATTESTED → CLOSED.

A material post-freeze change MUST create a new case revision. The prior frozen state MUST remain verifiable.

## 3. Evidence

Every evaluator MUST receive the same identified evidence root for the comparison to claim a common evidence set.

Evidence timing MUST distinguish:
- contemporaneous evidence;
- evidence that existed but was unavailable at the relevant action boundary;
- later reconstruction or investigation.

Later evidence MUST NOT be silently reclassified as contemporaneous.

## 4. Evaluator independence

Before reveal:
- evaluators MUST NOT receive another evaluator's determination;
- native terminology and reasoning MAY differ;
- the orchestrator MUST NOT force a shared conclusion vocabulary into native evaluator work.

The protocol does not imply organizational independence merely because determinations are procedurally independent.

## 5. Freeze

Each determination MUST bind:
- case ID and revision;
- evidence root;
- evidence cutoff root;
- evaluator identity;
- method identity and version;
- determination artifact hash;
- frozen-at timestamp.

## 6. Reveal and comparison

Reveal MUST occur only after all required evaluator determinations are frozen or the case is explicitly closed as incomplete.

Shared comparison vocabulary is post-reveal only:
ESTABLISHED, NOT_ESTABLISHED, PARTIALLY_ESTABLISHED, UNRESOLVED, CONTRADICTED, OUT_OF_SCOPE.

Comparison MUST distinguish at least:
- convergence;
- evaluator-specific finding;
- conclusion disagreement;
- evidentiary-boundary disagreement;
- unresolved matter;
- out-of-scope matter.

## 7. Representation confirmation

The orchestration layer MAY draft a comparison automatically, but MUST NOT finalize characterization of an evaluator's result without that evaluator's confirmation.

## 8. Attestation

Joint attestation MUST bind the frozen determinations, final comparison and case root. Attestation means the comparison is acknowledged as the joint comparison artifact; it does not erase disagreement.

## 9. Failure states

Conforming implementations MUST represent failure explicitly, including evaluator decline, withdrawal, timeout, conflict, evidence rejection, bundle mismatch, invalid determination, withheld attestation and case withdrawal.

A partially completed multi-evaluator case MUST NOT be silently presented as completed multi-evaluator assurance.
