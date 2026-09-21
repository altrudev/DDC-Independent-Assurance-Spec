# Revision model

Frozen state is immutable.

If a material correction or new evidence is accepted after freeze:
- create a new case revision;
- preserve the predecessor revision;
- record the reason for revision;
- identify which evidence or metadata changed;
- generate new roots;
- do not backdate new evidence into the predecessor cutoff.

Example:
CASE-0042 → CASE-0042-R1.
