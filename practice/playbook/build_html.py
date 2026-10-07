"""
Render the built notebooks as one self-contained HTML page (the reading copy published as a claude.ai artifact).

    uv run python practice/playbook/build.py        # build and run the notebooks first
    python3 practice/playbook/build_html.py         # then write practice/playbook/artifact.html

The page embeds every cell of practice/LeetCode_Playbook/*.ipynb in order: markdown is rendered in the
browser (marked), code is highlighted (highlight.js) and shown with its saved output, and the sidebar
groups the sections by notebook. Code runs in the notebooks, not on the page.
Options: --dir <folder of notebooks> --out <page.html>
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NB_DIR = HERE.parent / "LeetCode_Playbook"
TEMPLATE = HERE / "page_template.html"
OUT = HERE / "artifact.html"


def arg(name, default):
    return Path(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def output_text(cell):
    parts = []
    for o in cell.get("outputs", []):
        if o["output_type"] == "stream":
            parts.append("".join(o["text"]))
        elif "text/plain" in o.get("data", {}):
            parts.append("".join(o["data"]["text/plain"]) + "\n")
    return "".join(parts).rstrip("\n")


def in_page(markdown):
    """Links between notebooks become links inside the one page."""
    markdown = re.sub(r"\]\([\w.-]+\.ipynb#([\w-]+)\)", r"](#\1)", markdown)
    return re.sub(r"\]\(([\w.-]+)\.ipynb\)", r"](#nb-\1)", markdown)


def main():
    files = sorted(arg("--dir", NB_DIR).glob("[0-9][0-9]_*.ipynb"))
    cells, titles, setup_shown, pending = [], {}, False, None
    for f in files:
        for c in json.loads(f.read_text())["cells"]:
            text = "".join(c["source"])
            if c["cell_type"] == "code":
                if text.startswith("# Setup:"):
                    if setup_shown:
                        continue                     # one setup cell is enough on the page
                    setup_shown = True
                cells.append({"t": "code", "s": text, "o": output_text(c)})
                continue
            if text.startswith("<!-- notebook-header -->"):
                title = re.search(r"^# \d+\. (.+)$", text, re.M).group(1)
                blurb = re.search(r"^\*LeetCode Playbook[^*]*\* · (.+)$", text, re.M).group(1)
                cells.append({"t": "part", "id": "nb-" + f.stem, "num": f.stem[:2], "title": title, "blurb": blurb})
                continue
            anchor = re.match(r'<a id="([\w-]+)"></a>', text)     # starts a new section
            if anchor:
                pending = anchor.group(1)
            if pending and pending not in titles and not text.startswith('<a id="notebooks">'):
                heading = re.search(r"^## (.+)$", text, re.M)
                if heading:
                    titles[pending] = heading.group(1).strip()
            cells.append({"t": "md", "s": in_page(text)})
    data = json.dumps({"cells": cells, "titles": titles}, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE.read_text().replace("__NOTEBOOK_JSON__", data)
    out = arg("--out", OUT)
    out.write_text(page)
    print(f"wrote {out}: {len(files)} notebooks, {len(cells)} cells, {len(page.encode()) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
