"""The README's code blocks are tests."""
import doctest
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_readme_session_runs_and_prints_what_it_says():
    text = (ROOT / "README.md").read_text()
    block = next(b for b in re.findall(r"```python\n(.*?)```", text, re.S) if ">>> " in b)
    from conftest import fresh_registry
    from ValaQuenta.engine.registry import get_registry
    reg = get_registry()
    reg._modules.clear()          # the README session starts from an empty registry
    reg._formulary.clear()
    parser = doctest.DocTestParser()
    test = parser.get_doctest(block, {}, "README", "README.md", 0)
    runner = doctest.DocTestRunner(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        runner.run(test)
    assert runner.failures == 0, f"{runner.failures} README example(s) failed"


def test_readme_links_resolve():
    text = (ROOT / "README.md").read_text()
    missing = []
    for m in re.finditer(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (ROOT / target).exists():
            missing.append(target)
    assert missing == []
