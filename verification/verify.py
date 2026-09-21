#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def strict_load(path):
    def hook(pairs):
        out={}
        for k,v in pairs:
            if k in out: raise ValueError(f"duplicate key {k!r}")
            out[k]=v
        return out
    try:
        return json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=hook)
    except Exception as e:
        errors.append(f"{path.relative_to(ROOT)}: {e}")
        return None

schemas=sorted((ROOT/"schemas").glob("*.json"))
for p in schemas:
    value=strict_load(p)
    if value and value.get("$schema")!="https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{p.relative_to(ROOT)}: unexpected JSON Schema dialect")

required={
 "case.schema.json",
 "evidence-cutoff.schema.json",
 "evidence-bundle-envelope.schema.json",
 "determination-envelope.schema.json",
 "comparison.schema.json",
 "attestation.schema.json",
}
missing=required-{p.name for p in schemas}
if missing: errors.append("missing schemas: "+", ".join(sorted(missing)))

for p in sorted((ROOT/"examples").rglob("*.json")):
    strict_load(p)

print(f"Schemas: {len(schemas)}")
print("SPEC VERIFY:", "PASS" if not errors else "FAIL")
for e in errors: print("FAIL:",e)
sys.exit(0 if not errors else 1)
