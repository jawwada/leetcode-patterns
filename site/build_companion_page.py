"""Assemble the Brute to Optimal page. Called by build_companion.py; not run directly.

Data per chapter (site/companion/selection.json order): title and intro from book/<topic>/order.json and
00_background.md, selected background sections, fundamentals from practice/basics, the problems.
Data per problem: metadata and runnable tabs from companion/<topic>/<slug>.py, the two paragraphs and
costs from site/problems.json, pseudocode from site/companion/pseudo/*.json.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BOOK = os.path.join(ROOT, "book")
BASICS = os.path.join(ROOT, "practice", "basics")
BG_SECTIONS = ["What it is", "Operations and what they cost", "The invariant", "Python toolbox", "Mistakes people make"]
AREA_TITLES = {"sorting": "Sorting", "searches": "Searching: binary search, BFS, DFS", "graphs": "Graph algorithms",
               "trees": "Trees and BSTs", "linked_lists": "Linked lists", "stacks": "Stacks and queues",
               "monotonic_stacks": "Monotonic stacks", "heaps": "Heaps", "tries": "Tries", "backtracking": "Backtracking",
               "bits": "Bits", "math": "Math", "matrices": "Matrices", "strings": "Strings"}
# which fundamentals areas a chapter page points to
CHAPTER_AREAS = {"arrays_hashing": ["sorting"], "two_pointers": ["strings"], "stack": ["stacks", "monotonic_stacks"],
                 "queues": ["stacks"], "binary_search": ["searches"], "linked_list": ["linked_lists"], "trees": ["trees"],
                 "tries": ["tries"], "heap": ["heaps"], "backtracking": ["backtracking"], "graphs": ["graphs", "searches"],
                 "bit_manipulation": ["bits"], "math_geometry": ["math", "matrices"], "strings": ["strings"]}


def md_sections(md):
    out, cur = {}, None
    for line in md.split("\n"):
        m = re.match(r"^## (.+)$", line)
        if m:
            cur = m.group(1).strip(); out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v).strip("\n") for k, v in out.items()}


def build_page(check_file):
    from build_companion import Bad, CODE, SELECTION, CHAPTER_TITLES, FUNDAMENTALS
    partial = "--partial" in sys.argv
    problems_json = {p["slug"]: p for p in json.load(open(os.path.join(SITE, "problems.json")))}
    pseudo = {}
    for f in glob.glob(os.path.join(SITE, "companion", "pseudo", "*.json")):
        pseudo.update(json.load(open(f)))
    errors, chapters, problems = [], [], {}
    fundamentals = []
    for area, names in FUNDAMENTALS.items():
        items = []
        for name in names:
            path = os.path.join(CODE, "fundamentals", area, name + ".py")
            if not os.path.exists(path):
                if not partial:
                    errors.append(f"missing {os.path.relpath(path, ROOT)}")
                continue
            try:
                e = check_file(path)
            except Bad as ex:
                errors.append(f"{os.path.relpath(path, ROOT)}: {ex}"); continue
            ps = pseudo.get(f"{area}/{name}")
            if not ps and not partial:
                errors.append(f"fundamentals {area}/{name}: no pseudocode"); continue
            items.append({"id": f"fund-{area}-{name}", "name": name, "area": area, "title": e["title"], "key_ops": e["key_ops"],
                          "statement": e["statement"], "py": e["py"], "pseudo": (ps or {}).get("algorithm")})
        fundamentals.append({"area": area, "id": "fund-" + area, "title": AREA_TITLES.get(area, area), "items": items})
    for topic, slugs in SELECTION.items():
        order = json.load(open(os.path.join(BOOK, topic, "order.json")))
        why = {o["slug"]: o.get("why_here", "") for o in order.get("order", [])}
        bg = md_sections(open(os.path.join(BOOK, topic, "00_background.md")).read())
        intro = bg.get("The chapter", "").split("Problems, in reading order:")[0].strip()
        background = [{"title": s, "md": bg[s]} for s in BG_SECTIONS if s in bg]
        kept = []
        for slug in slugs:
            path = os.path.join(CODE, topic, slug + ".py")
            if not os.path.exists(path):
                errors.append(f"missing {os.path.relpath(path, ROOT)}"); continue
            try:
                e = check_file(path)
            except Bad as ex:
                errors.append(f"{os.path.relpath(path, ROOT)}: {ex}"); continue
            pj = problems_json[slug]
            ps = pseudo.get(slug)
            if not ps:
                errors.append(f"{slug}: no pseudocode in site/companion/pseudo/"); continue
            problems[slug] = {
                "slug": slug, "topic": topic, "title": e["title"], "leetcode": e["leetcode"], "difficulty": e["difficulty"],
                "pattern": e["pattern"], "statement": e["statement"], "why_here": why.get(slug, ""),
                "lc_slug": re.sub(r"[^a-z0-9]+", "-", pj["title"].lower()).strip("-"),
                "brute": {"text": pj["brute_force"]["approach"], "time": pj["brute_force"]["time"], "space": pj["brute_force"]["space"],
                          "py": e["brute_py"], "pseudo": ps["brute"]},
                "opt": {"text": pj["optimization"], "time": pj["complexity"]["time"], "space": pj["complexity"]["space"],
                        "py": e["opt_py"], "pseudo": ps["optimal"]},
            }
            kept.append(slug)
        chapters.append({"topic": topic, "title": CHAPTER_TITLES[topic], "intro": intro, "background": background,
                         "areas": [a for a in CHAPTER_AREAS.get(topic, []) if a in FUNDAMENTALS], "problems": kept})
    if errors:
        print("\n".join(errors[:80]))
        if len(errors) > 80:
            print(f"... {len(errors) - 80} more")
        return 1
    data = {"chapters": chapters, "problems": problems, "fundamentals": fundamentals}
    template = open(os.path.join(SITE, "companion_template.html")).read()
    fragment = template.replace("__DATA__", json.dumps(data).replace("</", "<\\/"))
    open(os.path.join(SITE, "companion.html"), "w").write(fragment)
    full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + fragment + "\n</html>\n")
    open(os.path.join(SITE, "companion_index.html"), "w").write(full)
    write_readme(chapters, problems, fundamentals)
    nb = sum(len(f["items"]) for f in fundamentals)
    print(f"built companion: {len(chapters)} chapters, {len(problems)} problems, {nb} fundamentals -> site/companion_index.html ({len(full) // 1024} KB)")
    return 0


def write_readme(chapters, problems, fundamentals):
    lines = ["# Brute to Optimal: code files", "",
             "One runnable file per problem, in the book's reading order. Each file has a brute force and the optimal",
             "solution written in plain Python, and two demos at the bottom that print the same answers. Run a file with",
             "`python3 companion/<chapter>/<problem>.py`, change the inputs, run again. Format: `site/companion/SPEC.md`.",
             "`fundamentals/` holds the data structure operations and classic algorithms (sorting, BFS/DFS, topological",
             "sort, union find, Kruskal, Prim, Dijkstra, heaps, tries, KMP ...) in the same style, one algorithm per file.", "",
             "## Fundamentals", ""]
    for f in fundamentals:
        lines.append(f"### {f['title']}")
        lines.append("")
        for it in f["items"]:
            lines.append(f"- [{it['title']}](fundamentals/{f['area']}/{it['name']}.py) · {it['key_ops']}")
        lines.append("")
    lines += ["## Problems", ""]
    for c in chapters:
        lines.append(f"### {c['title']}")
        lines.append("")
        for k, s in enumerate(c["problems"], 1):
            p = problems[s]
            lines.append(f"{k}. [{p['title']}]({c['topic']}/{s}.py) · LC {p['leetcode']} · {p['difficulty']} · {p['pattern']}")
        lines.append("")
    open(os.path.join(ROOT, "companion", "README.md"), "w").write("\n".join(lines))
