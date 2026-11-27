// SPDX-License-Identifier: GPL-3.0-only
// bk.js -- JavaScript ports used by the box_kite gallery: the Cayley-Dickson table by doubling (box_kite.cd_multiplication_table), the associator, the
// zero-divisor search (zero_divisor_pairs), the octahedral Laplacian spectrum (chart_spectrum), the labelled octonion group (labelled_automorphisms,
// labelled_group_is_split's quotient), and a small orthographic orbit camera (z is up; yaw about z, then pitch about the screen x axis).
// Each page checks these against numbers baked from the Python engine (bk_data.js) and prints the result in #selfcheck.
(function () {
  const D = window.BKDATA, B = { data: D };

  // ---- Cayley-Dickson doubling:  (a,b)(c,d) = (ac - conj(d) b, d a + b conj(c)); entries are [sign, index]
  B.table = (function () {
    let tab = [[[1, 0]]], N = 1;
    const conj = i => (i === 0 ? [1, 0] : [-1, i]);
    for (let lev = 0; lev < 4; lev++) {
      const M = 2 * N, nt = Array.from({ length: M }, () => Array(M));
      for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
        nt[i][j] = tab[i][j];
        let [s, k] = tab[j][i]; nt[i][j + N] = [s, k + N];
        let [cs, ci] = conj(j); [s, k] = tab[i][ci]; nt[i + N][j] = [cs * s, k + N];
        [s, k] = tab[ci][i]; nt[i + N][j + N] = [-cs * s, k];
      }
      tab = nt; N = M;
    }
    return tab;
  })();
  B.mul = (i, j) => B.table[i][j];

  // ---- associator [e_i,e_j,e_k] = (e_i e_j) e_k - e_i (e_j e_k), as a 16-vector, and its norm
  B.assoc = function (i, j, k) {
    const v = Array(16).fill(0);
    let [s1, m] = B.mul(i, j), [s2, n] = B.mul(m, k), [s3, q] = B.mul(j, k), [s4, r] = B.mul(i, q);
    v[n] += s1 * s2; v[r] -= s3 * s4; return v;
  };
  B.defect = (i, j, k) => Math.hypot(...B.assoc(i, j, k));
  B.defectAll = function () { const a = new Float64Array(4096); for (let i = 0; i < 16; i++) for (let j = 0; j < 16; j++) for (let k = 0; k < 16; k++) a[i * 256 + j * 16 + k] = B.defect(i, j, k); return a; };

  // ---- sedenion product of two sparse vectors given as {index: coefficient}
  B.vmul = function (x, y) {
    const o = {};
    for (const i in x) for (const j in y) { const [s, k] = B.mul(+i, +j); o[k] = (o[k] || 0) + s * x[i] * y[j]; }
    return o;
  };
  B.isZero = o => Object.values(o).every(c => Math.abs(c) < 1e-12);
  B.diag = (a, b, s) => ({ [a]: 1, [b + 8]: s });                       // e_a + s e_{b+8}
  B.diagName = (a, b, s) => 'e' + a + (s > 0 ? ' + ' : ' − ') + 'e' + (b + 8);
  // every ordered pair of diagonals whose product vanishes: [a,b,s, c,d,t]
  B.zdPairs = function () {
    if (B._zd) return B._zd;
    const ds = []; for (let a = 1; a < 8; a++) for (let b = 1; b < 8; b++) for (const s of [1, -1]) ds.push([a, b, s]);
    const out = []; for (const p of ds) for (const q of ds) if (B.isZero(B.vmul(B.diag(...p), B.diag(...q)))) out.push([...p, ...q]);
    return (B._zd = out);
  };
  B.assessorPlanes = () => { const o = []; for (let a = 1; a < 8; a++) for (let b = 1; b < 8; b++) if (a !== b) o.push([a, b]); return o; };
  B.strut = (a, b) => a ^ b;
  // strut-s box-kite: the six assessors with a^b = s, ordered as in the engine (reversal pairs adjacent), edges from the zero-divisor products
  B.kite = function (s) {
    const V = D.struts[s].vertices, key = v => v[0] + ',' + v[1], pos = {}; V.forEach((v, i) => (pos[key(v)] = i));
    const E = new Set();
    for (const [a, b, sa, c, d, sb] of B.zdPairs()) {
      if (B.strut(a, b) !== +s || B.strut(c, d) !== +s || (a === c && b === d)) continue;
      const i = pos[a + ',' + b], j = pos[c + ',' + d]; if (i !== undefined && j !== undefined) E.add(Math.min(i, j) + ',' + Math.max(i, j));
    }
    return { vertices: V, edges: [...E].map(e => e.split(',').map(Number)).sort((x, y) => x[0] - y[0] || x[1] - y[1]) };
  };
  // what a diagonal e_a + s e_{b+8} annihilates, restricted to a set of assessor indices (or all)
  B.kills = (a, b, s) => B.zdPairs().filter(p => p[0] === a && p[1] === b && p[2] === s).map(p => [p[3], p[4], p[5]]);

  // ---- symmetric eigenvalues (Jacobi) -- for the octahedral Laplacian spectrum
  B.eig = function (M) {
    const n = M.length, A = M.map(r => r.slice());
    for (let sweep = 0; sweep < 100; sweep++) {
      let off = 0; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) off += A[i][j] * A[i][j];
      if (off < 1e-22) break;
      for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) {
        if (Math.abs(A[p][q]) < 1e-300) continue;
        const th = (A[q][q] - A[p][p]) / (2 * A[p][q]), t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1)), c = 1 / Math.sqrt(t * t + 1), s = t * c;
        for (let k = 0; k < n; k++) { const kp = A[k][p], kq = A[k][q]; A[k][p] = c * kp - s * kq; A[k][q] = s * kp + c * kq; }
        for (let k = 0; k < n; k++) { const pk = A[p][k], qk = A[q][k]; A[p][k] = c * pk - s * qk; A[q][k] = s * pk + c * qk; }
      }
    }
    return A.map((r, i) => r[i]).sort((x, y) => x - y);
  };
  B.laplacian = function (n, edges) { const L = Array.from({ length: n }, () => Array(n).fill(0)); for (const [i, j] of edges) { L[i][i]++; L[j][j]++; L[i][j]--; L[j][i]--; } return L; };
  B.spectrum = edges => B.eig(B.laplacian(6, edges));

  // ---- the labelled octonion group: signed permutations of e1..e7 preserving the octonion table; each = {p:[images of 1..7], g:[signs]}
  B.octLines = function () { const L = new Set(); for (let i = 1; i < 8; i++) for (let j = i + 1; j < 8; j++) L.add([i, j, B.mul(i, j)[1]].sort((x, y) => x - y).join(',')); return [...L].map(s => s.split(',').map(Number)); };
  B.perms7 = function () { const out = [], a = [1, 2, 3, 4, 5, 6, 7]; (function rec(k) { if (k === 7) { out.push(a.slice()); return; } for (let i = k; i < 7; i++) { [a[k], a[i]] = [a[i], a[k]]; rec(k + 1); [a[k], a[i]] = [a[i], a[k]]; } })(0); return out; };
  B.group = function () {
    if (B._grp) return B._grp;
    const lines = new Set(B.octLines().map(l => l.join(','))), fano = [], all = [];
    for (const p of B.perms7()) { const f = i => (i === 0 ? 0 : p[i - 1]); if ([...lines].every(l => { const [a, b, c] = l.split(',').map(Number); return lines.has([f(a), f(b), f(c)].sort((x, y) => x - y).join(',')); })) fano.push(p); }
    for (const p of fano) for (let m = 0; m < 128; m++) {
      const g = [1, ...Array.from({ length: 7 }, (_, i) => (m >> i & 1 ? -1 : 1))];                // g[0] = 1; g[i] = sign of e_i's image
      const f = i => (i === 0 ? 0 : p[i - 1]); let ok = true;
      for (let i = 1; i < 8 && ok; i++) for (let j = 1; j < 8; j++) { const [s, k] = B.mul(i, j), [s2, k2] = B.mul(f(i), f(j)); if (f(k) !== k2 || g[i] * g[j] * s2 !== s * g[k]) { ok = false; break; } }
      if (ok) all.push({ p, g });
    }
    return (B._grp = { fano, all });
  };
  // extension to the sedenions: act alike on e_i and e_{i+8}; checked against the full 16 x 16 table
  B.extendsToSedenions = function (el) {
    const f = i => (i % 8 === 0 ? i : el.p[i % 8 - 1] + (i >= 8 ? 8 : 0)), g = i => el.g[i % 8];
    for (let i = 0; i < 16; i++) for (let j = 0; j < 16; j++) { const [s, k] = B.mul(i, j), [s2, k2] = B.mul(f(i), f(j)); if (f(k) !== k2 || g(i) * g(j) * s2 !== s * g(k)) return false; }
    return true;
  };
  B.cycleType = function (p) { const seen = new Set(), c = []; for (let s = 1; s < 8; s++) { if (seen.has(s)) continue; let n = 0, x = s; while (!seen.has(x)) { seen.add(x); x = p[x - 1]; n++; } c.push(n); } return c.sort((a, b) => b - a).join(''); };
  B.cycles = function (p) { const seen = new Set(), c = []; for (let s = 1; s < 8; s++) { if (seen.has(s)) continue; const cy = []; let x = s; while (!seen.has(x)) { seen.add(x); cy.push(x); x = p[x - 1]; } c.push(cy); } return c; };
  // orbit and stabiliser of the unit point (e_1 + e_{2+8})/sqrt 2 (a=1, sign +, b=2, sign +) under the group of order 1344
  B.orbitOfPoint = function () {
    const G = B.group().all, act = (el, [a, sa, b, sb]) => [el.p[a - 1], sa * el.g[a], el.p[b - 1], sb * el.g[b]], seen = new Set(); let stab = 0;
    for (const el of G) { const q = act(el, [1, 1, 2, 1]); seen.add(q.join(',')); if (q.join(',') === '1,1,2,1') stab++; }
    return { orbit: seen.size, stabiliser: stab };
  };

  // ---- does 2^3.PSL(2,7) split?  Lift a generating pair of the 168 permutations in all 8 x 8 ways; a complement would span only 168 elements.
  B.compose = (a, b) => ({ p: a.p.map(x => b.p[x - 1]), g: a.g.map((s, i) => (i === 0 ? 1 : s * b.g[a.p[i - 1]])) });
  B.key = el => el.p.join('') + '|' + el.g.join(',');
  B.span = function (gens) { const id = { p: [1, 2, 3, 4, 5, 6, 7], g: [1, 1, 1, 1, 1, 1, 1, 1] }, seen = new Map([[B.key(id), id]]); let fr = [id];
    while (fr.length) { const nx = []; for (const x of fr) for (const g of gens) { const y = B.compose(x, g), k = B.key(y); if (!seen.has(k)) { seen.set(k, y); nx.push(y); } } fr = nx; } return seen; };
  B.permOrder = function (p) { let y = p.slice(), n = 1; while (y.some((v, i) => v !== i + 1)) { y = y.map(v => p[v - 1]); n++; } return n; };
  B.split = function () {
    const G = B.group(), by = {}; G.all.forEach(el => (by[el.p.join('')] = by[el.p.join('')] || []).push(el));
    const triv = p => ({ p, g: [1, 1, 1, 1, 1, 1, 1, 1] }), seven = G.fano.find(p => B.permOrder(p) === 7);
    const inv = G.fano.find(q => B.permOrder(q) === 2 && new Set([...B.span([triv(seven), triv(q)]).values()].map(e => e.p.join(''))).size === 168);
    const orders = new Set(); let tried = 0;
    for (const a of by[seven.join('')]) for (const b of by[inv.join('')]) { orders.add(B.span([a, b]).size); tried++; }
    return { tried, orders: [...orders].sort((x, y) => x - y), split: orders.has(168) };
  };

  // ---- orthographic orbit camera.  A scene is drawn by calling view.p(x,y,z) -> {x,y,d} (d: larger = further) in a callback.
  B.View = function (canvas, draw, opt) {
    opt = opt || {}; const v = this; v.yaw = opt.yaw !== undefined ? opt.yaw : -0.7; v.pitch = opt.pitch !== undefined ? opt.pitch : 0.5; v.zoom = opt.zoom || 1; v.orbit = false; v.drag = false;
    v.home = { yaw: v.yaw, pitch: v.pitch, zoom: v.zoom };
    v.p = function (x, y, z) {
      const cy = Math.cos(v.yaw), sy = Math.sin(v.yaw), x1 = x * cy - y * sy, y1 = x * sy + y * cy, cp = Math.cos(v.pitch), sp = Math.sin(v.pitch), y2 = y1 * cp - z * sp, z2 = y1 * sp + z * cp;
      const W = canvas.width, H = canvas.height, sc = Math.min(W, H) * 0.30 * v.zoom;
      return { x: W / 2 + x1 * sc, y: H / 2 - z2 * sc, d: y2 };
    };
    v.draw = () => draw(v);
    let lx = 0, ly = 0, moved = 0;
    canvas.addEventListener('pointerdown', e => { v.drag = true; moved = 0; lx = e.clientX; ly = e.clientY; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener('pointermove', e => { if (!v.drag) return; const dx = e.clientX - lx, dy = e.clientY - ly; moved += Math.abs(dx) + Math.abs(dy); lx = e.clientX; ly = e.clientY; v.yaw += dx * 0.008; v.pitch = Math.max(-1.5708, Math.min(1.5708, v.pitch + dy * 0.008)); v.draw(); });
    canvas.addEventListener('pointerup', e => { v.drag = false; if (moved < 4 && opt.onclick) { const r = canvas.getBoundingClientRect(); opt.onclick((e.clientX - r.left) * canvas.width / r.width, (e.clientY - r.top) * canvas.height / r.height); } });
    canvas.addEventListener('wheel', e => { e.preventDefault(); v.zoom = Math.max(0.4, Math.min(4, v.zoom * (e.deltaY < 0 ? 1.1 : 0.9))); v.draw(); }, { passive: false });
    canvas.addEventListener('dblclick', () => { v.yaw = v.home.yaw; v.pitch = v.home.pitch; v.zoom = v.home.zoom; v.draw(); });
    v.pose = (y, p) => { v.yaw = y; v.pitch = p; v.orbit = false; v.draw(); };
    setInterval(() => { if (v.orbit && !v.drag && !matchMedia('(prefers-reduced-motion: reduce)').matches) { v.yaw += 0.012; v.draw(); } }, 60);
  };
  // the orientation gizmo: three labelled axes from a corner point
  B.gizmo = function (g, view, ox, oy, labels, colors) {
    const dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]], o = view.p(0, 0, 0), fg = getComputedStyle(document.body).color;
    g.font = '12px system-ui'; g.lineWidth = 2;
    dirs.forEach((d, i) => { const q = view.p(d[0], d[1], d[2]), dx = (q.x - o.x) * 0.34, dy = (q.y - o.y) * 0.34; g.strokeStyle = colors[i]; g.beginPath(); g.moveTo(ox, oy); g.lineTo(ox + dx, oy + dy); g.stroke(); g.fillStyle = colors[i]; g.fillText(labels[i], ox + dx * 1.18 + 3, oy + dy * 1.18 + 4); });
    g.fillStyle = fg; g.beginPath(); g.arc(ox, oy, 2.5, 0, 7); g.fill();
  };
  B.css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  // octahedron coordinates for strut s: axis k carries the k-th reversal pair (non_edges), first member at +1, second at -1
  B.octCoords = function (s) { const ax = D.struts[s].non_edges; return D.struts[s].vertices.map((v, i) => { const k = ax.findIndex(e => e.includes(i)), c = [0, 0, 0]; c[k] = ax[k][0] === i ? 1 : -1; return c; }); };
  B.label = v => '(' + v[0] + ',' + (v[1] + 8) + ')';

  // ---- self-check: every JS number against the engine's
  B.selfCheck = function () {
    const out = [], ok = (name, c) => out.push((c ? '✓ ' : '✗ ') + name);
    let same = true; for (let i = 0; i < 16; i++) for (let j = 0; j < 16; j++) { const t = D.table[i * 16 + j]; if (B.table[i][j][0] !== t[0] || B.table[i][j][1] !== t[1]) same = false; }
    ok('Cayley–Dickson table (256 entries) equals the engine\'s', same);
    const def = B.defectAll(); let nz = 0, dm = 0; for (let n = 0; n < 4096; n++) { if (def[n] > 1e-9) nz++; dm = Math.max(dm, Math.abs(def[n] - D.defect[n])); }
    ok('associator: ' + nz + ' of 4096 non-zero (engine ' + D.census.nonzero + '), norms agree to ' + dm.toExponential(1), nz === D.census.nonzero && dm < 1e-8);
    const zd = B.zdPairs(); ok('zero-divisor pairs: ' + zd.length + ' ordered (engine ' + D.zd_pairs.length + ')', zd.length === D.zd_pairs.length && zd.length === 336);
    let kitesOK = true, specOK = true;
    for (let s = 1; s < 8; s++) { const k = B.kite(s), e = D.struts[s].edges; if (JSON.stringify(k.edges) !== JSON.stringify(e)) kitesOK = false; const sp = B.spectrum(k.edges), ref = D.struts[s].spectrum; if (sp.some((x, i) => Math.abs(x - ref[i]) > 1e-7)) specOK = false; }
    ok('7 box-kites: edges recomputed from the products equal the engine\'s (12 each, octahedra)', kitesOK);
    ok('octahedral spectrum {0,4,4,4,6,6} recomputed for all 7', specOK);
    const G = B.group(); ok('labelled group: ' + G.all.length + ' signed automorphisms = ' + G.fano.length + ' permutations × ' + G.all.length / G.fano.length + ' signs (engine ' + D.aut.signed_automorphisms + ' = ' + D.aut.fano_permutations + ' × ' + D.aut.sign_kernel + ')',
       G.all.length === D.aut.signed_automorphisms && G.fano.length === D.aut.fano_permutations);
    const ct = {}; G.fano.forEach(p => (ct[B.cycleType(p)] = (ct[B.cycleType(p)] || 0) + 1));
    ok('cycle types of the 168: ' + JSON.stringify(ct), JSON.stringify(Object.keys(ct).sort().map(k => [k, ct[k]])) === JSON.stringify(Object.keys(D.cycle_types).sort().map(k => [k, D.cycle_types[k]])));
    ok('all 1344 extend to the sedenions', G.all.every(B.extendsToSedenions));
    const ob = B.orbitOfPoint(); ok('orbit of one unit zero-divisor point: ' + ob.orbit + ', stabiliser ' + ob.stabiliser + ' (engine ' + D.aut.orbits_on_unit_points[0] + ', ' + D.aut.point_stabiliser + ')', ob.orbit === D.aut.orbits_on_unit_points[0] && ob.stabiliser === D.aut.point_stabiliser);
    const sp = B.split(); ok('split search in the browser: ' + sp.tried + ' lift pairs, subgroup orders ' + JSON.stringify(sp.orders) + ', split = ' + sp.split + ' (engine ' + JSON.stringify(D.split.subgroup_orders) + ', split = ' + D.split.split + ')', sp.tried === D.split.lift_pairs_tried && JSON.stringify(sp.orders) === JSON.stringify(D.split.subgroup_orders) && sp.split === D.split.split);
    const el = document.getElementById('selfcheck'); if (el) { const bad = out.filter(s => s[0] === '✗').length; el.innerHTML = '<b class="' + (bad ? 'bad' : 'ok') + '">Self-check: ' + (bad ? bad + ' mismatch' : 'all agree with the Python engine') + '</b><br><span class="mono pre">' + out.join('\n') + '</span>'; }
    return out;
  };
  window.BK = B;
})();
