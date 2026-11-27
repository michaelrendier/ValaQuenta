#!/usr/bin/env python3
"""build_pages.py -- writes the five canvas2d_*.html pages and index.html of the box_kite gallery from one shared chrome, so the pages cannot drift.
Page logic is in the JS strings below; the maths is in bk.js, checked against bk_data.js (baked by build_data.py from the Python engine).
Run:  python3 build_pages.py"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/michaelrendier"
SOURCES = [
    (f"{GH}/ValaQuenta/blob/main/modules/box_kite/maths.py", "ValaQuenta/modules/box_kite/maths.py", "the Python engine these pages port and check against (Cayley–Dickson table, assessors, box-kites, associator, the labelled group)"),
    (f"{GH}/ValaQuenta/blob/main/wiki/box_kite.md", "ValaQuenta/wiki/box_kite.md", "the engine's record page, including 'The group, enumerated'"),
    (f"{GH}/Ainulindale/blob/main/wiki/84_the_box_kite_debugger.md", "Ainulindale/wiki/84_the_box_kite_debugger.md", "the narrative of the box-kite as a debugger"),
    (f"{GH}/ValaQuenta/blob/main/tests/test_box_kite.py", "ValaQuenta/tests/test_box_kite.py", "the tests, including an independent recursive Cayley–Dickson product"),
]
REFS = [
    ('R. P. C. de Marrais, "The 42 Assessors and the Box-Kites They Fly: Diagonal Axis-Pair Systems of Zero-Divisors in the Sedenions\' 16 Dimensions", arXiv:math/0011260 (2000).', "https://arxiv.org/abs/math/0011260"),
    ('R. P. C. de Marrais, "Placeholder Substructures I: The Road from Zero-Divisors to the 84 Diagonal Sedenions" and "II: The Emergence of the Pentagonal Genes", arXiv:math/0207003 and arXiv:math/0207005.', "https://arxiv.org/abs/math/0207003"),
    ('K. Imaeda and M. Imaeda, "Sedenions: algebra and analysis", Applied Mathematics and Computation 115 (2000) 77–88.', "https://doi.org/10.1016/S0096-3003(99)00140-X"),
    ('R. E. Cawagas, "On the structure and zero divisors of the Cayley–Dickson sedenion algebra", Discussiones Mathematicae – General Algebra and Applications 24 (2004) 251–265.', "https://doi.org/10.7151/dmgaa.1086"),
    ('J. C. Baez, "The Octonions", Bull. Amer. Math. Soc. 39 (2002) 145–205. The octonions, the Fano plane, the automorphism group G₂, the 480 multiplication tables.', "https://doi.org/10.1090/S0273-0979-01-00934-X"),
    ('J. H. Conway and D. A. Smith, On Quaternions and Octonions (A K Peters, 2003). The 1344 and the 168 in the labelled octonion group.', "https://doi.org/10.1201/9781439864180"),
    ('J. H. Conway, R. T. Curtis, S. P. Norton, R. A. Parker, R. A. Wilson, Atlas of Finite Groups (Oxford, 1985): L₃(2) = PSL(2,7), order 168.', "https://brauer.maths.qmul.ac.uk/Atlas/v3/lin/L32/"),
    ("The Python Software Foundation, Python 3 documentation: itertools.permutations, itertools.product.", "https://docs.python.org/3/library/itertools.html"),
    ("OpenSCAD User Manual (camera, projection, text, polyhedron).", "https://openscad.org/documentation.html"),
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
 "canvas2d_octahedron.html": about_card(
    "One box-kite: six assessors joined by the products that vanish. An assessor (a, b) is the plane spanned by e_a and e_(b+8) in the sedenions, drawn here as the label (a, b+8). Its two diagonals e_a ± e_(b+8) are zero-divisors: multiplied by the right diagonal of another assessor they give exactly zero. Each vertex is one assessor, each edge is a pair of assessors whose diagonals annihilate each other. The six vertices sit on ±x, ±y, ±z, so the shape is an octahedron, K<sub>2,2,2</sub>.",
    "Choose the strut s (the XOR of a and b, the same for all six). Drag to turn the octahedron; click a vertex. Its four neighbours light up and the panel lists, for each of its two diagonals, the four diagonals it annihilates, found by multiplying out in the browser. The three dashed lines through the centre are the reversal pairs (a, b) and (b, a): the only pairs in the kite that do NOT annihilate each other. The coloured gizmo in the corner names the axes by the pair they carry.",
    "Every vertex has exactly four neighbours and one non-neighbour, the reversal partner. The Laplacian spectrum of the graph (switch it on) is {0, 4, 4, 4, 6, 6} for every strut: one zero mode, a triple mode at 4, a double at 6. All seven struts give the same picture, only the labels change.",
    "That the octahedron is a place in space. The six axes are drawn at right angles because the graph is K<sub>2,2,2</sub>; the zero-divisors themselves live in 16 dimensions. e<sub>0</sub> is not in the picture on purpose: it is outside every box-kite. The frame has no σ = ½ marker because it has no σ coordinate; the only balance in it is the equal split of each diagonal into 1/√2 and ±1/√2.",
    "6 vertices, 12 edges, 3 non-edges (the reversal pairs), 4-regular; spectrum [0,4,4,4,6,6]; each diagonal annihilates 4 others (84 diagonals × 4 = 336 ordered pairs). Strut 1 is de Marrais's Box-Kite I: (3,10) (2,11) (5,12) (4,13) (7,14) (6,15) in his notation."),
 "canvas2d_glued42.html": about_card(
    "All 42 assessors at once: seven octahedra, one per strut s = 1…7, set at seven corners of a cube. The cube corner is the binary expansion of s (x = bit 1, y = bit 2, z = bit 4); the eighth corner, s = 0, is left empty and marked e<sub>0</sub>, the place the geometry does not occupy.",
    "Choose a strut to isolate it or leave 'all'. Drag to turn, wheel to zoom, double-click to reset. Click a vertex for its assessor, its strut and its four neighbours. The numbers under the picture are computed from the engine's glued graph: 42 vertices, 84 edges, and the count of edges that cross between kites.",
    "That the 42 assessors are the disjoint union of seven octahedra: every one of the 84 edges is inside a strut, none crosses between two (cross-strut edges = 0). So the Laplacian spectrum is the octahedral spectrum seven times over: 7 zero modes, 21 at 4, 14 at 6.",
    "How the seven kites are glued into one geometry. The engine does not do it yet (its own stated open item), and the picture does not either: the cube positions are a drawing choice made from the bits of s, not part of the engine's graph. No line between kites is drawn because the engine has none.",
    "42 vertices, 84 edges, 0 cross-strut edges, 7 components; zero modes 7 (one per kite), eigenvalue 4 with multiplicity 21 and 6 with multiplicity 14."),
 "canvas2d_fano.html": about_card(
    "Left: the Fano plane on the seven imaginary octonion units e1…e7: seven points, seven lines, three points on a line, three lines through a point. A line is a triple {a, b, a XOR b}. Right: PG(3,2), the geometry on the fifteen indices 1…15 (the imaginary units of the sedenions): 15 points, 35 lines, 15 planes. The octonion Fano plane is one of those planes: the points 1…7.",
    "Left: click a point s. The three lines through it are coloured; each line {s, a, b} gives a pair of assessors (a, b) and (b, a), and that pair is one axis of the strut-s octahedron: the colours match the axes of the octahedron page. Right: click a point to see its seven lines; choose a line or a plane from the lists; the octonion plane is the plane marked 'O'.",
    "Why there are seven box-kites and why each has three axes: a strut is a point of the Fano plane and the three lines through it are the three reversal pairs. The assessor's two indices and its strut are a Fano line, a XOR b = s. Counts check by hand: each point lies on 7 lines, each line in 3 planes, each plane holds 7 points and 7 lines.",
    "That PG(3,2) is a geometry the sedenion product uses for anything other than labelling; the engine's own overlap check (skeleton_overlap) is where that is measured. And it does not show e<sub>0</sub>, which is in neither plane.",
    "15 points, 35 lines, 15 planes; points on a line 3; lines through a point 7; the 7 Fano lines of the octonions {1,2,3} {1,4,5} {1,6,7} {2,4,6} {2,5,7} {3,4,7} {3,5,6}."),
 "canvas2d_associator.html": about_card(
    "The associator of the basis elements, [e_i, e_j, e_k] = (e_i e_j) e_k − e_i (e_j e_k), as a 16 × 16 grid: row i, column j, for one chosen k. A cell is blank when the product is associative there and filled when it is not. The engine calls this the curvature, by analogy: it measures how far the product bends when you regroup it.",
    "Slide k from 0 to 15, or switch to 'count over k', which shows for each (i, j) how many k bend it. Click a cell for the exact vector. Dotted lines divide the indices 0…7 (the octonions) from 8…15 (the doubled half). The table underneath counts the non-zero triples in each of the eight blocks.",
    "1848 of the 4096 triples do not associate, and every one of them has norm exactly 2: the grid has two values, 0 and 2, nothing in between. The octonion block (i, j, k all below 8) is NOT flat: 168 of its 512 triples bend, the 7 × 6 × 5 − 42 ordered triples of distinct imaginary units that do not lie on a line. k = 0 never bends (e<sub>0</sub> is the identity); k = 8 bends in 168 cells, every other k in 120.",
    "A curvature in any differential-geometric sense: there is no metric or connection here, only a count of failures of one law. And it does not say where the zero-divisors are: the associator is a property of the basis table.",
    "1848 non-zero, 2248 zero, 4096 in all; blocks (i, j, k below / above 8): 168, 168, 336, 168, 168, 336, 168, 336; per-k counts 0, 120 × 7, 168, 120 × 7."),
 "canvas2d_group.html": about_card(
    "The group of the labelled octonions: signed permutations of e1…e7 that keep the octonion multiplication table. Found here by trying all 5040 permutations (168 keep the Fano lines) and all 128 sign patterns on each (8 survive per permutation): 1344 elements in all. Each acts on the seven box-kites by permuting their struts.",
    "Left: the seven struts on a ring, the arrows s → π(s) of one chosen permutation, its cycles colour-coded. Choose a cycle type or step through the 168. Right: the census of cycle types, the eight sign changes that fix every kite, and the numbers that make 1344 = 8 × 168.",
    "The 168 permutations have cycle types 1 + 21 + 42 + 56 + 48 = 168: the identity, 21 involutions with three fixed points, 42 of type 4·2·1, 56 of type 3·3·1 and 48 seven-cycles. The 1344 act TRANSITIVELY on the 168 unit zero-divisor points with a point stabiliser of order 8, and extend to the sedenions. The extension 2³·PSL(2,7) does not split: no subgroup of order 168 maps onto the 168 permutations (all 64 lifts of a generating pair span the whole group of order 1344).",
    "That 168 = |PSL(2,7)| acts regularly on the 168 points: it does not, because the points are an orbit of the group of order 1344 and the stabiliser has order 8. And it is not the full automorphism group of the sedenions, which is not computed here.",
    "168 Fano permutations; 1344 signed; kernel 8 = 2³; 168 points, one orbit, stabiliser 8; cycle types {1111111: 1, 22111: 21, 421: 42, 331: 56, 7: 48}; 64 lift pairs, all spanning 1344, so split = false."),
}


def page(fname, title, sub, kind, body, script):
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
    refs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in REFS)
    out = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="bk.css">
<!-- SPDX-License-Identifier: GPL-3.0-only. {kind}: raw Canvas 2D, no libraries, no network. Code: bk.js. Data: bk_data.js, baked by build_data.py from the Python engine (box_kite 0.4). Generated by build_pages.py. -->
</head><body>{CT}
<header><h1>{html.escape(title)}</h1><div class="sub">{sub} A picture shows a structure; it is not evidence that the structure means anything beyond its definition.</div><p><a href="index.html">← Box-kite gallery</a></p></header>
<main>{body}
{ABOUT[fname]}<div class="card"><span id="selfcheck" class="sub">running self-check…</span></div></main>
<footer><p><b>Code and data.</b> Everything shown is recomputed in the browser by <code>bk.js</code> (the Cayley–Dickson table by doubling, every product, the group by enumeration) and compared with the numbers the Python engine baked into <code>bk_data.js</code>.</p><ul>{src}</ul><p><b>Literature.</b></p><ul>{refs}</ul></footer>
<script src="bk_data.js"></script><script src="bk.js"></script><script>
const BK=window.BK, D=BK.data, AX=['#d9534f','#3fa56b','#4a8fe0'];
function css(n){{return BK.css(n);}}
function tag(g,txt,x,y,fg,bg,al){{g.font='13px system-ui';const w=g.measureText(txt).width;g.fillStyle=bg;g.globalAlpha=0.82;g.fillRect(al==='c'?x-w/2-3:x-3,y-12,w+6,17);g.globalAlpha=1;g.fillStyle=fg;g.textAlign=al==='c'?'center':'left';g.fillText(txt,x,y);}}
{script}
BK.selfCheck();
</script></body></html>"""
    open(os.path.join(HERE, fname), "w", encoding="utf-8").write(out)


# ------------------------------------------------------------------ 1 one box-kite as an octahedron
page("canvas2d_octahedron.html", "One box-kite as an octahedron",
     "Six assessors on ±x, ±y, ±z; the edges are the products that vanish. Click a vertex.", "canvas2d_octahedron",
     """<div class="card"><div class="row"><label>strut s <select id="sel"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option></select></label>
<button id="vf">front</button><button id="vt">top</button><button id="vr">right</button><button id="vi">iso</button><button id="vo">orbit</button><span id="vol" class="sub">orbit: off</span>
<label><input type="checkbox" id="axes" checked> reversal axes</label><label><input type="checkbox" id="spec"> spectrum</label></div>
<canvas id="cv" width="640" height="520"></canvas><div id="spwrap" hidden><canvas id="sp" width="640" height="150"></canvas></div></div>
<div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cv=document.getElementById('cv'),sel=document.getElementById('sel'),info=document.getElementById('info'),spc=document.getElementById('sp');let pick=0,proj=[];
function setup(){const s=+sel.value,K=D.struts[s];return{s,K,C:BK.octCoords(s)};}
function names(K){return K.vertices.map(BK.label);}
function draw(v){const g=cv.getContext('2d'),W=cv.width,H=cv.height,fg=css('--fg'),card=css('--card'),mut=css('--mut'),{s,K,C}=setup();g.clearRect(0,0,W,H);
 proj=C.map(c=>v.p(c[0]*1.1,c[1]*1.1,c[2]*1.1));const nb=new Set();K.edges.forEach(e=>{if(e[0]===pick)nb.add(e[1]);if(e[1]===pick)nb.add(e[0]);});
 if(document.getElementById('axes').checked){K.non_edges.forEach((e,k)=>{g.strokeStyle=AX[k];g.globalAlpha=0.7;g.setLineDash([6,5]);g.lineWidth=1.5;g.beginPath();g.moveTo(proj[e[0]].x,proj[e[0]].y);g.lineTo(proj[e[1]].x,proj[e[1]].y);g.stroke();});g.setLineDash([]);g.globalAlpha=1;}
 K.edges.forEach(e=>{const a=proj[e[0]],b=proj[e[1]],hot=(e[0]===pick||e[1]===pick);g.strokeStyle=hot?css('--acc'):mut;g.globalAlpha=hot?1:0.55;g.lineWidth=hot?3:1.4;g.beginPath();g.moveTo(a.x,a.y);g.lineTo(b.x,b.y);g.stroke();});g.globalAlpha=1;
 const nm=names(K);const ord=[...C.keys()].sort((i,j)=>proj[j].d-proj[i].d);
 ord.forEach(i=>{const p=proj[i],k=K.non_edges.findIndex(e=>e.includes(i));g.fillStyle=AX[k];g.strokeStyle=(i===pick)?fg:card;g.lineWidth=(i===pick)?3:2;g.beginPath();g.arc(p.x,p.y,(i===pick)?11:(nb.has(i)?9:7),0,7);g.fill();g.stroke();
  tag(g,nm[i],p.x+(p.x>W/2?-14:14),p.y-12,fg,card,p.x>W/2?'r':'l');});
 g.textAlign='left';BK.gizmo(g,v,58,H-52,K.non_edges.map(e=>'('+K.vertices[e[0]][0]+','+(K.vertices[e[0]][1]+8)+')↔('+K.vertices[e[1]][0]+','+(K.vertices[e[1]][1]+8)+')'),AX);
 g.fillStyle=mut;g.font='13px system-ui';g.fillText('strut s = '+s+'   ·   assessor (a, b+8) = plane span(e_a, e_(b+8))',10,18);}
function text(){const{s,K}=setup(),V=K.vertices[pick],[a,b]=V,nm=names(K);const nbs=K.edges.filter(e=>e.includes(pick)).map(e=>e[0]===pick?e[1]:e[0]);
 let t='assessor '+nm[pick]+' = the plane span(e'+a+', e'+(b+8)+')\nstrut a XOR b = '+a+' XOR '+b+' = '+(a^b)+'   reversal partner: '+BK.label([b,a])+' (never annihilates it)\nneighbours: '+nbs.map(i=>nm[i]).join('  ')+'\n';
 [1,-1].forEach(sg=>{t+='\n'+BK.diagName(a,b,sg)+'  annihilates  '+BK.kills(a,b,sg).map(k=>BK.diagName(k[0],k[1],k[2])).join(',  ');});
 t+='\n\n(every product above was multiplied out in this browser from the Cayley–Dickson table)';info.textContent=t;}
function spectrum(){const w=document.getElementById('spwrap');w.hidden=!document.getElementById('spec').checked;if(w.hidden)return;const{K}=setup(),ev=BK.spectrum(K.edges),g=spc.getContext('2d'),fg=css('--fg'),acc=css('--acc'),mut=css('--mut');g.clearRect(0,0,640,150);
 g.font='13px system-ui';g.fillStyle=mut;g.fillText('Laplacian eigenvalues of the octahedral graph (the dispersion relation ω² on the kite)',8,16);ev.forEach((x,i)=>{const h=x*14,X=40+i*95;g.fillStyle=acc;g.fillRect(X,130-h,60,Math.max(h,1));g.fillStyle=fg;g.fillText(x.toFixed(3),X+8,124-h);});}
const view=new BK.View(cv,draw,{yaw:-0.7,pitch:0.5,onclick:(x,y)=>{let best=-1,bd=26;proj.forEach((p,i)=>{const d=Math.hypot(p.x-x,p.y-y);if(d<bd){bd=d;best=i;}});if(best>=0){pick=best;text();view.draw();}}});
function all(){view.draw();spectrum();text();}
sel.onchange=()=>{pick=0;all();};document.getElementById('axes').onchange=()=>view.draw();document.getElementById('spec').onchange=spectrum;
document.getElementById('vf').onclick=()=>view.pose(0,0);document.getElementById('vt').onclick=()=>view.pose(0,1.5708);document.getElementById('vr').onclick=()=>view.pose(-1.5708,0);document.getElementById('vi').onclick=()=>view.pose(-0.7,0.5);
document.getElementById('vo').onclick=()=>{view.orbit=!view.orbit;document.getElementById('vol').textContent='orbit: '+(view.orbit?'on':'off');};all();if(location.search.includes('spec=1')){document.getElementById('spec').checked=true;spectrum();}addEventListener('resize',()=>view.draw());
""")

# ------------------------------------------------------------------ 2 the 42 assessors
page("canvas2d_glued42.html", "All 42 assessors: seven octahedra",
     "The 42 assessors, one octahedron per strut, at seven corners of a cube; the eighth corner is e₀.", "canvas2d_glued42",
     """<div class="card"><div class="row"><label>show <select id="sel"><option value="0">all seven struts</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option></select></label>
<button id="vf">front</button><button id="vt">top</button><button id="vr">right</button><button id="vi">iso</button><button id="vo">orbit</button><span id="vol" class="sub">orbit: off</span>
<label><input type="checkbox" id="lab" checked> labels</label></div><canvas id="cv" width="700" height="560"></canvas></div>
<div class="card info"><span id="info" class="mono pre"></span></div><div class="card"><span id="stats" class="mono pre"></span></div>""",
     r"""
const cv=document.getElementById('cv'),sel=document.getElementById('sel'),info=document.getElementById('info');let proj=[];
const hue=s=>'hsl('+((s-1)*51)+',68%,52%)',R=0.36,cor=s=>[(s&1)?1:-1,(s&2)?1:-1,(s&4)?1:-1];
function draw(v){const g=cv.getContext('2d'),W=cv.width,H=cv.height,fg=css('--fg'),card=css('--card'),mut=css('--mut'),only=+sel.value,line=css('--line');g.clearRect(0,0,W,H);proj=[];
 const cube=[];for(let a=0;a<8;a++)for(let b=a+1;b<8;b++){const d=a^b;if(d===1||d===2||d===4)cube.push([a,b]);}
 const cp=a=>v.p((a&1)?1:-1,(a&2)?1:-1,(a&4)?1:-1);g.strokeStyle=line;g.lineWidth=1;cube.forEach(([a,b])=>{const p=cp(a),q=cp(b);g.beginPath();g.moveTo(p.x,p.y);g.lineTo(q.x,q.y);g.stroke();});
 const items=[];
 for(let s=1;s<8;s++){const K=D.struts[s],C=BK.octCoords(s),c0=cor(s),P=C.map(c=>v.p(c0[0]+R*c[0],c0[1]+R*c[1],c0[2]+R*c[2])),on=(!only||only===s);
  K.edges.forEach(e=>items.push({t:'e',s,a:P[e[0]],b:P[e[1]],d:(P[e[0]].d+P[e[1]].d)/2,on}));
  P.forEach((p,i)=>{items.push({t:'v',s,p,i,d:p.d,on});proj.push({s,i,p,on});});}
 items.sort((x,y)=>y.d-x.d);
 items.forEach(o=>{if(o.t==='e'){g.strokeStyle=hue(o.s);g.globalAlpha=o.on?0.9:0.12;g.lineWidth=o.on?2:1;g.beginPath();g.moveTo(o.a.x,o.a.y);g.lineTo(o.b.x,o.b.y);g.stroke();g.globalAlpha=1;}
  else{g.fillStyle=hue(o.s);g.globalAlpha=o.on?1:0.15;g.strokeStyle=card;g.lineWidth=1.5;g.beginPath();g.arc(o.p.x,o.p.y,o.on?6:4,0,7);g.fill();g.stroke();g.globalAlpha=1;
   if(o.on&&document.getElementById('lab').checked&&(only||o.i%2===0)){tag(g,BK.label(D.struts[o.s].vertices[o.i]),o.p.x+8,o.p.y-6,fg,card,'l');}}});
 const e0=cp(0);g.strokeStyle=fg;g.lineWidth=2;g.setLineDash([4,3]);g.beginPath();g.moveTo(e0.x,e0.y-9);g.lineTo(e0.x+9,e0.y);g.lineTo(e0.x,e0.y+9);g.lineTo(e0.x-9,e0.y);g.closePath();g.stroke();g.setLineDash([]);tag(g,'e₀ (outside)',e0.x+14,e0.y+4,fg,card,'l');
 for(let s=1;s<8;s++){const c=cp(s),p=v.p(cor(s)[0]*1.12,cor(s)[1]*1.12,cor(s)[2]*1.12);tag(g,'s='+s,p.x,p.y+4,hue(s),card,'c');}g.textAlign='left';
 BK.gizmo(g,v,48,H-46,['x: bit 1 of s','y: bit 2','z: bit 4'],AX);g.fillStyle=mut;g.font='13px system-ui';g.fillText('corner = binary digits of the strut (a drawing choice, not part of the graph)',10,H-12);}
const view=new BK.View(cv,draw,{yaw:-0.7,pitch:0.45,zoom:0.8,onclick:(x,y)=>{let best=null,bd=18;proj.forEach(o=>{if(!o.on)return;const d=Math.hypot(o.p.x-x,o.p.y-y);if(d<bd){bd=d;best=o;}});if(best){const K=D.struts[best.s],V=K.vertices[best.i],nb=K.edges.filter(e=>e.includes(best.i)).map(e=>K.vertices[e[0]===best.i?e[1]:e[0]]);
 info.textContent='assessor '+BK.label(V)+'  (a='+V[0]+', b='+V[1]+')  strut s = '+V[0]+' XOR '+V[1]+' = '+best.s+'\nneighbours inside kite '+best.s+': '+nb.map(BK.label).join('  ')+'\nneighbours in any other kite: none (cross-strut edges = '+D.glued.cross_strut_edges+')';}}});
function stats(){const sp=D.glued.spectrum,c={};sp.forEach(x=>{const k=Math.round(x*1000)/1000;c[k]=(c[k]||0)+1;});
 document.getElementById('stats').textContent='glued graph (engine): '+D.glued.n_vertices+' vertices, '+D.glued.n_edges+' edges; edges within a strut '+D.glued.within_strut_edges+', between struts '+D.glued.cross_strut_edges+'\nLaplacian spectrum of the union, value × multiplicity: '+Object.keys(c).map(k=>k+' × '+c[k]).join(',  ')+'\n= the octahedral spectrum {0,4,4,4,6,6} seven times: seven separate pieces, no coupling.\nHow the pieces are glued into one geometry is the engine\'s stated open item; this page does not glue them.';}
sel.onchange=()=>view.draw();document.getElementById('lab').onchange=()=>view.draw();
document.getElementById('vf').onclick=()=>view.pose(0,0);document.getElementById('vt').onclick=()=>view.pose(0,1.5708);document.getElementById('vr').onclick=()=>view.pose(-1.5708,0);document.getElementById('vi').onclick=()=>view.pose(-0.7,0.45);
document.getElementById('vo').onclick=()=>{view.orbit=!view.orbit;document.getElementById('vol').textContent='orbit: '+(view.orbit?'on':'off');};
info.textContent='Click a vertex.';stats();view.draw();addEventListener('resize',()=>view.draw());
""")

# ------------------------------------------------------------------ 3 Fano and PG(3,2)
page("canvas2d_fano.html", "The Fano plane and PG(3,2): strut = a XOR b",
     "A strut is a point of the Fano plane; the three lines through it are the three axes of its octahedron.", "canvas2d_fano",
     """<div class="card"><div class="row"><span>Left: Fano plane on e1…e7 (click a point s). Right: PG(3,2) on 1…15.</span></div>
<div class="row"><canvas id="cf" width="420" height="400" style="width:min(100%,420px)"></canvas><canvas id="cp" width="420" height="400" style="width:min(100%,420px)"></canvas></div>
<div class="row"><label>line <select id="ln"></select></label><label>plane <select id="pl"></select></label><span id="cnt" class="sub"></span></div></div>
<div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cf=document.getElementById('cf'),cpn=document.getElementById('cp'),info=document.getElementById('info'),ln=document.getElementById('ln'),pl=document.getElementById('pl');
let S=1,Q=1;const OL=D.octonion_lines,PL=D.pg_lines,PP=D.pg_planes;
// Fano layout: triangle corners 1,2,4, midpoints 3,5,6, centre 7 (the XOR layout: the midpoint of x,y is x^y)
const FP={1:[210,50],2:[60,330],4:[360,330]};FP[3]=[(FP[1][0]+FP[2][0])/2,(FP[1][1]+FP[2][1])/2];FP[5]=[(FP[1][0]+FP[4][0])/2,(FP[1][1]+FP[4][1])/2];FP[6]=[(FP[2][0]+FP[4][0])/2,(FP[2][1]+FP[4][1])/2];FP[7]=[210,237];
function lineGeom(l){const k=l.slice().sort((a,b)=>a-b).join();return k==='3,5,6'?{circle:true}:{pts:l};}
function drawFano(){const g=cf.getContext('2d'),fg=css('--fg'),card=css('--card'),mut=css('--mut'),line=css('--line');g.clearRect(0,0,420,400);
 const through=OL.filter(l=>l.includes(S)),col=l=>{const o=l.filter(x=>x!==S),K=D.struts[S],k=K.non_edges.findIndex(e=>{const a=K.vertices[e[0]],b=K.vertices[e[1]];return o.includes(a[0])&&o.includes(a[1]);});return k;};
 OL.forEach(l=>{const th=through.includes(l);g.strokeStyle=th?AX[col(l)]:line;g.lineWidth=th?5:2;g.beginPath();
  if(lineGeom(l).circle){g.arc(210,267,Math.hypot(210-FP[3][0],267-FP[3][1])*0.88,0,7);}else{const[a,b,c]=l.slice().sort((x,y)=>(Math.hypot(FP[x][0]-210,FP[x][1]-237)-Math.hypot(FP[y][0]-210,FP[y][1]-237)));
   // draw through all three collinear points: extend to the two extremes
   const pts=l.map(x=>FP[x]).sort((p,q)=>p[0]-q[0]||p[1]-q[1]);g.moveTo(pts[0][0],pts[0][1]);g.lineTo(pts[2][0],pts[2][1]);}g.stroke();});
 for(let p=1;p<8;p++){const[x,y]=FP[p];g.fillStyle=(p===S)?fg:card;g.strokeStyle=fg;g.lineWidth=2;g.beginPath();g.arc(x,y,16,0,7);g.fill();g.stroke();g.fillStyle=(p===S)?card:fg;g.font='bold 15px system-ui';g.textAlign='center';g.fillText('e'+p,x,y+5);}g.textAlign='left';
 g.fillStyle=mut;g.font='13px system-ui';g.fillText('Fano plane: lines are {a, b, a XOR b}',8,18);}
const PR=[];for(let i=0;i<15;i++){const a=-Math.PI/2+i*2*Math.PI/15;PR[i+1]=[210+155*Math.cos(a),205+155*Math.sin(a)];}
function drawPG(){const g=cpn.getContext('2d'),fg=css('--fg'),card=css('--card'),mut=css('--mut'),line=css('--line'),acc=css('--acc');g.clearRect(0,0,420,400);
 const lsel=+ln.value,psel=+pl.value,planePts=psel>=0?PP[psel]:[],through=PL.filter(l=>l.includes(Q));
 through.forEach(l=>{g.strokeStyle=acc;g.globalAlpha=0.35;g.lineWidth=1.5;g.beginPath();l.forEach((p,i)=>{i?g.lineTo(PR[p][0],PR[p][1]):g.moveTo(PR[p][0],PR[p][1]);});g.closePath();g.stroke();});g.globalAlpha=1;
 if(lsel>=0){g.strokeStyle='#e08a1e';g.lineWidth=4;g.beginPath();PL[lsel].forEach((p,i)=>{i?g.lineTo(PR[p][0],PR[p][1]):g.moveTo(PR[p][0],PR[p][1]);});g.closePath();g.stroke();}
 for(let p=1;p<16;p++){const[x,y]=PR[p],inP=planePts.includes(p),oct=(p<8);g.fillStyle=inP?'#e08a1e':(p===Q?acc:card);g.strokeStyle=oct?'#3fa56b':fg;g.lineWidth=oct?3:1.5;g.beginPath();g.arc(x,y,14,0,7);g.fill();g.stroke();g.fillStyle=(inP||p===Q)?'#000':fg;g.font='13px system-ui';g.textAlign='center';g.fillText(p,x,y+5);}g.textAlign='left';
 g.fillStyle=mut;g.font='13px system-ui';g.fillText('PG(3,2): 15 points; green rim = the octonion Fano plane (1…7)',8,392);}
function text(){const K=D.struts[S];let t='strut s = '+S+' (point e'+S+' of the Fano plane).  Lines through it:\n';
 OL.filter(l=>l.includes(S)).forEach(l=>{const o=l.filter(x=>x!==S);t+='  {'+l.join(', ')+'}  ->  reversal pair ('+o[0]+','+(o[1]+8)+') and ('+o[1]+','+(o[0]+8)+')  = one axis of the octahedron\n';});
 const th=PL.filter(l=>l.includes(Q));t+='\nPG(3,2) point '+Q+': on '+th.length+' lines  '+th.map(l=>'{'+l.join(',')+'}').join(' ')+'\n';
 const lsel=+ln.value,psel=+pl.value;if(lsel>=0)t+='line {'+PL[lsel].join(', ')+'}: '+PL[lsel][0]+' XOR '+PL[lsel][1]+' = '+PL[lsel][2]+'; lies in '+PP.filter(p=>PL[lsel].every(x=>p.includes(x))).length+' planes\n';
 if(psel>=0)t+='plane '+(psel+1)+' = {'+PP[psel].join(', ')+'}'+(PP[psel].every(x=>x<8)?'   <- the octonion plane O':'')+': holds '+PL.filter(l=>l.every(x=>PP[psel].includes(x))).length+' lines\n';
 info.textContent=t;}
cf.addEventListener('pointerdown',e=>{const r=cf.getBoundingClientRect(),x=(e.clientX-r.left)*420/r.width,y=(e.clientY-r.top)*400/r.height;for(let p=1;p<8;p++)if(Math.hypot(FP[p][0]-x,FP[p][1]-y)<20)S=p;drawFano();text();});
cpn.addEventListener('pointerdown',e=>{const r=cpn.getBoundingClientRect(),x=(e.clientX-r.left)*420/r.width,y=(e.clientY-r.top)*400/r.height;for(let p=1;p<16;p++)if(Math.hypot(PR[p][0]-x,PR[p][1]-y)<18)Q=p;drawPG();text();});
ln.innerHTML='<option value="-1">none</option>'+PL.map((l,i)=>'<option value="'+i+'">{'+l.join(',')+'}</option>').join('');
pl.innerHTML='<option value="-1">none</option>'+PP.map((p,i)=>'<option value="'+i+'">'+(i+1)+(p.every(x=>x<8)?' (octonion O)':'')+'</option>').join('');
ln.onchange=pl.onchange=()=>{drawPG();text();};
(function(){let ok=true;for(let p=1;p<16;p++)if(PL.filter(l=>l.includes(p)).length!==7)ok=false;const lp=PL.every(l=>PP.filter(q=>l.every(x=>q.includes(x))).length===3),pp=PP.every(q=>q.length===7&&PL.filter(l=>l.every(x=>q.includes(x))).length===7),xr=PL.every(l=>(l[0]^l[1])===l[2]);
 document.getElementById('cnt').textContent=D.pg_points.length+' points, '+PL.length+' lines, '+PP.length+' planes;  7 lines per point: '+ok+';  3 planes per line: '+lp+';  7 points and 7 lines per plane: '+pp+';  every line is {a, b, a XOR b}: '+xr;})();
drawFano();drawPG();text();addEventListener('resize',()=>{drawFano();drawPG();});
""")

# ------------------------------------------------------------------ 4 the associator
page("canvas2d_associator.html", "The associator: where the product bends",
     "[e_i, e_j, e_k] over the 16 basis elements: 1848 of 4096 triples do not associate, each by exactly 2.", "canvas2d_associator",
     """<div class="card"><div class="row"><label>view <select id="mode"><option value="k">one k</option><option value="n">count over k</option></select></label>
<label>k <input type="range" id="k" min="0" max="15" value="9"> <b id="kout">9</b></label><button id="kp">−</button><button id="kn">+</button></div>
<canvas id="cv" width="600" height="600" style="width:min(100%,600px)"></canvas></div>
<div class="card info"><span id="info" class="mono pre"></span></div><div class="card"><span id="blocks"></span></div>""",
     r"""
const cv=document.getElementById('cv'),kin=document.getElementById('k'),kout=document.getElementById('kout'),mode=document.getElementById('mode'),info=document.getElementById('info');
const DEF=BK.defectAll(),CELL=34,OX=44,OY=44;let sel=null;
function nCount(i,j){let n=0;for(let k=0;k<16;k++)if(DEF[i*256+j*16+k]>1e-9)n++;return n;}
function draw(){const g=cv.getContext('2d'),fg=css('--fg'),card=css('--card'),mut=css('--mut'),acc=css('--acc'),line=css('--line'),k=+kin.value,byK=mode.value==='k';g.clearRect(0,0,600,600);kout.textContent=byK?k:'—';
 g.font='12px system-ui';g.textAlign='center';
 for(let i=0;i<16;i++){g.fillStyle=mut;g.fillText('e'+i,OX-18,OY+i*CELL+CELL/2+4);g.fillText('e'+i,OX+i*CELL+CELL/2,OY-10);}
 for(let i=0;i<16;i++)for(let j=0;j<16;j++){const v=byK?DEF[i*256+j*16+k]:nCount(i,j),x=OX+j*CELL,y=OY+i*CELL;
  g.fillStyle=v>1e-9?(byK?acc:'hsl(30,85%,'+(78-v*3.2)+'%)'):card;g.fillRect(x,y,CELL-1,CELL-1);if(v>1e-9){g.fillStyle=byK?card:'#000';g.fillText(byK?'2':v,x+CELL/2,y+CELL/2+4);}
  if(sel&&sel[0]===i&&sel[1]===j){g.strokeStyle=fg;g.lineWidth=3;g.strokeRect(x,y,CELL-1,CELL-1);}}
 g.setLineDash([3,4]);g.strokeStyle=fg;g.lineWidth=1.5;g.beginPath();g.moveTo(OX+8*CELL-0.5,OY);g.lineTo(OX+8*CELL-0.5,OY+16*CELL);g.moveTo(OX,OY+8*CELL-0.5);g.lineTo(OX+16*CELL,OY+8*CELL-0.5);g.stroke();g.setLineDash([]);
 g.textAlign='left';g.fillStyle=mut;g.fillText(byK?'row i, column j, for k = '+k+':  filled = [e_i, e_j, e_'+k+'] is not zero':'for each (i, j): how many k make [e_i, e_j, e_k] non-zero',OX,18);g.fillText('dotted lines: octonion indices 0…7 | doubled half 8…15',OX,OY+16*CELL+22);}
function text(){if(!sel){info.textContent='Click a cell.';return;}const[i,j]=sel,k=+kin.value,v=BK.assoc(i,j,k),nz=v.map((c,m)=>c?(c>0?'+':'−')+Math.abs(c)+' e'+m:'').filter(Boolean);
 const[s1,m]=BK.mul(i,j),[s2,n]=BK.mul(m,k),[s3,q]=BK.mul(j,k),[s4,r]=BK.mul(i,q);
 info.textContent='[e'+i+', e'+j+', e'+k+']  =  (e'+i+' e'+j+') e'+k+'  −  e'+i+' (e'+j+' e'+k+')\n(e'+i+' e'+j+') e'+k+'  =  '+(s1*s2>0?'+':'−')+'e'+n+'\ne'+i+' (e'+j+' e'+k+')  =  '+(s3*s4>0?'+':'−')+'e'+r+'\ndifference  =  '+(nz.length?nz.join('  '):'0   (associative here)')+'      norm '+Math.hypot(...v);}
cv.addEventListener('pointerdown',e=>{const r=cv.getBoundingClientRect(),x=(e.clientX-r.left)*600/r.width,y=(e.clientY-r.top)*600/r.height,j=Math.floor((x-OX)/CELL),i=Math.floor((y-OY)/CELL);if(i>=0&&i<16&&j>=0&&j<16){sel=[i,j];draw();text();}});
kin.oninput=()=>{draw();text();};mode.onchange=()=>{draw();text();};document.getElementById('kp').onclick=()=>{kin.value=(+kin.value+15)%16;draw();text();};document.getElementById('kn').onclick=()=>{kin.value=(+kin.value+1)%16;draw();text();};
(function(){const names=['O','H'],cnt={};let tot=0;for(let i=0;i<16;i++)for(let j=0;j<16;j++)for(let k=0;k<16;k++)if(DEF[i*256+j*16+k]>1e-9){const key=(i>7?'H':'O')+(j>7?'H':'O')+(k>7?'H':'O');cnt[key]=(cnt[key]||0)+1;tot++;}
 const vals=new Set(Array.from(DEF).map(x=>Math.round(x*1e6)/1e6));let rows='';['OOO','OOH','OHO','OHH','HOO','HOH','HHO','HHH'].forEach(b=>{rows+='<tr><td class="mono">'+b+'</td><td>'+cnt[b]+'</td><td>'+(512)+'</td></tr>';});
 document.getElementById('blocks').innerHTML='<b>Non-zero triples by block</b> (O: index 0…7, H: index 8…15 for i, j, k): <table><tr><th>block</th><th>non-zero</th><th>of</th></tr>'+rows+'<tr><th>all</th><th>'+tot+'</th><th>4096</th></tr></table><p class="sub">Distinct norms in the whole table: {'+[...vals].sort((a,b)=>a-b).join(', ')+'}: the associator is 0 or exactly 2.</p>';})();
draw();text();
""")

# ------------------------------------------------------------------ 5 the group
page("canvas2d_group.html", "The group 1344 = 8 × 168 acting on the seven kites",
     "Signed permutations of the octonion units that keep the table; their action on the seven struts; the eight sign changes that fix every kite.", "canvas2d_group",
     """<div class="card"><div class="row"><label>cycle type <select id="ct"></select></label><button id="pv">◀</button><button id="nx">▶</button><button id="rd">random</button><span id="idx" class="sub"></span></div>
<canvas id="cv" width="520" height="440" style="width:min(100%,520px)"></canvas></div>
<div class="card info"><span id="info" class="mono pre"></span></div><div class="card"><span id="tbl" class="mono pre"></span></div>""",
     r"""
const cv=document.getElementById('cv'),ct=document.getElementById('ct'),info=document.getElementById('info'),G=BK.group();
const hue=s=>'hsl('+((s-1)*51)+',68%,52%)';let list=G.fano,at=0;const CY=[['#d9534f'],['#4a8fe0'],['#3fa56b'],['#e08a1e'],['#9b59b6']];
const types={};G.fano.forEach(p=>{const t=BK.cycleType(p);(types[t]=types[t]||[]).push(p);});const names={'1111111':'identity','22111':'2 2 (3 fixed)','421':'4 2 (1 fixed)','331':'3 3 (1 fixed)','7':'one 7-cycle'};
ct.innerHTML='<option value="all">all 168</option>'+Object.keys(types).sort((a,b)=>types[a].length-types[b].length).map(t=>'<option value="'+t+'">'+(names[t]||t)+' ('+types[t].length+')</option>').join('');
const POS=s=>{const a=-Math.PI/2+(s-1)*2*Math.PI/7;return[260+160*Math.cos(a),215+160*Math.sin(a)];};
function arrow(g,a,b,c){const dx=b[0]-a[0],dy=b[1]-a[1],L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L,s=[a[0]+ux*20,a[1]+uy*20],e=[b[0]-ux*22,b[1]-uy*22];g.strokeStyle=c;g.fillStyle=c;g.lineWidth=2.5;g.beginPath();g.moveTo(s[0],s[1]);g.lineTo(e[0],e[1]);g.stroke();g.beginPath();g.moveTo(e[0],e[1]);g.lineTo(e[0]-ux*10-uy*5,e[1]-uy*10+ux*5);g.lineTo(e[0]-ux*10+uy*5,e[1]-uy*10-ux*5);g.closePath();g.fill();}
function draw(){const g=cv.getContext('2d'),fg=css('--fg'),card=css('--card'),mut=css('--mut'),p=list[at],cy=BK.cycles(p);g.clearRect(0,0,520,440);
 cy.forEach((c,ci)=>{const col=CY[ci%5][0];if(c.length===1){const[x,y]=POS(c[0]);g.strokeStyle=col;g.lineWidth=3;g.beginPath();g.arc(x,y,26,0,7);g.stroke();}
  else c.forEach((s,i)=>{arrow(g,POS(s),POS(c[(i+1)%c.length]),col);});});
 for(let s=1;s<8;s++){const[x,y]=POS(s);g.fillStyle=hue(s);g.strokeStyle=card;g.lineWidth=2;g.beginPath();g.arc(x,y,18,0,7);g.fill();g.stroke();g.fillStyle='#000';g.font='bold 15px system-ui';g.textAlign='center';g.fillText(s,x,y+5);}g.textAlign='left';
 g.fillStyle=mut;g.font='13px system-ui';g.fillText('the seven box-kites (struts 1…7)',8,18);g.fillText('an arrow s → π(s): the group element sends kite s to kite π(s)',8,36);
 document.getElementById('idx').textContent='permutation '+(at+1)+' of '+list.length+'   cycle type '+BK.cycleType(p);
 const imgs=p.map((x,i)=>(i+1)+'→'+x).join('  '),lifts=G.all.filter(e=>e.p.join('')===p.join('')).map(e=>e.g.slice(1).map(x=>x>0?'+':'−').join(''));
 info.textContent='π: '+imgs+'\ncycles: '+cy.map(c=>'('+c.join(' ')+')').join(' ')+'\nthe 8 signed automorphisms over this permutation (signs on e1…e7): '+lifts.join('  ');}
function fill(){const G2=G.all,o=BK.orbitOfPoint(),kernel=G2.filter(e=>e.p.every((x,i)=>x===i+1));let t='|signed automorphisms| = '+G2.length+'   |Fano permutations| = '+G.fano.length+'   kernel (sign changes fixing every kite) = '+kernel.length+'\n1344 = 8 × 168\n\ncycle types of the 168 permutations on the 7 struts:\n';
 Object.keys(types).sort((a,b)=>types[a].length-types[b].length).forEach(k=>{t+='  '+(names[k]||k).padEnd(18)+String(types[k].length).padStart(4)+'\n';});t+='  '+'total'.padEnd(18)+String(G.fano.length).padStart(4)+'\n';
 t+='\nthe 8 sign changes that fix every kite (signs on e1…e7): '+kernel.map(e=>e.g.slice(1).map(x=>x>0?'+':'−').join('')).join('  ')+'\n';
 t+='\nacting on the 168 unit zero-divisor points: orbit of one point = '+o.orbit+', stabiliser order = '+o.stabiliser+'  (1344 / 168 = 8)\n';
 const sp=BK.split();t+='\ndoes 2³·PSL(2,7) split?  '+sp.tried+' lifts of a generating pair tried, subgroup orders spanned: '+sp.orders.join(', ')+'  ->  split = '+sp.split+'  (non-split: no subgroup of order 168 maps onto the 168 permutations)';document.getElementById('tbl').textContent=t;}
function setList(){const v=ct.value;list=v==='all'?G.fano:types[v];at=0;draw();}
ct.onchange=setList;document.getElementById('pv').onclick=()=>{at=(at+list.length-1)%list.length;draw();};document.getElementById('nx').onclick=()=>{at=(at+1)%list.length;draw();};document.getElementById('rd').onclick=()=>{at=Math.floor(Math.random()*list.length);draw();};
ct.value='7';setList();fill();addEventListener('resize',draw);
""")

# ------------------------------------------------------------------ index
cards = [
    ("canvas2d_octahedron.html", "One box-kite as an octahedron", "Pick a strut; six assessors on ±x, ±y, ±z; click a vertex for the four diagonals it annihilates; the {0,4,4,4,6,6} spectrum."),
    ("canvas2d_glued42.html", "All 42 assessors: seven octahedra", "The seven kites at seven corners of a cube, e₀ at the eighth; 84 edges, none between kites. The gluing is the engine's open item and is not faked."),
    ("canvas2d_fano.html", "Fano plane and PG(3,2)", "strut = a XOR b: a strut is a Fano point and its three lines are the octahedron's three axes; the 15 / 35 / 15 geometry on the sedenion indices."),
    ("canvas2d_associator.html", "The associator", "A 16 × 16 map of where the product bends: 1848 of 4096 triples, each by exactly 2; the octonion block is not flat (168 of 512)."),
    ("canvas2d_group.html", "The group 1344 = 8 × 168", "Its action on the seven kites, the 168 permutations by cycle type, the 8 sign changes, orbit and stabiliser, and the non-split result."),
]
cards_html = "".join(f'<div class="card"><h2 style="font-size:17px;margin:0"><a href="{u}">{html.escape(t)}</a></h2><span class="tag">canvas2d_</span><p>{html.escape(d)}</p></div>' for u, t, d in cards)
cards_html += '<div class="card"><h2 style="font-size:17px;margin:0">OpenSCAD companion</h2><span class="tag">scad</span><p>A printable octahedron with the six assessors of any strut labelled on its vertices: <a href="box_kite_octahedron.scad">box_kite_octahedron.scad</a> (STL and renders beside it).</p><p><img src="box_kite_octahedron_A.png" alt="OpenSCAD render of the strut-1 octahedron" style="max-width:100%;border:1px solid var(--line);border-radius:6px"></p></div>'
cards_html += '<div class="card"><h2 style="font-size:17px;margin:0">Code flow chart</h2><span class="tag">svg</span><p>The call graph of the engine in ISO 5807 symbols, derived from the source by <code>tools/flowchart.py</code>: <a href="../../docs/flowcharts/box_kite.svg">box_kite.svg</a>.</p></div>'
src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Box-Kite Gallery</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="bk.css"><!-- SPDX-License-Identifier: GPL-3.0-only. Generated by build_pages.py. --></head><body>{CT}
<header><h1>Box-kites: interactive visualizations</h1><div class="sub">ValaQuenta engine 5, <code>modules/box_kite</code> (0.4). Five pages and an OpenSCAD companion, each recomputing its numbers in the browser and comparing them with the Python engine. A picture shows a structure; it is not evidence that the structure means anything beyond its definition.</div></header>
<main>{cards_html}</main>
<footer><p><b>Sources.</b></p><ul>{src}</ul><p>Launch: <code>gallery/box_kite/serve_gallery.sh</code> (loopback only, port 8793).</p></footer></body></html>""")
print("pages written")
