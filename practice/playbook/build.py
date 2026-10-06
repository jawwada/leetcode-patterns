"""
Build practice/LeetCode_Playbook.ipynb from the markdown sections in practice/playbook/NN_slug.md.

Each section is plain markdown. Every ```python fence becomes a code cell; everything else becomes
markdown, and a line `<!-- cell -->` splits a markdown cell. Other fences (```text, ```py) stay as
markdown, so use them for code that should be shown but not run. Code cells run in order in one
namespace (like a kernel) and their output is embedded; a failing cell stops the build.

Rows of every "### Problem map" table (| Problem | Where | Key insight |) feed the A-Z problem finder
at the end, and the build reports topic-folder problems that no Problem map mentions yet.

Usage: python3 practice/playbook/build.py                        # build, execute, embed outputs
       python3 practice/playbook/build.py --no-exec              # build without running anything
       python3 practice/playbook/build.py --only 06,07 --out /tmp/x.ipynb --folders stack,queues
                                                                  # check some sections in isolation
"""
import ast
import contextlib
import io
import re
import sys
import json
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = HERE.parent / "LeetCode_Playbook.ipynb"
TOPICS = ["arrays_hashing", "backtracking", "binary_search", "bit_manipulation", "design",
          "dynamic_programming", "graphs", "greedy", "heap", "intervals", "linked_list",
          "math_geometry", "queues", "sliding_window", "stack", "strings", "trees", "tries",
          "two_pointers"]
SETUP = """\
# Setup: everything the notebook imports. Run this cell first.
from collections import Counter, defaultdict, deque, OrderedDict
from functools import cmp_to_key, lru_cache
from itertools import accumulate, combinations, permutations, product
import bisect, heapq, math, random, string"""


def parse(text):
    """One section file -> [(kind, source)]."""
    cells, buf, kind = [], [], "markdown"

    def flush():
        src = "\n".join(buf).strip("\n")
        if src.strip():
            cells.append((kind, src))
        buf.clear()

    for line in text.splitlines():
        if kind == "markdown" and line.strip() == "```python":
            flush()
            kind = "code"
        elif kind == "code" and line.strip() == "```":
            flush()
            kind = "markdown"
        elif kind == "markdown" and line.strip() == "<!-- cell -->":
            flush()
        else:
            buf.append(line)
    if kind == "code":
        raise ValueError("unclosed ```python fence")
    flush()
    return cells


def problem_rows(markdown):
    """Rows of the '### Problem map' tables: (name, where, insight)."""
    rows, inside = [], False
    for line in markdown.splitlines():
        if line.startswith("#"):
            inside = line.strip().lower().startswith("### problem map")
            continue
        if inside and line.startswith("|") and not re.match(r"^\|\s*(Problem|-)", line):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 3:
                rows.append((parts[0], parts[1], parts[2]))
    return rows


def lines(text):
    out = text.splitlines(keepends=True)
    return out


def execute(code_cells):
    ns = {"__name__": "__main__"}
    for n, cell in enumerate(code_cells, 1):
        src, where = cell.pop("_src"), cell.pop("_where")
        tree = ast.parse(src)
        last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
        buf, value = io.StringIO(), None
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(tree, f"<{where} cell {n}>", "exec"), ns)
                if last is not None:
                    value = eval(compile(ast.Expression(last.value), f"<{where} cell {n}>", "eval"), ns)
        except Exception:
            sys.stderr.write(f"\nFAILED: {where}, code cell {n}\n{src}\n\n")
            traceback.print_exc()
            sys.exit(1)
        cell["execution_count"] = n
        if buf.getvalue():
            cell["outputs"].append({"output_type": "stream", "name": "stdout", "text": lines(buf.getvalue())})
        if value is not None:
            cell["outputs"].append({"output_type": "execute_result", "execution_count": n, "metadata": {},
                                    "data": {"text/plain": lines(repr(value))}})
        if len(buf.getvalue().splitlines()) > 40:
            print(f"note: {where} cell {n} prints {len(buf.getvalue().splitlines())} lines")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    files = sorted(HERE.glob("[0-9][0-9]_*.md"))
    only = arg("--only")
    if only:
        files = [f for f in files if f.stem[:2] in only.split(",")]
    out = Path(arg("--out", OUT))
    topics = arg("--folders").split(",") if arg("--folders") else TOPICS
    cells, toc, finder = [], [], []
    for f in files:
        text = f.read_text()
        title = next((l[3:].strip() for l in text.splitlines() if l.startswith("## ")), f.stem)
        anchor = "s" + f.stem[:2]
        toc.append(f"{len(toc) + 1}. [{title}](#{anchor})" if f.stem[:2] != "00" else None)
        first_md = True
        for kind, src in parse(text):
            if kind == "markdown":
                if first_md:
                    src = f'<a id="{anchor}"></a>\n\n' + src
                    first_md = False
                for name, where, insight in problem_rows(src):
                    finder.append((name, where, insight, title, anchor))
            cells.append({"kind": kind, "src": src, "where": f.name})

    toc_md = "## Contents\n\n" + "\n".join(t for t in toc if t) + "\n\n[A-Z problem finder](#finder)"
    if finder:
        body = ["## A-Z problem finder", "",
                "Every problem in this repo and the practice bank, with the section that teaches its technique.", "",
                "| Problem | Technique | Where | Key insight |", "|---|---|---|---|"]
        for name, where, insight, title, anchor in sorted(finder, key=lambda r: re.sub(r"[^a-z0-9 ]", "", r[0].lower())):
            body.append(f"| {name} | [{title}](#{anchor}) | {where} | {insight} |")
        cells.append({"kind": "markdown", "src": '<a id="finder"></a>\n\n' + "\n".join(body), "where": "finder"})

    # title cell of 00 first, then contents, then the setup cell
    nb_cells = []
    for i, c in enumerate(cells):
        nb_cells.append(c)
        if i == 0:
            nb_cells.append({"kind": "markdown", "src": toc_md, "where": "toc"})
            nb_cells.append({"kind": "code", "src": SETUP, "where": "setup"})

    out_cells, code_cells = [], []
    for i, c in enumerate(nb_cells):
        cell = {"cell_type": c["kind"], "id": f"cell-{i:04d}", "metadata": {}, "source": lines(c["src"])}
        if c["kind"] == "code":
            cell.update({"execution_count": None, "outputs": [], "_src": c["src"], "_where": c["where"]})
            code_cells.append(cell)
        out_cells.append(cell)

    if "--no-exec" in sys.argv:
        for cell in code_cells:
            cell.pop("_src"), cell.pop("_where")
    else:
        execute(code_cells)

    nb = {"cells": out_cells, "nbformat": 4, "nbformat_minor": 5,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python", "version": "3"}}}
    try:
        import nbformat
        nbformat.validate(nbformat.from_dict(nb))
    except ImportError:
        pass
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")

    mentioned = " ".join(where for _, where, _, _, _ in finder)
    missing = [f"{t}/{p.name}" for t in topics for p in sorted((REPO / t).glob("*.py"))
               if p.name != "__init__.py" and f"{t}/{p.name}" not in mentioned]
    all_text = "\n".join(c["src"] for c in nb_cells)
    bank = sorted(p.relative_to(REPO).as_posix() for p in (HERE.parent / "simple").glob("*.py"))
    bank_missing = [b for b in bank if b not in all_text]
    print(f"wrote {out}: {len(out_cells)} cells ({len(code_cells)} code), "
          f"{len(files)} sections, {len(finder)} problem-map rows")
    print(f"topic problems not in any Problem map: {len(missing)}" + ("".join(f"\n  {m}" for m in missing)))
    if not only:
        print(f"practice/simple problems never referenced: {len(bank_missing)}" + ("".join(f"\n  {m}" for m in bank_missing)))


if __name__ == "__main__":
    main()
