"""The registry and the plugin manifests agree with the code."""
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"
LIBRARY_ONLY = {"spherical", "sigma_cavitation", "translator_common"}


def module_dirs():
    return sorted(d.name for d in MODULES.iterdir() if d.is_dir() and (d / "__init__.py").exists())


def test_every_tools_module_is_registered(registry):
    with_tools = {n for n in module_dirs() if (MODULES / n / "tools.py").exists()}
    assert with_tools == set(registry.list_modules())


def test_library_modules_are_exactly_the_maths_only_ones():
    without_tools = {n for n in module_dirs() if not (MODULES / n / "tools.py").exists()}
    assert without_tools == LIBRARY_ONLY


def test_every_registered_module_has_a_manifest_and_gpl(registry):
    for name in registry.list_modules():
        man = json.loads((MODULES / name / "manifest.json").read_text())
        assert man["license"] == "GPL-3.0-only", name
        assert man["name"] == name


def test_manifests_validate(registry):
    from ValaQuenta.engine import manifest
    problems = []
    for name in registry.list_modules():
        problems += manifest.validate(name, registry.get_module(name))
    assert problems == []


def test_plugin_format_validates():
    from ValaQuenta.engine import format as vqformat
    bad = {}
    for info in vqformat.discover():
        probs = vqformat.validate(info.manifest, name=info.name)
        if probs:
            bad[info.id] = probs
    assert bad == {}


def test_formularies_are_well_formed(registry):
    from ValaQuenta.engine.registry import CONFIDENCE
    for name in registry.list_modules():
        mod = registry.get_module(name)
        eqs = mod.formulary()
        assert eqs, name
        names = [e.name for e in eqs]
        assert len(names) == len(set(names)), f"{name}: duplicate equation names"
        for e in eqs:
            # COMPUTATIONAL is the one label outside the four tiers: a scan run in code
            # (clay_millennium.rh_noether_balance_scan); see wiki/clay_millennium.md.
            assert e.confidence in CONFIDENCE or e.confidence == "COMPUTATIONAL", (name, e.name, e.confidence)


def test_parameterless_equations_run(registry):
    """Every equation that needs no arguments must run through the registry without raising."""
    failures = []
    for name in registry.list_modules():
        for e in registry.get_module(name).formulary():
            if e.params:
                continue
            try:
                out = registry.run(f"{name}.{e.name}", {})
                assert "result" in out or out
            except Exception as exc:   # noqa: BLE001
                failures.append(f"{name}.{e.name}: {type(exc).__name__}: {exc}")
    assert failures == []


def test_registry_run_contract(registry):
    out = registry.run("noether.conservation_diagnostic",
                       {"psi_norms": [0.5, 0.5, 0.7], "g": 1.0, "algebra": 2})
    assert set(out) >= {"equation", "params", "result", "module"}
    assert out["result"]["status"] == "PASS"
