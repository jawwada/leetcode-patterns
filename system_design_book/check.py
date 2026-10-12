"""Validate system design chapters against SPEC.md.

Usage: python3 system_design_book/check.py [rank ...]   (no args: every chapter present)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diagrams  # noqa: E402

SECTIONS = ["Requirements", "Estimates", "API", "Data Model", "Architecture", "Deep Dives",
            "Scaling and Bottlenecks", "Failure Modes", "Trade-offs and Alternatives",
            "What Interviewers Probe"]
NEEDS_CODE = {"Estimates": "text", "API": "text", "Data Model": "text", "Architecture": "dot"}
MAX_COLS = 80
CODE_UNICODE = set("←→↑↓↔≤≥≠≈∞×·…²³√⌊⌋✓✗▲▼●○µ±─│┌┐└┘├┤┬┴┼═║╔╗╚╝")
PROSE_UNICODE = CODE_UNICODE | set("—–‘’“”é")


def load():
    manifest = json.load(open(os.path.join(HERE, "manifest.json")))["designs"]
    index = json.load(open(os.path.join(HERE, "algorithms_index.json")))
    return manifest, index


def parse(body):
    """Split into items: ('h3', title), ('h4', title), ('para', text), ('code', lang, text)."""
    items, para = [], []
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            if para:
                items.append(("para", "\n".join(para)))
                para = []
            lang = line[3:].strip()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            items.append(("code", lang, "\n".join(code)))
            i += 1
            continue
        if line.startswith("#"):
            if para:
                items.append(("para", "\n".join(para)))
                para = []
            level = len(line) - len(line.lstrip("#"))
            items.append(("h%d" % level, line[level:].strip()))
        elif line.strip() == "":
            if para:
                items.append(("para", "\n".join(para)))
                para = []
        else:
            para.append(line)
        i += 1
    if para:
        items.append(("para", "\n".join(para)))
    return items


def check_chapter(entry, path, index):
    errs, warns = [], []
    if not os.path.exists(path):
        return ["missing " + os.path.relpath(path, HERE)], warns
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return ["no front matter"], warns
    front = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    if front.get("rank") != str(entry["rank"]) or front.get("slug") != entry["slug"]:
        errs.append("front matter rank/slug do not match manifest")
    items = parse(m.group(2).strip())

    h3 = [it[1] for it in items if it[0] == "h3"]
    if h3 != SECTIONS:
        errs.append("### sections must be exactly, in order: %s; got %s" % (SECTIONS, h3))
    for it in items:
        if it[0] in ("h1", "h2", "h5", "h6"):
            errs.append("only ### template sections and #### deep dives: " + it[1])
    if not items or items[0][0] != "para":
        errs.append("open with a paragraph (the system and its crux) before ### Requirements")

    section, content = None, {}
    deep_dives = 0
    for it in items:
        if it[0] == "h3":
            section = it[1]
            content[section] = []
            continue
        if it[0] == "h4":
            if section != "Deep Dives":
                errs.append("#### only inside Deep Dives: " + it[1])
            deep_dives += 1
            continue
        if section is not None:
            content[section].append(it)
    if not 2 <= deep_dives <= 3:
        errs.append("Deep Dives needs 2 or 3 #### subsections, found %d" % deep_dives)
    for name in SECTIONS:
        got = content.get(name, [])
        if not any(it[0] == "para" for it in got):
            errs.append("section %s needs prose" % name)
        want = NEEDS_CODE.get(name)
        if want and not any(it[0] == "code" and it[1] == want for it in got):
            errs.append("section %s needs a ```%s block" % (name, want))

    last = items[-1] if items else None
    if not last or last[0] != "para" or not last[1].startswith("*Algorithms:*"):
        errs.append("last line must be '*Algorithms:* #N Title · ...'")
    else:
        parts = last[1][len("*Algorithms:*"):].strip().split(" · ")
        if not 1 <= len(parts) <= 6:
            errs.append("*Algorithms:* needs 1 to 6 entries")
        for part in parts:
            mm = re.match(r"^#(\d+) (.+)$", part)
            if not mm:
                errs.append("bad algorithms item: " + part)
            elif index.get(mm.group(1)) != mm.group(2):
                errs.append("algorithm #%s is titled %r, not %r"
                            % (mm.group(1), index.get(mm.group(1)), mm.group(2)))

    words = 0
    for it in items:
        if it[0] == "para":
            t = it[1]
            if t.startswith("*Algorithms:*"):
                continue
            words += len(t.split())
            for line in t.split("\n"):
                s = line.lstrip()
                if s.startswith("|") or s.startswith("- ") or s.startswith("* ") \
                        or s.startswith("+ ") or re.match(r"^\d+[.)] ", s):
                    errs.append("no lists or tables in prose: " + s[:50])
            if t.startswith("**"):
                errs.append("no bold labels: " + t[:40])
            for ch in t:
                if ord(ch) > 127 and ch not in PROSE_UNICODE:
                    errs.append("prose char not allowed: %r" % ch)
            for mm in re.finditer(r"Chapter (\d+)", t):
                if not 1 <= int(mm.group(1)) <= 50:
                    errs.append("no Chapter " + mm.group(1))
            for mm in re.finditer(r"(?<![\w&])#(\d+)", t):
                if mm.group(1) not in index:
                    errs.append("no algorithm entry #" + mm.group(1))
        elif it[0] == "code":
            lang, code = it[1], it[2]
            if lang not in ("text", "dot"):
                errs.append("code blocks are ```text or ```dot, not " + lang)
                continue
            if lang == "text":
                for n, line in enumerate(code.split("\n"), 1):
                    if len(line) > MAX_COLS:
                        errs.append("text block line longer than %d: %s" % (MAX_COLS, line[:40]))
                    for ch in line:
                        if ord(ch) > 127 and ch not in CODE_UNICODE:
                            errs.append("code char not allowed: %r" % ch)
            else:
                if re.search(r"^\s*(strict\s+)?(di)?graph\b", code, re.M):
                    errs.append("```dot holds only the graph body (no digraph wrapper)")
                    continue
                try:
                    w, h, nodes, edges = diagrams.layout_stats(code)
                except ValueError as e:
                    errs.append("diagram does not render: %s" % str(e)[:200])
                    continue
                scale = min(1.0, 6.6 / w) if w > 0 else 1.0
                if w > 12:
                    errs.append("diagram is %.1f in wide; it would print too small" % w)
                elif w > 9:
                    warns.append("diagram is %.1f in wide (prints at %.0f%%)" % (w, scale * 100))
                if h * scale > 8.5:
                    errs.append("diagram is %.1f in tall on the page" % (h * scale))
                if nodes > 32:
                    errs.append("diagram has %d nodes (max 32)" % nodes)
    if words < 1500 or words > 3400:
        warns.append("prose is %d words (aim 1800-3000)" % words)
    return errs, warns


def main(argv):
    manifest, index = load()
    if argv:
        wanted = set(int(a) for a in argv)
        entries = [e for e in manifest if e["rank"] in wanted]
    else:
        entries = []
        for e in manifest:
            if os.path.exists(os.path.join(HERE, "chapters", "%02d_%s.md" % (e["rank"], e["slug"]))):
                entries.append(e)
    failed = 0
    for e in entries:
        path = os.path.join(HERE, "chapters", "%02d_%s.md" % (e["rank"], e["slug"]))
        errs, warns = check_chapter(e, path, index)
        print("%-3d %-32s %s" % (e["rank"], e["slug"], "OK" if not errs else "FAIL"))
        for msg in errs:
            print("      error: " + msg)
        for msg in warns:
            print("      warn:  " + msg)
        if errs:
            failed += 1
    print("%d checked, %d failed" % (len(entries), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
