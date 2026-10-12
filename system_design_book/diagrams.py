"""Graphviz styling shared by the checker, the build and the preview tool.

A chapter's ```dot block holds only the body of a graph: nodes, edges, clusters and optional
graph attributes such as rankdir=TB. wrap() adds the book's defaults and expands class=NAME.

Preview every diagram of a chapter as PNG:
    python3 system_design_book/diagrams.py system_design_book/chapters/01_url_shortener.md OUT_DIR
"""
import os
import re
import subprocess
import sys

HEADER = """digraph G {
  graph [rankdir=LR, fontname="Helvetica Neue", fontsize=10, nodesep=0.3, ranksep=0.45,
         pad=0.08, bgcolor="transparent", newrank=true];
  node  [fontname="Helvetica Neue", fontsize=10, shape=box, style="rounded,filled",
         fillcolor="#EEF2FB", color="#1F3A93", penwidth=1.1, margin="0.12,0.06", height=0.4];
  edge  [fontname="Helvetica Neue", fontsize=8.5, color="#4B5563", fontcolor="#374151",
         arrowsize=0.7, penwidth=0.9];
"""

CLASSES = {
    "client": 'shape=box, style="rounded,filled", fillcolor="#FFFFFF", color="#6B7280"',
    "service": 'shape=box, style="rounded,filled", fillcolor="#EEF2FB", color="#1F3A93"',
    "edge": 'shape=box, style="rounded,filled", fillcolor="#E0F2FE", color="#0369A1"',
    "cache": 'shape=box, style="rounded,filled", fillcolor="#E8F5E9", color="#2E7D32"',
    "store": 'shape=cylinder, style="filled", fillcolor="#FDF3E7", color="#B45309"',
    "queue": 'shape=cds, style="filled", fillcolor="#F3E8FD", color="#7E22CE"',
    "worker": 'shape=box, style="rounded,filled", fillcolor="#FEF9C3", color="#A16207"',
    "external": 'shape=box, style="rounded,dashed,filled", fillcolor="#FFFFFF", color="#6B7280"',
}
CLASS_RE = re.compile(r'\bclass\s*=\s*"?([A-Za-z_]+)"?')


def wrap(body):
    def sub(m):
        name = m.group(1)
        if name not in CLASSES:
            raise ValueError("unknown diagram class: " + name)
        return CLASSES[name]
    return HEADER + CLASS_RE.sub(sub, body) + "\n}\n"


def render(body, fmt, out_path, dpi=None):
    """Render to a file; returns (ok, stderr)."""
    cmd = ["dot", "-T" + fmt, "-o", out_path]
    if dpi:
        cmd.insert(1, "-Gdpi=%d" % dpi)
    run = subprocess.run(cmd, input=wrap(body), capture_output=True, text=True)
    return run.returncode == 0, run.stderr.strip()


def layout_stats(body):
    """(width_in, height_in, nodes, edges) from dot's plain output."""
    run = subprocess.run(["dot", "-Tplain"], input=wrap(body), capture_output=True, text=True)
    if run.returncode != 0:
        raise ValueError(run.stderr.strip())
    lines = run.stdout.split("\n")
    head = lines[0].split()
    nodes = 0
    edges = 0
    for line in lines:
        if line.startswith("node "):
            nodes += 1
        elif line.startswith("edge "):
            edges += 1
    return float(head[2]), float(head[3]), nodes, edges


def dot_blocks(markdown):
    blocks = []
    for m in re.finditer(r"^```dot\n(.*?)^```", markdown, re.S | re.M):
        blocks.append(m.group(1))
    return blocks


if __name__ == "__main__":
    chapter, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    text = open(chapter, encoding="utf-8").read()
    stem = os.path.splitext(os.path.basename(chapter))[0]
    for i, body in enumerate(dot_blocks(text), 1):
        path = os.path.join(out_dir, "%s_diagram%d.png" % (stem, i))
        ok, err = render(body, "png", path, dpi=110)
        w, h, n, e = layout_stats(body)
        print("%s: %s  %.1f x %.1f in, %d nodes, %d edges %s"
              % (path, "ok" if ok else "FAILED", w, h, n, e, err))
