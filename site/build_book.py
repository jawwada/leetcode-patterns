"""Assemble the Intuition Journey book from book/<topic>/*.md + site/problems.json.

Outputs:
  site/book.html        page fragment for publishing
  site/book_index.html  standalone page for local reading
Validates: headings (exact order), drawing width <= 64 cols, no tabs, every ordered slug has a file,
every problem in the topic appears in order.json.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
SITE = os.path.join(ROOT, "site")

# learning path: each chapter builds on the ones before it
CHAPTERS = [
    "arrays_hashing", "two_pointers", "sliding_window", "stack", "queues", "binary_search", "linked_list",
    "trees", "tries", "heap", "backtracking", "graphs", "intervals", "greedy",
    "bit_manipulation", "math_geometry", "strings", "design", "dynamic_programming",
]

PROBLEM_HEADINGS = [
    "The problem", "What the problem is really asking", "Do it by hand first", "The first honest attempt",
    "The turning point", "Watch it work", "Why it is correct", "Cost",
    "Variations you will meet", "What to carry forward",
]
BG_HEADINGS = [
    "Why this chapter exists", "What it is", "Operations and what they cost", "The invariant",
    "How to picture it", "Advanced patterns", "Signals in a problem statement", "Python toolbox",
    "Mistakes people make", "The journey ahead",
]


def headings(md):
    return [m.group(1).strip() for m in re.finditer(r"^## (.+)$", md, re.M)]


def split_statement(md):
    """Return (markdown of the '## The problem' section body, md with that section removed).

    The statement lives in the .md so the file reads completely on GitHub; the page renders it in its own
    box under the title, so it is cut out of the prose body here."""
    m = re.search(r"^## The problem\n([\s\S]*?)(?=^## )", md, re.M)
    if not m:
        return "", md
    return m.group(1).strip(), md[:m.start()] + md[m.end():]


def check_md(path, md, expected, errors):
    got = headings(md)
    if got != expected:
        errors.append(f"{path}: headings differ\n   got      {got}\n   expected {expected}")
    if not md.startswith("# "):
        errors.append(f"{path}: must start with a '# Title' line")
    fence = None  # None = outside; else the fence's language ('' or 'text' = drawing)
    for i, line in enumerate(md.split("\n"), 1):
        if line.startswith("```"):
            fence = None if fence is not None else line[3:].strip().lower()
            continue
        if "\t" in line:
            errors.append(f"{path}:{i}: tab character")
        if fence in ("", "text", "txt") and len(line) > 64:
            errors.append(f"{path}:{i}: drawing line is {len(line)} cols (max 64)")


def main() -> int:
    problems = {p["slug"]: p for p in json.load(open(os.path.join(SITE, "problems.json")))}
    errors, chapters = [], []
    for topic in CHAPTERS:
        d = os.path.join(BOOK, topic)
        if not os.path.isdir(d):
            errors.append(f"missing chapter folder book/{topic}")
            continue
        try:
            order = json.load(open(os.path.join(d, "order.json")))
        except FileNotFoundError:
            errors.append(f"book/{topic}/order.json missing")
            continue
        bg_path = os.path.join(d, "00_background.md")
        if not os.path.exists(bg_path):
            errors.append(f"{bg_path} missing")
            continue
        bg = open(bg_path).read()
        check_md(bg_path, bg, BG_HEADINGS, errors)

        in_topic = {s for s, p in problems.items() if p["topic"] == topic}
        ordered = [o["slug"] for o in order.get("order", [])]
        if set(ordered) != in_topic or len(ordered) != len(set(ordered)):
            errors.append(f"book/{topic}/order.json: slugs mismatch. missing={sorted(in_topic - set(ordered))} "
                          f"extra={sorted(set(ordered) - in_topic)} dupes={len(ordered) - len(set(ordered))}")
        sections = []
        for o in order.get("order", []):
            slug = o["slug"]
            path = os.path.join(d, f"{slug}.md")
            if not os.path.exists(path):
                errors.append(f"{path} missing")
                continue
            md = open(path).read()
            check_md(path, md, PROBLEM_HEADINGS, errors)
            statement, md = split_statement(md)
            if not statement:
                errors.append(f"{path}: '## The problem' section is empty")
            p = problems.get(slug)
            if not p:
                continue
            bf = p.get("brute_force") or {}
            sections.append({
                "slug": slug, "title": p["title"], "leetcode": p["leetcode"], "difficulty": p["difficulty"],
                "pattern": p["pattern"], "file": p["file"], "problem": p["problem"], "statement": statement, "why_here": o.get("why_here", ""), "md": md,
                "code": p["code"], "time": p["complexity"]["time"], "space": p["complexity"]["space"],
                "brute_code": bf.get("code", ""), "brute_time": bf.get("time", ""), "brute_space": bf.get("space", ""),
            })
        see_also = []
        for o in order.get("see_also", []):
            p = problems.get(o["slug"])
            if not p or p["topic"] == topic:
                errors.append(f"book/{topic}/order.json: see_also slug {o['slug']} missing or in this chapter")
                continue
            see_also.append({"slug": o["slug"], "title": p["title"], "difficulty": p["difficulty"],
                             "topic": p["topic"], "why_here": o.get("why_here", "")})
        chapters.append({"topic": topic, "title": order.get("title", topic), "background": bg,
                         "sections": sections, "see_also": see_also})

    if errors:
        print("\n".join(errors[:60]))
        if len(errors) > 60:
            print(f"... {len(errors) - 60} more")
        return 1

    data = {"chapters": chapters}
    template = open(os.path.join(SITE, "book_template.html")).read()
    payload = json.dumps(data).replace("</", "<\\/")
    fragment = template.replace("__DATA__", payload)
    open(os.path.join(SITE, "book.html"), "w").write(fragment)
    full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + fragment + "\n</html>\n")
    open(os.path.join(SITE, "book_index.html"), "w").write(full)
    n = sum(len(c["sections"]) for c in chapters)
    words = sum(len(re.sub(r"```[\s\S]*?```", "", s["md"]).split()) for c in chapters for s in c["sections"])
    words += sum(len(re.sub(r"```[\s\S]*?```", "", c["background"]).split()) for c in chapters)
    print(f"built book: {len(chapters)} chapters, {n} readings, ~{words:,} words -> site/book_index.html ({len(full)//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
