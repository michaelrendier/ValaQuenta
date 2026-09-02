# The ValaQuenta Format

**`valaquenta.plugin/1`** — the plugin / extension contract for PtolemyDesktop.

A ValaQuenta plugin is to PtolemyDesktop what a WebExtension is to Firefox: a
directory with a **`manifest.json`**, a **typed entry point**, a **permission
list** the host gates, and a **discovery path**. PtolemyDesktop / PTorrent are
the GNU framework; ValaQuenta is one plugin layer on it (Cody's), and anyone
can wire their own the same way.

- Spec (this file): the normative description.
- Machine schema: [`schema/valaquenta-plugin-1.schema.json`](schema/valaquenta-plugin-1.schema.json).
- Reference implementation: [`engine/format.py`](engine/format.py) — `validate`,
  `discover`, `load`, `normalise`, `upgrade`; CLI
  `python3 -m ValaQuenta.engine.format {schema|validate|discover|load|upgrade}`.
- Reference plugins: every `modules/<name>/` (type `engine`) and
  [`examples/hello_lens/`](examples/hello_lens/) (type `lens`).

---

## 1. Package layout

    my_plugin/
      manifest.json        (required)
      plugin.py            entry module — or maths.py + tools.py for an engine
      proof_locale.json    optional — engines: the guided/academic proof catalog
      notebook.ipynb       optional — exercises the plugin end to end
      wiki.md              optional — the narrative page
      assets/              optional — images, .menu files, data

A distributable bundle is a **`.vqx`** — a zip of that directory, the `.xpi`
analogue. (A `.vqx` registry is anticipated, not built.)

Built-in ValaQuenta engines keep their historical layout —
`modules/<name>/{__init__,maths,tools}.py` + `manifest.json`, catalog in
`engine/proof_locale/<name>.json` — which is a conforming `engine` plugin.

---

## 2. The manifest

`manifest.json`, schema id `valaquenta.plugin/1`. Superset of the earlier
`valaquenta.engine-manifest/1` — the older per-engine files are read as
`format_version: 1` engines with `id` / `type` / `entry` / `license` back-filled
by `format.normalise()`; `format.upgrade(write=True)` writes them out in
canonical order.

### 2.1 Required keys

| key | type | notes |
|---|---|---|
| `schema` | const `"valaquenta.plugin/1"` | |
| `format_version` | const `1` | |
| `id` | string, reverse-DNS | `org.ainulindale.emerger`, `com.example.hello_lens`. Unique; the discovery key. |
| `type` | `engine` \| `face` \| `lens` \| `tab` | see §3 |
| `name` | string | short machine name |
| `version` | string | `0.1`, `1.2.3`, `2.0-rc1` |
| `entry` | `{ "module": <import path>, "class": <attr> }` | the Python object implementing the type contract |
| `license` | SPDX string | `GPL-3.0-only` (or permissive) ⇒ GNU-shippable; anything else ⇒ private (e.g. `LicenseRef-ValaQuenta-Private`) |
| `provenance` | object | §2.4 |

### 2.2 Optional keys

| key | type | notes |
|---|---|---|
| `display` | string | long name; defaults to `name` |
| `summary` | string | one line for menus |
| `confidence_floor` | `ESTABLISHED` \| `THEORETICAL` \| `CONJECTURE` \| `OPEN` | |
| `permissions` | string[] | §2.3; absent ⇒ read-only registry + proof + manifest |
| `dependencies` | `{ <plugin-id>: <version-range> }` | `">=0.1"`, `"1.x"`, `"*"` |
| `environment` | object | named constants the plugin consumes, native space, `requires_engines`, `external` |
| `ui` | object | `menu` (label/group/order/blurb), `tools[]`, `display_modes[]`, `analysis_lenses[]`, `proof{guided,academic}`, `desktop{window,surface,opengl,pgui_widgets}` — consumed by the ValaQuenta Tab and the desktop renderer |

### 2.3 Permissions

Declared like WebExtension `permissions`. The host (Ptolemy) grants or prompts.

| permission | grants |
|---|---|
| `registry.read` | list / get engines and equations |
| `registry.run` | execute an equation |
| `proof.render` | `render_guided` / `render_academic` |
| `manifest.read` | `manifest.load` / `menu_tree` |
| `codegate.propose` | queue a code-write proposal (still Ptolemy-approved) |
| `net.search` | web search via the harness |
| `net.browse` | fetch a URL via the harness |
| `fs.read:<scope>` | read files under `<scope>` (a repo-relative path) |

**Default** (no `permissions` key): `registry.read` + `proof.render` +
`manifest.read` only. Everything else is denied until declared.

### 2.4 Provenance

Required object. Keys: `origin` (where the idea entered — process, not
narrative), `authors[]`, `created` (ISO date), `status_label` (e.g.
`THEORETICAL:CALCULATED`), `predecessors[]` (sibling plugin names/ids),
`citations[]` (bibliography keys), `wiki` (`{ainulindale, valaquenta}` —
repo-relative paths), `notebook`, `proof_locale`. A non-scaffold plugin must
fill `origin`.

---

## 3. Plugin types and their entry contract

`entry.class` in `entry.module` must implement:

| `type` | contract | reference |
|---|---|---|
| `engine` | subclass of `EquationModule` — `name`, `display_name`, `version`, `description`, `confidence_floor`, `formulary()`, `run(eq, params)`, `viewer_data(eq, params, mode)` | `engine/registry.py`; every `modules/<name>/` |
| `face` | a chat-room identity: attributes `name`, `role`; methods `probe() -> float`, `opinion(topic) -> (stance, weight)`, `act(request) -> str` (only if it acts) | `PtolemyDesktop/ptolemy_console.py` `Face` |
| `lens` | `analyse(target) -> dict` — runs ACROSS whatever it is handed (an equation result, a value, an engine name) and returns a plain dict | `examples/hello_lens/plugin.py` |
| `tab` | `run_tab(scr) -> None` (curses) **and** `act(query) -> str` (headless) | Archimedes / `DerivationBrowser` |

`format.validate()` imports `entry.module`, resolves `entry.class` (for an
engine it will fall back to the sole `EquationModule` subclass if the named
attribute is missing), and checks the contract.

---

## 4. Host API

What a plugin may call on the host. Namespaced; gated by §2.3.

| namespace | ungated | permission-gated |
|---|---|---|
| `registry` | `list_modules`, `list_equations`, `get_module`, `get_equation` (`registry.read`) | `run` (`registry.run`) |
| `proof_locale` | `render_guided`, `render_academic`, `proof_catalog` (`proof.render`) | — |
| `manifest` | `load`, `menu_tree`, `available` (`manifest.read`) | — |
| `constants` | the canonical constants (`Ω_ZS`, `d*`, …) | — |
| `codegate` | — | `propose(path, new_text, reason)` (`codegate.propose`) |
| `fs` | — | `read(path)` under a granted `fs.read:<scope>` |
| `net` | — | `search(q)` (`net.search`), `browse(url)` (`net.browse`) |

---

## 5. Discovery and loading

`format.discover()` search order — **first `id` wins**:

1. **built-in** — `ValaQuenta/modules/<name>/manifest.json`
2. **examples** — `ValaQuenta/examples/*/manifest.json`
3. **user** — `~/.valaquenta/plugins/*/manifest.json`
   (`$VALAQUENTA_HOME` overrides `~/.valaquenta`)
4. **path** — `$VALAQUENTA_PLUGIN_PATH` (os-pathsep list of plugin dirs, or a
   single plugin dir), and any `paths=` passed to `discover()`

Enable/disable: `~/.valaquenta/enabled.json` (`{ "<id>": true|false }`;
absent ⇒ enabled). Version pinning is by `dependencies` ranges.

After discovery the host registers each plugin by `type`: `engine` → the
`ModuleRegistry`; `face` / `lens` / `tab` → the console.

---

## 6. Versioning and migration

- `format_version` is bumped only for a breaking manifest change; `1` is
  current. A plugin declaring a higher `format_version` than the host knows is
  refused with a clear message.
- `valaquenta.engine-manifest/1` files (pre-Format) are accepted: `normalise()`
  sets `schema`/`format_version`, derives `id` = `org.ainulindale.<name>`,
  `type` = `engine`, `entry` from `ValaQuenta.modules.<name>`, `license` =
  `LicenseRef-ValaQuenta-Private`. `python3 -m ValaQuenta.engine.format upgrade
  --write` rewrites them in canonical order.

---

## 7. Licensing and distribution

The `license` field is load-bearing:

- **`GPL-3.0-only`** or a permissive SPDX id ⇒ the plugin can ship with
  PtolemyDesktop / PTorrent (both GNU) and go "out there" on its own.
- Anything else (e.g. **`LicenseRef-ValaQuenta-Private`**) ⇒ the plugin stays
  behind ValaQuenta — discoverable and runnable locally, never published.

The Raw monad that PtolemyDesktop ships is trained on GNU components only and
carries a GNU licence; a user's own engine layer (Cody's ValaQuenta) is
private and marked so.

---

## 8. Minimal example — a `lens`

`examples/hello_lens/manifest.json`:

```json
{
  "schema": "valaquenta.plugin/1",
  "format_version": 1,
  "id": "com.example.hello_lens",
  "type": "lens",
  "name": "hello_lens",
  "version": "1.0",
  "license": "GPL-3.0-only",
  "entry": { "module": "ValaQuenta.examples.hello_lens.plugin", "class": "HelloLens" },
  "permissions": [],
  "provenance": { "origin": "reference plugin", "authors": ["ValaQuenta Format"],
    "created": "2026-09-01", "status_label": "ESTABLISHED",
    "predecessors": [], "citations": [],
    "wiki": { "ainulindale": "", "valaquenta": "ValaQuenta/wiki/valaquenta_format.md" },
    "notebook": "", "proof_locale": "" }
}
```

`examples/hello_lens/plugin.py`:

```python
class HelloLens:
    name = "hello"
    def analyse(self, target):
        return {"lens": "hello", "type_in": type(target).__name__, "...": "..."}
```

`python3 -m ValaQuenta.engine.format discover` then lists it as
`lens  com.example.hello_lens  v1.0  example  HelloLens`.
