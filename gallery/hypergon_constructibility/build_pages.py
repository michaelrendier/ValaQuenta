#!/usr/bin/env python3
"""build_pages.py -- writes the four canvas2d_*.html pages and index.html of the hypergon_constructibility gallery from one shared chrome, so the pages cannot drift.
Page logic is in the BODY/JS strings below.  Run:  python3 build_pages.py"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/michaelrendier"
SOURCES = [
    (f"{GH}/ValaQuenta/blob/main/modules/hypergon_constructibility/maths.py", "ValaQuenta/modules/hypergon_constructibility/maths.py", "the Python engine these pages port and check against (Gauss–Wantzel, the Niemeier gap, the Moonshine control)"),
    (f"{GH}/ValaQuenta/blob/main/modules/bell_curve/maths.py", "ValaQuenta/modules/bell_curve/maths.py", "nball_volume, nsphere_area, nball_peak: the Gamma function as the bookkeeping of a hypersphere"),
    (f"{GH}/ValaQuenta/blob/main/wiki/hypergon_constructibility.md", "ValaQuenta/wiki/hypergon_constructibility.md", "the engine's record page, Part 4 is the Niemeier gap"),
    (f"{GH}/Ainulindale/blob/main/wiki/77_hypergon_constructibility.md", "Ainulindale/wiki/77_hypergon_constructibility.md", "the narrative and the findings ledger rows X-64 to X-66"),
]
REFS = [
    ('C. F. Gauss, Disquisitiones Arithmeticae (1801), §VII; P. L. Wantzel, "Recherches sur les moyens de reconnaître si un Problème de Géométrie peut se résoudre avec la règle et le compas", J. Math. Pures Appl. 2 (1837) 366–372. Constructibility of the regular n-gon.', "https://eudml.org/doc/235309"),
    ('H.-V. Niemeier, "Definite quadratische Formen der Dimension 24 und Diskriminante 1", J. Number Theory 5 (1973) 142–178.', "https://doi.org/10.1016/0022-314X(73)90042-1"),
    ('J. H. Conway and N. J. A. Sloane, Sphere Packings, Lattices and Groups (Springer, 1999), ch. 16 and 18: the 24 Niemeier lattices and their Coxeter numbers; ch. 1: the volume of the n-ball.', "https://doi.org/10.1007/978-1-4757-6568-7"),
    ('A. P. Ogg, "Automorphismes de courbes modulaires", Séminaire Delange–Pisot–Poitou 16 (1974/75), exposé 7. The 15 primes dividing the order of the Monster.', "https://eudml.org/doc/110853"),
    ('A. N. Schellekens, "Meromorphic c = 24 conformal field theories", Commun. Math. Phys. 153 (1993) 159–185. The 71 holomorphic c = 24 theories.', "https://doi.org/10.1007/BF02096959"),
    ('P. J. Davis, "Leonhard Euler\'s Integral: A Historical Profile of the Gamma Function", Amer. Math. Monthly 66 (1959) 849–869.', "https://doi.org/10.1080/00029890.1959.11989422"),
    ('G. Veneziano, "Construction of a crossing-symmetric, Regge-behaved amplitude for linearly rising trajectories", Nuovo Cimento A 57 (1968) 190–197. The amplitude was Euler\'s beta function, Γ(a)Γ(b)/Γ(a+b).', "https://doi.org/10.1007/BF02824451"),
    ('H. Darmon and A. Granville, "On the equations z^m = F(x, y) and Ax^p + By^q = Cz^r", Bull. London Math. Soc. 27 (1995) 513–543; F. Beukers, "The Diophantine equation Ax^p + By^q = Cz^r", Duke Math. J. 91 (1998) 61–88. Where generalized Fermat meets the ADE (spherical) signatures.', "https://doi.org/10.1112/blms/27.6.513"),
    ("The Python Software Foundation, Python 3 documentation: math.lgamma, math.gamma.", "https://docs.python.org/3/library/math.html#math.lgamma"),
    ("OpenSCAD User Manual (camera, projection, multmatrix).", "https://openscad.org/documentation.html"),
    ("MDN Web Docs, Canvas API.", "https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API"),
]
CT = ('<div class="ct"><b>Michael Rendier</b> <a href="mailto:the.wandering.god@gmail.com">✉ the.wandering.god@gmail.com</a> · '
      '<a href="https://facebook.com/rendier" target="_blank" rel="noopener">Facebook</a> · <a href="https://orcid.org/0009-0007-7239-6760" target="_blank" rel="noopener">ORCID 0009-0007-7239-6760</a></div>')


def about_card(looking, read, shows, not_shows, numbers):
    """The information panel every visual carries."""
    return ('<div class="card"><b>About this visual</b>'
            f'<p><b>What you are looking at.</b> {looking}</p><p><b>How to read it.</b> {read}</p>'
            f'<p><b>What it shows.</b> {shows}</p><p><b>What it does not show.</b> {not_shows}</p><p><b>Numbers to check.</b> {numbers}</p></div>')


ABOUT = {
 "canvas2d_ring.html": about_card(
    "The sixteen basis positions e0 … e15 of the sedenions, one prime each (2, 3, 5, 7, …, 53), set round a ring. A position is a regular n-gon with n = its prime. Blue: that regular polygon can be built with straightedge and compass. Orange: it cannot (a hole).",
    "Click a position. The polygon of that prime is drawn on the right with its vertices, and the test is written out: Gauss–Wantzel says the regular n-gon is constructible exactly when φ(n), the count of numbers below n sharing no factor with it, is a power of 2. For a prime p that is when p − 1 is a power of 2. The box at the bottom tests any n.",
    "4 of the 16 are constructible: e0 = 2, e1 = 3, e2 = 5, e6 = 17. The other 12 are holes. Constructibility is the exception among primes: the next one beyond the table is 257, then 65,537, and the test with φ finds no other n up to 70,000.",
    "That a hole means anything for factoring: the engine tested that (the nilpotent-split conjecture) and it failed its control. The ring is a classification of 16 numbers by a fact from 1796–1837.",
    "constructible 4/16; for n ≤ 70,000 there are 139 constructible n ≥ 3 (the same count as the Python engine's <code>totient_constructibility_check</code>), none of them a prime beyond 3, 5, 17, 257, 65,537."),
 "canvas2d_niemeier_gap.html": about_card(
    "The 23 root systems of the Niemeier lattices: the ways to make an A/D/E root system of rank 24 whose pieces all share one Coxeter number h. Each tile is one root system, standing in the column of its h mod 16 (the sixteen sedenion places). Under the columns, the 15 Moonshine primes (those dividing the order of the Monster) stand in the column of p mod 16.",
    "Shaded columns are residues no tile reaches: the Niemeier gap. Switch the rank to see the same construction at another rank: the gap is a fact about 24 and 16, not about root systems in general. Switch Moonshine primes on to see them fall in the gap columns; the control card says how often a prime set of that size does that anyway.",
    "<b>Theorem</b> (proved in the engine): the gap is exactly {1, 11, 15}. An odd h forces every piece to be A(h−1), and then h−1 divides 24; so the odd h are 3, 5, 7, 9, 13, 25. The tiles are generated here, in the browser, from the defining condition and equal the Python engine's 23.",
    "That the gap is a Fermat 'forbidden zone': no definition of such a zone as a set of solutions of x^p + y^q = z^r is in code, so that reading stays THEORETICAL. And the Moonshine fill is not evidence: 68% of 14-prime subsets of the odd primes up to 71 also cover all three gap residues.",
    "23 root systems at rank 24; h in {2,…,10, 12, 13, 14, 16, 18, 22, 25, 30, 46}; gap {1, 11, 15}. Control: 7,904 of 11,628 subsets cover the gap (68.0%), 5,283 cover all eight odd residues (45.4%)."),
 "canvas2d_nball.html": about_card(
    "Two curves of one function. Top: the volume V and the surface area S of the unit ball in n dimensions, drawn for every real n, not only whole numbers. The Gamma function is what makes that possible: V = π^(n/2) / Γ(n/2 + 1) and S = 2π^(n/2) / Γ(n/2) = n·V. Bottom: |Γ(x)| on the real line, with its poles at 0, −1, −2, … marked in red.",
    "Marks on the top plot: the dimensions of the Cayley–Dickson tower (1, 2, 4, 8, 16) and the peaks. Hover for values. The slider gives V, S and Γ(n/2) at any n. At n = 2 the ball is the disc (V = π) and the sphere is the circle (S = 2π, with Γ(1) = 1): the circle is where the whole family starts to be recognisable.",
    "V peaks at n = 5.2569 (value 5.2778) and S at n = 7.2569 (value 33.16); after that both fall towards zero, so a 16-dimensional unit ball has volume 0.2353, less than the 2-disc. 5.257 is the 'n* = 5.257' of the RiemannHypothesisProof to-do list. The identity behind Γ: the Gaussian integral of e^(−|x|²) over n dimensions is (√π)^n, and in spherical coordinates it equals (S/2)·Γ(n/2).",
    "That Γ 'is' a hypersphere in a stronger sense than this identity, or that 5.257 matches anything in the sedenion tower: the match to the to-do list's number is noted and not derived. The poles are the places the integral ∫ t^(z−1) e^(−t) dt stops converging, and the function is continued past them; they carry real information (residues (−1)^k / k!) and are not noise.",
    "Peak V at n = 5.256946, V = 5.277768; peak S at n = 7.256946, S = 33.1612. V(1) = 2, V(2) = π, V(3) = 4π/3, V(8) = 4.0587, V(16) = 0.23533. Γ(1/2) = √π = 1.77245. The browser's Gamma agrees with Python's to 10 significant figures at 8 test points."),
 "canvas2d_frame3d.html": about_card(
    "A 3D Cartesian reference frame, orthographic, rotated by dragging: the OpenSCAD view of the same data. Scene A draws the n-ball in a coordinate system built from its own quantities: x = dimension n, y = volume V, z = area S, so every point of the curve lies on the surface z = n·y (faint lines). Scene B draws the Niemeier gap as bars: x = h mod 16, y = row (Niemeier root systems, Moonshine primes), z = how many.",
    "Drag to turn; wheel to zoom; the buttons give the canonical poses (front, top, right, iso); double-click resets. The gizmo in the corner is the frame: red x, green y, blue z. The scale cube is a bounding box with ticks. One orbit, no more: depth is read from the motion.",
    "Three dimensions are the whole budget of the frustum; the rest is colour. In A the colour is n; the peaks of V and S show as the highest points along y and z; the sedenion dimensions are marked. In B the empty first row at residues 1, 11, 15 is the gap, filled in the second row by Moonshine primes.",
    "A claim about natural constants beyond what the axes already are: the frame is built from V, S and n, with no fitted number in it. It does not make the gap or the peak meaningful; it only places them in one frame.",
    "The same data is rendered by OpenSCAD in <code>hypergon_frame.scad</code> (MODE 0 and 1) with the PNGs beside it. Scene A: the curve starts at (0, 1, 0) and passes (2, π, 2π)."),
}


def page(fname, title, sub, kind, body, script):
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
    refs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in REFS)
    out = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="hg.css">
<!-- SPDX-License-Identifier: GPL-3.0-only. {kind}: raw Canvas 2D, no libraries, no network. Code: hg.js. Data: hg_data.js, baked by build_data.py from the Python engines. Generated by build_pages.py. -->
</head><body>{CT}
<header><h1>{html.escape(title)}</h1><div class="sub">{sub} A picture shows a structure; it is not evidence that the structure means anything beyond its definition.</div><p><a href="index.html">← Hypergon constructibility gallery</a></p></header>
<main>{body}
{ABOUT[fname]}<div class="card"><span id="selfcheck" class="sub">running self-check…</span></div></main>
<footer><p><b>Code and data.</b> Everything shown is recomputed in the browser by <code>hg.js</code> and compared with the numbers the Python engines baked into <code>hg_data.js</code>.</p><ul>{src}</ul><p><b>Literature.</b></p><ul>{refs}</ul></footer>
<script src="hg_data.js"></script><script src="hg.js"></script><script>
{script}
HG.selfCheck();
</script></body></html>"""
    open(os.path.join(HERE, fname), "w", encoding="utf-8").write(out)


LEG = '<span class="sw" style="background:var(--nil)"></span>constructible<span class="sw" style="background:var(--inv)"></span>hole (not constructible)'

# ------------------------------------------------------------------ 1 ring
page("canvas2d_ring.html", "The sixteen hypergons: Gauss–Wantzel round the sedenion ring",
     "Positions e0 … e15 carry the primes 2 … 53. A regular n-gon is constructible when φ(n) is a power of 2; 4 of the 16 are.",
     "canvas2d_ring",
     f"""<div class="card"><div class="row">{LEG}</div><div class="row" style="align-items:flex-start"><canvas id="ring"></canvas><canvas id="poly"></canvas></div>
<div class="info mono pre" id="info">Click a position on the ring.</div></div>
<div class="card"><b>Any n.</b> <div class="row"><label>n <input id="n" type="number" min="3" max="99999999" value="257" style="width:9em"></label></div><div class="info mono pre" id="nout"></div></div>""",
     """
const D=HG.data,ring=document.getElementById('ring'),poly=document.getElementById('poly'),info=document.getElementById('info');let sel=-1;
const R=210,CX=250,CY=250,NR=27;
function pos(k){const a=-Math.PI/2+k*2*Math.PI/16;return[CX+R*Math.cos(a),CY+R*Math.sin(a)];}
function drawRing(){const g=HG.setup(ring,500,500),nil=HG.cvar('--nil'),inv=HG.cvar('--inv'),fg=HG.cvar('--fg'),mut=HG.cvar('--mut'),line=HG.cvar('--line'),acc=HG.cvar('--acc');
 g.strokeStyle=line;g.lineWidth=1;g.beginPath();g.arc(CX,CY,R,0,2*Math.PI);g.stroke();g.textAlign='center';g.textBaseline='middle';
 D.rows.forEach((r,k)=>{const[x,y]=pos(k);g.fillStyle=r.constructible?nil:inv;g.beginPath();g.arc(x,y,NR,0,2*Math.PI);g.fill();if(k===sel){g.strokeStyle=acc;g.lineWidth=4;g.stroke();}
  g.fillStyle='#fff';g.font='bold 15px system-ui';g.fillText(r.prime,x,y-4);g.font='11px system-ui';g.fillText(r.channel,x,y+11);});
 g.fillStyle=mut;g.font='13px system-ui';g.fillText('4 of 16 constructible',CX,CY-10);g.fillText('e0 at the top, clockwise',CX,CY+10);}
function drawPoly(){const g=HG.setup(poly,300,300),fg=HG.cvar('--fg'),mut=HG.cvar('--mut'),line=HG.cvar('--line'),nil=HG.cvar('--nil'),inv=HG.cvar('--inv');
 if(sel<0){g.fillStyle=mut;g.font='13px system-ui';g.textAlign='center';g.fillText('the regular p-gon appears here',150,150);return;}
 const p=D.rows[sel].prime,c=D.rows[sel].constructible;g.strokeStyle=line;g.beginPath();g.arc(150,150,125,0,2*Math.PI);g.stroke();
 g.strokeStyle=c?nil:inv;g.lineWidth=2;g.beginPath();for(let i=0;i<=p;i++){const a=-Math.PI/2+i*2*Math.PI/p,x=150+125*Math.cos(a),y=150+125*Math.sin(a);i?g.lineTo(x,y):g.moveTo(x,y);}g.stroke();
 g.fillStyle=c?nil:inv;for(let i=0;i<p;i++){const a=-Math.PI/2+i*2*Math.PI/p;g.beginPath();g.arc(150+125*Math.cos(a),150+125*Math.sin(a),3.5,0,2*Math.PI);g.fill();}
 g.fillStyle=fg;g.font='13px system-ui';g.textAlign='left';g.fillText('regular '+p+'-gon',8,16);}
function explain(n){const f=HG.factor(n),ph=HG.phi(n),c=HG.constructible(n);const pf=f.length?f.join(' × '):'';
 let s='n = '+n+'   =   '+(n<4?'(too small)':pf)+'\\nφ(n) = '+ph+(HG.isPow2(ph)?'  = 2^'+Math.log2(ph)+'  (a power of 2)':'  = '+HG.factor(ph).join(' × ')+'  (not a power of 2)')+'\\n';
 s+=(n>=3?(c?'constructible with straightedge and compass (Gauss–Wantzel)':'NOT constructible: φ(n) has an odd prime factor'):'');
 if(n>=3&&c){const fp=[...new Set(f.filter(x=>x>2))];s+='\\nn = 2^'+f.filter(x=>x===2).length+(fp.length?' × '+fp.join(' × ')+'  (distinct Fermat primes)':'');}
 return s;}
ring.addEventListener('pointerdown',e=>{const r=ring.getBoundingClientRect(),x=(e.clientX-r.left)*500/r.width,y=(e.clientY-r.top)*500/r.height;sel=-1;
 D.rows.forEach((row,k)=>{const[px,py]=pos(k);if(Math.hypot(px-x,py-y)<=NR)sel=k;});drawRing();drawPoly();if(sel>=0){const r=D.rows[sel];info.textContent=r.channel+'   p = '+r.prime+'\\n'+explain(r.prime);}else info.textContent='Click a position on the ring.';});
const nin=document.getElementById('n'),nout=document.getElementById('nout');function upd(){const n=Math.floor(+nin.value);nout.textContent=n>=3&&n<=99999999?explain(n):'enter an integer from 3 to 99,999,999';}
nin.oninput=upd;addEventListener('resize',()=>{drawRing();drawPoly();});drawRing();drawPoly();upd();
""")

# ------------------------------------------------------------------ 2 niemeier gap
page("canvas2d_niemeier_gap.html", "The Niemeier gap: Coxeter numbers modulo 16",
     "The 23 root systems of rank 24 with one Coxeter number h, in the column h mod 16. No tile ever lands in columns 1, 11, 15.",
     "canvas2d_niemeier_gap",
     """<div class="card"><div class="row"><label>rank <select id="rk"><option>8</option><option>12</option><option>16</option><option selected>24</option><option>32</option></select></label>
<label><input type="checkbox" id="ms" checked> Moonshine primes (the 15 primes dividing |Monster|)</label><span><span class="sw" style="background:var(--nil)"></span>root system<span class="sw" style="background:var(--inv)"></span>Moonshine prime<span class="sw" style="background:rgba(180,35,24,.25)"></span>gap column</span></div>
<canvas id="cv"></canvas><div class="info mono pre" id="info"></div></div>
<div class="card"><b>The control.</b> Is it surprising that the Moonshine primes fill the gap? Every 14-subset of the 19 odd primes up to 71 (the 14 odd Moonshine primes are one of them), counted exactly:<canvas id="ctl"></canvas><div class="info mono pre" id="cinfo"></div></div>
<div class="card"><b>The proof, as data.</b><div class="mono pre" id="proof"></div></div>""",
     """
const D=HG.data,cv=document.getElementById('cv'),info=document.getElementById('info'),rk=document.getElementById('rk'),ms=document.getElementById('ms');
const CW=58,X0=40,TH=21;function draw(){const rank=+rk.value,sys=HG.niemeier(rank),gap=HG.gapOf(sys,16),cols=Array.from({length:16},()=>[]);sys.forEach(s=>cols[s.h%16].push(s));
 const mx=Math.max(1,...cols.map(c=>c.length)),H=70+mx*(TH+3)+90,W=X0+16*CW+10,g=HG.setup(cv,W,H),nil=HG.cvar('--nil'),inv=HG.cvar('--inv'),fg=HG.cvar('--fg'),mut=HG.cvar('--mut'),line=HG.cvar('--line');
 g.textAlign='center';g.textBaseline='middle';g.font='12px system-ui';
 for(let r=0;r<16;r++){const x=X0+r*CW;if(gap.includes(r)){g.fillStyle='rgba(180,35,24,.22)';g.fillRect(x,28,CW-2,H-34);}g.fillStyle=mut;g.fillText('e'+r+' · '+r,x+CW/2-1,14);
  cols[r].sort((a,b)=>a.h-b.h).forEach((s,i)=>{const y=34+i*(TH+3);g.fillStyle=nil;g.fillRect(x+2,y,CW-6,TH);g.fillStyle='#fff';g.font='11px system-ui';g.fillText('h='+s.h,x+CW/2-1,y+TH/2);g.font='12px system-ui';});
  if(ms.checked&&rank===24){const ps=D.by_residue[r]||[],y0=34+mx*(TH+3)+22;ps.forEach((p,i)=>{g.fillStyle=inv;g.beginPath();g.arc(x+CW/2-1,y0+i*22,9,0,2*Math.PI);g.fill();g.fillStyle='#000';g.font='bold 10.5px system-ui';g.fillText(p,x+CW/2-1,y0+i*22);g.font='12px system-ui';});}}

 const odd=[...new Set(sys.filter(s=>s.h%2).map(s=>s.h))].sort((a,b)=>a-b);
 info.textContent='rank '+rank+': '+sys.length+' root systems with one Coxeter number (the 23 are the Niemeier lattices at rank 24)\\nh values: '+[...new Set(sys.map(s=>s.h))].join(', ')+'\\nresidues not reached: {'+gap.join(', ')+'}'+(rank===24?'   ← the Niemeier gap (Python engine: {'+D.gap.join(', ')+'})':'   (Python engine at this rank: {'+D.other_rank_gap[rank].join(', ')+'})')+'\\nodd h: '+odd.join(', ')+'   (each is A(h−1) repeated, so h−1 divides '+rank+')'+(ms.checked&&rank!==24?'\\n(Moonshine primes are drawn at rank 24 only)':'');}
cv.addEventListener('pointermove',e=>{const r=cv.getBoundingClientRect(),x=(e.clientX-r.left)*cv.width/r.width/(window.devicePixelRatio||1),y=(e.clientY-r.top)*cv.height/r.height/(window.devicePixelRatio||1),c=Math.floor((x-X0)/CW);if(c<0||c>15)return;
 const sys=HG.niemeier(+rk.value).filter(s=>s.h%16===c).sort((a,b)=>a.h-b.h),i=Math.floor((y-34)/(TH+3));cv.title=(i>=0&&i<sys.length)?sys[i].label+'  (h='+sys[i].h+', h mod 16 = '+c+')':'';});
rk.onchange=ms.onchange=draw;addEventListener('resize',draw);draw();
(function(){const c=D.control,g=HG.setup(document.getElementById('ctl'),700,110),nil=HG.cvar('--nil'),inv=HG.cvar('--inv'),fg=HG.cvar('--fg'),mut=HG.cvar('--mut'),line=HG.cvar('--line');g.font='12px system-ui';g.textBaseline='middle';
 [['cover the gap {1, 11, 15}',c.cover_gap],['cover all eight odd residues',c.cover_all_odd]].forEach((b,i)=>{const y=14+i*44;g.fillStyle=line;g.fillRect(250,y,430,24);g.fillStyle=i?inv:nil;g.fillRect(250,y,430*b[1]/c.subsets,24);g.fillStyle=fg;g.textAlign='left';g.fillText(b[0],6,y+12);
  g.fillStyle='#fff';g.fillText((100*b[1]/c.subsets).toFixed(1)+'%  ('+b[1]+' of '+c.subsets+')',258,y+12);});
 document.getElementById('cinfo').textContent='The actual Moonshine set covers the gap and all eight odd residues. So do '+(100*c.p_cover_gap).toFixed(0)+'% and '+(100*c.p_cover_all_odd).toFixed(0)+'% of prime sets of that size: the fill is an arithmetic fact, not evidence.';
 const p=D.proof;document.getElementById('proof').textContent='divisors of 24: '+p.divisors_of_rank.join(', ')+'\\nodd h from (h − 1) | 24: '+p.odd_h_from_divisors.join(', ')+'\\nodd h found in the 23 systems: '+p.odd_h_found.join(', ')+'   (every one of them is A(h−1) repeated)\\nresidues mod 16 of the odd h: '+p.odd_h_residues.join(', ')+'\\n⇒ odd residues never reached: 1, 11, 15';})();
""")

# ------------------------------------------------------------------ 3 n-ball
page("canvas2d_nball.html", "The n-ball and the Gamma function",
     "Volume and surface area of the unit ball in every real dimension n, and |Γ| on the real line with its poles. One function, from the circle upward.",
     "canvas2d_nball",
     """<div class="card"><b>Volume V and sphere area S of the unit ball.</b><div class="row"><label><input type="checkbox" id="lg"> logarithmic y</label>
<span><span class="sw" style="background:var(--nil)"></span>V = π^(n/2)/Γ(n/2+1)<span class="sw" style="background:var(--inv)"></span>S = 2π^(n/2)/Γ(n/2) = n·V</span></div><canvas id="cv"></canvas><div class="info mono pre" id="info">Hover the plot.</div></div>
<div class="card"><b>Any real n.</b> <div class="row"><label>n <input id="n" type="range" min="0" max="32" step="0.01" value="2" style="width:320px"></label><span id="nv" class="mono"></span></div><div class="info mono pre" id="nout"></div></div>
<div class="card"><b>|Γ(x)| on the real line.</b> <span class="sub">poles at 0, −1, −2, … (red lines); Γ(x) = ∫₀^∞ t^(x−1) e^(−t) dt for x > 0, continued by Γ(x) = Γ(x+1)/x.</span><canvas id="gm"></canvas><div class="info mono pre" id="ginfo">Hover.</div></div>""",
     """
const D=HG.data,cv=document.getElementById('cv'),info=document.getElementById('info'),lg=document.getElementById('lg');const PL=56,PR=14,PT=18,PB=36,W=860,Hh=380,NMAX=32;
function Y(v,vmax,log){return log?(Math.log10(Math.max(v,1e-8))+8)/(Math.log10(vmax)+8):v/vmax;}
function draw(){const g=HG.setup(cv,W,Hh),nil=HG.cvar('--nil'),inv=HG.cvar('--inv'),fg=HG.cvar('--fg'),mut=HG.cvar('--mut'),line=HG.cvar('--line'),acc=HG.cvar('--acc'),log=lg.checked,vmax=36,pw=W-PL-PR,ph=Hh-PT-PB;
 const X=n=>PL+n/NMAX*pw,YY=v=>PT+ph-Y(v,vmax,log)*ph;g.font='12px system-ui';g.textBaseline='middle';
 g.strokeStyle=line;(log?[1e-6,1e-4,1e-2,1,10]:[0,10,20,30]).forEach(v=>{g.beginPath();g.moveTo(PL,YY(v));g.lineTo(W-PR,YY(v));g.stroke();g.fillStyle=mut;g.textAlign='right';g.fillText(String(v),PL-6,YY(v));});
 for(let n=0;n<=NMAX;n+=4){g.fillStyle=mut;g.textAlign='center';g.fillText(String(n),X(n),Hh-PB+14);}g.fillText('dimension n',PL+pw/2,Hh-8);
 g.setLineDash([3,4]);g.strokeStyle=mut;[1,2,4,8,16].forEach((n,i)=>{g.beginPath();g.moveTo(X(n),PT);g.lineTo(X(n),PT+ph);g.stroke();g.fillStyle=mut;g.textAlign='center';g.fillText('n='+n,X(n)+(i<2?(i?10:-10):0),PT+6+(i%2)*14);});g.setLineDash([]);
 [[HG.V,nil],[HG.S,inv]].forEach(([f,c])=>{g.strokeStyle=c;g.lineWidth=2.5;g.beginPath();let first=true;for(let n=0.02;n<=NMAX;n+=0.05){const v=f(n);first?g.moveTo(X(n),YY(v)):g.lineTo(X(n),YY(v));first=false;}g.stroke();});g.lineWidth=1;
 [[D.peak_volume,HG.V(D.peak_volume),nil,'V peak n = '+D.peak_volume.toFixed(4)],[D.peak_area,HG.S(D.peak_area),inv,'S peak n = '+D.peak_area.toFixed(4)]].forEach(([n,v,c,t],i)=>{g.fillStyle=c;g.beginPath();g.arc(X(n),YY(v),5,0,2*Math.PI);g.fill();g.fillStyle=fg;g.textAlign='left';g.fillText(t,X(n)+9,YY(v)-(i?4:-4));});
 g.fillStyle=nil;[1,2,4,8,16].forEach(n=>{g.beginPath();g.arc(X(n),YY(HG.V(n)),3.5,0,2*Math.PI);g.fill();});g.fillStyle=inv;[1,2,4,8,16].forEach(n=>{g.beginPath();g.arc(X(n),YY(HG.S(n)),3.5,0,2*Math.PI);g.fill();});}
cv.addEventListener('pointermove',e=>{const r=cv.getBoundingClientRect(),x=(e.clientX-r.left)*W/r.width,n=(x-PL)/(W-PL-PR)*NMAX;if(n<0||n>NMAX)return;info.textContent='n = '+n.toFixed(2)+'\\nV = '+HG.V(n).toPrecision(6)+'      S = '+HG.S(Math.max(n,1e-6)).toPrecision(6)+'      Γ(n/2+1) = '+HG.gamma(n/2+1).toPrecision(6);});
lg.onchange=draw;
const nn=document.getElementById('n'),nv=document.getElementById('nv'),nout=document.getElementById('nout');
function slide(){const n=+nn.value;nv.textContent='n = '+n.toFixed(2);const known={1:'a segment [−1, 1]: V = 2, S = 2 (two points)',2:'the DISC and the CIRCLE: V = π, S = 2π, Γ(1) = 1',3:'the ordinary ball: V = 4π/3, S = 4π',4:'V = π²/2',8:'V = π⁴/24',16:'V = π⁸/40320 = 0.2353'};
 nout.textContent='V = '+HG.V(n).toPrecision(8)+'\\nS = '+(n>0?HG.S(n).toPrecision(8):'—')+'\\nΓ(n/2) = '+(n>0?HG.gamma(n/2).toPrecision(8):'∞ (pole)')+'      Γ(n/2+1) = '+HG.gamma(n/2+1).toPrecision(8)+(known[Math.round(n)]&&Math.abs(n-Math.round(n))<0.006?'\\n'+known[Math.round(n)]:'');}
nn.oninput=slide;
const gm=document.getElementById('gm'),gi=document.getElementById('ginfo');const GW=860,GH=300,GX0=-4.5,GX1=4.5,GY=8;
function drawG(){const g=HG.setup(gm,GW,GH),fg=HG.cvar('--fg'),mut=HG.cvar('--mut'),line=HG.cvar('--line'),nil=HG.cvar('--nil');const X=x=>(x-GX0)/(GX1-GX0)*GW,Yv=v=>GH-20-Math.min(v,GY)/GY*(GH-40);g.font='12px system-ui';g.textBaseline='middle';
 g.strokeStyle=line;g.beginPath();g.moveTo(0,Yv(0));g.lineTo(GW,Yv(0));g.stroke();for(let x=-4;x<=4;x++){g.fillStyle=mut;g.textAlign='center';g.fillText(String(x),X(x),GH-8);}
 g.strokeStyle='#d33';g.lineWidth=1.5;for(let k=0;k<=4;k++){g.beginPath();g.moveTo(X(-k),12);g.lineTo(X(-k),GH-20);g.stroke();g.fillStyle='#d33';g.fillText(k?'−'+k:'0',X(-k),6);}
 g.strokeStyle=nil;g.lineWidth=2.5;let pen=false;for(let x=GX0;x<=GX1;x+=0.004){const z=HG.gamma(x),near=Math.abs(x-Math.round(x))<0.002&&x<=0.001;if(near||!isFinite(z)){pen=false;continue;}const v=Math.abs(z);if(v>GY){pen=false;continue;}pen?g.lineTo(X(x),Yv(v)):(g.beginPath(),g.moveTo(X(x),Yv(v)));pen=true;g.stroke();}
 g.fillStyle=fg;g.textAlign='left';g.fillText('|Γ(x)|, clipped at '+GY,8,GH-34);}
gm.addEventListener('pointermove',e=>{const r=gm.getBoundingClientRect(),x=GX0+(e.clientX-r.left)/r.width*(GX1-GX0);const k=Math.round(x),near=x<=0.2&&Math.abs(x-k)<0.04;
 gi.textContent='x = '+x.toFixed(3)+'      Γ(x) = '+(near?'pole':HG.gamma(x).toPrecision(7))+(x<0&&Math.abs(x-k)<0.04?'\\nnear the pole at '+k+': residue (−1)^'+(-k)+' / '+(-k)+'! = '+((((-k)%2)?-1:1)/[1,1,2,6,24][-k]).toFixed(4):'');});
addEventListener('resize',()=>{draw();drawG();});draw();slide();drawG();
""")

# ------------------------------------------------------------------ 4 frame
page("canvas2d_frame3d.html", "A 3D Cartesian frame for the hypergon data (OpenSCAD companion)",
     "Orthographic, orbit by dragging. Scene A: the n-ball curve in the frame (n, V, S). Scene B: the Niemeier gap as bars. The OpenSCAD source and renders sit beside this page.",
     "canvas2d_frame3d",
     """<div class="card"><div class="row"><label>scene <select id="sc"><option value="A">A · n-ball curve in (n, V, S)</option><option value="B">B · Niemeier gap bars</option></select></label>
<button id="vf">front</button><button id="vt">top</button><button id="vr">right</button><button id="vi">iso</button><button id="vo"><span id="vol">orbit: on</span></button></div>
<canvas id="cv"></canvas><div class="info mono pre" id="info">Drag to turn, wheel to zoom, double-click to reset.</div></div>
<div class="card"><b>OpenSCAD.</b> <a href="hypergon_frame.scad">hypergon_frame.scad</a> (set <code>MODE = 0</code> for scene A, <code>1</code> for scene B) and its renders: <a href="hypergon_frame_A.png">A</a>, <a href="hypergon_frame_B.png">B</a>.
<div class="row"><img id="ia" src="hypergon_frame_A.png" alt="OpenSCAD render of scene A" style="max-width:48%;border:1px solid var(--line)" onerror="this.style.display='none'"><img id="ib" src="hypergon_frame_B.png" alt="OpenSCAD render of scene B" style="max-width:48%;border:1px solid var(--line)" onerror="this.style.display='none'"></div></div>""",
     """
const D=HG.data,cv=document.getElementById('cv'),info=document.getElementById('info'),sc=document.getElementById('sc');const W=860,Hh=560;
let yaw=-0.7,pitch=0.5,zoom=1,orbit=true;const home={yaw:-0.7,pitch:0.5,zoom:1};
// world = (x, y, z) with z up. Scene A box: n in [0,16], V in [0,6], S in [0,36]; scene B box: residue 0..16, row 0..2, count 0..3.
const BOX={A:[16,6,36],B:[16,2,3]},ASC={A:[1/16,1/6,1/36],B:[1/16,1/2,1/3]};
function proj(p,s){const q=[(p[0]*ASC[s][0]-0.5)*2,(p[1]*ASC[s][1]-0.5)*2,(p[2]*ASC[s][2]-0.5)*2];const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
 const x1=q[0]*cy-q[1]*sy,y1=q[0]*sy+q[1]*cy,z1=q[2];const y2=y1*cp-z1*sp,z2=y1*sp+z1*cp;const k=170*zoom;return[W/2+x1*k,Hh/2-z2*k,y2];}
function line(g,a,b,s,c,w){const p=proj(a,s),q=proj(b,s);g.strokeStyle=c;g.lineWidth=w||1;g.beginPath();g.moveTo(p[0],p[1]);g.lineTo(q[0],q[1]);g.stroke();}
function frame(g,s,fg,mut,line_){const[bx,by,bz]=BOX[s];const c=[];for(let i=0;i<8;i++)c.push([i&1?bx:0,i&2?by:0,i&4?bz:0]);
 [[0,1],[2,3],[4,5],[6,7],[0,2],[1,3],[4,6],[5,7],[0,4],[1,5],[2,6],[3,7]].forEach(e=>line(g,c[e[0]],c[e[1]],s,line_,1));
 const o=[0,0,0];line(g,o,[bx,0,0],s,'#d33',2.5);line(g,o,[0,by,0],s,'#2a9d4a',2.5);line(g,o,[0,0,bz],s,'#2b6cb0',2.5);g.font='12px system-ui';g.textBaseline='middle';
 const lab=s==='A'?['n →','V →','S →']:['h mod 16 →','row →','count →'];[[bx,0,0,0],[0,by,0,1],[0,0,bz,2]].forEach(a=>{const p=proj([a[0],a[1],a[2]],s);g.fillStyle=['#d33','#2a9d4a','#2b6cb0'][a[3]];g.textAlign='left';g.fillText(lab[a[3]],p[0]+5,p[1]);});}
function gizmo(g){const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);const ax=[[1,0,0,'#d33','x'],[0,1,0,'#2a9d4a','y'],[0,0,1,'#2b6cb0','z']];g.font='bold 12px system-ui';g.textAlign='center';
 ax.forEach(a=>{const x1=a[0]*cy-a[1]*sy,y1=a[0]*sy+a[1]*cy,z1=a[2];const y2=y1*cp-z1*sp,z2=y1*sp+z1*cp;g.strokeStyle=a[3];g.lineWidth=2.5;g.beginPath();g.moveTo(60,Hh-60);g.lineTo(60+x1*36,Hh-60-z2*36);g.stroke();g.fillStyle=a[3];g.fillText(a[4],60+x1*46,Hh-60-z2*46);});}
function sceneA(g,fg,mut,line_){const s='A',pts=[];for(let n=0.02;n<=16;n+=0.1)pts.push([n,HG.V(n),HG.S(n)]);
 for(let n=0;n<=16;n+=1)line(g,[n,0,0],[n,6,6*n>36?36:6*n],s,line_,.6);      // the surface z = n*y, one straight line for each whole n
 for(let i=1;i<pts.length;i++){const t=pts[i][0]/16,h=240-200*t;line(g,pts[i-1],pts[i],s,'hsl('+h+',75%,50%)',3);}
 [1,2,4,8,16].forEach(n=>{const p=proj([n,HG.V(n),HG.S(n)],s);g.fillStyle=fg;g.beginPath();g.arc(p[0],p[1],4,0,2*Math.PI);g.fill();g.font='12px system-ui';g.textAlign='left';g.fillText('n='+n,p[0]+6,p[1]-6);});
 [[D.peak_volume,'V peak'],[D.peak_area,'S peak']].forEach(([n,t])=>{const p=proj([n,HG.V(n),HG.S(n)],s);g.fillStyle='#c2600f';g.beginPath();g.arc(p[0],p[1],5.5,0,2*Math.PI);g.fill();g.fillStyle=fg;g.fillText(t+' '+n.toFixed(3),p[0]+8,p[1]+10);});
 info.textContent='Scene A: x = n, y = V, z = S; the curve lies on the surface z = n·y (faint lines, one per whole n).\\nIt starts at (0, 1, 0) and passes (2, π, 2π): the circle. V is highest at n = 5.257, S at n = 7.257; both fall after.';}
function box(g,s,x,y,h,col){const f=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,h],[1,0,h],[1,1,h],[0,1,h]].map(v=>proj([x+.1+v[0]*.8,y+.1+v[1]*.8,v[2]],s));const faces=[[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]].map(q=>({q,d:q.reduce((a,i)=>a+f[i][2],0)})).sort((a,b)=>b.d-a.d);
 faces.forEach((F,i)=>{g.fillStyle=col;g.globalAlpha=i<2?.55:.9;g.beginPath();F.q.forEach((k,j)=>j?g.lineTo(f[k][0],f[k][1]):g.moveTo(f[k][0],f[k][1]));g.closePath();g.fill();g.globalAlpha=1;g.strokeStyle='rgba(0,0,0,.35)';g.stroke();});}
function sceneB(g,fg,mut,line_){const s='B',cnt={},ms={};D.systems.forEach(t=>{cnt[t.h%16]=(cnt[t.h%16]||0)+1;});D.moonshine.forEach(p=>{if(p%2)ms[p%16]=(ms[p%16]||0)+1;});
 const bars=[];for(let r=0;r<16;r++){if(cnt[r])bars.push([r,0,cnt[r],'#2b6cb0']);if(ms[r])bars.push([r,1,ms[r],'#c2600f']);}
 bars.map(b=>({b,d:proj([b[0]+.5,b[1]+.5,0],s)[2]})).sort((a,b)=>b.d-a.d).forEach(o=>box(g,s,o.b[0],o.b[1],o.b[2],o.b[3]));
 D.gap.forEach(r=>{const p=proj([r+.5,0.5,0],s);g.fillStyle='#b42318';g.font='bold 12px system-ui';g.textAlign='center';g.fillText('gap '+r,p[0],p[1]+16);});
 info.textContent='Scene B: x = h mod 16, y = row (0 Niemeier root systems, blue; 1 Moonshine primes, orange), z = how many.\\nColumns 1, 11 and 15 are empty in row 0 and filled in row 1: the gap and its Moonshine fill. (Row 1 counts the 14 odd Moonshine primes by residue.)';}
function draw(){const g=HG.setup(cv,W,Hh),fg=HG.cvar('--fg'),mut=HG.cvar('--mut'),line_=HG.cvar('--line'),s=sc.value;frame(g,s,fg,mut,line_);(s==='A'?sceneA:sceneB)(g,fg,mut,line_);gizmo(g);}
let drag=null;cv.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY,yaw,pitch];cv.setPointerCapture(e.pointerId);});cv.addEventListener('pointermove',e=>{if(!drag)return;yaw=drag[2]+(e.clientX-drag[0])*.008;pitch=Math.max(-1.55,Math.min(1.55,drag[3]+(e.clientY-drag[1])*.008));orbit=false;vol.textContent='orbit: off';draw();});
cv.addEventListener('pointerup',()=>drag=null);cv.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.4,Math.min(3,zoom*(e.deltaY<0?1.1:.91)));draw();},{passive:false});cv.addEventListener('dblclick',()=>{({yaw,pitch,zoom}=home);draw();});
const pose=(y,p)=>()=>{yaw=y;pitch=p;orbit=false;vol.textContent='orbit: off';draw();};vf.onclick=pose(0,0);vt.onclick=pose(0,1.5707);vr.onclick=pose(-1.5707,0);vi.onclick=pose(-0.7,0.5);
vo.onclick=()=>{orbit=!orbit;vol.textContent='orbit: '+(orbit?'on':'off');};sc.onchange=draw;setInterval(()=>{if(orbit&&!drag&&!matchMedia('(prefers-reduced-motion: reduce)').matches){yaw+=0.012;draw();}},60);draw();
""")

# ------------------------------------------------------------------ index
cards = [
    ("canvas2d_ring.html", "The sixteen hypergons", "Gauss–Wantzel round the sedenion ring: 4 of the 16 positions are constructible; click one for its polygon and the φ(n) test; test any n."),
    ("canvas2d_niemeier_gap.html", "The Niemeier gap", "The 23 root systems of rank 24 by h mod 16, the three empty columns {1, 11, 15}, the Moonshine primes, the proof as data, and the exact control (68% of prime sets do the same)."),
    ("canvas2d_nball.html", "The n-ball and the Gamma function", "Volume and sphere area at every real dimension, the peak at n = 5.257, the circle at n = 2, and |Γ| with its poles."),
    ("canvas2d_frame3d.html", "A 3D Cartesian frame (OpenSCAD companion)", "The n-ball curve in the frame (n, V, S) and the Niemeier gap as bars, orbitable, with the OpenSCAD source and renders."),
]
cards_html = "".join(f'<div class="card"><h2 style="font-size:17px;margin:0"><a href="{u}">{html.escape(t)}</a></h2><span class="tag">canvas2d_</span><p>{html.escape(d)}</p></div>' for u, t, d in cards)
src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hypergon Constructibility Gallery</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="hg.css"><!-- SPDX-License-Identifier: GPL-3.0-only. Generated by build_pages.py. --></head><body>{CT}
<header><h1>Hypergon constructibility: interactive visualizations</h1><div class="sub">ValaQuenta engine 4, <code>modules/hypergon_constructibility</code>, with the n-ball of <code>bell_curve</code>. Four pages, each checked against the Python engines on load. No libraries, no network.</div></header>
<main>{cards_html}<div class="card"><h2 style="font-size:17px;margin:0">Code flow chart</h2><span class="tag">svg</span><p>The call graph of the engine in ISO 5807 symbols, derived from the source: coming with the paper section.</p></div></main>
<footer><p><b>Sources.</b></p><ul>{src}</ul><p>Launch: <code>gallery/hypergon_constructibility/serve_gallery.sh</code> (loopback only).</p></footer></body></html>""")
print("pages written")
