"""Build one independently runnable notebook per source in topics/manifest.json.

python practice/playbook/build_topics.py
python practice/playbook/build_topics.py --out-dir /tmp/playbook --no-exec
"""
import argparse
import json
import re
from pathlib import Path

import build

SOURCES = Path(__file__).resolve().parent / "topics"


def check_topic_links(notebooks):
    """Fail for missing notebook targets or explicit anchors in the active set."""
    anchors = {
        filename: {anchor for cell in cells if cell["kind"] == "markdown"
                   for anchor in re.findall(r'<a id="([\w-]+)"></a>', cell["src"])}
        for filename, cells in notebooks.items()
    }
    errors = []
    for filename, cells in notebooks.items():
        for cell in cells:
            if cell["kind"] != "markdown":
                continue
            for target in re.findall(r"\]\(([^)]+)\)", cell["src"]):
                if "://" in target or target.startswith("../"):
                    continue
                file, _, anchor = target.partition("#")
                if file and not file.endswith(".ipynb"):
                    continue
                destination = file or filename
                if destination not in anchors or (anchor and anchor not in anchors[destination]):
                    errors.append(f"{filename}: {target}")
    if errors:
        raise ValueError("Broken topic links:\n" + "\n".join(sorted(set(errors))))


def build_all(run=True, out_dir=None):
    out_dir = Path(out_dir) if out_dir else build.OUT_DIR
    manifest = json.loads((SOURCES / "manifest.json").read_text())
    notebooks = {}
    for number, item in enumerate(manifest):
        parsed = build.parse((SOURCES / item["source"]).read_text())
        body = [{"kind": kind, "src": source, "where": item["source"]}
                for kind, source in parsed]
        all_markdown = "\n".join(cell["src"] for cell in body if cell["kind"] == "markdown")
        anchor = item["topic_anchor"]
        marker = "" if f'<a id="{anchor}"></a>' in all_markdown else f'<a id="{anchor}"></a>\n'
        navigation = ["[Topic index](00_Topic_Index.ipynb#notebooks)",
                      f'[A–Z problem finder]({manifest[-1]["file"]}#finder)']
        if number:
            previous = manifest[number - 1]
            navigation.insert(0, f'← [{previous["title"]}]({previous["file"]})')
        if number + 1 < len(manifest):
            following = manifest[number + 1]
            navigation.append(f'[{following["title"]}]({following["file"]}) →')
        has_code = any(cell["kind"] == "code" for cell in body)
        instruction = ("Run the setup cell first, then the remaining cells from top to bottom. "
                       "This notebook has its own imports and helpers.") if has_code else "Choose a linked lesson to open its runnable examples."
        header = (f'<!-- notebook-header -->\n<a id="top"></a>\n{marker}\n'
                  f'# {number}. {item["title"]}\n\n'
                  f'*LeetCode Playbook · topic notebook {number}* · {item["title"]}.\n\n'
                  + " · ".join(navigation) + "\n\n" + instruction)
        cells = [{"kind": "markdown", "src": header, "where": "header"}]
        if has_code:
            cells.append({"kind": "code", "src": build.SETUP, "where": "setup"})
        cells.extend(body)
        notebooks[item["file"]] = cells

    check_topic_links(notebooks)
    code_count = 0
    for filename, cells in notebooks.items():
        _, count = build.to_notebook(cells, out_dir / filename, run)
        code_count += count
        print(f"wrote {filename}: {count} code cells")
    print(f"{len(notebooks)} notebooks; {code_count} code cells; all topic links resolve.")
    return len(notebooks), code_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-exec", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    build_all(not args.no_exec, args.out_dir)
