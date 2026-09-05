"""
ainulindale_engine.engine.console_curses
==========================================
Curses console — the DERIVATION BROWSER.  Ptolemy /derivation shortcut mode.

A file-manager over the registry.  You pick ValaQuenta apart one scope at a
time — `dir()`-style — the way APISniff's CodeBrowser walks a package.  The
breadcrumb IS the API path (`/ <engine> / <equation>`); the engine naming
conventions ARE the function breadcrumbs.

    +--------------------------------------------------------+
    | ValaQuenta · DERIVATION BROWSER            v0.155      |
    | /  emerger  /  emerge                                 |   breadcrumb = API path
    +---------------------------+----------------------------+
    | ..                        | DECLARATION               |
    | verify                ✓   |   <plain-English, outside- |
    | > emerge              ◈   |    observer, one line of   |
    | firing_order          ◈   |    what this does as a     |
    | domain_of             ✓   |    derivation step>        |
    | ...                       |                            |
    | (LISTING — one dir())     | latex / radian / params   |
    |                           | [Enter] run   [p] proof   |
    +---------------------------+----------------------------+
    | ↑↓ nav  →/Enter open·run  ←/⌫ up  / filter  d mode  q |
    +--------------------------------------------------------+

The root listing is grouped PROCEDURALLY from the engine manifests
(modules/<engine>/manifest.json — Full Engine Protocol part 2c): group
headers, tools, display modes, analysis lenses and provenance all come from
the manifest, nothing is hand-maintained here.  A missing manifest is
scaffolded live from the registry so the Tab is always complete.

Keys:
    Up / Down       move the selection (skips group headers; scrolls a RESULT
                    with Tab-focus RIGHT)
    Enter / Right   descend (group → engine → equation), or run, or up on '..'
    Left / Bksp     up one level
    Tab             toggle focus LEFT (listing) / RIGHT (result scroll)
    /               filter the current listing
    a               analysis-lens menu (per-engine from the manifest)
    i               manifest / provenance panel for the current engine
    d               cycle display mode (per-engine from the manifest)
    p               proof-on-the-fly INPUTS for the selected equation
    r               re-run
    q / Esc         quit

Version: 0.160 — procedural menus from the engine manifests
"""

import ast
import curses
import json
import textwrap
from typing import Any, Dict, List, Optional, Tuple

from .registry import ModuleRegistry, CONFIDENCE
from . import manifest


# ── Colour pair IDs ───────────────────────────────────────────────────────────
C_NORMAL, C_ACCENT, C_DIM, C_GOLD, C_TEAL, C_ORANGE, C_RED, C_TITLE = range(8)

CONFIDENCE_COLOUR_ID = {
    'ESTABLISHED': C_GOLD, 'THEORETICAL': C_TEAL,
    'CONJECTURE': C_ORANGE, 'OPEN': C_RED,
}
DISPLAY_MODES = ['text', 'complex_plane', '3d_cartesian', 'fano', 'sonification']

# Analysis toolset — the browser runs these ACROSS any engine's mathematics.
# The Emerger (sedenion bracketing) and the FactoralDecomposition tools are
# lenses; you pick a result or an engine, then run a lens on it.
ANALYSIS_TOOLS = [
    ('emerge',    'Sedenion bracketing & firing order — bracket the result as a 16-vector'),
    ('spectral',  'Factor the result signal into its wavelengths (FactoralDecomposition)'),
    ('lineage',   'Generational lineage / two-trees of the result, if it is an integer'),
    ('calibrate', 'Run the factoral decomposition ON this engine (FD vq_lineage_of)'),
]


def _probe_tool(name):
    """Lazy import probe.  Returns (callable_or_None, note)."""
    try:
        if name == 'emerge':
            from ..modules.emerger import emerge  # noqa: PLC0415
            return emerge, 'ValaQuenta.modules.emerger'
        if name == 'spectral':
            from FactoralDecomposition.engine import spectral_decompose  # noqa: PLC0415
            return spectral_decompose, 'FactoralDecomposition.engine'
        if name == 'lineage':
            from FactoralDecomposition.engine import factor_lineage  # noqa: PLC0415
            return factor_lineage, 'FactoralDecomposition.engine'
        if name == 'calibrate':
            from FactoralDecomposition.engine import vq_lineage_of  # noqa: PLC0415
            return vq_lineage_of, 'FactoralDecomposition.engine'
    except Exception as e:                       # noqa: BLE001
        return None, f'unavailable: {type(e).__name__}'
    return None, 'unknown tool'


def _init_colours():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(C_ACCENT, curses.COLOR_CYAN, -1)
    curses.init_pair(C_DIM, curses.COLOR_WHITE, -1)
    curses.init_pair(C_GOLD, curses.COLOR_YELLOW, -1)
    curses.init_pair(C_TEAL, curses.COLOR_GREEN, -1)
    curses.init_pair(C_ORANGE, curses.COLOR_MAGENTA, -1)
    curses.init_pair(C_RED, curses.COLOR_RED, -1)
    curses.init_pair(C_TITLE, curses.COLOR_BLACK, curses.COLOR_CYAN)


def _safe_addstr(win, y, x, text, attr=0):
    h, w = win.getmaxyx()
    if y < 0 or y >= h:
        return
    if x < 0:
        text, x = text[-x:], 0
    if x >= w:
        return
    text = text[:w - x - 1]
    if not text:
        return
    try:
        win.addstr(y, x, text, attr)
    except curses.error:
        pass


def _box(win, title, colour_pair=C_ACCENT):
    win.box()
    _safe_addstr(win, 0, 2, f' {title} ', curses.color_pair(colour_pair) | curses.A_BOLD)


def _match_brace(s, i):
    """Index of the '}' matching the '{' at s[i], or -1. Quote-aware."""
    depth, q = 0, None
    for k in range(i, len(s)):
        c = s[k]
        if q is not None:
            if c == q and s[k - 1] != '\\':
                q = None
            continue
        if c in '"\'':
            q = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return k
    return -1


def _expand_mapping(span):
    """A '{...}' literal -> one entry per line (via _pp), or None if it
    isn't a dict."""
    for loader in (json.loads, ast.literal_eval):
        try:
            obj = loader(span)
        except (ValueError, SyntaxError):
            continue
        if isinstance(obj, dict):
            return _pp(obj)
    return None


def _reflow(text):
    """Break any Python/JSON dict literal embedded in `text` onto one entry
    per line. Leaves prose and non-mapping braces (LaTeX \\frac{a}{b}, sets)
    alone — only spans that actually parse as a dict are expanded."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text[i] == '{':
            j = _match_brace(text, i)
            if j - i > 8:
                exp = _expand_mapping(text[i:j + 1])
                if exp is not None:
                    out.append('\n' + exp)
                    i = j + 1
                    continue
        out.append(text[i])
        i += 1
    return ''.join(out)


def _prettify(obj):
    """Result panel: dict/list -> one entry per line; a string with a dict
    literal in it -> that literal broken onto one entry per line; prose ->
    unchanged."""
    if isinstance(obj, (dict, list, tuple)):
        return _pp(obj)
    if isinstance(obj, str):
        s = obj.strip()
        if s[:1] in ('{', '['):
            for loader in (json.loads, ast.literal_eval):
                try:
                    return _pp(loader(s))
                except (ValueError, SyntaxError):
                    pass
        return _reflow(obj)
    return str(obj)


def _pp(obj, indent=0, depth=0):
    """Compact recursive pretty-print for lens output (dicts / lists / scalars)."""
    pad = '  ' * indent
    if depth > 5:
        return pad + '…'
    if isinstance(obj, dict):
        rows = []
        for k, v in list(obj.items())[:40]:
            if isinstance(v, (dict, list, tuple)) and v:
                rows.append(f'{pad}{k}:')
                rows.append(_pp(v, indent + 1, depth + 1))
            else:
                rows.append(f'{pad}{k}: {v!r}'[:200])
        return '\n'.join(rows)
    if isinstance(obj, (list, tuple)):
        if all(not isinstance(x, (dict, list, tuple)) for x in obj):
            return pad + str(list(obj))[:200]
        return '\n'.join(_pp(x, indent + 1, depth + 1) for x in obj[:20])
    return pad + repr(obj)[:200]


# ═══════════════════════════════════════════════════════════════════════════════
class DerivationBrowser:
    """One scope at a time.  path = [] | [engine] | [engine, equation]."""

    RUN_ROW = '‹ run ▸ ›'

    def __init__(self, stdscr, registry: ModuleRegistry):
        self._scr = stdscr
        self._reg = registry
        self._modules: List[str] = registry.list_modules()

        # ── procedural menu from the engine manifests (Full Engine Protocol 2c)
        self._menu = manifest.menu_tree(registry)
        self._entry: Dict[str, Dict[str, Any]] = {}
        self._grouped: List[Tuple[str, List[str]]] = []
        self._headers: set = set()
        for g in self._menu['groups']:
            names = []
            for e in g['engines']:
                self._entry[e['engine']] = e
                names.append(e['engine'])
            label = f"── {g['group']} ──"
            self._headers.add(label)
            self._grouped.append((label, names))

        self.path: List[str] = []
        self.sel: int = 0
        self.filter: str = ''
        self.mode_idx: int = 0
        self.result: Optional[List[str]] = None
        self.result_scroll: int = 0
        self.focus_right: bool = False
        self.show_tools: bool = False          # 'a' — the analysis lens menu
        self.show_info: bool = False           # 'i' — the manifest / provenance panel
        self._last_value: Any = None           # last equation run value, for the lenses

    # ── navigation model ────────────────────────────────────────────────────
    def _engine_eqs(self, engine: str) -> List[str]:
        return [k.split('.', 1)[1] for k in self._reg.list_equations(engine)]

    def _engine_entry(self, engine: str) -> Dict[str, Any]:
        return self._entry.get(engine, {})

    def _engine_lenses(self, engine: str) -> List[str]:
        lenses = self._engine_entry(engine).get('analysis_lenses') or []
        return lenses or [t[0] for t in ANALYSIS_TOOLS]

    def _root_rows(self) -> List[str]:
        """Grouped engine listing from the manifests: header rows (── group ──,
        not selectable) interleaved with their engines."""
        rows: List[str] = []
        for label, names in self._grouped:
            rows.append(label)
            rows.extend(names)
        return rows

    def _listing(self) -> List[str]:
        if self.show_tools:
            engine = self.path[0] if self.path else ''
            return ['..'] + self._engine_lenses(engine)
        if not self.path:
            items = self._root_rows()
        elif len(self.path) == 1:
            items = ['..'] + self._engine_eqs(self.path[0])
        else:
            items = ['..', self.RUN_ROW]
        if self.filter:
            f = self.filter.lower()
            items = [i for i in items
                     if i in ('..', self.RUN_ROW) or i in self._headers
                     or f in i.lower()]
        return items or ['..']

    def _current_equation(self):
        if len(self.path) == 2:
            return self._reg.get_equation(f'{self.path[0]}.{self.path[1]}')
        return None

    def _selected(self) -> str:
        lst = self._listing()
        self.sel = max(0, min(self.sel, len(lst) - 1))
        # never land on a non-selectable group header
        if lst[self.sel] in self._headers:
            fwd = [i for i in range(self.sel, len(lst)) if lst[i] not in self._headers]
            bwd = [i for i in range(self.sel, -1, -1) if lst[i] not in self._headers]
            if fwd:
                self.sel = fwd[0]
            elif bwd:
                self.sel = bwd[0]
        return lst[self.sel]

    def _step_sel(self, delta: int) -> None:
        """Move the selection by `delta`, skipping group-header rows."""
        lst = self._listing()
        i = self.sel
        while True:
            i += delta
            if i < 0 or i >= len(lst):
                return
            if lst[i] not in self._headers:
                self.sel = i
                return

    def _modes(self) -> List[str]:
        """Display modes for the current engine, from its manifest; the global
        list otherwise."""
        if self.path:
            m = self._engine_entry(self.path[0]).get('display_modes')
            if m:
                return m
        return DISPLAY_MODES

    def _mode(self) -> str:
        modes = self._modes()
        return modes[self.mode_idx % len(modes)]

    # ── actions ─────────────────────────────────────────────────────────────
    def _enter(self):
        item = self._selected()
        if item in self._headers:
            return
        if item == '..':
            self._up()
            return
        if self.show_tools:                      # run an analysis lens
            self._run_tool(item)
            return
        if not self.path:                       # root -> engine
            self.path = [item]; self.sel = 0; self.filter = ''
        elif len(self.path) == 1:               # engine -> equation
            self.path = [self.path[0], item]; self.sel = 0; self.filter = ''
            self.result = None; self._last_value = None
        elif item == self.RUN_ROW:
            self._run()

    def _up(self):
        if self.show_tools:
            self.show_tools = False
            self.sel = 0
            return
        if self.path:
            self.path.pop()
        self.sel = 0
        self.filter = ''
        self.result = None
        self._last_value = None
        self.focus_right = False

    def _run(self):
        eq = self._current_equation()
        if eq is None:
            return
        engine, name = self.path
        mod = self._reg.get_module(engine)
        params = {p: 1.0 for p in (eq.params or [])}
        def _try(call):
            for p in (params, {}):              # params-filled, then argument-free
                try:
                    return call(p), None
                except Exception as e:          # noqa: BLE001
                    last = e
            return None, last

        data, err = _try(lambda p: mod.viewer_data(name, p, self._mode()))
        if data:
            text = _prettify(data.get('text') or data)
        else:
            text = f'ERROR: {type(err).__name__}: {err}'
        val, _ = _try(lambda p: mod.run(name, p).get('result'))
        self._last_value = val
        self.result = self._wrap(f'▸ RESULT  ({engine}.{name}, mode={self._mode()})\n\n{text}'
                                 f'\n\n[a] run an analysis lens on this result')
        self.result_scroll = 0
        self.focus_right = True

    def _proof_inputs(self):
        """Proof-on-the-fly seam. Shows the DECLARATION data plus, when a
        proof_locale catalog exists for this engine, the GUIDED ordered
        operator steps (the English puzzle pieces the sympy derivation fills).
        Toggle guided / academic rendering with `p` again."""
        eq = self._current_equation()
        if eq is None or not self.path:
            return
        engine = self.path[0]
        d = eq.declaration()
        self._proof_academic = not getattr(self, '_proof_academic', True)  # first p = guided
        try:
            from .proof_locale import render_guided, render_academic, proof_catalog
        except Exception:                          # noqa: BLE001
            render_guided = render_academic = proof_catalog = None

        lines = [f'▸ PROOF-ON-THE-FLY  ({engine}.{eq.name})', '',
                 f"process    : {d['process']}",
                 f"latex      : {d['latex']}",
                 f"radian_form: {d['radian_form']}",
                 f"params     : {', '.join(d['params']) or '(none)'}",
                 f"confidence : {d['confidence']}   code_verified: {d['code_verified']}",
                 '']
        if proof_catalog and proof_catalog(engine):
            body = (render_academic if self._proof_academic else render_guided)(engine, eq.name)
            lines += [f"── proof_locale  [{'academic' if self._proof_academic else 'guided'}]"
                      f"  (p toggles) ──", '', body]
        else:
            lines += ['[proof engine: sympy step-by-step — TODO]',
                      f'[no proof_locale catalog for {engine!r} yet]']
        self.result = self._wrap('\n'.join(lines))
        self.result_scroll = 0
        self.focus_right = True

    # ── analysis lenses — run a tool ACROSS the current mathematics ─────────
    def _numbers_in(self, obj, out=None, depth=0):
        """Every real number reachable in a value (list/tuple/dict/nested)."""
        out = [] if out is None else out
        if depth > 6:
            return out
        if isinstance(obj, bool):
            return out
        if isinstance(obj, (int, float)):
            out.append(float(obj)); return out
        if isinstance(obj, dict):
            for v in obj.values():
                self._numbers_in(v, out, depth + 1)
        elif isinstance(obj, (list, tuple, set)):
            for v in obj:
                self._numbers_in(v, out, depth + 1)
        return out

    def _analysis_value(self):
        """Best input for a lens: the last run value, else run the current
        equation argument-free."""
        if self._last_value is not None:
            return self._last_value
        eq = self._current_equation()
        if eq and eq.compute:
            try:
                self._last_value = eq.compute(*[1.0 for _ in (eq.params or [])]) \
                    if eq.params else eq.compute()
            except Exception as e:              # noqa: BLE001
                self._last_value = f'ERROR: {type(e).__name__}: {e}'
        return self._last_value

    def _run_tool(self, name):
        fn, note = _probe_tool(name)
        engine = self.path[0] if self.path else '(none)'
        head = f'▸ LENS  {name}  on  {engine}' + (
            f'.{self.path[1]}' if len(self.path) == 2 else '') + f'   [{note}]'
        if fn is None:
            self.result = self._wrap(head + '\n\n' + note +
                                     '\n\n(put the sibling repo on PYTHONPATH to enable)')
            self.result_scroll = 0; self.focus_right = True; return

        val = self._analysis_value()
        nums = self._numbers_in(val)
        try:
            if name == 'calibrate':
                res = fn(engine)
            elif name == 'lineage':
                ints = [int(round(x)) for x in nums if abs(x) >= 2 and abs(x - round(x)) < 1e-9]
                res = fn(ints[0]) if ints else '(no integer >= 2 in the result to decompose)'
            elif name == 'spectral':
                sig = nums[:512] if len(nums) >= 4 else (nums * 4)[:8]
                res = fn(sig) if sig else '(no numeric signal in the result)'
            elif name == 'emerge':
                vec = (nums + [0.0] * 16)[:16]
                res = fn(vec, mode='sigma_rb')
            else:
                res = '(unknown lens)'
        except Exception as e:                  # noqa: BLE001
            res = f'ERROR: {type(e).__name__}: {e}'
        body = res if isinstance(res, str) else _pp(res)
        self.result = self._wrap(f'{head}\n\ninput numbers: {len(nums)}\n\n{body}')
        self.result_scroll = 0
        self.focus_right = True

    @staticmethod
    def _wrap(text: str, width: int = 66) -> List[str]:
        out: List[str] = []
        for raw in text.splitlines():
            out.extend(textwrap.wrap(raw, width) or [''])
        return out

    def _read_filter(self):
        curses.echo(); curses.curs_set(1)
        h, _ = self._scr.getmaxyx()
        _safe_addstr(self._scr, h - 1, 0, ' filter: '.ljust(self._scr.getmaxyx()[1]),
                     curses.color_pair(C_TITLE))
        try:
            s = self._scr.getstr(h - 1, 9, 40).decode('utf-8', 'ignore')
        except Exception:
            s = ''
        curses.noecho(); curses.curs_set(0)
        self.filter = s.strip()
        self.sel = 0

    # ── main loop ──────────────────────────────────────────────────────────
    def run(self):
        curses.curs_set(0)
        self._scr.keypad(True)
        _init_colours()
        while True:
            self._draw()
            k = self._scr.getch()
            if k in (ord('q'), 27):
                break
            elif k == ord('\t'):
                self.focus_right = not self.focus_right and self.result is not None
            elif k == curses.KEY_UP:
                if self.focus_right and self.result:
                    self.result_scroll = max(0, self.result_scroll - 1)
                else:
                    self._step_sel(-1)
            elif k == curses.KEY_DOWN:
                if self.focus_right and self.result:
                    self.result_scroll += 1
                else:
                    self._step_sel(1)
            elif k in (curses.KEY_ENTER, 10, 13, curses.KEY_RIGHT):
                self._enter()
            elif k in (curses.KEY_LEFT, curses.KEY_BACKSPACE, 127, 8, ord('h')):
                self._up()
            elif k == ord('/'):
                self._read_filter()
            elif k == ord('d'):
                self.mode_idx += 1
            elif k == ord('p'):
                self._proof_inputs()
            elif k == ord('a'):
                self.show_tools = not self.show_tools
                self.sel = 0
            elif k == ord('i'):
                self.show_info = not self.show_info
            elif k == ord('r') and len(self.path) == 2:
                self._run()

    # ── draw ───────────────────────────────────────────────────────────────
    def _draw(self):
        self._scr.erase()
        h, w = self._scr.getmaxyx()

        _safe_addstr(self._scr, 0, 0,
                     ' ValaQuenta · DERIVATION BROWSER '.ljust(w),
                     curses.color_pair(C_TITLE) | curses.A_BOLD)
        crumb = ' /  ' + '  /  '.join(self.path) if self.path else ' /'
        if self.result is not None:
            crumb += '   ▸ ' + ('RESULT' if 'RESULT' in self.result[0] else 'PROOF')
        _safe_addstr(self._scr, 1, 0, crumb.ljust(w), curses.color_pair(C_ACCENT))

        body_y, body_h = 2, h - 3
        left_w = max(24, min(40, w // 3))

        lwin = self._scr.derwin(body_h, left_w, body_y, 0)
        self._draw_listing(lwin)
        rwin = self._scr.derwin(body_h, w - left_w, body_y, left_w)
        self._draw_right(rwin)

        focus = 'RIGHT' if self.focus_right and self.result else 'LEFT'
        status = (f' ↑↓ nav  →/Enter open·run  ←/⌫ up  Tab:{focus}  / filter'
                  f'  a:lenses  i:info  d:{self._mode()}  p:proof  q:quit ')
        if self.filter:
            status = f' [filter: {self.filter}] ' + status
        _safe_addstr(self._scr, h - 1, 0, status.ljust(w), curses.color_pair(C_DIM))
        self._scr.refresh()

    def _draw_listing(self, win):
        if self.show_tools:
            title = 'ANALYSIS LENSES'
        else:
            title = 'ENGINES' if not self.path else (
                self.path[0].upper() if len(self.path) == 1 else self.path[1])
        _box(win, title, C_ACCENT if not self.focus_right else C_DIM)
        h, w = win.getmaxyx()
        lst = self._listing()
        self.sel = max(0, min(self.sel, len(lst) - 1))
        top = max(0, self.sel - (h - 3))
        for row, item in enumerate(lst[top:top + h - 2], start=1):
            i = top + row - 1
            mark = ''
            attr = 0
            if item in self._headers:
                _safe_addstr(win, row, 1, item.ljust(w - 3),
                             curses.color_pair(C_DIM) | curses.A_BOLD)
                continue
            if not self.path and item in self._entry:
                st = self._entry[item].get('status', '')
                mark = '  ' + {'ESTABLISHED': '✓', 'THEORETICAL': '◈',
                               'CONJECTURE': '◇', 'OPEN': '?'}.get(
                    st.split(':')[0], '◈' if 'CALCULATED' in st else '')
            elif len(self.path) == 1 and item != '..':
                eq = self._reg.get_equation(f'{self.path[0]}.{item}')
                if eq:
                    attr = curses.color_pair(CONFIDENCE_COLOUR_ID.get(eq.confidence, C_NORMAL))
                    mark = '  ' + CONFIDENCE.get(eq.confidence, '?')
            if i == self.sel:
                attr |= curses.A_REVERSE | curses.A_BOLD
            _safe_addstr(win, row, 1, (item + mark).ljust(w - 3), attr)

    def _draw_right(self, win):
        if self.result is not None:
            _box(win, 'RESULT' if 'RESULT' in self.result[0] else 'PROOF INPUTS',
                 C_ACCENT if self.focus_right else C_DIM)
            h, _w = win.getmaxyx()
            view = self.result[self.result_scroll:self.result_scroll + h - 2]
            for row, line in enumerate(view, start=1):
                _safe_addstr(win, row, 2, line, curses.color_pair(C_TEAL))
            return

        _box(win, 'DECLARATION', C_ACCENT)
        h, w = win.getmaxyx()
        y = [1]

        def put(s, attr=0):
            for seg in self._wrap(s, w - 4):
                _safe_addstr(win, y[0], 2, seg, attr)
                y[0] += 1

        item = self._selected()

        if self.show_info:
            self._draw_info(put, w)
            return

        if self.show_tools:
            ctx = ('/'.join(self.path)) or '(pick an engine first)'
            engine = self.path[0] if self.path else ''
            lens_names = self._engine_lenses(engine)
            tdesc_of = dict(ANALYSIS_TOOLS)
            put('ANALYSIS LENSES', curses.color_pair(C_ACCENT) | curses.A_BOLD)
            put('Run a tool ACROSS the current mathematics — including its own.')
            put(f'context: {ctx}')
            if engine and self._engine_entry(engine).get('analysis_lenses'):
                put(f'(from {engine}/manifest.json)', curses.color_pair(C_DIM))
            put('')
            for tname in lens_names:
                fn, note = _probe_tool(tname)
                ok = '✓' if fn else '·'
                col = C_GOLD if tname == item else (C_TEAL if fn else C_DIM)
                put(f'{ok} {tname}', curses.color_pair(col) | (curses.A_BOLD if tname == item else 0))
                if tname == item:
                    put(f'   {tdesc_of.get(tname, "engine-specific lens")}', curses.color_pair(C_DIM))
                    put(f'   [{note}]', curses.color_pair(C_DIM))
            put('')
            put('Enter runs the highlighted lens on the last result, or on this '
                'equation run argument-free.  ← exits.', curses.color_pair(C_DIM))
            return

        if not self.path:                                  # ROOT
            put('ValaQuenta — the derivation engine.', curses.color_pair(C_ACCENT) | curses.A_BOLD)
            put('')
            n_missing = len(self._menu['missing_manifest'])
            put(f'{len(self._modules)} engines, '
                f'{len(self._reg.list_equations())} equations, '
                f'{len(self._menu["groups"])} groups.')
            if n_missing:
                put(f'{n_missing} engine(s) on a live scaffold — '
                    f'run manifest scaffold to seed.', curses.color_pair(C_DIM))
            put('')
            if item in self._entry:
                e = self._entry[item]
                mod = self._reg.get_module(item)
                put(f'▸ {e["display"]}  v{mod.version}',
                    curses.color_pair(C_GOLD) | curses.A_BOLD)
                put(f'{e["menu"].get("group", "")}   ·   {e["status"]}'
                    + ('   [scaffold]' if e['scaffolded'] else ''),
                    curses.color_pair(C_DIM))
                put('')
                put(e['summary'] or mod.process_description)
                put('')
                put('i → manifest / provenance panel', curses.color_pair(C_DIM))
        elif len(self.path) == 1:                           # ENGINE
            mod = self._reg.get_module(self.path[0])
            e = self._engine_entry(self.path[0])
            if item == '..':
                put(f'{mod.display_name}  v{mod.version}',
                    curses.color_pair(C_GOLD) | curses.A_BOLD)
                put(f'{e.get("menu", {}).get("group", "")}   ·   '
                    f'{e.get("status", mod.confidence_floor)}', curses.color_pair(
                    CONFIDENCE_COLOUR_ID.get(mod.confidence_floor, C_DIM)))
                put('')
                put(mod.process_description)
                put('')
                put(f'{len(self._engine_eqs(self.path[0]))} equations. '
                    f'→ steps into one.   i → manifest panel')
            else:
                eq = self._reg.get_equation(f'{self.path[0]}.{item}')
                if eq:
                    put(f'{eq.name}', curses.color_pair(C_GOLD) | curses.A_BOLD)
                    tcol = CONFIDENCE_COLOUR_ID.get(eq.confidence, C_DIM)
                    verified = '✓ code-verified' if eq.code_verified else '○ not code-verified'
                    put(f'{eq.confidence}   {verified}', curses.color_pair(tcol))
                    put('')
                    put(str(eq),
                        0 if eq.process else curses.color_pair(C_ORANGE))
                    put('')
                    put(f'params: {", ".join(eq.params) if eq.params else "(none — runs argument-free)"}')
                    put('→ steps into it.')
        else:                                              # EQUATION
            eq = self._current_equation()
            if eq is None:
                put('(equation not found)'); return
            if item == self.RUN_ROW:
                put(f'Run  {self.path[0]}.{eq.name}', curses.color_pair(C_GOLD) | curses.A_BOLD)
                put('')
                put(f'Enter runs it with default params '
                    f'({", ".join(eq.params) + " → 1.0" if eq.params else "argument-free"}), '
                    f'display mode {self._mode()}. Output replaces this pane.')
                put('')
                put('p → the proof-on-the-fly INPUTS for this step.', curses.color_pair(C_DIM))
                return
            d = eq.declaration()
            put(f'{eq.name}', curses.color_pair(C_GOLD) | curses.A_BOLD)
            tcol = CONFIDENCE_COLOUR_ID.get(eq.confidence, C_DIM)
            put(f"{d['confidence']}   {'✓ code-verified' if d['code_verified'] else '○ not code-verified'}",
                curses.color_pair(tcol))
            put('')
            put('DECLARATION', curses.color_pair(C_ACCENT) | curses.A_BOLD)
            put(d['process'], 0 if d['process_set'] else curses.color_pair(C_ORANGE))
            put('')
            put(f"display : {d['display']}", curses.color_pair(C_DIM))
            put(f"latex   : {d['latex']}", curses.color_pair(C_DIM))
            put(f"radian  : {d['radian_form']}", curses.color_pair(C_DIM))
            put(f"params  : {', '.join(d['params']) or '(none)'}")
            put('')
            put('[Enter] run    [p] proof inputs    [d] mode', curses.color_pair(C_TEAL))

    # ── the manifest / provenance panel  (key 'i') ─────────────────────────
    def _draw_info(self, put, w):
        engine = self.path[0] if self.path else self._selected()
        e = self._entry.get(engine)
        if not e:
            put('(no engine selected)'); return
        man = manifest.load(engine) or {}
        prov = e.get('provenance', {})
        env = e.get('environment', {})
        dsk = e.get('desktop', {})

        put(f'{e["display"]}', curses.color_pair(C_GOLD) | curses.A_BOLD)
        put(f'{e["menu"].get("group", "")}   ·   {e["status"]}'
            + ('   [scaffold — provenance pending]' if e['scaffolded'] else
               '   [manifest.json]'), curses.color_pair(C_DIM))
        put('')
        put('PROVENANCE', curses.color_pair(C_ACCENT) | curses.A_BOLD)
        if prov.get('origin'):
            put(prov['origin'])
        put(f"authors    : {', '.join(prov.get('authors', [])) or '—'}", curses.color_pair(C_DIM))
        put(f"created    : {prov.get('created') or '—'}", curses.color_pair(C_DIM))
        put(f"predecessors: {', '.join(prov.get('predecessors', [])) or '—'}", curses.color_pair(C_DIM))
        put(f"citations  : {', '.join(prov.get('citations', [])) or '—'}", curses.color_pair(C_DIM))
        wiki = prov.get('wiki', {})
        put(f"wiki       : {wiki.get('valaquenta') or '—'}", curses.color_pair(C_DIM))
        put(f"             {wiki.get('ainulindale') or '—'}", curses.color_pair(C_DIM))
        put(f"notebook   : {prov.get('notebook') or '—'}", curses.color_pair(C_DIM))
        put(f"proof_locale: {prov.get('proof_locale') or '—'}", curses.color_pair(C_DIM))
        put('')
        put('ENVIRONMENT', curses.color_pair(C_ACCENT) | curses.A_BOLD)
        put(f"native space: {env.get('native_space', '—')}", curses.color_pair(C_DIM))
        for c in env.get('constants', []):
            val = c.get('value')
            put(f"  {c.get('symbol', '?'):<10} {('= ' + repr(val)) if val is not None else '(engine)'}"
                f"  — {c.get('role', '')}", curses.color_pair(C_DIM))
        if env.get('requires_engines'):
            put(f"requires   : {', '.join(env['requires_engines'])}", curses.color_pair(C_DIM))
        if env.get('external'):
            put(f"external   : {', '.join(env['external'])}", curses.color_pair(C_DIM))
        put('')
        put('DESKTOP RENDERER', curses.color_pair(C_ACCENT) | curses.A_BOLD)
        put(f"window {dsk.get('window', '—')}   surface {dsk.get('surface', '—')}"
            f"   opengl {dsk.get('opengl', False)}", curses.color_pair(C_DIM))
        if dsk.get('pgui_widgets'):
            put(f"pgui widgets: {', '.join(dsk['pgui_widgets'])}", curses.color_pair(C_DIM))
        put(f"tools ({len(e.get('tools', []))})   display modes: "
            f"{', '.join(e.get('display_modes', []))}", curses.color_pair(C_DIM))
        put('')
        put('i → close panel', curses.color_pair(C_TEAL))


def run_curses(registry: ModuleRegistry):
    """Entry point called by __main__."""
    curses.wrapper(lambda stdscr: DerivationBrowser(stdscr, registry).run())
