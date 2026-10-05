#!/usr/bin/env python3
"""Build the Brute to Optimal companion from companion/<topic>/<slug>.py (format: site/companion/SPEC.md).

    python3 site/build_companion.py --check FILE...   # validate files (used by the writers)
    python3 site/build_companion.py                   # validate everything, build site/companion.html
                                                      # (publishable fragment) + site/companion_index.html

Per file: split at the section markers; the brute tab = imports + helpers + brute force + its demo, the
optimal tab = imports + helpers + optimal + its demo; both must run (exit 0, under 10 s) and print the
same lines; the docstring header must name the problem; the slug must be in site/companion/selection.json.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
CODE = os.path.join(ROOT, "companion")
MARKERS = ["helpers", "brute force", "optimal", "try the brute force", "try the optimal"]
SELECTION = json.load(open(os.path.join(SITE, "companion", "selection.json")))
FUNDAMENTALS = json.load(open(os.path.join(SITE, "companion", "fundamentals.json")))
FUND_MARKERS = ["helpers", "algorithm", "try it"]
CHAPTER_TITLES = {t: json.load(open(os.path.join(ROOT, "book", t, "order.json"))).get("title", t) for t in SELECTION}


class Bad(Exception):
    pass


def run(code, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return "timeout", "", ""
    finally:
        os.unlink(path)


def split(text, markers=MARKERS):
    pat = re.compile(r"^# --- (" + "|".join(re.escape(m) for m in markers) + r") ---\s*$", re.M)
    hits = list(pat.finditer(text))
    if not hits:
        raise Bad("no section markers")
    order = [h.group(1) for h in hits]
    if order != [m for m in markers if m in order] or len(order) != len(set(order)):
        raise Bad(f"sections out of order or repeated: {order}")
    for req in markers[1:]:
        if req not in order:
            raise Bad(f"missing section '# --- {req} ---'")
    head = text[: hits[0].start()]
    secs = {}
    for i, h in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        secs[h.group(1)] = text[h.end():end].strip("\n")
    return head, secs


def parse_doc(head):
    m = re.match(r'\s*"""(.*?)"""', head, re.S)
    if not m:
        raise Bad("missing module docstring")
    lines = m.group(1).strip("\n").split("\n")
    tm = re.match(r"(.+?)\s*(?:\(LeetCode\s+(\d+)\))?\s*-\s*(Easy|Medium|Hard|Fundamentals)\s*$", lines[0].strip())
    if not tm or (tm.group(3) != "Fundamentals" and not tm.group(2)):
        raise Bad(f"first docstring line must be '<Title> (LeetCode n) - <Difficulty>' or '<Title> - Fundamentals', got {lines[0]!r}")
    chapter = re.search(r"^Chapter:\s*(\S+)", m.group(1), re.M)
    pattern = re.search(r"^(?:Pattern|Key operations):\s*(.+)$", m.group(1), re.M)
    if not chapter or not pattern:
        raise Bad("docstring needs 'Chapter:' and 'Pattern:' (or 'Key operations:') lines")
    body = [l for l in lines[1:] if not l.startswith(("Chapter:", "Pattern:", "Key operations:"))]
    statement = "\n".join(body).strip()
    if not statement:
        raise Bad("docstring has no problem statement")
    imports = "\n".join(l for l in head[m.end():].split("\n") if l.strip()).strip()
    if any(not l.startswith(("import ", "from ")) for l in imports.split("\n") if l):
        raise Bad("only import lines may follow the docstring before the first marker")
    return {"title": tm.group(1).strip(), "leetcode": int(tm.group(2)) if tm.group(2) else None, "difficulty": tm.group(3),
            "chapter": chapter.group(1), "pattern": pattern.group(1).strip(), "statement": statement, "imports": imports}


def tabs(meta, secs):
    def build(code, demo):
        parts = [meta["imports"], secs.get("helpers", ""), code, "# --- try it: change the inputs and run ---\n" + demo]
        return "\n\n\n".join(p for p in parts if p) + "\n"
    return build(secs["brute force"], secs["try the brute force"]), build(secs["optimal"], secs["try the optimal"])


STYLE = [(r"\blambda\b", "lambda"), (r"\bsetdefault\b", "setdefault"), (r"\bdefaultdict\b", "defaultdict"),
         (r"\bCounter\b", "Counter"), (r":=", "walrus"), (r"^class Solution\b", "class Solution"),
         (r"\bany\(|\ball\(", "any()/all()"), (r"->\s*\w+:\s*$", "type hint")]


def check_style(code):
    for bad, why in STYLE:
        if re.search(bad, code, re.M):
            raise Bad(f"style: {why} is not allowed (see SPEC.md)")


def check_fund_file(path):
    text = open(path).read()
    name = os.path.splitext(os.path.basename(path))[0]
    area = os.path.basename(os.path.dirname(path))
    if name not in FUNDAMENTALS.get(area, []):
        raise Bad(f"fundamentals/{area}/{name} is not in site/companion/fundamentals.json")
    if "\t" in text:
        raise Bad("tab character")
    head, secs = split(text, FUND_MARKERS)
    meta = parse_doc(head)
    if meta["difficulty"] != "Fundamentals" or meta["chapter"] != "fundamentals/" + area:
        raise Bad(f"docstring must say '- Fundamentals' and 'Chapter: fundamentals/{area}'")
    if not re.search(r"^(def|class) ", secs["algorithm"], re.M):
        raise Bad("section 'algorithm' defines no function or class")
    if "print(" not in secs["try it"]:
        raise Bad("section 'try it' prints nothing")
    check_style(secs["algorithm"] + "\n" + secs.get("helpers", ""))
    py = "\n\n\n".join(p for p in [meta["imports"], secs.get("helpers", ""), secs["algorithm"],
                                    "# --- try it: change the inputs and run ---\n" + secs["try it"]] if p) + "\n"
    rc, out, err = run(py)
    if rc != 0:
        raise Bad(f"file failed (rc={rc}): {err.strip().splitlines()[-1:]}")
    if not out.strip():
        raise Bad("prints nothing")
    n = len([l for l in secs["algorithm"].split("\n") if l.strip()])
    if n > 70:
        raise Bad(f"algorithm section is {n} lines (max 70)")
    return {"kind": "fund", "id": name, "area": area, **meta, "key_ops": meta["pattern"], "py": py, "expected": out}


def check_file(path):
    if os.sep + "fundamentals" + os.sep in path:
        return check_fund_file(path)
    text = open(path).read()
    slug = os.path.splitext(os.path.basename(path))[0]
    topic = os.path.basename(os.path.dirname(path))
    if slug not in SELECTION.get(topic, []):
        raise Bad(f"{topic}/{slug} is not in site/companion/selection.json")
    if "\t" in text:
        raise Bad("tab character")
    head, secs = split(text)
    meta = parse_doc(head)
    if meta["chapter"] != topic:
        raise Bad(f"Chapter: {meta['chapter']} but file is under {topic}")
    for name in ("brute force", "optimal"):
        if not re.search(r"^(def|class) ", secs[name], re.M):
            raise Bad(f"section '{name}' defines no function or class")
    if not re.search(r"^(def|class) brute_force\b|^class BruteForce\b", secs["brute force"], re.M):
        raise Bad("the brute force must be `def brute_force(...)` or `class BruteForce`")
    for name in ("try the brute force", "try the optimal"):
        if "print(" not in secs[name]:
            raise Bad(f"section '{name}' prints nothing")
    check_style(secs["brute force"] + "\n" + secs["optimal"] + "\n" + secs.get("helpers", ""))
    brute_py, opt_py = tabs(meta, secs)
    rb, ob, eb = run(brute_py)
    ro, oo, eo = run(opt_py)
    if rb != 0:
        raise Bad(f"brute tab failed (rc={rb}): {eb.strip().splitlines()[-1:] }")
    if ro != 0:
        raise Bad(f"optimal tab failed (rc={ro}): {eo.strip().splitlines()[-1:]}")
    if ob != oo:
        raise Bad(f"the two demos print different lines:\n  brute:   {ob[:400]!r}\n  optimal: {oo[:400]!r}")
    rc, out, err = run(text)
    if rc != 0:
        raise Bad(f"whole file failed (rc={rc}): {err.strip().splitlines()[-1:]}")
    n = lambda s: len([l for l in s.split("\n") if l.strip()])
    if n(secs["brute force"]) > 45 or n(secs["optimal"]) > 60:
        raise Bad(f"too long: brute {n(secs['brute force'])} lines, optimal {n(secs['optimal'])} lines (max 45 / 60)")
    return {"slug": slug, "topic": topic, **meta, "brute_py": brute_py, "opt_py": opt_py, "expected": oo,
            "brute_code": secs["brute force"], "opt_code": secs["optimal"]}


def main():
    args = sys.argv[1:]
    if args and args[0] == "--check":
        bad = 0
        for a in args[1:]:
            try:
                check_file(os.path.abspath(a))
                print(f"ok    {a}")
            except Bad as e:
                bad += 1
                print(f"FAIL  {a}: {e}")
        return 1 if bad else 0
    from build_companion_page import build_page  # the page assembly lives next to this file
    return build_page(check_file)


if __name__ == "__main__":
    sys.exit(main())
