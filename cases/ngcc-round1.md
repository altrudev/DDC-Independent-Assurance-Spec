# Case Study: NGCC Round 1 Reproduction Harness

External project: ngcc-dev/ngcc-harness
Assessment type: architecture and evidence-channel review
Profile: DDC Research & Security Harness Assurance Profile v0.1
Status: Informational case study; not an audit, certification, or endorsement.

Pinned external revision reviewed: `ngcc-dev/ngcc-harness@ae52ba77713e161dd3a6afe73d20b43cc8039522`  
Review date: 2026-09-21

Primary implementation files inspected include `Makefile`, `api/link_rules.mk`, `api/link_finish.mk`, `api/link_shim.c`, `api/ngcc_kat.c`, `tools/ngcc_attack.c`, `tools/reproduce.sh`, `security/design_parameter_audit.py`, `security/check_vulnerability_ids.py`, `download.sh`, `extract.sh`, `SOURCE_ARCHIVES.md`, and related candidate Makefiles.

## 1. Why this case is useful

The NGCC Round 1 reproduction harness is a strong public example of expert-led, AI-assisted technical assurance. It provides source-built candidate libraries, stable finding IDs, runtime reproducers, controls, static checks, source archive digests, and bounded claim language.

The purpose of this case study is not to relitigate its cryptographic findings. It tests whether the DDC profile identifies evidence-channel questions that remain relevant even in a disciplined harness.

## 2. Strong controls observed

- candidate reference implementations are built from source rather than executing shipped binaries;
- candidate build scripts are not automatically trusted;
- stable vulnerability IDs distinguish findings;
- verification modes distinguish runtime, static, runtime+static, and review evidence;
- incomplete reproducer builds do not silently pass;
- negative controls are used for multiple runtime witnesses;
- original source archive SHA-256 values are recorded;
- test-vector identity can be checked through SHA-256 manifests;
- reports distinguish runtime witnesses from parameter ceilings, proof gaps, and review-only findings;
- limitations are frequently stated beside the finding.

## 3. Open evidence-channel findings

### NGCC-DDC-01 — Download verification is not mandatory in the acquisition script

SOURCE_ARCHIVES.md records SHA-256 identities for official archives. download.sh downloads archives but does not visibly compare the resulting bytes against those recorded digests before they can be consumed.

DDC interpretation: source location and successful transfer do not establish verified local artifact identity.

Recommended closure: verify the expected digest immediately after download and refuse extraction on mismatch.

### NGCC-DDC-02 — Archive identity is not fully closed to retained source identity

The repository states that retained reference source files were copied without modification from official archives, but a public per-member mapping from archive member to retained repository file is not evident.

Recommended closure: publish or generate a manifest binding archive SHA -> member path -> member SHA -> retained path -> retained SHA.

### NGCC-DDC-03 — Extraction is an untrusted-input authority boundary

extract.sh invokes bsdtar or unzip on submission archives and strips execute bits afterward. A visible pre-extraction policy for path traversal, absolute paths, symlinks, hard links, or special filesystem entries is not part of that script.

Recommended closure: inspect the archive namespace before extraction, reject unsafe entry types and paths, then extract into an isolated destination.

### NGCC-DDC-04 — Harness-side source patches need first-class provenance

The harness permits patched copies under candidate patches directories when source cannot compile as submitted.

Recommended closure: bind each patch to the original file hash, patch hash, output hash, reason, and explicit claim about semantic effect.

### NGCC-DDC-05 — Build environment is not fully pinned

The harness records compiler and flags, but the repository does not appear to define one hermetic execution environment for all published results.

This is especially material for undefined-behaviour, stale-stack, crash, ABI, optimizer, OpenSSL, GMP, or memory-layout-sensitive findings.

Recommended closure: publish a pinned environment or complete environment receipt, and state when a claim is environment-specific.

### NGCC-DDC-06 — Derived public reference data depends on a private analysis tree

data/README.md states that the public dataset is regenerated from a private analysis tree.

The public result may be correct and verifiable while the evidence-generation channel remains partially opaque.

Recommended closure: distinguish fields independently derivable from official source material from fields that depend on private interpretation or transformation, and publish transformation receipts where possible.

### NGCC-DDC-07 — Discovery provenance is compressed

Reports credit AI assistance, but the public finding inventory does not expose whether a particular issue originated from automated search, AI suggestion, human review, external suggestion, or mixed discovery.

This does not affect technical validity by itself.

Recommended closure: add optional discovery provenance as a separate field from verification status.

### NGCC-DDC-08 — Report-to-harness revision binding could be stronger

A finding page can link to the current reproduction harness, but a public report is strongest when it binds to the exact repository commit, target source identity, environment, reproducer identity, positive witness, and control result used at publication.

Recommended closure: emit a machine-readable evidence receipt per finding or report.

### NGCC-DDC-09 — External reproduction should be explicit and revision-scoped

If a result is independently reproduced, the record should identify who or where, what exact commit or artifact was run, which result matched, and which later revisions are not covered.

Recommended closure: maintain external reproduction records separate from ordinary local reruns.

### NGCC-DDC-10 — Controls can be extended to test the test

Negative controls are already a major strength. A stronger falsification layer can mutate the reproducer or trigger conditions and require expected changes in outcome.

Recommended closure: add mutation controls for finding classes where overfitting or shared assumptions are material.



## 4. Harness implementation findings

The findings below concern the reproduction harness itself, not the validity of the candidate vulnerabilities it reports. Where a defect creates a possible false-result path but has not been shown to affect a published NGCC finding, that limitation is stated explicitly.

### NGCC-IMPL-01 — Root build orchestration masks candidate build failures

At the pinned revision, the root Makefile executes each candidate build as:

`make ... libs && echo "BUILD ... ok" || { echo "BUILD ... FAILED"; }`

The failure branch ends with a successful `echo`, so the candidate target itself returns success after a failed child build.

**Impact:** `make all` can continue and potentially exit successfully even though one or more ordinary candidate libraries failed to build. This weakens the repository-level success signal.

**Closure:** preserve and propagate the failing child exit status.

### NGCC-IMPL-02 — KAT Make targets do not propagate harness failure status

In `api/link_rules.mk`, each test target captures the KAT harness return code in `rc`, but the recipe ends by running `tail -1` and does not `exit $rc`.

The root `test-<candidate>` recipe similarly invokes the child test and then runs `tail` without propagating the child status.

**Impact:** a KAT result such as MISMATCH, CRYPTOFAIL, OVERFLOW, LOADFAIL, TIMEOUT, or CRASH can be recorded in logs while the surrounding Make target still succeeds. A human-readable result line and process success are therefore not equivalent.

**Closure:** explicitly return the harness/child Make status after emitting the result line.

### NGCC-IMPL-03 — Prior result files can contaminate a later failed run

The root `status` target aggregates any existing `<candidate>/results/summary.tsv` files. The build/test workflow does not establish a fresh run directory or invalidate prior summaries before attempting a new run.

Combined with the failure-status masking above, a failed current build or test can leave an older summary available for aggregation.

**Impact:** repository-level status can mix evidence from different executions unless the operator cleans first. This is a post-run contamination risk.

**Closure:** use run-scoped result directories or delete/invalidate a candidate's prior summary before beginning a new build/test attempt; bind every summary to a run ID and source/build identity.

### NGCC-IMPL-04 — Generic reproducer classification ignores the tool exit code

`tools/reproduce.sh` captures the exit status from `ngcc_attack` in `rc`, but the generic `run()` function determines CONFIRMED versus NOT-CONFIRMED from output text alone and never validates `rc`.

The attack tool documents exit 0 for confirmed, 1 for not confirmed, and 2 for load/usage errors.

**Impact:** an abnormal/error execution that happens to emit matching verdict text can be accepted by the shell runner. The normal published paths may still behave correctly, but the runner does not cryptographically or structurally bind verdict text to the expected process disposition.

**Closure:** require both the expected verdict token and its corresponding expected exit status.

### NGCC-IMPL-05 — Fresh-process equality claims use 64-bit FNV-1a rather than full-object or cryptographic equality

Fresh-process key, ciphertext, shared-secret, and signature-tail checks reduce objects to a 64-bit FNV-1a value before separate processes are compared.

**Impact:** equality of these 64-bit values is not proof that the full objects are identical. Collisions are possible and FNV-1a is not a cryptographic digest. This specifically weakens the evidence form used by the fresh-process checks for HEP-QC and VDOO.

**Closure:** emit SHA-256 (or stronger) over the full relevant object, or persist and compare the complete bytes in an isolated evidence artifact.

### NGCC-IMPL-06 — Two hash reproducers ignore candidate API error returns

`hash_collide_rate()` and `hash_prefix()` call candidate hash functions without checking their return values before comparing output buffers. Those buffers are initially zeroed by `calloc`.

By contrast, `hash_collide_zeropad()` checks and fails on a hash API error.

**Impact:** if the candidate hash call fails and leaves output untouched or partially untouched, the reproducer can compare invalid buffers and potentially report a collision/prefix relation that was not actually computed.

**Closure:** require successful return status for every candidate hash operation before evaluating output equality.

### NGCC-IMPL-07 — Signature malleability sweep uses declared maximum length rather than the actual returned signature length

`sig_malleable()` initializes `nl` from the declared metadata length, calls the signer, then computes the bit-sweep range from `m->sn_len` rather than the returned `nl`. Verification is performed with `nl`.

If an implementation returns a shorter signature than its declared maximum, bit flips beyond `nl` do not alter the verifier's input but can still be counted as accepted flips.

A related boundary exists in `sig_hint_padding()`, where the hard-coded offset is checked against `m->sn_len`, not the returned `nl`.

**Impact:** latent false-positive risk for variable-length signatures. This review has not established that the currently published Aigis-Sig+, CS, or MORNING-ATLAS findings are affected.

**Closure:** bound mutations to the actual returned signature length unless the specific finding is intentionally about bytes outside the encoded length, in which case the API semantics must be stated explicitly.

### NGCC-IMPL-08 — Candidate code executes in-process with harness privileges

The harness correctly avoids executing submitted Makefiles, scripts, objects, and prebuilt binaries. However, it compiles candidate source into shared libraries and loads those libraries directly into the KAT/reproducer process with `dlopen`.

No mandatory syscall sandbox, filesystem isolation, network isolation, privilege drop, or process boundary is evident in the public harness.

**Impact:** buggy or malicious candidate source executes with the authority of the harness process. Signal trapping and optional resource limits do not constrain arbitrary filesystem/network/process side effects.

**Closure:** execute each candidate library in a separate constrained worker/sandbox with bounded filesystem, network, process, memory, CPU, and syscall authority; preserve the worker receipt as part of the witness.

## 5. DDC interpretation of implementation findings

The implementation findings create three different classes of risk and should not be collapsed:

- **result-status integrity:** IMPL-01, IMPL-02, IMPL-03, IMPL-04;
- **false-positive / witness-integrity risk:** IMPL-05, IMPL-06, IMPL-07;
- **execution-authority risk:** IMPL-08.

None of these findings, by themselves, refute a specific candidate vulnerability. A published candidate finding should be reassessed only where its witness path actually depends on the affected harness behavior.

## 6. DDC disposition

The harness demonstrates substantial evidence discipline and strong local reproducibility.

The remaining profile gaps are primarily evidence-channel closure gaps, not evidence that the published vulnerabilities are false.

Open provenance edge != invalid technical finding.

Successful local reproduction != universally closed evidence channel.

## 7. Candidate closure architecture

official source archive
-> digest verification
-> safe archive namespace check
-> member provenance manifest
-> retained source tree
-> transformation receipts
-> pinned build environment
-> build artifact receipt
-> positive witness + negative control + mutation control
-> claim and adjudication record
-> publication receipt bound to commit and evidence cutoff
-> external reproduction records

The profile is intentionally general enough to apply to smart-contract audit harnesses, protocol conformance suites, MCP assurance systems, Agent Replay fixtures, and other DDCAL technical assessments.