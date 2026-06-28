"""
ainulindale_engine.__main__
=============================
Single callable entry point.

How it's called determines which GUI it uses:

    python3 -m ainulindale_engine              # auto-detect
    python3 -m ainulindale_engine --qt         # Qt viewer + VisPy + QTermWidget
    python3 -m ainulindale_engine --curses     # curses console (Ptolemy /derivation)
    python3 -m ainulindale_engine --headless   # no GUI, JSON output
    python3 -m ainulindale_engine --info       # print registry, exit

Ptolemy shortcut (/derivation):
    The curses mode is the self-contained console GUI that lives at
    the /derivation shortcut in Ptolemy. No Qt dependency required.

Version: 0.111
"""

import sys
import argparse

# ── Register all available modules ───────────────────────────────────────────

from .engine.registry import get_registry, register
from .modules.inversion import InversionModule
from .modules.lagrangian import LagrangianModule
from .modules.noether import NoetherModule
from .modules.noether_information import NoetherInformationModule
from .modules.berry_keating import BerryKeatingModule
from .modules.sonification import SonificationModule
from .modules.hyperwebster import HyperWebsterModule
from .modules.jwst import JWSTModule
from .modules.turing_diagonal import TuringDiagonalModule
from .modules.singularity_null import SingularityNullModule

def _register_all():
    registry = get_registry()
    register(InversionModule())
    register(LagrangianModule())
    register(NoetherModule())
    register(NoetherInformationModule())
    register(BerryKeatingModule())
    register(SonificationModule())
    register(HyperWebsterModule())
    register(JWSTModule())
    register(TuringDiagonalModule())
    register(SingularityNullModule())
    return registry

# ── GUI routers ───────────────────────────────────────────────────────────────

def _run_headless(registry):
    """Headless mode: print registry summary and exit."""
    print(registry.summary())

def _run_curses(registry):
    """Curses console GUI — Ptolemy /derivation mode."""
    try:
        from .engine.console_curses import run_curses
        run_curses(registry)
    except ImportError:
        print("[ainulindale_engine] curses console not yet built — Phase 3")
        print("Running headless mode instead.")
        _run_headless(registry)

def _run_qt(registry):
    """Qt viewer with VisPy + QTermWidget."""
    try:
        from .engine.console_qt import run_qt
        run_qt(registry)
    except ImportError:
        print("[ainulindale_engine] Qt viewer not yet built — Phase 3")
        print("Falling back to curses.")
        _run_curses(registry)

def _auto_detect(registry):
    """Auto-detect best available GUI."""
    try:
        from PyQt5 import QtWidgets
        _run_qt(registry)
    except ImportError:
        try:
            import curses
            _run_curses(registry)
        except ImportError:
            _run_headless(registry)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ainulindale Derivation Engine and Viewer",
        epilog=(
            "Ptolemy /derivation shortcut uses --curses mode.\n"
            "The GUI skin is the only difference between modes."
        )
    )
    parser.add_argument('--qt',       action='store_true', help='Qt viewer (VisPy + QTermWidget)')
    parser.add_argument('--curses',   action='store_true', help='Curses console GUI')
    parser.add_argument('--headless', action='store_true', help='No GUI, text output')
    parser.add_argument('--info',     action='store_true', help='Print registry info and exit')
    parser.add_argument('--version',  action='store_true', help='Print version and exit')

    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"ainulindale_engine {__version__}")
        return

    print("[ainulindale_engine] loading modules...")
    registry = _register_all()

    if args.info:
        print(registry.summary())
        return

    if args.headless:
        _run_headless(registry)
    elif args.curses:
        _run_curses(registry)
    elif args.qt:
        _run_qt(registry)
    else:
        _auto_detect(registry)


if __name__ == "__main__":
    main()
