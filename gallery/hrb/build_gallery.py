"""
gallery/hrb/build_gallery.py -- writes the H_RB gallery pages (canvas2d_*.html, svg_*.html, index.html) from data/hrb_data.js.

    python3 ValaQuenta/gallery/hrb/build_gallery.py          (after experiments.py has written data/hrb_data.js)
    ValaQuenta/gallery/hrb/serve_gallery.sh [port=8790]

Every page: Cody's favicon, contact bar, light/dark tokens, the d* four-faces block, sources on GitHub, literature.
A picture shows a space or a machinery; it is not evidence. Status labels: CALCULATED = this repository's code produced it;
the two lifts of sigma_rb to the sedenion are definitions (OPEN). No bare sigma: sigma_riemann, sigma_rb, ... (wiki/DISAMBIGUATION_NOTES.md).

d* faces (all four are needed to chart ln(10) in Universal Native Space):
  d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)
  d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)
  d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)
  d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)
Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/michaelrendier/ValaQuenta/blob/main/"

CSS = """
:root{--bg:#f5f3ec;--fg:#16202c;--mut:#3a4656;--card:#fbfaf6;--line:#d6d1c3;--acc:#1f5fa8;--c1:#1f5fa8;--c2:#b5481a;--c3:#2a7d4f;--c4:#8a3fa0;--c5:#b08900;--c6:#157a85;--badge:#ffd34d;--badge-fg:#000}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151c;--fg:#e8edf3;--mut:#b9c3d0;--card:#18202a;--line:#33404f;--acc:#8ec0ff;--c1:#8ec0ff;--c2:#ff9f6b;--c3:#6fd39b;--c4:#d59bff;--c5:#ffd34d;--c6:#6fe0ea}}
:root[data-theme="dark"]{--bg:#10151c;--fg:#e8edf3;--mut:#b9c3d0;--card:#18202a;--line:#33404f;--acc:#8ec0ff;--c1:#8ec0ff;--c2:#ff9f6b;--c3:#6fd39b;--c4:#d59bff;--c5:#ffd34d;--c6:#6fe0ea}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,Segoe UI,sans-serif}
.ct-bar{background:#0d1020;color:#cfd6ee;font:13px system-ui;padding:6px 16px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}.ct-bar a,.ct-foot a{color:#9cc4ff}.ct-bar b{color:#e6e9f5}
.ct-orcid{display:inline-block;width:14px;height:14px;border-radius:50%;background:#a6ce39;color:#fff;font:700 9px/14px sans-serif;text-align:center;margin-right:4px;vertical-align:-2px}.ct-sep{opacity:.4}
header,main,footer{max-width:1200px;margin:0 auto;padding:0 16px}header{padding-top:18px}h1{margin:.1em 0 .2em;font-size:1.6rem}h2{font-size:1.15rem;margin:1.4em 0 .4em}
p.lead{margin:.2em 0 1em;color:var(--mut);max-width:80ch}.nav a{color:var(--acc);margin-right:14px}
.fig{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 20px;padding:12px;position:relative}.fig canvas{display:block;width:100%}
.imgno{position:absolute;top:8px;right:8px;background:var(--badge);color:var(--badge-fg);font-weight:700;border-radius:6px;padding:1px 8px;font-size:.85rem}
.cbar{color:var(--mut);font-size:.85rem;margin-top:4px}.note{color:var(--mut);font-size:.92rem;max-width:90ch}
table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{border:1px solid var(--line);padding:4px 8px;text-align:left}th{background:var(--card)}
.tag{display:inline-block;border:1px solid var(--line);border-radius:6px;padding:0 6px;font-size:.78rem;color:var(--mut);margin-right:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}.card a{color:var(--acc);font-weight:600;text-decoration:none}
pre.dstar{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:.78rem;color:var(--mut);overflow:auto}
.ct-foot{background:#0d1020;color:#cfd6ee;font:13px system-ui;padding:12px 16px;margin-top:30px}
button{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:5px 12px;font:inherit;cursor:pointer}input[type=range]{width:min(520px,90%)}
@media(max-width:700px){h1{font-size:1.3rem}}
"""
CONTACT = ('<div class="ct-bar"><b>Michael Rendier</b><a href="mailto:the.wandering.god@gmail.com">✉ the.wandering.god@gmail.com</a><span class="ct-sep">·</span>'
           '<a href="https://facebook.com/rendier" target="_blank" rel="noopener">Facebook</a><span class="ct-sep">·</span>'
           '<a href="https://orcid.org/0009-0007-7239-6760" target="_blank" rel="noopener"><span class="ct-orcid">iD</span>ORCID 0009-0007-7239-6760</a></div>')
FOOT = ('<footer class="ct-foot"><div><b>Cody Michael Allison (Michael Rendier)</b></div><div>All repositories: <a href="https://github.com/michaelrendier" target="_blank" rel="noopener">github.com/michaelrendier</a>'
        ' · <a href="https://michaelrendier.github.io/" target="_blank" rel="noopener">michaelrendier.github.io</a> · License GPL-3.0-only</div></footer>')
DSTAR = """<pre class="dstar">d* faces (all four are needed to chart ln(10) in Universal Native Space):
  d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)
  d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)
  d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)
  d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)
Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG</pre>"""

SRC_COMMON = [("modules/h_rb_hat/maths.py", "the scalar Ĥ_RB (facets, energies, σ_ζ sums)"), ("modules/h_rb_hat/oblique_sigma_rb.py", "the documented sigma_rb map (ψ 16 in, sigma_rb 16 out)"), ("modules/h_rb_hat/sigma16.py", "the two exploratory lifts (pages S1–S7 only)"),
              ("gallery/hrb/experiments.py", "every number on this page")]
LIT_COMMON = ["Moreno, G. (1998). The zero divisors of the Cayley–Dickson algebras over the real numbers. Bol. Soc. Mat. Mexicana 4, 13–28.",
              "Baez, J. C. (2002). The octonions. Bull. Amer. Math. Soc. 39, 145–205.",
              "Schafer, R. D. (1966). An Introduction to Nonassociative Algebras. Academic Press.",
              "Noether, E. (1918). Invariante Variationsprobleme. Nachr. Ges. Wiss. Göttingen, 235–257."]


def page(slug, num, title, lead, body, script, sources=(), lit=(), kind="canvas2d"):
    fn = f"{kind}_{slug}.html"
    if num.startswith("S"):
        body = ('<p class="note" style="border:1px solid var(--line);border-radius:8px;padding:8px 12px;background:var(--card)"><b>Exploratory.</b> This page uses one of two lifts of sigma_rb that were written for this gallery on 2026-11-25. '
                'They are not the documented map. The documented sigma_rb map is sigma_rb[k] = ψ[k]·conj ψ[k⊕4] (16 in, 16 out): see pages R1–R9.</p>' + body)
    def url(p):
        return "https://github.com/michaelrendier/TuringStack/blob/main/" + p[len("../TuringStack/"):] if p.startswith("../TuringStack/") else GH + p
    src = "".join(f'<li><a href="{url(p)}" target="_blank" rel="noopener">{p.replace("../", "")}</a> — {d}</li>' for p, d in list(sources) + SRC_COMMON)
    li = "".join(f"<li>{html.escape(x)}</li>" for x in list(lit) + LIT_COMMON)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><link rel="icon" type="image/png" href="favicon.png"><style>{CSS}</style></head><body>{CONTACT}
<header><div class="nav"><a href="index.html">← H_RB gallery</a><button onclick="hrbTheme('dark')">dark</button> <button onclick="hrbTheme('light')">light</button></div>
<h1>{html.escape(title)}</h1><p class="lead">{lead}</p></header><main>
{body}
<h2>Sources and status</h2><p class="note">CALCULATED means this repository's code produced the number; a picture shows a space or a machinery, it is not evidence. Pages S1–S7 use two exploratory lifts that are definitions, labelled OPEN; pages R1–R9 use the documented map. Sigma is never written bare: sigma_riemann (σ_ζ), sigma_rb (σ_RB), see <a href="{GH}wiki/DISAMBIGUATION_NOTES.md">DISAMBIGUATION_NOTES</a>.</p>
<ul class="note">{src}</ul><h2>Literature</h2><ul class="note">{li}</ul>{DSTAR}
</main>{FOOT}
<script src="data/hrb_data.js"></script><script src="hrb.js"></script><script>
const D=window.HRB, L=window.HRBLIB, $=(id)=>document.getElementById(id);
{script}
</script></body></html>"""
    open(os.path.join(HERE, fn), "w", encoding="utf-8").write(doc)
    return fn, num, title


def fig(id_, no, extra=""):
    return f'<div class="fig"><span class="imgno">{no}</span><canvas id="{id_}"></canvas>{extra}</div>'


P = []

# ───────────────────────────── the 16-component sigma_rb test bench ─────────────────────────────
P.append(page("direction_atlas", "S1", "Direction atlas: what the 15 imaginary components do",
    "Input: one sedenion sigma_rb = sigma_riemann·e₀ + 15 imaginary components. Its imaginary part is a direction û on the sphere S¹⁴. Under lift B (Ĥ_RB = L_C, Ĥ_BR = R_C) the current balance is β·ad_û with ad_û = L_û − R_û. This page classifies every direction the algebra singles out.",
    """<div class="fig"><span class="imgno">S1</span><div id="t1"></div></div>""" + fig("c1", "S1b") +
    """<p class="note">Reading: the 15 basis directions e₁…e₁₅ are interchangeable (ad has rank 14, all singular values 2 — checked for each). Of the 210 directions (eᵢ ± eⱼ)/√2, exactly <b>84</b> are zero divisors (L_û has nullity 4, ad_û has rank 10): the known 84. The other 126 behave like basis directions. Random directions on S¹⁴ (4,000 sampled) are never special: ad has rank 14 with a continuum of singular values. So the facets are not the 15 components as such: only the zero-divisor directions are structurally different.</p>""",
    """const A=D.atlas, basis=A.filter(a=>a.kind==='basis'), pairs=A.filter(a=>a.kind==='pair');
const zd=pairs.filter(a=>a.nullity_L===4), nz=pairs.filter(a=>a.nullity_L===0);
L.table($('t1'),['class','count','rank(ad_û)','nullity(L_û)','singular values of ad_û','singular values of L_û'],[
['basis e_k',basis.length,basis[0].rank_ad,basis[0].nullity_L,JSON.stringify(basis[0].sv_ad),JSON.stringify(basis[0].sv_L)],
['(e_i±e_j)/√2, zero divisor',zd.length,zd[0].rank_ad,zd[0].nullity_L,JSON.stringify(zd[0].sv_ad),JSON.stringify(zd[0].sv_L)],
['(e_i±e_j)/√2, not zero divisor',nz.length,nz[0].rank_ad,nz[0].nullity_L,JSON.stringify(nz[0].sv_ad),JSON.stringify(nz[0].sv_L)],
['random û on S¹⁴ (4000)',D.random_classes.reduce((s,c)=>s+c.count,0),'14','0','a continuum: '+D.random_classes.length+' distinct classes','—']]);
L.bars($('c1'),[{label:'basis e_k',v:basis.length},{label:'zero-divisor pairs',v:zd.length},{label:'other pairs',v:nz.length}],{ylabel:'directions',title:'the 210 pair directions split 84 / 126; the 15 basis directions are one class'});"""
    , [("modules/box_kite/maths.py", "basis_mul: the sedenion structure constants")]))

P.append(page("gauge_lift_a", "S2", "Lift A: the direction is a gauge",
    "Lift A multiplies the real energies E_red, E_blue by p^(−sigma_rb). The output lies in the plane span(e₀, û); it depends on (sigma_riemann, τ) only. This page shows the spread of the output norm over random directions, and where the output sits when û is cycled through e₁…e₁₅.",
    """<div class="fig"><span class="imgno">S2</span><div id="t1"></div></div>""" + fig("c1", "S2b") +
    """<p class="note">Spread of |Σ_RB| over 50 random directions at fixed (sigma_riemann, τ): ~10⁻¹⁵ (rounding). In lift A, cycling through the 15 imaginary components only moves the output between the 15 planes (e₀, e_k): the sedenion output carries no more information than the complex Dirichlet sum.</p>""",
    """L.table($('t1'),['(sigma_riemann, τ)','spread of |Σ_RB|'],Object.entries(D.lift_a_spread).map(([k,v])=>[k,v.toExponential(2)]));
L.bars($('c1'),D.cycle_basis.map(c=>{const k=c.k;return {label:'e'+k,v:Math.hypot(...c.A_total)}}),{ylabel:'|Σ_RB| (sigma_riemann=½, τ=3)',title:'output norm for û = e_k, k = 1…15 (identical)'});"""))

P.append(page("cycle_basis", "S3", "Cycling the sedenion: every basis direction, both lifts",
    "For û = e₁ … e₁₅ at sigma_riemann = ½, τ = 3: the lift-A output vector and the lift-B invariants of Ĥ_RB − Ĥ_BR and Ĥ_RB.",
    """<div class="fig"><span class="imgno">S3</span><div id="t1"></div></div>""" + """<p class="note">All 15 rows agree: ad has rank 14, the same singular values, Ĥ_RB has nullity 0. The 15 imaginary basis directions are one equivalence class for these operators; differences appear only for zero-divisor directions (S1, S4).</p>""",
    """L.table($('t1'),['û','lift A: nonzero components','lift B: rank(Ĥ_RB−Ĥ_BR)','singular values','nullity(Ĥ_RB)'],D.cycle_basis.map(c=>['e'+c.k,c.A_total.map((v,i)=>Math.abs(v)>1e-9?'e'+i+'='+v.toFixed(4):null).filter(Boolean).join(', '),c.B_rank_asym,JSON.stringify(c.B_sv_asym),c.B_nullity_HRB]));"""))

P.append(page("zero_divisor_action", "S4", "Where Ĥ_RB acts as a zero divisor",
    "Under lift B, C = α + β·û with α = Re, β = −Σ p^(−sigma_riemann) sin(τ ln p). L_C = α + β·L_û. For a zero-divisor direction L_û has nullity 4, so Ĥ_RB is singular exactly where α = 0. For a basis direction it is never singular. The picture is α over the (sigma_riemann, τ) plane with its zero set marked.",
    fig("c1", "S4") + """<div class="fig"><span class="imgno">S4b</span><div id="t1"></div></div><p class="note">The dots are sign changes of α (20 primes, the code's list). They are where Ĥ_RB would act as a zero divisor if û is one of the 84 zero-divisor directions. Truncating to 20 primes matters: with 168 primes (see S5) the pattern moves.</p>""",
    """const P=D.plane_p20;
L.heat($('c1'),P.alpha,{xmin:P.sigma_riemann[0],xmax:P.sigma_riemann.slice(-1)[0],ymin:P.tau[0],ymax:P.tau.slice(-1)[0],div:true,zmin:-8,zmax:8,xlabel:'sigma_riemann',ylabel:'τ = |Im sigma_rb|',title:'α(sigma_riemann, τ) = Re of the truncated Dirichlet sum (colour clipped to ±8)',aspect:0.55,
after:(F)=>{F.g.fillStyle='#000';D.alpha_zero_crossings.forEach(([s,t])=>{F.g.beginPath();F.g.arc(F.px(s),F.py(t),1.3,0,7);F.g.fill();});L.vline(F,0.5,'sigma_riemann=½','--fg');}});
const z=D.zero_divisor_action;L.table($('t1'),['C = α + β·û','nullity of Ĥ_RB = L_C'],[['α=0, û a zero divisor',z['alpha=0,zd']],['α=0, û a basis direction',z['alpha=0,basis']],['α=1, û a zero divisor',z['alpha=1,zd']],['α=1, û a basis direction',z['alpha=1,basis']]]);"""))

P.append(page("balance_plane", "S5", "The current balance β(sigma_riemann, τ): the difference map",
    "Ĥ_RB − Ĥ_BR = J_red + J_blue = β·ad_û. The magnitude β is the imaginary part of the Dirichlet sum at s = sigma_riemann + iτ; the direction content is ad_û. Where β = 0 the two operators coincide. On the real axis (τ = 0) β ≡ 0: a real sigma_rb has no current balance in this lift.",
    fig("c1", "S5") + '<p><button id="b20">20 primes (code list)</button> <button id="b168">168 primes</button></p><p class="note">This map is the whole difference between a facet taken on the real axis and the same sigma_riemann with imaginary content. It is also the quantity to compare against Navier–Stokes (page C1).</p>',
    """let key='plane_p20';function draw(){const P=D[key];L.heat($('c1'),P.beta,{xmin:P.sigma_riemann[0],xmax:P.sigma_riemann.slice(-1)[0],ymin:P.tau[0],ymax:P.tau.slice(-1)[0],div:true,zmin:-8,zmax:8,xlabel:'sigma_riemann',ylabel:'τ = |Im sigma_rb|',title:'β(sigma_riemann, τ) (colour clipped to ±8), '+(key==='plane_p20'?'20':'168')+' primes',aspect:0.55,
after:(F)=>{[0.5,1,2].forEach(s=>L.vline(F,s,'sigma_riemann='+s,'--fg'));}});}
$('b20').onclick=()=>{key='plane_p20';draw();};$('b168').onclick=()=>{key='plane_p168';draw();};draw();"""))

P.append(page("gap_scan", "S6", "The Mass Gap scan: nothing special at 0.000707 in these lifts",
    "The onset residual Δ = A_π − d*·ln10 = 0.000707357533 (the number the author calls the Mass Gap; 1/(1000√2) = 0.000707107). Sweep τ across eight decades at sigma_riemann = ½ and ½ ± Δ, and sigma_riemann across ½ at τ = 0 and τ = Δ.",
    fig("c1", "S6") + fig("c2", "S6b") + """<div class="fig"><span class="imgno">S6c</span><div id="t1"></div></div>
<p class="note">Both lifts are analytic in (sigma_riemann, τ): |β| = c₁·τ with c₁ = Σ p^(−½) ln p = 12.2034, so |β| at τ = Δ is 0.00863. The curve has slope 1 over the whole range and no feature at Δ; α is smooth through sigma_riemann = ½ ± Δ. <b>Result (CALCULATED): no structure at Δ in lift A or lift B.</b> Whether a string-theory observable sits at Δ cannot be tested here, because neither lift defines a string observable; the earlier claim that several models found string theory at this location is not reproduced by this test and stays unverified until an observable is stated. GAP·1000·√2 = 1.000355 (relative difference 3.5×10⁻⁴), recorded, not explained.</p>""",
    """const G=D.gap_scan,T=G.tau;
L.lines($('c1'),[{name:'|β| at sigma_riemann=½',x:T,y:G.half.map(Math.abs)},{name:'sigma_riemann=½+Δ',x:T,y:G['half+gap'].map(Math.abs),dash:[4,3]},{name:'sigma_riemann=½−Δ',x:T,y:G['half-gap'].map(Math.abs),dash:[2,3]}],{logx:true,logy:true,xmin:1e-8,xmax:10,ymin:1e-7,ymax:20,xlabel:'τ = |Im sigma_rb|',ylabel:'|β| = |J_red+J_blue| coefficient',title:'current balance against τ; Δ marked',after:(F)=>L.vline(F,D.constants.GAP,'τ = Δ','--c2')});
L.lines($('c2'),[{name:'α at τ=0',x:G.sigma_riemann_near_half,y:G.alpha_near_half_tau0},{name:'α at τ=Δ',x:G.sigma_riemann_near_half,y:G.alpha_near_half_tauGAP,dash:[4,3]}],{xlabel:'sigma_riemann',ylabel:'α',title:'α near sigma_riemann = ½ (smooth)',after:(F)=>{L.vline(F,0.5,'½','--fg');L.vline(F,0.5+D.constants.GAP,'½+Δ','--c2');}});
L.table($('t1'),['quantity','value'],[['Δ = A_π − d*·ln10',D.constants.GAP],['1/(1000√2)',D.constants.GAP_closed_form],['Δ·1000·√2',G.ratio_1000_sqrt2_gap],['c₁ = Σ p^(−½) ln p',G.slope_const_c1],['β(sigma_riemann=½, τ=Δ)',G.beta_at_tau_GAP],['c₁·Δ',G.tau_GAP_times_c1]]);"""))

P.append(page("facet_table", "S7", "Facets as σ_ζ values: scalar engine and the 16D lift",
    "A facet in the scalar engine is a value of sigma_riemann (GR 2, Yang–Mills 1, Navier–Stokes 1 with Im = 0, QM and Riemann ½). The table gives the code's own coupling sums and, for lift B, α, β and the size of the current balance at each facet for τ = 0, τ = γ₁ (the first Riemann zero ordinate) and τ = Δ.",
    fig("c1", "S7") + """<div class="fig"><span class="imgno">S7b</span><div id="t1"></div></div><p class="note">Yang–Mills and Navier–Stokes have the same scalar coupling sum (1.7428669168860038): in the scalar engine they are not distinguished; NS is the Im = 0 restriction. QM and Riemann also share one value (4.98963325). Answer to "are facets the 15 imaginary components?": in these lifts no. A facet is a value of the real scalar sigma_riemann; the 15 imaginary components set the direction and, through τ, the size of the current balance.</p>""",
    """const sf=D.scalar_facets_from_code;L.bars($('c1'),Object.entries(sf).map(([k,v])=>({label:k.replace('facet_',''),v})),{ylabel:'coupling sum (20 primes)',title:'coupling sums from h_rb_hat.maths facet_*'});
L.table($('t1'),['facet','sigma_riemann','τ','α','β','|C|','|ad| size (Frobenius)'],D.facets.map(f=>[f.facet,f.sigma_riemann.toFixed(4),f.tau_label,f.alpha.toFixed(5),f.beta.toFixed(5),f.modulus.toFixed(5),f.asym_fro.toFixed(5)]));"""))

# ───────────────────────────── A. the operator (scalar engine) ─────────────────────────────
P.append(page("coupling_convergence", "A2", "Coupling-sum convergence per facet",
    "Partial sums of Σ p^(−sigma_riemann) over the first 168 primes for each facet value. Convergent for sigma_riemann > 1; the sum at ½ keeps growing like 2√x/ln x.",
    fig("c1", "A2"), """const ks=Object.keys(D.partial_sums);L.lines($('c1'),ks.map(k=>({name:k,x:D.partial_sums[k].map((_,i)=>i+1),y:D.partial_sums[k]})),{logy:true,xlabel:'number of primes',ylabel:'partial sum',title:'Σ_{p≤p_n} p^(−sigma_riemann)',aspect:0.55});"""))

P.append(page("term_explorer", "A3", "Term-by-term explorer",
    "One term of the scalar Ĥ_RB at prime p is p^(−sigma_riemann)·[E_red + E_blue]. Move sigma_riemann: the red and blue contributions of each prime change together, by the same factor.",
    '<p>sigma_riemann = <input type="range" id="sl" min="-0.5" max="3" step="0.01" value="0.5"> <b id="sv">0.50</b></p>' + fig("c1", "A3") + '<p class="note">E_red = x·p_momentum and E_blue = ½p² + ℘(x; g₂=1, g₃=0) at x = 1, p_momentum = 1 (red 1.0, blue 1.5508). Both are multiplied by the same p^(−sigma_riemann), so their ratio does not depend on sigma_riemann (page B2).</p>',
    """const pr=D.constants.primes,Er=1.0,Eb=D.energies.find(e=>Math.abs(e[0]-1)<1e-9)[2];
function d(){const s=+$('sl').value;$('sv').textContent=s.toFixed(2);L.lines($('c1'),[{name:'red term',x:pr,y:pr.map(p=>Math.pow(p,-s)*Er)},{name:'blue term',x:pr,y:pr.map(p=>Math.pow(p,-s)*Eb)}],{logy:true,ymin:1e-4,ymax:1e4,xlabel:'prime p',ylabel:'term',title:'p^(−sigma_riemann)·E at x=1, p_momentum=1',aspect:0.5});}
$('sl').oninput=d;d();"""))

P.append(page("red_vs_blue", "A4", "R̂ against B̂: xp against ½p² + ℘",
    "The two energies of the scalar engine at p_momentum = 1: Red is the Berry–Keating xp, Blue is ½p² plus the Weierstrass ℘ (g₂ = 1, g₃ = 0), which has poles at the lattice points.",
    fig("c1", "A4"), """L.lines($('c1'),[{name:'E_red = x·p',x:D.energies.map(e=>e[0]),y:D.energies.map(e=>e[1])},{name:'E_blue = ½p² + ℘(x)',x:D.energies.map(e=>e[0]),y:D.energies.map(e=>e[2])}],{ymin:-4,ymax:25,xmin:-3,xmax:3,xlabel:'x',ylabel:'energy',title:'E_red and E_blue',aspect:0.5});"""))

P.append(page("reflection", "A5", "The reflection: sigma_riemann ↔ 1 − sigma_riemann",
    "R̂† = B̂ is the operator form of ξ(s) = ξ(1−s). The coupling sum at sigma_riemann and at 1 − sigma_riemann are mirror images about ½; the two curves cross at sigma_riemann = ½, value 4.98963.",
    fig("c1", "A5") + '<p class="note">The functional equation s ↦ 1−s is an involution (ℤ₂), a discrete symmetry; its fixed set is sigma_riemann = ½ (Ainulindale wiki 99 §1).</p>',
    """L.lines($('c1'),[{name:'Σ p^(−s)',x:D.reflection.map(r=>r[0]),y:D.reflection.map(r=>r[1])},{name:'Σ p^(−(1−s))',x:D.reflection.map(r=>r[0]),y:D.reflection.map(r=>r[2]),dash:[5,4]}],{xlabel:'sigma_riemann',ylabel:'coupling sum (20 primes)',title:'sums at s and 1 − s',aspect:0.5,after:(F)=>L.vline(F,0.5,'sigma_riemann = ½','--c2')});"""))

P.append(page("phase_diagram", "A6", "The sigma_riemann phase diagram",
    "Which sigma_riemann projects which theory, with the Euler-product magnitude along the axis (from h_rb_hat.sigma_phase_diagram, 120 points).",
    fig("c1", "A6") + '<div class="fig"><span class="imgno">A6b</span><div id="t1"></div></div>',
    """const pd=D.phase_diagram;L.lines($('c1'),[{name:'|Euler product|',x:pd.map(r=>r.sigma),y:pd.map(r=>r.euler_mag)}],{logy:true,xlabel:'sigma_riemann',ylabel:'|Π(1−p^(−s))^(−1)|, 20 primes',title:'Euler product magnitude',aspect:0.5,after:(F)=>{L.vline(F,0.5,'½','--c2');L.vline(F,1,'1','--c3');L.vline(F,2,'2','--c4');}});
const seen=[];pd.forEach(r=>{if(!seen.length||seen[seen.length-1][0]!==r.theory)seen.push([r.theory,r.sigma,r.sigma]);else seen[seen.length-1][2]=r.sigma;});L.table($('t1'),['theory','from','to'],seen.map(s=>[s[0],s[1].toFixed(3),s[2].toFixed(3)]));"""))

# ───────────────────────────── B. currents ─────────────────────────────
P.append(page("currents", "B1", "J_red and J_blue as paired currents (lift A)",
    "In lift A the two Noether-type currents are J_red = C·E_red and J_blue = C·E_blue. Their difference and sum carry the same factor C(sigma_rb).",
    fig("c1", "B1") + '<p class="note">J_red + J_blue is the torque of the precession picture; J_red − J_blue is the piston. Under lift A both scale with C and their ratio E_red/E_blue = 0.6448 is fixed.</p>',
    """const pr=D.constants.primes,Er=1.0,Eb=D.energies.find(e=>Math.abs(e[0]-1)<1e-9)[2],S=(s)=>pr.reduce((a,p)=>a+Math.pow(p,-s),0),xs=[...Array(141)].map((_,i)=>-0.5+i*0.025);
L.lines($('c1'),[{name:'J_red',x:xs,y:xs.map(s=>S(s)*Er)},{name:'J_blue',x:xs,y:xs.map(s=>S(s)*Eb)},{name:'J_red + J_blue',x:xs,y:xs.map(s=>S(s)*(Er+Eb)),dash:[4,3]}],{logy:true,xlabel:'sigma_riemann',ylabel:'current',title:'lift A currents at x=1, p_momentum=1',aspect:0.5,after:(F)=>L.vline(F,0.5,'½','--fg')});"""))

P.append(page("amgm_balance", "B2", "The scalar balance does not depend on sigma_riemann",
    "sigma_rb_term returns balance = E_red − E_blue and a flag 'self_adjoint' meaning |balance| < 10⁻¹⁰, and its docstring says the balance is zero on the critical line. The number does not contain sigma_riemann at all.",
    fig("c1", "B2") + '<p class="note"><b>Finding (CALCULATED, new): the docstring claim cannot hold</b>, because balance is computed from x and p_momentum only; AM = GM of (J_red, J_blue) is likewise either true at every sigma_riemann or at none. Recorded as VQ-9 in the findings ledger; the code is not changed in this pass.</p>',
    """L.lines($('c1'),[{name:'balance, p=2, x=1, p_mom=1',x:D.balance_scalar.map(b=>b[0]),y:D.balance_scalar.map(b=>b[1])},{name:'balance, p=5, x=0.3, p_mom=2',x:D.balance_scalar.map(b=>b[0]),y:D.balance_scalar.map(b=>b[2])}],{xlabel:'sigma_riemann',ylabel:'E_red − E_blue',title:'the balance is flat in sigma_riemann',aspect:0.5,after:(F)=>L.vline(F,0.5,'½','--c2')});"""))

P.append(page("x9_integrand", "B3", "The L_(I|O) integrand: J_red·J_blue is constant",
    "Ledger item X-9: with J_red = e^(−(1−sigma_riemann)E) and J_blue = e^(−sigma_riemann·E) the product is e^(−E) for every sigma_riemann, so the integral is e^(−E)·path length and the claimed maximum at ½ does not follow.",
    fig("c1", "B3") + '<p class="note">E = 2 here. The product is the flat line e^(−2) = 0.1353. A path-dependent integrand is still to be settled (Ainulindale wiki 135 X-9).</p>',
    """L.lines($('c1'),[{name:'J_red = e^(−(1−s)E)',x:D.x9.map(r=>r[0]),y:D.x9.map(r=>r[2])},{name:'J_blue = e^(−sE)',x:D.x9.map(r=>r[0]),y:D.x9.map(r=>r[3])},{name:'J_red·J_blue',x:D.x9.map(r=>r[0]),y:D.x9.map(r=>r[1]),dash:[5,4]}],{xlabel:'sigma_riemann',ylabel:'current',title:'E = 2',aspect:0.5,after:(F)=>L.vline(F,0.5,'½','--fg')});"""))

P.append(page("crank", "B4", "The oblique crank and the precession stroke",
    "The Witches Hat half-angle is the crank throw θ = arctan(d*) at the working value d* = 0.246, 13.8203°. One cycle I→O→I is one precession revolution; ω = (J_red + J_blue)/L_(I|O).",
    '<div class="fig"><span class="imgno">B4</span><svg id="sv" viewBox="0 0 700 360" style="width:100%"></svg></div><p class="note">Effective torque τ_eff = τ·d*/√(1+d*²). The page uses only the working d*.</p>',
    """const th=Math.atan(0.246),cx=120,cy=300,R=250,fg=L.css('--fg'),c1=L.css('--c1'),c2=L.css('--c2');
$('sv').innerHTML=`<line x1="${cx}" y1="${cy}" x2="${cx}" y2="30" stroke="${fg}" stroke-width="2"/><line x1="${cx}" y1="${cy}" x2="${cx+R*Math.sin(th)*1.0}" y2="${cy-R*Math.cos(th)}" stroke="${c2}" stroke-width="3"/><path d="M ${cx} ${cy-90} A 90 90 0 0 1 ${cx+90*Math.sin(th)} ${cy-90*Math.cos(th)}" fill="none" stroke="${c1}" stroke-width="2"/><text x="${cx+100}" y="${cy-95}" fill="${c1}" font-size="15">θ = arctan(d*) = ${(th*180/Math.PI).toFixed(4)}°</text><text x="${cx+10}" y="40" fill="${fg}" font-size="14">axis (real e₀)</text><text x="${cx+170}" y="110" fill="${c2}" font-size="14">hat axis (oblique crank)</text><text x="340" y="250" fill="${fg}" font-size="14">ω_prec = (J_red + J_blue) / L_(I|O)</text><text x="340" y="275" fill="${fg}" font-size="14">τ_eff = τ·d*/√(1+d*²) = τ·${(0.246/Math.sqrt(1+0.246*0.246)).toFixed(5)}</text>`;"""
    , kind="svg"))

# ───────────────────────────── C. Navier–Stokes ─────────────────────────────
P.append(page("ns_vs_hrb", "C1", "Navier–Stokes against Ĥ_RB",
    "In h_rb_hat the Navier–Stokes facet is sigma_riemann = 1 with Im = 0 and has the same coupling sum as Yang–Mills. Under lift B the real axis has β = 0 (Ĥ_RB = Ĥ_BR); the Yang–Mills facet is the same sigma_riemann with imaginary content. This page overlays the two.",
    fig("c1", "C1") + """<div class="fig"><span class="imgno">C1b</span><div id="t1"></div></div><p class="note">The only difference between the NS and YM facets in this lift is the imaginary part: NS has zero current balance, YM at τ ≠ 0 has β(τ) as drawn. Where in Ĥ_RB Navier–Stokes is found is the question equation space (later) is for; this page fixes what the difference is in the present definition, it does not locate NS.</p>""",
    """const P=D.plane_p20,j=P.sigma_riemann.findIndex(s=>Math.abs(s-1)<1e-9),bet=P.tau.map((_,i)=>P.beta[i][j]);
L.lines($('c1'),[{name:'YM: β(τ) at sigma_riemann=1',x:P.tau,y:bet},{name:'NS: Im = 0 (β ≡ 0)',x:P.tau,y:P.tau.map(()=>0),dash:[5,4]}],{xlabel:'τ = |Im sigma_rb|',ylabel:'β (J_red + J_blue coefficient)',title:'difference between the facets at sigma_riemann = 1',aspect:0.5});
const sf=D.scalar_facets_from_code;L.table($('t1'),['quantity','value'],[['facet_yang_mills coupling sum',sf.facet_yang_mills],['facet_navier_stokes coupling sum',sf.facet_navier_stokes],['difference',sf.facet_yang_mills-sf.facet_navier_stokes]]);"""))

P.append(page("halocline_reference", "C2", "Interface profile: the difference field against a shear-layer reference",
    "The halocline question: is the difference between the Navier–Stokes and Ĥ_RB shapes a localized interface? The difference field in lift B is |β(τ)| at sigma_riemann = 1. A tanh shear layer is drawn as a reference shape only.",
    fig("c1", "C2") + '<p class="note">The reference is not a fit and not a claim. In lift B the difference field oscillates over the whole τ range (it is a sum of 20 oscillations) and is not localized like a tanh layer. A localized interface, if one exists, is not in this definition of the difference; a different definition would be a new test.</p>',
    """const P=D.plane_p20,j=P.sigma_riemann.findIndex(s=>Math.abs(s-1)<1e-9),b=P.tau.map((_,i)=>Math.abs(P.beta[i][j])),m=Math.max(...b);
L.lines($('c1'),[{name:'|β(τ)| / max',x:P.tau,y:b.map(v=>v/m)},{name:'reference: ½(1+tanh((τ−20)/3))',x:P.tau,y:P.tau.map(t=>0.5*(1+Math.tanh((t-20)/3))),dash:[5,4]}],{xlabel:'τ',ylabel:'normalised',title:'difference field and a shear-layer shape',aspect:0.5});"""))

# ───────────────────────────── D. Chladni / hypercomplex Laplacian ─────────────────────────────
P.append(page("stability_496", "D1", "The 496-bond stability map of T₃₂ (regenerated from the engine)",
    "Each of the C(32,2) = 496 composite elements e_i+e_j is multiplied by every other in T₃₂/GF(2); the colour is the popcount of the product, the distance from the zero-divisor locus (0 = exact zero divisor). Reproduced from TuringStack/hypercomplex_laplacian.py.",
    fig("c1", "D1") + '<p class="note" id="n1"></p>',
    """const Z=D.chladni_496.popcount;let zc=0;Z.forEach(r=>r.forEach(v=>{if(v===0)zc++;}));$('n1').textContent='Exact zero-divisor bonds: '+zc+' of '+(Z.length*Z.length)+' (the TuringStack figure legend reports 7,440; this regeneration counts every ordered pair with product 0, the diagonal included, and the difference has not been traced).';
L.heat($('c1'),Z,{xmin:0,xmax:496,ymin:0,ymax:496,xlabel:'composite index b',ylabel:'composite index a',title:'popcount of e_a·e_b in T₃₂/GF(2)',aspect:1,zmin:0,zmax:4});""",
    [("../TuringStack/sha1_chladni_stability.py", "the original figure"), ("../TuringStack/hypercomplex_laplacian.py", "t32_mul, trace_laplacian")]))

P.append(page("chladni_scales", "D2", "The Laplacian across Cayley–Dickson scales",
    "Null-space dimension of L_w and the nilpotent fraction at each CD scale (4, 8, 16, 32), with the n-ball volume V(n). Sample: all elements for dim ≤ 16 where feasible, random for 32.",
    fig("c1", "D2") + '<div class="fig"><span class="imgno">D2b</span><div id="t1"></div></div>',
    """const S=D.chladni_scales;L.lines($('c1'),[{name:'mean nullity / dim',x:S.map(s=>s.dim),y:S.map(s=>s.mean_nullity/s.dim)},{name:'nilpotent fraction',x:S.map(s=>s.dim),y:S.map(s=>s.nilpotent_fraction),dash:[5,4]}],{xlabel:'CD dimension',ylabel:'fraction',title:'zero-divisor access with scale',aspect:0.5,xmin:4,xmax:32});
L.table($('t1'),['dim','mean nullity of L_w','nilpotent fraction','V(n)=π^(n/2)/Γ(n/2+1)'],S.map(s=>[s.dim,s.mean_nullity.toFixed(3),s.nilpotent_fraction.toFixed(3),s.V_n.toExponential(3)]));""",
    [("../TuringStack/hypercomplex_laplacian.py", "spectral_profile, multiscale_spectrum")]))

P.append(page("trace_laplacian_sha1", "D3", "Trace-Laplacian of the SHA-1 constants",
    "Δ(w) = w·0xFFFFFFFF is zero exactly when w is nilpotent. The five IV constants have spectral distance 0; the four round constants have distance 32.",
    '<div class="fig"><span class="imgno">D3</span><canvas id="c1"></canvas></div><div class="fig"><span class="imgno">D3b</span><div id="t1"></div></div>',
    """const R=D.sha1;L.table($('t1'),['constant','value','spectral distance'],R.map(r=>[r.name,'0x'+(r.w>>>0).toString(16).toUpperCase().padStart(8,'0'),r.dist]));
function draw(){const cv=$('c1'),w=cv.parentElement.clientWidth,h=R.length*26+20,dpr=window.devicePixelRatio||1;cv.style.width=w+'px';cv.style.height=h+'px';cv.width=w*dpr;cv.height=h*dpr;const g=cv.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);g.fillStyle=L.css('--card');g.fillRect(0,0,w,h);
R.forEach((r,i)=>{const bw=(w-180)/32;g.fillStyle=L.css('--fg');g.font='13px monospace';g.fillText(r.name,10,i*26+20);r.bits.slice().reverse().forEach((b,k)=>{g.fillStyle=b?L.css(r.dist===0?'--c2':'--c1'):L.css('--line');g.fillRect(50+k*bw,i*26+6,bw-1,18);});g.fillStyle=L.css('--fg');g.fillText('dist '+r.dist,50+32*bw+8,i*26+20);});}
draw();window.addEventListener('resize',draw);""",
    [("../TuringStack/hypercomplex_laplacian.py", "trace_laplacian"), ("../TuringStack/UDEO_Cryptographic_Vulnerability.md", "the white paper")], ["Stevens, M. et al. (2017). The first collision for full SHA-1. CRYPTO 2017, LNCS 10401, 570–596."]))

# ───────────────────────────── E. monad / oblique gear ─────────────────────────────
P.append(page("tilt_axis", "R1", "The documented map: sigma_rb[k] = ψ[k]·conj ψ[k⊕4], tilt and axis",
    "The sedenion input ψ (16 components, real or complex) goes in; the sedenion sigma_rb (16 components) comes out. sigma_rb[k⊕4] = conj sigma_rb[k] exactly, so the real part (sigma_rb_tilt, ⊕4-even, the driven part) and the imaginary part (sigma_rb_axis, ⊕4-odd, the conserved anchor) are two 8-vectors. Sixteen components carry eight values. This is the seed-20260831 input of oblique_gear_test.py; the numbers match its recorded output.",
    fig("c1", "R1") + fig("c2", "R1b") + '<p class="note" id="n1"></p>',
    """const T=D.sigma_rb_tilt_axis;$('n1').textContent='Pairing residual max|sigma_rb[k⊕4] − conj sigma_rb[k]| = '+T.conj_pair_resid+'; sigma_self = '+T.sigma_self.toFixed(5)+' (random ψ).';
L.bars($('c1'),T.re.map((v,k)=>({label:''+k,v})),{xlabel:'k',ylabel:'Re',title:'sigma_rb_tilt = Re sigma_rb[k] (⊕4-even)'});L.bars($('c2'),T.im.map((v,k)=>({label:''+k,v})),{xlabel:'k',ylabel:'Im',title:'sigma_rb_axis = Im sigma_rb[k] (⊕4-odd)'});"""))

# ───────────────────────────── F. repo-wide ─────────────────────────────
P.append(page("census", "F1", "Where Ĥ_RB appears: reference census by repository",
    "Pattern counts of Ĥ_RB / h_rb_hat, 0_RB, Σ_RB / sigma_rb names and J_red / J_blue across the repositories (docs/HRB_REFERENCE_CENSUS.md). Archives, worktrees and build output excluded.",
    fig("c1", "F1") + '<div class="fig"><span class="imgno">F1b</span><div id="t1"></div></div>',
    """const C=D.census,ks=Object.keys(C).sort((a,b)=>C[b].H-C[a].H);L.bars($('c1'),ks.slice(0,14).map(k=>({label:k.slice(0,9),v:C[k].H})),{ylabel:'Ĥ_RB name mentions',title:'Ĥ_RB mentions, top repositories',aspect:0.45});
L.table($('t1'),['repo','files','code','notebooks','docs','Ĥ_RB','0_RB','sigma_rb names','J'],ks.map(k=>[k,C[k].files,C[k].code,C[k].notebook,C[k].doc,C[k].H,C[k].Z,C[k].S,C[k].J]));""",
    [("docs/HRB_REFERENCE_CENSUS.md", "the per-file census")]))

P.append(page("dependency_flow", "F2", "Dependency flow of h_rb_hat",
    "h_rb_hat feeds five engines in ValaQuenta and is carried, by the propagation tool, to eight repositories.",
    '<div class="fig"><span class="imgno">F2</span><svg id="sv" viewBox="0 0 900 380" style="width:100%"></svg></div>',
    """const E=D.deps,fg=L.css('--fg'),c1=L.css('--c1'),c2=L.css('--c2'),line=L.css('--line');let s=`<rect x="360" y="150" width="180" height="50" rx="10" fill="none" stroke="${c2}" stroke-width="2.5"/><text x="450" y="181" text-anchor="middle" fill="${fg}" font-size="16">h_rb_hat</text>`;
E.h_rb_hat.forEach((m,i)=>{const y=20+i*70;s+=`<rect x="20" y="${y}" width="220" height="40" rx="8" fill="none" stroke="${c1}"/><text x="130" y="${y+25}" text-anchor="middle" fill="${fg}" font-size="14">${m}</text><path d="M240 ${y+20} L360 175" stroke="${line}" fill="none"/>`;});
E.downstream_repos.forEach((m,i)=>{const y=10+i*45;s+=`<rect x="660" y="${y}" width="220" height="34" rx="8" fill="none" stroke="${c1}"/><text x="770" y="${y+22}" text-anchor="middle" fill="${fg}" font-size="14">${m}</text><path d="M540 175 L660 ${y+17}" stroke="${line}" fill="none"/>`;});
s+=`<text x="130" y="372" text-anchor="middle" fill="${fg}" font-size="13">imports h_rb_hat</text><text x="770" y="376" text-anchor="middle" fill="${fg}" font-size="13">carried by tools/propagate.py</text>`;$('sv').innerHTML=s;""", kind="svg"))

P.append(page("sigma_collisions", "F3", "The sigma disambiguation matrix",
    "Every sigma carries its own name. Searching for a bare sigma pulls the wrong context; search for the token.",
    '<div class="fig"><span class="imgno">F3</span><div id="t1"></div></div>',
    """L.table($('t1'),['written','token','meaning','engines (seen)'],[
['σ_ζ','sigma_riemann','Re s, the Dirichlet/Euler exponent; critical line ½','h_rb_hat, tier7_cosmos, berry_keating'],
['σ_RB (16-component input)','sigma_rb','real scalar sigma_riemann plus 15 imaginary components','h_rb_hat/sigma16.py'],
['σ_RB tilt / axis','sigma_rb_tilt, sigma_rb_axis','Re and Im of ψ[k]·conj ψ[k⊕4]','oblique_gear, VAPMIP monads'],
['σ_self','sigma_self','red/(red+blue), a derived scalar','VAPMIP'],
['σ_val','sigma_valuation','the σ-valuation and σ-faces','Ainulindale SIGMA_VALUATION_FULL'],
['σ-stratum','sigma_stratum','σ₀…σ₄ nested inclusion levels (σ₄ = string / ground state)','box_kite, Ainulindale wiki'],
['σ_exp','sigma_expansion','the σ-expansion engine','sigma_expansion'],
['σ_cav','sigma_cavitation','the cavitation library','sigma_cavitation'],
['σ_std','sigma_std, stdev','standard deviation','bell_curve'],
['σ_Pauli','sigma_pauli_x…','Pauli matrices (code names sigma_x/y/z: rename queued)','tier6_physics']]);"""))

P.append(page("pending", "—", "Not built yet, and why",
    "Visualizations proposed for Ĥ_RB that need data or a decision first.",
    '<div class="fig"><span class="imgno">—</span><div id="t1"></div></div>',
    """L.table($('t1'),['proposal','blocked on'],[
['Vortex lattice (Abrikosov Tree) against the Navier–Stokes vortex field','a vortex-field dataset from AbrikosovTree, mapped to sigma_riemann and τ'],
['Regularity (blow-up) indicator against the coupling sum','an NS dataset; none is in the repositories'],
['Ĥ_RB → 0_RB rename timeline','first-commit dates per file (git history) and the decided rename map'],
['Box-kite / Fano view of the three channels','the channel assignment of Red, Green and Blue onto the Fano lines (author to state)'],
['Chladni nodal-line pictures at scales 4, 8, 16, 64','a vectorised T_n product (the 32D map above is built; other scales next)'],
['String-theory observable at Δ','a stated observable to compute; the two lifts define none']]);"""))


# ───────────────────────────── R. the documented sigma_rb map ─────────────────────────────
P.append(page("split_1_7", "R2", "The 1 + 7 split: one kept scalar, seven struts",
    "Each 8-vector is its mean (the kept scalar, the point-shadow sigma_self reads) plus seven struts (the residual). The seven are what the scalar discards and what a path recovers piece by piece.",
    fig("c1", "R2") + fig("c2", "R2b") + '<p class="note" id="n1"></p>',
    """const S=D.doc.split_1_7;$('n1').textContent='tilt mean = '+S.tilt_mean.toFixed(5)+', axis mean = '+S.axis_mean.toFixed(5)+' (seed '+D.doc.seed+')';
L.bars($('c1'),S.tilt_struts.map((v,k)=>({label:'strut '+k,v})),{title:'sigma_rb_tilt minus its mean (7 independent struts)',ylabel:'tilt'});L.bars($('c2'),S.axis_struts.map((v,k)=>({label:'strut '+k,v})),{title:'sigma_rb_axis minus its mean',ylabel:'axis'});"""))

P.append(page("pair_planes", "R3", "Cycling through the sedenion: single components and ⊕4 pairs",
    "A lone component ψ = e_k has no partner, so sigma_rb = 0 and sigma_self = ½: every basis element sits at the critical-line value. Two members of a ⊕4 pair, in phase, give sigma_self = 1; in antiphase, sigma_self = 0; sigma_rb has support on exactly that pair.",
    '<div class="fig"><span class="imgno">R3</span><div id="t1"></div></div><div class="fig"><span class="imgno">R3b</span><div id="t2"></div></div>',
    """L.table($('t1'),['ψ = e_k','max |sigma_rb|','sigma_self'],D.doc.single.map(s=>['e'+s.k,s.max_sigma_rb,s.sigma_self]));
L.table($('t2'),['pair','phase','nonzero components of sigma_rb','tilt of the pair','sigma_self'],D.doc.pairs.map(s=>[s.pair,s.phase,JSON.stringify(s.nonzero),s.tilt_j.toFixed(4),s.sigma_self]));"""))

P.append(page("gear_rotation", "R4", "Gear rotation: the axis is invariant, the tilt is driven",
    "Rotate one ⊕4 plane by θ. The axis of that pair does not change (it is what the gear turns around); the tilt follows cos2θ·tilt + ½ sin2θ·(|ψ_j|² − |ψ_{j⊕4}|²).",
    fig("c1", "R4") + '<p class="note">Solid: tilt computed from the rotated ψ. Dashed: the law. They coincide to 5×10⁻¹⁶ (test T3 of oblique_gear_test.py, ported to tests/test_h_rb_hat_oblique.py).</p>',
    """const G=D.doc.gear;L.lines($('c1'),[{name:'tilt (computed)',x:G.theta,y:G.tilt_j},{name:'cos2θ·tilt + ½ sin2θ·Δ|ψ|²',x:G.theta,y:G.law,dash:[5,4]},{name:'axis (computed)',x:G.theta,y:G.axis_j}],{xlabel:'θ',ylabel:'pair 2',title:'one gear turned through 2π',aspect:0.5});"""))

P.append(page("sigma_self_law", "R5", "sigma_self = ½ + Σ tilt / (p_red + p_blue)",
    "300 random complex ψ: sigma_self computed from the red and blue energies against the closed form. sigma_self = ½ exactly when the tilts sum to zero.",
    fig("c1", "R5") + '<p class="note">All 300 points lie on the diagonal (test T4).</p>',
    """const R=D.doc.sigma_self_law;L.lines($('c1'),[{name:'sigma_self computed',x:R.map(r=>r[0]),y:R.map(r=>r[1])},{name:'diagonal',x:R.map(r=>r[0]),y:R.map(r=>r[0]),dash:[5,4]}],{xlabel:'½ + Σ tilt / (p_red + p_blue)',ylabel:'sigma_self',title:'300 random psi',aspect:0.5,after:(F)=>{L.vline(F,0.5,'½','--c2');L.hline(F,0.5,'','--c2');}});"""))

P.append(page("balance_sweep", "R6", "Balancing the gear: Σ tilt goes to 0 while the axis stays",
    "Rotate every pair a fraction λ of the way to its zero-tilt angle. Σ tilt falls to 0 and sigma_self reaches ½; |axis| is constant to 10⁻⁹ (test T6).",
    fig("c1", "R6"), """const S=D.doc.balance_sweep;L.lines($('c1'),[{name:'Σ tilt',x:S.map(r=>r[0]),y:S.map(r=>r[1])},{name:'|axis|',x:S.map(r=>r[0]),y:S.map(r=>r[2])},{name:'sigma_self',x:S.map(r=>r[0]),y:S.map(r=>r[3])}],{xlabel:'λ (fraction of the way to balance)',ylabel:'value',title:'seed 7',aspect:0.5});"""))

P.append(page("strut_blind_delta", "R7", "Feeding the onset residual into the tilt: sigma_self = ½ + Δ/E",
    "Wiki 123: type Δ = A_π − d*·ln10 = 0.000707357533 into sigma_rb_tilt as the mean across the 8 struts, with each pair energy E fixed. sigma_self is strut-blind: ½ + Δ/E whatever the distribution of the tilt across the struts. The result lies on the sigma_riemann = ½ facet, not at string theory; the string / M-theory route is the sigma-stratum argument (wiki 25 §VII), a separate object.",
    '<div class="fig"><span class="imgno">R7</span><div id="t1"></div></div><div class="fig"><span class="imgno">R7b</span><div id="t2"></div></div>',
    """const S=D.doc.strut_blind;L.table($('t1'),['distribution','strut spread','sigma_self from red/(red+blue)','½ + Δ/E'],S.trials.map((r,i)=>['#'+i,r.spread.toFixed(4),r.sigma_self.toFixed(12),r.half_plus_delta.toFixed(12)]));
L.table($('t2'),['pair energy E','½ + Δ/E'],S.by_energy.map(r=>[r[0],r[1].toFixed(12)]));"""))

P.append(page("rectifier_law", "R8", "The rectifier law",
    "For the energy-unnormalised embedding, sigma_self = ½ + 4Δ/Σ|Δ + λ·u_k|. Below the first sign flip the struts are invisible and sigma_self = 1; above it the deviation falls as 1/λ (slope −1).",
    fig("c1", "R8"), """const R=D.doc.rectifier;L.lines($('c1'),[{name:'embedding',x:R.map(r=>r[0]),y:R.map(r=>r[1]-0.5)},{name:'closed form',x:R.map(r=>r[0]),y:R.map(r=>r[2]-0.5),dash:[5,4]}],{logx:true,logy:true,xlabel:'λ (strut scale)',ylabel:'sigma_self − ½',title:'inverse first power at large λ',aspect:0.5,ymin:1e-6,ymax:1});"""))

P.append(page("saddle_flow", "R9", "The gear flow: σ_self = ½ is a saddle",
    "Drive the gear train by its own tilt (midpoint integrator). A generic ψ flows into balance (max |tilt| → 0). From exactly balanced, any perturbation grows exponentially: Lyapunov rate ≈ 6.1 per unit flow time (the 2026-08-31 anomaly chase recorded 6.1; reproduced here). |axis| is conserved on both branches.",
    fig("c1", "R9") + fig("c2", "R9b") + '<p class="note" id="n1"></p>',
    """const F=D.doc.flow,ks=Object.keys(F);$('n1').textContent='Lyapunov rate from balance: '+D.doc.lambda.toFixed(3)+' per unit flow time (record: 6.1, midpoint). Gain 0.0125, 400 steps.';
L.lines($('c1'),ks.map(k=>({name:k,x:F[k].max_abs_tilt.map((_,i)=>i),y:F[k].max_abs_tilt})),{logy:true,xlabel:'step',ylabel:'max |tilt|',title:'balanced + noise grows; generic decays',aspect:0.5,ymin:1e-12,ymax:10});
L.lines($('c2'),ks.map(k=>({name:k,x:F[k].axis_norm.map((_,i)=>i),y:F[k].axis_norm})),{xlabel:'step',ylabel:'|axis|',title:'the axis is conserved on both branches',aspect:0.4});"""))

# index
GROUPS = [("Code flow chart", ["FC1"]), ("The documented sigma_rb map: ψ (16) in, sigma_rb (16) out", ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9"]),
          ("Exploratory lifts (my own definitions on 2026-11-25, NOT the documented map)", ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]),
          ("A. The operator (scalar engine)", ["A2", "A3", "A4", "A5", "A6"]), ("B. J_red and J_blue", ["B1", "B2", "B3", "B4"]),
          ("C. Navier–Stokes against Ĥ_RB", ["C1", "C2"]), ("D. Chladni and the hypercomplex Laplacian", ["D1", "D2", "D3"]),
          ("F. Repository-wide", ["F1", "F2", "F3"]), ("Pending", ["—"])]
byno = {n: (fn, t) for fn, n, t in P}
byno["FC1"] = ("svg_flowchart_h_rb_hat.html", "Code flow chart: the h_rb_hat engine (derived from the source)")
cards = ""
for g, nos in GROUPS:
    cards += f"<h2>{html.escape(g)}</h2><div class='grid'>" + "".join(f"<div class='card'><span class='tag'>{n}</span><a href='{byno[n][0]}'>{html.escape(byno[n][1])}</a></div>" for n in nos) + "</div>"
idx = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>H_RB Data Gallery</title>
<link rel="icon" type="image/png" href="favicon.png"><style>{CSS}</style></head><body>{CONTACT}<header><h1>Ĥ_RB data gallery</h1>
<p class="lead">The Noether Current Operator (J_red the Noether current, J_blue the Noether information current; Ĥ_RB − Ĥ_BR = J_red + J_blue), drawn from the ValaQuenta engine <code>h_rb_hat</code>. Every number is produced by importing the engines (<code>gallery/hrb/experiments.py</code>); a picture shows a space or a machinery, it is not evidence.</p>
<p class="note"><b>What the documented sigma_rb map gives (R1–R9, CALCULATED; the numbers match the 2026-08-31 record):</b> (1) ψ in, sigma_rb out, two 8-vectors: tilt (Re, driven) and axis (Im, conserved), eight values in sixteen components. (2) A lone component is invisible to sigma_rb and sits at sigma_self = ½; a ⊕4 pair gives sigma_self 1 (in phase) or 0 (antiphase). (3) sigma_self = ½ + Σ tilt/(p_red + p_blue); feeding Δ = 0.000707 into the tilt gives ½ + Δ/E whatever the struts do, so it lands on the sigma_riemann = ½ facet. (4) σ_self = ½ is a saddle of the gear flow with Lyapunov rate ≈ 6.1. <b>The exploratory lifts (S1–S7) are not the documented map</b>; they found the 84 zero-divisor directions of the sedenion and no feature at Δ, and are kept only as exploratory data. The scalar balance E_red − E_blue of <code>sigma_rb_term</code> does not contain sigma_riemann (finding VQ-9).</p></header>
<main>{cards}{DSTAR}</main>{FOOT}</body></html>"""
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(idx)
open(os.path.join(HERE, "serve_gallery.sh"), "w").write('#!/bin/bash\n# Serve the H_RB gallery on loopback only. Stop with: pkill -f "http.server $PORT"\nPORT=${1:-8790}; DIR="$(cd "$(dirname "$0")" && pwd)"\ncurl -s -o /dev/null "http://127.0.0.1:$PORT/index.html" || { nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$DIR" >/dev/null 2>&1 & sleep 1; }\nxdg-open "http://127.0.0.1:$PORT/index.html" >/dev/null 2>&1\n')
os.chmod(os.path.join(HERE, "serve_gallery.sh"), 0o755)
print(len(P), "pages + index")
