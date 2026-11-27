// SPDX-License-Identifier: GPL-3.0-only
// t32.js -- JavaScript port of ValaQuenta/modules/t32_nilpotency/maths.py (t32_mul, Hyperwebster address, square law, detector).
// The port checks itself against vectors baked from the Python module (t32_data.js); each page prints the result in #selfcheck.
(function () {
  const D = window.T32DATA, T = {};
  T.data = D;
  // Recursive Cayley-Dickson multiplication over GF(2); words are unsigned 32-bit, dim a power of 2 up to 32.
  function mul(a, b, dim) {
    if (dim === 1) return (a & b) >>> 0;
    const h = dim >>> 1, m = ((1 << h) - 1) >>> 0;
    const a1 = (a & m) >>> 0, a2 = (a >>> h) >>> 0, b1 = (b & m) >>> 0, b2 = (b >>> h) >>> 0;
    const lo = (mul(a1, b1, h) ^ mul(b2, a2, h)) >>> 0, hi = (mul(b2, a1, h) ^ mul(a2, b1, h)) >>> 0;
    return ((lo | (hi << h)) >>> 0);
  }
  T.mul = mul;
  T.ones = dim => (dim === 32 ? 0xFFFFFFFF : ((1 << dim) - 1)) >>> 0;
  T.sq = (w, dim) => mul(w, w, dim);
  T.parity = w => { let c = 0; w >>>= 0; while (w) { c ^= 1; w &= w - 1; } return c; };            // popcount mod 2: the closed form of w.w
  T.delta = (w, dim) => mul(w, T.ones(dim), dim);                       // the detector  w . 1
  T.cls = (w, dim) => { const s = mul(w, w, dim); return s === 0 ? 'n' : s === 1 ? 'i' : 'o'; };   // n nilpotent (incl. 0), i involutory, o other
  const IDX = {}; Array.from(D.hw_chars).forEach((c, i) => { IDX[c] = i; });
  T.hwIndex = IDX;
  T.hwAddress = function (n) {                                          // bijective base-97 Horner address of str(n), 0-based
    const s = String(n); let a = 0n, p = 1n;
    for (let i = s.length - 1; i >= 0; i--) { a += BigInt(IDX[s[i]] + 1) * p; p *= 97n; }
    return a - 1n;
  };
  T.hwToT32 = n => Number(T.hwAddress(n) & 0xFFFFFFFFn);
  T.hex = (w, dim) => '0x' + w.toString(16).toUpperCase().padStart(Math.max(1, dim >>> 2), '0');
  T.bin = (w, dim) => w.toString(2).padStart(dim, '0');
  T.parse = function (s, dim) {                                         // decimal, 0x hex or 0b binary; reduced to dim bits
    s = String(s).trim().toLowerCase(); let v = NaN;
    if (/^0x[0-9a-f]+$/.test(s)) v = parseInt(s, 16); else if (/^0b[01]+$/.test(s)) v = parseInt(s.slice(2), 2); else if (/^\d+$/.test(s)) v = Number(s);
    if (!isFinite(v)) return null; return (dim === 32 ? v >>> 0 : (v & ((1 << dim) - 1)) >>> 0);
  };
  T.cvar = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  T.setup = function (cv, w, h) {                                       // a canvas of CSS size w x h with a DPR-sized backing store
    const r = window.devicePixelRatio || 1; cv.style.width = w + 'px'; cv.style.height = h + 'px'; cv.width = Math.round(w * r); cv.height = Math.round(h * r);
    const g = cv.getContext('2d'); g.setTransform(r, 0, 0, r, 0, 0); return g;
  };
  T.selfCheck = function () {
    let m = 0, s = 0, h = 0, c = 0, e = 0;
    D.mul_vectors.forEach(v => { if (mul(v[0], v[1], 32) === v[2]) m++; });
    D.square_vectors.forEach(v => { if (mul(v[0], v[0], 32) === v[1] && v[1] === T.parity(v[0])) s++; });
    D.hw_vectors.forEach(v => { if (T.hwAddress(v[0]) === BigInt(v[1]) && T.hwToT32(v[0]) === v[2]) h++; });
    Object.keys(D.census).forEach(k => { const d = +k, py = D.census[k]; let n = 0, i = 0, o = 0; for (let w = 0; w < (1 << d); w++) { const x = T.cls(w, d); if (x === 'n') n++; else if (x === 'i') i++; else o++; } if (n === py.nilpotent && i === py.involutory && o === py.other) c++; });
    const ok = m === D.mul_vectors.length && s === D.square_vectors.length && h === D.hw_vectors.length && c === Object.keys(D.census).length;
    const el = document.getElementById('selfcheck');
    if (el) el.innerHTML = '<span class="' + (ok ? 'ok' : 'bad') + '">self-check ' + (ok ? 'passed' : 'FAILED') + '</span>: this page\'s JavaScript port matches the Python engine on ' + m + '/' + D.mul_vectors.length + ' products, ' + s + '/' + D.square_vectors.length + ' squares (each equal to the weight parity), ' + h + '/' + D.hw_vectors.length + ' Hyperwebster addresses, ' + c + '/' + Object.keys(D.census).length + ' exhaustive censuses.';
    return ok;
  };
  window.T32 = T;
})();
