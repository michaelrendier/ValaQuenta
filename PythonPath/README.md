# ValaQuenta/PythonPath

Standalone, stdlib-only, single-file tools meant to be imported from **any** program, not only from ValaQuenta. Put this directory on `PYTHONPATH`; nothing here imports ValaQuenta or depends on a project path.

```bash
export PYTHONPATH="$PYTHONPATH:/home/rendier/Projects/ThePlace/ValaQuenta/PythonPath"
```

| file | what |
|---|---|
| `DPrint.py` | the dPrint() protocol: a global flag and a live stream of data changes |

## DPrint

```python
import DPrint as DP

DP.print(total, grid[2])         # checkpoint: prints  total = 0   grid[2] = [...]   (names read from the call)
DP.print("TABLE", rows)          # label form;  DP.print("BANNER") prints a banner;  DP.print() dumps the scope
@DP.watch                         # every assignment inside prints as it happens
def work(n): ...
with DP.watch():                  # the same for a block and what it calls
    ...
```

| switch | effect |
|---|---|
| `DPRINT=1` / `0` (environment), or `DP.flag = 1` | global flag; off by default; off means no tracer and no output |
| `DPRINT=1` alone | the feed covers all of your code (not stdlib, not site-packages) from import time |
| `DPRINT_SCOPE="Table.address,energy,mymod.*"` | only code matching these `module.qualname` / file patterns, plus its callees |
| `python -m DPrint [--scope PAT] script.py args` | run a script under the feed, module load included |
| `DPRINT_WHERE=0`, `DPRINT_FILE=path`, `DPRINT_DEPTH=8`, `DPRINT_ITEMS=200`, `DPRINT_STR=500`, `DPRINT_DEEP=1` | location column, output file, descent depth, items per container, string length, watch callees |

Output: `[dp] file.py:LINE  name = value`. A call prints `-> name`, its arguments, and `<= name returns value`. Object creation prints `-> new Leaf   lineage: Leaf < Base < object   created at file.py:LINE in caller`; `DP.print(obj)` adds the owner chain (`parent()`, `parentWidget()`, `parentItem()` or `.parent`). A change inside a container prints by path (`grid[2][3] = 7`, `self.count = 4`). A change a callee makes to an object the caller holds prints once.

Limits: Python assignments only; a change is attributed to the line that just ran; containers larger than `DPRINT_ITEMS` are tracked by length; tracing slows Python roughly tenfold, so narrow the scope when volume matters; `sys.settrace` replaces a debugger or coverage tracer while the flag is on; the already-running `__main__` frame cannot be watched from inside (use `python -m DPrint`).

Tests: `ValaQuenta/Testing/test_DPrint.py`.
