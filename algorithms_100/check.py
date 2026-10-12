"""Validate entries of the 100 Algorithms books against SPEC.md.

Usage: python3 algorithms_100/check.py [rank ...] | --batch N   (no args: all present entries)
"""
import ast
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_COLS = 80
CODE_UNICODE = set("←→↑↓≤≥≠∞×·…²√⌊⌋✓✗▲▼●○─│┌┐└┘├┤┬┴┼")
PROSE_UNICODE = CODE_UNICODE | set("—–‘’“”é")
PSEUDO_BAD = [
    (re.compile(r"==|!=|<=|>="), "use = ≠ ≤ ≥ instead of == != <= >="),
    (re.compile(r"^\s*(if|for|while|return|else|elif|def|function|end|class)\b"),
     "keywords must be in CAPITALS (no END lines)"),
    (re.compile(r"^\s*(?!(IF|ELSE|WHILE|RETURN|FOR|AND|OR|NOT)\b)[A-Za-z_][\w.\[\], ]*\s=\s"),
     "assignment must use ←"),
    (re.compile(r":\s*(//.*)?$"), "no colon at the end of a line"),
    (re.compile(r"\t"), "no tabs"),
    (re.compile(r"[{}]\s*$"), "no braces for blocks"),
]
BANNED_NAMES = {"Counter", "defaultdict", "OrderedDict", "any", "all", "setdefault"}
ALLOWED_IMPORTS = {"collections", "heapq", "math", "random", "bisect"}


def load_manifest():
    with open(os.path.join(HERE, "manifest.json")) as f:
        return json.load(f)["algorithms"]


def split_blocks(body):
    """Return a list of ('para', text) and ('code', lang, text) items."""
    items, lines, i = [], body.split("\n"), 0
    para = []
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
        if line.strip() == "":
            if para:
                items.append(("para", "\n".join(para)))
                para = []
        else:
            para.append(line)
        i += 1
    if para:
        items.append(("para", "\n".join(para)))
    return items


def check_pseudo(entry, path):
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
    items = split_blocks(m.group(2).strip())
    kinds = []
    for it in items:
        kinds.append(it[0] if it[0] == "para" else it[1])
    if "pseudo" not in kinds or kinds.count("pseudo") != 1:
        errs.append("need exactly one ```pseudo block")
        return errs, warns
    p = kinds.index("pseudo")
    before, after = kinds[:p], kinds[p + 1:]
    if not before or before[0] != "para" or before.count("para") < 2:
        errs.append("need at least 2 prose paragraphs (problem, idea) first")
    if "text" not in before:
        errs.append("need a ```text picture before the pseudocode")
    for k in kinds:
        if k not in ("para", "text", "pseudo"):
            errs.append("unexpected code block language: " + k)
    if not after or any(k != "para" for k in after) or len(after) < 2:
        errs.append("after pseudocode: closing paragraph(s) then *Practice:* line")
    prose_words = 0
    for idx, it in enumerate(items):
        if it[0] == "para":
            t = it[1]
            if t.startswith("*Practice:*"):
                if idx != len(items) - 1:
                    errs.append("*Practice:* must be the last line")
                parts = t[len("*Practice:*"):].strip().split(" · ")
                if not 2 <= len(parts) <= 4:
                    errs.append("*Practice:* needs 2 to 4 problems")
                for part in parts:
                    if not re.match(r"^LC \d+ \S.*$", part):
                        errs.append("bad practice item: " + part)
                continue
            prose_words += len(t.split())
            for line in t.split("\n"):
                s = line.lstrip()
                if s.startswith("#") or s.startswith("|") or s.startswith("- ") \
                        or s.startswith("* ") or re.match(r"^\d+\. ", s):
                    errs.append("no headings/tables/lists in prose: " + s[:40])
            if t.startswith("**"):
                errs.append("no bold labels: " + t[:40])
            for ch in t:
                if ord(ch) > 127 and ch not in PROSE_UNICODE:
                    errs.append("prose char not allowed: %r" % ch)
        else:
            lang, code = it[1], it[2]
            for n, line in enumerate(code.split("\n"), 1):
                if len(line) > MAX_COLS:
                    errs.append("%s line %d longer than %d" % (lang, n, MAX_COLS))
                for ch in line:
                    if ord(ch) > 127 and ch not in CODE_UNICODE:
                        errs.append("%s line %d char not allowed: %r" % (lang, n, ch))
                if lang == "pseudo":
                    bare = line.split("//")[0] if "//" in line else line
                    for rx, msg in PSEUDO_BAD:
                        target = line if rx.pattern.endswith("$") else bare
                        if rx.search(target):
                            errs.append("pseudo line %d: %s: %s" % (n, msg, line.strip()))
            if lang == "text" and not 3 <= len(code.split("\n")) <= 24:
                warns.append("picture has %d lines (aim 4-20)" % len(code.split("\n")))
            if lang == "pseudo" and len(code.split("\n")) > 70:
                warns.append("pseudocode has %d lines" % len(code.split("\n")))
    if prose_words < 170 or prose_words > 650:
        warns.append("prose is %d words (aim 250-450)" % prose_words)
    if "[" in "".join(i[1] for i in items if i[0] == "para") and "](" in text:
        errs.append("no markdown links")
    return errs, warns


class StyleVisitor(ast.NodeVisitor):
    def __init__(self, topic):
        self.topic = topic
        self.errs = []
        self.func_depth = 0

    def bad(self, node, msg):
        self.errs.append("python line %d: %s" % (getattr(node, "lineno", 0), msg))

    def visit_FunctionDef(self, node):
        if self.func_depth > 0:
            self.bad(node, "nested function (use a top-level helper)")
        if ast.get_docstring(node) is None and node.name != "__init__":
            self.bad(node, "function %s needs a one-line docstring" % node.name)
        if node.returns is not None:
            self.bad(node, "no type hints")
        for a in node.args.args + node.args.kwonlyargs:
            if a.annotation is not None:
                self.bad(node, "no type hints")
        if node.args.vararg or node.args.kwarg:
            self.bad(node, "no *args / **kwargs")
        self.func_depth += 1
        self.generic_visit(node)
        self.func_depth -= 1

    def visit_ClassDef(self, node):
        saved = self.func_depth
        self.func_depth = 0
        self.generic_visit(node)
        self.func_depth = saved

    def visit_ListComp(self, node):
        if not (isinstance(node.elt, ast.BinOp) and isinstance(node.elt.op, ast.Mult)):
            self.bad(node, "no list comprehensions (only [[0] * m for ...] 2D init)")
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.bad(node, "no set comprehensions")

    def visit_DictComp(self, node):
        self.bad(node, "no dict comprehensions")

    def visit_GeneratorExp(self, node):
        self.bad(node, "no generator expressions")

    def visit_Lambda(self, node):
        self.bad(node, "no lambda")

    def visit_IfExp(self, node):
        self.bad(node, "no ternary a if c else b")

    def visit_NamedExpr(self, node):
        self.bad(node, "no walrus")

    def visit_AnnAssign(self, node):
        self.bad(node, "no type hints")

    def visit_Starred(self, node):
        self.bad(node, "no * unpacking")

    def visit_Name(self, node):
        if node.id in BANNED_NAMES:
            self.bad(node, "avoid " + node.id)

    def visit_Attribute(self, node):
        if node.attr in BANNED_NAMES:
            self.bad(node, "avoid ." + node.attr)
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            self.bad(node, "no chained method calls")
        self.generic_visit(node)

    def visit_Call(self, node):
        for kw in node.keywords:
            if kw.arg is None:
                self.bad(node, "no ** unpacking")
        self.generic_visit(node)

    def visit_Slice(self, node):
        if node.step is not None:
            ok = (isinstance(node.step, ast.UnaryOp) and isinstance(node.step.op, ast.USub)
                  and isinstance(node.step.operand, ast.Constant)
                  and node.step.operand.value == 1 and node.lower is None
                  and node.upper is None)
            if not ok:
                self.bad(node, "no slicing tricks beyond a[i:j] and a[::-1]")
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.check_module(node, alias.name)

    def visit_ImportFrom(self, node):
        self.check_module(node, node.module or "")
        if node.module == "collections":
            for alias in node.names:
                if alias.name != "deque":
                    self.bad(node, "from collections only deque")

    def check_module(self, node, name):
        root = name.split(".")[0]
        if root not in ALLOWED_IMPORTS:
            self.bad(node, "import not allowed: " + name)
        if root == "bisect" and self.topic != "Binary Search":
            self.bad(node, "bisect only in Binary Search entries")


def check_python(entry, path):
    errs, warns = [], []
    if not os.path.exists(path):
        return ["missing " + os.path.relpath(path, HERE)], warns
    src = open(path, encoding="utf-8").read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return ["syntax error: %s" % e], warns
    doc = ast.get_docstring(tree, clean=False)
    if doc is None:
        errs.append("module docstring missing")
    else:
        first = doc.strip("\n").split("\n")[0]
        want = "%s - %s" % (entry["title"], entry["subtitle"])
        if first != want:
            errs.append("docstring line 1 must be %r, got %r" % (want, first))
        parts = doc.strip("\n").split("\n\n")
        if len(parts) < 2 or "->" not in parts[1]:
            errs.append("docstring: blank line then problem paragraph ending with 'input -> output'")
    lines = src.split("\n")
    for n, line in enumerate(lines, 1):
        if len(line) > MAX_COLS:
            errs.append("python line %d longer than %d" % (n, MAX_COLS))
        if "\t" in line:
            errs.append("python line %d has a tab" % n)
    markers = []
    for line in lines:
        if line.startswith("# --- ") and line.endswith(" ---"):
            markers.append(line[6:-4])
    want_markers = ["algorithm", "try it"]
    if [mk for mk in markers if mk != "helpers"] != want_markers:
        errs.append("markers must be [helpers], algorithm, try it; got %s" % markers)
    if "helpers" in markers and markers.index("helpers") != 0:
        errs.append("# --- helpers --- must come first")
    v = StyleVisitor(entry["topic"])
    v.visit(tree)
    errs.extend(v.errs)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            length = node.end_lineno - node.lineno + 1
            if length > 32:
                warns.append("function %s is %d lines (aim <= 25)" % (node.name, length))
    expected = []
    if "# --- try it ---" in src:
        demo = src.split("# --- try it ---", 1)[1]
        for line in demo.split("\n"):
            if "# -> " in line:
                expected.append(line.split("# -> ", 1)[1].rstrip())
            elif line.strip().startswith("print("):
                errs.append("demo print without '# -> expected': " + line.strip()[:50])
    if not 2 <= len(expected) <= 6:
        errs.append("demo needs 2 to 5 checked prints, found %d" % len(expected))
    try:
        run = subprocess.run([sys.executable, "-I", path], capture_output=True, text=True,
                             timeout=60, cwd=os.path.dirname(path))
    except subprocess.TimeoutExpired:
        errs.append("running the file timed out")
        return errs, warns
    if run.returncode != 0:
        errs.append("running the file failed: " + run.stderr.strip().split("\n")[-1])
        return errs, warns
    got = run.stdout.rstrip("\n").split("\n") if run.stdout.strip() else []
    if len(got) != len(expected):
        errs.append("demo printed %d lines but %d are expected" % (len(got), len(expected)))
    for i in range(min(len(got), len(expected))):
        if got[i].rstrip() != expected[i]:
            errs.append("demo line %d: got %r, expected %r" % (i + 1, got[i], expected[i]))
    return errs, warns


def main(argv):
    manifest = load_manifest()
    if argv[:1] == ["--batch"]:
        batch = int(argv[1])
        entries = [e for e in manifest if e["batch"] == batch]
    elif argv:
        wanted = set(int(a) for a in argv)
        entries = [e for e in manifest if e["rank"] in wanted]
    else:
        entries = []
        for e in manifest:
            stem = "%03d_%s" % (e["rank"], e["slug"])
            if os.path.exists(os.path.join(HERE, "pseudo", stem + ".md")) or \
                    os.path.exists(os.path.join(HERE, "python", stem + ".py")):
                entries.append(e)
    failed = 0
    for e in entries:
        stem = "%03d_%s" % (e["rank"], e["slug"])
        e1, w1 = check_pseudo(e, os.path.join(HERE, "pseudo", stem + ".md"))
        e2, w2 = check_python(e, os.path.join(HERE, "python", stem + ".py"))
        errs, warns = e1 + e2, w1 + w2
        status = "OK" if not errs else "FAIL"
        print("#%-3d %-40s %s" % (e["rank"], e["slug"], status))
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
