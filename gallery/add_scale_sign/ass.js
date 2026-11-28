/* SPDX-License-Identifier: GPL-3.0-only. add_scale_sign gallery: the shared library. Raw JavaScript, no libraries, no network.
   Elements of Aff(1,R) are {add, scale, sign}: x -> sign*scale*x + add. Everything here is recomputed in the browser and compared with
   window.ASSDATA, which build_data.py bakes from the Python engine (ValaQuenta/modules/add_scale_sign, version 0.2). */
(function () {
  'use strict';
  const D = window.ASSDATA || null, B = {data: D};
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };
  // exact rationals (small integers): the JavaScript twin of Python's fractions.Fraction
  class Q {
    constructor(n, d = 1) { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d) || 1; this.n = n / g; this.d = d / g; }
    add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); }
    mul(o) { return new Q(this.n * o.n, this.d * o.d); }
    neg() { return new Q(-this.n, this.d); }
    inv() { return new Q(this.d, this.n); }
    eq(o) { return this.n === o.n && this.d === o.d; }
    str() { return this.d === 1 ? String(this.n) : this.n + '/' + this.d; }
    val() { return this.n / this.d; }
    static parse(s) { const p = String(s).split('/'); return new Q(+p[0], p.length > 1 ? +p[1] : 1); }
  }
  B.Q = Q;
  // ---- float elements
  B.el = (add, scale, sign) => ({add, scale, sign});
  B.apply = (x, v) => x.sign * x.scale * v + x.add;
  B.comp = (x, y) => ({add: x.add + x.sign * x.scale * y.add, scale: x.scale * y.scale, sign: x.sign * y.sign});   // x@y : y fires first
  B.inv = x => ({add: -x.sign * x.add / x.scale + 0, scale: 1 / x.scale, sign: x.sign});
  B.comm = (x, y) => B.comp(B.comp(B.comp(B.inv(x), B.inv(y)), x), y);                                            // x^-1 y^-1 x y
  B.u = x => x.sign * Math.log(x.scale) + x.add;
  B.gamma = x => Math.tanh(0.5 * B.u(x));
  B.defect = x => (x.sign - 1) * Math.log(x.scale);
  B.same = (x, y, t = 1e-9) => Math.abs(x.add - y.add) < t && Math.abs(x.scale - y.scale) < t && x.sign === y.sign;
  B.fromArr = a => ({add: a[0], scale: a[1], sign: a[2]});
  B.compose = steps => steps.map(B.fromArr).reduce((out, e) => B.comp(e, out), B.el(0, 1, 1));              // first listed fires first
  B.smith = x => ({g_scale: Math.tanh(0.5 * Math.log(x.scale)), g_add: Math.tanh(0.5 * x.add)});
  B.quadrant = x => { const s = B.smith(x); return ((s.g_add >= 0) ? 'N' : 'S') + ((s.g_scale >= 0) ? 'E' : 'W') + (x.sign < 0 ? '′' : ''); };
  // ---- the Long Path
  B.trajectory = (steps, x0 = 1) => { let x = x0; const t = [x]; steps.forEach(s => { x = B.apply(B.fromArr(s), x); t.push(x); }); return t; };
  B.collisions = (t, tol = 1e-9) => { const m = new Map(), out = []; t.forEach((x, i) => { const k = Math.round(x / tol); if (m.has(k)) { out.push([m.get(k), i, x]); } m.set(k, i); }); return out.sort((a, b) => a[0] - b[0] || a[1] - b[1]); };
  B.wouldCollide = (t, step, tol = 1e-9) => { const c = B.apply(B.fromArr(step), t[t.length - 1]), k = Math.round(c / tol); return t.some(x => Math.round(x / tol) === k); };
  B.zeta = steps => steps.map((s, i) => [s, i]).sort((a, b) => Math.abs(B.u(B.fromArr(b[0]))) - Math.abs(B.u(B.fromArr(a[0]))) || a[1] - b[1]).map(p => p[0]);
  B.wordInfo = (steps, order) => { const st = order === 'zeta' ? B.zeta(steps) : steps, T = B.compose(steps);
    return {steps: st, element: T, traj: B.trajectory(st), u_total: B.u(T), u_sum: st.reduce((s, e) => s + B.u(B.fromArr(e)), 0), defect: B.defect(T)}; };
  // ---- the exact grid
  B.grid = () => { const E = D.grid.elements.map(e => ({add: Q.parse(e[0]), scale: Q.parse(e[1]), sign: e[2]}));
    const cmp = (x, y) => ({add: x.add.add(new Q(x.sign).mul(x.scale).mul(y.add)), scale: x.scale.mul(y.scale), sign: x.sign * y.sign});
    const eq = (x, y) => x.add.eq(y.add) && x.scale.eq(y.scale) && x.sign === y.sign;
    return {E, cmp, eq, name: e => 'x ↦ ' + (e.sign < 0 ? '−' : '+') + e.scale.str() + '·x ' + (e.add.n < 0 ? '− ' + e.add.neg().str() : '+ ' + e.add.str())}; };
  B.pos = (ev, cv) => { const r = cv.getBoundingClientRect(); return [(ev.clientX - r.left) * cv.width / r.width, (ev.clientY - r.top) * cv.height / r.height]; };
  B.css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  B.fmt = (x, n = 4) => (Math.abs(x) < 5e-13 ? 0 : +x.toFixed(n)).toString();
  // ---- self-check: every JS number against the engine's
  B.selfCheck = function () {
    const out = [], ok = (n, c) => out.push((c ? '✓ ' : '✗ ') + n), tol = 1e-12;
    let m = 0; D.samples.forEach(s => { const e = B.el(s.a, s.s, s.g), sm = B.smith(e);
      m = Math.max(m, Math.abs(B.u(e) - s.u), Math.abs(B.gamma(e) - s.gamma), Math.abs(sm.g_scale - s.g_scale), Math.abs(sm.g_add - s.g_add), Math.abs(B.defect(e) - s.defect)); if (B.quadrant(e).replace('′', '') !== s.quadrant.replace('′', '') && (s.a !== 0 && s.s !== 1)) m = 1; });
    ok('word u, fold Γ, both Smith coordinates and the firing defect at ' + D.samples.length + ' points, max difference ' + m.toExponential(1), m < tol);
    let bm = 0; D.brackets.forEach(b => { const A = B.el(b.a, 1, 1), S = B.el(0, b.s, 1), G = B.el(0, 1, -1);
      [[B.comm(A, S), b.AS], [B.comm(A, G), b.AG], [B.comm(S, G), b.SG]].forEach(([c, r]) => { bm = Math.max(bm, Math.abs(c.add - r[0]), Math.abs(c.scale - r[1]), c.sign - r[2] ? 9 : 0); }); });
    ok('group commutators of ADD, SCALE, SIGN at ' + D.brackets.length + ' parameter pairs, max difference ' + bm.toExponential(1), bm < tol);
    let wok = true; Object.keys(D.words).forEach(k => { const w = D.words[k]; ['chrono', 'zeta'].forEach(o => { const i = B.wordInfo(w.steps, o), r = w[o];
      const tm = Math.max(...i.traj.map((x, j) => Math.abs(x - r.trajectory[j])));
      const col = JSON.stringify(B.collisions(i.traj).map(c => [c[0], c[1]])) === JSON.stringify(r.collisions.map(c => [c[0], c[1]]));
      const wc = Object.keys(r.would_collide).every(c => B.wouldCollide(i.traj, [+c, 1, 1]) === r.would_collide[c]);
      if (tm > tol || !col || !wc || Math.abs(i.u_total - r.u_total) > tol || Math.abs(i.u_sum - r.u_sum) > tol || Math.abs(i.defect - r.firing_defect) > tol || !B.same(i.element, B.fromArr(w.element))) wok = false; }); });
    ok('the Long Path of ' + Object.keys(D.words).length + ' words, chrono and zeta: trajectory, collisions, flip test, u_total, Σ u of steps, defect', wok);
    const G = B.grid(), n = G.E.length; let com = 0, clo = 0, cm = true, clm = true, as = 0;
    const idx = e => G.E.findIndex(f => G.eq(e, f));
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { const p = G.cmp(G.E[i], G.E[j]), q = G.cmp(G.E[j], G.E[i]), c = G.eq(p, q) ? 1 : 0, l = idx(p) >= 0 ? 1 : 0;
      com += c; clo += l; if (c !== D.grid.commute[i][j]) cm = false; if (l !== D.grid.closure[i][j]) clm = false; if (G.cmp(G.E[i], G.E[j]).add.str() !== D.grid.prod_add[i][j]) cm = false; }
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) for (let k = 0; k < n; k++) if (!G.eq(G.cmp(G.cmp(G.E[i], G.E[j]), G.E[k]), G.cmp(G.E[i], G.cmp(G.E[j], G.E[k])))) as++;
    ok('exact grid (rationals): 18 elements, ' + n * n * n + ' triples, associativity failures ' + as + ' (engine: associative = ' + D.laws.associative + ')', as === 0 && D.laws.associative && n * n * n === D.laws.triples);
    ok('exact grid: ' + com + ' commuting ordered pairs of 324 and ' + clo + ' products inside the grid, every cell and every product\'s add equal to the engine\'s', cm && clm && com === D.grid.commuting_pairs && clo === D.grid.closed_pairs);
    const el = document.getElementById('selfcheck');
    if (el) { const bad = out.filter(s => s[0] === '✗').length; el.innerHTML = '<b class="' + (bad ? 'bad' : 'ok') + '">Self-check: ' + (bad ? bad + ' mismatch' : 'all ' + out.length + ' agree with the Python engine') + '</b><br>' + out.join('<br>'); }
    return out;
  };
  window.ASSB = B;
})();
