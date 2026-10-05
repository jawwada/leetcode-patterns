"""
Simplify Path (LeetCode 71) - Medium
Chapter: strings
Pattern: Stack simulation

Convert an absolute Unix path to canonical form: a single leading '/', no trailing '/', no '.'
components, '..' resolved to the parent (a no-op at root) and consecutive slashes collapsed.
Example: "/home//foo/" -> "/home/foo"; "/a/./b/../../c/" -> "/c"; "/../" -> "/".
"""


# --- brute force ---
def brute_force(path):
    """Drop "" and ".", then repeatedly delete the first ".." and the name before it. O(n^2)."""
    parts = []
    for part in path.split("/"):
        if part != "" and part != ".":
            parts.append(part)
    changed = True
    while changed:                        # rescan from the start after every deletion
        changed = False
        for i in range(len(parts)):
            if parts[i] == "..":
                parts.pop(i)              # the ".." itself goes
                if i > 0:
                    parts.pop(i - 1)      # and it cancels the name before it (none at the root)
                changed = True
                break
    return "/" + "/".join(parts)


# --- optimal ---
def simplify_path(path):
    """Stack of names: a name pushes, ".." pops, "" and "." do nothing. O(n) time, O(n) space."""
    stack = []
    for part in path.split("/"):
        if part == "..":
            if len(stack) > 0:
                stack.pop()               # go up one level; no-op at the root
        elif part != "" and part != ".":
            stack.append(part)            # "" (from //) and "." are skipped
    return "/" + "/".join(stack)


# --- try the brute force ---
print(brute_force("/home//foo/"))                  # -> /home/foo
print(brute_force("/a/./b/../../c/"))              # -> /c
print(brute_force("/../"))                         # -> /
print(brute_force("/.../a/../b/c/../d/./"))        # -> /.../b/d


# --- try the optimal ---
print(simplify_path("/home//foo/"))                # -> /home/foo
print(simplify_path("/a/./b/../../c/"))            # -> /c
print(simplify_path("/../"))                       # -> /
print(simplify_path("/.../a/../b/c/../d/./"))      # -> /.../b/d
