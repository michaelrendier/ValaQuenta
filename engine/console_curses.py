"""
ainulindale_engine.engine.console_curses
==========================================
Curses console GUI — Ptolemy /derivation shortcut mode.

No Qt, no VisPy. Terminal-only. Full registry access.

Layout:
    +----------------------------------+
    | AINULINDALE  v0.111              |
    +----------------+-----------------+
    | MODULE LIST    | EQUATION LIST   |
    |                |                 |
    +----------------+-----------------+
    | PARAMS         | OUTPUT          |
    |                |                 |
    +----------------------------------+
    | [ status bar ]                   |
    +----------------------------------+

Keys:
    Tab         cycle panes
    Up/Down     navigate lists
    Enter       run selected equation
    d           cycle display mode
    q / Esc     quit

Version: 0.111
"""

import curses
import textwrap
from typing import Dict, Any, List, Optional

from .registry import ModuleRegistry


# ── Colour pair IDs ───────────────────────────────────────────────────────────
C_NORMAL   = 0
C_ACCENT   = 1
C_DIM      = 2
C_GOLD     = 3
C_TEAL     = 4
C_ORANGE   = 5
C_RED      = 6
C_TITLE    = 7

CONFIDENCE_COLOUR_ID = {
    'ESTABLISHED': C_GOLD,
    'THEORETICAL': C_TEAL,
    'CONJECTURE':  C_ORANGE,
    'OPEN':        C_RED,
}

DISPLAY_MODES = ['text', 'complex_plane', '3d_cartesian', 'fano', 'sonification']


def _init_colours():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(C_ACCENT, curses.COLOR_CYAN,    -1)
    curses.init_pair(C_DIM,    curses.COLOR_WHITE,   -1)
    curses.init_pair(C_GOLD,   curses.COLOR_YELLOW,  -1)
    curses.init_pair(C_TEAL,   curses.COLOR_GREEN,   -1)
    curses.init_pair(C_ORANGE, curses.COLOR_MAGENTA, -1)
    curses.init_pair(C_RED,    curses.COLOR_RED,     -1)
    curses.init_pair(C_TITLE,  curses.COLOR_BLACK,   curses.COLOR_CYAN)


def _safe_addstr(win, y, x, text, attr=0):
    h, w = win.getmaxyx()
    if y < 0 or y >= h:
        return
    if x < 0:
        text = text[-x:]
        x = 0
    if x >= w:
        return
    text = text[:w - x]
    if not text:
        return
    try:
        win.addstr(y, x, text, attr)
    except curses.error:
        pass


def _draw_box_title(win, title: str, colour_pair: int = C_ACCENT):
    win.box()
    h, w = win.getmaxyx()
    label = f' {title} '
    _safe_addstr(win, 0, 2, label, curses.color_pair(colour_pair) | curses.A_BOLD)


class ConsoleCursesUI:

    def __init__(self, stdscr, registry: ModuleRegistry):
        self._scr = stdscr
        self._registry = registry

        self._modules: List[str] = registry.list_modules()
        self._cur_mod_idx: int = 0
        self._equations: List[str] = []
        self._cur_eq_idx: int = 0
        self._display_mode_idx: int = 0
        self._output_lines: List[str] = []
        self._params: Dict[str, Any] = {}
        self._focus: int = 0  # 0=modules 1=equations 2=output

        self._refresh_equations()

    def _refresh_equations(self):
        if not self._modules:
            self._equations = []
            return
        mod_name = self._modules[self._cur_mod_idx]
        self._equations = self._registry.list_equations(mod_name)
        self._cur_eq_idx = 0

    def _get_display_mode(self) -> str:
        return DISPLAY_MODES[self._display_mode_idx % len(DISPLAY_MODES)]

    def _run_current(self):
        if not self._equations:
            return
        full_key = self._equations[self._cur_eq_idx]
        parts = full_key.split('.', 1)
        if len(parts) != 2:
            return
        mod_name, eq_name = parts
        mod = self._registry.get_module(mod_name)
        if mod is None:
            return
        eq = self._registry.get_equation(full_key)
        mode = self._get_display_mode()

        # Default params: fill numeric params with 1.0
        params = {}
        if eq and eq.params:
            for p in eq.params:
                params[p] = self._params.get(p, 1.0)

        try:
            data = mod.viewer_data(eq_name, params, mode)
        except Exception as e:
            data = {'text': f'ERROR: {type(e).__name__}: {e}'}

        text = data.get('text', '')
        if not text:
            text = str(data)[:800]

        self._output_lines = []
        for raw_line in text.splitlines():
            self._output_lines.extend(textwrap.wrap(raw_line, 60) or [''])

    def run(self):
        curses.curs_set(0)
        self._scr.nodelay(False)
        self._scr.keypad(True)
        _init_colours()

        while True:
            self._draw()
            key = self._scr.getch()

            if key in (ord('q'), 27):  # q or Esc
                break
            elif key == ord('\t'):
                self._focus = (self._focus + 1) % 3
            elif key == ord('d'):
                self._display_mode_idx = (self._display_mode_idx + 1) % len(DISPLAY_MODES)
            elif key == curses.KEY_UP:
                if self._focus == 0 and self._cur_mod_idx > 0:
                    self._cur_mod_idx -= 1
                    self._refresh_equations()
                elif self._focus == 1 and self._cur_eq_idx > 0:
                    self._cur_eq_idx -= 1
            elif key == curses.KEY_DOWN:
                if self._focus == 0 and self._cur_mod_idx < len(self._modules) - 1:
                    self._cur_mod_idx += 1
                    self._refresh_equations()
                elif self._focus == 1 and self._cur_eq_idx < len(self._equations) - 1:
                    self._cur_eq_idx += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                self._run_current()

    def _draw(self):
        self._scr.erase()
        h, w = self._scr.getmaxyx()

        # ── Title bar ────────────────────────────────────────────────────────
        title = ' AINULINDALE  —  DERIVATION ENGINE  v0.111 '
        _safe_addstr(
            self._scr, 0, 0,
            title.ljust(w),
            curses.color_pair(C_TITLE) | curses.A_BOLD,
        )

        # ── Layout: two columns, two rows ────────────────────────────────────
        mid_y = max(4, (h - 2) // 2)
        mid_x = max(20, w // 2)

        panel_h_top = mid_y - 1
        panel_h_bot = h - mid_y - 2

        # Module list (top-left)
        mod_win = self._scr.derwin(panel_h_top, mid_x, 1, 0)
        self._draw_module_list(mod_win)

        # Equation list (top-right)
        eq_win = self._scr.derwin(panel_h_top, w - mid_x, 1, mid_x)
        self._draw_equation_list(eq_win)

        # Params (bottom-left)
        param_win = self._scr.derwin(panel_h_bot, mid_x, mid_y, 0)
        self._draw_params(param_win)

        # Output (bottom-right)
        out_win = self._scr.derwin(panel_h_bot, w - mid_x, mid_y, mid_x)
        self._draw_output(out_win)

        # Status bar
        mode = self._get_display_mode()
        focus_names = ['MODULES', 'EQUATIONS', 'OUTPUT']
        status = (
            f' Tab:focus({focus_names[self._focus]})  '
            f'↑↓:nav  Enter:run  d:mode({mode})  q:quit '
        )
        _safe_addstr(
            self._scr, h - 1, 0,
            status[:w].ljust(w),
            curses.color_pair(C_DIM),
        )

        self._scr.refresh()

    def _draw_module_list(self, win):
        focused = (self._focus == 0)
        _draw_box_title(win, 'MODULES', C_ACCENT if focused else C_DIM)
        h, w = win.getmaxyx()
        for i, mod_name in enumerate(self._modules):
            row = i + 1
            if row >= h - 1:
                break
            mod = self._registry.get_module(mod_name)
            label = (mod.display_name if mod else mod_name)[:w - 4]
            attr = curses.color_pair(C_ACCENT) | curses.A_BOLD if i == self._cur_mod_idx else 0
            _safe_addstr(win, row, 2, label, attr)

    def _draw_equation_list(self, win):
        focused = (self._focus == 1)
        _draw_box_title(win, 'EQUATIONS', C_ACCENT if focused else C_DIM)
        h, w = win.getmaxyx()
        for i, full_key in enumerate(self._equations):
            row = i + 1
            if row >= h - 1:
                break
            eq = self._registry.get_equation(full_key)
            if eq:
                c = CONFIDENCE_COLOUR_ID.get(eq.confidence, C_NORMAL)
                label = f'[{eq.confidence[0]}] {eq.display}'[:w - 4]
                attr = curses.color_pair(c)
                if i == self._cur_eq_idx:
                    attr |= curses.A_BOLD | curses.A_REVERSE
            else:
                label = full_key[:w - 4]
                attr = 0
            _safe_addstr(win, row, 2, label, attr)

    def _draw_params(self, win):
        _draw_box_title(win, f'PARAMS  mode:{self._get_display_mode()}', C_DIM)
        h, w = win.getmaxyx()
        row = 1

        if self._equations:
            eq = self._registry.get_equation(self._equations[self._cur_eq_idx])
            if eq and eq.params:
                for p in eq.params:
                    if row >= h - 1:
                        break
                    val = self._params.get(p, 1.0)
                    _safe_addstr(win, row, 2, f'{p} = {val}'[:w - 4],
                                 curses.color_pair(C_TEAL))
                    row += 1
                if row < h - 1:
                    _safe_addstr(win, row, 2, '(param edit not yet wired)',
                                 curses.color_pair(C_DIM))
            else:
                _safe_addstr(win, 1, 2, 'no params', curses.color_pair(C_DIM))

    def _draw_output(self, win):
        focused = (self._focus == 2)
        _draw_box_title(win, 'OUTPUT', C_ACCENT if focused else C_DIM)
        h, w = win.getmaxyx()
        max_lines = h - 2
        lines = self._output_lines[-max_lines:] if self._output_lines else ['Press Enter to run.']
        for i, line in enumerate(lines):
            row = i + 1
            if row >= h - 1:
                break
            _safe_addstr(win, row, 2, line[:w - 4], curses.color_pair(C_TEAL))


def run_curses(registry: ModuleRegistry):
    """Entry point called by __main__."""
    curses.wrapper(lambda stdscr: ConsoleCursesUI(stdscr, registry).run())
