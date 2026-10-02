"""
Simplify Path (LeetCode 71)  — Medium
Pattern: Stack simulation

Problem
-------
Convert an absolute Unix path to its canonical form: a single leading '/', no trailing '/',
no '.' components, and '..' resolved to the parent directory (at root, '..' is a no-op).
Multiple consecutive slashes collapse.
Example: "/home//foo/" -> "/home/foo"; "/a/./b/../../c/" -> "/c"; "/../" -> "/".

Brute force
-----------
Split on '/' and discard "" and "." parts, then repeatedly find the first ".." and delete it
together with the component before it, restarting the scan after every deletion. O(n^2)
time in the number of components (each restart rescans the prefix), O(n) space. The wasted
work: the prefix before the first ".." is re-examined on every pass although nothing in it
changed.

From brute force to optimal
---------------------------
The redundancy is rescanning a prefix that is already canonical. Observation: ".." always
cancels the most recently added surviving component -- LIFO. So walk the components once,
pushing directory names onto a stack and popping on "..". The stack at the end IS the
canonical path; join it with '/'. Each component is pushed and popped at most once.

Intuition
---------
A path is a sequence of "go into directory" and "go up" moves. A stack of directory names
tracks the current location: a name pushes, ".." pops, "." and empty parts do nothing.

Geometric view
--------------
Think of walking a tree from the root: each name descends one level (push), ".." climbs one
level (pop, unless already at the root). After consuming the whole path the stack is the
chain of ancestors from root to the final directory.

Steps
-----
1. stack = [].
2. For part in path.split('/'): if part == "..": pop if non-empty; elif part not in ("", "."):
   push part.
3. Return "/" + "/".join(stack).

Complexity: O(n) time, O(n) space — one pass over the characters, one push/pop per component.
Pitfalls: Treating "..." or ".hidden" as special (they are valid directory names); popping on
".." at root (must be a no-op); returning "" instead of "/" for an empty stack.
"""


class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in path.split("/"):
            if part == "..":
                if stack:
                    stack.pop()                    # go up one level; no-op at root
            elif part and part != ".":
                stack.append(part)                 # "" (from //) and "." are skipped
        return "/" + "/".join(stack)


def brute_force(path: str) -> str:
    parts = [p for p in path.split("/") if p not in ("", ".")]
    changed = True
    while changed:                                 # rescan from the start after each change
        changed = False
        for i, p in enumerate(parts):
            if p == "..":
                del parts[max(i - 1, 0):i + 1]     # cancel "name/.."; at root ".." vanishes
                changed = True
                break
    return "/" + "/".join(parts)


if __name__ == "__main__":
    s = Solution()
    cases = ["/home/", "/home//foo/", "/home/user/Documents/../Pictures", "/../", "/.../a/../b/c/../d/./", "/a/b/../../.."]
    assert s.simplifyPath("/home/") == "/home"
    assert s.simplifyPath("/home//foo/") == "/home/foo"
    assert s.simplifyPath("/home/user/Documents/../Pictures") == "/home/user/Pictures"
    assert s.simplifyPath("/../") == "/"
    assert s.simplifyPath("/.../a/../b/c/../d/./") == "/.../b/d"
    for c in cases:
        assert s.simplifyPath(c) == brute_force(c)
    print("ok")
