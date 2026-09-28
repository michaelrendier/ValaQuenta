"""Shared fixtures. The repository root IS the ``ValaQuenta`` package, so the
directory that contains it must be on sys.path (``pip install .`` does this for
an installed copy; running from a checkout needs the parent directory)."""
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARENT = str(ROOT.parent)
sys.path.insert(0, PARENT)      # test THIS checkout, never a stale installed copy
import ValaQuenta  # noqa: E402

assert pathlib.Path(ValaQuenta.__file__).resolve().parent == ROOT, (
    f"tests imported {ValaQuenta.__file__}, not the checkout at {ROOT}; "
    "the checkout directory must be named 'ValaQuenta'")


def fresh_registry():
    """Empty the process-global registry and register every module once."""
    import contextlib
    import io
    from ValaQuenta.engine.registry import get_registry
    from ValaQuenta.__main__ import _register_all
    reg = get_registry()
    reg._modules.clear()
    reg._formulary.clear()
    with contextlib.redirect_stdout(io.StringIO()):   # the registry prints one line per module
        return _register_all()


@pytest.fixture()
def registry():
    return fresh_registry()


@pytest.fixture(scope="session")
def root():
    return ROOT
