"""
ainulindale_engine.engine.proof_locale
========================================
English "puzzle pieces" for the on-the-fly derivation proofs — handled the way
translations are handled with a locale catalog.

One JSON catalog per engine: `proof_locale/<engine>.json`. NO narrative — just
operator details, in order:

    descriptive   one line: what the engine does, process-only
    operators     the operators the engine is TUNED on -- symbol, english, role, tier
    ordering      the derivation steps, IN ORDER -- op + english, no connective prose
    equations     per-equation `descriptive` / `ordering` overrides

The derivation browser (`console_curses.py`, key `p`) attaches the catalog to
the proof view: `render_guided` gives the tutorial feel, `render_academic`
gives the proof skeleton the sympy on-the-fly engine fills.

Every future engine gets a catalog here (Full Engine Protocol, part 2b).
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List, Optional

_DIR = pathlib.Path(__file__).parent
_CACHE: Dict[str, Optional[Dict[str, Any]]] = {}


def available() -> List[str]:
    """Engine names that have a locale catalog."""
    return sorted(p.stem for p in _DIR.glob("*.json"))


def proof_catalog(engine: str) -> Optional[Dict[str, Any]]:
    """Load the catalog for `engine`, or None if there isn't one yet."""
    if engine in _CACHE:
        return _CACHE[engine]
    path = _DIR / f"{engine}.json"
    cat = json.loads(path.read_text()) if path.exists() else None
    _CACHE[engine] = cat
    return cat


def _resolve(cat: Dict[str, Any], eq: Optional[str]):
    """Merge engine-level fields with an equation override, if any."""
    descriptive = cat.get("descriptive", "")
    ordering = cat.get("ordering", [])
    if eq and eq in cat.get("equations", {}):
        e = cat["equations"][eq]
        descriptive = e.get("descriptive", descriptive)
        ordering = e.get("ordering", ordering)
    return descriptive, ordering, cat.get("operators", [])


def render_guided(engine: str, eq: Optional[str] = None) -> str:
    """Tutorial feel: the ordered operator steps + the operator glossary."""
    cat = proof_catalog(engine)
    if cat is None:
        return f"(no proof_locale catalog for '{engine}' yet)"
    descriptive, ordering, operators = _resolve(cat, eq)
    out = [f"GUIDED DERIVATION — {cat.get('display', engine)}"
           + (f"  ::  {eq}" if eq else ""), "", descriptive, "",
           "STEPS (operators, in order):"]
    for s in ordering:
        out.append(f"  {s.get('n', '·')}. [{s['op']}]  {s['english']}")
    if operators:
        out += ["", "OPERATORS:"]
        for o in operators:
            out.append(f"  {o['symbol']:<12} = {o['english']}")
            out.append(f"  {'':<12}   role: {o['role']}  [{o.get('tier', '')}]")
    return "\n".join(out)


def render_academic(engine: str, eq: Optional[str] = None) -> str:
    """Proof skeleton — Definitions / Construction / Result — for the sympy
    on-the-fly engine to fill."""
    cat = proof_catalog(engine)
    if cat is None:
        return f"(no proof_locale catalog for '{engine}' yet)"
    descriptive, ordering, operators = _resolve(cat, eq)
    out = [f"PROPOSITION ({cat.get('display', engine)}"
           + (f", {eq}" if eq else "") + ").", f"  {descriptive}", "",
           "DEFINITIONS."]
    for o in operators:
        out.append(f"  Let {o['symbol']} := {o['english']}.  ({o['role']})")
    out += ["", "CONSTRUCTION."]
    for s in ordering:
        out.append(f"  ({s.get('n', '·')}) Apply {s['op']}: {s['english']}")
    out += ["", "RESULT.  As stated; the step chain above is the derivation the "
            "engine executes (CALCULATED). QED-skeleton — the sympy proof engine "
            "discharges each step."]
    return "\n".join(out)
