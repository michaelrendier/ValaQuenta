// SPDX-License-Identifier: GPL-3.0-only
// hg.js -- JavaScript ports used by the hypergon_constructibility gallery: Gamma (Lanczos), the n-ball (bell_curve.nball_volume / nsphere_area),
// Gauss-Wantzel by Euler's phi, and the Niemeier enumeration (hypergon_constructibility.niemeier_root_systems).
// Each page checks these against numbers baked from the Python engines (hg_data.js) and prints the result in #selfcheck.
(function () {
  const D = window.HGDATA, H = { data: D };
  const LG = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
  H.lgamma = function (z) {                                  // ln Gamma(z) for z > 0 (Lanczos, g = 7)
    if (z < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * z))) - H.lgamma(1 - z);
    z -= 1; let x = LG[0]; for (let i = 1; i < 9; i++) x += LG[i] / (z + i);
    const t = z + 7.5; return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
  };
  H.gamma = function (z) {                                   // Gamma(z) for real z not a non-positive integer (reflection below 1/2)
    if (z < 0.5) return Math.PI / (Math.sin(Math.PI * z) * H.gamma(1 - z));
    return Math.exp(H.lgamma(z));
  };
  H.V = n => Math.exp(0.5 * n * Math.log(Math.PI) - H.lgamma(0.5 * n + 1));          // unit n-ball volume
  H.S = n => 2 * Math.exp(0.5 * n * Math.log(Math.PI) - H.lgamma(0.5 * n));          // unit sphere area S_{n-1}
  H.phi = function (n) { let r = n, m = n; for (let p = 2; p * p <= m; p++) if (m % p === 0) { while (m % p === 0) m /= p; r -= r / p; } if (m > 1) r -= r / m; return r; };
  H.isPow2 = n => n > 0 && (n & (n - 1)) === 0;
  H.constructible = n => n >= 3 && H.isPow2(H.phi(n));      // Gauss-Wantzel: phi(n) a power of 2
  H.factor = function (n) { const f = []; let m = n; for (let p = 2; p * p <= m; p++) while (m % p === 0) { f.push(p); m /= p; } if (m > 1) f.push(m); return f; };
  // Equal-Coxeter-number ADE root systems of a given rank (coin change over the components with that h)
  H.components = function (h, maxRank) {
    const o = []; if (h - 1 >= 1 && h - 1 <= maxRank) o.push(['A' + (h - 1), h - 1]);
    if (h % 2 === 0) { const n = (h + 2) / 2; if (n >= 4 && n <= maxRank) o.push(['D' + n, n]); }
    [['E6', 6, 12], ['E7', 7, 18], ['E8', 8, 30]].forEach(e => { if (e[2] === h && e[1] <= maxRank) o.push([e[0], e[1]]); });
    return o;
  };
  H.niemeier = function (rank) {
    const found = [];
    for (let h = 2; h < 2 * rank; h++) {
      const comps = H.components(h, rank);
      (function split(i, left, chosen) {
        if (left === 0) { if (chosen.length) found.push({ h, m: chosen.slice() }); return; }
        if (i === comps.length) return;
        const [name, r] = comps[i];
        for (let k = Math.floor(left / r); k >= 0; k--) split(i + 1, left - k * r, k ? chosen.concat([[name, k]]) : chosen);
      })(0, rank, []);
    }
    return found.map(s => ({ h: s.h, label: s.m.map(([n, k]) => k > 1 ? n + '^' + k : n).join(' ') }));
  };
  H.gapOf = function (systems, mod) { const r = new Set(systems.map(s => s.h % mod)), g = []; for (let k = 0; k < mod; k++) if (!r.has(k)) g.push(k); return g; };
  H.cvar = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  H.setup = function (cv, w, h) { const r = window.devicePixelRatio || 1; cv.style.width = w + 'px'; cv.style.height = h + 'px'; cv.width = Math.round(w * r); cv.height = Math.round(h * r); const g = cv.getContext('2d'); g.setTransform(r, 0, 0, r, 0, 0); g.clearRect(0, 0, w, h); return g; };
  H.selfCheck = function () {
    const out = document.getElementById('selfcheck'), bad = [];
    const rel = (a, b) => Math.abs(a - b) / Math.max(1e-300, Math.abs(b));
    D.nball_check.forEach(r => { if (rel(H.V(r.n), r.V) > 1e-10 || rel(H.S(r.n), r.S) > 1e-10) bad.push('n-ball at n=' + r.n); });
    D.gamma_check.forEach(r => { if (rel(H.gamma(r.x), r.g) > 1e-10) bad.push('Gamma(' + r.x + ')'); });
    const cons = []; for (let n = 3; n <= 70000; n++) if (H.constructible(n)) cons.push(n);
    if (cons.length !== D.constructible_to_70000.length || cons.some((v, i) => v !== D.constructible_to_70000[i])) bad.push('constructible n <= 70000');
    const sys = H.niemeier(24), g = H.gapOf(sys, 16);
    if (sys.length !== D.systems.length || sys.some((s, i) => s.h !== D.systems[i].h || s.label !== D.systems[i].label)) bad.push('the 23 Niemeier root systems');
    if (JSON.stringify(g) !== JSON.stringify(D.gap)) bad.push('gap');
    out.innerHTML = bad.length ? '<span class="bad">self-check FAILED: ' + bad.join(', ') + '</span>'
      : '<span class="ok">self-check passed</span>: Gamma, n-ball volume and area, ' + cons.length + ' constructible n ≤ 70,000, and the 23 Niemeier root systems with their gap {' + g.join(', ') + '} recomputed here equal the Python engine\'s.';
  };
  window.HG = H;
})();
