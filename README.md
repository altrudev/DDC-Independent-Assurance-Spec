# DDC Independent Assurance Spec

Public interoperability specification for independently produced assurance determinations over one frozen evidence set.

**Status:** pre-release draft.  
**Owner:** Valentyn Rukhaylo / Altru.dev / DDC Assurance Lab.  
**License:** No license grant is made yet. Copyright retained pending an explicit specification/software licensing decision.

The specification defines evidence cutoffs, immutable bundle identity, evaluator independence, frozen determination envelopes, post-reveal comparison, representation confirmation, and joint attestation. It does **not** define or disclose an evaluator's proprietary reasoning method.

Canonical commercial implementation: **DDC Independent Assurance** by DDC Assurance Lab.

## Domain profiles

- [DDC Research & Security Harness Assurance Profile v0.1](profiles/research-security-harness-v0.1.md) — evidence-channel closure for research, security, cryptographic, protocol, and audit harnesses.
- [NGCC Round 1 case study](cases/ngcc-round1.md) — applies the profile to a public AI-assisted cryptographic reproduction harness without treating open provenance edges as invalidation of its technical findings.
