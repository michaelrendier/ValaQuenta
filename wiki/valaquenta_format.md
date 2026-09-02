# The ValaQuenta Format — `valaquenta.plugin/1`

**Status:** ESTABLISHED (infrastructure). Spec: [`../FORMAT.md`](../FORMAT.md).

## What it is

The plugin / extension contract for PtolemyDesktop — the WebExtension analogue.
A plugin is a directory with a `manifest.json` (schema `valaquenta.plugin/1`), a
typed entry point, a permission list the host gates, and a discovery path.
PtolemyDesktop / PTorrent are the GNU framework; ValaQuenta is Cody's plugin
layer on it, and anyone can wire their own the same way.

## Why now

We had a full set of plugins — 23 engines, the `manifest.json` system,
`proof_locale` catalogs, the four faces, analysis lenses — but no formal
contract for a *third party* to add one. The Format is that contract.

## Files

| path | role |
|---|---|
| `FORMAT.md` | the normative spec (§1 layout · §2 manifest · §3 types · §4 host API · §5 discovery · §6 migration · §7 licensing) |
| `schema/valaquenta-plugin-1.schema.json` | machine schema (JSON Schema 2020-12) |
| `engine/format.py` | `validate` · `discover` · `load` · `normalise` · `upgrade`; CLI |
| `modules/<name>/manifest.json` | 23 reference `type: engine` plugins (upgraded in place to `valaquenta.plugin/1`) |
| `examples/hello_lens/` | reference `type: lens` plugin, outside `modules/` |

## Plugin types

| type | entry contract |
|---|---|
| `engine` | `EquationModule` subclass (`engine/registry.py`) |
| `face` | chat-room identity — `name`/`role`/`probe`/`opinion`/`act` (`PtolemyDesktop/ptolemy_console.py` `Face`) |
| `lens` | `analyse(target) -> dict` |
| `tab` | `run_tab(scr)` + `act(query) -> str` |

## Permissions

Absent ⇒ read-only `registry.read` + `proof.render` + `manifest.read`.
Declared: `registry.run`, `codegate.propose`, `net.search`, `net.browse`,
`fs.read:<scope>`. The host (Ptolemy) grants.

## Licensing

`license` is load-bearing: `GPL-3.0-only` / permissive ⇒ ships with the GNU
framework and can go out on its own; anything else (e.g.
`LicenseRef-ValaQuenta-Private`) ⇒ stays behind ValaQuenta.

## Commands

```
python3 -m ValaQuenta.engine.format schema      # the JSON Schema
python3 -m ValaQuenta.engine.format discover    # every plugin found, by type
python3 -m ValaQuenta.engine.format validate    # gate every plugin
python3 -m ValaQuenta.engine.format load <id>   # resolve one
python3 -m ValaQuenta.engine.format upgrade --write   # canonicalise the built-ins
python3 -m ValaQuenta --manifests               # engine-side validation (delegates here)
```

As of 2026-09-01: 23 engines + `hello_lens` validate clean; the built-in engine
manifests are `valaquenta.plugin/1` in canonical order.

Related: [`engine_manifest.md`](engine_manifest.md) (the engine case, Full
Engine Protocol part 2c).
