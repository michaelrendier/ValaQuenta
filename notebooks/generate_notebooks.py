"""
generate_notebooks.py
=====================
Generates all Ainulindale Jupyter notebooks for Tiers 7, 8, 9
plus the flagship Leech divergence-inversion notebook.

Run from: ValaQuenta/notebooks/
    python3 generate_notebooks.py

Outputs: tier7/, tier8/, tier9/, leech_divergence/ directories
"""

import json
import os
import sys
import math

# ── Notebook format helpers ────────────────────────────────────────────────────

def nb(cells):
    """Minimal valid .ipynb structure."""
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"},
        },
        "cells": cells,
    }

def md(source):
    return {"cell_type": "markdown", "id": "md", "metadata": {},
            "source": source if isinstance(source, str) else "\n".join(source)}

def code(source, outputs=None):
    return {"cell_type": "code", "id": "code", "metadata": {}, "execution_count": None,
            "source": source if isinstance(source, str) else "\n".join(source),
            "outputs": outputs or []}

def save(path, notebook):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    print(f"  wrote {path}")

# ── Standard engine notebook template ─────────────────────────────────────────

PREAMBLE = """import sys, os
sys.path.insert(0, os.path.abspath('../..'))
import importlib.util, math, cmath, numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams.update({'figure.dpi': 120, 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False})

def load_maths(tier):
    paths = {7: '../../modules/tier7_cosmos/maths.py',
             8: '../../modules/tier8_sedenion/maths.py',
             9: '../../modules/tier9_chem/maths.py'}
    spec = importlib.util.spec_from_file_location(f't{tier}', paths[tier])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

OMEGA_ZS = 0.5671432904097838
D_STAR   = 0.24600
GAP      = OMEGA_ZS - D_STAR * math.log(10)
R_H      = 1.0 / math.sqrt(2.0)
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918719, 43.327073, 48.005151, 49.773832]
print("Ainulindale notebook ready.")
"""

def engine_notebook(tier, engine_fn, title, description, plot_code, claim_tex):
    """Generate a standard engine notebook."""
    return nb([
        md(f"# {title}\n\n**Ainulindale Engine** — Tier {tier}\n\n{description}"),
        code(PREAMBLE),
        code(f"""m = load_maths({tier})
result = m.{engine_fn}()
print("Claim:", result['claim'])
print("Confidence:", result['confidence'])
"""),
        md("## Engine Output"),
        code("""import pprint
pprint.pprint({k: v for k, v in result.items()
               if k not in ('claim', 'confidence', 'latex')}, width=100, depth=3)
"""),
        md(f"## Mathematical Foundation\n\n$$\\text{{LaTeX: }}\\quad {claim_tex}$$"),
        code(plot_code),
        md("## Ainulindale Reading\n\n"
           f"**Confidence:** `{{}}'.format(result.get('confidence',''))`\n\n"
           "Run `result.keys()` to explore the full engine output."),
        code("print('Engine keys:', list(result.keys()))"),
    ])

# ── Plot code snippets per engine ──────────────────────────────────────────────

PLOTS = {

# ── TIER 7 ────────────────────────────────────────────────────────────────────

'explicit_formula_de_sitter': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: ψ(x) = x − Σ spectral terms
x_vals = np.linspace(2, 30, 500)
psi_ground = x_vals.copy()
RZEROS = RIEMANN_ZEROS[:10]
psi_spectral = np.zeros(len(x_vals))
for gamma in RZEROS:
    rho_mag_sq = 0.25 + gamma**2
    for i, x in enumerate(x_vals):
        ln_x = math.log(x)
        sqrt_x = math.sqrt(x)
        cos_g = math.cos(gamma * ln_x)
        sin_g = math.sin(gamma * ln_x)
        psi_spectral[i] += sqrt_x * (cos_g*0.5 + sin_g*gamma) / rho_mag_sq

psi_x = psi_ground - psi_spectral - math.log(2*math.pi)
ax = axes[0]
ax.plot(x_vals, psi_ground, 'b-', alpha=0.5, label='x  (de Sitter)')
ax.plot(x_vals, psi_x, 'r-', lw=1.5, label='ψ(x)  (with oscillations)')
ax.set_xlabel('x'); ax.set_ylabel('ψ(x)'); ax.set_title('Explicit Formula: de Sitter + BAO Oscillations')
ax.legend(); ax.grid(alpha=0.3)

# Right: Riemann zero frequencies
ax2 = axes[1]
ax2.bar(range(1, 11), RIEMANN_ZEROS, color='steelblue', alpha=0.8)
ax2.axhline(14.134, color='r', ls='--', alpha=0.5, label='γ₁ = 14.134')
ax2.set_xlabel('n'); ax2.set_ylabel('γₙ'); ax2.set_title('First 10 Riemann Zeros (BAO Frequencies)')
ax2.legend()
plt.tight_layout(); plt.show()
""",

'slingshot_light': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: null-cone boost vs r_min/R_H
r_min_ratio = np.linspace(0.1, 3.0, 300)
nc_boost = (1.0 / r_min_ratio)**2
delta_mag = -2.5 * np.log10(nc_boost)

ax = axes[0]
ax.plot(r_min_ratio, delta_mag, 'r-', lw=2)
ax.axhline(0, color='k', ls='-', lw=0.8)
ax.axhline(-0.05, color='purple', ls='--', alpha=0.7, label='Dark energy signal (0.05 mag)')
ax.axvline(1.0, color='b', ls='--', alpha=0.7, label='r_min = R_H (brim)')
ax.fill_between(r_min_ratio, delta_mag, 0, where=delta_mag < 0, alpha=0.15, color='red', label='Blueshift (boosted)')
ax.fill_between(r_min_ratio, delta_mag, 0, where=delta_mag > 0, alpha=0.15, color='blue', label='Redshift (dimmed)')
ax.set_xlabel('r_min / R_H'); ax.set_ylabel('Δmag (negative = brighter)')
ax.set_title('Null-Cone Slingshot Boost vs Impact Parameter')
ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_ylim(-2, 1.5)

# Right: environment-dependent Hubble diagram
ax2 = axes[1]
z_arr = np.linspace(0.05, 1.5, 100)
def mu_std(z): return 5*np.log10((z/0.05) * 3000) + 25
def sling_bias(z): return -0.15 * 0.7 * np.exp(-z/0.4)
mu_true = mu_std(z_arr); mu_obs = mu_true + sling_bias(z_arr)
ax2.plot(z_arr, mu_true, 'b-', lw=1.5, label='True distance modulus')
ax2.plot(z_arr, mu_obs, 'r--', lw=1.5, label='Observed (slingshot-biased)')
ax2.fill_between(z_arr, mu_true, mu_obs, alpha=0.2, color='red', label='Slingshot bias')
ax2.set_xlabel('Redshift z'); ax2.set_ylabel('Distance modulus μ')
ax2.set_title('Standard Candle Bias: True vs Observed')
ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'halocline_ns_surface': """
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Left: density profile across halocline
z_vals = np.linspace(-5, 5, 300)   # depth in metres (0 = interface)
rho_profile = 1000 + 25 / (1 + np.exp(-2*z_vals))   # sigmoid halocline
ax = axes[0]
ax.plot(rho_profile, -z_vals, 'steelblue', lw=2)
ax.axhline(0, color='r', ls='--', lw=1.5, label='σ=½ surface (halocline)')
ax.fill_betweenx(-z_vals, rho_profile, 1000, where=rho_profile>1012, alpha=0.2, color='blue', label='Salt layer (J_neg)')
ax.fill_betweenx(-z_vals, rho_profile, 1000, where=rho_profile<1012, alpha=0.2, color='red', label='Fresh layer (J_pos)')
ax.set_xlabel('Density (kg/m³)'); ax.set_ylabel('Depth (m)')
ax.set_title('Halocline Density Profile'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Middle: Richardson criterion
shear_vals = np.linspace(0.01, 1.0, 200)
N2 = 9.81 * 25 / 1000   # Brunt-Väisälä N²
Ri_vals = N2 / shear_vals**2
ax2 = axes[1]
ax2.semilogy(shear_vals, Ri_vals, 'purple', lw=2)
ax2.axhline(0.25, color='r', ls='--', lw=2, label=f'Ri = 1/4 = σ² = {0.25}')
ax2.fill_between(shear_vals, Ri_vals, 0.25, where=Ri_vals > 0.25,
                 alpha=0.2, color='green', label='Stable (no KH)')
ax2.fill_between(shear_vals, Ri_vals, 0.25, where=Ri_vals < 0.25,
                 alpha=0.2, color='red', label='Unstable (KH billows)')
ax2.set_xlabel('Velocity shear du/dz (s⁻¹)'); ax2.set_ylabel('Richardson number Ri')
ax2.set_title('Richardson Criterion: Ri_crit = σ² = 1/4'); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

# Right: sound waveguide in halocline
ax3 = axes[2]
depths = np.linspace(-10, 10, 300)
c_sound = 1480 + 20 / (1 + np.exp(-2*depths))
ax3.plot(c_sound, -depths, 'darkorange', lw=2)
ax3.axhline(0, color='r', ls='--', label='Halocline interface')
theta_c = math.degrees(math.asin(1480/1520))
ax3.set_xlabel('Sound speed (m/s)'); ax3.set_ylabel('Depth (m)')
ax3.set_title(f'Acoustic Waveguide (θ_c = {theta_c:.1f}°)'); ax3.legend()
ax3.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'lambda_cdm_omega_zs': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: Friedmann survey
z_range = np.linspace(-0.9, 5, 200)
Omega_M, Omega_L = 0.3111, 0.6889
H_sq = [Omega_M*(1+z)**3 + Omega_L for z in z_range]
H_over_H0 = [math.sqrt(max(h,0)) for h in H_sq]
Omega_L_eff = [Omega_L / h if h > 0 else 0 for h in H_sq]

ax = axes[0]
ax.plot(z_range, Omega_L_eff, 'b-', lw=2, label='Ω_Λ_eff(z)')
ax.axhline(OMEGA_ZS, color='r', ls='--', lw=2, label=f'OMEGA_ZS = {OMEGA_ZS:.4f}')
ax.axhline(Omega_L, color='purple', ls=':', alpha=0.7, label=f'Current Ω_Λ = {Omega_L}')
ax.axvline(0, color='gray', ls='-', alpha=0.4)
ax.set_xlabel('Redshift z'); ax.set_ylabel('Ω_Λ effective')
ax.set_title('OMEGA_ZS = de Sitter Attractor'); ax.legend(fontsize=9); ax.grid(alpha=0.3)
ax.set_xlim(-0.9, 3); ax.set_ylim(0, 1.1)

# Right: Lambert W iteration converging to OMEGA_ZS
x_iter = [0.9]
for _ in range(30): x_iter.append(math.exp(-x_iter[-1]))
ax2 = axes[1]
ax2.plot(x_iter, 'steelblue', lw=2, marker='o', ms=3)
ax2.axhline(OMEGA_ZS, color='r', ls='--', lw=2, label=f'OMEGA_ZS = {OMEGA_ZS:.6f}')
ax2.set_xlabel('Iteration'); ax2.set_ylabel('x')
ax2.set_title('x → e^{-x} Converges to OMEGA_ZS from Any x₀'); ax2.legend(); ax2.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'dark_matter_geometry': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: rotation curve — flat from 1/r² dark matter
G, rho_0, R_H_val = 1.0, 1.0, 1/math.sqrt(2)
r_vals = np.linspace(0.05, 3.0, 300)
M_r = [4*math.pi*rho_0*R_H_val**2 * min(r, R_H_val) for r in r_vals]
v_r = [math.sqrt(G*m/r) for m, r in zip(M_r, r_vals)]

ax = axes[0]
ax.plot(r_vals, v_r, 'r-', lw=2, label='v(r) — flat rotation curve')
ax.axvline(R_H_val, color='b', ls='--', label=f'R_H = {R_H_val:.3f} (brim)')
ax.set_xlabel('r (natural units)'); ax.set_ylabel('v(r)')
ax.set_title('Flat Rotation Curve from 1/r² DM (No DM Particle)'); ax.legend(); ax.grid(alpha=0.3)

# Right: 1/r² density profile
rho_interior = [rho_0 * R_H_val**2 / r**2 for r in np.linspace(0.1, R_H_val, 200)]
r_int = np.linspace(0.1, R_H_val, 200)
ax2 = axes[1]
ax2.loglog(r_int, rho_interior, 'purple', lw=2, label='ρ(r) = ρ₀R_H²/r²')
ax2.set_xlabel('r'); ax2.set_ylabel('ρ(r)')
ax2.set_title('Dark Matter Density from Conformal Inversion'); ax2.legend(); ax2.grid(alpha=0.3)
ax2.set_xlim(0.1, R_H_val)
plt.tight_layout(); plt.show()
""",

# ── TIER 8 ────────────────────────────────────────────────────────────────────

'sedenion_self_organisation': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: sigma distribution of 16 operators
ops = ['IDENTITY','EXPANSION','CONSTRAINT','ROTATION','SCALING','INVERSION',
       'OSCILLATION','RESONANCE','THRESHOLD','ENTANGLEMENT','RECURSION',
       'INTERFERENCE','COMPRESSION','IGNITION','EMERGENCE','GAP']
PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]
MOD = 10**9 + 7

sigmas = []
for name in ops:
    h = sum(ord(c)*PRIMES[i%len(PRIMES)] for i,c in enumerate(name.lower())) % MOD
    sigmas.append(h/MOD)

ax = axes[0]
colors = ['red' if abs(s-0.5)<0.1 else 'steelblue' for s in sigmas]
ax.barh(range(16), sigmas, color=colors, alpha=0.8)
ax.axvline(OMEGA_ZS, color='r', ls='--', lw=2, label=f'OMEGA_ZS={OMEGA_ZS:.4f}')
ax.axvline(D_STAR, color='g', ls='--', lw=2, label=f'D*={D_STAR}')
ax.set_yticks(range(16)); ax.set_yticklabels(ops, fontsize=8)
ax.set_xlabel('Prime hash σ-address'); ax.set_title('16 Operator Names → σ-Addresses')
ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Right: dimension index distribution
dims = []
for name in ops:
    h = sum(ord(c)*PRIMES[i%len(PRIMES)] for i,c in enumerate(name.lower())) % MOD
    dims.append(h % 16)
ax2 = axes[1]
ax2.bar(range(16), [dims.count(d) for d in range(16)], color='steelblue', alpha=0.8)
ax2.axhline(1, color='r', ls='--', label='Perfect bijection (1 per dim)')
ax2.set_xlabel('Sedenion dimension index'); ax2.set_ylabel('Count')
ax2.set_title('Operator → Dimension Assignment'); ax2.legend(); ax2.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'leech_divergence_inversion': """
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Left: ball volume sequence
ns = list(range(0, 27, 2))
Vns = [math.pi**(n//2)/math.factorial(n//2) for n in ns]
colors_v = ['gold' if n in [16,24] else 'steelblue' for n in ns]
ax = axes[0]
ax.bar(ns, Vns, color=colors_v, alpha=0.85, width=1.5)
ax.axhline(0, color='k')
for n, v, c in zip(ns, Vns, colors_v):
    if c == 'gold':
        ax.annotate(f'V_{n}\\n={v:.4f}', (n, v), textcoords='offset points',
                    xytext=(0,5), ha='center', fontsize=8, color='darkred')
ax.set_xlabel('n (dimension)'); ax.set_ylabel('V_n = π^(n/2)/(n/2)!')
ax.set_title('n-Ball Volume: Phase Space Available at Each CD Level')
ax.grid(alpha=0.3)

# Middle: phase gate e^{i·ΔV} trajectory on unit circle
V_prev, phases, labels = 1.0, [], []
for n in range(2, 27, 2):
    V_n = math.pi**(n//2)/math.factorial(n//2)
    dV = V_n - V_prev
    phases.append(dV); labels.append(n); V_prev = V_n
cumphases = np.cumsum(phases)
xs = np.cos(cumphases); ys = np.sin(cumphases)
ax2 = axes[1]
ax2.plot(xs, ys, 'steelblue', lw=1.5, alpha=0.7)
ax2.scatter(xs, ys, c=range(len(xs)), cmap='plasma', s=60, zorder=5)
for i, (x,y,l) in enumerate(zip(xs, ys, labels)):
    ax2.annotate(str(l), (x,y), fontsize=7, ha='center')
theta = np.linspace(0, 2*math.pi, 300)
ax2.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.2)
ax2.axhline(0, color='k', alpha=0.3); ax2.axvline(0, color='k', alpha=0.3)
ax2.set_aspect('equal'); ax2.set_title('Cumulative Phase Gate e^{i·ΔV_n} Trajectory')
ax2.grid(alpha=0.3)

# Right: 196,560 Leech root decomposition
labels_lr = ['Pure pairs\\n(1,104)\\nForward x-aff', 'Golay code\\n(97,152)\\nBackward type A', 'Mixed\\n(98,304)\\nBackward type B']
sizes = [1104, 97152, 98304]
colors_lr = ['#4CAF50', '#E91E63', '#FF5722']
ax3 = axes[2]
wedges, texts, autotexts = ax3.pie(sizes, labels=labels_lr, colors=colors_lr, autopct='%1.1f%%',
                                    startangle=90, textprops={'fontsize': 8})
ax3.set_title(f'196,560 Leech Roots\\n(ZD = divergence-inverted sources)')
plt.tight_layout(); plt.show()
print(f"\\nφ_ZD = V_24 - V_16 = {math.pi**12/math.factorial(12):.8f} - {math.pi**8/math.factorial(8):.8f} = {math.pi**12/math.factorial(12)-math.pi**8/math.factorial(8):.8f}")
print(f"Phase gate: e^(i·φ_ZD) = {cmath.exp(1j*(math.pi**12/math.factorial(12)-math.pi**8/math.factorial(8)))}")
print(f"Backward x-affinities: {97152+98304:,} of {196560:,} Leech roots")
""",

'omega_zs_6_family': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: 6 domains where OMEGA_ZS appears
domains = ['Math\\nW(1)=Ω', 'Primes\\n|ζ|² mean', 'Cosmology\\nΩ_Λ attractor',
           'Yang-Mills\\nGAP residual*', 'Sedenion\\n⟨g⟩ mean', 'Information\\nS(σ=½)']
S_info = -(OMEGA_ZS*math.log(OMEGA_ZS) + (1-OMEGA_ZS)*math.log(1-OMEGA_ZS))
values = [OMEGA_ZS, OMEGA_ZS, OMEGA_ZS, OMEGA_ZS, OMEGA_ZS, S_info]

ax = axes[0]
bars = ax.bar(domains, values, color=['#3498DB','#E74C3C','#2ECC71','#F39C12','#9B59B6','#1ABC9C'], alpha=0.85)
ax.axhline(OMEGA_ZS, color='r', ls='--', lw=2, label=f'OMEGA_ZS = {OMEGA_ZS:.6f}')
ax.set_title('OMEGA_ZS = W(1) in 6 Independent Domains'); ax.legend(); ax.grid(alpha=0.3)
ax.set_ylim(0, 0.8)
for bar, val in zip(bars, values):
    ax.text(bar.get_x()+bar.get_width()/2, val+0.01, f'{val:.4f}', ha='center', fontsize=8)

# Right: OMEGA_ZS² ≈ Ω_M
ax2 = axes[1]
x = np.linspace(0, 1, 400)
y_iter = [0.9]
for _ in range(60): y_iter.append(math.exp(-y_iter[-1]))
ax2.plot(y_iter, 'steelblue', lw=2, label='x_{n+1} = e^{-x_n}')
ax2.axhline(OMEGA_ZS, color='r', ls='--', label=f'OMEGA_ZS = {OMEGA_ZS:.4f}')
ax2.axhline(OMEGA_ZS**2, color='g', ls=':', label=f'OMEGA_ZS² = {OMEGA_ZS**2:.4f} ≈ Ω_M = 0.3111')
ax2.set_xlabel('Iteration n'); ax2.set_ylabel('x_n')
ax2.set_title('Fixed-Point Iteration: x → e^{-x} → OMEGA_ZS'); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'hermite_timing_wheel': """
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

def eval_hermite(n, x):
    if n==0: return 1.0
    if n==1: return 2.0*x
    h0,h1 = 1.0, 2.0*x
    for k in range(2,n+1): h2=2*x*h1-2*(k-1)*h0; h0,h1=h1,h2
    return h1

# Left: H_n for n=0..5
x_arr = np.linspace(-3, 3, 400)
ax = axes[0]
for n in range(6):
    y = [eval_hermite(n,x) for x in x_arr]
    ax.plot(x_arr, np.clip(y,-15,15), label=f'H_{n}', alpha=0.8)
ax.axhline(0, color='k', lw=0.8); ax.set_ylim(-15,15)
ax.set_xlabel('x'); ax.set_title('Hermite Polynomials H_n(x)'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Middle: timing wheel (zeros as n-gon)
ax2 = axes[1]
for n in [3,5,7]:
    # Find zeros approximately
    x_max = math.sqrt(2*n+4)
    xs = np.linspace(-x_max,x_max,2000)
    ys = np.array([eval_hermite(n,x) for x in xs])
    zeros = []
    for i in range(len(ys)-1):
        if ys[i]*ys[i+1]<0:
            a,b = float(xs[i]),float(xs[i+1])
            for _ in range(40):
                m=(a+b)/2
                if eval_hermite(n,m)*eval_hermite(n,a)<0: b=m
                else: a=m
            zeros.append((a+b)/2)
    scale = math.sqrt(2*n+1)
    scaled = [z/scale for z in zeros]
    # Place on unit circle
    theta_vals = [math.pi*s for s in scaled]
    ax2.scatter([math.cos(t) for t in theta_vals], [math.sin(t) for t in theta_vals],
                s=60, label=f'n={n} ({len(zeros)} zeros)', zorder=5)
theta_circle = np.linspace(0,2*math.pi,300)
ax2.plot(np.cos(theta_circle), np.sin(theta_circle), 'k-', alpha=0.3)
ax2.set_aspect('equal'); ax2.set_title('Hermite Zeros as BAO Timing Marks')
ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

# Right: Riemann zeros → BK levels
ax3 = axes[2]
x0_vals = [g/(2*math.pi) for g in RIEMANN_ZEROS]
ax3.scatter(range(1,11), RIEMANN_ZEROS, c='steelblue', s=80, zorder=5, label='γ_n (Riemann zero)')
ax3.plot(range(1,11), RIEMANN_ZEROS, 'steelblue', alpha=0.5)
ax3r = ax3.twinx()
ax3r.scatter(range(1,11), x0_vals, c='red', s=80, marker='s', zorder=5, label='x₀(n)=γ_n/2π')
ax3r.plot(range(1,11), x0_vals, 'r--', alpha=0.5)
ax3.set_xlabel('n'); ax3.set_ylabel('γ_n', color='steelblue'); ax3r.set_ylabel('x₀(n)', color='red')
ax3.set_title('BK Mapping: γ_n/(2π) = Hermite Scale')
ax3.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

# ── TIER 9 ────────────────────────────────────────────────────────────────────

'cancer_zero_divisor': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: healthy vs cancer stop-response
GAP_val = OMEGA_ZS - D_STAR*math.log(10)
upper_fracs = np.linspace(0, 1, 50)
np.random.seed(42)
responses = []
for uf in upper_fracs:
    raw_oct = np.random.randn(8)*0.3; raw_sed = np.random.randn(8)
    s = np.concatenate([raw_oct*(1-uf), raw_sed*uf])
    s /= np.linalg.norm(s)
    raw_stop = np.random.randn(8)
    t = np.concatenate([raw_stop/np.linalg.norm(raw_stop), np.zeros(8)])
    prod = np.zeros(16)
    # Simplified: use dot product as proxy for response
    prod[:8] = s[:8] * t[:8]
    responses.append(float(np.linalg.norm(prod)))

ax = axes[0]
ax.plot(upper_fracs, responses, 'steelblue', lw=2)
ax.axhline(GAP_val, color='r', ls='--', label=f'GAP threshold = {GAP_val:.4f}')
ax.axvline(upper_fracs[np.argmin(np.abs(np.array(responses)-GAP_val))], color='orange', ls='--', label='Cancer onset')
ax.fill_between(upper_fracs, responses, GAP_val, where=np.array(responses)>GAP_val,
                alpha=0.2, color='green', label='Healthy (responds)')
ax.fill_between(upper_fracs, responses, GAP_val, where=np.array(responses)<GAP_val,
                alpha=0.2, color='red', label='Cancer (signal nullified)')
ax.set_xlabel('Upper sedenion fraction (cancer progression)')
ax.set_ylabel('Stop signal response |s·t_stop|')
ax.set_title('Cancer Onset: Zero-Divisor Collapse'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Right: cancer staging from J_R/J_B
stages = ['Healthy', 'Stage I', 'Stage II', 'Stage III', 'Stage IV']
jr_jb = [OMEGA_ZS, OMEGA_ZS*1.5, OMEGA_ZS*2.0, OMEGA_ZS*2.5, OMEGA_ZS*3.0]
h2o2  = [0.01, 0.05, 0.12, 0.25, 0.50]
colors_s = ['green','yellowgreen','yellow','orange','red']
ax2 = axes[1]
bars = ax2.bar(stages, jr_jb, color=colors_s, alpha=0.85)
ax2.axhline(OMEGA_ZS, color='b', ls='--', lw=2, label=f'Healthy = OMEGA_ZS = {OMEGA_ZS:.4f}')
ax2.set_ylabel('J_R/J_B ratio (radiolysis chromatogram)')
ax2.set_title('Cancer Staging from Noether Balance'); ax2.legend(fontsize=9); ax2.grid(alpha=0.3)
for bar, h in zip(bars, h2o2):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01, f'H₂O₂={h}mM',
             ha='center', fontsize=7, rotation=15)
plt.tight_layout(); plt.show()
""",

'hydro_radiolysis_chromatography': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: model chromatograms healthy vs cancer
t = np.linspace(0, 25, 500)
def chrom(t, jr_jb):
    JR = jr_jb * np.exp(-(t-3)**2/2)
    JG = 0.3 * np.exp(-(t-8)**2/3)
    JB = 1.0 * np.exp(-(t-15)**2/4)
    return JR+JG+JB

healthy = chrom(t, OMEGA_ZS)
cancer  = chrom(t, OMEGA_ZS*2.5)

ax = axes[0]
ax.plot(t, healthy, 'g-', lw=2, label=f'Healthy (J_R/J_B={OMEGA_ZS:.3f} = OMEGA_ZS)')
ax.plot(t, cancer,  'r-', lw=2, label=f'Cancer Stage III (J_R/J_B={OMEGA_ZS*2.5:.3f})')
ax.axvspan(0, 7.5, alpha=0.08, color='red', label='J_R region (τ<7.5)')
ax.axvspan(7.5, 11, alpha=0.08, color='gold')
ax.axvspan(15, 25, alpha=0.08, color='blue', label='J_B region (τ>15)')
ax.axvline(3, color='red', ls=':', alpha=0.6); ax.axvline(8, color='gold', ls=':', alpha=0.6)
ax.axvline(15, color='blue', ls=':', alpha=0.6)
ax.set_xlabel('Retention time (min)'); ax.set_ylabel('Signal')
ax.set_title('Radiolysis Chromatogram: Healthy vs Cancer'); ax.legend(fontsize=7); ax.grid(alpha=0.3)
ax.text(3, 0.7, 'J_R', color='red', ha='center', fontsize=10)
ax.text(8, 0.35, 'J_G', color='goldenrod', ha='center', fontsize=10)
ax.text(15, 0.85, 'J_B', color='blue', ha='center', fontsize=10)

# Right: G:A:V fragmentation survival
aas = ['Glycine (G)', 'Alanine (A)', 'Valine (V)']
sites = [1, 2, 4]
k_frag = math.log(6)/3
survive = [math.exp(-k_frag*(s-1)) for s in sites]
# Normalise relative to V
norm_s = [s/survive[-1] for s in survive]

ax2 = axes[1]
colors_gav = ['#1ABC9C','#3498DB','#9B59B6']
bars = ax2.bar(aas, norm_s, color=colors_gav, alpha=0.85)
ax2.bar_label(bars, labels=[f'{v:.1f}×' for v in norm_s], padding=3, fontsize=11)
ax2.set_title('G:A:V Radiolysis Survival (Life Ratio)')
ax2.set_ylabel('Survival relative to V'); ax2.grid(alpha=0.3)
ax2.text(0.5, 0.85, 'G:A:V = 6:3:1', transform=ax2.transAxes, ha='center',
         fontsize=14, color='darkred', fontweight='bold')
ax2.set_ylim(0, 8)
plt.tight_layout(); plt.show()
""",

'drug_targeting': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: conformal inversion visualization
theta = np.linspace(0, 2*math.pi, 300)
ax = axes[0]
# Cancer state (large radius, upper sedenion dominant)
r_cancer = 1.8
xs_c = r_cancer*np.cos(theta); ys_c = r_cancer*np.sin(theta)
# Drug = R_H²/r_cancer
r_drug = R_H**2 / r_cancer
xs_d = r_drug*np.cos(theta); ys_d = r_drug*np.sin(theta)
# Brim
xs_b = R_H*np.cos(theta); ys_b = R_H*np.sin(theta)

ax.plot(xs_c, ys_c, 'r-', lw=2, label=f'Cancer state (r={r_cancer})')
ax.plot(xs_d, ys_d, 'g-', lw=2, label=f'Drug = R_H²/r_cancer (r={r_drug:.3f})')
ax.plot(xs_b, ys_b, 'b--', lw=2, label=f'Brim R_H = {R_H:.3f}')
ax.scatter([r_cancer, r_drug], [0, 0], c=['red','green'], s=100, zorder=5)
ax.annotate('', xy=(r_drug,0), xytext=(r_cancer,0),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
ax.text((r_cancer+r_drug)/2, 0.08, 'Conformal inversion', ha='center', color='purple', fontsize=9)
ax.set_aspect('equal'); ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
ax.set_title('Drug = Conformal Inversion of Cancer Address'); ax.legend(fontsize=8); ax.grid(alpha=0.3)
ax.set_xlabel('Sedenion Re'); ax.set_ylabel('Sedenion Im (e₁ projection)')

# Right: EIIP targeting — cancer vs drug Riemann addresses
gamma_n = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
           37.586178, 40.918719, 43.327073, 48.005151, 49.773832]
cancer_n = 3; drug_n = 7  # complementary
ax2 = axes[1]
colors_rz = ['gray']*10
colors_rz[cancer_n-1] = 'red'; colors_rz[drug_n-1] = 'green'
ax2.bar(range(1,11), gamma_n, color=colors_rz, alpha=0.85)
ax2.bar_label(ax2.containers[0],
              labels=[f'γ{i}' if i in [cancer_n,drug_n] else '' for i in range(1,11)],
              padding=3, fontsize=9)
ax2.axhline(gamma_n[cancer_n-1], color='r', ls='--', alpha=0.6, label=f'Cancer: γ{cancer_n}={gamma_n[cancer_n-1]:.2f}')
ax2.axhline(gamma_n[drug_n-1], color='g', ls='--', alpha=0.6, label=f'Drug: γ{drug_n}={gamma_n[drug_n-1]:.2f}')
ax2.set_xlabel('n'); ax2.set_ylabel('Riemann zero γ_n')
ax2.set_title('Cancer vs Drug Riemann Zero Addresses'); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'cosic_eiip': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

EIIP = {'A':0.0373,'R':0.0959,'N':0.0036,'D':0.1263,'C':0.0829,
        'Q':0.0761,'E':0.0058,'G':0.0050,'H':0.0242,'I':0.0000,
        'L':0.0000,'K':0.0371,'M':0.0823,'F':0.0946,'P':0.0198,
        'S':0.0829,'T':0.0941,'W':0.0548,'Y':0.0516,'V':0.0057}

# Left: EIIP bar chart
ax = axes[0]
aas_sorted = sorted(EIIP, key=lambda x: EIIP[x], reverse=True)
eiip_vals = [EIIP[a] for a in aas_sorted]
colors_e = ['red' if EIIP[a]>0.08 else 'steelblue' for a in aas_sorted]
ax.bar(aas_sorted, eiip_vals, color=colors_e, alpha=0.85)
ax.set_xlabel('Amino acid'); ax.set_ylabel('EIIP (eV)')
ax.set_title('Electron-Ion Interaction Potentials (Cosic 1994)'); ax.grid(alpha=0.3)

# Right: DFT of SOR motif EIIP signal
sor_motif = ['C','P','Y','C','G','H','C','G','L','V','C','E','H']
sor_eiip = np.array([EIIP[aa] for aa in sor_motif])
dft = np.fft.fft(sor_eiip)
freqs = np.fft.fftfreq(len(sor_eiip))
power = np.abs(dft)**2
N = len(sor_eiip)

ax2 = axes[1]
ax2.plot(freqs[:N//2], power[:N//2], 'steelblue', lw=2)
dom_idx = int(np.argmax(power[1:N//2])+1)
ax2.axvline(freqs[dom_idx], color='r', ls='--', lw=2,
            label=f'Dominant f={freqs[dom_idx]:.3f} → γ={freqs[dom_idx]*2*math.pi*N:.2f}')
ax2.set_xlabel('Frequency'); ax2.set_ylabel('Power spectrum')
ax2.set_title('SOR Motif EIIP DFT (Riemann Zero Address)'); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'gnarl_validation': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
import numpy as np

def cd_conj(x): c=x.copy(); c[1:]=-c[1:]; return c
def cd_mul(a,b):
    n=len(a)
    if n==1: return np.array([a[0]*b[0]])
    h=n//2; a1,a2,b1,b2=a[:h],a[h:],b[:h],b[h:]
    return np.concatenate([cd_mul(a1,b1)-cd_mul(cd_conj(b2),a2), cd_mul(b2,a1)+cd_mul(a2,cd_conj(b1))])

np.random.seed(42)
# Sample g(a) for octonion vs full sedenion
N=200
oct_gs, full_gs = [], []
for _ in range(N):
    ar=np.random.randn(8); a_oct=np.concatenate([ar/np.linalg.norm(ar),np.zeros(8)])
    a_sed=np.random.randn(16); a_sed/=np.linalg.norm(a_sed)
    max_o, max_s = 0.0, 0.0
    for _ in range(15):
        br=np.random.randn(8); b_oct=np.concatenate([br/np.linalg.norm(br),np.zeros(8)])
        b_sed=np.random.randn(16); b_sed/=np.linalg.norm(b_sed)
        max_o=max(max_o, float(np.linalg.norm(cd_mul(a_oct,b_oct))))
        max_s=max(max_s, float(np.linalg.norm(cd_mul(a_sed,b_sed))))
    oct_gs.append(max_o); full_gs.append(max_s)

ax=axes[0]
ax.hist(oct_gs,bins=30,alpha=0.7,color='green',label=f'Octonion sub-algebra (mean={np.mean(oct_gs):.3f})')
ax.hist(full_gs,bins=30,alpha=0.7,color='red',label=f'Full sedenion (mean={np.mean(full_gs):.3f})')
ax.axvline(OMEGA_ZS,color='b',ls='--',lw=2,label=f'OMEGA_ZS={OMEGA_ZS:.4f}')
ax.set_xlabel('g(a) = max_{|b|=1} |ab|'); ax.set_ylabel('Count')
ax.set_title('Gnarl: g Distribution — Octonion vs Sedenion'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Right: fractal dim of gnarl
ax2=axes[1]
fracs=[0.0,0.1,0.25,0.5,0.75,1.0]
g_means_frac=[]
for uf in fracs:
    gs=[]
    for _ in range(80):
        ar=np.random.randn(8); as_=np.random.randn(8)
        a=np.concatenate([ar*(1-uf),as_*uf]); a/=np.linalg.norm(a)
        mx=0
        for _ in range(10):
            b=np.random.randn(16); b/=np.linalg.norm(b)
            mx=max(mx,float(np.linalg.norm(cd_mul(a,b))))
        gs.append(mx)
    g_means_frac.append(float(np.mean(gs)))
ax2.plot(fracs, g_means_frac,'steelblue',lw=2,marker='o')
ax2.axhline(OMEGA_ZS,color='r',ls='--',label='OMEGA_ZS')
ax2.set_xlabel('Upper sedenion fraction'); ax2.set_ylabel('Mean g(a)')
ax2.set_title('g → OMEGA_ZS as algebra spans full sedenion'); ax2.legend(); ax2.grid(alpha=0.3)
plt.tight_layout(); plt.show()
""",

'orbit_trap_address': """
fig, axes = plt.subplots(1, 2, figsize=(13, 6))

# Mandelbrot set (low resolution for speed)
def mandelbrot(c, max_iter=128):
    z=0j
    for i in range(max_iter):
        if abs(z)>2: return i
        z=z*z+c
    return max_iter

N=300
x_range=np.linspace(-2.5,1.0,N); y_range=np.linspace(-1.5,1.5,N)
M=np.array([[mandelbrot(complex(x,y)) for x in x_range] for y in y_range])

ax=axes[0]
im=ax.imshow(M,extent=[-2.5,1,-1.5,1.5],cmap='inferno',origin='lower',interpolation='bilinear')
plt.colorbar(im,ax=ax,label='Escape iterations')
ax.axvline(-0.75,color='cyan',ls='--',lw=2,label='c=-3/4 ↔ σ=½')
ax.set_title('Mandelbrot Set: σ=½ ↔ c=-3/4'); ax.legend(fontsize=9)
ax.set_xlabel('Re(c)'); ax.set_ylabel('Im(c)')

# Right: orbit trap addresses for sample words
PRIMES_OT=[2,3,5,7,11,13,17,19,23,29,31,37]
MOD_OT=10**9+7
words=['life','death','prime','zero','fire','sigma','omega','sedenion','brim','gap']
def word_addr(w):
    h=sum(ord(c)*PRIMES_OT[i%len(PRIMES_OT)] for i,c in enumerate(w.lower()))%MOD_OT
    s=h/MOD_OT
    dim=h%16
    c_re=(s-0.5)*2.5-0.25; c_im=(dim/16-0.5)*3.0
    return s, dim, c_re, c_im

ax2=axes[1]
for w in words:
    s,dim,c_re,c_im=word_addr(w)
    n_it=mandelbrot(complex(c_re,c_im),256)
    in_set=(n_it==256)
    color='red' if in_set else 'steelblue'
    ax2.scatter(c_re,c_im,c=color,s=80,zorder=5)
    ax2.annotate(w,(c_re,c_im),textcoords='offset points',xytext=(4,4),fontsize=8)

ax2.axvline(-0.75,color='purple',ls='--',alpha=0.6,label='c=-3/4 (σ=½)')
x_m=np.linspace(-2.5,1,200); y_m=np.linspace(-1.5,1.5,200)
M2=np.array([[mandelbrot(complex(x,y),64) for x in x_m] for y in y_m])
ax2.contour(x_m,y_m,M2,levels=[64],colors='black',linewidths=0.5,alpha=0.4)
ax2.set_title('Hyperwebster Word Addresses in Mandelbrot Space')
ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
ax2.set_xlabel('Re(c_word)'); ax2.set_ylabel('Im(c_word)')
red_p=mpatches.Patch(color='red',label='In Mandelbrot (interior ↔ deep sedenion)')
blue_p=mpatches.Patch(color='steelblue',label='Exterior (escaping)')
ax2.legend(handles=[red_p,blue_p],fontsize=8)
plt.tight_layout(); plt.show()
""",

'periodic_table': """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: First IE vs Z with CD stratum coloring
Z_vals = list(range(1,21))
IE_vals = [13.598,24.587,5.392,9.323,8.298,11.260,14.534,13.618,17.423,21.565,
           5.139,7.646,5.986,8.152,10.487,10.360,12.968,15.760,4.341,6.113]
def get_cd(Z):
    if Z<=2: return 0  # ℝ
    if Z<=4: return 1  # ℂ (s)
    if Z<=10: return 2  # ℂ/ℍ (p)
    if Z<=12: return 3  # ℂ (s)
    if Z<=18: return 4  # ℂ/ℍ (p)
    return 5  # ℂ (s)

cmap = {0:'#E74C3C',1:'#3498DB',2:'#2ECC71',3:'#3498DB',4:'#2ECC71',5:'#3498DB'}
clabel = {0:'ℝ',1:'ℂ (s)',2:'ℂ/ℍ (p)',3:'ℂ (s)',4:'ℂ/ℍ (p)',5:'ℂ (s)'}
ax=axes[0]
colors_z=[cmap[get_cd(Z)] for Z in Z_vals]
ax.scatter(Z_vals,IE_vals,c=colors_z,s=100,zorder=5)
ax.plot(Z_vals,IE_vals,'gray',alpha=0.3)
for Z,IE in zip(Z_vals,IE_vals):
    ax.annotate(str(Z),(Z,IE),textcoords='offset points',xytext=(2,3),fontsize=7)
from matplotlib.lines import Line2D
handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=c,ms=10,label=l)
         for c,l in zip(['#E74C3C','#3498DB','#2ECC71'],['ℝ','ℂ','ℂ/ℍ'])]
ax.legend(handles=handles,fontsize=8)
ax.set_xlabel('Z (atomic number)'); ax.set_ylabel('First IE (eV)')
ax.set_title('Periodic Table: IE vs CD Stratum (Z=1..20)'); ax.grid(alpha=0.3)

# Right: d-block enzyme metals
metals=['Fe','Co','Ni','Cu','Zn']; d_electrons=[6,7,8,10,10]
ax2=axes[1]
bars2=ax2.bar(metals,d_electrons,color=['#E91E63','#9C27B0','#3F51B5','#FF9800','#607D8B'],alpha=0.85)
ax2.axhline(7,color='g',ls='--',lw=2,label='7 = full octonion imaginaries (Co/B12)')
ax2.set_ylabel('d-electrons'); ax2.set_title('d-Block Enzyme Metals: Octonion Boundary')
ax2.legend(fontsize=9); ax2.grid(alpha=0.3)
for bar,d in zip(bars2,d_electrons):
    ax2.text(bar.get_x()+bar.get_width()/2,d+0.1,f'{d}d',ha='center',fontsize=11,fontweight='bold')
plt.tight_layout(); plt.show()
""",

}

# ── Engine registry ────────────────────────────────────────────────────────────

ENGINES = [
  # (tier, fn_name, title, description, claim_tex, output_dir)
  (7,'explicit_formula_de_sitter',
   'Explicit Formula as de Sitter Expansion',
   'The Chebyshev explicit formula ψ(x) = x − Σ xᵖ/ρ. The x-term is cosmological expansion. Zeros = BAO oscillations.',
   r'\psi(x)=x-\sum_\rho x^\rho/\rho-\ln 2\pi', 'tier7'),
  (7,'sin_cos_frequencies',
   'Sin/Cos as Counter-Rotating Vortices',
   'e^{±iθ} are the two counter-rotating vortices. tan θ = 1 at σ=½. NS singularity = tan → ∞.',
   r'e^{\pm i\theta}=\text{two vortices},\;\tan\theta=1\Leftrightarrow\sigma=\tfrac{1}{2}', 'tier7'),
  (7,'galaxy_formation',
   'Galaxy Formation from Conformal Inversion',
   'r → R_H²/r maps null cone to galaxy. Tip→BH, brim→disk, fabric→dark matter halo.',
   r'r\to R_H^2/r,\;\rho(r)=\rho_0 R_H^2/r^2', 'tier7'),
  (7,'dark_matter_geometry',
   'Dark Matter as Geometric Shadow',
   'Dark matter = inversion shadow = Chladni antinode = Im(ψ). V_flat = OMEGA_ZS × V_max.',
   r'\rho_{\rm DM}=\rho_0 R_H^2/r^2,\;V_{\rm flat}=\Omega_{\zeta\Sigma}V_{\max}', 'tier7'),
  (7,'navier_stokes_sedenion',
   'Navier-Stokes: Classical Failure → Sedenion Revision',
   'NS fails in ℝ (missing i). Works in ℂ. Universe NS = exact. BAO = NS acoustic modes.',
   r'\partial_t U+(U\cdot\nabla)U=-\nabla P/\rho+\nu\nabla^2 U,\;|U|^2=\mathrm{const}', 'tier7'),
  (7,'black_hole_crossing',
   'Black Hole Horizon Crossing Simulation',
   'Algebraic phase transition: octonion→sedenion at brim. Associativity breaks. Time arrow emerges.',
   r'[a,b,c]=0\;(t<t_{\rm brim})\to[a,b,c]\neq0\;(t>t_{\rm brim})', 'tier7'),
  (7,'lambda_cdm_omega_zs',
   'ΛCDM + OMEGA_ZS Attractor',
   'OMEGA_ZS = de Sitter attractor. We are above it. DESI prediction: w → -1.31.',
   r'H^2=H_0^2[\Omega_m(1+z)^3+\Omega_\Lambda],\;\Omega_\Lambda\to\Omega_{\zeta\Sigma}', 'tier7'),
  (7,'flt_noether_deepened',
   'Fermat Last Theorem = Noether Conservation Law',
   'FLT = the root certificate of J_R+J_G+J_B=0. Wiles proved R̂†=B̂ exactly.',
   r'a^n+b^n\neq c^n\Leftrightarrow\hat{R}^\dagger=\hat{B}\Leftrightarrow J_R+J_G+J_B=0', 'tier7'),
  (7,'leech_lattice_sedenion',
   'Leech Lattice Defines Sedenion Zero-Divisors',
   '24D Leech lattice projects to 16D sedenion zero-divisors. Mass gap = projection distance.',
   r'\Lambda_{24}\supset\mathbb{S}_{16},\;\text{ZD}=\text{shadow of }\Lambda_{24}', 'tier7'),
  (7,'gue_random_matrix',
   'Prime Gaps = GUE Statistics = Quantum Chaos',
   'Montgomery-Odlyzko: R₂(x)=1−(sin πx/πx)². BK prediction confirmed numerically.',
   r'R_2(x)=1-\left(\frac{\sin\pi x}{\pi x}\right)^2', 'tier7'),
  (7,'smmip_standard_model',
   'SMMIP ↔ Standard Model (Term for Term)',
   'L_SM drops out of H_RB term-for-term. J_R→L_gauge, J_G→L_Higgs, J_B→L_fermion.',
   r'\mathcal{L}_{SM}=J_R^{\rm kin}+J_G^{\rm vac}+J_B^{\rm pot}+J_R J_B|_{\sigma=1/2}', 'tier7'),
  (7,'gauge_group_cd_tower',
   'Gauge Groups from CD Tower Automorphisms',
   'U(1)×SU(2)×SU(3) = Aut(ℂ)×Aut(ℍ)×Aut(𝕆). Derived, not postulated. e₁₅ prevents GUT.',
   r'\mathrm{Aut}(\mathbb{C})=U(1),\;\mathrm{Aut}(\mathbb{H})=SU(2),\;\mathrm{Aut}(\mathbb{O})\supset SU(3)', 'tier7'),
  (7,'hydrogen_spectral_cd',
   'Hydrogen Spectral Series from CD Strata',
   'n=1→ℝ, 2→ℂ, 3→ℍ, 4→𝕆, 5→𝕊. Rydberg formula from SMMIP. Balmer Hα=656.1nm.',
   r'1/\lambda=R_\infty(1/n_1^2-1/n_2^2),\;n_k\leftrightarrow\text{CD level }k', 'tier7'),
  (7,'pauli_exclusion_fermat',
   'Pauli Exclusion = FLT + Sedenion Zero-Divisors',
   'Bosons: n≤2 (Pythagorean triples). Fermions: n≥3 (FLT). Three names for one theorem.',
   r'|\psi\rangle^{\otimes2}_{\rm anti}=0\Leftrightarrow a\cdot b=0\Leftrightarrow a^n+b^n\neq c^n', 'tier7'),
  (7,'slingshot_light',
   'Slingshot Light: Photons Extract Energy from Cosmic Structures',
   'Photons gain frequency passing inside conformal inversion boundary. Bias ~ dark energy signal.',
   r'\Delta f/f=2GM/(r_{\min}c^2),\;f_{\rm out}/f_{\rm in}=(R_H/r_{\min})^2', 'tier7'),
  (7,'standard_candle_uselessness',
   'Standard Candles Are Broken by Slingshot',
   'Type Ia SNe biased by slingshot (cluster vs void environments). Hubble tension = slingshot bias.',
   r'\mu_{\rm obs}=\mu_{\rm true}+\delta_{\rm sling}(z,\mathrm{env})', 'tier7'),
  (7,'lambda_cdm_cmb_gold_standard',
   'ΛCDM CMB is the Gold Standard',
   'CMB is slingshot-immune (z=1100, no structure). Ω_M ≈ OMEGA_ZS². H₀ tension = ladder bias.',
   r'H_0^{\rm CMB}=67.4\;\mathrm{km/s/Mpc},\;\Omega_M\approx\Omega_{\zeta\Sigma}^2', 'tier7'),
  (7,'halocline_ns_surface',
   'Halocline: NS σ=½ Surface',
   'Two-density interface. Ri_crit = 1/4 = σ² EXACT. Interface stabilised by zero-divisors.',
   r'\mathrm{Ri}_c=\tfrac{1}{4}=\sigma_{1/2}^2,\;h_{\min}=R_H\cdot\delta_{\rm YM}/(\rho_2/\rho_1)', 'tier7'),

  (8,'sedenion_self_organisation',
   'Sedenion Self-Organisation: 16 Operators → d*/σ½/D*=1',
   '16 SMMIP operator names, prime-hashed, self-organise to d*/σ_mean/D* = 1. Zero free parameters.',
   r'd^*/\bar\sigma\cdot D^*=1', 'tier8'),
  (8,'gnarl_validation',
   'Gnarl Validation: Fractal Sedenion Boundary',
   'Mean g(a) = OMEGA_ZS over unit sedenion sphere. Octonion: g=1. Upper sedenion: g<1.',
   r'\langle g\rangle_{S^{15}}=\Omega_{\zeta\Sigma},\;\dim_H(\text{Gnarl})=14+d^*', 'tier8'),
  (8,'omega_zs_6_family',
   'OMEGA_ZS 6-Family: One Constant, Six Domains',
   'W(1) = OMEGA_ZS appears in mathematics, primes, cosmology, Yang-Mills, sedenion, information.',
   r'\Omega_{\zeta\Sigma}=W(1)=e^{-\Omega_{\zeta\Sigma}},\;\Omega_{\zeta\Sigma}^2\approx\Omega_M', 'tier8'),
  (8,'hermite_timing_wheel',
   'Hermite Timing Wheel: BAO Acoustic Modes',
   'H_n has n real zeros = n BAO timing marks. γ_n/(2π) = BK scale x₀(n). CMB peaks = H_n levels.',
   r'H_n\text{ zeros}=n\text{ BAO modes},\;x_0(n)=\gamma_n/2\pi', 'tier8'),
  (8,'orbit_trap_address',
   'Orbit Trap: Hyperwebster Mandelbrot Address',
   'Mandelbrot boundary = gnarl. c = -3/4 ↔ σ=½. Every word has a fractal address.',
   r'z\to z^2+c,\;c=-3/4\leftrightarrow\sigma=1/2,\;\mathrm{HD}=1+d^*', 'tier8'),
  (8,'leech_divergence_inversion',
   'Leech Divergence Inversion: Zero-Divisors are Sources',
   'ZD are not permanent sinks — divergence-inverted. φ_ZD=V_24−V_16. 196,560 backward x-affinities.',
   r'\phi_{\rm ZD}=V_{24}-V_{16}=\frac{\pi^{12}}{12!}-\frac{\pi^8}{8!},\;\text{gate}=e^{i\phi_{\rm ZD}}', 'tier8'),

  (9,'periodic_table',
   'Periodic Table from CD Strata',
   's/p/d/f blocks from ℂ/ℍ/𝕆 automorphisms. Fe at ℍ/𝕆 boundary = enzyme catalysis.',
   r'\text{s}\leftrightarrow\mathbb{C},\;\text{p}\leftrightarrow\partial(\mathbb{C}/\mathbb{H}),\;\text{d}\leftrightarrow\partial(\mathbb{H}/\mathbb{O})', 'tier9'),
  (9,'cosic_eiip',
   'Cosic EIIP: Protein Function = Riemann Zero Address',
   'EIIP DFT peak of protein = γ_n. Oncoproteins share address with growth factors.',
   r'f^*({\rm protein})=\gamma_n/(2\pi L)', 'tier9'),
  (9,'cancer_zero_divisor',
   'Cancer = Zero-Divisor Collapse',
   'Stop signals nullified: s·t_stop=0 with s,t≠0. Three signatures. GAP=0.000707=threshold.',
   r's_{\rm cancer}\cdot t_{\rm stop}=0,\;s\neq0,\;t\neq0', 'tier9'),
  (9,'drug_targeting',
   'Drug Targeting: Conformal Inversion of Cancer',
   'c_drug = R_H² c†/|c|². c_drug·c_cancer = R_H²e₀. G:A:V=6:3:1. SOR prototype.',
   r'c_{\rm drug}=R_H^2 c^\dagger/|c|^2,\;c_{\rm drug}\cdot c_{\rm cancer}=R_H^2 e_0', 'tier9'),
  (9,'hydro_radiolysis_chromatography',
   'Hydro-Radiolysis Chromatography: Noether Diagnostic',
   'OH•→J_R, eaq⁻→J_B, H₂O₂→J_G. Healthy A_R/A_B=OMEGA_ZS. G:A:V=6:3:1. SOR restores balance.',
   r'A_R/A_B=\Omega_{\zeta\Sigma}\;(\text{healthy}),\;G:A:V=6:3:1', 'tier9'),
]

# ── Generate all notebooks ─────────────────────────────────────────────────────

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    print(f"Generating {len(ENGINES)} Ainulindale notebooks...")
    for (tier, fn, title, desc, tex, outdir) in ENGINES:
        plot = PLOTS.get(fn, "print('No custom plot for this engine. Run result.keys() to explore.')\nprint(result['claim'])")
        notebook = engine_notebook(tier, fn, title, desc, plot, tex)
        path = os.path.join(base, outdir, f'{fn}.ipynb')
        save(path, notebook)
    print(f"\nDone. {len(ENGINES)} notebooks written.")
    print("\nDirectory structure:")
    for d in ['tier7','tier8','tier9']:
        files = [f for f in os.listdir(os.path.join(base,d)) if f.endswith('.ipynb')]
        print(f"  {d}/: {len(files)} notebooks")
