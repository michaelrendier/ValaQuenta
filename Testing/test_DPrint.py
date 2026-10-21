"""Test suite for ``DPrint`` (``ValaQuenta/PythonPath/DPrint.py``).

Each test runs a small program in a fresh interpreter with ``PYTHONPATH`` pointing at
``ValaQuenta/PythonPath`` only, so the module is exercised exactly as an outside user imports it.
Run from the scratchpad (the working directory does not matter)::

    python -m pytest /path/to/ValaQuenta/Testing/test_DPrint.py -p no:cacheprovider
"""
import os
import pathlib
import subprocess
import sys
import textwrap

DPATH = str(pathlib.Path(__file__).resolve().parent.parent / "PythonPath")


def run(code, tmp_path, env=None, args=()):
    """Run ``code`` as a script in a fresh interpreter and return its stdout lines.

    :param code: program text.
    :param tmp_path: directory for the script.
    :param env: extra environment variables (``DPRINT`` etc.).
    :param args: arguments placed before the script (for example ``("-m", "DPrint")``).
    :returns: stdout split into lines.
    :rtype: list
    """
    script = tmp_path / "prog.py"
    script.write_text(textwrap.dedent(code))
    e = {k: v for k, v in os.environ.items() if not k.startswith("DPRINT")}
    e["PYTHONPATH"] = DPATH
    e.update(env or {})
    cmd = [sys.executable, *args, str(script)] if not args else [sys.executable, *args, str(script)]
    r = subprocess.run(cmd, capture_output=True, text=True, env=e, cwd=tmp_path, timeout=120)
    assert r.returncode == 0, r.stderr
    return r.stdout.splitlines()


def test_flag_off_is_silent_and_inert(tmp_path):
    """With DPRINT unset: no output, no tracer installed, decorators return the function unchanged."""
    out = run("""
        import sys, DPrint as DP
        def f(a):
            b = a + 1
            return b
        g = DP.watch(f)
        DP.print(f(1))
        print("same", g is f, "tracer", sys.gettrace(), "flag", DP.flag)
    """, tmp_path)
    assert out == ["same True tracer None flag 0"]


def test_print_reads_names_and_keeps_falsy_values(tmp_path):
    """``DP.print`` labels each argument from the call's source; 0, '' and [] print as themselves."""
    out = run("""
        import DPrint as DP
        total = 0; text = ""; rows = []
        r = DP.print(total, text, rows)
        DP.print("BANNER")
        DP.print("rows", [1, [2, 3]])
        x = DP.print(3 + 4)
        assert x == 7 and r == (0, "", [])
    """, tmp_path, {"DPRINT": "1", "DPRINT_WHERE": "0", "DPRINT_SCOPE": "nothing.*"})
    assert out == ["[dp] total = 0", "[dp] text = ''", "[dp] rows = []", "[dp] BANNER",
                   "[dp] rows = [1, [2, 3]]", "[dp] 3 + 4 = 7"]


def test_watch_prints_every_assignment_down_to_the_leaves(tmp_path):
    """The feed prints arguments, loop variables, in-place container edits by path, and the return value."""
    out = run("""
        import DPrint as DP
        @DP.watch
        def work(n):
            grid = [[0, 0], [0, 0]]
            for i in range(n):
                grid[i][1] = i + 5
            d = {"k": {"v": 1}}
            d["k"]["v"] = 2
            return grid
        work(2)
    """, tmp_path, {"DPRINT": "1", "DPRINT_WHERE": "0", "DPRINT_SCOPE": "work"})
    for want in ["[dp] -> work", "[dp]   n = 2", "[dp]   i = 0", "[dp]   i = 1", "[dp]   grid[0][1] = 5",
                 "[dp]   grid[1][1] = 6", "[dp]   d['k']['v'] = 2", "[dp] <= work returns [[0, 5], [0, 6]]"]:
        assert want in out, (want, out)


def test_object_creation_shows_lineage_and_creation_site(tmp_path):
    """Creation prints the class lineage and where it was created; field assignments follow; super() is not 'new' twice."""
    out = run("""
        import DPrint as DP
        class Base:
            def __init__(self):
                self.parent = None
        class Leaf(Base):
            def __init__(self, parent):
                super().__init__()
                self.parent = parent
        def make():
            return Leaf(Base())
        DP.watch("prog.*")
        make()
    """, tmp_path, {"DPRINT": "1", "DPRINT_WHERE": "0"})
    text = "\n".join(out)
    assert "-> new Leaf   lineage: Leaf < Base < object   created at prog.py:" in text
    assert text.count("-> new Leaf") == 1
    assert "self.parent = Base(parent=None)" in text


def test_callee_mutation_is_not_printed_twice(tmp_path):
    """A change made in a callee to an object the caller also holds prints once."""
    out = run("""
        import DPrint as DP
        class Box:
            def __init__(self): self.v = 0
        def poke(b): b.v = 9
        @DP.watch
        def top():
            b = Box()
            poke(b)
            return b.v
        top()
    """, tmp_path, {"DPRINT": "1", "DPRINT_WHERE": "0", "DPRINT_SCOPE": "top"})
    assert sum(1 for l in out if l.endswith("b.v = 9")) == 1, out


def test_scope_pattern_excludes_other_code(tmp_path):
    """Only code matching DPRINT_SCOPE (and its callees) is watched."""
    out = run("""
        import DPrint as DP
        def a():
            x = 1
        def b():
            y = 2
        a(); b()
    """, tmp_path, {"DPRINT": "1", "DPRINT_WHERE": "0", "DPRINT_SCOPE": "a", "DPRINT_DEEP": "0"})
    assert "[dp] -> a" in out and not any("y = 2" in l or "-> b" in l for l in out)


def test_with_block_baseline_and_callees(tmp_path):
    """``with DP.watch():`` prints only what changes inside the block, plus the callees it runs."""
    out = run("""
        import DPrint as DP
        DP.flag = 1
        def g(x):
            return x + 1
        keep = 5
        with DP.watch():
            z = [1]
            z.append(2)
            w = g(3)
    """, tmp_path, {"DPRINT_WHERE": "0"})
    assert "[dp]   z = [1, 2]" in out and "[dp]   w = 4" in out and not any("keep" in l for l in out)


def test_runner_watches_module_load(tmp_path):
    """``python -m DPrint script.py`` prints module-level assignments from the first line."""
    out = run("""
        import DPrint
        ANSWER = 6 * 7
        class K:
            n = 1
    """, tmp_path, {"DPRINT_WHERE": "0"}, args=("-m", "DPrint"))
    assert "[dp]   ANSWER = 42" in out and "[dp]   => class K" in out and "[dp]   DPrint = <module DPrint>" in out


def test_lineage_and_owner_chain(tmp_path):
    """``DP.lineage`` gives the class lineage and follows ``.parent`` upward."""
    out = run("""
        import DPrint as DP
        class A: pass
        class B(A):
            def __init__(self, parent=None): self.parent = parent
        print(DP.lineage(B(B(A()))))
    """, tmp_path)
    assert out == ["B < A < object   owners: B -> A"]


def test_feed_never_breaks_the_program(tmp_path):
    """An object whose attribute access raises is shown by repr and the program still completes."""
    out = run("""
        import DPrint as DP
        class Bad:
            @property
            def boom(self): raise RuntimeError("x")
        @DP.watch
        def f():
            b = Bad()
            return 1
        print("done", f())
    """, tmp_path, {"DPRINT": "1", "DPRINT_WHERE": "0", "DPRINT_SCOPE": "f"})
    assert out[-1] == "done 1"
