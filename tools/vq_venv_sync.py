#!/usr/bin/env python3
"""
vq_venv_sync.py — mirror package installs into the ValaQuenta .venv.

POLICY (Cody, 2026-08-15): VALAQUENTA IS THE ROOT ENVIRONMENT.

    "anything at all in the entire github that is used in the python3 work
     that is installed into any repo should FIRST be installed into
     ValaQuenta to minimize versioning errors down the line... then that
     root install is used to specific software in the actual repo"

So the order is: ValaQuenta first, repo second. This script enforces the
first half automatically.

    ADD      everything. No package is withheld on size or system-library
             grounds -- a repo that needs it needs it, and a failed install
             is a debugging task, not a reason to refuse. Large or
             system-dependent packages are installed and ANNOTATED in the
             ledger so the cost is visible.
    NEVER    uninstall. Installs propagate upward; removals do not. A repo
             dropping a dependency must not disarm every other repo.
    NEVER    silently downgrade a version already pinned here. This is the
             one guard that serves the stated goal directly: a silent numpy
             downgrade breaks astropy, scipy and the compressed-FITS codecs
             at once. A genuine version conflict between two repos is a real
             problem to surface, not to resolve by coin flip -- it is logged
             as a conflict and left for a human call.

Everything it declines to do is written to the ledger. The ledger is the
point: a skip that is invisible is the same failure mode as the ear wired
through L_a.

Usage:
    vq_venv_sync.py --from-command "pip install foo bar"    # hook entry
    vq_venv_sync.py --packages foo bar                      # direct
    vq_venv_sync.py --status                                # show ledger
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VQ_ROOT   = Path("/home/rendier/Projects/ThePlace/ValaQuenta")
VQ_PY     = VQ_ROOT / ".venv" / "bin" / "python"
LEDGER    = VQ_ROOT / "tools" / "venv_sync_ledger.jsonl"

# NOT a blocklist. These are installed like anything else; the note is
# recorded alongside so the disk/system cost stays visible in the ledger.
# Formerly the "NOT INSTALLED HERE" section of requirements.txt — superseded
# 2026-08-15 by the root-environment policy above.
ANNOTATE = {
    "openai-whisper": "large: pulls torch (~2-3 GB)",
    "whisper":        "large: pulls torch (~2-3 GB)",
    "torch":          "large: ~2-3 GB",
    "pyrtlsdr":       "needs system librtlsdr",
    "pyaudio":        "needs system portaudio19-dev",
    "selenium":       "needs a webdriver binary",
    "pyqt5":          "large: bundles Qt5",
    "pyqt6":          "large: bundles Qt6",
    "qtermwidget":    "no PyPI package — expect failure; ships with the system lib",
    "bpy":            "Blender's Python — expect failure",
    "mathutils":      "Blender's Python — expect failure",
    "espeak":         "system binary, not a Python package — expect failure",
    "rm-tools":       "Faraday rotation; BulletCluster keeps its own pin",
}

INSTALL_RE = re.compile(r"\bpip3?\b.*\binstall\b|\bpip\b.*\binstall\b")
REMOVE_RE  = re.compile(r"\bpip3?\b.*\b(uninstall|remove)\b")


def log(entry: dict) -> None:
    entry["ts"] = datetime.now().isoformat(timespec="seconds")
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps(entry) + "\n")


def installed_version(pkg: str):
    """Version already present in the ValaQuenta venv, or None."""
    try:
        out = subprocess.run(
            [str(VQ_PY), "-m", "pip", "show", pkg],
            capture_output=True, text=True, timeout=60,
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    for line in out.stdout.splitlines():
        if line.lower().startswith("version:"):
            return line.split(":", 1)[1].strip()
    return None


def parse_packages(command: str):
    """Package names from a pip install command. Requirements files ignored."""
    try:
        parts = shlex.split(command)
    except ValueError:
        return []
    pkgs, seen_install = [], False
    skip_next = False
    for p in parts:
        if skip_next:
            skip_next = False
            continue
        if p == "install":
            seen_install = True
            continue
        if not seen_install:
            continue
        if p in ("-r", "--requirement", "-c", "--constraint", "-t", "--target",
                 "--index-url", "-i", "--extra-index-url", "--find-links", "-f"):
            skip_next = True
            continue
        if p.startswith("-"):
            continue
        if p.endswith((".txt", ".whl", ".tar.gz")) or "/" in p:
            continue
        pkgs.append(p)
    return pkgs


def base_name(spec: str) -> str:
    return re.split(r"[<>=!~\[]", spec, 1)[0].strip().lower()


def sync(packages, dry_run=False):
    results = []
    for spec in packages:
        name = base_name(spec)
        if not name:
            continue

        note = ANNOTATE.get(name)
        have = installed_version(name)
        pinned = re.search(r"[<>=!~]", spec)

        # The one guard: never silently change a version already pinned here.
        if have and pinned:
            r = {"package": spec, "action": "conflict",
                 "reason": f"ValaQuenta already has {name} {have}; this asks for "
                           f"'{spec}'. NOT changed — a cross-repo version conflict "
                           f"is a human call, not a coin flip."}
            results.append(r); log(r); continue

        if have:
            r = {"package": spec, "action": "already-present", "version": have}
            results.append(r); log(r); continue

        if dry_run:
            r = {"package": spec, "action": "would-install"}
            if note:
                r["note"] = note
            results.append(r); continue

        proc = subprocess.run(
            [str(VQ_PY), "-m", "pip", "install", "--upgrade-strategy", "only-if-needed", spec],
            capture_output=True, text=True, timeout=1800,
        )
        if proc.returncode == 0:
            r = {"package": spec, "action": "installed",
                 "version": installed_version(name)}
        else:
            r = {"package": spec, "action": "failed",
                 "reason": proc.stderr.strip().splitlines()[-1] if proc.stderr else "unknown"}
        if note:
            r["note"] = note
        results.append(r); log(r)
    return results


def main():
    ap = argparse.ArgumentParser(description="Guarded ValaQuenta venv mirror.")
    ap.add_argument("--from-command", help="a shell command; pip installs are extracted")
    ap.add_argument("--packages", nargs="*", help="package specs directly")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true", help="print the ledger tail")
    args = ap.parse_args()

    if args.status:
        if not LEDGER.exists():
            print("ledger empty — nothing has been mirrored yet")
            return
        rows = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
        print(f"{len(rows)} ledger entries. Last 20:\n")
        for r in rows[-20:]:
            extra = r.get("version") or r.get("reason", "")
            print(f"  {r['ts']}  {r['action']:<15} {r['package']:<24} {extra}")
        skipped = [r for r in rows if r["action"] == "skipped"]
        if skipped:
            print(f"\n{len(skipped)} skipped — apply by hand if actually wanted.")
        return

    if not VQ_PY.exists():
        print(f"ValaQuenta venv not found at {VQ_PY}", file=sys.stderr)
        sys.exit(0)          # never block the caller's workflow

    pkgs = list(args.packages or [])
    if args.from_command:
        cmd = args.from_command
        if REMOVE_RE.search(cmd):
            log({"package": cmd[:120], "action": "ignored-removal",
                 "reason": "policy: never uninstall from the shared venv"})
            return
        if not INSTALL_RE.search(cmd):
            return
        # do not recurse on our own installs
        if str(VQ_PY) in cmd:
            return
        pkgs += parse_packages(cmd)

    if not pkgs:
        return

    for r in sync(pkgs, dry_run=args.dry_run):
        extra = r.get("version") or r.get("reason", "")
        print(f"[vq-sync] {r['action']:<15} {r['package']:<24} {extra}")


if __name__ == "__main__":
    main()
