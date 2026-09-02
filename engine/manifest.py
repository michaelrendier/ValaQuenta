"""
ainulindale_engine.engine.manifest
====================================
The ENGINE MANIFEST — the additional required class of engine data (Cody,
2026-09-01).  One JSON file per engine, carried BY the module:

    modules/<engine>/manifest.json

The module carries its own provenance, its environmental constants, and its
ValaQuenta-Tab / desktop-renderer plugin-registration information.  The
curses UI (The ValaQuenta Tab) reads these to build its menus, tools and
display options PROCEDURALLY — nothing in the UI is hand-maintained per
engine any more.  This is the standard Python packaging pattern (metadata +
entry points shipped as data files inside the package).

Where proof_locale/<engine>.json answers "how do I narrate the proof", the
manifest answers "how do I appear in the tool, what do I depend on, and
where did I come from".

This file loads and scaffolds the per-engine manifest and builds the Tab's
menu_tree.  The manifest IS the `type: engine` case of THE VALAQUENTA FORMAT
(`valaquenta.plugin/1`, ../FORMAT.md) — schema validation is delegated to
engine/format.py; `format.normalise()` upgrades a bare
`valaquenta.engine-manifest/1` file on read.

SCHEMA  (schema id: "valaquenta.engine-manifest/1")
--------------------------------------------------
    engine            str   — MUST equal module.name
    display           str   — module.display_name
    version           str   — tracks module.version
    summary           str   — one line for the menu row
    confidence_floor  str   — ESTABLISHED | THEORETICAL | CONJECTURE | OPEN

    provenance:
        origin        str        — where the idea entered (short, factual)
        authors       [str]
        created       str        — ISO date
        status_label  str        — e.g. "THEORETICAL:CALCULATED"
        predecessors  [str]      — sibling engine names this one grows from
        citations     [str]      — bibliography keys (Ainulindale/wiki/98)
        wiki:
            ainulindale  str     — repo-relative path
            valaquenta   str
        notebook      str        — repo-relative path
        proof_locale  str        — repo-relative path

    environment:
        constants     [ {symbol, role, value|null, source} ]
        native_space  str        — default "spherical complex radial polar"
        arithmetic    str        — default "fractions.Fraction exact; float only at boundary"
        requires_engines [str]   — sibling engines called at runtime
        external      [str]      — outside packages (e.g. "FactoralDecomposition.engine")

    ui:
        menu:  { label, group, order:int, blurb }
        tools: [ {name, equation, label, desc, params:[str]} ]
        display_modes    [str]
        analysis_lenses  [str]   — subset of engine/console_curses ANALYSIS_TOOLS,
                                   or engine-specific lens names
        proof:  { guided:bool, academic:bool }
        desktop: { window, surface, opengl:bool, pgui_widgets:[str] }

Any missing engine is SCAFFOLDED on the fly from the registry + path
conventions, so the Tab is always complete.  `scaffold_all()` writes the
scaffolds to disk for hand-refinement.

Full Engine Protocol: this file is part 2c.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List, Optional

SCHEMA_ID = "valaquenta.engine-manifest/1"
MANIFEST_NAME = "manifest.json"

_HERE = pathlib.Path(__file__).resolve().parent          # .../ValaQuenta/engine
_VQ = _HERE.parent                                       # .../ValaQuenta
_PLACE = _VQ.parent                                      # .../ThePlace
_MODULES = _VQ / "modules"

_CACHE: Dict[str, Optional[Dict[str, Any]]] = {}

_DEFAULT_NATIVE_SPACE = "spherical complex radial polar"
_DEFAULT_ARITHMETIC = "fractions.Fraction exact; float only at output boundary"
_DEFAULT_DISPLAY_MODES = ["text"]
_GLOBAL_LENSES = ["emerge", "spectral", "lineage", "calibrate"]


# ─────────────────────────────────────────────────────────────────────────────
#  load
# ─────────────────────────────────────────────────────────────────────────────
def _manifest_path(engine: str) -> pathlib.Path:
    return _MODULES / engine / MANIFEST_NAME


def available() -> List[str]:
    """Engine names that have a manifest.json on disk."""
    return sorted(p.parent.name for p in _MODULES.glob(f"*/{MANIFEST_NAME}"))


def load(engine: str) -> Optional[Dict[str, Any]]:
    """Load the manifest for `engine`, or None if it hasn't been written yet."""
    if engine in _CACHE:
        return _CACHE[engine]
    path = _manifest_path(engine)
    data = json.loads(path.read_text()) if path.exists() else None
    _CACHE[engine] = data
    return data


def clear_cache() -> None:
    _CACHE.clear()


# ─────────────────────────────────────────────────────────────────────────────
#  path-convention provenance discovery
# ─────────────────────────────────────────────────────────────────────────────
def _rel(p: pathlib.Path) -> str:
    try:
        return str(p.resolve().relative_to(_PLACE))
    except ValueError:
        return str(p)


def _first(glob_root: pathlib.Path, pattern: str) -> str:
    hits = sorted(glob_root.glob(pattern))
    return _rel(hits[0]) if hits else ""


def _discover_paths(engine: str) -> Dict[str, str]:
    vq_wiki = _VQ / "wiki" / f"{engine}.md"
    pl = _HERE / "proof_locale" / f"{engine}.json"
    return {
        "valaquenta_wiki": _rel(vq_wiki) if vq_wiki.exists() else "",
        "ainulindale_wiki": _first(_PLACE / "Ainulindale" / "wiki",
                                   f"*{engine}*.md"),
        "notebook": _first(_VQ / "notebooks", f"**/*{engine}*.ipynb"),
        "proof_locale": _rel(pl) if pl.exists() else "",
    }


# ─────────────────────────────────────────────────────────────────────────────
#  scaffold  (registry introspection -> a filled-in manifest dict)
# ─────────────────────────────────────────────────────────────────────────────
_GROUP_HINTS = {
    "emerger": "Sedenion · ZD geometry",
    "box_kite": "Sedenion · ZD geometry",
    "angular_rank": "Sedenion · ZD geometry",
    "t32_nilpotency": "Sedenion · ZD geometry",
    "tier8_sedenion": "Sedenion · ZD geometry",
    "archimedes_screw": "Primes · number theory",
    "hyperwebster": "Primes · number theory",
    "hypergon_constructibility": "Primes · number theory",
    "sigma_expansion": "Critical line · σ",
    "berry_keating": "Critical line · σ",
    "noether": "Currents · conservation",
    "noether_information": "Currents · conservation",
    "lagrangian": "Currents · conservation",
    "inversion": "Inside-out · inversion",
    "scale": "Decomposition · The Scale",
    "add_scale_sign": "Decomposition · The Scale",
    "units": "Decomposition · The Scale",
    "bao_mass_gap": "Cosmology · physics",
    "desitter_cavitation": "Cosmology · physics",
    "sigma_cavitation": "Cosmology · physics",
    "tier6_physics": "Cosmology · physics",
    "tier7_cosmos": "Cosmology · physics",
    "tier9_chem": "Cosmology · physics",
    "jwst": "Cosmology · physics",
    "l_io_photon_path": "Cosmology · physics",
    "spherical": "Cosmology · physics",
    "singularity_null": "Tower · identity",
    "turing_diagonal": "Tower · identity",
    "h_rb_hat": "Tower · identity",
    "sonification": "Instruments · display",
    "udeo_crypto": "UDEO · translation",
    "translator_common": "UDEO · translation",
    "translator_discocat": "UDEO · translation",
    "translator_vsa": "UDEO · translation",
    "clay_millennium": "Lineage · decomposition",
    "derivation_chain": "Lineage · decomposition",
    "constants": "Reference",
}


def scaffold(engine: str, module: Any) -> Dict[str, Any]:
    """Build a manifest dict for `engine` from what the module already knows
    plus the path conventions.  Text-only provenance fields are left blank
    (or 'TODO') for a human to fill; everything mechanical is populated."""
    disc = _discover_paths(engine)
    eqs = list(module.formulary())

    modes: List[str] = []
    for eq in eqs:
        for m in (eq.display_options or []):
            if m not in modes:
                modes.append(m)
    modes = modes or list(_DEFAULT_DISPLAY_MODES)

    tools = [{
        "name": eq.name,
        "equation": eq.name,
        "label": _titlecase(eq.name),
        "desc": (str(eq).split(".")[0])[:110],
        "params": list(eq.params or []),
    } for eq in eqs]

    have_locale = bool(disc["proof_locale"])

    return {
        "schema": SCHEMA_ID,
        "engine": engine,
        "display": module.display_name,
        "version": module.version,
        "summary": module.process_description[:140],
        "confidence_floor": module.confidence_floor,
        "provenance": {
            "origin": "",
            "authors": ["Cody Michael Allison"],
            "created": "",
            "status_label": module.confidence_floor,
            "predecessors": [],
            "citations": [],
            "wiki": {
                "ainulindale": disc["ainulindale_wiki"],
                "valaquenta": disc["valaquenta_wiki"],
            },
            "notebook": disc["notebook"],
            "proof_locale": disc["proof_locale"],
        },
        "environment": {
            "constants": [],
            "native_space": _DEFAULT_NATIVE_SPACE,
            "arithmetic": _DEFAULT_ARITHMETIC,
            "requires_engines": [],
            "external": [],
        },
        "ui": {
            "menu": {
                "label": module.display_name,
                "group": _GROUP_HINTS.get(engine, "Engines"),
                "order": 100,
                "blurb": module.process_description[:200],
            },
            "tools": tools,
            "display_modes": modes,
            "analysis_lenses": list(_GLOBAL_LENSES),
            "proof": {"guided": have_locale, "academic": have_locale},
            "desktop": {
                "window": "PDesktopWindow",
                "surface": "svg",
                "opengl": True,
                "pgui_widgets": [],
            },
        },
        "_scaffolded": True,
    }


def _titlecase(name: str) -> str:
    return " ".join(w.capitalize() for w in name.replace("-", "_").split("_"))


# ─────────────────────────────────────────────────────────────────────────────
#  menu_tree  —  what The ValaQuenta Tab consumes
# ─────────────────────────────────────────────────────────────────────────────
def entry_for(engine: str, module: Any) -> Dict[str, Any]:
    """The manifest for `engine` if written, else a live scaffold.  Always a
    complete dict — the Tab never has to special-case a missing file."""
    man = load(engine)
    if man is None:
        man = scaffold(engine, module)
    return man


def menu_tree(registry: Any) -> Dict[str, Any]:
    """Procedural menu for the whole registry, grouped and ordered.

    Returns:
        {
          "groups": [ {group, order, engines:[entry,...]}, ... ],   # sorted
          "missing_manifest": [engine, ...],                        # scaffolded live
          "count": int,
        }
    where each `entry` is  {engine, display, summary, status, menu, tools,
    display_modes, analysis_lenses, proof, provenance, environment, desktop}.
    """
    by_group: Dict[str, Dict[str, Any]] = {}
    missing: List[str] = []

    for engine in registry.list_modules():
        module = registry.get_module(engine)
        man = load(engine)
        if man is None:
            man = scaffold(engine, module)
            missing.append(engine)

        ui = man.get("ui", {})
        menu = ui.get("menu", {})
        group = menu.get("group") or "Engines"
        entry = {
            "engine": engine,
            "display": man.get("display", module.display_name),
            "summary": man.get("summary", ""),
            "status": man.get("provenance", {}).get("status_label",
                                                    man.get("confidence_floor", "")),
            "menu": menu,
            "tools": ui.get("tools", []),
            "display_modes": ui.get("display_modes", list(_DEFAULT_DISPLAY_MODES)),
            "analysis_lenses": ui.get("analysis_lenses", list(_GLOBAL_LENSES)),
            "proof": ui.get("proof", {"guided": False, "academic": False}),
            "provenance": man.get("provenance", {}),
            "environment": man.get("environment", {}),
            "desktop": ui.get("desktop", {}),
            "scaffolded": bool(man.get("_scaffolded")),
        }
        g = by_group.setdefault(group, {"group": group, "order": menu.get("order", 100),
                                        "engines": []})
        g["order"] = min(g["order"], menu.get("order", 100))
        g["engines"].append(entry)

    groups = sorted(by_group.values(), key=lambda g: (g["order"], g["group"]))
    for g in groups:
        g["engines"].sort(key=lambda e: (e["menu"].get("order", 100), e["display"]))

    return {"groups": groups, "missing_manifest": sorted(missing),
            "count": len(registry.list_modules())}


# ─────────────────────────────────────────────────────────────────────────────
#  validate
# ─────────────────────────────────────────────────────────────────────────────
_REQUIRED_TOP = ("schema", "engine", "display", "version", "summary",
                 "confidence_floor", "provenance", "environment", "ui")
_REQUIRED_PROV = ("origin", "authors", "created", "status_label",
                  "predecessors", "citations", "wiki", "notebook", "proof_locale")
_REQUIRED_UI = ("menu", "tools", "display_modes", "analysis_lenses",
                "proof", "desktop")


def validate(engine: str, module: Any = None) -> List[str]:
    """Problems with `engine`'s manifest; [] means clean.  The schema check is
    delegated to the ValaQuenta Format validator (`engine/format.py`,
    `valaquenta.plugin/1`); the engine-specific cross-checks (version match,
    tool→equation, origin filled) stay here."""
    man = load(engine)
    if man is None:
        return [f"{engine}: no manifest.json (run scaffold_all to seed it)"]
    p: List[str] = []

    try:
        from . import format as _fmt                              # noqa: PLC0415
        p += [f"{engine}: {e}" for e in _fmt.validate(man, name=engine)]
    except Exception as e:                                        # noqa: BLE001
        # format.py unavailable — fall back to the local structural check
        for k in _REQUIRED_TOP:
            if k not in man and k != "engine":
                p.append(f"{engine}: missing top-level '{k}'")
        p.append(f"{engine}: (format.py check skipped: {type(e).__name__}: {e})")

    prov = man.get("provenance", {})
    for k in _REQUIRED_PROV:
        if k not in prov:
            p.append(f"{engine}: provenance missing '{k}'")
    ui = man.get("ui", {})
    for k in _REQUIRED_UI:
        if k not in ui:
            p.append(f"{engine}: ui missing '{k}'")
    if module is not None:
        if man.get("version") != module.version:
            p.append(f"{engine}: manifest version {man.get('version')!r} != "
                     f"module {module.version!r}")
        eq_names = {eq.name for eq in module.formulary()}
        for t in ui.get("tools", []):
            if t.get("equation") and t["equation"] not in eq_names:
                p.append(f"{engine}: tool {t.get('name')!r} -> unknown equation "
                         f"{t['equation']!r}")
    if not man.get("_scaffolded") and not prov.get("origin"):
        p.append(f"{engine}: provenance.origin is blank (hand-fill it)")
    return p


# ─────────────────────────────────────────────────────────────────────────────
#  write scaffolds to disk
# ─────────────────────────────────────────────────────────────────────────────
def write_scaffold(engine: str, module: Any, overwrite: bool = False) -> str:
    path = _manifest_path(engine)
    if path.exists() and not overwrite:
        return f"skip  {engine}  (exists)"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = scaffold(engine, module)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    clear_cache()
    return f"wrote {engine}  -> {_rel(path)}"


def scaffold_all(registry: Any, overwrite: bool = False) -> List[str]:
    out = []
    for engine in registry.list_modules():
        out.append(write_scaffold(engine, registry.get_module(engine), overwrite))
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  CLI  —  python3 -m ValaQuenta.engine.manifest [scaffold|validate|menu]
# ─────────────────────────────────────────────────────────────────────────────
def _cli(argv: List[str]) -> int:
    import sys
    sys.path.insert(0, str(_PLACE))
    from ValaQuenta.__main__ import _register_all       # noqa: PLC0415
    reg = _register_all()
    cmd = argv[0] if argv else "menu"

    if cmd == "scaffold":
        for line in scaffold_all(reg, overwrite="--force" in argv):
            print(" ", line)
    elif cmd == "validate":
        bad = 0
        for engine in reg.list_modules():
            probs = validate(engine, reg.get_module(engine))
            for pr in probs:
                print("  ✗", pr)
                bad += 1
            if not probs:
                print("  ✓", engine)
        print(f"\n{bad} problem(s)")
        return 1 if bad else 0
    elif cmd == "menu":
        tree = menu_tree(reg)
        for g in tree["groups"]:
            print(f"\n=== {g['group']}  (order {g['order']}) ===")
            for e in g["engines"]:
                tag = " [scaffold]" if e["scaffolded"] else ""
                print(f"  {e['display']:<38} {e['status']:<22} "
                      f"{len(e['tools'])} tools{tag}")
        if tree["missing_manifest"]:
            print(f"\nno manifest yet (scaffolded live): "
                  f"{', '.join(tree['missing_manifest'])}")
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(_cli(sys.argv[1:]))
