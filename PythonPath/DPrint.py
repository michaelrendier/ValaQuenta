#!/usr/bin/env python3
"""
DPrint — the dPrint() protocol as an importable module: a live stream of data changes.

Standalone: standard library only, one file, no ValaQuenta import and no project path.
Put its directory on ``PYTHONPATH`` and use it from any program::

    export PYTHONPATH="$PYTHONPATH:/path/to/ValaQuenta/PythonPath"
    import DPrint as DP

Global flag (off by default): environment ``DPRINT=1`` (on) / ``DPRINT=0`` (off), or ``DP.flag = 1``.
With the flag off nothing is installed and nothing prints; decorators return the function unchanged.

THE TWO TIERS
    DP.print(...)   a checkpoint: prints ``name = value`` (the name is read from the call's own source).
    DP.watch        the automatic feed: every assignment in a scope prints as it happens, inspectable
                    all the way down (``grid[2][3] = 7``, ``self.count = 4``); a function call prints
                    its arguments; object creation prints its lineage and where it was created.

SCOPES (what the automatic feed covers)
    * ``DPRINT=1`` alone: all of YOUR code, from import time, so you can watch modules load.
      "Your code" is every file that is not the standard library, not site-packages and not generated.
    * ``DPRINT_SCOPE="Table.address,energy,mymod.*"``: only code whose ``module.qualname`` (or file
      name) matches one of the fnmatch patterns, plus what it calls.
    * ``@DP.watch`` on a function or class, or ``with DP.watch():`` around a block.
    * ``python -m DPrint [--scope PAT] script.py args...`` runs a script under the feed.

OUTPUT:  ``[dp] file.py:LINE  name = value``   (the prefix makes the feed greppable)
    DPRINT_WHERE=0   drop the file:line column        DPRINT_FILE=path   append the feed to a file
    DPRINT_DEPTH=8   how far down into containers/objects        DPRINT_ITEMS=200   items shown per container
    DPRINT_STR=500   characters shown per string      DPRINT_DEEP=1   a watched scope also watches its callees

LIMITS (stated, not hidden)
    * Python assignments only: changes made inside C extensions or by other threads' untraced code are invisible.
    * A change is attributed to the line that just ran, reported when the next line begins.
    * Containers larger than DPRINT_ITEMS are tracked by length only.
    * Tracing slows Python by an order of magnitude; narrow the scope when volume matters.
    * Uses ``sys.settrace``; it replaces a tracer already installed (debugger, coverage) while the flag is on.
"""
import ast
import fnmatch
import linecache
import os
import sys
import sysconfig
import threading
import types

__all__ = ["print", "watch", "unwatch", "on", "off", "flag", "lineage", "fmt", "main"]

_PREFIX = "[dp] "
_MISSING = object()
_lock = threading.RLock()
_tl = threading.local()
_builtin_print = print


# ── configuration ────────────────────────────────────────────────────────────
def _env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


class _Cfg:
    on = os.environ.get("DPRINT", "0") not in ("", "0")
    scope = [p.strip() for p in os.environ.get("DPRINT_SCOPE", "").split(",") if p.strip()]
    depth = _env_int("DPRINT_DEPTH", 8)
    items = _env_int("DPRINT_ITEMS", 200)
    strlen = _env_int("DPRINT_STR", 500)
    where = os.environ.get("DPRINT_WHERE", "1") not in ("", "0")
    deep = os.environ.get("DPRINT_DEEP", "1") not in ("", "0")
    file = os.environ.get("DPRINT_FILE", "")
    all_mode = False                     # trace all of the user's code
    watched = set()                      # code objects registered by @DP.watch
    manual = 0                           # open `with DP.watch():` blocks
    errors = 0


_out_file = None


def _out():
    global _out_file
    if _Cfg.file:
        if _out_file is None:
            _out_file = open(_Cfg.file, "a", buffering=1)
        return _out_file
    return sys.stdout


def _emit(text, depth=0, frame=None, line=None):
    where = ""
    if _Cfg.where and frame is not None:
        ln = line or frame.f_lineno
        where = f"{os.path.basename(frame.f_code.co_filename)}{':' + str(ln) if ln else ''}  "
    with _lock:
        _builtin_print(f"{_PREFIX}{where}{'  ' * min(depth, 20)}{text}", file=_out(), flush=True)


# ── formatting: values, down to the leaves ───────────────────────────────────
_SCALARS = (type(None), bool, int, float, complex)


def _short(s, n=None):
    n = _Cfg.strlen if n is None else n
    return s if len(s) <= n else s[:n] + f"…(+{len(s) - n})"


def _is_arraylike(v):
    return hasattr(v, "shape") and hasattr(v, "dtype") and hasattr(v, "tolist")


def _fields(v):
    """instance fields as {name: value}, or None when the object should be shown by repr"""
    if isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType, types.MethodType, type)):
        return None
    t = type(v)
    custom_repr = t.__repr__ is not object.__repr__
    dataclass = hasattr(t, "__dataclass_fields__")
    if custom_repr and not dataclass:
        return None
    out = {}
    try:
        out.update(vars(v))
    except TypeError:
        pass
    for klass in t.__mro__:
        for slot in getattr(klass, "__slots__", ()) or ():
            if isinstance(slot, str) and hasattr(v, slot):
                out[slot] = getattr(v, slot)
    return out if (out or not custom_repr) else None


def _typename(v):
    t = v if isinstance(v, type) else type(v)
    return t.__qualname__


def _fmt(v, d, n, seen):
    if isinstance(v, _SCALARS):
        return repr(v)
    if isinstance(v, str):
        return repr(_short(v))
    if isinstance(v, (bytes, bytearray)):
        return _short(repr(v))
    if isinstance(v, types.ModuleType):
        return f"<module {'DPrint' if getattr(v, '__file__', None) == __file__ else v.__name__}>"
    if isinstance(v, (types.FunctionType, types.BuiltinFunctionType, types.MethodType)):
        return f"<function {getattr(v, '__qualname__', getattr(v, '__name__', '?'))}>"
    if isinstance(v, type):
        return f"<class {v.__module__}.{v.__qualname__}>"
    if _is_arraylike(v):
        try:
            head = v.ravel()[:5].tolist() if hasattr(v, "ravel") else []
            return f"{_typename(v)}(shape={tuple(v.shape)}, dtype={v.dtype}, head={head})"
        except Exception:
            return f"<{_typename(v)}>"
    if id(v) in seen:
        return f"<cycle {_typename(v)}>"
    if isinstance(v, (list, tuple, set, frozenset, dict)):
        if d <= 0:
            return f"<{_typename(v)} len={len(v)}>"
        seen = seen | {id(v)}
        if isinstance(v, dict):
            body = [f"{_fmt(k, d - 1, n, seen)}: {_fmt(x, d - 1, n, seen)}" for k, x in list(v.items())[:n]]
            br = "{}"
        else:
            body = [_fmt(x, d - 1, n, seen) for x in list(v)[:n]]
            br = {list: "[]", tuple: "()"}.get(type(v), "{}")
        if len(v) > n:
            body.append(f"…+{len(v) - n}")
        if type(v) not in (list, tuple, dict, set):
            return f"{_typename(v)}{br[0]}{', '.join(body)}{br[1]}"
        if isinstance(v, tuple) and len(v) == 1:
            return f"({body[0]},)"
        return br[0] + ", ".join(body) + br[1]
    f = _fields(v)
    if f is None:
        return _short(repr(v))
    if d <= 0:
        return f"<{_typename(v)}>"
    seen = seen | {id(v)}
    items = list(f.items())[:n]
    body = [f"{k}={_fmt(x, d - 1, n, seen)}" for k, x in items]
    if len(f) > n:
        body.append(f"…+{len(f) - n}")
    return f"{_typename(v)}({', '.join(body)})"


def fmt(value, depth=None, items=None):
    """Format a value the way the feed does, all the way down.

    :param value: any object.
    :param depth: levels of containers/objects to descend (default ``DPRINT_DEPTH``).
    :param items: items shown per container (default ``DPRINT_ITEMS``).
    :returns: the text.
    :rtype: str
    """
    return _fmt(value, _Cfg.depth if depth is None else depth, _Cfg.items if items is None else items, frozenset())


# ── lineage: parentage of an object ─────────────────────────────────────────
_OWNER_ATTRS = ("parentItem", "parentWidget", "parent", "parentObject")


def _describe(o):
    name = _typename(o)
    try:
        on = o.objectName() if callable(getattr(o, "objectName", None)) else ""
        if on:
            name += f"[{on}]"
    except Exception:
        pass
    return name


def _owner_chain(obj):
    chain, seen, cur = [], {id(obj)}, obj
    for _ in range(30):
        nxt = None
        for a in _OWNER_ATTRS:
            try:
                attr = getattr(cur, a, None)
                cand = attr() if callable(attr) else attr
            except Exception:
                cand = None
            if cand is not None and id(cand) not in seen and not isinstance(cand, (str, int, float, bool)):
                nxt = cand
                break
        if nxt is None:
            break
        chain.append(_describe(nxt))
        seen.add(id(nxt))
        cur = nxt
    return chain


def lineage(obj):
    """Parentage of an object: its class lineage, and the chain of owners above it.

    The class lineage is the method resolution order (``Child < Base < object``). The owner chain follows
    ``parentItem()``, ``parentWidget()``, ``parent()`` or a plain ``.parent`` attribute upward.

    :param obj: an object or a class.
    :returns: ``"A < B < object"`` and, when it has owners, ``"  owners: X -> Y"``.
    :rtype: str
    """
    t = obj if isinstance(obj, type) else type(obj)
    text = " < ".join(c.__qualname__ if c.__module__ in ("builtins", "__main__") else f"{c.__module__}.{c.__qualname__}"
                      for c in t.__mro__)
    if not isinstance(obj, type):
        owners = _owner_chain(obj)
        if owners:
            text += "   owners: " + " -> ".join(owners)
    return text


# ── shadows: a comparable image of a value, and the diff of two images ──────
def _shadow(v, d, n, seen):
    if isinstance(v, _SCALARS) or isinstance(v, (str, bytes, bytearray)):
        return ("=", repr(v)[: _Cfg.strlen + 1])
    if isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType, types.MethodType, type)):
        return ("=", _fmt(v, 0, n, seen))
    if _is_arraylike(v):
        try:
            size = int(v.size)
            digest = hash(v.tobytes()) if size <= 1_000_000 else id(v)
            return ("A", tuple(v.shape), str(v.dtype), digest)
        except Exception:
            return ("=", f"<{_typename(v)}>")
    if id(v) in seen:
        return ("C",)
    seen = seen | {id(v)}
    if isinstance(v, (list, tuple, set, frozenset, dict)):
        if len(v) > n or d <= 0:
            return ("B", _typename(v), len(v))
        if isinstance(v, dict):
            return ("D", {repr(k): _shadow(x, d - 1, n, seen) for k, x in v.items()})
        if isinstance(v, (set, frozenset)):
            return ("S", frozenset(repr(x) for x in v))
        return ("L", [_shadow(x, d - 1, n, seen) for x in v])
    f = _fields(v)
    if f is None:
        return ("=", _short(repr(v), 200))
    if len(f) > n or d <= 0:
        return ("B", _typename(v), len(f))
    return ("O", _typename(v), {k: _shadow(x, d - 1, n, seen) for k, x in f.items()})


def _diff(old, new, value, path, out, budget):
    """append (path, text) for every leaf where two shadows differ; ``value`` is the current object at ``path``"""
    if old == new:
        return
    if budget[0] <= 0:
        return
    kind = new[0]
    if old[0] == kind == "D" and isinstance(value, dict):
        keys = {repr(k): k for k in value}
        for r, sh in new[1].items():
            if r not in old[1]:
                budget[0] -= 1
                out.append((f"{path}[{r}]", fmt(value[keys[r]])))
            else:
                _diff(old[1][r], sh, value[keys[r]], f"{path}[{r}]", out, budget)
        for r in old[1]:
            if r not in new[1]:
                budget[0] -= 1
                out.append((f"{path}[{r}]", "<removed>"))
        return
    if old[0] == kind == "L" and len(old[1]) == len(new[1]):
        for i, (a, b) in enumerate(zip(old[1], new[1])):
            _diff(a, b, value[i], f"{path}[{i}]", out, budget)
        return
    if old[0] == kind == "O" and old[1] == new[1]:
        f = _fields(value) or {}
        for k, sh in new[2].items():
            if k not in old[2]:
                budget[0] -= 1
                out.append((f"{path}.{k}", fmt(f[k])))
            else:
                _diff(old[2][k], sh, f[k], f"{path}.{k}", out, budget)
        for k in old[2]:
            if k not in new[2]:
                budget[0] -= 1
                out.append((f"{path}.{k}", "<removed>"))
        return
    if old[0] == kind == "B":
        budget[0] -= 1
        out.append((path, f"{new[1]} len {old[2]} -> {new[2]}" if old[2] != new[2] else f"{new[1]} (large; len {new[2]})"))
        return
    budget[0] -= 1
    out.append((path, fmt(value)))


# ── which code is traced ─────────────────────────────────────────────────────
_stdlib_dirs = tuple(
    os.path.normcase(os.path.realpath(p)) for p in
    {sysconfig.get_paths().get(k, "") for k in ("stdlib", "platstdlib", "purelib", "platlib")} if p)
_user_cache = {}
_static_cache = {}


def _is_user_code(filename):
    r = _user_cache.get(filename)
    if r is None:
        if not filename or filename.startswith("<") or filename == __file__:
            r = False
        else:
            real = os.path.normcase(os.path.realpath(filename))
            r = not (real.startswith(_stdlib_dirs) or "site-packages" in real or "dist-packages" in real)
        _user_cache[filename] = r
    return r


def _qualname(code, frame):
    return f"{frame.f_globals.get('__name__', '?')}.{getattr(code, 'co_qualname', code.co_name)}"


def _static_match(frame):
    """scope decision that depends only on the code object"""
    code = frame.f_code
    r = _static_cache.get(code)
    if r is None:
        if not _is_user_code(code.co_filename):
            r = False
        elif _Cfg.all_mode or code in _Cfg.watched:
            r = True
        elif _Cfg.scope:
            q, base = _qualname(code, frame), os.path.basename(code.co_filename)
            r = any(fnmatch.fnmatch(q, p) or fnmatch.fnmatch(q.split(".", 1)[-1], p) or fnmatch.fnmatch(base, p)
                    for p in _Cfg.scope)
        else:
            r = False
        _static_cache[code] = r
    return r


def _in_scope(frame):
    code = frame.f_code
    if code.co_filename == __file__:
        return False, False
    if _static_match(frame):
        return True, True
    if (_Cfg.manual or getattr(_tl, "active", 0)) and _Cfg.deep and _is_user_code(code.co_filename):
        return True, False
    return False, False


# ── the per-frame feed ───────────────────────────────────────────────────────
_recent = {}
_created = set()
_gens = {}


def _skip_name(name):
    return name.startswith("__") or name == ".0" or name.startswith("_dp_")


class _Frame:
    """local trace function for one frame: diffs the frame's variables each line"""

    def __init__(self, frame, origin, block=False):
        self.shadows = {}
        self.prev = None
        self.origin = origin
        self.depth = getattr(_tl, "depth", 0)
        _tl.depth = self.depth + 1
        if origin:
            _tl.active = getattr(_tl, "active", 0) + 1
        self.closed = False
        self.gen = bool(frame.f_code.co_flags & 0x1A0)           # generator / coroutine / async generator
        code = frame.f_code
        self.kind = "block" if block else "module" if code.co_name == "<module>" else (
            "class" if "__module__" in code.co_names and "__qualname__" in code.co_names else "function")
        self.label = {"module": f"module {frame.f_globals.get('__name__')}", "block": "watch block",
                      "class": f"class {code.co_name}"}.get(self.kind, getattr(code, "co_qualname", code.co_name))
        if block:                                   # a `with` block starts from what already exists: baseline, no print
            self.shadows = {k: _shadow(v, _Cfg.depth, _Cfg.items, frozenset()) for k, v in frame.f_locals.items()
                            if not _skip_name(k)}
        if self.kind != "function":
            _emit(f"=> {self.label}", self.depth, frame)
        else:
            head = f"-> {self.label}"
            if code.co_name == "__init__" and code.co_varnames:
                me = frame.f_locals.get(code.co_varnames[0])
                if me is not None and id(me) not in _created:
                    if len(_created) > 20000:
                        _created.clear()
                    _created.add(id(me))
                    caller = frame.f_back
                    site = f"{os.path.basename(caller.f_code.co_filename)}:{caller.f_lineno} in {getattr(caller.f_code, 'co_qualname', caller.f_code.co_name)}" if caller else "?"
                    head = f"-> new {_typename(me)}   lineage: {lineage(me)}   created at {site}"
            _emit(head, self.depth, frame)

    def step(self, frame):
        loc = frame.f_locals
        line = self.prev
        for name in list(loc):
            if _skip_name(name):
                continue
            v = loc[name]
            sh = _shadow(v, _Cfg.depth, _Cfg.items, frozenset())
            old = self.shadows.get(name, _MISSING)
            if old is _MISSING:
                _emit(f"{name} = {fmt(v)}", self.depth + 1, frame, line)
            elif old != sh:
                changes = []
                _diff(old, sh, v, name, changes, [20])
                for path, text in changes:
                    key = (id(v), path) if not isinstance(v, (*_SCALARS, str, bytes)) else None
                    line_text = f"{path} = {text}"
                    if key is not None:
                        if _recent.get(key) == line_text:
                            continue
                        if len(_recent) > 20000:
                            _recent.clear()
                        _recent[key] = line_text
                    _emit(line_text, self.depth + 1, frame, line)
            self.shadows[name] = sh
        for gone in [k for k in self.shadows if k not in loc]:
            _emit(f"del {gone}", self.depth + 1, frame, line)
            del self.shadows[gone]

    def resume(self, origin):
        """a generator frame runs again: same state, new place in the call stack, no header"""
        self.depth = getattr(_tl, "depth", 0)
        _tl.depth = self.depth + 1
        self.origin = origin
        if origin:
            _tl.active = getattr(_tl, "active", 0) + 1

    def close(self, frame, text):
        if self.closed:
            return
        self.closed = not self.gen
        _tl.depth = max(self.depth, 0)
        if self.origin:
            _tl.active = max(getattr(_tl, "active", 1) - 1, 0)
        _emit(text, self.depth, frame, self.prev)

    def __call__(self, frame, event, arg):
        try:
            if event == "line":
                self.step(frame)
                self.prev = frame.f_lineno
            elif event == "return":
                self.step(frame)
                if self.kind != "function":
                    self.close(frame, f"<= {self.label}")
                elif self.gen:
                    self.close(frame, f"<= {self.label} yields/returns {fmt(arg)}")
                elif frame.f_code.co_name == "__init__" and arg is None:
                    self.close(frame, f"<= {self.label}")
                else:
                    self.close(frame, f"<= {self.label} returns {fmt(arg)}")
            elif event == "exception":
                self.step(frame)
                exc, val, _tb = arg
                _emit(f"! {exc.__name__}: {_short(str(val), 200)}", self.depth + 1, frame)
        except Exception as e:                                 # the feed must never break the program
            _Cfg.errors += 1
            if _Cfg.errors <= 3:
                _builtin_print(f"{_PREFIX}DPrint internal error: {type(e).__name__}: {e}", file=sys.stderr)
            if _Cfg.errors >= 3:
                off()
        return self


def _global_trace(frame, event, arg):
    if event != "call" or not _Cfg.on:
        return None
    try:
        ok, origin = _in_scope(frame)
        if not ok:
            return None
        if frame.f_code.co_flags & 0x1A0:
            st = _gens.get(id(frame))
            if st is not None:
                st.resume(origin)
                return st
            if len(_gens) > 5000:
                _gens.clear()
            st = _gens[id(frame)] = _Frame(frame, origin)
            return st
        return _Frame(frame, origin)
    except Exception:
        return None


def _tracer_needed():
    return _Cfg.on and (_Cfg.all_mode or _Cfg.watched or _Cfg.scope or _Cfg.manual)


def _install():
    if _tracer_needed() and sys.gettrace() is not _global_trace:
        sys.settrace(_global_trace)
        threading.settrace(_global_trace)


def _uninstall():
    if sys.gettrace() is _global_trace:
        sys.settrace(None)
    threading.settrace(None)


# ── the public switches ──────────────────────────────────────────────────────
def on(scope=None):
    """Turn the global flag on.

    :param scope: ``None`` keeps what is registered (all of your code if nothing is); ``"*"`` forces all of
        your code; a string or list of fnmatch patterns on ``module.qualname`` narrows the feed.
    :returns: None
    """
    _Cfg.on = True
    if scope == "*":
        _Cfg.all_mode = True
    elif scope:
        _Cfg.scope = [scope] if isinstance(scope, str) else list(scope)
    if not (_Cfg.scope or _Cfg.watched or _Cfg.manual):
        _Cfg.all_mode = True
    _static_cache.clear()
    _install()


def off():
    """Turn the global flag off and remove the tracer.

    :returns: None
    """
    _Cfg.on = False
    _static_cache.clear()
    _uninstall()


def unwatch():
    """Forget every registered scope (decorated code, patterns, all-mode) and remove the tracer.

    :returns: None
    """
    _Cfg.watched.clear()
    _Cfg.scope = []
    _Cfg.all_mode = False
    _static_cache.clear()
    if not _Cfg.manual:
        _uninstall()


class _Scope:
    """context manager and decorator factory returned by ``DP.watch(...)``"""

    def __init__(self, patterns=None):
        self.patterns = patterns
        self.frame = None

    def __call__(self, target):                               # @DP.watch(...)
        return _register(target)

    def __enter__(self):
        if not _Cfg.on:
            return self
        _Cfg.manual += 1
        self.frame = sys._getframe(1)
        if self.patterns:
            _Cfg.scope += [p for p in self.patterns if p not in _Cfg.scope]
            _static_cache.clear()
        _install()
        self.frame.f_trace = _Frame(self.frame, True, block=True)
        self.frame.f_trace_lines = True
        return self

    def __exit__(self, *exc):
        if self.frame is not None:
            tr = self.frame.f_trace
            if isinstance(tr, _Frame):
                tr.step(self.frame)
                tr.close(self.frame, f"<= {tr.label}")
            self.frame.f_trace = None
            self.frame = None
            _Cfg.manual = max(_Cfg.manual - 1, 0)
            if not _tracer_needed():
                _uninstall()
        return False


def _register(target):
    if isinstance(target, type):
        for v in vars(target).values():
            fn = v.__func__ if isinstance(v, (staticmethod, classmethod)) else v
            if isinstance(fn, types.FunctionType):
                _Cfg.watched.add(fn.__code__)
    else:
        fn = getattr(target, "__func__", target)
        code = getattr(fn, "__code__", None)
        if code is None:
            return target
        _Cfg.watched.add(code)
    _static_cache.clear()
    _install()
    return target


def watch(target=None, *patterns):
    """Watch a scope: every assignment inside it prints as it happens.

    Forms::

        @DP.watch                  # a function or a class (every method)
        @DP.watch()                # same, with parentheses
        with DP.watch():           # the block, and what it calls
        DP.watch("Table.address", "energy")      # patterns on module.qualname, kept for the whole run

    With the flag off this does nothing and returns its target unchanged.

    :param target: a function, a class, a pattern string, or None.
    :param patterns: further patterns when ``target`` is a string.
    :returns: the target itself (decorator forms), or a context manager.
    """
    if target is None:
        return _Scope()
    if isinstance(target, str):
        pats = [target, *patterns]
        if _Cfg.on:
            _Cfg.scope += [p for p in pats if p not in _Cfg.scope]
            _static_cache.clear()
            _install()
        return _Scope(pats)
    return _register(target)


# ── DP.print: the checkpoint ─────────────────────────────────────────────────
def _call_node(frame):
    """the ast node of the expression that is calling us, read from the caller's own source"""
    code = frame.f_code
    try:
        if hasattr(code, "co_positions"):
            pos = list(code.co_positions())[frame.f_lasti // 2]
            l1, l2, c1, c2 = pos
            if l1 is not None and c1 is not None:
                lines = linecache.getlines(code.co_filename)
                chunk = lines[l1 - 1:l2]
                if len(chunk) == 1:
                    seg = chunk[0].encode()[c1:c2].decode()
                else:
                    seg = chunk[0].encode()[c1:].decode() + "".join(chunk[1:-1]) + chunk[-1].encode()[:c2].decode()
                return ast.parse(seg.strip(), mode="eval").body
        text = linecache.getline(code.co_filename, frame.f_lineno).strip()
        tree = ast.parse(text.lstrip("@"), mode="eval")
        return tree.body
    except Exception:
        return None


def _show(label, value, frame):
    _emit(f"{label} = {fmt(value)}", 0, frame)
    f = _fields(value)
    if not isinstance(value, (*_SCALARS, str, bytes, list, tuple, dict, set, frozenset, type)) and (
            f is not None or type(value).__module__ not in ("builtins",)) and not isinstance(
            value, (types.ModuleType, types.FunctionType)):
        _emit(f"  lineage: {lineage(value)}", 0, frame)


def _dp_print(*args, **named):
    """Print values with their names, as ``name = value``.

    The name is read from the call's own source, so ``DP.print(total, grid[2])`` prints ``total = …`` and
    ``grid[2] = …``. A string literal first argument is a label for the rest (``DP.print("TABLE", rows)``);
    a lone string literal prints as a banner. With no arguments it dumps the calling scope (locals, and the
    fields and lineage of ``self``). Falsy values print as themselves. Used as ``@DP.print`` it watches the
    function (same as ``@DP.watch``). With the flag off it returns at once.

    :param args: values to print.
    :param named: ``label=value`` pairs, printed under the label.
    :returns: the value (one argument), a tuple (several), or None.
    """
    if not _Cfg.on:
        return args[0] if len(args) == 1 and not named else (args if args else None)
    frame = sys._getframe(1)
    node = _call_node(frame)
    if not isinstance(node, ast.Call):                         # bare @DP.print: decorator use
        if len(args) == 1 and callable(args[0]):
            return _register(args[0])
        node = None
    exprs = list(node.args) if node is not None and len(node.args) == len(args) else [None] * len(args)
    if not args and not named:
        for name, v in list(frame.f_locals.items()):
            if not _skip_name(name):
                _show(name, v, frame)
        return None
    if exprs and isinstance(exprs[0], ast.Constant) and isinstance(exprs[0].value, str):
        if len(args) == 1:
            _emit(args[0], 0, frame)
            return args[0]
        label = args[0]
        for i, v in enumerate(args[1:], 1):
            _show(label if len(args) == 2 else f"{label}[{i - 1}]", v, frame)
        return args[1] if len(args) == 2 else args[1:]
    for i, v in enumerate(args):
        label = ast.unparse(exprs[i]) if exprs[i] is not None else f"arg{i}"
        _show(label, v, frame)
    for k, v in named.items():
        _show(k, v, frame)
    if len(args) == 1 and not named:
        return args[0]
    return args if args else (list(named.values())[0] if len(named) == 1 else None)


# ── module surface: DP.flag, DP.print ───────────────────────────────────────
class _Module(types.ModuleType):
    @property
    def flag(self):
        """the global flag: 1 (on) or 0 (off); assignable (``DP.flag = 1``)"""
        return 1 if _Cfg.on else 0

    @flag.setter
    def flag(self, v):
        on() if v not in (0, False, "", "0", None) else off()


sys.modules[__name__].__class__ = _Module
print = _dp_print                                              # noqa: A001  (the point of the module: DP.print)


def main(argv=None):
    """Run a script under the feed: ``python -m DPrint [--scope PAT] script.py args...``

    :param argv: arguments after the module name (default ``sys.argv[1:]``).
    :returns: None
    """
    import runpy
    argv = list(sys.argv[1:] if argv is None else argv)
    scope = []
    while argv and argv[0] == "--scope":
        scope.append(argv[1])
        argv = argv[2:]
    if not argv:
        _builtin_print(__doc__)
        return
    sys.modules.setdefault("DPrint", sys.modules[__name__])   # a script that imports DPrint gets this instance
    on(scope or "*")
    sys.argv = argv
    sys.path.insert(0, os.path.dirname(os.path.abspath(argv[0])))
    try:
        runpy.run_path(argv[0], run_name="__main__")
    finally:
        off()


if _Cfg.on:                                                    # DPRINT=1 at import: watch everything from here on
    if not _Cfg.scope:
        _Cfg.all_mode = True
    _install()

if __name__ == "__main__":
    main()
