"""
ValaQuenta.__main__
===================
Single callable entry point.

How it's called determines which GUI it uses:

    python3 -m ValaQuenta              # auto-detect
    python3 -m ValaQuenta --qt         # Qt viewer + VisPy + QTermWidget
    python3 -m ValaQuenta --curses     # curses console (Ptolemy /derivation)
    python3 -m ValaQuenta --headless   # no GUI, JSON output
    python3 -m ValaQuenta --info       # print registry, exit

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
from .modules.sigma_expansion import SigmaExpansionModule
from .modules.t32_nilpotency import T32NilpotencyModule
from .modules.hypergon_constructibility import HypergonConstructibilityModule
from .modules.l_io_photon_path import LIOPhotonPathModule
from .modules.archimedes_screw import ArchimedesScrewModule
from .modules.box_kite import BoxKiteModule
from .modules.bao_mass_gap import BaoMassGapModule
from .modules.angular_rank import AngularRankModule
from .modules.scale import ScaleModule
from .modules.units import UnitsModule
from .modules.add_scale_sign import AddScaleSignModule
from .modules.desitter_cavitation import DeSitterCavitationModule
from .modules.emerger import EmergerModule
from .modules.constants import ConstantsModule
from .modules.derivation_chain import DerivationChainModule
from .modules.h_rb_hat import SigmaRBModule
from .modules.clay_millennium import ClayMillenniumModule
from .modules.tier6_physics import Tier6PhysicsModule
from .modules.tier7_cosmos import Tier7CosmosModule
from .modules.tier8_sedenion import Tier8SedenionModule
from .modules.tier9_chem import Tier9ChemModule
from .modules.translator_discocat import DisCoCatTranslatorModule
from .modules.translator_vsa import VSATranslatorModule
from .modules.udeo_crypto import UDEOCryptoModule
from .modules.bracketing_firing_order import BracketingFiringOrderModule
from .modules.oblique_gear import ObliqueGearModule
from .modules.prime_gauge_field import PrimeGaugeFieldModule
from .modules.spectral_primes import SpectralPrimesModule

def _register_all():
    registry = get_registry()
    register(BaoMassGapModule())   # headline result — first in the module list
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
    register(SigmaExpansionModule())
    register(T32NilpotencyModule())
    register(HypergonConstructibilityModule())
    register(LIOPhotonPathModule())
    register(ArchimedesScrewModule())
    register(BoxKiteModule())
    register(AngularRankModule())
    register(ScaleModule())
    register(UnitsModule())
    register(AddScaleSignModule())
    register(DeSitterCavitationModule())
    register(EmergerModule())
    register(ConstantsModule())
    register(DerivationChainModule())
    register(SigmaRBModule())
    register(ClayMillenniumModule())
    register(Tier6PhysicsModule())
    register(Tier7CosmosModule())
    register(Tier8SedenionModule())
    register(Tier9ChemModule())
    register(DisCoCatTranslatorModule())
    register(VSATranslatorModule())
    register(UDEOCryptoModule())
    register(BracketingFiringOrderModule())
    register(ObliqueGearModule())
    register(PrimeGaugeFieldModule())
    register(SpectralPrimesModule())
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
    except ImportError as exc:
        print(f"[ValaQuenta] curses console unavailable ({exc})")
        print("Running headless mode instead.")
        _run_headless(registry)

def _run_qt(registry):
    """Qt viewer with VisPy + QTermWidget."""
    try:
        from .engine.console_qt import run_qt
        run_qt(registry)
    except ImportError as exc:
        print(f"[ValaQuenta] Qt viewer unavailable ({exc})")
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
    """
    Parse the command line, register the modules and launch the requested interface.

    Flags: --qt, --curses, --headless, --info, --manifests, --version. With no
    flag the best available interface is chosen automatically.
    """
    parser = argparse.ArgumentParser(
        description="ValaQuenta Derivation Engine and Viewer",
        epilog=(
            "Ptolemy /derivation shortcut uses --curses mode.\n"
            "The GUI skin is the only difference between modes."
        )
    )
    parser.add_argument('--qt',       action='store_true', help='Qt viewer (VisPy + QTermWidget)')
    parser.add_argument('--curses',   action='store_true', help='Curses console GUI')
    parser.add_argument('--headless', action='store_true', help='No GUI, text output')
    parser.add_argument('--info',     action='store_true', help='Print registry info and exit')
    parser.add_argument('--manifests', action='store_true',
                        help='Validate the engine manifests (Full Engine Protocol 2c) and exit')
    parser.add_argument('--version',  action='store_true', help='Print version and exit')

    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"ValaQuenta {__version__}")
        return

    print("[ValaQuenta] loading modules...")
    get_registry().verbose = True
    registry = _register_all()

    if args.info:
        print(registry.summary())
        return

    if args.manifests:
        from .engine import manifest as _m
        bad = 0
        for engine in registry.list_modules():
            probs = _m.validate(engine, registry.get_module(engine))
            for pr in probs:
                print("  ✗", pr); bad += 1
            if not probs:
                print("  ✓", engine)
        tree = _m.menu_tree(registry)
        print(f"\n{len(tree['groups'])} menu groups, {tree['count']} engines, "
              f"{bad} manifest problem(s)")
        if tree['missing_manifest']:
            print("  (live scaffold, not written: "
                  + ", ".join(tree['missing_manifest']) + ")")
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
