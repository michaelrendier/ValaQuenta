"""
ainulindale_engine.engine.registry
=====================================
Module registry — the contract that all equation modules must satisfy.

HOW TO ADD A NEW MODULE (the code half)
========================================
1. Create a directory under ainulindale_engine/modules/your_module/
2. Add __init__.py, maths.py, tools.py
3. In maths.py, define a class that inherits from EquationModule
4. Implement all required methods (see EquationModule below)
5. Register your module: registry.register(YourModule())
6. Done. The engine and viewer pick it up automatically.

FULL ENGINE PROTOCOL (amended 2026-09-01 by Cody — SIX parts, was five)
========================================================================
Steps 1–6 above ship the code. They do not finish the engine. An engine is
not "done" until all six artifacts exist, because code alone is
undiscoverable from a cold context — which is the exact failure the
.clauderc_* family exists to prevent.

    1. ENGINE            modules/<name>/{__init__,maths,tools}.py, plus
                         registration in __main__.py::_register_all() and a
                         listing in modules/__init__.py.
    2. NOTEBOOK          notebooks/engines/NN_<name>.ipynb (or the topic
                         subdirectory) — exercises the formulary end to end
                         and shows the open items honestly.
    2b. PROOF_LOCALE     engine/proof_locale/<name>.json — the English
                         "puzzle pieces" for the on-the-fly proofs:
                         descriptive (process-only), operators
                         (symbol/english/role/tier), ordering (the
                         derivation steps, IN ORDER, no narrative),
                         and per-equation overrides. render_guided /
                         render_academic consume it; the derivation
                         browser attaches it under key `p`.
    2c. MANIFEST         modules/<name>/manifest.json — the engine carries
                         its own provenance, environmental constants, and
                         ValaQuenta-Tab / desktop-renderer plugin
                         registration. engine/manifest.py loads it;
                         menu_tree() builds The ValaQuenta Tab's menus,
                         tools, display modes and analysis lenses
                         PROCEDURALLY from these — nothing in the UI is
                         hand-maintained per engine. A missing manifest is
                         scaffolded live from the registry; write the
                         scaffolds with `python3 -m ValaQuenta.engine.manifest
                         scaffold`, then hand-fill provenance.origin (and
                         drop the `_scaffolded` flag). Schema + validator in
                         engine/manifest.py; `... manifest validate` gates it.
    3. AINULINDALE WIKI  Ainulindale/wiki/NN_<name>.md — the narrative page:
                         origin quote, what changed, honest boundaries,
                         predecessor links.
    4. VALAQUENTA WIKI   ValaQuenta/wiki/<name>.md — the engineering page:
                         file, class, claim, mechanism, confidence table.
                         Add the row to wiki/00_index.md.
    5. .clauderc_ValaQuenta ENTRY   ← NEW, added 2026-08-04.
                         export CTX_<NAME>="…" in ~/.clauderc_ValaQuenta AND
                         the module name appended to VALAQUENTA_ENGINE_INDEX,
                         so `ctxengine <name>` resolves without reading source.
                         An engine missing from that index is invisible to a
                         cold session no matter how complete its code is —
                         l_io_photon_path sat unindexed in exactly that state.

Canonical-maths changes that accompany an engine go in
~/.clauderc_canonical_maths. All ~/.clauderc* files are copied into
ContextPlease/claude/ before the push (github push protocol).

The engine does not need to know your module's internals.
Your module does not need to know the engine's internals.
They communicate only through this registry contract.

Module requirements:
    - Pure Python3. No external dependencies in maths.py.
    - All ratio arithmetic via fractions.Fraction.
    - Float only at output boundary.
    - Every equation has a confidence tier label.
    - Every equation has a radian-primary form.
    - Every equation carries `process=` — a plain-English, OUTSIDE-OBSERVER
      description of what it does AS A DERIVATION STEP ("Given X, computes Y
      by Z"), not a run narration and not a SHOUTY headline. It feeds the
      derivation engine's proof-on-the-fly (console_curses.py, the sympy
      guided tour). A missing `process=` renders as a visible TODO.
    - Every module defines `process_description` (a property; default is the
      first sentence of `description`, override for a crisper line).
    - Every engine carries a manifest (Full Engine Protocol 2c):
      modules/<name>/manifest.json — provenance, environmental constants, and
      the UI plugin-registration block the ValaQuenta Tab / desktop renderer
      read. `module.manifest()` returns it (loads the sidecar, scaffolds if
      absent).

Version: 0.113 — engine manifest (2c): provenance + env constants + UI registration
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


# ── Confidence tiers ─────────────────────────────────────────────────────────

CONFIDENCE = {
    'ESTABLISHED':   '✓',   # Verified by code and/or established mathematics
    'THEORETICAL':   '◈',   # Defined test or derivation path exists
    'CONJECTURE':    '◇',   # Named direction; no formal derivation yet
    'OPEN':          '?',   # Active open problem
}


# ── Equation descriptor ──────────────────────────────────────────────────────

class Equation:
    """
    A single named equation with metadata.

    Attributes:
        name        : short identifier (e.g. 'inversion_map')
        display     : human-readable name
        latex       : LaTeX string (for viewer rendering)
        radian_form : equation rewritten in radian-primary units
        confidence  : one of CONFIDENCE keys
        code_verified: True if backed by executable code
        params      : list of parameter names
        compute     : callable(*params) -> result
        display_options: list of viewer modes this equation supports
                         e.g. ['fano', 'complex_plane', '3d_cartesian', 'sonification']
    """

    def __init__(self, name, display, latex, radian_form,
                 confidence, code_verified, params,
                 compute=None, display_options=None, process=None):
        self.name           = name
        self.display        = display
        self.latex          = latex
        self.radian_form    = radian_form
        self.confidence     = confidence
        self.code_verified  = code_verified
        self.params         = params
        self.compute        = compute
        self.display_options = display_options or []
        # process: outside-observer, one-line "what this does as a derivation
        # step" — for the proof-on-the-fly engine and the derivation browser.
        self.process        = process

    def __repr__(self):
        tier = CONFIDENCE.get(self.confidence, '?')
        verified = '✓' if self.code_verified else '○'
        return f"[{tier}][{verified}] {self.name}: {self.display}"

    def __str__(self):
        """The DECLARATION line: a plain-English, non-involved process
        description. Falls back to a de-shouted `display`, flagged as a TODO
        when `process=` was not supplied."""
        if self.process:
            return self.process
        d = self.display
        if ':' in d:
            head, _, tail = d.partition(':')
            if head.strip().upper() == head.strip() and tail.strip():
                d = tail.strip()
        return f"{d}  [process= not set]"

    def declaration(self) -> Dict[str, Any]:
        """Everything the derivation browser / proof-on-the-fly needs about
        this step, as data."""
        return {
            'name': self.name,
            'process': str(self),
            'process_set': self.process is not None,
            'display': self.display,
            'latex': self.latex,
            'radian_form': self.radian_form,
            'confidence': self.confidence,
            'code_verified': self.code_verified,
            'params': list(self.params or []),
            'display_options': list(self.display_options),
        }


# ── Module base class ─────────────────────────────────────────────────────────

class EquationModule(ABC):
    """
    Base class for all equation modules.

    Every module in ainulindale_engine/modules/ must implement this interface.
    The engine and viewer call only these methods.
    """

    # ── Required attributes ──────────────────────────────────────────────────

    @property
    @abstractmethod
    def name(self) -> str:
        """Short module name, e.g. 'inversion'"""

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name, e.g. 'Inside-Out Inversion Engine'"""

    @property
    @abstractmethod
    def version(self) -> str:
        """Version string, e.g. '0.111'"""

    @property
    @abstractmethod
    def description(self) -> str:
        """One-paragraph description of what this module computes."""

    @property
    def process_description(self) -> str:
        """One-line, OUTSIDE-OBSERVER description of what this engine does as a
        process — for the derivation browser and the proof-on-the-fly engine.
        Default: the first sentence of `description`. Override for a crisper
        line."""
        import re
        s = ' '.join((self.description or '').split())
        parts = re.split(r'(?<=[.!?])\s+', s, maxsplit=1)
        return parts[0] if parts and parts[0] else s

    def manifest(self) -> Dict[str, Any]:
        """This engine's manifest (Full Engine Protocol 2c) —
        modules/<name>/manifest.json if written, else a live scaffold built
        from the registry.  Provenance, environmental constants, and the UI
        plugin-registration block the ValaQuenta Tab / desktop renderer read."""
        from . import manifest as _m                              # lazy: avoid cycle
        return _m.load(self.name) or _m.scaffold(self.name, self)

    @property
    @abstractmethod
    def confidence_floor(self) -> str:
        """Minimum confidence tier of claims in this module."""

    # ── Required methods ─────────────────────────────────────────────────────

    @abstractmethod
    def formulary(self) -> List[Equation]:
        """
        Return the complete list of Equation objects this module contributes.
        Called once at registration. Cached by the registry.
        """

    @abstractmethod
    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a named equation with given parameters.
        Returns a dict with at minimum:
            'result': the computed value
            'equation': the Equation object
            'params': the params used
        May include additional diagnostic keys.
        """

    @abstractmethod
    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        """
        Return data formatted for a specific viewer display mode.
        display_mode: one of 'fano', 'complex_plane', '3d_cartesian',
                              'sonification', 'text'
        Returns viewer-ready data dict. Structure depends on display_mode.
        """

    # ── Optional hooks ───────────────────────────────────────────────────────

    def on_register(self, registry: 'ModuleRegistry') -> None:
        """Called when this module is registered. Override if needed."""
        pass

    def shell_commands(self) -> Dict[str, Any]:
        """
        Optional: return dict of {command_name: callable} for the
        QTermWidget shell interface.
        Default: empty dict (no extra shell commands).
        """
        return {}

    def summary(self) -> str:
        """Return a text summary of this module for console display."""
        lines = [
            f"Module: {self.display_name}",
            f"Version: {self.version}",
            f"Description: {self.description}",
            f"Confidence floor: {self.confidence_floor}",
            f"Equations: {len(self.formulary())}",
        ]
        for eq in self.formulary():
            lines.append(f"  {eq}")
        return "\n".join(lines)


# ── Registry ─────────────────────────────────────────────────────────────────

class ModuleRegistry:
    """
    The central registry. Holds all registered equation modules.
    The engine and viewer access modules only through this object.
    """

    def __init__(self):
        self._modules: Dict[str, EquationModule] = {}
        self._formulary: Dict[str, Equation] = {}  # flat: name -> Equation

    def register(self, module: EquationModule) -> None:
        """Register a module. Calls module.on_register(self)."""
        if module.name in self._modules:
            raise ValueError(f"Module '{module.name}' already registered. "
                             f"Use a unique module name.")
        self._modules[module.name] = module
        for eq in module.formulary():
            key = f"{module.name}.{eq.name}"
            self._formulary[key] = eq
        module.on_register(self)
        print(f"  [registry] registered: {module.display_name} v{module.version} "
              f"({len(module.formulary())} equations)")

    def get_module(self, name: str) -> Optional[EquationModule]:
        return self._modules.get(name)

    def get_equation(self, full_name: str) -> Optional[Equation]:
        """full_name: 'module_name.equation_name'"""
        return self._formulary.get(full_name)

    def list_modules(self) -> List[str]:
        return list(self._modules.keys())

    def list_equations(self, module_name: Optional[str] = None) -> List[str]:
        if module_name:
            return [k for k in self._formulary if k.startswith(module_name + '.')]
        return list(self._formulary.keys())

    def run(self, full_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run a named equation: 'module.equation_name'"""
        parts = full_name.split('.', 1)
        if len(parts) != 2:
            raise ValueError(f"Use 'module.equation_name' format, got: {full_name}")
        module_name, eq_name = parts
        module = self._modules.get(module_name)
        if not module:
            raise KeyError(f"Module not found: {module_name}")
        return module.run(eq_name, params)

    def summary(self) -> str:
        lines = [
            "=" * 60,
            "  AINULINDALE ENGINE — MODULE REGISTRY",
            f"  {len(self._modules)} module(s), {len(self._formulary)} equation(s)",
            "=" * 60,
        ]
        for name, mod in self._modules.items():
            lines.append(f"\n  [{name}] {mod.display_name} v{mod.version}")
            for eq in mod.formulary():
                tier = CONFIDENCE.get(eq.confidence, '?')
                verified = '✓' if eq.code_verified else '○'
                lines.append(f"    {tier}{verified} {eq.name}: {eq.display}")
        lines.append("=" * 60)
        return "\n".join(lines)


# ── Global registry instance ─────────────────────────────────────────────────

_registry = ModuleRegistry()


def get_registry() -> ModuleRegistry:
    """Access the global registry."""
    return _registry


def register(module: EquationModule) -> None:
    """Register a module with the global registry."""
    _registry.register(module)


if __name__ == "__main__":
    print(_registry.summary())
    print()
    print("No modules registered yet. Import and register modules to populate.")
    print("Example:")
    print("  from ainulindale_engine.modules.inversion import InversionModule")
    print("  register(InversionModule())")
