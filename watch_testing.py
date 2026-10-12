#!/usr/bin/env python3
"""
Live monitor for a practice file.

Run it in its own terminal, then edit testing.py in your editor. Every time you
save, this re-runs the file and prints a running discussion of what happened:
what your code produced, or exactly where it broke and a nudge toward the fix.

    python3 watch_testing.py            # watches ./testing.py
    python3 watch_testing.py other.py   # watches another file

Stop it with Ctrl-C. No third-party packages needed.
"""

import os
import re
import subprocess
import sys
import time
from datetime import datetime

TARGET = sys.argv[1] if len(sys.argv) > 1 else "testing.py"
POLL_SECONDS = 0.4

# Section markers in the scaffold, so the discussion can name what you're on.
SECTIONS = [
    "1. GRAPH DFS",
    "2. GRID / MATRIX DFS",
    "3. BINARY TREE DFS",
    "4. ITERATIVE DFS",
]

# Common stumbles -> a one-line nudge. The watcher never writes the answer,
# it just points at the idea you're missing so you can write it yourself.
HINTS = [
    (r"NameError.*'dfs'",
     "dfs isn't defined where you call it — did the function body get indented under it?"),
    (r"RecursionError",
     "infinite recursion — you're revisiting a node. Mark visited BEFORE you recurse into neighbors."),
    (r"IndexError",
     "out-of-bounds — your grid DFS needs the bounds check (r<0 or c<0 or r>=rows or c>=cols) FIRST."),
    (r"KeyError",
     "a node has no entry in the graph dict — iterate graph.get(node, []) or make sure every node is a key."),
    (r"TypeError.*NoneType",
     "you hit a None child/neighbor — add the base case 'if node is None: return' before using it."),
    (r"IndentationError",
     "indentation — the body lines must sit one level inside the def/for/if above them."),
    (r"SyntaxError",
     "syntax slip — unmatched bracket, missing colon, or a stray comment line turned into code."),
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def filled_sections(src):
    """Guess which sections have real code (a line that isn't blank/comment)."""
    lines = src.splitlines()
    # Find the start line of each section header.
    starts = []
    for i, line in enumerate(lines):
        for s in SECTIONS:
            if s in line:
                starts.append((i, s))
    starts.append((len(lines), None))
    done = []
    for (start, name), (nxt, _) in zip(starts, starts[1:]):
        body = lines[start:nxt]
        has_code = any(
            ln.strip() and not ln.strip().startswith("#") and not ln.strip().startswith("def dfs(node")
            for ln in body
        )
        # treat the pre-written `def dfs(node, graph, visited):` as not-yet-filled
        real = any(
            ln.strip() and not ln.strip().startswith("#")
            and ln.strip() != "def dfs(node, graph:dict, visited:set):"
            for ln in body
        )
        done.append((name, real))
    return done


def nudge(err_text):
    for pattern, msg in HINTS:
        if re.search(pattern, err_text):
            return msg
    return None


def run(path):
    return subprocess.run(
        [sys.executable, path],
        capture_output=True, text=True, timeout=10,
    )


def report(path):
    clear()
    src = read(path)
    stamp = datetime.now().strftime("%H:%M:%S")
    print(f"\033[1m◆ watching {path}\033[0m   saved at {stamp}")
    print("─" * 60)

    if src is None:
        print(f"  (file {path} not found — is the path right?)")
        return

    progress = filled_sections(src)
    if progress:
        print("  sections:")
        for name, real in progress:
            mark = "\033[32m�filled\033[0m" if real else "\033[90m· empty\033[0m"
            print(f"    {mark}  {name}")
        print("─" * 60)

    try:
        proc = run(path)
    except subprocess.TimeoutExpired:
        print("  \033[31m⏱ timed out (10s)\033[0m — likely infinite recursion or a loop that never ends.")
        print("     In DFS that means a node gets re-entered: mark it visited before recursing.")
        return

    out = proc.stdout.strip()
    err = proc.stderr.strip()

    if proc.returncode == 0:
        if out:
            print("  \033[32m✓ ran clean. your prints:\033[0m")
            for line in out.splitlines():
                print(f"     {line}")
        else:
            print("  \033[33m✓ ran clean, but printed nothing.\033[0m")
            print("     Add a print in your test block so you can see the traversal.")
    else:
        print("  \033[31m✗ it broke:\033[0m")
        tail = err.splitlines()[-6:] if err else ["(no error text)"]
        for line in tail:
            print(f"     {line}")
        hint = nudge(err)
        if hint:
            print()
            print(f"  \033[36m→ {hint}\033[0m")


def main():
    last = None
    print(f"monitoring {TARGET} — edit and save, I'll react. Ctrl-C to stop.")
    try:
        while True:
            try:
                mtime = os.path.getmtime(TARGET)
            except FileNotFoundError:
                mtime = None
            if mtime != last:
                last = mtime
                report(TARGET)
                print("\n─" * 0 + "\nwaiting for your next save…")
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print("\nstopped. nice work.")


if __name__ == "__main__":
    main()
