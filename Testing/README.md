# ValaQuenta/Testing

**Test suites for work done in ValaQuenta, and only that.** Tests are kept out of the engine code: a module's `maths.py` / `tools.py` carry the live `dprint` stream and nothing else. This directory holds the suites that check them.

> **Scope.** Documented as API code reference, like the rest of ValaQuenta: file, class or function, parameters, return values, what the run prints, and a confidence table. No narrative. Results and the record go to the wiki.

## Rules

1. Only ValaQuenta work lives here. Tests for other repositories live in those repositories.
2. New code is tested here, not inline. Existing modules that carry their own checks (`verify()`, `self_check`, `tests/`) are left as they are; nothing is retro-fitted.
3. Each suite is one file, `test_<module>.py`, importing the module under test by its public name.
4. Docstrings are Sphinx reST field lists (`:param`, `:returns:`, `:raises:`), imperative, no history.
5. Suites are run from the scratchpad, which is mirrored in ContextPlease. A run's output, not the suite, is what goes to the scratchpad.
6. A failing result is data: it is recorded with the input that produced it and is not repaired in the same pass.

## Layout

```
Testing/
  README.md             this file: the index
  test_<module>.py      one suite per module under test
  fixtures/             inputs a suite needs, named for the suite that reads them
```

## Entry format (one per suite, in this README's table)

| field | content |
|---|---|
| suite | `test_<module>.py` |
| module under test | import path |
| checks | each assertion, one line |
| run | the exact command, from the scratchpad |
| prints | what the run prints on success |
| confidence | `:CALCULATED`, `OURS`, or `ESTABLISHED` per the repository's labels |

## Suites

| field | `test_DPrint.py` |
|---|---|
| module under test | `DPrint` (`ValaQuenta/PythonPath/DPrint.py`), imported through `PYTHONPATH` in a fresh interpreter per test |
| checks | flag off is silent and installs no tracer; `DP.print` reads names and keeps falsy values; `@DP.watch` prints arguments, loop variables, in-place edits by path and the return; creation prints lineage and creation site (once under `super()`); a callee's change prints once; scope patterns exclude other code; `with DP.watch():` baselines and follows callees; `python -m DPrint` watches module load; `DP.lineage` owner chain; a failing attribute never breaks the program |
| run | `cd <scratchpad> && python -m pytest ValaQuenta/Testing/test_DPrint.py -p no:cacheprovider -q` |
| prints | `10 passed` |
| confidence | `:CALCULATED` (the behaviour is exercised end to end) |
