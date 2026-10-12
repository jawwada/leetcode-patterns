"""Build the two 100 Algorithms books (pseudocode + Python) as PDFs, and the ranked list.

Usage: python3 algorithms_100/build.py [--partial] [--md-only]
  --partial   skip entries that are not written yet (default: all 100 must exist)
  --md-only   write the combined Markdown files but do not run pandoc
"""
import ast
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build")
PSEUDO_PDF = os.path.join(HERE, "100_Algorithms_Pseudocode.pdf")
PYTHON_PDF = os.path.join(HERE, "100_Algorithms_Python.pdf")
LIST_TXT = os.path.join(REPO, "algorithms.txt")

TOPIC_ORDER = [
    "Arrays & Hashing", "Hash Map Internals", "Two Pointers", "Sliding Window",
    "Binary Search", "Sorting", "Heaps", "Stacks", "Queues", "Intervals", "Greedy",
    "Backtracking", "DFS", "BFS", "Cycle Detection", "Topological Sort",
    "Connected Components", "Shortest Path", "MST", "BST", "Tries", "Strings", "Math",
    "Geometry", "Bit Manipulation", "Design",
]

TIER_INTRO = {
    1: "These thirty-five algorithms are the core of the interview. Each one is the standard "
       "answer to a whole family of problems: hashing to remember the past, two pointers and "
       "sliding windows for sequences, binary search for anything monotone, sorting and heaps "
       "for order, stacks for nesting, BFS and DFS for every tree and graph, Kahn's algorithm, "
       "union-find and Dijkstra for dependencies, components and distances, the trie for "
       "prefixes and the LRU cache for design. Learn them until you can write each one from a "
       "blank page without hesitation.",
    2: "The next thirty-five deepen every topic of the first tier and add the classic harder "
       "variants: partition-based selection, the histogram stack, expression evaluation, the "
       "greedy exchange arguments, grid backtracking, BFS on implicit graphs, topological order "
       "by DFS, KMP. They come up often enough that each one deserves a careful read and a run "
       "of its code.",
    3: "The last thirty round out the set: second implementations of ideas you already own "
       "(open addressing, heap sort, Prim), the string toolkit, number theory, geometry, bit "
       "tricks and the designs that turn up in senior loops. Read each one once, keep its "
       "picture in mind, and come back to it when a problem calls for it.",
}

PSEUDO_INTRO = r"""
# How to Read This Book {#how-to-read}

```{=latex}
\markboth{How to Read This Book}{}
```

This book holds one hundred algorithms in the order to learn them. The order is importance for a coding interview: how often the idea appears, how many other problems it unlocks, and how much it costs to be missing it. Tier 1, the first thirty-five, are the algorithms to know cold. Tier 2, the next thirty-five, come up often enough that you should know them well. Tier 3, the last thirty, are good to know and separate a prepared candidate from a strong one. Inside a tier, related algorithms sit next to each other, so each tier is one pass over every topic and the next tier deepens it.

Every entry fits on a page or two and always reads in the same order. It opens with the problem in plain words and a tiny example. Then comes the idea: when a brute force exists, one sentence names it and its cost, and the rest explains the insight that beats it as a picture of the data and the motion of the algorithm. A framed picture traces the algorithm on the example, and every number in it was produced by running the code. The pseudocode follows, then a closing paragraph on the cost, the signals in a problem statement that call for the algorithm, and the classic mistake, and finally a few LeetCode problems to practise on. A reference such as #41 points to entry 41 and is a link.

The companion book, *100 Algorithms in Python*, has the same entries in the same order, each one a short runnable file whose variable names match this pseudocode line for line.

## Notation

The pseudocode reads like careful English. Indentation alone marks a block, so there are no END lines. Keywords are in capitals, `←` assigns and `=` compares, so no line ever has to be read twice. Ranges are inclusive at both ends, arrays start at index 0, and containers are written with the operation you would say out loud.

```pseudo
FUNCTION Name(a, b)               // RETURN hands back a value
    x ← 0                         // assignment
    IF x = 0 AND b ≠ null         // comparison: = ≠ < ≤ > ≥
        ...
    ELSE IF x > 0 OR NOT done
        ...
    ELSE
        ...
    FOR i FROM 0 TO n - 1         // inclusive at both ends
    FOR i FROM n - 1 DOWNTO 0     // counting down
    FOR EACH x IN items
    WHILE lo < hi
    floor(a / b), a mod b, ∞      // integer division, remainder, infinity
    seen ← empty map              // also: empty set, list, stack, queue, min-heap
    seen[key] ← value             // write; "key IN seen" tests membership
    stack.push(x), stack.pop(), stack.top()
    queue.enqueue(x), queue.dequeue()
    heap.push(x), heap.pop(), heap.top()
    a[i..j]                       // the slice from i to j, both included
```
"""

PYTHON_INTRO = r"""
# How to Read This Book {#how-to-read}

```{=latex}
\markboth{How to Read This Book}{}
```

This book holds the same one hundred algorithms as *100 Algorithms in Pseudocode*, in the same order, as Python you can run. The order is importance for a coding interview. Tier 1, the first thirty-five, are the algorithms to know cold; Tier 2, the next thirty-five, are the ones to know well; Tier 3, the last thirty, are good to know. Inside a tier, related algorithms sit next to each other.

Each entry states the problem with a tiny example and then shows one complete file. A file has up to three parts: the helpers, when the input is a tree or a linked list; the algorithm, where every function opens with a one-line docstring that gives the idea and its cost; and a try-it section of prints whose expected output follows `# ->` on the same line. Every file runs on its own, for example `python3 algorithms_100/python/001_two_sum.py`, and every printed line was checked against its comment. The variable names match the pseudocode book line for line, so the two books can be read side by side.

The Python is simple on purpose. Loops are written out instead of comprehensions, there are no lambdas or one-line tricks, and names say what they hold. The aim is that you read a function once, close the book and write it again. The toolbox is small.

```python
from collections import deque    # a queue: append() and popleft() are O(1)
import heapq                     # a min-heap on a list: heappush, heappop, heap[0]
import math                      # math.inf, math.sqrt, math.ceil
import random                    # random pivots and sampling
import bisect                    # ready-made binary search (search chapter only)

# sorted(items) returns a new sorted list; items.sort() sorts in place.
# Both are O(n log n) and stable, and tuples sort field by field.
```
"""


def load_manifest():
    with open(os.path.join(HERE, "manifest.json")) as f:
        data = json.load(f)
    return data["algorithms"], data["tiers"]


def md_escape(text):
    return re.sub(r"([\\`*_{}\[\]<>#|~^$])", r"\\\1", text)


def latex_escape(text):
    out = []
    for ch in text:
        if ch in "&%$#_{}":
            out.append("\\" + ch)
        elif ch == "^":
            out.append("\\^{}")
        elif ch == "~":
            out.append("\\~{}")
        elif ch == "\\":
            out.append("\\textbackslash{}")
        else:
            out.append(ch)
    return "".join(out)


def raw_latex(code):
    return "```{=latex}\n" + code + "\n```\n"


def stem(entry):
    return "%03d_%s" % (entry["rank"], entry["slug"])


def read_pseudo(entry):
    path = os.path.join(HERE, "pseudo", stem(entry) + ".md")
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n.*?\n---\n(.*)$", text, re.S)
    return m.group(1).strip() if m else text.strip()


def load_standard_helpers():
    """Map helper name -> exact source of the canonical helper in build/helpers.py."""
    src = open(os.path.join(BUILD, "helpers.py"), encoding="utf-8").read()
    found = {}
    for node in ast.parse(src).body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            found[node.name] = ast.get_source_segment(src, node)
    return found


STANDARD = None


def collapse_helpers(code):
    """Drop canonical helpers from an entry's code; note them on the helpers marker."""
    global STANDARD
    if STANDARD is None:
        STANDARD = load_standard_helpers()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code
    lines = code.split("\n")
    drop, names = set(), []
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in STANDARD:
            if ast.get_source_segment(code, node) == STANDARD[node.name]:
                names.append(node.name)
                for i in range(node.lineno - 1, node.end_lineno):
                    drop.add(i)
    if not names:
        return code
    kept = []
    for i, line in enumerate(lines):
        if i in drop:
            continue
        kept.append(line)
        if line == "# --- helpers ---":
            kept.append("# standard helpers %s: printed once under Standard Helpers"
                        % ", ".join(names))
    text = "\n".join(kept)
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n", "\n\n\n")
    return text


def helpers_section():
    src = open(os.path.join(BUILD, "helpers.py"), encoding="utf-8").read()
    body = src.split("# --- helpers ---", 1)[1].strip("\n")
    return ("\n## Standard Helpers\n\nEntries whose input is a binary tree or a linked list build "
            "it from a plain Python list, so a test reads like the LeetCode example. "
            "`build_tree` takes a level-order list with `None` for a missing child, and "
            "`tree_to_list` turns a tree back into one; `build_list` and `to_list` do the same "
            "for linked lists. Every file carries its own copy so it runs on its own; the book "
            "prints them once, here, and each entry names the ones it uses.\n\n"
            "```python\nfrom collections import deque      # popleft is O(1)\n\n\n"
            + body + "\n```\n")


def read_python(entry):
    """Return (problem paragraph, code without the module docstring)."""
    path = os.path.join(HERE, "python", stem(entry) + ".py")
    if not os.path.exists(path):
        return None
    src = open(path, encoding="utf-8").read()
    m = re.match(r'\s*"""(.*?)"""\n(.*)$', src, re.S)
    if not m:
        return "", src
    doc_parts = m.group(1).strip("\n").split("\n\n")
    problem = " ".join(" ".join(doc_parts[1:]).split()) if len(doc_parts) > 1 else ""
    return problem, collapse_helpers(m.group(2).strip("\n"))


def entry_heading(entry, kind):
    plain = "%d. %s" % (entry["rank"], entry["title"])
    meta = "%s · %s · Tier %d" % (entry["subtitle"], entry["topic"], entry["tier"])
    if kind == "python":
        meta += " · python/%s.py" % stem(entry)
    return (raw_latex("\\clearpage") + "\n## %s {#a%d}\n\n" % (md_escape(plain), entry["rank"])
            + raw_latex("\\markright{%s}" % latex_escape(plain))
            + "\n[%s]{.meta}\n" % md_escape(meta))


def topic_index(entries):
    lines = ["# Topic Index {#topic-index}", "", raw_latex("\\markboth{Topic Index}{}"),
             "The book is ordered by importance. This index groups the same entries by topic; "
             "every number is a link.", "",
             "| Topic | Entries |", "|:--------------------|:--------------------------------------"
             "----------------------------------|"]
    for topic in TOPIC_ORDER:
        items = []
        for e in entries:
            if e["topic"] == topic:
                items.append("#%d %s" % (e["rank"], md_escape(e["title"])))
        if items:
            lines.append("| %s | %s |" % (md_escape(topic), " · ".join(items)))
    return "\n".join(lines) + "\n"


def front_matter(subtitle):
    return "\n".join([
        "---",
        'title: "100 Algorithms"',
        'subtitle: "%s"' % subtitle,
        'date: "Ordered by importance for coding interviews"',
        "documentclass: scrbook",
        "classoption: [oneside, 11pt, openany]",
        "papersize: letter",
        "geometry: [margin=0.9in, headheight=14pt]",
        "toc: true",
        "toc-depth: 1",
        "colorlinks: true",
        "linkcolor: accent",
        "urlcolor: accent",
        "toccolor: ink",
        "---",
        "",
    ])


def tier_chapter(tier, name):
    heading = "Tier %d · %s" % (tier, name)
    return ("# %s {#tier%d}\n\n" % (heading, tier)
            + raw_latex("\\markboth{%s}{}" % latex_escape(heading))
            + "\n%s\n" % TIER_INTRO[tier])


def build_markdown(kind, entries, tiers):
    if kind == "pseudo":
        parts = [front_matter("in Pseudocode"), PSEUDO_INTRO, topic_index(entries)]
    else:
        parts = [front_matter("in Python"), PYTHON_INTRO, helpers_section(),
                 topic_index(entries)]
    current_tier = None
    for e in entries:
        if e["tier"] != current_tier:
            current_tier = e["tier"]
            parts.append(tier_chapter(current_tier, tiers[str(current_tier)]))
        parts.append(entry_heading(e, kind))
        if kind == "pseudo":
            parts.append(read_pseudo(e) + "\n")
        else:
            problem, code = read_python(e)
            prose = md_escape(problem).replace("-\\>", "→")
            parts.append(prose + "\n\n```python\n" + code + "\n```\n")
    return "\n".join(parts)


def write_list(entries, tiers):
    lines = ["100 Algorithms, in order of importance", "",
             "Books: algorithms_100/100_Algorithms_Pseudocode.pdf and "
             "algorithms_100/100_Algorithms_Python.pdf", ""]
    current_tier = None
    for e in entries:
        if e["tier"] != current_tier:
            current_tier = e["tier"]
            if len(lines) > 4:
                lines.append("")
            lines.append("Tier %d - %s" % (current_tier, tiers[str(current_tier)]))
        lines.append("%d. %s - %s [%s]" % (e["rank"], e["title"], e["subtitle"], e["topic"]))
    with open(LIST_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_pandoc(md_path, pdf_path):
    cmd = [
        "pandoc", md_path, "-o", pdf_path,
        "--from", "markdown-tex_math_dollars-raw_tex",
        "--pdf-engine=lualatex",
        "--syntax-definition", os.path.join(BUILD, "pseudo.xml"),
        "--syntax-highlighting", os.path.join(BUILD, "algo.theme"),
        "--lua-filter", os.path.join(BUILD, "filters.lua"),
        "--include-in-header", os.path.join(BUILD, "header.tex"),
    ]
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=BUILD)
    if run.returncode != 0:
        print(run.stderr)
        raise SystemExit("pandoc failed for " + os.path.basename(pdf_path))
    if run.stderr.strip():
        print(run.stderr.strip())


def main(argv):
    entries, tiers = load_manifest()
    partial = "--partial" in argv
    present = []
    for e in entries:
        ok = read_pseudo(e) is not None and read_python(e) is not None
        if ok:
            present.append(e)
        elif not partial:
            raise SystemExit("entry #%d %s is missing (use --partial)" % (e["rank"], e["slug"]))
    write_list(entries, tiers)
    outputs = [("pseudo", PSEUDO_PDF), ("python", PYTHON_PDF)]
    for kind, pdf in outputs:
        md_path = os.path.join(BUILD, "%s_book.md" % kind)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(build_markdown(kind, present, tiers))
        if "--md-only" not in argv:
            run_pandoc(md_path, pdf)
            print("wrote " + os.path.relpath(pdf, REPO))
    print("wrote " + os.path.relpath(LIST_TXT, REPO) + "; %d entries in the books" % len(present))


if __name__ == "__main__":
    main(sys.argv[1:])
