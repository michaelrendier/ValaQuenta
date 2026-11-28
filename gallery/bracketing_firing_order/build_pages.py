#!/usr/bin/env python3
"""build_pages.py -- writes the five canvas2d_*.html pages and index.html of the bracketing_firing_order gallery from one shared chrome.
Page logic is in the JS strings below; the maths is in bf.js, checked against bf_data.js (baked by build_data.py from the Python engine).
Run:  python3 build_pages.py"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/michaelrendier"
SOURCES = [
    (f"{GH}/ValaQuenta/blob/main/modules/bracketing_firing_order/maths.py", "ValaQuenta/modules/bracketing_firing_order/maths.py", "the Python engine these pages port and check against (plans, the four orderings, both readings, evolve, set membership)"),
    (f"{GH}/ValaQuenta/blob/main/wiki/bracketing_firing_order.md", "ValaQuenta/wiki/bracketing_firing_order.md", "the record page, with the four orderings and the claim table"),
    (f"{GH}/ValaQuenta/blob/main/tests/test_bracketing_firing_order.py", "ValaQuenta/tests/test_bracketing_firing_order.py", "the tests (17)"),
    (f"{GH}/GenerationalLineage/blob/main/engine/bracketing_firing_order.py", "GenerationalLineage/engine/bracketing_firing_order.py", "the standalone port (tool 4: plans)"),
    (f"{GH}/SedenionSpectralRelativity/blob/main/firing_plan.py", "SedenionSpectralRelativity/firing_plan.py", "the origin of the plan layer"),
    (f"{GH}/ValaQuenta/blob/main/modules/h_rb_hat/sigma16.py", "ValaQuenta/modules/h_rb_hat/sigma16.py", "the 16-component σ_RB input and output of Ĥ_RB (lift B, used on the first page)"),
]
REFS = [
    ("Wikipedia, \"Catalan number\": the number of binary bracketings, Catalan(n−1).", "https://en.wikipedia.org/wiki/Catalan_number"),
    ("Wikipedia, \"Bell number\": the number of set partitions.", "https://en.wikipedia.org/wiki/Bell_number"),
    ("Wikipedia, \"Separable permutation\": the orders reached by written-order bracketings (6, 22, 90 for n = 3, 4, 5).", "https://en.wikipedia.org/wiki/Separable_permutation"),
    ("N. J. A. Sloane, OEIS A005132: Recamán's sequence, whose flip is a set-membership test.", "https://oeis.org/A005132"),
    ("R. D. Schafer, An Introduction to Nonassociative Algebras (Academic Press, 1966): the sedenions are not associative.", "https://archive.org/details/introductiontono0000scha"),
    ("R. P. C. de Marrais, \"The 42 Assessors and the Box-Kites They Fly\", arXiv:math/0011260 (2000).", "https://arxiv.org/abs/math/0011260"),
    ("The Python Software Foundation, Python 3 documentation: itertools.permutations, fractions.Fraction.", "https://docs.python.org/3/library/itertools.html"),
    ("MDN Web Docs, Canvas API and BigInt.", "https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API"),
]
CT = ('<div class="ct"><b>Michael Rendier</b> <a href="mailto:the.wandering.god@gmail.com">✉ the.wandering.god@gmail.com</a> · '
      '<a href="https://facebook.com/rendier" target="_blank" rel="noopener">Facebook</a> · <a href="https://orcid.org/0009-0007-7239-6760" target="_blank" rel="noopener">ORCID 0009-0007-7239-6760</a></div>')


def about_card(looking, read, shows, not_shows, numbers):
    """The information panel every visual carries."""
    return ('<div class="card"><b>About this visual</b>'
            f'<p><b>What you are looking at.</b> {looking}</p><p><b>How to read it.</b> {read}</p>'
            f'<p><b>What it shows.</b> {shows}</p><p><b>What it does not show.</b> {not_shows}</p><p><b>Numbers to check.</b> {numbers}</p></div>')


ABOUT = {
 "canvas2d_evolve.html": about_card(
    "A sedenion as a 16-component vector on the axes e₀…e₁₅ (the î ĵ k̂ of sixteen dimensions), and what a plan does to it. The input is the vector you set; each panel is the vector after one more step fires, drawn as 16 bars (dashed outline: the previous panel). The last panel is the output. Ĥ_RB has the same shape: one 16-component σ_RB in, one 16-component sedenion out.",
    "Set the input (or pick a preset, including the σ_RB of the h_rb_hat engine). Choose up to four items from the library: the input itself, a basis unit, an editable-preset sedenion a₁…a₄, or the Ĥ_RB coupling element C. Pick a tab: A bracketing, B firing order, C firing order of brackets, D bracketing of firing orders, then a plan from its list. Switch the reading: <b>operator</b> multiplies the input by the items' left-multiplication matrices in firing order (each panel is the vector after one item fires); <b>element</b> multiplies the sedenions themselves, panel by panel in the order the products are computed.",
    "That under the operator reading the bracketing does nothing (matrices associate) and only the firing order moves the output, while under the element reading the bracketing moves it too, because the sedenion product is not associative. The table under the picture puts the input, the output and the change side by side for every component.",
    "A quantum measurement, a physical evolution or a claim about what Ĥ_RB does with σ_RB: the Ĥ_RB leaf is lift B of the h_rb_hat engine (a definition chosen to be testable, status OPEN there). The element reading has no separate input; put the input in as an item (source x) to make it part of the product.",
    "n = 3, input e₁ + e₁₀, plan ((A B | 2 1) C | 2 1) with the engine's a₁, a₂, a₃ fires C, B, A; its operator output starts −7, 1, −28, 12, 30, … and its element value starts 2, 9, 13, 7, 13, …"),
 "canvas2d_allplans.html": about_card(
    "Every plan of one kind over 3 or 4 items, as a grid: the plan's notation, the 16 components of its output, and a coloured frame shared by plans that give the same output vector.",
    "Choose A, B, C or D, the reading, the number of items and the item set. A frame colour that repeats means those plans agree. Click a cell for its output components and its firing sequence.",
    "How many different vectors each kind makes. For generic sedenions in the element reading every plan is different (3 items: 2, 6, 8, 12 plans, all distinct; 4 items: 5, 24, 40, 120). In the operator reading the outputs follow the firing sequence only, so A gives one output and C gives as many as it reaches orders (22 for four items). The item sets show where plans collapse: one sedenion repeated (power-associative: the brackets stop mattering) and real scalars (everything commutes and associates).",
    "Which plan is right: the page does not rank plans. Plans of one kind overlap those of another (A, B and C are all inside D), so the counts are plan counts, not counts of distinct vectors over the union.",
    "Counts of plans: A 2, 5; B 6, 24; C 8, 40; D 12, 120 (n = 3, 4); fire sequences reached with n = 4: 1, 24, 22, 24."),
 "canvas2d_tree.html": about_card(
    "One plan drawn as a tree. Leaves are the items, each bracket is one operation, and the small numbered badge on a branch says when that child fires inside its bracket (1 first).",
    "Pick the items' order (a firing order of the leaves), the shape (flat, or one of the binary groupings of the fired sequence) and click a bracket to change its order: a binary bracket swaps, a flat bracket steps through all n! orders. The page says which kind the plan is: A, B, C or D, or a mixture. Both readings' outputs are drawn on the right.",
    "That the four kinds are four different choices on one object: A changes only the grouping, B only the order inside one bracket, C the orders on a fixed grouping, D the order of the leaves before the grouping (so it can group items that were not neighbours, as in ((A C) B)).",
    "That the tree is a geometry of the sedenion. It is the structure of the plan; the sedenion vectors appear only in the output panels.",
    "((A B | 2 1) C | 2 1): bracket badges 2 1 inside and 2 1 outside, fire sequence C B A, kind C. Flat with order 3 1 2 is B."),
 "canvas2d_counts.html": about_card(
    "How many plans there are, for n items from 1 to 16, on a log scale: A (Catalan(n−1)), B (n!), C (Catalan(n−1)·2ⁿ⁻¹), D (n!·Catalan(n−1)), and for comparison Bell(n) (set partitions, tool 1) and 2ⁿ⁻¹ (contiguous blocks, which is what the Emerger's {4:8:4} is).",
    "Read the height as the number of digits. The table below gives every value exactly (computed with BigInt in the browser).",
    "D is the largest kind and contains A, B and C: D = (2n−2)!/(n−1)!, every ordered binary product of the n items. At n = 16: Bell 10,480,142,147; contiguous blocks 32,768; A 9,694,845; D 202,843,204,931,727,360,000. Three different meanings of bracketing give three different counts, so a claim should say which.",
    "Which plans matter. A count is not a measure of importance, and these are plan counts, not counts of distinct outputs.",
    "n = 3: A 2, B 6, C 8, D 12; n = 16: Bell(16) = 10,480,142,147; 2¹⁵ = 32,768."),
 "canvas2d_membership.html": about_card(
    "Set membership, the third tool of the engine: a memory of where a sequence has been. Any sequence of functions can be run from a starting number; the page records the positions visited, finds the returns (collisions), and answers, before a step is taken, whether it would land on a visited position.",
    "Pick Recamán's sequence (the flip between subtracting and adding is exactly this membership test), a preset word, or build your own from the buttons. Under the picture are the collisions and the verdicts of the flip test for candidate next steps. The second panel is the jurisdiction check: a map from each object to the operations legal for it, and a request tested against it.",
    "That Recamán's rule is a set-membership test against the whole history, not a threshold (the first terms 0, 1, 3, 6, 2, 7, 13, 20, 12, 21, 11, 22 come out of the engine's would_collide); that Recamán's sequence still revisits some numbers, because only the down-step is tested; that a word can return to a position it left (+2 then −2); and that a violation of a jurisdiction is a failed membership test, nothing more.",
    "Anything about why Recamán's sequence behaves as it does (that is open), or any claim that the jurisdictions in the default map are the right ones: the map is supplied by the caller and the page only tests membership.",
    "Recamán, 40 terms, equal to the engine's (OEIS A005132); +2, −2 from 1: collision (0, 2) at 1; lineage with build_up: violation, emerger with build_up: legal."),
}


def page(fname, title, sub, kind, body, script):
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
    refs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in REFS)
    shell = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>@TITLE@</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="bf.css">
<!-- SPDX-License-Identifier: GPL-3.0-only. @KIND@: raw Canvas 2D, no libraries, no network. Code: bf.js. Data: bf_data.js, baked by build_data.py from the Python engine (bracketing_firing_order 0.2). Generated by build_pages.py. -->
</head><body>@CT@
<header><h1>@TITLE@</h1><div class="sub">@SUB@ A picture shows a structure; it is not evidence that the structure means anything beyond its definition.</div><p><a href="index.html">← Bracketing and firing order gallery</a></p></header>
<main>@BODY@
@ABOUT@<div class="card"><span id="selfcheck" class="sub">running self-check…</span></div></main>
<footer><p><b>Code and data.</b> Everything shown is recomputed in the browser by <code>bf.js</code> (the sedenion product, the plans, the four orderings, both readings, exact counts with BigInt, set membership) and compared with the numbers the Python engine produced (<code>bf_data.js</code>); the result is printed above. Light and dark follow the system.</p>
<p><b>GitHub sources.</b></p><ul>@SRC@</ul><p><b>Literature and documentation.</b></p><ul>@REFS@</ul></footer>
<script src="bf_data.js"></script><script src="bf.js"></script><script>
const A=window.BFB, D=A.data, $=id=>document.getElementById(id), css=n=>A.css(n);
const COL=['#4a8fe0','#d9534f','#3fa56b','#d4a017'];
const PRE={a1:D.A,a2:D.B,a3:D.C,a4:D.D,hrb:D.hrb.C};
const SRCNAMES={x:'x (the input)',a1:'a₁',a2:'a₂',a3:'a₃',a4:'a₄',hrb:'Ĥ_RB coupling C'};
function srcVec(s,x){if(s==='x')return x.slice();if(s[0]==='e')return A.unit(+s.slice(1));return PRE[s].slice();}
function srcOptions(){let h='';Object.keys(SRCNAMES).forEach(k=>h+='<option value="'+k+'">'+SRCNAMES[k]+'</option>');for(let i=1;i<16;i++)h+='<option value="e'+i+'">e'+i+' (basis unit)</option>';return h;}
function tag(g,txt,x,y,fg,bg,al){g.font='12px system-ui';const w=g.measureText(txt).width;g.fillStyle=bg;g.globalAlpha=0.85;g.fillRect(al==='c'?x-w/2-3:x-3,y-12,w+6,16);g.globalAlpha=1;g.fillStyle=fg;g.textAlign=al==='c'?'center':'left';g.fillText(txt,x,y);g.textAlign='left';}
const norm=v=>Math.sqrt(v.reduce((s,a)=>s+a*a,0));
function kindOf(plan,leafPerm){const ords=[];(function w(p){if(p.t==='B'){ords.push(p);p.kids.forEach(w);}})(plan);const flat=plan.t==='B'&&plan.kids.every(k=>k.t==='L'),def=ords.every(b=>b.order.every((o,i)=>o===i+1)),ident=leafPerm.every((p,i)=>p===i);
 if(flat&&ords.length===1&&!def&&ident)return 'B (firing order)';if(flat&&def&&ident)return 'one flat bracket in written order (a bracketing with no order change)';
 if(ident&&def)return 'A (bracketing)';if(ident)return 'C (firing order of brackets)';if(def)return 'D (bracketing of a firing order)';return 'D with orders on its brackets (a redundant spelling of a D plan)';}
@SCRIPT@
A.selfCheck();
</script></body></html>"""
    out = (shell.replace("@TITLE@", html.escape(title)).replace("@KIND@", kind).replace("@CT@", CT).replace("@SUB@", sub).replace("@BODY@", body)
           .replace("@ABOUT@", ABOUT[fname]).replace("@SRC@", src).replace("@REFS@", refs).replace("@SCRIPT@", script))
    open(os.path.join(HERE, fname), "w", encoding="utf-8").write(out)


# ------------------------------------------------------------------ 1 the evolving sedenion
page("canvas2d_evolve.html", "The evolving sedenion: input to output",
     "A 16-component vector on e₀…e₁₅, and what bracketings, firing orders, firing orders of brackets and bracketings of firing orders do to it.", "canvas2d_evolve",
     """<div class="card"><b>Input sedenion</b> <label>preset <select id="pre"><option value="a">e₁ + e₁₀</option><option value="b">e₀ (the identity)</option><option value="c">σ_RB of the h_rb_hat engine</option><option value="d">e₃</option></select></label>
<div class="grid16" id="xg"></div>
<div class="row"><label>items n <select id="n"><option>3</option><option>4</option></select></label><span id="lib"></span></div>
<div class="row tabs"><span>kind:</span><button data-m="A" class="on">A bracketing</button><button data-m="B">B firing order</button><button data-m="C">C firing order of brackets</button><button data-m="D">D bracketing of firing orders</button>
<label>reading <select id="rd"><option value="operator">operator (matrices)</option><option value="element">element (sedenion product)</option></select></label>
<label><input type="checkbox" id="sh"> same scale on every panel</label></div>
<div class="row"><label>plan <select id="pl" style="max-width:340px"></select></label><button id="pv">◀</button><button id="nx">▶</button><span id="cnt" class="sub"></span></div>
<canvas id="cv" width="940" height="420"></canvas><div style="overflow-x:auto"><table id="tb" class="mono"></table></div></div><div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cv=$('cv');let mode='A',plans=[],idx=0;
const XS={a:A.unit(1).map((v,i)=>v+(i===10?1:0)),b:A.unit(0),c:D.hrb.sigma.map(v=>v),d:A.unit(3)};
function setX(v){v.forEach((a,i)=>$('x'+i).value=a);}
let h='';for(let i=0;i<16;i++)h+='<label>e'+i+'<input type="number" id="x'+i+'" step="0.1" value="0"></label>';$('xg').innerHTML=h;
let lh='';for(let i=0;i<4;i++)lh+='<label>item '+'ABCD'[i]+' <select id="s'+i+'">'+srcOptions()+'</select></label> ';$('lib').innerHTML=lh;
['a2','a3','a1','a4'].forEach((s,i)=>$('s'+i).value=['a1','a2','a3','a4'][i]);
function X(){return Array.from({length:16},(_,i)=>+$('x'+i).value||0);}
function leaves(){const x=X();return Array.from({length:+$('n').value},(_,i)=>A.leaf('ABCD'[i],srcVec($('s'+i).value,x)));}
function build(){plans=A.plans(mode,leaves());$('pl').innerHTML=plans.map((p,i)=>'<option value="'+i+'">'+(i+1)+'. '+A.notation(p)+'   fires '+A.fireSeq(p).join(' ')+'</option>').join('');idx=Math.min(idx,plans.length-1);$('pl').value=idx;draw();}
function draw(){const g=cv.getContext('2d'),fg=css('--fg'),mut=css('--mut'),card=css('--card'),line=css('--line'),acc=css('--acc'),x=X(),ls=leaves(),plan=A.plans(mode,ls)[idx],reading=$('rd').value;g.clearRect(0,0,cv.width,cv.height);
 let states=reading==='operator'?A.evolveOperator(plan,x):[['input x (pinned)',x]].concat(A.evolveValue(plan)),out=reading==='operator'?states[states.length-1][1]:A.valueOf(plan);
 const sc=Math.max(1,...states.map(s=>Math.max(...s[1].map(Math.abs)))),W=cv.width,pw=220,ph=120,cols=Math.floor(W/(pw+10)),rows=Math.ceil(states.length/cols);cv.height=rows*(ph+54)+10;
 states.forEach((s,i)=>{const cx=10+(i%cols)*(pw+10),cy=8+Math.floor(i/cols)*(ph+54),last=(i===states.length-1),first=(reading==='operator'&&i===0);
  g.fillStyle=card;g.strokeStyle=last?COL[2]:first?COL[3]:line;g.lineWidth=last||first?2.5:1;g.fillRect(cx,cy,pw,ph+44);g.strokeRect(cx,cy,pw,ph+44);
  g.fillStyle=fg;g.font='12px system-ui';const prev=i>0&&reading==='operator'?states[i-1][1]:null,d=prev?norm(s[1].map((v,k)=>v-prev[k])):0;
  const psc=$('sh').checked?sc:Math.max(1e-9,...s[1].map(Math.abs),...(prev?prev.map(Math.abs):[0]));
  g.fillText((first?'INPUT':last&&reading==='operator'?'OUTPUT, after '+s[0]:reading==='operator'?'after '+s[0]:s[0]),cx+6,cy+15);g.fillStyle=mut;g.fillText('|v| = '+A.fmt(norm(s[1]))+(prev?'   |Δ| = '+A.fmt(d):'')+(psc!==sc?'   full height = '+A.fmt(psc):''),cx+6,cy+30);
  A.bars(g,s[1],cx+6,cy+38,pw-12,ph-36,psc,last?COL[2]:COL[0],prev,fg,mut);});
 const inp=x,o=out;$('tb').innerHTML='<tr><th></th>'+inp.map((_,i)=>'<th>e'+i+'</th>').join('')+'</tr><tr><th>input</th>'+inp.map(v=>'<td>'+A.fmt(v)+'</td>').join('')+'</tr><tr><th>output</th>'+o.map(v=>'<td>'+A.fmt(v)+'</td>').join('')+'</tr><tr><th>Δ</th>'+o.map((v,i)=>'<td>'+A.fmt(v-inp[i])+'</td>').join('')+'</tr>';
 const other=reading==='operator'?A.valueOf(plan):A.applyPlan(plan,x);
 $('cnt').textContent='plan '+(idx+1)+' of '+plans.length;
 $('info').textContent='plan '+A.notation(plan)+'   fires '+A.fireSeq(plan).join(' → ')+'   kind '+kindOf(plan,ls.map((_,i)=>i))+'\nreading: '+reading+'   |input| = '+A.fmt(norm(x))+'   |output| = '+A.fmt(norm(out))+'   |output − input| = '+A.fmt(norm(out.map((v,i)=>v-x[i])))+
 '\nthe other reading gives '+(JSON.stringify(other)===JSON.stringify(out)?'the SAME output for this plan':'a DIFFERENT output (|difference| = '+A.fmt(norm(other.map((v,i)=>v-out[i])))+')')+
 '\n'+(reading==='operator'?'operator reading: matrices associate, so only the firing order changes the output; every bracketing at written order gives one output.':'element reading: the sedenion product is not associative, so the bracketing changes the output as well. The input x is part of the product only if an item takes source x.')+
 '\nitems: '+ls.map((l,i)=>'ABCD'[i]+' = '+SRCNAMES[$('s'+i).value]||('ABCD'[i]+' = '+$('s'+i).value)).join('   ');}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{mode=b.dataset.m;document.querySelectorAll('.tabs button').forEach(c=>c.classList.toggle('on',c===b));idx=0;build();});
$('pl').onchange=()=>{idx=+$('pl').value;draw();};$('pv').onclick=()=>{idx=(idx+plans.length-1)%plans.length;$('pl').value=idx;draw();};$('nx').onclick=()=>{idx=(idx+1)%plans.length;$('pl').value=idx;draw();};
$('rd').onchange=draw;$('sh').onchange=draw;$('n').onchange=()=>{idx=0;build();};$('pre').onchange=()=>{setX(XS[$('pre').value]);build();};
for(let i=0;i<4;i++)$('s'+i).onchange=build;for(let i=0;i<16;i++)$('x'+i).oninput=build;setX(XS.a);
const Q=new URLSearchParams(location.search);if(Q.get('n'))$('n').value=Q.get('n');if(Q.get('rd'))$('rd').value=Q.get('rd');if(Q.get('sh'))$('sh').checked=true;if(Q.get('m')){mode=Q.get('m');document.querySelectorAll('.tabs button').forEach(c=>c.classList.toggle('on',c.dataset.m===mode));}if(Q.get('i'))idx=+Q.get('i');build();
""")

# ------------------------------------------------------------------ 2 all the plans of one kind
page("canvas2d_allplans.html", "Every plan of one kind, and which agree",
     "All plans of A, B, C or D over three or four items, each with its output vector; a shared frame colour marks plans that give the same output.", "canvas2d_allplans",
     """<div class="card"><div class="row tabs"><span>kind:</span><button data-m="A" class="on">A bracketing</button><button data-m="B">B firing order</button><button data-m="C">C firing order of brackets</button><button data-m="D">D bracketing of firing orders</button></div>
<div class="row"><label>reading <select id="rd"><option value="element">element (sedenion product)</option><option value="operator">operator (matrices on the input)</option></select></label>
<label>items n <select id="n"><option>3</option><option>4</option></select></label>
<label>item set <select id="set"><option value="gen">generic: a₁ a₂ a₃ a₄</option><option value="bas">basis units e₁ e₁₀ e₁₂ e₅</option><option value="same">one sedenion repeated: a₁ a₁ a₁ a₁</option><option value="real">real scalars 2 3 5 7</option></select></label></div>
<div id="stat" class="sub"></div><canvas id="cv" width="960" height="600"></canvas></div><div class="card info"><span id="info" class="mono pre">click a cell</span></div>""",
     r"""
const cv=$('cv');let mode='A',cells=[];
const SETS={gen:[D.A,D.B,D.C,D.D],bas:[A.unit(1),A.unit(10),A.unit(12),A.unit(5)],same:[D.A,D.A,D.A,D.A],real:[2,3,5,7].map(r=>A.unit(0).map(v=>v*r))};
function run(p){return $('rd').value==='element'?A.valueOf(p):A.applyPlan(p,D.X);}
function draw(){const g=cv.getContext('2d'),fg=css('--fg'),mut=css('--mut'),card=css('--card'),n=+$('n').value,vs=SETS[$('set').value].slice(0,n),ls=vs.map((v,i)=>A.leaf('ABCD'[i],v)),ps=A.plans(mode,ls),outs=ps.map(run),keys=outs.map(o=>o.join(','));
 const groups=new Map();keys.forEach(k=>groups.set(k,(groups.get(k)||0)+1));const gid=new Map();[...groups.keys()].forEach((k,i)=>gid.set(k,i));
 const cw=156,ch=100,cols=Math.floor(cv.width/cw),rows=Math.ceil(ps.length/cols);cv.height=rows*ch+8;g.clearRect(0,0,cv.width,cv.height);const sc=Math.max(1,...outs.map(o=>Math.max(...o.map(Math.abs))));cells=[];
 ps.forEach((p,i)=>{const x=4+(i%cols)*cw,y=4+Math.floor(i/cols)*ch,k=gid.get(keys[i]),big=groups.get(keys[i])>1,hue=(k*137.5)%360;
  g.fillStyle=card;g.fillRect(x,y,cw-6,ch-6);g.strokeStyle=big?'hsl('+hue+',70%,50%)':css('--line');g.lineWidth=big?3:1;g.strokeRect(x,y,cw-6,ch-6);
  g.fillStyle=fg;g.font='11px ui-monospace,monospace';g.fillText(A.notation(p).slice(0,24),x+4,y+13);A.bars(g,outs[i],x+4,y+20,cw-14,48,sc,big?'hsl('+hue+',65%,50%)':COL[0],null,fg,mut);cells.push({x,y,w:cw-6,h:ch-6,i});});
 const sizes=[...groups.values()],sets={A:1,B:1,C:1,D:1};
 $('stat').textContent='kind '+mode+': '+ps.length+' plans, '+groups.size+' distinct output vectors'+(groups.size<ps.length?'; the largest group has '+Math.max(...sizes)+' plans':'; every plan gives its own output')+'   ·   fire sequences reached: '+new Set(ps.map(p=>A.fireSeq(p).join(','))).size+' of '+(n===3?6:24)+' possible orders';
 cv._ps=ps;cv._outs=outs;}
cv.addEventListener('pointerdown',ev=>{const [x,y]=[ev.offsetX*cv.width/cv.clientWidth,ev.offsetY*cv.height/cv.clientHeight],c=cells.find(c=>x>=c.x&&x<=c.x+c.w&&y>=c.y&&y<=c.y+c.h);if(!c)return;const p=cv._ps[c.i],o=cv._outs[c.i];
 const same=cv._ps.filter((q,j)=>cv._outs[j].join(',')===o.join(',')).map(A.notation);$('info').textContent='plan '+A.notation(p)+'   fires '+A.fireSeq(p).join(' → ')+'\noutput e0…e15: '+o.map(A.fmt).join(', ')+'\n'+same.length+' plan(s) give this output: '+same.join('   ');});
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{mode=b.dataset.m;document.querySelectorAll('.tabs button').forEach(c=>c.classList.toggle('on',c===b));draw();});
['rd','n','set'].forEach(i=>$(i).onchange=draw);
const Q=new URLSearchParams(location.search);['n','rd','set'].forEach(k=>{if(Q.get(k))$(k).value=Q.get(k);});if(Q.get('m')){mode=Q.get('m');document.querySelectorAll('.tabs button').forEach(c=>c.classList.toggle('on',c.dataset.m===mode));}draw();
""")

# ------------------------------------------------------------------ 3 the tree
page("canvas2d_tree.html", "A plan as a tree",
     "Leaves, brackets and the firing order on every bracket; click a bracket to change its order.", "canvas2d_tree",
     """<div class="card"><div class="row"><label>items n <select id="n"><option>3</option><option>4</option></select></label><label>firing order of the leaves <select id="pm"></select></label>
<label>shape <select id="sh"></select></label><button id="rs">reset orders</button></div><canvas id="cv" width="760" height="330"></canvas>
<canvas id="ov" width="760" height="130" style="margin-top:8px"></canvas></div><div class="card info"><span id="info" class="mono pre"></span></div>""",
     r"""
const cv=$('cv'),ov=$('ov');let nodes=[],orders={},plan=null,perm=[],shapes=[];
const names='ABCD';
function leavesAll(n){return Array.from({length:n},(_,i)=>A.leaf(names[i],[D.A,D.B,D.C,D.D][i]));}
function setup(){const n=+$('n').value,P=A.perms(Array.from({length:n},(_,i)=>i));$('pm').innerHTML=P.map((p,i)=>'<option value="'+i+'">'+p.map(k=>names[k]).join(' ')+'</option>').join('');build();}
function build(){const n=+$('n').value,P=A.perms(Array.from({length:n},(_,i)=>i));perm=P[+$('pm').value||0];const ls=leavesAll(n),pl=perm.map(k=>ls[k]);
 shapes=[A.br(pl)].concat(A.plans('A',pl));$('sh').innerHTML=shapes.map((s,i)=>'<option value="'+i+'">'+(i===0?'flat: one bracket':A.notation(s))+'</option>').join('');orders={};apply();}
function clone(p,ctr){if(p.t==='L')return p;const id=ctr.n++,o=orders[id]||p.order;return {t:'B',kids:p.kids.map(k=>clone(k,ctr)),order:o,id};}
function apply(){plan=clone(shapes[+$('sh').value||0],{n:0});draw();}
function layout(p,depthMap){if(p.t==='L'){p.h=0;return 0;}p.h=1+Math.max(...p.kids.map(k=>layout(k)));return p.h;}
function draw(){const g=cv.getContext('2d'),W=cv.width,H=cv.height,fg=css('--fg'),mut=css('--mut'),card=css('--card'),line=css('--line'),acc=css('--acc');g.clearRect(0,0,W,H);layout(plan);
 const n=+$('n').value,dx=(W-120)/(n-1||1),top=40,bot=H-50,hh=plan.h?(bot-top)/plan.h:0;nodes=[];let li=0;
 function place(p){if(p.t==='L'){p.x=60+li*dx;li++;p.y=bot;return;}p.kids.forEach(place);p.x=p.kids.reduce((s,k)=>s+k.x,0)/p.kids.length;p.y=bot-p.h*hh;}place(plan);
 (function edges(p){if(p.t==='L')return;p.kids.forEach((k,i)=>{g.strokeStyle=mut;g.lineWidth=2;g.beginPath();g.moveTo(p.x,p.y);g.lineTo(k.x,k.y);g.stroke();const fo=p.order.indexOf(i+1)+1,bx=p.x+(k.x-p.x)*0.45,by=p.y+(k.y-p.y)*0.45;
   g.fillStyle=COL[3];g.beginPath();g.arc(bx,by,10,0,7);g.fill();g.fillStyle='#000';g.font='bold 12px system-ui';g.textAlign='center';g.fillText(fo,bx,by+4);g.textAlign='left';edges(k);});})(plan);
 (function nodesDraw(p){if(p.t==='L'){g.fillStyle=card;g.strokeStyle=COL[0];g.lineWidth=2;g.fillRect(p.x-22,p.y-16,44,32);g.strokeRect(p.x-22,p.y-16,44,32);g.fillStyle=fg;g.font='bold 15px system-ui';g.textAlign='center';g.fillText(p.name,p.x,p.y+5);g.textAlign='left';return;}
   p.kids.forEach(nodesDraw);g.fillStyle=card;g.strokeStyle=acc;g.lineWidth=3;g.beginPath();g.arc(p.x,p.y,15,0,7);g.fill();g.stroke();g.fillStyle=fg;g.font='11px system-ui';g.textAlign='center';g.fillText('( )',p.x,p.y+4);g.textAlign='left';nodes.push(p);})(plan);
 g.fillStyle=mut;g.font='12px system-ui';g.fillText('badge = when this child fires inside its bracket (1 first). Click a bracket to change its order.',8,16);
 const ls=leavesAll(n),x=D.X,op=A.applyPlan(plan,x),el=A.valueOf(plan),sc=Math.max(1,...op.map(Math.abs),...el.map(Math.abs)),o=ov.getContext('2d');o.clearRect(0,0,ov.width,ov.height);
 o.fillStyle=mut;o.font='12px system-ui';o.fillText('operator reading: output of the input e₁ + e₁₀',8,14);A.bars(o,op,8,22,350,70,sc,COL[0],x,fg,mut);o.fillText('element reading: the product of the items',390,14);A.bars(o,el,390,22,350,70,sc,COL[1],null,fg,mut);
 const orderCtr=(function c(p){return p.t==='L'?[]:[p.order].concat(...p.kids.map(c));})(plan);
 $('info').textContent='plan '+A.notation(plan)+'   fires '+A.fireSeq(plan).join(' → ')+'\nkind: '+kindOf(plan,perm)+'\nleaf order (a firing order of the leaves): '+perm.map(k=>names[k]).join(' ')+'\n|operator output| = '+A.fmt(norm(op))+'   |element value| = '+A.fmt(norm(el))+'   the two readings '+(JSON.stringify(op)===JSON.stringify(el)?'agree':'differ')+' for this plan';}
cv.addEventListener('pointerdown',ev=>{const x=ev.offsetX*cv.width/cv.clientWidth,y=ev.offsetY*cv.height/cv.clientHeight,hit=nodes.find(p=>Math.hypot(p.x-x,p.y-y)<18);if(!hit)return;
 const k=hit.kids.length;if(k===2)orders[hit.id]=hit.order[0]===1?[2,1]:[1,2];else{const P=A.perms(Array.from({length:k},(_,i)=>i+1)),cur=P.findIndex(q=>q.join()===hit.order.join());orders[hit.id]=P[(cur+1)%P.length];}apply();});
$('n').onchange=setup;$('pm').onchange=build;$('sh').onchange=()=>{orders={};apply();};$('rs').onclick=()=>{orders={};apply();};setup();const Q=new URLSearchParams(location.search);if(Q.get('n')){$('n').value=Q.get('n');setup();}if(Q.get('pm')){$('pm').value=Q.get('pm');build();}$('sh').value=Q.get('sh')||1;apply();
""")

# ------------------------------------------------------------------ 4 the counts
page("canvas2d_counts.html", "How many plans: the counts to sixteen items",
     "A, B, C and D against n on a log scale, with Bell(n) and 2ⁿ⁻¹ for comparison; exact values below.", "canvas2d_counts",
     """<div class="card"><canvas id="cv" width="900" height="420"></canvas><div style="overflow-x:auto"><table id="tb" class="mono"></table></div></div>""",
     r"""
const cv=$('cv');
const lg=v=>{const s=String(v);return s.length-1+Math.log10(parseFloat(s[0]+'.'+(s.slice(1,12)||'0')));};
const SER=[['A  bracketing (Catalan(n−1))',n=>A.modeCounts(n).A,COL[0]],['B  firing order (n!)',n=>A.modeCounts(n).B,COL[1]],['C  firing order of brackets',n=>A.modeCounts(n).C,COL[2]],['D  bracketing of firing orders',n=>A.modeCounts(n).D,COL[3]],['Bell(n), set partitions',n=>A.bell(n),'#8e5ea2'],['2^(n−1), contiguous blocks',n=>2n**BigInt(n-1),'#777']];
function draw(){const g=cv.getContext('2d'),W=cv.width,H=cv.height,fg=css('--fg'),mut=css('--mut'),line=css('--line'),L=54,R=20,T=24,Bm=40,ymax=22;g.clearRect(0,0,W,H);
 const X=n=>L+(n-1)/15*(W-L-R),Y=v=>H-Bm-v/ymax*(H-T-Bm);g.font='12px system-ui';g.fillStyle=mut;g.strokeStyle=line;
 for(let e=0;e<=ymax;e+=2){g.beginPath();g.moveTo(L,Y(e));g.lineTo(W-R,Y(e));g.stroke();g.textAlign='right';g.fillText('10^'+e,L-6,Y(e)+4);}for(let n=1;n<=16;n++){g.textAlign='center';g.fillText(n,X(n),H-Bm+16);}g.textAlign='left';g.fillText('number of items n',W/2-40,H-8);g.fillText('plans (log scale)',6,14);
 SER.forEach(([nm,f,c],k)=>{g.strokeStyle=c;g.lineWidth=k===3?3.5:2.2;g.setLineDash(k>3?[6,4]:[]);g.beginPath();for(let n=1;n<=16;n++){const y=Y(Math.max(0,lg(f(n))));n===1?g.moveTo(X(n),y):g.lineTo(X(n),y);}g.stroke();g.setLineDash([]);
   g.fillStyle=c;g.fillRect(L+10+(k%3)*280,T+4+Math.floor(k/3)*16-8,14,3);g.fillStyle=fg;g.fillText(nm,L+30+(k%3)*280,T+4+Math.floor(k/3)*16);});
 let h='<tr><th>n</th>'+SER.map(s=>'<th>'+s[0].split('(')[0].trim()+'</th>').join('')+'</tr>';for(let n=1;n<=16;n++)h+='<tr'+(n===16?' style="font-weight:600"':'')+'><td>'+n+'</td>'+SER.map(s=>'<td>'+A.comma(s[1](n))+'</td>').join('')+'</tr>';$('tb').innerHTML=h;}
draw();addEventListener('resize',draw);
""")

# ------------------------------------------------------------------ 5 set membership
page("canvas2d_membership.html", "Set membership: has it been here before?",
     "The third tool: a memory of the positions visited, the flip test, and the jurisdiction check, for any sequence of functions.", "canvas2d_membership",
     """<div class="card"><div class="row"><label>sequence <select id="sq"></select></label><label>start x₀ <input type="number" id="x0" value="1" step="0.5" style="width:5em"></label><label id="nl">terms <input type="range" id="nt" min="5" max="80" value="40"><b id="ntv"></b></label></div>
<div class="row" id="bl"><button data-w="add,1">+1</button><button data-w="add,2">+2</button><button data-w="add,-1">−1</button><button data-w="add,-2">−2</button><button data-w="mul,2">×2</button><button data-w="mul,0.5">×½</button><button data-w="mul,-1">−x</button><button id="undo">undo</button><button id="clr">clear</button></div>
<canvas id="cv" width="900" height="300"></canvas></div><div class="card info"><span id="info" class="mono pre"></span></div>
<div class="card"><b>Jurisdiction: is the operation in the object's own set?</b><div class="row"><label>map (one line per object, <code>object: op, op</code>)<br><textarea id="jm" rows="4" cols="46" style="font:13px monospace;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px"></textarea></label>
<label>object <input id="jo" value="lineage" size="10"></label><label>operation <input id="jp" value="build_up" size="10"></label></div><div id="jv" class="mono pre"></div></div>""",
     r"""
const cv=$('cv');let custom=[['add',1],['add',-1]];const names=Object.keys(D.words);
$('sq').innerHTML='<option value="rec">Recamán (flip = membership in the visited set)</option>'+names.map(n=>'<option value="'+n+'">'+n+'</option>').join('')+'<option value="cus">your own word</option>';
const nm=w=>w[0]==='add'?(w[1]>=0?'+':'−')+Math.abs(w[1]):w[1]===-1?'−x':w[1]===0.5?'×½':'×'+w[1];
function draw(){const g=cv.getContext('2d'),W=cv.width,H=cv.height,fg=css('--fg'),mut=css('--mut'),card=css('--card'),line=css('--line'),k=$('sq').value,rec=k==='rec';$('nl').style.display=rec?'':'none';$('bl').style.display=k==='cus'?'':'none';$('ntv').textContent=$('nt').value;
 let t,steps=[],lab=[];if(rec){t=A.recaman(+$('nt').value);}else{const ws=k==='cus'?custom:D.words[k].steps;steps=ws.map(A.callable);lab=ws.map(nm);t=A.trajectory(steps,+$('x0').value);}
 const col=A.collisions(t,rec?0.5:1e-9),lo=Math.min(...t,0),hi=Math.max(...t,1),L=48,R=14,T=14,Bm=26,X=i=>L+i/Math.max(1,t.length-1)*(W-L-R),Y=v=>H-Bm-(v-lo)/(hi-lo||1)*(H-T-Bm);g.clearRect(0,0,W,H);g.strokeStyle=line;g.lineWidth=1;g.fillStyle=mut;g.font='11px system-ui';
 for(let i=0;i<=4;i++){const v=lo+(hi-lo)*i/4;g.beginPath();g.moveTo(L,Y(v));g.lineTo(W-R,Y(v));g.stroke();g.textAlign='right';g.fillText(A.fmt(v),L-4,Y(v)+4);}g.textAlign='left';
 g.strokeStyle=COL[0];g.lineWidth=2;g.beginPath();t.forEach((v,i)=>i?g.lineTo(X(i),Y(v)):g.moveTo(X(i),Y(v)));g.stroke();
 t.forEach((v,i)=>{let up=i>0&&v>t[i-1];g.fillStyle=i===0?fg:up?COL[1]:COL[2];g.beginPath();g.arc(X(i),Y(v),t.length>45?2.5:4,0,7);g.fill();});
 col.forEach(c=>{g.strokeStyle=COL[3];g.lineWidth=3;g.beginPath();g.arc(X(c[1]),Y(c[2]),9,0,7);g.stroke();});
 g.fillStyle=mut;g.fillText('position against step; green = a step down, red = a step up; ringed = a return to a visited position',L,H-6);
 let txt='';if(rec){const flips=[];for(let n=1;n<t.length;n++)if(t[n]>t[n-1])flips.push(n);txt='Recamán: a(n) = a(n−1) − n if that is positive and not already visited, else a(n−1) + n.\nterms: '+t.slice(0,24).join(', ')+(t.length>24?', …':'')+'\nsteps that went UP because the down-step was refused: '+flips.length+' of '+(t.length-1)+'\nterms that appear more than once among these (ringed): '+col.length+'. The rule tests only the DOWN-step against the visited set; an up-step may land on a visited number, so repeats do occur.';}
 else{const trial=[-3,-1,0,1,2,3].map(c=>'+'+c+': '+(A.wouldCollide(t,x=>x+c)?'YES, refused':'free')).join('   ');txt='word: '+(lab.join('  ,  ')||'(empty)')+'\npositions: '+t.map(A.fmt).join(' → ')+'\ncollisions (earlier, later, position): '+(col.length?col.map(c=>'('+c[0]+', '+c[1]+', '+A.fmt(c[2])+')').join('  '):'none — self-avoiding')+'\nthe next step "+c" would land on a visited position?  '+trial;}
 $('info').textContent=txt;}
function jur(){const map={};$('jm').value.split('\n').forEach(l=>{const m=l.split(':');if(m.length===2)map[m[0].trim()]=m[1].split(',').map(s=>s.trim()).filter(Boolean);});const v=A.jurisdiction(map,$('jo').value.trim(),$('jp').value.trim());
 $('jv').textContent=v===null?'the object is not in the map':v?'VIOLATION: "'+$('jp').value+'" is not in the set of operations legal for "'+$('jo').value+'" ('+map[$('jo').value.trim()].join(', ')+')':'legal: "'+$('jp').value+'" is in the set for "'+$('jo').value+'"';}
document.querySelectorAll('#bl button[data-w]').forEach(b=>b.onclick=()=>{const p=b.dataset.w.split(',');custom.push([p[0],+p[1]]);$('sq').value='cus';draw();});$('undo').onclick=()=>{custom.pop();draw();};$('clr').onclick=()=>{custom=[];draw();};
const Q=new URLSearchParams(location.search);if(Q.get('sq'))$('sq').value=Q.get('sq');['sq','x0','nt'].forEach(i=>$(i).oninput=draw);$('sq').onchange=draw;$('jm').value=Object.keys(D.juris_map).map(k=>k+': '+D.juris_map[k].join(', ')).join('\n');['jm','jo','jp'].forEach(i=>$(i).oninput=jur);draw();jur();
""")

# ------------------------------------------------------------------ index
cards = [
    ("canvas2d_evolve.html", "The evolving sedenion: input to output", "A 16-component input on e₀…e₁₅ and the vector after every step of a plan, under A, B, C and D, in the operator and the element reading; Ĥ_RB's coupling is one of the items."),
    ("canvas2d_allplans.html", "Every plan of one kind, and which agree", "All plans of A, B, C or D over 3 or 4 items with their outputs; frames mark plans that give the same vector; item sets where plans collapse."),
    ("canvas2d_tree.html", "A plan as a tree", "Leaves, brackets and numbered firing order; click a bracket to change its order; the page names the kind (A, B, C or D)."),
    ("canvas2d_counts.html", "How many plans: the counts to sixteen items", "A, B, C, D, Bell(n) and 2ⁿ⁻¹ on a log scale with exact values (BigInt); D contains A, B and C."),
    ("canvas2d_membership.html", "Set membership: has it been here before?", "Recamán's flip as a membership test, words of callables with their collisions and the flip test, and the jurisdiction check."),
]
cards_html = "".join(f'<div class="card"><h2 style="font-size:17px;margin:0"><a href="{u}">{html.escape(t)}</a></h2><span class="tag">canvas2d_</span><p>{html.escape(d)}</p></div>' for u, t, d in cards)
cards_html += '<div class="card"><h2 style="font-size:17px;margin:0">Code flow chart</h2><span class="tag">svg</span><p>The call graph of the engine in ISO 5807 symbols, derived from the source by <code>tools/flowchart.py</code>: <a href="../../docs/flowcharts/bracketing_firing_order_flow.svg">bracketing_firing_order_flow.svg</a>.</p></div>'
src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>: {html.escape(d)}</li>' for u, t, d in SOURCES)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bracketing and Firing Order Gallery</title>
<link rel="icon" type="image/png" href="favicon.png"><link rel="stylesheet" href="bf.css"><!-- SPDX-License-Identifier: GPL-3.0-only. Generated by build_pages.py. --></head><body>{CT}
<header><h1>Bracketing, firing order and set membership: interactive visualizations</h1><div class="sub">ValaQuenta engine 7, <code>modules/bracketing_firing_order</code> (0.2). Five pages, each recomputing its numbers in the browser and comparing them with the Python engine. A picture shows a structure; it is not evidence that the structure means anything beyond its definition.</div></header>
<main>{cards_html}</main>
<footer><p><b>Sources.</b></p><ul>{src}</ul><p>Launch: <code>gallery/bracketing_firing_order/serve_gallery.sh</code> (loopback only, port 8795).</p></footer></body></html>""")
print("pages written")
