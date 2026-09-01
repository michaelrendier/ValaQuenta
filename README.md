# ValaQuenta

**The derivation engine.** Pure mathematics. Runnable code. No physical substrate required.

```
Ainulindale (the Music) → ValaQuenta (the engines) → VAPMIP (the world)
```

---

## Architecture

ValaQuenta is a Python package. All engines import cleanly as `from ValaQuenta.X import Y`.

```
ValaQuenta/
├── bao_mass_gap.py      Yang-Mills mass gap (ESTABLISHED)
├── hamiltonian.py       H=xp, Fermat elliptic, RedBlue
├── noether.py           Ascending/descending Noether currents
├── galactic_cavity.py   Dark matter = pilot wave (SPARC confirmed)
├── telperion.py         Galactic bell geometry — 10/10 predictions confirmed
├── fixed_point.py       The Unit + T_256 (Bang as inside-out horizon)
├── capacitor.py         Semantic low-pass filter
├── understand.py        Read → Ponder → Calculate → Understand
│
├── modules/             Domain engines (one module per Millennium problem / tier)
│   ├── add_scale_sign/  THE TIER-0 DATATYPE — Aff(1,ℝ) = ADD ⋊ (SCALE × SIGN)
│   ├── berry_keating/   Riemann zeros, d*, Witches Hat, prime gaps
│   ├── clay_millennium/ Yang-Mills, Navier-Stokes, P vs NP
│   ├── constants/       OMEGA_ZS, d*, GAP, φ, π
│   ├── derivation_chain/ Tier 0 → Tier 9 derivation registry
│   ├── h_rb_hat/        SIGMA_RB baseline engine (general)
│   ├── hyperwebster/    Zipf = Prime Number Theorem
│   ├── inversion/       Circle inversion / L_(I|O) geometry
│   ├── jwst/            BAO, CMB, cosmological engines
│   ├── lagrangian/      VAPMIP Lagrangian — L_NN (rename pending)
│   ├── noether/         Noether currents, conservation proofs
│   ├── noether_information/ Information current, distillation
│   ├── sigma_cavitation/ Bang = phase transition, BEC medium
│   ├── singularity_null/ ZD lattice, 42/84/168 exact counts
│   ├── sonification/    Schumann resonances, sound from primes
│   ├── spherical/       N-ball transformer V(n), n* peak
│   ├── tier6_physics/   Pilot wave, Bohmian mechanics
│   ├── tier7_cosmos/    Galactic cavity, dark energy, BEC
│   ├── tier8_sedenion/  16 operators, ZD structure
│   ├── tier9_chem/      Cancer = ZD, drug = adjoint
│   └── turing_diagonal/ Halting problem geometry
│
├── notebooks/           Derivation notebooks (70, all executing)
│   ├── engines/         One per top-level engine (13)
│   ├── core/            One per foundational module (14)
│   ├── tier7/ tier8/ tier9/   Cosmology, sedenion, chemistry (29)
│   └── translator/ h_rb_hat/ singularity_null/ turing_diagonal/
├── ZeroLattice/         Telperion paper notebooks (4)
├── code/                Standalone implementations
│   ├── noether_engine/
│   ├── sonification/
│   └── wiles_modularity/
├── wiki/                One page per engine — results (51)
│
├── requirements.txt     Dependencies, derived from actual imports
├── install.sh           Linux installer
├── install-macos.sh     macOS installer
├── install.ps1          Windows installer
└── verify_install.py    Checks the arithmetic, not just the imports
```

---

## Engines and Results

### modules/add_scale_sign/ — the tier-0 datatype

```
ASS(add, scale, sign)  =  x ↦ sign·scale·x + add   —  an element of
  Aff(1,ℝ) = ℝ ⋊ (ℝ_{>0} × ℤ/2) = ADD ⋊ (SCALE × SIGN)

compose  A @ B        invert  ~A        residual  A.residual('SIGN')  (str.strip-style)
decompose  A.lineage(order='chrono' | 'zeta')  →  ASSWord

each generator's equation part:   ADD → a      SCALE → ln s      SIGN → g
the generalized equation:         u = Σₖ [ gₖ·ln sₖ + aₖ ]      Γ = tanh(u/2)
ground state a=0, s=1, g=+1  ⇒  u=0  ⇒  Γ=0  ⇒  the now

firing order (the 3-phase camshaft):  SIGN → SCALE → ADD,  x ↦ ADD(SCALE(SIGN(x)))
firing defect  u − (a + ln s) = (g−1)·ln s   (non-zero ⇔ SIGN flipped a non-trivial SCALE)
orthogonal Smith charts:  Γ_SCALE = tanh(½·ln s)  ⟂  Γ_ADD = tanh(½·a),  parity g
```

Registered as `AddScaleSignModule` (6 code-verified equations; `python3 -m
ValaQuenta --info`). The decomposition maths (the four-question test, roll-down)
stays in `VAPMIP/add_scale_sign.py` — not duplicated. Also an engine + tool in
the SFR decomposer suite (with the fast inverse square root as the worked
example). Formal spec: [wiki/add_scale_sign.md](wiki/add_scale_sign.md) ·
`Ainulindale/wiki/107_add_scale_sign_datatype.md`.

### bao_mass_gap.py — Yang-Mills Mass Gap

```
Status: ESTABLISHED (all 5 checks pass)

OMEGA_ZS = 0.5671432904097838  (Lambert W(1), exact)
D_STAR   = 0.24600             (BK spectral, 5 sig figs)
GAP      = 0.000707357533249   (OMEGA_ZS − D_STAR × ln(10))

GAP ≈ 1/(1000√2)  [0.035% approximation]
NOTE: 1/√2000 = 0.02236 — NOT the gap (31.6× larger)
```

See [wiki/bao_mass_gap.md](wiki/bao_mass_gap.md)

### hamiltonian.py — H = xp

```
HamiltonianXP:
  scale_check(2,3,λ=2) → True
  trajectory(1,1,t=1)  → x=e, p=1/e, E=xp=1.0 (conserved exactly)
  zeros (BK, first 5)  → [14.1347, 21.0220, 25.0109, 30.4249, 32.9351]

FermatEllipticHamiltonian (lemniscatic, g₂=1, g₃=0):
  Discriminant Δ = 1.0 (valid elliptic curve)
  ℘(1.0) = 1.05083333

RedBlueHamiltonian:
  Red(σ=½) = Blue(σ=½) = 0.707...  (balance at σ=½ ✓)
```

See [wiki/hamiltonian.md](wiki/hamiltonian.md)

### noether.py — Ascending/Descending Noether Currents

```
forced_sigma(E, σ₀=any) → 0.5   exactly, for any real σ₀ and any E

FIXED (2026-08-28): the old softmax-weighted-average iteration converged to
σ=½ only for E ≲ 10 (returned σ₀ unchanged above; OverflowError for σ₀<0).
The balance F=B is, in logs, E(1−2σ)=0 — linear in σ — so it is now solved
exactly in one Newton step from any σ₀, with no exp evaluated away from the
balance point. See wiki/noether.md. (Notebook 03_noether.ipynb still shows
the old behaviour and needs a re-run.)

The boundary is ORIENTED: up (toward next CD shadow) / down (toward ZD).
σ=½ is the shadow of the world above — projection of the next CD level.
```

See [wiki/noether.md](wiki/noether.md)

### galactic_cavity.py — Galactic Pilot Wave

```
r_t    = 0.738 kpc   (dark matter threshold, d* × r_max_bar)
v_flat = 220.0 km/s  (flat rotation, confirmed)
Period = 22.7 Gyr    (frozen — exceeds universe age 13.8 Gyr)
P1 (r_t = d* × r_max_bar): confirmed against SPARC 97-galaxy sample 2026-05-30
```

See [wiki/galactic_cavity.md](wiki/galactic_cavity.md)

### capacitor.py — Semantic Low-Pass Filter

```
H(0) = 1.0  (DC gain — the prime passes through unattenuated)
Pole at s = −1/τ  (stable, left half-plane)
Transfer function: H(s) = 1/(1+sτ)
```

See [wiki/capacitor.md](wiki/capacitor.md)

### understand.py — LSHS Pipeline

```
U.process("why is the mass gap 1 over root 2000")
  prime = 0.5 + 48.0052j  (Riemann zero γ₉)
  σ     = 0.5000000000    (derived, never assigned)
  dc    = 0.50000000      (the prime, extracted)

σ=½ is derived for every input. The mathematics forces it.
```

See [wiki/understand.md](wiki/understand.md)

---

## Key Identity — What "1/root(2000)" Actually Means

Do not write `GAP = 1/√2000`. Write `GAP ≈ 1/(1000√2)`:

```
1/√2000        = 0.022360...   ← NOT the gap
1/(1000√2)     = 0.000707...   ← the approximate identity (0.035% error)
1/√(2,000,000) = 0.000707...   ← same thing, unambiguous
```

The 1/√2 factor is explained (σ=½ symmetry, first CD doubling). The 10³ factor is an open question.

---

## Install

```bash
git clone <this repo>            # into a directory on your PATH-able parent
cd ValaQuenta

bash install.sh                  # Linux   — creates .venv, installs, verifies
bash install-macos.sh            # macOS   — same, prefers Homebrew python
powershell -ExecutionPolicy Bypass -File .\install.ps1   # Windows
```

Flags: `--user` (no venv), `--system` (use distro packages), `--no-jupyter`.
Run the scripts with `bash install.sh`, not `./install.sh` — the executable bit
does not survive every filesystem.

Then, any time:

```bash
python3 verify_install.py
```

This does not merely check that imports succeed. It recomputes GAP from its two
inputs, confirms OMEGA_ZS satisfies `W·e^W = 1`, counts the zero-divisor pairs
(84), and checks that `H=xp` conserves energy. If the arithmetic is broken it
will say so.

Dependencies are in `requirements.txt`: numpy, scipy and matplotlib are
required; JupyterLab is needed only to open the notebooks.

### ⚠ The venv is the general-purpose environment for every repo

**`ValaQuenta/.venv` is provisioned to run code in ANY repo in ThePlace** —
ValaQuenta, Ainulindale, VAPMIP, PtolC, RiemannHypothesisProof, FourthAgePapers,
SedenionSpectralRelativity. Only **BulletCluster** keeps a separate venv, because
its telescope pins are specific to that work.

```bash
source env.sh          # activate
./env.sh check         # verify — prints every module and its version
```

**Do not use the system python for project code.** It has numpy 2.4.6 (pip,
`~/.local`) shadowing numpy 1.26.4 (apt), and every apt-built C extension is
still linked against 1.x. Confirmed broken system-wide: `pandas`,
`scikit-learn`, **`nltk`**, `bottleneck`, `numcodecs`, `zarr`, `reproject`,
`aplpy`. pip cannot repair it in place — PEP 668, externally managed.
**All of them work inside the venv.**

> The 2026-08-06 primer recorded "NLTK is broken in this environment — do not
> spend time fixing it." That was never NLTK's fault. It is the numpy ABI split,
> and the venv fixes it. WordNet corpora still need
> `python -m nltk.downloader wordnet`.

Verified 2026-08-14, Python 3.12.3, **35/35 imports clean**. `requirements.txt`
records the version actually installed and tested beside each pin, plus the
packages deliberately *excluded* (whisper, PyQt, rtlsdr, bpy, qtermwidget) and
the system libraries some entries imply.

## Run

```bash
python3 -c "from ValaQuenta.bao_mass_gap import validate; validate()"
python3 -c "from ValaQuenta.understand import Understand; u=Understand(); print(u.process('the prime'))"
python3 -m ValaQuenta --info        # registry summary
python3 -m ValaQuenta --curses      # THE DERIVATION BROWSER, no Qt needed
```

### The Derivation Browser (`--curses`)

A file-manager over the registry — you pick ValaQuenta apart one scope at a
time, `dir()`-style, the way a package browser walks a package. The breadcrumb
**is** the API path (`/ <engine> / <equation>`); the engine naming conventions
**are** the function breadcrumbs.

- **Left pane** — the current listing (engines → equations → run). `..` goes up.
- **Right pane** — the **DECLARATION**: a plain-English, outside-observer line
  of *what this does as a derivation step* (`Equation.process`,
  `EquationModule.process_description`), then `latex` / `radian_form` / params.
  An equation with no `process=` shows a visible `[process= not set]` TODO.
- **`Enter`** runs the equation; **`p`** shows the proof-on-the-fly INPUTS a
  sympy guided derivation would consume (the seam is wired, the tour is TODO).
- **`a`** opens the **analysis lenses** — run a tool *across any engine's
  mathematics, including its own*: `emerge` (sedenion bracketing & firing
  order), `spectral` and `lineage` (`FactoralDecomposition`), `calibrate`
  (the factoral decomposition of the current engine). Sibling repos are
  imported lazily; a missing one is reported, not fatal.

Keys: `↑↓` nav · `→/Enter` open·run · `←/⌫` up · `Tab` focus · `/` filter ·
`d` display mode · `a` lenses · `p` proof inputs · `q` quit.

## Where to start

| If you want | Go to |
|---|---|
| Results without running anything | [wiki/00_index.md](wiki/00_index.md) |
| The order the derivation goes in | [wiki/derivation_chain.md](wiki/derivation_chain.md) |
| The top-level engines, worked | [notebooks/engines/](notebooks/engines/) |
| One module per Millennium problem / tier | [notebooks/core/](notebooks/core/) |
| What is known to be broken | [wiki/00_index.md](wiki/00_index.md) § Known defects |

All 70 notebooks execute clean — 393/393 code cells, verified 2026-07-28.

---

## Relation to Other Repos

| Repo | Role |
|------|------|
| `Ainulindale/` | The Music — theory, wikis, derivation notebooks, addenda |
| `ValaQuenta/` | The Engines — runnable mathematics, this repo |
| `VAPMIP/` | The World — LSHS system, Ptolemy corpus engine, SVG outputs |
