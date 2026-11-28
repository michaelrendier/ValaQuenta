#!/usr/bin/env python3
"""build_pages.py -- writes the five canvas2d_*.html pages and index.html of the add_scale_sign gallery from one shared chrome, so the pages cannot drift.
Page logic is in the JS strings below; the maths is in ass.js, checked against ass_data.js (baked by build_data.py from the Python engine).
Run:  python3 build_pages.py"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/michaelrendier"
SOURCES = [
    (f"{GH}/ValaQuenta/blob/main/modules/add_scale_sign/maths.py", "ValaQuenta/modules/add_scale_sign/maths.py", "the Python engine these pages port and check against (ASS, ASSWord, group_laws_exact)"),
    (f"{GH}/ValaQuenta/blob/main/wiki/add_scale_sign.md", "ValaQuenta/wiki/add_scale_sign.md", "the engine's record page, with the claim table of the clean-house pass"),
    (f"{GH}/Ainulindale/blob/main/wiki/107_add_scale_sign_datatype.md", "Ainulindale/wiki/107_add_scale_sign_datatype.md", "the formal specification of the datatype"),
    (f"{GH}/ValaQuenta/blob/main/tests/test_add_scale_sign.py", "ValaQuenta/tests/test_add_scale_sign.py", "the tests: laws, brackets, the Noether identity, the firing defect, the quadrant labels"),
    (f"{GH}/GenerationalLineage/blob/main/engine/add_scale_sign.py", "GenerationalLineage/engine/add_scale_sign.py", "the downstream copy of the datatype"),
]
REFS = [
    ("Wikipedia, \"Affine group\": Aff(1, ℝ) = ℝ ⋊ ℝ*, the group of x ↦ ax + b.", "https://en.wikipedia.org/wiki/Affine_group"),
    ("Wikipedia, \"Semidirect product\".", "https://en.wikipedia.org/wiki/Semidirect_product"),
    ("Wikipedia, \"Commutator\": the group commutator [x, y] = x⁻¹y⁻¹xy used here.", "https://en.wikipedia.org/wiki/Commutator"),
    ("Wikipedia, \"Smith chart\" and \"Reflection coefficient\": Γ = tanh(u/2) is the real-axis form of the fold.", "https://en.wikipedia.org/wiki/Smith_chart"),
    ("S. Lang, Algebra (Springer GTM 211), chapter on groups: semidirect products and the affine group.", "https://doi.org/10.1007/978-1-4613-0041-0"),
    ("N. J. A. Sloane, OEIS A005132: Recamán's sequence, the set-membership flip test that ASSWord.would_collide copies.", "https://oeis.org/A005132"),
    ("The Python Software Foundation, Python 3 documentation: fractions.Fraction, dataclasses.", "https://docs.python.org/3/library/fractions.html"),
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
 "canvas2d_plane.html": about_card(
    "Two elements X and Y of Aff(1, ℝ), each a map x ↦ sign·scale·x + add, drawn as straight lines y = f(x) on the plane. A third and fourth line are the two composites X∘Y (Y fires first) and Y∘X. The dashed diagonal is y = x; where a line crosses it is that map's fixed point.",
    "Set add, ln scale and the sign of X and of Y. Watch the red and gold lines: they coincide exactly when X and Y commute. Move the start point x₀: the cobweb on the diagonal follows x₀ → Y(x₀) → X(Y(x₀)).",
    "That composition of two lines is a line (the group is closed), that its slope is the product of the slopes (scale × scale, sign × sign) and that its intercept is add<sub>X</sub> + sign<sub>X</sub>·scale<sub>X</sub>·add<sub>Y</sub>, so the order of two maps differs only in the intercept unless the maps share a fixed point or one is a pure sign or scale of the other.",
    "Anything about the engine's own arithmetic beyond one float: the numbers here are floats, and the exact (Fraction) statements are on the grid page. It does not show the record of steps: composing keeps only the resulting line.",
    "X∘Y has add = a<sub>X</sub> + g<sub>X</sub>s<sub>X</sub>a<sub>Y</sub>, scale = s<sub>X</sub>s<sub>Y</sub>, sign = g<sub>X</sub>g<sub>Y</sub>. With X = ADD(3) and Y = SCALE(2): X∘Y = (3, 2, +1), Y∘X = (6, 2, +1)."),
 "canvas2d_bracket.html": about_card(
    "The group commutator [x, y] = x⁻¹y⁻¹xy of two generators, walked step by step on a number line: fire y, then x, then y⁻¹, then x⁻¹, and see where the starting point lands. Below, the translation it adds up to as the parameter moves.",
    "Choose a pair: (ADD, SCALE), (ADD, SIGN) or (SCALE, SIGN). Move the sliders and the start x₀. The four hops are drawn alternately above and below the line. The three start points listed under the picture all move by the same amount: the commutator is a pure translation.",
    "<code>[SCALE, ADD] = ADD</code> in the group: the commutator of ADD(a) with SCALE(s) is the translation a·(1/s − 1), of ADD(a) with SIGN(−1) the translation −2a, and SCALE with SIGN commute (the commutator is the identity). Only ADD ever appears on the right: order matters at this tier through the offset alone.",
    "The Lie-algebra bracket of the same name, which is the derivative of this one at the identity. The convention x⁻¹y⁻¹xy is the one the wiki's table uses; the other convention gives the negated translation.",
    "ADD(3), SCALE(2): [ADD, SCALE] = (−1.5, 1, +1). ADD(3), SIGN(−1): [ADD, SIGN] = (−6, 1, +1). SCALE(2), SIGN(−1): identity."),
 "canvas2d_fold.html": about_card(
    "The read-out of one element: its word u = g·ln s + a, its fold Γ = tanh(u/2), and its place on the two orthogonal Smith charts. Left: the unit disc with Γ_SCALE = tanh(½·ln s) on the east–west axis and Γ_ADD = tanh(½·a) on the north–south axis. Right: u over the (add, ln s) plane, and below it the firing defect (g − 1)·ln s against ln s.",
    "Move the sliders or click the right-hand map to set (add, ln s). Flip the sign: the point is drawn filled for g = +1 and as a ring for g = −1, and its quadrant gets a prime (′). The defect plot has two lines: g = +1 is flat at zero, g = −1 is −2·ln s.",
    "That SIGN only matters to the fold where SCALE is not 1: at s = 1 the defect is zero for either sign. The quadrant letters follow the rings: north = add ≥ 0, east = scale ≥ 1 (at version 0.1 the two letters were swapped; the page's self-check found it, test and ledger X-71).",
    "The fold of a composite: u of a product is not the sum of the factors' u, and this page does not combine elements (that is the first page). Γ here is the real-axis form of the Smith-chart fold, not a full complex chart.",
    "Γ_SCALE = tanh(½·ln s), Γ_ADD = tanh(½·a), Γ = tanh(½·(g·ln s + a)); the defect is (g−1)·ln s, which is −2·ln s for g = −1. At (a, s, g) = (3, 0.25, +1): Γ_SCALE = −0.6, Γ_ADD = 0.905, quadrant NW (add north, scale below 1 west)."),
 "canvas2d_longpath.html": about_card(
    "An ASS word as a path. Each step is a generator (ADD, SCALE or SIGN) fired on the previous position; the page draws the positions visited, starting from x₀, with each step as a hop. This is ASSWord.trajectory, collisions and would_collide.",
    "Pick a preset word or build one with the buttons. Switch between the chrono order (as fired) and the zeta order (steps sorted by |u| descending): the end element is the same only if the steps commute, and the two paths show it. A ringed position was visited twice. The list under the picture says which candidate next steps would land on a visited position.",
    "That the order of a word is part of its content: re-ordering the same three steps changes the path and the final point. Collisions are real: ADD(+1) then ADD(−1) returns to x₀; two SIGN(−1) steps return to x₀. The flip test is the Recamán rule: a candidate is refused if it lands on a position already visited.",
    "Anything about Recamán's sequence beyond that borrowed test; and it does not draw the composite element, only the positions. The composite and its u are in the text.",
    "Preset 2 (SCALE 8, ADD 2, SIGN(−1)·SCALE ½) with x₀ = 1: chrono path 1 → 8 → 10 → −5; zeta path differs. Preset 1: collision (0, 2) at position 1."),
 "canvas2d_grouptable.html": about_card(
    "An exact finite window onto the group: 18 elements with add ∈ {−2, 0, 3/2}, scale ∈ {1/2, 1, 3}, sign ∈ {−1, +1}, in exact rational arithmetic. Row i, column j is the product x<sub>i</sub>∘x<sub>j</sub>. The page is a map of three facts about those 324 products.",
    "Choose what the colour shows. <b>commute</b>: a cell is filled when x<sub>i</sub>∘x<sub>j</sub> = x<sub>j</sub>∘x<sub>i</sub>. <b>closure</b>: filled when the product is again one of the 18 elements. <b>add</b>: the offset of the product on a diverging scale. Click a cell for the exact product both ways.",
    "That the group is associative (all 5832 triples are checked on load: zero failures) but far from commutative (76 of the 324 ordered pairs commute) and that the window is not a subgroup (only 84 of the 324 products stay inside). The centre of the window is the identity alone.",
    "A Cayley table of a finite group. A finite group's table is closed, and this window is not (84 of 324 products stay inside); the only finite subgroups of Aff(1, ℝ) have order 1 or 2. The picture is a census of a sample.",
    "5832 triples, 0 associativity failures; 76 commuting ordered pairs; 84 products inside the grid; centre = {identity}."),
}


def page(fname, title, sub, kind, body, script):
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
    refs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in REFS)
    shell = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>@TITLE@</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="ass.css">
<!-- SPDX-License-Identifier: GPL-3.0-only. @KIND@: raw Canvas 2D, no libraries, no network. Code: ass.js. Data: ass_data.js, baked by build_data.py from the Python engine (add_scale_sign 0.3). Generated by build_pages.py. -->
</head><body>@CT@
<header><h1>@TITLE@</h1><div class="sub">@SUB@ A picture shows a structure; it is not evidence that the structure means anything beyond its definition.</div><p><a href="index.html">← ADD:SCALE:SIGN gallery</a></p></header>
<main>@BODY@
@ABOUT@<div class="card"><span id="selfcheck" class="sub">running self-check…</span></div></main>
<footer><p><b>Code and data.</b> Everything shown is recomputed in the browser by <code>ass.js</code> (composition, inverse, commutator, word, fold, the Long Path and exact rational arithmetic) and compared with the numbers the Python engine produced (<code>ass_data.js</code>); the result is printed above. Light and dark follow the system.</p>
<p><b>GitHub sources.</b></p><ul>@SRC@</ul><p><b>Literature and documentation.</b></p><ul>@REFS@</ul></footer>
<script src="ass_data.js"></script><script src="ass.js"></script><script>
const A=window.ASSB, D=A.data, AXC=['#d9534f','#3fa56b','#4a8fe0','#d4a017'];
const $=id=>document.getElementById(id), css=n=>A.css(n);
function plane(cv,x0,x1,y0,y1,pd){pd=pd===undefined?34:pd;const W=cv.width,H=cv.height;return{X:x=>pd+(x-x0)/(x1-x0)*(W-2*pd),Y:y=>H-pd-(y-y0)/(y1-y0)*(H-2*pd),ix:px=>x0+(px-pd)/(W-2*pd)*(x1-x0),iy:py=>y0+(H-pd-py)/(H-2*pd)*(y1-y0)};}
function tag(g,txt,x,y,fg,bg,al){g.font='13px system-ui';const w=g.measureText(txt).width;g.fillStyle=bg;g.globalAlpha=0.82;g.fillRect(al==='c'?x-w/2-3:al==='r'?x-w-3:x-3,y-12,w+6,17);g.globalAlpha=1;g.fillStyle=fg;g.textAlign=al==='c'?'center':al==='r'?'right':'left';g.fillText(txt,x,y);g.textAlign='left';}
@SCRIPT@
A.selfCheck();
</script></body></html>"""
    out = (shell.replace("@TITLE@", html.escape(title)).replace("@KIND@", kind).replace("@CT@", CT).replace("@SUB@", sub).replace("@BODY@", body)
           .replace("@ABOUT@", ABOUT[fname]).replace("@SRC@", src).replace("@REFS@", refs).replace("@SCRIPT@", script))
    open(os.path.join(HERE, fname), "w", encoding="utf-8").write(out)


def editor(p, label, a0, s0, g0):
    return (f'<fieldset class="ed"><legend>{label}</legend><label>add <input type="range" id="{p}a" min="-4" max="4" step="0.25" value="{a0}"><b id="{p}av"></b></label> '
            f'<label>ln scale <input type="range" id="{p}s" min="-2" max="2" step="0.05" value="{s0}"><b id="{p}sv"></b></label> '
            f'<label><input type="checkbox" id="{p}g"{" checked" if g0 else ""}> sign −1</label></fieldset>')


# ------------------------------------------------------------------ 1 two elements and their composites
page("canvas2d_plane.html", "Two maps and their composites",
     "Elements of Aff(1, ℝ) as lines y = sign·scale·x + add; the composites X∘Y and Y∘X, and where they differ.", "canvas2d_plane",
     f"""<div class="card">{editor('x', 'X', 3, 0, False)}{editor('y', 'Y', 0, 0.69, False)}
<div class="row"><label>start x₀ <input type="range" id="x0" min="-5" max="5" step="0.25" value="1"><b id="x0v"></b></label>
<span class="sw" style="background:#d9534f"></span>X <span class="sw" style="background:#3fa56b"></span>Y <span class="sw" style="background:#4a8fe0"></span>X∘Y (Y first) <span class="sw" style="background:#d4a017"></span>Y∘X</div>
<canvas id="cv" width="640" height="560"></canvas></div><div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cv=$('cv');
function el(p){return A.el(+$(p+'a').value,Math.exp(+$(p+'s').value),$(p+'g').checked?-1:1);}
function nm(e){return (e.sign<0?'−':'+')+A.fmt(e.scale,3)+'·x '+(e.add<0?'− '+A.fmt(-e.add,3):'+ '+A.fmt(e.add,3));}
function draw(){['x','y'].forEach(p=>{$(p+'av').textContent=$(p+'a').value;$(p+'sv').textContent='s='+A.fmt(Math.exp(+$(p+'s').value),3);});$('x0v').textContent=$('x0').value;
 const g=cv.getContext('2d'),W=cv.width,H=cv.height,L=6,m=plane(cv,-L,L,-L,L),fg=css('--fg'),mut=css('--mut'),card=css('--card'),line=css('--line');g.clearRect(0,0,W,H);
 g.strokeStyle=line;g.lineWidth=1;g.font='12px system-ui';g.fillStyle=mut;for(let v=-6;v<=6;v+=2){g.beginPath();g.moveTo(m.X(v),m.Y(-L));g.lineTo(m.X(v),m.Y(L));g.moveTo(m.X(-L),m.Y(v));g.lineTo(m.X(L),m.Y(v));g.stroke();g.textAlign='center';g.fillText(v,m.X(v),H-14);g.textAlign='right';g.fillText(v,28,m.Y(v)+4);}
 g.textAlign='left';g.strokeStyle=mut;g.lineWidth=1.5;g.beginPath();g.moveTo(m.X(-L),m.Y(0));g.lineTo(m.X(L),m.Y(0));g.moveTo(m.X(0),m.Y(-L));g.lineTo(m.X(0),m.Y(L));g.stroke();
 g.setLineDash([5,5]);g.beginPath();g.moveTo(m.X(-L),m.Y(-L));g.lineTo(m.X(L),m.Y(L));g.stroke();g.setLineDash([]);
 const X=el('x'),Y=el('y'),XY=A.comp(X,Y),YX=A.comp(Y,X),same=A.same(XY,YX);
 g.save();g.beginPath();g.rect(m.X(-L),m.Y(L),m.X(L)-m.X(-L),m.Y(-L)-m.Y(L));g.clip();
 [[X,0],[Y,1],[XY,2],[YX,3]].forEach(([e,k])=>{g.strokeStyle=AXC[k];g.lineWidth=k>1?3.2:2;g.globalAlpha=k===3?0.9:1;if(k===3&&same)g.setLineDash([9,6]);g.beginPath();g.moveTo(m.X(-L),m.Y(A.apply(e,-L)));g.lineTo(m.X(L),m.Y(A.apply(e,L)));g.stroke();g.setLineDash([]);g.globalAlpha=1;});
 g.restore();
 [[X,0],[Y,1],[XY,2],[YX,3]].forEach(([e,k])=>{const d=1-e.sign*e.scale;if(Math.abs(d)>1e-9){const f=e.add/d;if(Math.abs(f)<L){g.fillStyle=AXC[k];g.strokeStyle=card;g.lineWidth=2;g.beginPath();g.arc(m.X(f),m.Y(f),6,0,7);g.fill();g.stroke();}}});
 const x0=+$('x0').value,y1=A.apply(Y,x0),x2=A.apply(X,y1);g.strokeStyle=fg;g.lineWidth=1.5;g.fillStyle=fg;
 const path=[[x0,x0],[x0,y1],[y1,y1],[y1,x2],[x2,x2]];g.beginPath();path.forEach((p,i)=>{i?g.lineTo(m.X(p[0]),m.Y(p[1])):g.moveTo(m.X(p[0]),m.Y(p[1]));});g.stroke();
 [[x0,'x₀'],[y1,'Y(x₀)'],[x2,'X(Y(x₀))']].forEach(([v,t])=>{g.beginPath();g.arc(m.X(v),m.Y(v),4,0,7);g.fill();if(Math.abs(v)<L)tag(g,t,m.X(v)+8,m.Y(v)+18,fg,card,'l');});
 g.fillStyle=mut;g.font='13px system-ui';g.fillText('y = f(x)   (dashed: y = x; dots: fixed points)',40,18);
 $('info').textContent='X    x ↦ '+nm(X).replace(/^\+/,'')+'\nY    x ↦ '+nm(Y).replace(/^\+/,'')+'\nX∘Y  x ↦ '+nm(XY).replace(/^\+/,'')+'   (add = '+A.fmt(X.add)+' + '+X.sign+'·'+A.fmt(X.scale,3)+'·'+A.fmt(Y.add)+')\nY∘X  x ↦ '+nm(YX).replace(/^\+/,'')+'\n\nX and Y '+(same?'COMMUTE here: X∘Y = Y∘X':'do NOT commute: the composites differ by the translation '+A.fmt(XY.add-YX.add)+' (scale and sign agree: '+(XY.scale===YX.scale||Math.abs(XY.scale-YX.scale)<1e-12)+')')+'\nstart x₀ = '+x0+' → Y(x₀) = '+A.fmt(y1)+' → X(Y(x₀)) = '+A.fmt(x2)+'   (X∘Y)(x₀) = '+A.fmt(A.apply(XY,x0));}
document.querySelectorAll('input').forEach(i=>i.oninput=draw);draw();
""")

# ------------------------------------------------------------------ 2 the bracket
page("canvas2d_bracket.html", "The bracket [SCALE, ADD] = ADD",
     "The group commutator x⁻¹y⁻¹xy of two generators, walked on a number line, and the translation it adds up to.", "canvas2d_bracket",
     """<div class="card"><div class="row"><label>pair <select id="pair"><option value="AS">ADD, SCALE</option><option value="AG">ADD, SIGN(−1)</option><option value="SG">SCALE, SIGN(−1)</option></select></label>
<label>add a <input type="range" id="a" min="-4" max="4" step="0.25" value="3"><b id="av"></b></label>
<label>ln scale <input type="range" id="s" min="-2" max="2" step="0.05" value="0.69"><b id="sv"></b></label>
<label>start x₀ <input type="range" id="x0" min="-4" max="4" step="0.25" value="1"><b id="x0v"></b></label></div>
<canvas id="cv" width="780" height="250"></canvas><canvas id="cv2" width="780" height="270" style="margin-top:10px"></canvas></div>
<div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cv=$('cv'),cv2=$('cv2');
function pair(){const a=+$('a').value,s=Math.exp(+$('s').value),k=$('pair').value,A_=A.el(a,1,1),S=A.el(0,s,1),G=A.el(0,1,-1);return k==='AS'?{x:A_,y:S,n:['ADD('+a+')','SCALE('+A.fmt(s,3)+')'],k}:k==='AG'?{x:A_,y:G,n:['ADD('+a+')','SIGN(−1)'],k}:{x:S,y:G,n:['SCALE('+A.fmt(s,3)+')','SIGN(−1)'],k};}
function tOf(k,a,s){return k==='AS'?a*(1/s-1):k==='AG'?-2*a:0;}
function draw(){$('av').textContent=$('a').value;$('sv').textContent='s='+A.fmt(Math.exp(+$('s').value),3);$('x0v').textContent=$('x0').value;
 const P=pair(),x0=+$('x0').value,g=cv.getContext('2d'),W=cv.width,H=cv.height,fg=css('--fg'),mut=css('--mut'),card=css('--card'),line=css('--line');g.clearRect(0,0,W,H);
 const xi=A.inv(P.x),yi=A.inv(P.y),steps=[[P.y,'y = '+P.n[1]],[P.x,'x = '+P.n[0]],[yi,'y⁻¹'],[xi,'x⁻¹']],pts=[x0];steps.forEach(s=>pts.push(A.apply(s[0],pts[pts.length-1])));
 const lo=Math.min(...pts,-1)-1,hi=Math.max(...pts,1)+1,m=plane(cv,lo,hi,0,1,40),Y0=H/2+10;g.strokeStyle=mut;g.lineWidth=1.5;g.beginPath();g.moveTo(m.X(lo),Y0);g.lineTo(m.X(hi),Y0);g.stroke();
 g.font='12px system-ui';g.fillStyle=mut;g.textAlign='center';for(let v=Math.ceil(lo);v<=hi;v++){g.beginPath();g.moveTo(m.X(v),Y0-4);g.lineTo(m.X(v),Y0+4);g.stroke();if(hi-lo<=26||v%2===0)g.fillText(v,m.X(v),Y0+18);}
 for(let i=0;i<4;i++){const x1=m.X(pts[i]),x2=m.X(pts[i+1]),up=i%2===0,cx=(x1+x2)/2,r=Math.max(Math.abs(x2-x1)/2,2),h=Math.min(r,85);g.strokeStyle=AXC[i];g.lineWidth=2.5;g.beginPath();
  g.moveTo(x1,Y0);g.bezierCurveTo(x1,Y0+(up?-1:1)*h*1.3,x2,Y0+(up?-1:1)*h*1.3,x2,Y0);g.stroke();tag(g,(i+1)+'. '+steps[i][1],cx,Y0+(up?-1:1)*(h*0.98+(up?4:22)),fg,card,'c');}
 pts.forEach((v,i)=>{g.fillStyle=i===0?fg:i===4?AXC[3]:mut;g.beginPath();g.arc(m.X(v),Y0,i===0||i===4?7:5,0,7);g.fill();});
 g.textAlign='left';tag(g,'start x₀ = '+x0,m.X(x0),Y0+38,fg,card,'c');const dl=pts[4]-x0;tag(g,'end = '+A.fmt(pts[4])+'   (moved '+(dl>=0?'+':'')+A.fmt(dl)+')',m.X(pts[4]),Y0+60,AXC[3],card,'c');
 // lower plot: the translation against the parameter
 const h=cv2.getContext('2d'),W2=cv2.width,H2=cv2.height,k=P.k,a=+$('a').value,ls=+$('s').value,s=Math.exp(ls);h.clearRect(0,0,W2,H2);
 const xs=k==='AG'?[-4,4]:[-2,2],f=k==='AS'?(t=>a*(1/Math.exp(t)-1)):k==='AG'?(t=>-2*t):(t=>0),sample=[];for(let i=0;i<=200;i++){const t=xs[0]+(xs[1]-xs[0])*i/200;sample.push([t,f(t)]);}
 let ym=Math.max(1,...sample.map(p=>Math.abs(p[1])));ym=Math.min(ym,12);const q=plane(cv2,xs[0],xs[1],-ym,ym,46);h.strokeStyle=line;h.lineWidth=1;h.fillStyle=mut;h.font='12px system-ui';
 for(let v=Math.ceil(xs[0]);v<=xs[1];v++){h.beginPath();h.moveTo(q.X(v),q.Y(-ym));h.lineTo(q.X(v),q.Y(ym));h.stroke();h.textAlign='center';h.fillText(v,q.X(v),H2-12);}
 h.strokeStyle=mut;h.lineWidth=1.5;h.beginPath();h.moveTo(q.X(xs[0]),q.Y(0));h.lineTo(q.X(xs[1]),q.Y(0));h.stroke();
 h.save();h.beginPath();h.rect(q.X(xs[0]),q.Y(ym),q.X(xs[1])-q.X(xs[0]),q.Y(-ym)-q.Y(ym));h.clip();h.strokeStyle=AXC[2];h.lineWidth=3;h.beginPath();sample.forEach((p,i)=>i?h.lineTo(q.X(p[0]),q.Y(p[1])):h.moveTo(q.X(p[0]),q.Y(p[1])));h.stroke();h.restore();
 const cur=k==='AG'?a:ls;h.fillStyle=AXC[3];h.beginPath();h.arc(q.X(cur),q.Y(Math.max(-ym,Math.min(ym,f(cur)))),7,0,7);h.fill();h.fillStyle=mut;h.textAlign='left';
 h.fillText(k==='AS'?'translation  a·(1/s − 1)  against ln s  (a = '+a+')':k==='AG'?'translation  −2a  against a':'translation 0 against ln s: SCALE and SIGN commute',48,18);
 // numbers
 const C=A.comm(P.x,P.y),tr=Math.abs(C.scale-1)<1e-12&&C.sign===1,starts=[-2,0,3].map(v=>{let x=v;steps.forEach(st=>{x=A.apply(st[0],x);});return v+' → '+A.fmt(x)+' (moved '+A.fmt(x-v)+')';});
 $('info').textContent='[x, y] = x⁻¹y⁻¹xy with x = '+P.n[0]+', y = '+P.n[1]+'\ncomputed: add = '+A.fmt(C.add)+', scale = '+A.fmt(C.scale)+', sign = '+(C.sign>0?'+1':'−1')+'   '+(tr?'a PURE TRANSLATION':'not a translation')+'\nformula : '+(k==='AS'?'a·(1/s − 1) = '+A.fmt(tOf(k,a,s)):k==='AG'?'−2a = '+A.fmt(tOf(k,a,s)):'0 (identity)')+'\nthree start points move by the same amount: '+starts.join('   ')+'\n\n'+(k==='AS'?'This is [SCALE, ADD] = ADD: dilating and translating in the other order leaves a translation behind, proportional to a.':k==='AG'?'SIGN reflects the offset, so swapping ADD and SIGN leaves a translation of −2a.':'SCALE and SIGN commute: nothing is left behind.');}
document.querySelectorAll('input,select').forEach(i=>i.oninput=draw);$('pair').onchange=draw;draw();
""")

# ------------------------------------------------------------------ 3 the fold and the charts
page("canvas2d_fold.html", "The fold and the two Smith charts",
     "One element read out: u = g·ln s + a, Γ = tanh(u/2), Γ_SCALE east–west, Γ_ADD north–south, and the firing defect.", "canvas2d_fold",
     """<div class="card"><div class="row"><label>add a <input type="range" id="a" min="-4" max="4" step="0.05" value="3"><b id="av"></b></label>
<label>ln scale <input type="range" id="s" min="-3" max="3" step="0.05" value="-1.39"><b id="sv"></b></label><label><input type="checkbox" id="g"> sign −1 (the filled dot becomes a ring)</label></div>
<div class="row"><canvas id="cv" width="360" height="360"></canvas><canvas id="cm" width="360" height="360"></canvas></div>
<canvas id="cd" width="740" height="200" style="margin-top:10px"></canvas></div><div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cv=$('cv'),cm=$('cm'),cd=$('cd');
function cur(){return A.el(+$('a').value,Math.exp(+$('s').value),$('g').checked?-1:1);}
function heat(e){const g=cm.getContext('2d'),W=cm.width,H=cm.height,q=plane(cm,-4,4,-3,3,30),card=css('--card'),fg=css('--fg'),mut=css('--mut'),sg=e.sign;g.clearRect(0,0,W,H);
 for(let px=30;px<W-30;px+=4)for(let py=30;py<H-30;py+=4){const a=q.ix(px+2),ls=q.iy(py+2),u=sg*ls+a,v=Math.max(-1,Math.min(1,u/4));g.fillStyle=v>=0?'rgba(217,83,79,'+(0.12+0.7*v)+')':'rgba(74,143,224,'+(0.12-0.7*v)+')';g.fillRect(px,py,4,4);}
 g.save();g.beginPath();g.rect(30,30,W-60,H-60);g.clip();g.strokeStyle=fg;g.lineWidth=2;g.beginPath();g.moveTo(q.X(-4),q.Y(4/sg));g.lineTo(q.X(4),q.Y(-4/sg));g.stroke();g.restore();
 g.strokeStyle=mut;g.lineWidth=1;g.beginPath();g.moveTo(q.X(0),q.Y(-3));g.lineTo(q.X(0),q.Y(3));g.moveTo(q.X(-4),q.Y(0));g.lineTo(q.X(4),q.Y(0));g.stroke();
 g.fillStyle=mut;g.font='12px system-ui';g.fillText('u over (add →, ln s ↑), sign '+(sg>0?'+1':'−1')+'; black line u = 0',32,20);g.fillText('add',W-34,q.Y(0)-4);g.fillText('ln s',q.X(0)+4,42);
 g.fillStyle=AXC[3];g.strokeStyle=card;g.lineWidth=2;g.beginPath();g.arc(q.X(Math.max(-4,Math.min(4,e.add))),q.Y(Math.max(-3,Math.min(3,Math.log(e.scale)))),7,0,7);g.fill();g.stroke();}
function chart(e){const g=cv.getContext('2d'),W=cv.width,H=cv.height,cx=W/2,cy=H/2,R=140,fg=css('--fg'),mut=css('--mut'),card=css('--card'),line=css('--line');g.clearRect(0,0,W,H);
 g.strokeStyle=line;g.lineWidth=1;g.beginPath();g.arc(cx,cy,R,0,7);g.stroke();g.strokeStyle=mut;g.beginPath();g.moveTo(cx-R,cy);g.lineTo(cx+R,cy);g.moveTo(cx,cy-R);g.lineTo(cx,cy+R);g.stroke();
 g.font='12px system-ui';g.fillStyle=mut;[[-2,'ln s=−2'],[-1,'−1'],[1,'1'],[2,'2']].forEach(([v,t])=>{const x=cx+R*Math.tanh(v/2);g.beginPath();g.moveTo(x,cy-4);g.lineTo(x,cy+4);g.stroke();g.textAlign='center';g.fillText(t,x,cy+18);});
 [[-2,'a=−2'],[-1,'−1'],[1,'1'],[2,'2']].forEach(([v,t])=>{const y=cy-R*Math.tanh(v/2);g.beginPath();g.moveTo(cx-4,y);g.lineTo(cx+4,y);g.stroke();g.textAlign='left';g.fillText(t,cx+8,y+4);});
 g.textAlign='center';g.fillText('E: scale > 1',cx+R-30,cy-24);g.fillText('W: scale < 1',cx-R+34,cy-24);g.fillText('N: add ≥ 0',cx,cy-R-6);g.fillText('S: add < 0',cx,cy+R+16);
 const s=A.smith(e),px=cx+R*s.g_scale,py=cy-R*s.g_add;g.strokeStyle=AXC[3];g.lineWidth=1.5;g.setLineDash([4,4]);g.beginPath();g.moveTo(px,cy);g.lineTo(px,py);g.lineTo(cx,py);g.stroke();g.setLineDash([]);
 g.lineWidth=3;g.strokeStyle=AXC[3];g.fillStyle=e.sign>0?AXC[3]:card;g.beginPath();g.arc(px,py,9,0,7);g.fill();g.stroke();g.textAlign='left';tag(g,A.quadrant(e),px+12,py-8,fg,card,'l');}
function defect(e){const g=cd.getContext('2d'),W=cd.width,H=cd.height,q=plane(cd,-3,3,-7,7,46),fg=css('--fg'),mut=css('--mut'),line=css('--line');g.clearRect(0,0,W,H);g.strokeStyle=line;g.lineWidth=1;g.fillStyle=mut;g.font='12px system-ui';
 for(let v=-3;v<=3;v++){g.beginPath();g.moveTo(q.X(v),q.Y(-7));g.lineTo(q.X(v),q.Y(7));g.stroke();g.textAlign='center';g.fillText(v,q.X(v),H-12);}g.strokeStyle=mut;g.beginPath();g.moveTo(q.X(-3),q.Y(0));g.lineTo(q.X(3),q.Y(0));g.stroke();
 g.lineWidth=3;g.strokeStyle=AXC[1];g.beginPath();g.moveTo(q.X(-3),q.Y(0));g.lineTo(q.X(3),q.Y(0));g.stroke();g.strokeStyle=AXC[0];g.beginPath();g.moveTo(q.X(-3),q.Y(6));g.lineTo(q.X(3),q.Y(-6));g.stroke();
 g.textAlign='left';g.fillStyle=AXC[1];g.fillText('g = +1: defect 0',q.X(1.2),q.Y(0)-8);g.fillStyle=AXC[0];g.fillText('g = −1: defect −2·ln s',q.X(0.4),q.Y(-4.6));g.fillStyle=mut;g.fillText('firing defect (g−1)·ln s against ln s',50,16);
 const d=A.defect(e),ls=Math.log(e.scale);g.fillStyle=AXC[3];g.beginPath();g.arc(q.X(Math.max(-3,Math.min(3,ls))),q.Y(Math.max(-7,Math.min(7,d))),7,0,7);g.fill();}
function draw(){$('av').textContent=$('a').value;$('sv').textContent='s='+A.fmt(Math.exp(+$('s').value),3);const e=cur(),sm=A.smith(e);heat(e);chart(e);defect(e);
 $('info').textContent='ASS(add='+A.fmt(e.add)+', scale='+A.fmt(e.scale,4)+', sign='+(e.sign>0?'+1':'−1')+')\nword  u = g·ln s + a = '+e.sign+'·'+A.fmt(Math.log(e.scale),4)+' + '+A.fmt(e.add)+' = '+A.fmt(A.u(e),5)+'\nfold  Γ = tanh(u/2) = '+A.fmt(A.gamma(e),5)+'\nΓ_SCALE = tanh(½·ln s) = '+A.fmt(sm.g_scale,5)+'   Γ_ADD = tanh(½·a) = '+A.fmt(sm.g_add,5)+'   quadrant '+A.quadrant(e)+'\nfiring defect (g−1)·ln s = '+A.fmt(A.defect(e),5)+(Math.abs(A.defect(e))<1e-9?'   (additive: SIGN does not flip a non-trivial SCALE)':'   (SIGN flipped a non-trivial SCALE: the word is order-sensitive)');}
document.querySelectorAll('input').forEach(i=>i.oninput=draw);
cm.addEventListener('pointerdown',ev=>{const q=plane(cm,-4,4,-3,3,30),[x,y]=A.pos(ev,cm);$('a').value=Math.round(Math.max(-4,Math.min(4,q.ix(x)))*20)/20;$('s').value=Math.round(Math.max(-3,Math.min(3,q.iy(y)))*20)/20;draw();});draw();
""")

# ------------------------------------------------------------------ 4 the Long Path
page("canvas2d_longpath.html", "The Long Path of a word",
     "Each step of an ASS word fired on the last position: the positions visited, the collisions, the order, and the flip test.", "canvas2d_longpath",
     """<div class="card"><div class="row"><label>preset <select id="pre"></select></label><label>order <select id="ord"><option value="chrono">chrono (as fired)</option><option value="zeta">zeta (by |u| descending)</option></select></label>
<label>start x₀ <input type="number" id="x0" value="1" step="0.5" style="width:5em"></label></div>
<div class="row"><button data-s="1,1,1,0">ADD +1</button><button data-s="-1,1,1,0">ADD −1</button><button data-s="2,1,1,0">ADD +2</button><button data-s="0,2,1,0">SCALE ×2</button><button data-s="0,0.5,1,0">SCALE ×½</button><button data-s="0,1,-1,0">SIGN −1</button><button id="undo">undo</button><button id="clr">clear</button></div>
<canvas id="cv" width="820" height="300"></canvas></div><div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cv=$('cv');let steps=[];const names=Object.keys(D.words);
names.forEach((n,i)=>{const o=document.createElement('option');o.value=n;o.textContent=n;$('pre').appendChild(o);});
function nm(s){return s[2]<0&&s[1]===1&&s[0]===0?'SIGN(−1)':s[1]!==1&&s[0]===0?'SCALE('+A.fmt(s[1],3)+(s[2]<0?'·SIGN':'')+')':s[0]!==0&&s[1]===1&&s[2]>0?'ADD('+(s[0]>0?'+':'')+s[0]+')':'ASS('+s.join(', ')+')';}
function load(){steps=D.words[$('pre').value].steps.map(s=>s.slice());draw();}
function draw(){const g=cv.getContext('2d'),W=cv.width,H=cv.height,fg=css('--fg'),mut=css('--mut'),card=css('--card'),x0=+$('x0').value||0;g.clearRect(0,0,W,H);
 const I=A.wordInfo(steps,$('ord').value),t=[x0];I.steps.forEach(s=>t.push(A.apply(A.fromArr(s),t[t.length-1])));const col=A.collisions(t);
 const lo=Math.min(...t,0)-1,hi=Math.max(...t,0)+1,m=plane(cv,lo,hi,0,1,46),Y0=H/2;g.strokeStyle=mut;g.lineWidth=1.5;g.beginPath();g.moveTo(m.X(lo),Y0);g.lineTo(m.X(hi),Y0);g.stroke();
 g.font='12px system-ui';g.fillStyle=mut;g.textAlign='center';const stepv=Math.max(1,Math.ceil((hi-lo)/18));for(let v=Math.ceil(lo/stepv)*stepv;v<=hi;v+=stepv){g.beginPath();g.moveTo(m.X(v),Y0-4);g.lineTo(m.X(v),Y0+4);g.stroke();g.fillText(v,m.X(v),Y0+18);}
 for(let i=0;i<I.steps.length;i++){const x1=m.X(t[i]),x2=m.X(t[i+1]),up=i%2===0,r=Math.abs(x2-x1)/2,h=Math.max(Math.min(r,100),14);g.strokeStyle=AXC[i%3];g.lineWidth=2.5;g.beginPath();g.moveTo(x1,Y0);g.bezierCurveTo(x1,Y0+(up?-1:1)*h*1.3,x2,Y0+(up?-1:1)*h*1.3,x2,Y0);g.stroke();
  tag(g,(i+1)+'. '+nm(I.steps[i]),(x1+x2)/2,Y0+(up?-1:1)*(h*0.98+(up?4:22))+(up?-1:1)*Math.floor(i/2)*20,fg,card,'c');}
 t.forEach((v,i)=>{g.fillStyle=i===0?fg:AXC[3];g.beginPath();g.arc(m.X(v),Y0,i===0?7:5,0,7);g.fill();});
 col.forEach(c=>{g.strokeStyle=css('--bad');g.lineWidth=3;g.beginPath();g.arc(m.X(c[2]),Y0,12,0,7);g.stroke();});
 g.textAlign='left';tag(g,'x₀ = '+A.fmt(x0),m.X(x0),Y0+44,fg,card,'c');
 const cand=[['ADD(−1)',[-1,1,1]],['ADD(0)',[0,1,1]],['ADD(+1)',[1,1,1]],['ADD(+2)',[2,1,1]],['SCALE(×2)',[0,2,1]],['SCALE(×½)',[0,0.5,1]],['SIGN(−1)',[0,1,-1]]];
 $('info').textContent='word ('+$('ord').value+'): '+(I.steps.length?I.steps.map(nm).join('  ∘  '):'IDENTITY')+'\npositions: '+t.map(v=>A.fmt(v)).join(' → ')+'\ncollisions (earlier, later, position): '+(col.length?col.map(c=>'('+c[0]+', '+c[1]+', '+A.fmt(c[2])+')').join('  '):'none — self-avoiding')+
 '\nresulting element: x ↦ '+(I.element.sign<0?'−':'+')+A.fmt(I.element.scale,4)+'·x '+(I.element.add<0?'− '+A.fmt(-I.element.add,4):'+ '+A.fmt(I.element.add,4))+'\nu_total = '+A.fmt(I.u_total,5)+'   Σ u of the steps = '+A.fmt(I.u_sum,5)+'   firing defect (g−1)·ln s = '+A.fmt(I.defect,5)+
 '\n\nflip test, the next step would land on a visited position?\n'+cand.map(c=>'  '+c[0].padEnd(11)+(A.wouldCollide(t,c[1])?'YES, refused':'no')).join('\n');}
document.querySelectorAll('button[data-s]').forEach(b=>b.onclick=()=>{steps.push(b.dataset.s.split(',').map(Number).slice(0,3));draw();});
$('undo').onclick=()=>{steps.pop();draw();};$('clr').onclick=()=>{steps=[];draw();};$('pre').onchange=load;$('ord').onchange=draw;$('x0').oninput=draw;$('pre').value=names[1];load();
""")

# ------------------------------------------------------------------ 5 the exact grid
page("canvas2d_grouptable.html", "The exact grid: who commutes, what closes",
     "Eighteen elements in exact rational arithmetic and the 324 ordered products of a window onto Aff(1, ℝ).", "canvas2d_grouptable",
     """<div class="card"><div class="row"><label>colour by <select id="mode"><option value="commute">commute: x∘y = y∘x</option><option value="closure">closure: x∘y is in the grid</option><option value="add">add of the product x∘y</option></select></label>
<span id="stat" class="sub"></span></div><canvas id="cv" width="640" height="640"></canvas></div><div class="card info"><span id="info" class="mono pre">click a cell</span></div>""",
     r"""
const cv=$('cv'),G=A.grid(),n=G.E.length,P=44,C=(640-P)/n;let pick=null;
function cell(x,y){return [Math.floor((x-P)/C),Math.floor((y-P)/C)];}
function draw(){const g=cv.getContext('2d'),mode=$('mode').value,fg=css('--fg'),mut=css('--mut'),card=css('--card'),line=css('--line'),acc=css('--acc');g.clearRect(0,0,cv.width,cv.height);
 for(let i=0;i<n;i++)for(let j=0;j<n;j++){const x=P+j*C,y=P+i*C;let v;
  if(mode==='commute'){v=D.grid.commute[i][j];g.fillStyle=v?AXC[1]:card;g.globalAlpha=v?0.85:1;}
  else if(mode==='closure'){v=D.grid.closure[i][j];g.fillStyle=v?AXC[2]:card;g.globalAlpha=v?0.85:1;}
  else{const a=A.Q.parse(D.grid.prod_add[i][j]).val(),t=Math.max(-1,Math.min(1,a/8));g.fillStyle=t>=0?'rgb(217,83,79)':'rgb(74,143,224)';g.globalAlpha=0.12+0.8*Math.abs(t);}
  g.fillRect(x,y,C-1,C-1);g.globalAlpha=1;}
 g.strokeStyle=mut;g.lineWidth=1.5;for(let b=0;b<=3;b++){const p=P+b*6*C;g.beginPath();g.moveTo(p,P);g.lineTo(p,P+n*C);g.moveTo(P,p);g.lineTo(P+n*C,p);g.stroke();}
 g.fillStyle=mut;g.font='11px system-ui';g.textAlign='center';for(let k=0;k<n;k++){g.fillText(k,P+k*C+C/2,P-8);g.textAlign='right';g.fillText(k,P-6,P+k*C+C/2+4);g.textAlign='center';}
 g.textAlign='left';g.fillText('x∘y: row = x, column = y (y fires first). Blocks of 6 = add −2, 0, 3/2; within a block scale 1/2, 1, 3, each with sign −1, +1.',8,14);
 if(pick){g.strokeStyle=fg;g.lineWidth=3;g.strokeRect(P+pick[1]*C,P+pick[0]*C,C-1,C-1);}
 const id=D.grid.centre[0];g.strokeStyle=acc;g.lineWidth=2;g.setLineDash([4,3]);g.strokeRect(P+id*C,P,C-1,n*C);g.strokeRect(P,P+id*C,n*C,C-1);g.setLineDash([]);
 $('stat').textContent='commuting ordered pairs: '+D.grid.commuting_pairs+' of '+n*n+'   ·   products inside the grid: '+D.grid.closed_pairs+'   ·   centre of the window: element '+D.grid.centre.join(', ')+' (the identity)';}
cv.addEventListener('pointerdown',ev=>{const [x,y]=A.pos(ev,cv),[j,i]=cell(x,y);if(i<0||j<0||i>=n||j>=n)return;pick=[i,j];draw();
 const X=G.E[i],Y=G.E[j],XY=G.cmp(X,Y),YX=G.cmp(Y,X),inG=G.E.findIndex(f=>G.eq(XY,f)),inG2=G.E.findIndex(f=>G.eq(YX,f));
 $('info').textContent='x = element '+i+':  '+G.name(X)+'\ny = element '+j+':  '+G.name(Y)+'\nx∘y: '+G.name(XY)+'   '+(inG>=0?'(element '+inG+')':'(outside the grid)')+'\ny∘x: '+G.name(YX)+'   '+(inG2>=0?'(element '+inG2+')':'(outside the grid)')+'\n'+(G.eq(XY,YX)?'they commute':'they do not commute: the products differ by the translation '+XY.add.add(YX.add.neg()).str()+' (scale and sign agree)');});
$('mode').onchange=draw;draw();
""")

# ------------------------------------------------------------------ index
cards = [
    ("canvas2d_plane.html", "Two maps and their composites", "X, Y and the composites X∘Y and Y∘X as lines on the plane; fixed points; a cobweb; whether the two orders agree."),
    ("canvas2d_bracket.html", "The bracket [SCALE, ADD] = ADD", "The commutator x⁻¹y⁻¹xy walked on a number line; it is always a pure translation, a·(1/s − 1) for ADD with SCALE and −2a for ADD with SIGN."),
    ("canvas2d_fold.html", "The fold and the two Smith charts", "u, Γ, Γ_SCALE east–west, Γ_ADD north–south, the sign sheet, and the firing defect (g−1)·ln s."),
    ("canvas2d_longpath.html", "The Long Path of a word", "ASSWord.trajectory, collisions and the flip test; chrono against zeta order."),
    ("canvas2d_grouptable.html", "The exact grid", "18 elements in exact rationals: 5832 triples associate, 76 of 324 pairs commute, 84 products stay inside; the centre is the identity."),
]
cards_html = "".join(f'<div class="card"><h2 style="font-size:17px;margin:0"><a href="{u}">{html.escape(t)}</a></h2><span class="tag">canvas2d_</span><p>{html.escape(d)}</p></div>' for u, t, d in cards)
cards_html += '<div class="card"><h2 style="font-size:17px;margin:0">Code flow chart</h2><span class="tag">svg</span><p>The call graph of the engine in ISO 5807 symbols, derived from the source by <code>tools/flowchart.py</code>: <a href="../../docs/flowcharts/add_scale_sign_flow.svg">add_scale_sign_flow.svg</a>.</p></div>'
src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ADD:SCALE:SIGN Gallery</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="ass.css"><!-- SPDX-License-Identifier: GPL-3.0-only. Generated by build_pages.py. --></head><body>{CT}
<header><h1>ADD:SCALE:SIGN: interactive visualizations</h1><div class="sub">ValaQuenta engine 6, <code>modules/add_scale_sign</code> (0.3). Five pages, each recomputing its numbers in the browser and comparing them with the Python engine. A picture shows a structure; it is not evidence that the structure means anything beyond its definition.</div></header>
<main>{cards_html}</main>
<footer><p><b>Sources.</b></p><ul>{src}</ul><p>Launch: <code>gallery/add_scale_sign/serve_gallery.sh</code> (loopback only, port 8794).</p></footer></body></html>""")
print("pages written")
