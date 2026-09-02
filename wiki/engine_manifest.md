# Engine Manifest — `engine/manifest.py` + `modules/<name>/manifest.json`

**Status:** ESTABLISHED (infrastructure). Full Engine Protocol **part 2c**.

## What it is

An additional required class of engine data. Every ValaQuenta engine carries,
**with the module**, a `manifest.json` that declares three things the code
itself does not:

1. **provenance** — origin, authors, created date, status label, predecessor
   engines, bibliography keys, and the repo-relative paths to its Ainulindale
   wiki page, ValaQuenta wiki page, notebook, and proof_locale catalog.
2. **environment** — the named constants the engine consumes (`Ω_ZS`, `d*`,
   `σ_RB`, …) with value + source, the native space, the arithmetic
   contract, and any sibling engines / external packages it calls.
3. **ui** — the ValaQuenta-Tab / desktop-renderer plugin registration:
   menu label + group + order, the tool list (name → equation → params →
   one-line description), display modes, analysis lenses, whether guided /
   academic proofs are available, and the desktop window / surface / OpenGL
   hints.

This is the standard Python packaging pattern — metadata and entry points
shipped as data files inside the package — applied per engine.

## Why

The curses UI (**The ValaQuenta Tab**, `engine/console_curses.py`) used to
hard-code its menu groupings, tool lists and display options. It now builds
all of that **procedurally** from `manifest.menu_tree(registry)`. Adding or
changing an engine never means editing the UI again — the engine declares its
own menu contribution and the Tab (and, downstream, the PtolemyDesktop
renderer) assemble themselves.

## Files

| Path | Role |
|------|------|
| `engine/manifest.py` | schema, loader (`load`), `menu_tree(registry)`, `validate`, `scaffold` / `scaffold_all`, CLI |
| `modules/<name>/manifest.json` | the data, one per engine (schema id `valaquenta.engine-manifest/1`) |

`EquationModule.manifest()` returns the sidecar (or a live scaffold if it is
not written yet).

## Commands

```
python3 -m ValaQuenta.engine.manifest menu       # the procedural menu tree
python3 -m ValaQuenta.engine.manifest scaffold   # write missing manifest.json files
python3 -m ValaQuenta.engine.manifest validate   # gate every manifest
python3 -m ValaQuenta --manifests                # same validation, via the main entry
```

## Scaffolding vs. hand-fill

A missing manifest is **scaffolded live** from the registry (display name,
version, formulary → tools, `display_options` → display modes,
`confidence_floor` → status) plus path-convention discovery of the wiki /
notebook / proof_locale files — so the Tab is always complete. `scaffold_all`
writes those scaffolds to disk carrying a `_scaffolded: true` flag and blank
`provenance.origin`. Hand-refinement fills `origin` (and the other narrative
provenance fields) and drops the flag; `validate` then requires `origin` to be
non-empty.

As of 2026-09-01: 23/23 engines have a `manifest.json`. `emerger` is
hand-filled (the reference example); the other 22 are written scaffolds
awaiting provenance.

## The ValaQuenta Tab keys that read the manifest

| Key | Uses |
|-----|------|
| root listing | `menu.group` / `menu.order` — grouped, non-selectable headers |
| `i` | the manifest / provenance panel for the current engine |
| `a` | per-engine `analysis_lenses` (falls back to the global four) |
| `d` | per-engine `display_modes` (falls back to the global list) |
