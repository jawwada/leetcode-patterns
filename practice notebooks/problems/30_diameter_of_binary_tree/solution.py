"""
Diameter of Binary Tree (LeetCode 543) - Medium
Area: trees
Key operations: post-order height, candidate = left + right at every node, nonlocal best

The diameter of a binary tree is the number of edges on the longest path between any two nodes;
the path does not have to pass through the root. Return the diameter.
Example: [1, 2, 3, 4, 5] (level order) -> 3, the path 4 -> 2 -> 1 -> 3 (or 5 -> 2 -> 1 -> 3).
"""
from collections import deque
from typing import List, Optional


# --- helpers ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_tree(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """Level-order list with None for a missing child -> root (LeetCode's format)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = deque([root]), 1
    while queue and i < len(vals):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(vals) and vals[i] is not None:
                setattr(node, side, TreeNode(vals[i]))
                queue.append(getattr(node, side))
            i += 1
    return root


# --- brute force ---
def brute_force(root: Optional[TreeNode]) -> int:
    """At every node compute height(left) + height(right) from scratch and take the maximum.
    O(n^2) on a skewed tree: a subtree's height is recomputed once for each of its ancestors."""
    def height(node):
        return 0 if node is None else 1 + max(height(node.left), height(node.right))

    if root is None:
        return 0
    through_here = height(root.left) + height(root.right)
    return max(through_here, brute_force(root.left), brute_force(root.right))


# --- optimal ---
def solve(root: Optional[TreeNode]) -> int:
    """One post-order pass: height(node) returns the longest downward arm in edges and, while both
    arm lengths are at hand, records left + right as a candidate diameter. O(n) time, O(h) space."""
    best = 0

    def height(node, depth=0):
        nonlocal best
        if node is None:
            return 0
        left = height(node.left, depth + 1)
        right = height(node.right, depth + 1)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best


# --- demo ---
def demo():
    return solve(build_tree([1, 2, 3, 4, 5]))


# --- bugs ---
BUGS = [
    {
        "replace": "        return 1 + max(left, right)",
        "with":    "        return max(left, right)",
        "fix": "return 1 + max(left, right); the edge to the parent adds one",
        "why": "Without the + 1 every arm length stays 0, so left + right is 0 at every node and [1, 2, 3, 4, 5] returns 0 instead of 3.",
        "decoys": [
            {"line": "        best = max(best, left + right)", "change": "should be max(best, left, right)"},
            {"line": "        if node is None:", "change": "should also return early when node is a leaf"},
            {"line": "    height(root)", "change": "should be height(root.left) + height(root.right)"},
        ],
    },
    {
        "replace": "        best = max(best, left + right)",
        "with":    "        best = max(best, left + right + 1)",
        "fix": "the path bending at node has left + right edges, no + 1",
        "why": "left + right already counts the edges of the path through node; adding one counts nodes, so [1, 2, 3, 4, 5] returns 4 and a single node returns 1.",
        "decoys": [
            {"line": "        return 1 + max(left, right)", "change": "should return left + right"},
            {"line": "        right = height(node.right, depth + 1)", "change": "should be computed before left"},
            {"line": "    best = 0", "change": "should start at 1 when root is not None"},
        ],
    },
    {
        "replace": "    height(root)",
        "with":    "    return height(root)",
        "fix": "call height(root) for its side effect and return best",
        "why": "The height of the root is the longest single arm, not the longest path: [1, 2] has height 2 but diameter 1, and the answer may bend below the root anyway.",
        "decoys": [
            {"line": "        nonlocal best", "change": "should be global best"},
            {"line": "        left = height(node.left, depth + 1)", "change": "should pass depth, not depth + 1"},
            {"line": "            return 0", "change": "should return -1 for a missing child"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
