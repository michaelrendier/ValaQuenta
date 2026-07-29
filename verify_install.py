#!/usr/bin/env python3
"""
verify_install.py — prove the install works.

Checks, in order:
  1. Python version
  2. third-party dependencies import
  3. every ValaQuenta engine imports
  4. a known constant comes out right

Step 4 matters most. Imports succeeding only proves the files parse; the
constant check proves the arithmetic runs. GAP is recomputed from its two
inputs rather than read back from the module, so a corrupted constant cannot
pass by agreeing with itself.

    python3 verify_install.py

Exit code 0 = everything works. Non-zero = something is wrong, and the output
says what.
"""
import importlib
import os
import sys
import traceback

# Import ValaQuenta as a package from the parent of this file's directory.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

GREEN, RED, YELLOW, DIM, RESET = (
    ('\033[32m', '\033[31m', '\033[33m', '\033[2m', '\033[0m')
    if sys.stdout.isatty() else ('', '', '', '', ''))

failures = []
warnings = []


def ok(msg):
    print(f'  {GREEN}PASS{RESET}  {msg}')


def bad(msg, detail=''):
    print(f'  {RED}FAIL{RESET}  {msg}')
    if detail:
        print(f'        {DIM}{detail}{RESET}')
    failures.append(msg)


def warn(msg, detail=''):
    print(f'  {YELLOW}SKIP{RESET}  {msg}')
    if detail:
        print(f'        {DIM}{detail}{RESET}')
    warnings.append(msg)


print('=' * 68)
print('ValaQuenta — install verification')
print('=' * 68)

# ── 1. Python version ────────────────────────────────────────────────────────
print('\n[1] Python')
v = sys.version_info
if v >= (3, 10):
    ok(f'Python {v.major}.{v.minor}.{v.micro}')
else:
    bad(f'Python {v.major}.{v.minor} is too old; 3.10 or newer required')

# ── 2. Dependencies ──────────────────────────────────────────────────────────
print('\n[2] Dependencies')
REQUIRED = ['numpy', 'scipy', 'matplotlib']
OPTIONAL = {
    'sympy': 'code/noether_engine only',
    'mpmath': 'code/io_polar.py only',
    'jupyterlab': 'needed only to open notebooks',
    'ipykernel': 'needed only to open notebooks',
    'pytest': 'needed only to run tests',
}
for name in REQUIRED:
    try:
        m = importlib.import_module(name)
        ok(f'{name} {getattr(m, "__version__", "?")}')
    except Exception as e:
        bad(f'{name} missing', f'{e.__class__.__name__}: {e}')
for name, why in OPTIONAL.items():
    try:
        m = importlib.import_module(name)
        ok(f'{name} {getattr(m, "__version__", "?")}  {DIM}({why}){RESET}')
    except Exception:
        warn(f'{name} not installed  ({why})')

# ── 3. Engines ───────────────────────────────────────────────────────────────
print('\n[3] Top-level engines')
TOPLEVEL = [
    'bao_mass_gap', 'capacitor', 'corpus', 'fixed_point', 'galactic_cavity',
    'hamiltonian', 'lexicon', 'noether', 'semantic_domain', 'semantic_word',
    'telperion', 'understand', 'zero_lattice',
]
for name in TOPLEVEL:
    try:
        importlib.import_module(f'ValaQuenta.{name}')
        ok(f'ValaQuenta.{name}')
    except Exception as e:
        bad(f'ValaQuenta.{name}', f'{e.__class__.__name__}: {e}')

print('\n[4] Engine modules')
MODULES = [
    'berry_keating', 'clay_millennium', 'constants', 'derivation_chain',
    'h_rb_hat', 'hyperwebster', 'inversion', 'jwst', 'lagrangian', 'noether',
    'noether_information', 'sigma_cavitation', 'singularity_null',
    'sonification', 'spherical', 'tier6_physics', 'tier7_cosmos',
    'tier8_sedenion', 'tier9_chem', 'translator_common', 'translator_discocat',
    'translator_vsa', 'turing_diagonal',
]
for name in MODULES:
    try:
        importlib.import_module(f'ValaQuenta.modules.{name}')
        ok(f'modules.{name}')
    except Exception as e:
        bad(f'modules.{name}', f'{e.__class__.__name__}: {e}')

# ── 5. The arithmetic actually runs ──────────────────────────────────────────
print('\n[5] Known results')
try:
    from ValaQuenta import bao_mass_gap as bmg

    # Recompute from the definition instead of trusting the stored value.
    gap = bmg.OMEGA_ZS - bmg.D_STAR * bmg.LN10
    if abs(gap - 0.000707357533248576) < 1e-15:
        ok(f'GAP recomputed = {gap!r}')
    else:
        bad(f'GAP = {gap!r}, expected 0.000707357533248576')

    # OMEGA_ZS is W(1): it must satisfy W*exp(W) = 1.
    import math
    residual = abs(bmg.OMEGA_ZS * math.exp(bmg.OMEGA_ZS) - 1.0)
    if residual < 1e-15:
        ok(f'OMEGA_ZS satisfies W*e^W = 1  (residual {residual:.2e})')
    else:
        bad(f'OMEGA_ZS fails its defining equation, residual {residual:.2e}')
except Exception:
    bad('bao_mass_gap constants', traceback.format_exc(limit=2).strip())

try:
    from ValaQuenta import zero_lattice as zl
    pairs = zl.find_zd_pairs()
    if len(pairs) == 84:
        ok('zero-divisor pairs = 84 (directed), as predicted')
    else:
        bad(f'zero-divisor pairs = {len(pairs)}, expected 84')
except Exception:
    bad('zero_lattice ZD count', traceback.format_exc(limit=2).strip())

try:
    from ValaQuenta import HamiltonianXP
    x, p = HamiltonianXP().trajectory(1.0, 1.0, t=1.0)
    if abs(x - math.e) < 1e-9 and abs(x * p - 1.0) < 1e-12:
        ok(f'H=xp conserved: x={x!r}, E={x*p!r}')
    else:
        bad(f'H=xp trajectory wrong: x={x!r}, E={x*p!r}')
except Exception:
    bad('hamiltonian trajectory', traceback.format_exc(limit=2).strip())

# ── Verdict ──────────────────────────────────────────────────────────────────
print('\n' + '=' * 68)
if failures:
    print(f'{RED}{len(failures)} check(s) FAILED{RESET}')
    for f in failures:
        print(f'  - {f}')
    print('\nValaQuenta is not correctly installed.')
    sys.exit(1)

print(f'{GREEN}All checks passed.{RESET}'
      + (f'  ({len(warnings)} optional component(s) not installed)'
         if warnings else ''))
print("""
Next:
    python3 -c "from ValaQuenta.bao_mass_gap import validate; validate()"
    python3 -m ValaQuenta --info
    jupyter lab notebooks/

Start with notebooks/engines/ for the top-level engines, or
wiki/00_index.md for results without running anything.
""")
sys.exit(0)
