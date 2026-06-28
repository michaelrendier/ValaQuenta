"""
ainulindale_engine.engine.registry
=====================================
Module registry — the contract that all equation modules must satisfy.

HOW TO ADD A NEW MODULE
========================
1. Create a directory under ainulindale_engine/modules/your_module/
2. Add __init__.py, maths.py, tools.py
3. In maths.py, define a class that inherits from EquationModule
4. Implement all required methods (see EquationModule below)
5. Register your module: registry.register(YourModule())
6. Done. The engine and viewer pick it up automatically.

The engine does not need to know your module's internals.
Your module does not need to know the engine's internals.
They communicate only through this registry contract.

Module requirements:
    - Pure Python3. No external dependencies in maths.py.
    - All ratio arithmetic via fractions.Fraction.
    - Float only at output boundary.
    - Every equation has a confidence tier label.
    - Every equation has a radian-primary form.

Version: 0.111
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
                 compute=None, display_options=None):
        self.name           = name
        self.display        = display
        self.latex          = latex
        self.radian_form    = radian_form
        self.confidence     = confidence
        self.code_verified  = code_verified
        self.params         = params
        self.compute        = compute
        self.display_options = display_options or []

    def __repr__(self):
        tier = CONFIDENCE.get(self.confidence, '?')
        verified = '✓' if self.code_verified else '○'
        return f"[{tier}][{verified}] {self.name}: {self.display}"


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
