"""
Simplify Path (LeetCode 71) - Basics
Area: stacks
Key operations: split on '/', skip '' and '.', pop on '..', join the survivors

Given an absolute Unix path, return its canonical form: '.' is the current directory, '..' goes up
one level (never above root), repeated slashes count as one, and there is no trailing slash.
Any other name, including '...', is an ordinary directory name.
Example: "/a/./b/../../c/" -> "/c"
"""


# --- brute force ---
def brute_force(path: str) -> str:
    """Split into names, then repeatedly delete the first '..' together with the name before it. O(n^2): every round rescans from the start."""
    parts = [p for p in path.split("/") if p not in ("", ".")]
    while ".." in parts:
        i = parts.index("..")
        del parts[max(i - 1, 0):i + 1]
    return "/" + "/".join(parts)


# --- optimal ---
def solve(path: str) -> str:
    """Stack of directory names: '..' pops (if anything is there), '' and '.' are skipped, names are pushed. O(n)."""
    stack = []
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return "/" + "/".join(stack)


# --- demo ---
def demo():
    return solve("/a/./b/../../c/")


# --- bugs ---
BUGS = [
    {
        "replace": "        if part in (\"\", \".\"):",
        "with":    "        if part == \".\":",
        "fix": "skip the empty names too: splitting '//' and a trailing '/' on '/' yields empty strings",
        "why": "'/home//foo/' splits into ['', 'home', '', 'foo', ''] and the empty names get pushed, producing '/home//foo/'.",
        "decoys": [
            {"line": "            if stack:", "change": "should be 'if len(stack) > 1:' to protect the root"},
            {"line": "    return \"/\" + \"/\".join(stack)", "change": "should be '/'.join(stack) without the prefix"},
            {"line": "            stack.append(part)", "change": "should insert at index 0"},
        ],
    },
    {
        "replace": "        if part == \"..\":",
        "with":    "        if part.startswith(\"..\"):",
        "fix": "only the exact name '..' goes up; '...' or '..x' are ordinary directory names",
        "why": "'/.../a' is a directory called '...' followed by 'a'; treating it as 'go up' returns '/a' instead of '/.../a'.",
        "decoys": [
            {"line": "    for part in path.split(\"/\"):", "change": "should split on '//'"},
            {"line": "                stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "    stack = []", "change": "should start as ['/']"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
