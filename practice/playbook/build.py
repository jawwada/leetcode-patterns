"""
Build the LeetCode Playbook notebooks from the markdown sections in practice/playbook/NN_slug.md.

Each section is plain markdown. Every ```python fence becomes a code cell; everything else becomes
markdown, and a line `<!-- cell -->` splits a markdown cell. Other fences (```text, ```py) stay as
markdown, so use them for code that should be shown but not run. Code cells run in order in one
namespace per notebook (like a kernel) and their output is embedded; a failing cell stops the build.

Every code cell should be followed by a markdown cell that starts with **Try it** (3-4 experiments);
the build lists the cells that are not.

Rows of every "### Problem map" table (| Problem | Where | Key insight |) feed the A-Z problem finder
in the last notebook, and the build reports topic-folder problems that no Problem map mentions yet.

Usage: python3 practice/playbook/build.py                  # all notebooks -> practice/LeetCode_Playbook/
       python3 practice/playbook/build.py --no-exec        # same, without running anything
       python3 practice/playbook/build.py --only 06,07 --out /tmp/x.ipynb --folders stack,queues
                                                            # some sections as one notebook, to check them
"""
import ast
import contextlib
import io
import re
import sys
import json
import traceback
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT_DIR = HERE.parent / "LeetCode_Playbook"
TOPICS = ["arrays_hashing", "backtracking", "binary_search", "bit_manipulation", "design",
          "dynamic_programming", "graphs", "greedy", "heap", "intervals", "linked_list",
          "math_geometry", "queues", "sliding_window", "stack", "strings", "trees", "tries",
          "two_pointers"]
SETUP = """\
# Setup: everything this notebook imports. Run this cell first.
from collections import Counter, defaultdict, deque, OrderedDict
from functools import cmp_to_key, lru_cache
from itertools import accumulate, combinations, permutations, product
import bisect, heapq, math, random, string"""

# (file name, title, one-line description, section prefixes in order)
NOTEBOOKS = [
    ("01_Start_Here.ipynb", "Start Here",
     "How to use the playbook, how to turn an idea into code, and the Python you need for it.", ["00", "01", "02"]),
    ("02_Arrays_Hashing_Prefix_Sums.ipynb", "Arrays, Hashing & Prefix Sums",
     "Remember what you have seen, and turn running totals into O(1) range questions.", ["03", "04"]),
    ("03_Two_Pointers_Sliding_Window_Strings.ipynb", "Two Pointers, Sliding Window & Strings",
     "Two fingers on a sequence, a window that crawls, and hand-written string parsing.", ["05", "06", "20"]),
    ("04_Stacks_Queues_Linked_Lists.ipynb", "Stacks, Queues & Linked Lists",
     "The linear structures: what waits on a stack, what a monotonic stack resolves, and pointer rewiring.",
     ["07", "08", "10"]),
    ("05_Binary_Search_Sorting.ipynb", "Binary Search & Sorting",
     "First True in a monotone landscape, searching on the answer, and what sorting unlocks.", ["09", "23"]),
    ("06_Trees_Tries.ipynb", "Trees & Tries",
     "What a recursive call passes down, returns up and records; prefix trees for many words.", ["11", "12"]),
    ("07_Heaps_Intervals_Greedy.ipynb", "Heaps, Intervals & Greedy",
     "Always the cheapest next, overlapping ranges, and local choices you can prove are safe.",
     ["13", "14", "15"]),
    ("08_Backtracking.ipynb", "Backtracking (and a short DP map)",
     "Choose, explore, un-choose; and how memoised recursion grows out of it.", ["16", "25"]),
    ("09_Graphs.ipynb", "Graphs",
     "BFS and DFS, ordering and connectivity, weighted shortest paths and spanning trees.", ["17", "18", "19"]),
    ("10_Matrices_Math_Bits.ipynb", "Matrices, Math & Bits",
     "Index arithmetic on grids, bit arrays and bit tricks, and the math recipes interviews use.", ["21", "22"]),
    ("11_Design.ipynb", "Design Problems",
     "From requirements to a class: one structure per operation, kept in sync by an invariant.", ["24"]),
    ("12_Interview_Day.ipynb", "Interview Day",
     "Checklists for the last mile, and the A-Z finder for every problem in the repo.", ["26"]),
]


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
    return [part for kind, src in cells for part in split_try_it(kind, src)]


def split_try_it(kind, src):
    """A markdown cell that opens with **Try it** keeps only its bullet list; the rest becomes its own cell."""
    if kind != "markdown" or not src.lstrip().startswith("**Try it**"):
        return [(kind, src)]
    lines = src.splitlines()
    end = 1
    while end < len(lines) and (lines[end].startswith(("-", " ")) or not lines[end].strip()):
        if not lines[end].strip() and not any(l.startswith("-") for l in lines[end + 1:end + 2]):
            break
        end += 1
    head, tail = "\n".join(lines[:end]).strip(), "\n".join(lines[end:]).strip()
    return [(kind, head)] + ([(kind, tail)] if tail else [])


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
    return text.splitlines(keepends=True)


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


def load_sections(prefixes=None):
    """prefix -> {"title", "file", "cells": [(kind, src)], "rows": [(name, where, insight)]}"""
    sections = {}
    for f in sorted(HERE.glob("[0-9][0-9]_*.md")):
        if prefixes and f.stem[:2] not in prefixes:
            continue
        text = f.read_text()
        title = next((l[3:].strip() for l in text.splitlines() if l.startswith("## ")), f.stem)
        cells, rows, first_md = [], [], True
        for kind, src in parse(text):
            if kind == "markdown":
                if first_md:
                    src = f'<a id="s{f.stem[:2]}"></a>\n\n' + src
                    first_md = False
                rows += problem_rows(src)
            cells.append((kind, src))
        sections[f.stem[:2]] = {"title": title, "file": f.name, "cells": cells, "rows": rows}
    return sections


def finder_md(sections, link):
    """The A-Z problem finder; link(prefix) gives the href of a section."""
    rows = [(name, where, insight, p) for p, s in sections.items() for name, where, insight in s["rows"]]
    body = ['<a id="finder"></a>', "", "## A-Z problem finder", "",
            "Every problem in this repo and the practice bank, with the section that teaches its technique.", "",
            "| Problem | Technique | Where | Key insight |", "|---|---|---|---|"]
    for name, where, insight, p in sorted(rows, key=lambda r: re.sub(r"[^a-z0-9 ]", "", r[0].lower())):
        body.append(f"| {name} | [{sections[p]['title']}]({link(p)}) | {where} | {insight} |")
    return "\n".join(body)


def to_notebook(nb_cells, out, run):
    """nb_cells: [{"kind", "src", "where"}] -> write an executed .ipynb; returns (#cells, #code cells)."""
    out_cells, code_cells = [], []
    for i, c in enumerate(nb_cells):
        cell = {"cell_type": c["kind"], "id": f"cell-{i:04d}", "metadata": {}, "source": lines(c["src"])}
        if c["kind"] == "code":
            cell.update({"execution_count": None, "outputs": [], "_src": c["src"], "_where": c["where"]})
            code_cells.append(cell)
        out_cells.append(cell)
    if run:
        execute(code_cells)
    else:
        for cell in code_cells:
            cell.pop("_src"), cell.pop("_where")
    nb = {"cells": out_cells, "nbformat": 4, "nbformat_minor": 5,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python", "version": "3"}}}
    try:
        import nbformat
        nbformat.validate(nbformat.from_dict(nb))
    except ImportError:
        pass
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    return len(out_cells), len(code_cells)


def report(sections, nb_cells, topics, full):
    no_try = [nb_cells[i]["where"] for i, c in enumerate(nb_cells)
              if c["kind"] == "code" and c["where"] != "setup"
              and not (i + 1 < len(nb_cells) and nb_cells[i + 1]["kind"] == "markdown"
                       and nb_cells[i + 1]["src"].lstrip().startswith("**Try it**"))]
    wheres = [where for s in sections.values() for _, where, _ in s["rows"]]
    mentioned = " ".join(wheres)
    missing = [f"{t}/{p.name}" for t in topics for p in sorted((REPO / t).glob("*.py"))
               if p.name != "__init__.py" and f"{t}/{p.name}" not in mentioned]
    paths = Counter(p for where in wheres for p in re.findall(r"`([a-z_]+/[a-z0-9_]+\.py)`", where)
                    if p.split("/")[0] in TOPICS)
    dupes = sorted(p for p, n in paths.items() if n > 1)
    print(f"code cells without a **Try it** block after them: {len(no_try)}"
          + "".join(f"\n  {w}: {n}" for w, n in sorted(Counter(no_try).items())))
    print(f"topic problems not in any Problem map: {len(missing)}" + "".join(f"\n  {m}" for m in missing))
    print(f"topic problems in more than one Problem map row: {len(dupes)}" + "".join(f"\n  {d}" for d in dupes))
    if full:
        files = {nb[0] for nb in NOTEBOOKS}
        anchors = {"s" + p for p in sections} | {"finder", "notebooks", "top"}
        links = Counter(m for c in nb_cells if c["kind"] == "markdown"
                        for m in re.findall(r"\]\(([\w.-]*#[\w-]+|[\w.-]+\.ipynb)\)", c["src"]))
        bad = sorted(l for l in links
                     if (l.split("#")[0] and l.split("#")[0] not in files)
                     or ("#" in l and l.split("#")[1] not in anchors))
        print(f"broken links: {len(bad)}" + "".join(f"\n  {b}" for b in bad))
        all_text = "\n".join(c["src"] for c in nb_cells)
        bank = sorted(p.relative_to(REPO).as_posix() for p in (HERE.parent / "simple").glob("*.py"))
        bank_missing = [b for b in bank if b not in all_text]
        print(f"practice/simple problems never referenced: {len(bank_missing)}"
              + "".join(f"\n  {m}" for m in bank_missing))


def build_one(prefixes, out, topics, run):
    """Selected sections as one notebook (used to check sections in isolation)."""
    sections = load_sections(prefixes)
    toc = [f"{i}. [{s['title']}](#s{p})" for i, (p, s) in enumerate(sections.items(), 1)]
    nb_cells = [{"kind": "markdown", "src": "## Contents\n\n" + "\n".join(toc), "where": "toc"},
                {"kind": "code", "src": SETUP, "where": "setup"}]
    for p, s in sections.items():
        nb_cells += [{"kind": k, "src": src, "where": s["file"]} for k, src in s["cells"]]
    if any(s["rows"] for s in sections.values()):
        nb_cells.append({"kind": "markdown", "src": finder_md(sections, lambda p: f"#s{p}"), "where": "finder"})
    n, code = to_notebook(nb_cells, out, run)
    print(f"wrote {out}: {n} cells ({code} code), {len(sections)} sections, "
          f"{sum(len(s['rows']) for s in sections.values())} problem-map rows")
    report(sections, nb_cells, topics, full=False)


def build_all(run):
    sections = load_sections()
    home = {p: nb[0] for nb in NOTEBOOKS for p in nb[3]}
    unplaced = sorted(set(sections) - set(home))
    if unplaced:
        sys.exit(f"sections not assigned to a notebook: {unplaced}")
    last = NOTEBOOKS[-1][0]

    def href(prefix, here):                   # link to a section from notebook `here`
        return f"#s{prefix}" if home[prefix] == here else f"{home[prefix]}#s{prefix}"

    every_cell, total = [], 0
    for k, (fname, title, blurb, prefixes) in enumerate(NOTEBOOKS):
        prev_nb, next_nb = NOTEBOOKS[k - 1] if k else None, NOTEBOOKS[k + 1] if k + 1 < len(NOTEBOOKS) else None
        nav = []
        if prev_nb:
            nav.append(f"← [{prev_nb[1]}]({prev_nb[0]})")
        nav.append("[All notebooks](01_Start_Here.ipynb#notebooks)" if k else "[All notebooks](#notebooks)")
        nav.append(f"[A-Z problem finder]({'' if fname == last else last}#finder)")
        if next_nb:
            nav.append(f"[{next_nb[1]}]({next_nb[0]}) →")
        contents = " · ".join(f"[{sections[p]['title']}](#s{p})" for p in prefixes)
        header = (f'<!-- notebook-header -->\n<a id="top"></a>\n\n# {k + 1}. {title}\n\n'
                  f"*LeetCode Playbook · notebook {k + 1} of {len(NOTEBOOKS)}* · {blurb}\n\n"
                  f"**In this notebook:** {contents}\n\n{' · '.join(nav)}\n\n"
                  "Run the setup cell below first; after that every section runs from its first cell.")
        nb_cells = [{"kind": "markdown", "src": header, "where": "header"},
                    {"kind": "code", "src": SETUP, "where": "setup"}]
        table = None
        if k == 0:                         # the list of notebooks, at the end of the first section
            rows = ['<a id="notebooks"></a>', "", "## The notebooks", "",
                    "| # | Notebook | Sections |", "|---|---|---|"]
            for j, (f2, t2, b2, p2) in enumerate(NOTEBOOKS, 1):
                secs = " · ".join(f"[{sections[p]['title']}]({href(p, fname)})" for p in p2)
                rows.append(f"| {j} | [{t2}]({f2}) | {secs} |")
            table = {"kind": "markdown", "src": "\n".join(rows), "where": "notebooks"}
        for p in prefixes:
            for kind, src in sections[p]["cells"]:
                if kind == "markdown":     # point links at the notebook that holds the target section
                    src = re.sub(r"\]\(#s(\d\d)\)", lambda m: f"]({href(m.group(1), fname)})", src)
                    if fname != last:
                        src = src.replace("](#finder)", f"]({last}#finder)")
                nb_cells.append({"kind": kind, "src": src, "where": sections[p]["file"]})
            if table:                      # the list of notebooks closes the Start Here section
                nb_cells.append(table)
                table = None
        if fname == last:
            nb_cells.append({"kind": "markdown", "src": finder_md(sections, lambda p: href(p, fname)),
                             "where": "finder"})
        n, code = to_notebook(nb_cells, OUT_DIR / fname, run)
        total += n
        print(f"wrote {(OUT_DIR / fname).relative_to(REPO)}: {n} cells ({code} code)")
        every_cell += nb_cells
    rows = sum(len(s["rows"]) for s in sections.values())
    print(f"{len(NOTEBOOKS)} notebooks, {total} cells, {len(sections)} sections, {rows} problem-map rows")
    report(sections, every_cell, TOPICS, full=True)


def main():
    run = "--no-exec" not in sys.argv
    only = arg("--only")
    if only:
        topics = arg("--folders").split(",") if arg("--folders") else TOPICS
        build_one(only.split(","), Path(arg("--out", HERE / "check.ipynb")), topics, run)
    else:
        build_all(run)


if __name__ == "__main__":
    main()
