from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def test_repository_spec_verifier_passes():
    root = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, "verification/verify.py"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, (
        "spec verifier failed\nSTDOUT:\n"
        + proc.stdout
        + "\nSTDERR:\n"
        + proc.stderr
    )
    assert "SPEC VERIFY: PASS" in proc.stdout
