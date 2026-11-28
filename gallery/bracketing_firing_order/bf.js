/* SPDX-License-Identifier: GPL-3.0-only. bracketing_firing_order gallery: the shared library. Raw JavaScript, no libraries, no network.
   Plans (brackets that carry firing orders) over 16-component vectors, the four orderings A-D, both readings, the evolving vector,
   exact counts (BigInt), set membership. Everything is recomputed here and compared with window.BFDATA, which build_data.py bakes
   from the Python engine (ValaQuenta/modules/bracketing_firing_order, version 0.2). */
(function () {
  'use strict';
  const D = window.BFDATA || null, B = {data: D};
  // ---- the Cayley-Dickson product (a1,a2)(b1,b2) = (a1 b1 - conj(b2) a2, b2 a1 + a2 conj(b1)), any power-of-two length
  const conj = v => v.map((x, i) => i ? -x : x);
  const mul = (a, b) => { const n = a.length; if (n === 1) return [a[0] * b[0]]; const h = n / 2, a1 = a.slice(0, h), a2 = a.slice(h), b1 = b.slice(0, h), b2 = b.slice(h);
    const l1 = mul(a1, b1), l2 = mul(conj(b2), a2), r1 = mul(b2, a1), r2 = mul(a2, conj(b1)); return l1.map((x, i) => x - l2[i]).concat(r1.map((x, i) => x + r2[i])); };
  B.mul = mul;
  B.unit = k => Array.from({length: 16}, (_, i) => +(i === k));
  B.lmat = a => { const cols = Array.from({length: a.length}, (_, k) => mul(a, B.unit(k))); return a.map((_, r) => cols.map(c => c[r])); };   // column k is a*e_k
  B.matvec = (M, x) => M.map(row => row.reduce((s, m, i) => s + m * x[i], 0));
  // ---- plans
  B.leaf = (name, vec) => ({t: 'L', name, vec, mat: null});
  B.br = (kids, order) => ({t: 'B', kids, order: order || kids.map((_, i) => i + 1)});
  B.fired = p => p.order.map(i => p.kids[i - 1]);
  B.notation = p => { if (p.t === 'L') return p.name; let s = p.kids.map(B.notation).join(' '); if (p.order.some((o, i) => o !== i + 1)) s += ' | ' + p.order.join(' '); return '(' + s + ')'; };
  B.fireSeq = p => p.t === 'L' ? [p.name] : [].concat(...B.fired(p).map(B.fireSeq));
  B.leavesFired = p => p.t === 'L' ? [p] : [].concat(...B.fired(p).map(B.leavesFired));
  B.evolveOperator = (p, x) => { let v = x.slice(); const out = [['input', v]]; B.leavesFired(p).forEach(l => { l.mat = l.mat || B.lmat(l.vec); v = B.matvec(l.mat, v); out.push([l.name, v]); }); return out; };
  B.applyPlan = (p, x) => { const s = B.evolveOperator(p, x); return s[s.length - 1][1]; };
  B.evolveValue = p => { const out = []; const go = q => { if (q.t === 'L') { out.push([q.name, q.vec]); return [q.vec, q.name]; }
      const vs = B.fired(q).map(go); let [acc, lab] = vs[0]; for (let i = 1; i < vs.length; i++) { acc = mul(acc, vs[i][0]); lab = '(' + lab + ' ' + vs[i][1] + ')'; out.push([lab, acc]); } return [acc, lab]; }; go(p); return out; };
  B.valueOf = p => { const s = B.evolveValue(p); return s[s.length - 1][1]; };
  // ---- the four orderings (same enumeration order as the Python engine)
  function* binary(ls, both) { if (ls.length === 1) { yield ls[0]; return; } for (let c = 1; c < ls.length; c++) for (const L of binary(ls.slice(0, c), both)) for (const R of binary(ls.slice(c), both)) for (const o of both ? [[1, 2], [2, 1]] : [[1, 2]]) yield B.br([L, R], o); }
  function perms(a) { if (a.length <= 1) return [a.slice()]; const out = []; a.forEach((x, i) => perms(a.slice(0, i).concat(a.slice(i + 1))).forEach(p => out.push([x].concat(p)))); return out; }
  B.perms = perms;
  B.plans = (mode, ls) => { if (mode === 'A') return [...binary(ls, false)]; if (mode === 'B') return perms(ls.map((_, i) => i + 1)).map(o => B.br(ls, o));
    if (mode === 'C') return [...binary(ls, true)]; const out = []; perms(ls).forEach(p => out.push(...binary(p, false))); return out; };
  B.reach = (mode, n) => new Set(B.plans(mode, Array.from({length: n}, (_, i) => B.leaf(String(i), B.unit(0)))).map(p => B.fireSeq(p).join(','))).size;
  // ---- exact counts (BigInt)
  const fact = n => { let r = 1n; for (let i = 2n; i <= BigInt(n); i++) r *= i; return r; };
  B.catalan = n => fact(2 * n) / (fact(n) * fact(n + 1));
  B.modeCounts = n => { const cat = B.catalan(n - 1), f = fact(n); return {A: cat, B: f, C: cat * 2n ** BigInt(n - 1), D: f * cat}; };
  B.bell = n => { let row = [1n]; for (let i = 1; i < n; i++) { const nx = [row[row.length - 1]]; row.forEach((x, j) => nx.push(nx[j] + x)); row = nx; } return row[row.length - 1]; };
  B.comma = s => String(s).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  // ---- set membership: any sequence of callables
  B.callable = w => w[0] === 'add' ? (x => x + w[1]) : (x => x * w[1]);
  B.trajectory = (steps, x0) => { let x = x0; const t = [x]; steps.forEach(s => { x = s(x); t.push(x); }); return t; };
  B.collisions = (t, tol = 1e-9) => { const m = new Map(), out = []; t.forEach((x, i) => { const k = Math.round(x / tol); if (m.has(k)) out.push([m.get(k), i, x]); m.set(k, i); }); return out.sort((a, b) => a[0] - b[0] || a[1] - b[1]); };
  B.wouldCollide = (t, f, tol = 1e-9) => { const c = f(t[t.length - 1]), k = Math.round(c / tol); return t.some(x => Math.round(x / tol) === k); };
  B.recaman = count => { const steps = []; let t = [0]; for (let n = 1; n < count; n++) { const cur = t[t.length - 1], f = x => x - n; if (cur - n > 0 && !B.wouldCollide(t, f, 0.5)) steps.push(f); else steps.push(x => x + n); t = B.trajectory(steps, 0); } return t; };
  B.jurisdiction = (map, obj, op) => map[obj] === undefined ? null : !map[obj].includes(op);
  // ---- drawing helper: 16 bars on the axes e0..e15
  B.bars = (g, vec, x, y, w, h, scale, col, ghost, fg, mut) => { const bw = w / 16, mid = y + h / 2; g.strokeStyle = mut; g.lineWidth = 1; g.beginPath(); g.moveTo(x, mid); g.lineTo(x + w, mid); g.stroke();
    if (ghost) { g.strokeStyle = mut; g.setLineDash([2, 2]); vec.forEach((_, i) => { const gv = ghost[i] / scale * (h / 2); g.strokeRect(x + i * bw + 1, gv >= 0 ? mid - gv : mid, bw - 2, Math.abs(gv)); }); g.setLineDash([]); }
    vec.forEach((v, i) => { const hh = v / scale * (h / 2); g.fillStyle = col; g.globalAlpha = 0.9; g.fillRect(x + i * bw + 1, hh >= 0 ? mid - hh : mid, bw - 2, Math.abs(hh)); g.globalAlpha = 1; });
    g.fillStyle = fg; g.font = '9px system-ui'; g.textAlign = 'center'; vec.forEach((_, i) => g.fillText(i, x + i * bw + bw / 2, y + h + 10)); g.textAlign = 'left'; };
  B.css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  B.fmt = x => Math.abs(x) < 5e-13 ? '0' : String(+x.toFixed(6));
  // ---- self-check: every JS number against the engine's
  B.selfCheck = function () {
    const out = [], ok = (n, c) => out.push((c ? '✓ ' : '✗ ') + n), eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
    ok('Cayley–Dickson product of 6 random sedenion pairs equals the engine\'s', D.mul_tests.every(t => eq(mul(t[0], t[1]), t[2])));
    let planOK = true, nplans = 0;
    [['3', [D.A, D.B, D.C]], ['4', [D.A, D.B, D.C, D.D]]].forEach(([n, vs]) => { const ls = vs.map((v, i) => B.leaf(String.fromCharCode(65 + i), v));
      'ABCD'.split('').forEach(m => { const ps = B.plans(m, ls), e = D.plans[n][m]; nplans += ps.length;
        if (!eq(ps.map(B.notation), e.notation) || !eq(ps.map(B.fireSeq), e.fire) || !eq(ps.map(p => B.applyPlan(p, D.X)), e.op) || !eq(ps.map(B.valueOf), e.val)) planOK = false; }); });
    ok('all four orderings for 3 and 4 items: ' + nplans + ' plans, notation, firing sequence, operator output and element output equal the engine\'s', planOK);
    let cOK = true; for (let n = 1; n <= 16; n++) { const c = B.modeCounts(n), e = D.counts[n]; if (['A', 'B', 'C', 'D'].some(k => String(c[k]) !== e[k]) || String(B.bell(n)) !== D.bell[n]) cOK = false; }
    ok('counts A, B, C, D and Bell for n = 1…16 (BigInt) equal the engine\'s; Bell(16) = ' + B.comma(B.bell(16)), cOK);
    ok('firing orders reached by each kind (n = 3, 4, 5): ' + ['3', '4', '5'].map(n => 'ABCD'.split('').map(m => B.reach(m, +n)).join('/')).join('  '), ['3', '4', '5'].every(n => 'ABCD'.split('').every(m => B.reach(m, +n) === D.reach[n][m])));
    const L3 = {A: B.leaf('A', D.A), B: B.leaf('B', D.B), C: B.leaf('C', D.C)}, pl = B.br([B.br([L3.A, L3.B], [2, 1]), L3.C], [2, 1]);
    ok('the evolving vector of ' + B.notation(pl) + ': the input, then the vector after each leaf, and every product of the element reading', B.notation(pl) === D.evolve.plan && eq(B.evolveOperator(pl, D.X).map(s => [s[0], s[1]]), D.evolve.op) && eq(B.evolveValue(pl), D.evolve.val));
    const H = D.hrb, Lc = B.lmat(H.C), o = B.matvec(Lc, H.sigma); ok('Ĥ_RB (lift B) as a one-leaf plan: L_C σ_RB equals the engine\'s output, max difference ' + Math.max(...o.map((v, i) => Math.abs(v - H.out[i]))).toExponential(1), o.every((v, i) => Math.abs(v - H.out[i]) < 1e-9));
    ok('Recamán by the flip test equals the engine\'s first 40 terms (OEIS A005132: 0, 1, 3, 6, 2, 7, 13, 20, 12, 21, 11, 22, …)', eq(B.recaman(40), D.recaman));
    let wOK = true; Object.keys(D.words).forEach(k => { const w = D.words[k], st = w.steps.map(B.callable), t = B.trajectory(st, 1); if (!eq(t, w.trajectory) || !eq(B.collisions(t).map(c => [c[0], c[1]]), w.collisions.map(c => [c[0], c[1]])) || !Object.keys(w.would).every(c => B.wouldCollide(t, x => x + (+c)) === w.would[c])) wOK = false; });
    ok('set membership on ' + Object.keys(D.words).length + ' words of callables: trajectory, collisions, flip test equal the engine\'s; jurisdiction verdicts ' + D.juris.length + ' of ' + D.juris.length, wOK && D.juris.every(j => B.jurisdiction(D.juris_map, j[0], j[1]) === j[2]));
    const el = document.getElementById('selfcheck'); if (el) { const bad = out.filter(s => s[0] === '✗').length; el.innerHTML = '<b class="' + (bad ? 'bad' : 'ok') + '">Self-check: ' + (bad ? bad + ' mismatch' : 'all ' + out.length + ' agree with the Python engine') + '</b><br>' + out.join('<br>'); }
    return out;
  };
  window.BFB = B;
})();
