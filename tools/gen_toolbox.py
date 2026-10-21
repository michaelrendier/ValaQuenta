"""Generate a Toolbox page from the registry, so it cannot drift from the code.

Full Engine Protocol part 6: every new engine, and every new equation added to an
existing engine's formulary(), gets its Toolbox page (re)generated and its row in
wiki/toolbox/00_index.md, followed by the index repass.

Run from the repository root's parent:  python3 ValaQuenta/tools/gen_toolbox.py <module_name> <NN>
Writes ValaQuenta/wiki/toolbox/<NN>_<module_name>.md and adds the index row if it is missing.
An equation that needs an external file raises FileNotFoundError; its example is then a note, not a result.
"""
import datetime
import inspect
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent))


def short(x, n=170):
    s = repr(x)
    return s if len(s) <= n else s[:n] + " ..."


def main(name, nn):
    from ValaQuenta.__main__ import _register_all
    reg = _register_all()
    mod = reg.get_module(name)
    out = [f"# {mod.display_name}\n",
           f"**Module:** `ValaQuenta.modules.{name}`\n**Import:** `from ValaQuenta.modules.{name}.tools import {type(mod).__name__}`\n**Theory page:** [{name}.md](../{name}.md)\n\n---\n",
           f"`{name}` · v{mod.version} · confidence floor **{mod.confidence_floor}**\n", mod.description + "\n",
           "### Equations (`formulary()`)\n",
           "Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.\n"]
    for e in mod.formulary():
        sig = str(inspect.signature(e.compute)) if e.compute else "()"
        params = ", ".join(f"`{p}`" for p in e.params) if e.params else "—"
        out.append(f"**`{e.name}`** — {e.display}\n  params: {params}  ·  confidence: `{e.confidence}`  ·  signature: `{sig}`")
        try:
            r = reg.run(f"{name}.{e.name}", {})["result"]
            out.append(f"```python\n>>> module.run('{e.name}', {{}})['result']\n{short(r)}\n```\n")
        except FileNotFoundError as ex:
            out.append(f"```python\n>>> module.run('{e.name}', {{}})['result']      # needs a local file: {ex}\n```\n")
    sc = mod.shell_commands()
    if sc:
        out.append("### Shell commands\n\n" + " · ".join(f"`{k}`" for k in sc) + "\n")
    out.append(f"\n---\n\n*Theory page: [`{name}.md`](../{name}.md).*\n")
    page = ROOT / "wiki" / "toolbox" / f"{nn}_{name}.md"
    page.write_text("\n".join(out))
    idx = ROOT / "wiki" / "toolbox" / "00_index.md"
    text = idx.read_text()
    row = f"| [{nn}_{name}.md]({nn}_{name}.md) | {mod.display_name} | {datetime.date.today()} | `modules/{name}/` |\n"
    if f"[{nn}_{name}.md]" not in text:
        last = [l for l in text.splitlines(True) if l.startswith("| [") and "_" in l.split("]")[0]][-1]
        idx.write_text(text.replace(last, last + row, 1))
        print("index row added; now do the index repass")
    print("wrote", page)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
