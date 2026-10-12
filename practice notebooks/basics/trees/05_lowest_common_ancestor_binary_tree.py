"""
Lowest Common Ancestor of a Binary Tree (LeetCode 236) - Basics
Area: trees
Key operations: post-order search, return the found node upward, both sides non-None means this node is the LCA

A binary tree has unique values; p and q are values that are in the tree. Return the value of their lowest
common ancestor (a node counts as an ancestor of itself).
Example: [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p=5, q=1 -> 3; p=5, q=4 -> 5
"""


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
def brute_force(root, p, q):
    """Find the root-to-node path of each target, then keep the last node the two paths share. O(n), two full searches plus a path compare."""
    def path(n, target):
        if n is None:
            return None
        if n.val == target:
            return [n.val]
        for child in (n.left, n.right):
            sub = path(child, target)
            if sub:
                return [n.val] + sub
        return None
    lca = None
    for x, y in zip(path(root, p), path(root, q)):
        if x != y:
            break
        lca = x
    return lca


# --- optimal ---
def solve(root, p, q):
    """Post-order: a node returns the target or LCA found below it; when both sides return something, it is the LCA. O(n)."""
    def lca(node):
        if node is None:
            return None
        if node.val in (p, q):
            return node
        left, right = lca(node.left), lca(node.right)
        if left and right:
            return node
        return left or right
    return lca(root).val


# --- demo ---
def demo():
    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    return solve(root, 5, 1), solve(root, 5, 4)


# --- bugs ---
BUGS = [
    {
        "replace": "        return left or right",
        "with":    "        return left",
        "fix": "pass up whichever side found something: left or right",
        "why": "A target found only in the right subtree is dropped on the way up, so lca(root) is None and .val raises: p=0, q=8 under node 1.",
        "decoys": [
            {"line": "        if node.val in (p, q):", "change": "should be node.val == p"},
            {"line": "    return lca(root).val", "change": "should return lca(root)"},
            {"line": "    def lca(node):", "change": "should also take p and q as parameters"},
        ],
    },
    {
        "replace": "        if left and right:",
        "with":    "        if left or right:",
        "fix": "this node is the LCA only when BOTH subtrees report a find",
        "why": "With 'or', every ancestor of a single find claims to be the LCA, so the answer floats up to the root: p=7, q=4 returns 3 instead of 2.",
        "decoys": [
            {"line": "        left, right = lca(node.left), lca(node.right)", "change": "should search right before left"},
            {"line": "            return None", "change": "should return root"},
            {"line": "        if node is None:", "change": "should be if node is None or node.val > max(p, q)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
