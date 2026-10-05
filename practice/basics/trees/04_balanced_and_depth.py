"""
Balanced Binary Tree (LeetCode 110) - Basics
Area: trees
Key operations: post-order height, return -1 upward as soon as a subtree is unbalanced, abs(left - right) > 1

A binary tree is height-balanced when at every node the heights of its two subtrees differ by at most 1.
Return True or False.
Example: [3, 9, 20, None, None, 15, 7] -> True; [1, 2, 2, 3, 3, None, None, 4, 4] -> False
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_tree(vals):  # level order, None = missing child (LeetCode style)
    nodes = [TreeNode(v) if v is not None else None for v in vals]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


# --- brute force ---
def brute_force(root):
    """Recompute both subtree heights from scratch at every node. O(n^2) on a chain: each height walk is repeated by every ancestor."""
    def height(n):
        return 1 + max(height(n.left), height(n.right)) if n else 0

    def balanced(n):
        return n is None or (abs(height(n.left) - height(n.right)) <= 1 and balanced(n.left) and balanced(n.right))
    return balanced(root)


# --- optimal ---
def solve(root):
    """Post-order: each node returns its height, or -1 as soon as any subtree is unbalanced. O(n)."""
    def height(node):
        if node is None:
            return 0
        left = height(node.left)
        if left == -1:
            return -1
        right = height(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            log(f"node {node.val}: left height {left}, right height {right} differ by more than 1 -> -1")
            return -1
        log(f"node {node.val}: left height {left}, right height {right} -> height {1 + max(left, right)}")
        return 1 + max(left, right)
    return height(root) != -1


# --- demo ---
def demo():
    return solve(build_tree([3, 9, 20, None, None, 15, 7])), solve(build_tree([1, 2, 2, 3, 3, None, None, 4, 4]))


# --- tests ---
def random_tree(rng, n):
    """Random shape with unique values 0..n-1: attach each new node to a random free slot."""
    nodes = [TreeNode(i) for i in range(n)]
    for i in range(1, n):
        while True:
            p = nodes[rng.randrange(i)]
            if p.left is None or p.right is None:
                break
        side = rng.choice([s for s in ("left", "right") if getattr(p, s) is None])
        setattr(p, side, nodes[i])
    return nodes[0] if n else None


def tests():
    assert solve(build_tree([3, 9, 20, None, None, 15, 7])) is True
    assert solve(build_tree([1, 2, 2, 3, 3, None, None, 4, 4])) is False
    assert solve(None) is True
    assert solve(build_tree([1])) is True
    assert solve(build_tree([1, 2])) is True                    # heights 1 and 0 differ by exactly 1
    assert solve(build_tree([1, 2, None, 3])) is False          # chain of 3
    assert solve(build_tree([1, 2, 3, 4, None, None, 5, 6])) is False  # balanced at root, not at node 2
    import random
    rng = random.Random(4)
    seen = set()
    for _ in range(200):
        root = random_tree(rng, rng.randint(0, 10))
        seen.add(solve(root))
        assert solve(root) == brute_force(root)
    assert seen == {True, False}


# --- bugs ---
BUGS = [
    {
        "replace": "        if abs(left - right) > 1:",
        "with":    "        if abs(left - right) >= 1:",
        "fix": "a difference of exactly 1 is still balanced; reject only when it exceeds 1",
        "why": "Strictness slip: [1, 2] has subtree heights 1 and 0 and is balanced, but >= 1 reports False.",
        "decoys": [
            {"line": "        return 1 + max(left, right)", "change": "should be 1 + min(left, right)"},
            {"line": "    return height(root) != -1", "change": "should be height(root) >= 1"},
            {"line": "        right = height(node.right)", "change": "should be computed before left"},
        ],
    },
    {
        "replace": "        return 1 + max(left, right)",
        "with":    "        return max(left, right)",
        "fix": "a node adds one level on top of its taller subtree: 1 + max(left, right)",
        "why": "Without the +1 every height stays 0, no difference ever exceeds 1, and a chain of 3 is reported balanced.",
        "decoys": [
            {"line": "        if left == -1:", "change": "should be left == 0"},
            {"line": "            return 0", "change": "should return -1 for an empty subtree"},
            {"line": "        left = height(node.left)", "change": "should be height(node)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
