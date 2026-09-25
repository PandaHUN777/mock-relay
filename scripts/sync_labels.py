"""Sync .github/labels.yml onto the GitHub repository.

Run from the repository root:

    python scripts/sync_labels.py

Requires the gh CLI to be installed and authenticated. Labels are created or
updated, never deleted, so GitHub's defaults survive.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABELS = ROOT / ".github" / "labels.yml"


def main() -> int:
    if not LABELS.exists():
        print("missing %s" % LABELS, file=sys.stderr)
        return 1
    entries = yaml.safe_load(LABELS.read_text(encoding="utf-8")) or []
    if not isinstance(entries, list):
        print("%s is not a list" % LABELS, file=sys.stderr)
        return 1

    names = [str(e.get("name") or "") for e in entries]
    if any(not n for n in names):
        print("every entry needs a name", file=sys.stderr)
        return 1
    if len(names) != len(set(names)):
        print("duplicate label names in %s" % LABELS, file=sys.stderr)
        return 1

    failed = 0
    for entry in entries:
        name = str(entry["name"])
        color = str(entry.get("color") or "ededed").lstrip("#")
        desc = str(entry.get("description") or "")
        result = subprocess.run(
            ["gh", "label", "create", name, "-c", color, "-d", desc,
             "--force"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print("ok    %s" % name)
        else:
            failed += 1
            print("fail  %s -> %s" % (name, result.stderr.strip()))

    print("%d labels, %d failed" % (len(entries), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
