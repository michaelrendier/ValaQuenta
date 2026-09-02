"""
ainulindale_engine.engine.format
==================================
THE VALAQUENTA FORMAT — the plugin / extension contract.

A ValaQuenta plugin is a directory (or a `.vqx` zip of one) carrying a
`manifest.json` that conforms to schema id **`valaquenta.plugin/1`**, plus the
Python entry module it names.  It is to PtolemyDesktop what a WebExtension is to
Firefox: a declared manifest, a typed entry point, a permission list the host
gates, and a discovery path.

    plugin type   entry.class must implement
    ───────────   ─────────────────────────────────────────────────────────
    engine        EquationModule            (engine/registry.py)
    face          name / role / probe / opinion / act   (ptolemy_console.Face)
    lens          analyse(target) -> dict
    tab           run_tab(scr) + act(query) -> str

The current per-engine `modules/<name>/manifest.json` files
(`valaquenta.engine-manifest/1`) are `format_version: 1` **engine** plugins with
`id` / `type` / `entry` / `license` implied — `normalise()` back-fills them on
read, so nothing breaks and `upgrade(write=True)` writes them out.

Full spec: `ValaQuenta/FORMAT.md`.  Machine schema:
`ValaQuenta/schema/valaquenta-plugin-1.schema.json`.

CLI:
    python3 -m ValaQuenta.engine.format schema
    python3 -m ValaQuenta.engine.format validate
    python3 -m ValaQuenta.engine.format discover
    python3 -m ValaQuenta.engine.format load <plugin-id>
    python3 -m ValaQuenta.engine.format upgrade [--write]
"""
from __future__ import annotations

import importlib
import json
import os
import pathlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import manifest as _mf

PLUGIN_SCHEMA_ID = "valaquenta.plugin/1"
FORMAT_VERSION = 1

_HERE = pathlib.Path(__file__).resolve().parent          # .../ValaQuenta/engine
_VQ = _HERE.parent                                       # .../ValaQuenta
_PLACE = _VQ.parent                                      # .../ThePlace
_SCHEMA_PATH = _VQ / "schema" / "valaquenta-plugin-1.schema.json"
_EXAMPLES = _VQ / "examples"
_USER_PLUGINS = pathlib.Path(
    os.environ.get("VALAQUENTA_HOME", pathlib.Path.home() / ".valaquenta")) / "plugins"

PLUGIN_TYPES = ("engine", "face", "lens", "tab")
KNOWN_PERMISSIONS = frozenset({
    "registry.read", "registry.run", "proof.render", "manifest.read",
    "codegate.propose", "net.search", "net.browse",
})
_ID_RE = re.compile(r"^[a-z0-9]+(\.[a-z0-9][a-z0-9_-]*)+$")
_FS_PERM_RE = re.compile(r"^fs\.read:[A-Za-z0-9_./-]+$")

# default id namespace + licence for the built-in ValaQuenta engines (Cody's
# private layer — kept behind ValaQuenta, not GNU-shipped)
_BUILTIN_NS = "org.ainulindale"
_BUILTIN_LICENSE = "LicenseRef-ValaQuenta-Private"

_SCHEMA_CACHE: Optional[Dict[str, Any]] = None


# ─────────────────────────────────────────────────────────────────────────────
#  schema
# ─────────────────────────────────────────────────────────────────────────────
def schema() -> Dict[str, Any]:
    global _SCHEMA_CACHE
    if _SCHEMA_CACHE is None:
        _SCHEMA_CACHE = json.loads(_SCHEMA_PATH.read_text())
    return _SCHEMA_CACHE


# ─────────────────────────────────────────────────────────────────────────────
#  normalise  (engine-manifest/1  ->  plugin/1)
# ─────────────────────────────────────────────────────────────────────────────
def _guess_entry_class(name: str) -> str:
    return "".join(w.capitalize() for w in name.replace("-", "_").split("_")) + "Module"


def normalise(man: Dict[str, Any], *, name: Optional[str] = None,
              path: Optional[pathlib.Path] = None) -> Dict[str, Any]:
    """Return `man` as a valaquenta.plugin/1 dict, back-filling the keys an
    engine-manifest/1 file omits, in canonical key order.  Idempotent."""
    m = dict(man)
    eng = m.get("engine") or name or m.get("name") or (path.parent.name if path else "")

    m["schema"] = PLUGIN_SCHEMA_ID
    m["format_version"] = FORMAT_VERSION
    m.setdefault("id", f"{_BUILTIN_NS}.{eng}")
    m.setdefault("type", "engine")
    m.setdefault("name", eng or m.get("display", ""))
    m.setdefault("entry", {
        "module": f"ValaQuenta.modules.{eng}",
        "class": _guess_entry_class(eng),
    })
    m.setdefault("license", _BUILTIN_LICENSE)
    m.setdefault("permissions", [])
    m.setdefault("dependencies", {})

    # canonical order: identity first, then metadata, then the big blocks,
    # then anything else the manifest carries (e.g. `engine`, `_scaffolded`)
    order = ["schema", "format_version", "id", "type", "name", "display",
             "version", "summary", "confidence_floor", "license", "entry",
             "permissions", "dependencies", "provenance", "environment", "ui"]
    out = {k: m[k] for k in order if k in m}
    for k, v in m.items():
        if k not in out:
            out[k] = v
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  entry resolution
# ─────────────────────────────────────────────────────────────────────────────
def resolve_entry(man: Dict[str, Any]) -> Dict[str, Any]:
    """{'module','class','ok','obj'|'error'} — imports the entry module and
    finds the named attribute (or, for an engine, the sole EquationModule
    subclass if the guessed name misses)."""
    m = normalise(man)
    ent = m.get("entry", {})
    mod_name, cls_name = ent.get("module", ""), ent.get("class", "")
    out = {"module": mod_name, "class": cls_name, "ok": False}
    try:
        mod = importlib.import_module(mod_name)
    except Exception as e:                                        # noqa: BLE001
        out["error"] = f"import {mod_name!r}: {type(e).__name__}: {e}"
        return out
    obj = getattr(mod, cls_name, None)
    if obj is None and m.get("type") == "engine":
        try:
            from .registry import EquationModule                  # noqa: PLC0415
            cands = [v for v in vars(mod).values()
                     if isinstance(v, type) and issubclass(v, EquationModule)
                     and v is not EquationModule]
            if len(cands) == 1:
                obj, out["class"] = cands[0], cands[0].__name__
        except Exception:                                         # noqa: BLE001
            pass
    if obj is None:
        out["error"] = f"{mod_name} has no attribute {cls_name!r}"
        return out
    out["ok"], out["obj"] = True, obj
    return out


def _type_contract_errors(ptype: str, obj: Any) -> List[str]:
    if obj is None:
        return []
    try:
        if ptype == "engine":
            from .registry import EquationModule                  # noqa: PLC0415
            if not (isinstance(obj, type) and issubclass(obj, EquationModule)):
                return ["entry.class is not an EquationModule subclass"]
        elif ptype == "lens":
            if not (callable(getattr(obj, "analyse", None)) or callable(obj)):
                return ["lens entry has no callable 'analyse'"]
        elif ptype == "tab":
            if not callable(getattr(obj, "run_tab", None)):
                return ["tab entry has no 'run_tab'"]
        elif ptype == "face":
            has = [hasattr(obj, a) for a in ("name", "act")]
            if not all(has):
                return ["face entry is not Face-shaped (needs name, act)"]
    except Exception as e:                                        # noqa: BLE001
        return [f"type-contract check failed: {type(e).__name__}: {e}"]
    return []


# ─────────────────────────────────────────────────────────────────────────────
#  validate
# ─────────────────────────────────────────────────────────────────────────────
def _schema_errors(m: Dict[str, Any]) -> List[str]:
    try:
        import jsonschema                                         # noqa: PLC0415
    except Exception:                                             # noqa: BLE001
        return _structural_errors(m)
    v = jsonschema.Draft202012Validator(schema())
    return [f"{'/'.join(str(p) for p in e.path) or '(root)'}: {e.message}"
            for e in sorted(v.iter_errors(m), key=lambda e: list(e.path))]


def _structural_errors(m: Dict[str, Any]) -> List[str]:
    """jsonschema-free fallback."""
    p: List[str] = []
    req = ("schema", "format_version", "id", "type", "name", "version",
           "entry", "provenance", "license")
    for k in req:
        if k not in m:
            p.append(f"(root): missing '{k}'")
    if m.get("schema") != PLUGIN_SCHEMA_ID:
        p.append(f"schema: expected {PLUGIN_SCHEMA_ID!r}")
    if m.get("type") not in PLUGIN_TYPES:
        p.append(f"type: {m.get('type')!r} not in {PLUGIN_TYPES}")
    if not isinstance(m.get("entry"), dict) or "module" not in m.get("entry", {}):
        p.append("entry: needs {module, class}")
    return p


def validate(man: Dict[str, Any], *, name: Optional[str] = None,
             deep: bool = True) -> List[str]:
    """Problems with `man` as a ValaQuenta plugin; [] = clean.  `deep` also
    imports the entry module and checks the type contract."""
    m = normalise(man, name=name)
    errs = list(_schema_errors(m))

    if not _ID_RE.match(str(m.get("id", ""))):
        errs.append(f"id: {m.get('id')!r} is not reverse-DNS")
    for perm in m.get("permissions", []):
        if perm not in KNOWN_PERMISSIONS and not _FS_PERM_RE.match(str(perm)):
            errs.append(f"permissions: unknown {perm!r}")
    deps = m.get("dependencies", {})
    if not isinstance(deps, dict) or any(not isinstance(v, str) for v in deps.values()):
        errs.append("dependencies: must be {plugin-id: version-range-string}")

    if deep:
        res = resolve_entry(m)
        if not res["ok"]:
            errs.append(f"entry: {res.get('error')}")
        else:
            errs.extend(f"entry: {e}" for e in
                        _type_contract_errors(m.get("type", ""), res.get("obj")))
    return errs


# ─────────────────────────────────────────────────────────────────────────────
#  discovery
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PluginInfo:
    id: str
    type: str
    name: str
    version: str
    path: str
    manifest: Dict[str, Any]
    entry: Dict[str, str] = field(default_factory=dict)
    license: str = ""
    permissions: List[str] = field(default_factory=list)
    source: str = "builtin"          # builtin | example | user | path

    @property
    def scaffolded(self) -> bool:
        return bool(self.manifest.get("_scaffolded"))


def _info_from_manifest(man: Dict[str, Any], path: pathlib.Path,
                        source: str, name_hint: Optional[str] = None) -> PluginInfo:
    m = normalise(man, name=name_hint, path=path)
    return PluginInfo(
        id=m["id"], type=m.get("type", "engine"),
        name=m.get("name", ""), version=str(m.get("version", "")),
        path=str(path), manifest=m, entry=dict(m.get("entry", {})),
        license=m.get("license", ""), permissions=list(m.get("permissions", [])),
        source=source)


def _scan_dir_of_plugins(root: pathlib.Path, source: str) -> List[PluginInfo]:
    out: List[PluginInfo] = []
    if not root.is_dir():
        return out
    for mpath in sorted(root.glob("*/manifest.json")):
        try:
            out.append(_info_from_manifest(json.loads(mpath.read_text()), mpath,
                                           source, name_hint=mpath.parent.name))
        except Exception:                                         # noqa: BLE001
            continue
    return out


def discover(paths: Optional[List[str]] = None) -> List[PluginInfo]:
    """Built-in engines, then examples, then user plugins, then
    $VALAQUENTA_PLUGIN_PATH / `paths`.  First id wins (built-in beats user)."""
    found: List[PluginInfo] = []

    # built-in engines (modules/<name>/manifest.json) via the engine loader
    for eng in _mf.available():
        man = _mf.load(eng)
        if man is None:
            continue
        mpath = _VQ / "modules" / eng / _mf.MANIFEST_NAME
        found.append(_info_from_manifest(man, mpath, "builtin", name_hint=eng))

    found += _scan_dir_of_plugins(_EXAMPLES, "example")
    found += _scan_dir_of_plugins(_USER_PLUGINS, "user")

    extra = list(paths or [])
    env = os.environ.get("VALAQUENTA_PLUGIN_PATH", "")
    extra += [p for p in env.split(os.pathsep) if p]
    for p in extra:
        pp = pathlib.Path(p).expanduser()
        if (pp / "manifest.json").is_file():
            try:
                found.append(_info_from_manifest(
                    json.loads((pp / "manifest.json").read_text()),
                    pp / "manifest.json", "path", name_hint=pp.name))
            except Exception:                                     # noqa: BLE001
                pass
        else:
            found += _scan_dir_of_plugins(pp, "path")

    seen: Dict[str, PluginInfo] = {}
    for info in found:
        seen.setdefault(info.id, info)
    return sorted(seen.values(), key=lambda i: (i.type, i.id))


def load(id_or_path: str) -> Optional[PluginInfo]:
    p = pathlib.Path(id_or_path).expanduser()
    if p.is_dir() and (p / "manifest.json").is_file():
        return _info_from_manifest(json.loads((p / "manifest.json").read_text()),
                                   p / "manifest.json", "path", name_hint=p.name)
    for info in discover():
        if info.id == id_or_path:
            return info
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  upgrade the built-in engine manifests in place
# ─────────────────────────────────────────────────────────────────────────────
def upgrade(write: bool = False) -> List[str]:
    out: List[str] = []
    for eng in _mf.available():
        mpath = _VQ / "modules" / eng / _mf.MANIFEST_NAME
        current = mpath.read_text()
        m = normalise(json.loads(current), name=eng, path=mpath)
        # verify the guessed entry resolves; fix the class name if it missed
        res = resolve_entry(m)
        if res["ok"]:
            m["entry"]["class"] = res["class"]
        rendered = json.dumps(m, indent=2, ensure_ascii=False) + "\n"
        tag = "" if res["ok"] else "  (entry UNRESOLVED)"
        if rendered == current:
            out.append(f"ok    {eng}  (plugin/1, canonical){tag}")
        elif write:
            mpath.write_text(rendered)
            _mf.clear_cache()
            out.append(f"wrote {eng}  -> id={m['id']} entry={m['entry']['class']}{tag}")
        else:
            out.append(f"would {eng}  -> id={m['id']} entry={m['entry']['class']}{tag}")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────
def _cli(argv: List[str]) -> int:
    import sys
    sys.path.insert(0, str(_PLACE))
    cmd = argv[0] if argv else "discover"

    if cmd == "schema":
        print(json.dumps(schema(), indent=2))
        return 0

    if cmd == "discover":
        for info in discover():
            tag = " [scaffold]" if info.scaffolded else ""
            print(f"  {info.type:<7} {info.id:<34} v{info.version:<7} "
                  f"{info.source:<8} {info.entry.get('class', '?')}{tag}")
        return 0

    if cmd == "load":
        if len(argv) < 2:
            print("usage: format load <plugin-id|path>"); return 2
        info = load(argv[1])
        if not info:
            print(f"not found: {argv[1]}"); return 1
        print(json.dumps({
            "id": info.id, "type": info.type, "version": info.version,
            "license": info.license, "permissions": info.permissions,
            "entry": info.entry, "path": info.path, "source": info.source,
        }, indent=2))
        return 0

    if cmd == "upgrade":
        for line in upgrade(write="--write" in argv):
            print(" ", line)
        return 0

    if cmd == "validate":
        try:
            import jsonschema  # noqa: F401
            mode = "jsonschema"
        except Exception:                                         # noqa: BLE001
            mode = "structural (jsonschema not installed)"
        print(f"[format] validation mode: {mode}\n")
        bad = 0
        for info in discover():
            errs = validate(info.manifest, name=info.name)
            if errs:
                bad += len(errs)
                print(f"  ✗ {info.id}")
                for e in errs:
                    print(f"      {e}")
            else:
                print(f"  ✓ {info.id}")
        print(f"\n{bad} problem(s) across {len(discover())} plugin(s)")
        return 1 if bad else 0

    print(__doc__)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(_cli(sys.argv[1:]))
