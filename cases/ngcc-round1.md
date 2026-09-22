# Case Study: NGCC Round 1 Reproduction Harness

External project: ngcc-dev/ngcc-harness
Assessment type: architecture and evidence-channel review
Profile: DDC Research & Security Harness Assurance Profile v0.1
Status: Informational case study; not an audit, certification, or endorsement.

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

## 4. DDC disposition

The harness demonstrates substantial evidence discipline and strong local reproducibility.

The remaining profile gaps are primarily evidence-channel closure gaps, not evidence that the published vulnerabilities are false.

Open provenance edge != invalid technical finding.

Successful local reproduction != universally closed evidence channel.

## 5. Candidate closure architecture

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