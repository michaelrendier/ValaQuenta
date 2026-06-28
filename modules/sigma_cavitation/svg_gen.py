"""
sigma_cavitation.svg_gen
========================
Generate σ-parameterised sedenion cavitation SVG.

SVG encodes the dual Riemann/Fermat structure:

  <text>   nodes  = Riemann zeros (causal events, quantised, Riemann)
  <path C> curves = Fermat geodesics (causal constraints, geometric, Fermat)
  <path L> line   = Mind's Eye caustic (connected amplitude tips = meaning)
  <circle> void   = cavitation radius ∝ |σ − ½|

σ controls the cavitation geometry and Bézier curvature:
  σ → ½   minimal void, nearly-straight paths  (QM / fixed point)
  σ = 1   void grows, paths bow outward         (Yang-Mills / pole)
  σ = 2   compact clusters, tight void          (GR / mass)
  σ < ½   inward-bowing paths, no zero labels   (Fermat forbidden)

Output: ~/.ptolemy/images/sedenion_cavitation_s{sigma*100:03.0f}_{ts}.svg
        also copied to Ainulindale/wiki/images/ if the repo is reachable.
"""

import math
import time
import shutil
from pathlib import Path

# ── Constants (mirrors h_rb_hat/maths.py — standalone so no package import needed) ──

_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

_RIEMANN_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446247, 59.347044, 60.831778, 65.112544,
    67.079811,
]

_SIGMA_CRITICAL   = 0.5
_SIGMA_YANG_MILLS = 1.0
_SIGMA_GR         = 2.0

# Sector colours match draw.py _SECTOR
_SECTOR = [
    '#9966ff', '#9966ff',  # e0-e1  scalar / pronominal
    '#ffee00', '#ffee00',  # e2-e3  verb / noun
    '#44dd88', '#44dd88', '#44dd88', '#44dd88',  # e4-e7  adj/adv/rel/det
    '#ff4444', '#ff4444', '#ff4444', '#ff4444',  # e8-e11 presup/anaph/embed/focus
    '#00ddff', '#00ddff', '#00ddff', '#00ddff',  # e12-e15 topic/quest/neg/meta
]

_OP_NAMES = [
    'scalar', 'pron',  'verb',  'noun',
    'adj',   'adv',   'rel',   'det',
    'presup','anaph', 'embed', 'focus',
    'topic', 'quest', 'neg',   'meta',
]

# ZD→great-circle traversal order (from original recovered SVG)
_ZD_ORDER = [11, 7, 3, 1, 0, 2, 6, 10, 8, 13, 15, 12, 9, 4, 5, 14]

_PTOLEMY_IMAGES = Path('~/.ptolemy/images').expanduser()
_WIKI_IMAGES    = Path('/home/rendier/Projects/Ptol/Ainulindale/wiki/images')


def _coupling(p: int, sigma: float) -> float:
    """p^{-σ}  — geometric coupling at prime p, exponent σ."""
    if sigma == 0.0:
        return 1.0
    return p ** (-sigma)


def _spoke_angle(k: int) -> float:
    """Angle for spoke k.  e0 at 12 o'clock, rotating clockwise."""
    return math.pi / 2.0 - 2.0 * math.pi * k / 16.0


def _sigma_label(sigma: float) -> str:
    if abs(sigma - _SIGMA_CRITICAL) < 0.04:
        return 'σ=½  QM / critical line / fixed point'
    if abs(sigma - _SIGMA_YANG_MILLS) < 0.04:
        return 'σ=1  Yang-Mills / Standard Model / pole'
    if abs(sigma - _SIGMA_GR) < 0.08:
        return 'σ=2  GR / mass / E=mc²'
    if sigma < _SIGMA_CRITICAL:
        return f'σ={sigma:.3f}  Fermat forbidden zone'
    return f'σ={sigma:.3f}'


def _xml_escape(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def generate(sigma: float, prompt: str, v: list,
             output_dir: str = None) -> str:
    """
    :param sigma:      coupling exponent — determines cavitation geometry
    :param prompt:     label shown at top of SVG
    :param v:          16 normalised amplitudes (signed; sum |v[k]| ≤ 1)
    :param output_dir: override output directory (default ~/.ptolemy/images/)
    :returns:          absolute path of written SVG file
    """
    if len(v) != 16:
        raise ValueError(f'v must have 16 elements, got {len(v)}')

    W, H   = 540, 580
    CX, CY = W / 2.0, (H / 2.0) + 10.0
    R      = 210.0
    thresh = 0.04   # active-spoke threshold

    lines = []
    E = lines.append   # emit shorthand

    # ── Header ────────────────────────────────────────────────────────────────
    E('<?xml version="1.0" encoding="UTF-8"?>')
    E(f'<svg xmlns="http://www.w3.org/2000/svg" '
      f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    E(f'  <rect width="{W}" height="{H}" fill="#0a0a0a"/>')

    # Prompt label (top)
    E(f'  <text x="{W//2}" y="18" font-family="monospace" font-size="11" '
      f'fill="#444444" text-anchor="middle">{_xml_escape(prompt)}</text>')

    # σ label (bottom)
    E(f'  <text x="{W//2}" y="{H - 8}" font-family="monospace" font-size="9" '
      f'fill="#556655" text-anchor="middle">{_sigma_label(sigma)}</text>')

    # ── Concentric reference circles ─────────────────────────────────────────
    for frac in (0.25, 0.5, 0.75, 1.0):
        E(f'  <circle cx="{CX:.1f}" cy="{CY:.1f}" r="{R * frac:.1f}" '
          f'fill="none" stroke="#1e1e1e" stroke-width="0.5"/>')

    # σ=½ dashed marker at R/2
    E(f'  <circle cx="{CX:.1f}" cy="{CY:.1f}" r="{R * 0.5:.1f}" '
      f'fill="none" stroke="#2a4a2a" stroke-width="1" stroke-dasharray="4,4"/>')
    E(f'  <text x="{CX + R * 0.5 + 4:.1f}" y="{CY:.1f}" '
      f'font-family="monospace" font-size="8" fill="#2a4a2a" '
      f'text-anchor="start">σ=½</text>')

    # ── Cavitation void ───────────────────────────────────────────────────────
    # Radius ∝ distance from fixed point σ=½
    void_r = abs(sigma - _SIGMA_CRITICAL) * R * 0.50
    if void_r > 2.5:
        # red above ½ (pole-direction, dissolving), blue below (forbidden)
        void_col = '#2a0a0a' if sigma > _SIGMA_CRITICAL else '#0a0a2a'
        void_stroke = '#6a1010' if sigma > _SIGMA_CRITICAL else '#10106a'
        E(f'  <circle cx="{CX:.1f}" cy="{CY:.1f}" r="{void_r:.1f}" '
          f'fill="{void_col}" stroke="{void_stroke}" stroke-width="0.8" '
          f'opacity="0.7"/>')

    # ── Per-spoke geometry ────────────────────────────────────────────────────
    tip_x  = []   # rim position (full R)
    tip_y  = []
    amp_x  = []   # amplitude position (v[k]·R from centre)
    amp_y  = []

    for k in range(16):
        a      = _spoke_angle(k)
        ca, sa = math.cos(a), math.sin(a)
        active = abs(v[k]) >= thresh

        # Rim coordinates
        tx = CX + ca * R
        ty = CY - sa * R
        tip_x.append(tx)
        tip_y.append(ty)

        # Amplitude-tip coordinates (σ-coupled radius)
        coup  = _coupling(_PRIMES[k], sigma)
        tip_r = abs(v[k]) * R * coup
        ax    = CX + ca * tip_r
        ay    = CY - sa * tip_r
        amp_x.append(ax)
        amp_y.append(ay)

        # Spoke line to rim
        sc = '#333333' if active else '#1a1a1a'
        sw = '0.8' if active else '0.4'
        E(f'  <line x1="{CX:.2f}" y1="{CY:.2f}" '
          f'x2="{tx:.2f}" y2="{ty:.2f}" '
          f'stroke="{sc}" stroke-width="{sw}"/>')

        # Prime label at spoke tip (beyond rim)
        lx = CX + ca * (R + 16)
        ly = CY - sa * (R + 16)
        lc = '#666666' if active else '#2a2a2a'
        E(f'  <text x="{lx:.1f}" y="{ly:.1f}" font-family="monospace" '
          f'font-size="9" fill="{lc}" text-anchor="middle" '
          f'dominant-baseline="central">p{_PRIMES[k]}</text>')

        # Amplitude dot
        if tip_r > 1.0:
            dot_col = '#c04040' if v[k] >= 0 else '#4060c0'
            dot_r   = 4.0 if active else 2.5
            E(f'  <circle cx="{ax:.2f}" cy="{ay:.2f}" r="{dot_r:.1f}" '
              f'fill="{dot_col}" opacity="0.9"/>')

        # ── Riemann zero text node ────────────────────────────────────────────
        # Only in the causal zone (σ ≥ ½ − ε).
        # Placed at radius proportional to γ_k, scaled by coupling.
        if sigma >= _SIGMA_CRITICAL - 0.04 and abs(v[k]) > 0.008:
            gamma      = _RIEMANN_ZEROS[k]
            gamma_norm = gamma / _RIEMANN_ZEROS[-1]   # 0..1
            r_zero     = gamma_norm * R * 0.80 * coup
            r_zero     = max(r_zero, 14.0)
            zx = CX + ca * r_zero
            zy = CY - sa * r_zero
            fs = max(5, min(9, int(5 + abs(v[k]) * 10)))
            zcol = '#c04040' if v[k] >= 0 else '#4060c0'
            E(f'  <text x="{zx:.1f}" y="{zy:.1f}" font-family="monospace" '
              f'font-size="{fs}" fill="{zcol}" opacity="0.70" '
              f'text-anchor="middle" dominant-baseline="central">'
              f'{gamma:.3f}</text>')

    # ── ZD Bézier curves (7 primary pairs: eₖ ↔ eₖ₊₈, k=1..7) ──────────────
    # Bézier curvature encodes the Fermat constraint:
    #   σ = ½  → control points on chord midpoint   (straight, coherent)
    #   σ > ½  → bow outward from centre             (dissolving toward pole)
    #   σ < ½  → bow toward centre                   (forbidden collapse)
    for k in range(1, 8):
        j      = k + 8
        x1, y1 = amp_x[k], amp_y[k]
        x2, y2 = amp_x[j], amp_y[j]

        # chord midpoint
        mx, my = (x1 + x2) * 0.5, (y1 + y2) * 0.5

        # perpendicular unit vector, pointing outward from centre
        dx, dy    = x2 - x1, y2 - y1
        chord_len = math.hypot(dx, dy) or 1.0
        px, py    = -dy / chord_len, dx / chord_len
        # ensure outward direction (away from CX,CY)
        if px * (mx - CX) + py * (my - CY) < 0:
            px, py = -px, -py

        # bow: positive = outward (σ > ½), negative = inward (σ < ½)
        bow  = (sigma - _SIGMA_CRITICAL) * chord_len * 0.35
        bx   = mx + px * bow
        by   = my + py * bow

        # cubic Bézier: both control points at same bow position
        cx1, cy1 = (x1 + bx) * 0.5, (y1 + by) * 0.5
        cx2, cy2 = (x2 + bx) * 0.5, (y2 + by) * 0.5

        col  = _SECTOR[k]
        op   = '0.20' if abs(v[k]) < thresh else '0.40'
        E(f'  <path d="M{x1:.1f},{y1:.1f} '
          f'C{cx1:.1f},{cy1:.1f} {cx2:.1f},{cy2:.1f} {x2:.1f},{y2:.1f}" '
          f'fill="none" stroke="{col}" stroke-width="0.9" opacity="{op}"/>')

    # ── Mind's Eye caustic: green causal geodesic ─────────────────────────────
    # Connects amplitude tips in ZD→great-circle order (point by point).
    # This is Thread 2: the focused envelope of Thread 1's scattered output.
    pts = ' '.join(f'{amp_x[i]:.2f},{amp_y[i]:.2f}' for i in _ZD_ORDER)
    E(f'  <polyline fill="none" stroke="#40a060" stroke-width="1.4" '
      f'opacity="0.88" '
      f'points="{amp_x[0]:.2f},{amp_y[0]:.2f} {pts}"/>')

    # ── ZD origin ─────────────────────────────────────────────────────────────
    E(f'  <circle cx="{CX:.1f}" cy="{CY:.1f}" r="3.5" '
      f'fill="#806020" opacity="0.9"/>')
    E(f'  <text x="{CX:.1f}" y="{CY + 13:.1f}" font-family="monospace" '
      f'font-size="8" fill="#806020" text-anchor="middle">ZD</text>')

    # eₖ labels in inner ring
    for k in range(16):
        a  = _spoke_angle(k)
        ex = CX + math.cos(a) * 20.0
        ey = CY - math.sin(a) * 20.0
        E(f'  <text x="{ex:.1f}" y="{ey:.1f}" font-family="monospace" '
          f'font-size="6" fill="#555555" text-anchor="middle" '
          f'dominant-baseline="central">e{k}</text>')

    E('</svg>')

    svg_text = '\n'.join(lines)

    # ── Persist to ~/.ptolemy/images/ ─────────────────────────────────────────
    out_dir = Path(output_dir) if output_dir else _PTOLEMY_IMAGES
    out_dir.mkdir(parents=True, exist_ok=True)
    ts    = int(time.time())
    fname = f'sedenion_cavitation_s{int(sigma * 100):03d}_{ts}.svg'
    dest  = out_dir / fname
    dest.write_text(svg_text, encoding='utf-8')

    # ── Mirror to Ainulindale wiki/images/ ────────────────────────────────────
    if _WIKI_IMAGES.exists():
        shutil.copy2(dest, _WIKI_IMAGES / fname)

    return str(dest)
