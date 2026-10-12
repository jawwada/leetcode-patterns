#!/usr/bin/env python3
"""
Validate every practice script and build practice/bank.json for the drill artifact.

    python3 practice/build_bank.py                 # check everything, write bank.json and the index
    python3 practice/build_bank.py --check PATH... # check only these files (agents use this)

For each script (see SPEC.md):
  1. run it with --quiet: must exit 0 and print "ok"
  2. split it at the section markers; strip the log(...) lines from the optimal section
  3. the shown program = helpers + stripped optimal + demo (+ print(demo())); it must compile and be
     15-45 non-blank lines (basics: 10-45)
  4. the stripped optimal must still pass the tests
  5. every BUGS variant: its "replace" line is unique in the shown program, the buggy program FAILS the
     tests (assert/raise/timeout), and each decoy's "line" is unique and differs from the bug line
Problems also need a README.md with the required headings.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS = ROOT / "problems"
BASICS = ROOT / "basics"
MARKERS = ["helpers", "brute force", "optimal", "demo", "tests", "bugs"]
README_HEADINGS = ["## Problem", "## Example", "## Brute force", "## From brute force to optimal",
                   "## Intuition", "## Walkthrough", "## Steps", "## Complexity", "## Pitfalls"]
TIMEOUT = 8


class Bad(Exception):
    pass


def run_py(src: str, timeout=TIMEOUT):
    """Run python source in a subprocess. Returns (returncode, stdout, stderr); returncode 'timeout' on hang."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(src)
        path = f.name
    try:
        p = subprocess.run([sys.executable, path, "--quiet"], capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return "timeout", "", ""
    finally:
        Path(path).unlink(missing_ok=True)


def split_sections(text: str):
    """Return (header, {marker: body}) where header is everything before the first marker."""
    pat = re.compile(r"^# --- (" + "|".join(re.escape(m) for m in MARKERS) + r") ---\s*$", re.M)
    hits = list(pat.finditer(text))
    if not hits:
        raise Bad("no section markers found")
    header = text[: hits[0].start()]
    sections = {}
    for i, h in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[h.end():end]
        # the bugs section ends where the __main__ block starts
        if h.group(1) == "bugs":
            m = re.search(r"^if __name__ == .__main__.:", body, re.M)
            if m:
                body = body[: m.start()]
        sections[h.group(1)] = body.strip("\n") + "\n"
    for req in ["optimal", "demo", "tests", "bugs"]:
        if req not in sections:
            raise Bad(f"missing section '# --- {req} ---'")
    order = [h.group(1) for h in hits]
    if order != [m for m in MARKERS if m in order]:
        raise Bad(f"sections out of order: {order}")
    return header, sections


def strip_logs(code: str):
    out = []
    for line in code.split("\n"):
        s = line.strip()
        if s.startswith("log("):
            if not s.endswith(")") or s.count("(") != s.count(")"):
                raise Bad(f"multi-line log call is not allowed: {s[:60]}")
            continue
        if "log(" in s and not s.startswith("#") and not s.startswith('"""') and "def log" not in s:
            raise Bad(f"log( must be a standalone statement: {s[:60]}")
        out.append(line)
    # drop blank lines left where a log line sat between two blank lines
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip("\n") + "\n"


def header_imports(header: str):
    """Import lines from the header, minus sys (only needed for the --quiet flag)."""
    lines = []
    for line in header.split("\n"):
        s = line.strip()
        if (s.startswith("import ") or s.startswith("from ")) and s not in ("import sys",):
            lines.append(s)
    return "\n".join(lines)


def parse_docstring(text: str):
    m = re.match(r'\s*"""(.*?)"""', text, re.S)
    if not m:
        raise Bad("missing module docstring")
    doc = m.group(1).strip("\n")
    first = doc.split("\n")[0].strip()
    tm = re.match(r"(.+?)\s*(?:\(LeetCode\s+(\d+)\))?\s*-\s*(Medium-Hard|Medium|Basics|Easy|Hard)\s*$", first)
    if not tm:
        raise Bad(f"first docstring line must be '<Title> (LeetCode n) - <Difficulty>', got: {first!r}")
    area = re.search(r"^Area:\s*(.+)$", doc, re.M)
    keys = re.search(r"^Key operations:\s*(.+)$", doc, re.M)
    if not area or not keys:
        raise Bad("docstring needs 'Area:' and 'Key operations:' lines")
    body = doc.split("\n", 3)
    statement = "\n".join(l for l in doc.split("\n")[1:] if not l.startswith(("Area:", "Key operations:"))).strip()
    return {"title": tm.group(1).strip(), "leetcode": int(tm.group(2)) if tm.group(2) else None,
            "difficulty": tm.group(3), "area": area.group(1).strip(), "key_ops": keys.group(1).strip(),
            "statement": statement}


def load_bugs(path: Path):
    """Execute the module (not as __main__) and return its BUGS list."""
    ns = {}
    src = path.read_text()
    code = compile(src, str(path), "exec")
    saved = sys.argv
    sys.argv = [str(path), "--quiet"]
    try:
        exec(code, {"__name__": "practice_module", "__file__": str(path)}, ns)  # noqa: S102 (our own files)
    finally:
        sys.argv = saved
    bugs = ns.get("BUGS")
    if not isinstance(bugs, list):
        raise Bad("BUGS must be a list")
    return bugs


def find_unique(lines, target, what):
    idx = [i for i, l in enumerate(lines) if l.rstrip() == target.rstrip()]
    if len(idx) != 1:
        raise Bad(f"{what} must match exactly one line of the shown program, matched {len(idx)}: {target!r}")
    return idx[0]


def check_file(path: Path, kind: str):
    text = path.read_text()
    meta = parse_docstring(text)
    header, sec = split_sections(text)

    rc, out, err = run_py(text)
    if rc != 0 or "ok" not in out.split():
        raise Bad(f"script failed (rc={rc}): {err.strip()[-400:] or out[-200:]}")

    stripped = strip_logs(sec["optimal"])
    imports = header_imports(header)
    helpers = sec.get("helpers", "")
    shown = "\n\n".join(p for p in [imports, helpers.strip("\n"), stripped.strip("\n"), sec["demo"].strip("\n") + "\n\nprint(demo())"] if p) + "\n"
    n_shown = len([l for l in shown.split("\n") if l.strip()])
    lo = 15 if kind == "problem" else 10
    if not (lo <= n_shown <= 45):
        raise Bad(f"shown program is {n_shown} non-blank lines after stripping logs; need {lo}-45")
    try:
        compile(shown, "shown", "exec")
    except SyntaxError as e:
        raise Bad(f"shown program does not compile after stripping logs: {e}")

    def program(optimal_code):
        parts = [imports, "import random\nrandom.seed(0)", helpers, sec.get("brute force", ""), optimal_code, sec["tests"], "tests()\nprint('ok')"]
        return "\n".join(p.strip("\n") for p in parts if p.strip()) + "\n"

    rc, out, err = run_py(shown)
    if rc != 0:
        raise Bad(f"shown program does not run: {err.strip()[-300:]}")
    expected = out.strip()
    rc, out, err = run_py(program(stripped))
    if rc != 0 or "ok" not in out.split():
        raise Bad(f"stripped optimal fails the tests (rc={rc}): {err.strip()[-300:]}")

    bugs = load_bugs(path)
    need = 2 if kind == "problem" else 1
    if len(bugs) < need:
        raise Bad(f"need at least {need} BUGS variants, found {len(bugs)}")
    shown_lines = shown.split("\n")
    variants = []
    for k, b in enumerate(bugs):
        for key in ["replace", "with", "fix", "why", "decoys"]:
            if key not in b:
                raise Bad(f"BUGS[{k}] missing '{key}'")
        if b["replace"].rstrip() == b["with"].rstrip():
            raise Bad(f"BUGS[{k}] 'with' equals 'replace'")
        li = find_unique(shown_lines, b["replace"], f"BUGS[{k}].replace")
        if li >= len(shown_lines) - 1 or not (b["replace"].rstrip() in stripped):
            raise Bad(f"BUGS[{k}].replace must be a line of the optimal section")
        buggy_opt = stripped.replace(b["replace"].rstrip() + "\n", b["with"].rstrip() + "\n", 1)
        if buggy_opt == stripped:
            raise Bad(f"BUGS[{k}] replacement did not apply")
        try:
            compile(buggy_opt, "buggy", "exec")
        except SyntaxError as e:
            raise Bad(f"BUGS[{k}] buggy program has a syntax error ({e}); bugs must be semantic")
        rc, out, err = run_py(program(buggy_opt), timeout=5)
        if rc == 0 and "ok" in out.split():
            raise Bad(f"BUGS[{k}] is not caught by the tests: {b['with'].strip()!r}")
        # what the learner would see if they ran the buggy program as shown
        brc, bout, berr = run_py(shown.replace(b["replace"].rstrip() + "\n", b["with"].rstrip() + "\n", 1), timeout=5)
        if brc == "timeout":
            actual = "no output after 5 seconds (infinite loop)"
        elif brc != 0:
            last = [l for l in berr.strip().split("\n") if l.strip()]
            actual = "raises " + (last[-1][:120] if last else "an exception")
        else:
            actual = bout.strip() or "(prints nothing)"
        if len(b["decoys"]) != 3:
            raise Bad(f"BUGS[{k}] needs exactly 3 decoys")
        decoys, seen = [], {li}
        for d in b["decoys"]:
            di = find_unique(shown_lines, d["line"], f"BUGS[{k}] decoy")
            if di in seen:
                raise Bad(f"BUGS[{k}] decoys must name distinct lines other than the bug line")
            seen.add(di)
            decoys.append({"line": di + 1, "text": d["change"].strip()})
        variants.append({"line": li + 1, "buggy": b["with"].rstrip(), "original": b["replace"].rstrip(),
                         "fix": b["fix"].strip(), "why": b["why"].strip(), "decoys": decoys, "actual": actual,
                         "failure": "hangs" if rc == "timeout" else ("raises" if "AssertionError" not in err else "wrong answer")})

    readme = ""
    if kind == "problem":
        rp = path.parent / "README.md"
        if not rp.exists():
            raise Bad("README.md missing")
        readme = rp.read_text()
        missing = [h for h in README_HEADINGS if h not in readme]
        if missing:
            raise Bad(f"README.md missing headings: {missing}")

    rel = path.relative_to(ROOT.parent).as_posix()
    entry = {**meta, "id": path.parent.name if kind == "problem" else f"{path.parent.name}/{path.stem}",
             "kind": kind, "file": rel, "code": shown, "expected": expected, "full": text, "bugs": variants,
             "readme": readme}
    if kind == "basic":
        entry["area_readme"] = (path.parent / "README.md").read_text() if (path.parent / "README.md").exists() else ""
    return entry


def all_files():
    files = []
    if PROBLEMS.exists():
        files += [(p, "problem") for p in sorted(PROBLEMS.glob("*/solution.py"))]
    if BASICS.exists():
        files += [(p, "basic") for p in sorted(BASICS.glob("*/*.py"))]
    return files


def write_index(entries):
    lines = ["# Practice bank", "",
             "Traced, testable scripts for interview drilling. Run any file for a step-by-step trace, add `--quiet` for tests only.",
             "Format: [SPEC.md](SPEC.md). Build/validate: `python3 practice/build_bank.py`. The drill artifact reads `bank.json`.", "",
             "## Problems", "", "| # | Problem | Area | Difficulty | Key operations | Bugs |", "|---|---|---|---|---|---|"]
    for e in [x for x in entries if x["kind"] == "problem"]:
        lc = f" (LC {e['leetcode']})" if e["leetcode"] else ""
        d = Path(e["file"]).parent.as_posix()
        lines.append(f"| {e['id'].split('_')[0]} | [{e['title']}]({d}/README.md){lc} · [code]({e['file']}) | {e['area']} | {e['difficulty']} | {e['key_ops']} | {len(e['bugs'])} |")
    lines += ["", "## Basics", ""]
    by_area = {}
    for e in [x for x in entries if x["kind"] == "basic"]:
        by_area.setdefault(Path(e["file"]).parent.name, []).append(e)
    for area, es in sorted(by_area.items()):
        lines.append(f"### {area.replace('_', ' ')} · [README](basics/{area}/README.md)")
        lines.append("")
        for e in es:
            lines.append(f"- [{e['title']}]({e['file']}) · {e['key_ops']}")
        lines.append("")
    (ROOT / "README.md").write_text("\n".join(lines))


def main():
    args = sys.argv[1:]
    if args and args[0] == "--check":
        targets = []
        for a in args[1:]:
            p = Path(a).resolve()
            kind = "problem" if PROBLEMS in p.parents else "basic"
            if p.is_dir():
                targets += [(q, kind) for q in sorted(p.glob("**/*.py")) if q.name != "__init__.py"]
            else:
                targets.append((p, kind))
    else:
        targets = all_files()
    entries, bad = [], 0
    for path, kind in targets:
        try:
            entries.append(check_file(path, kind))
            print(f"ok    {path.relative_to(ROOT.parent)}  ({len(entries[-1]['bugs'])} bugs)")
        except Bad as e:
            bad += 1
            print(f"FAIL  {path.relative_to(ROOT.parent)}: {e}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"FAIL  {path.relative_to(ROOT.parent)}: {type(e).__name__}: {e}")
    if not (args and args[0] == "--check"):
        if bad:
            print(f"\n{bad} file(s) failed; bank.json not written")
            sys.exit(1)
        (ROOT / "bank.json").write_text(json.dumps(entries, ensure_ascii=False))
        write_index(entries)
        n_bugs = sum(len(e["bugs"]) for e in entries)
        print(f"\nbank.json: {len(entries)} entries, {n_bugs} bug variants")
    elif bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
