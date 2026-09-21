# Freeze and hashing

A conforming implementation MUST preserve original bytes of frozen artifacts.

Two top-level identities are required:

1. **Evidence root** — binds the exact evidence set supplied to evaluators.
2. **Case root** — binds the complete case record.

Hash algorithm for v0.1: SHA-256.

Canonicalization rules for structured JSON:
- UTF-8;
- deterministic key ordering;
- no insignificant whitespace;
- arrays retain order;
- timestamps use RFC 3339;
- hashes are lowercase hexadecimal.

Implementations MUST document any container/manifest algorithm used to derive a root hash.

A corrected or expanded case MUST create a new revision rather than overwrite an earlier frozen artifact.
