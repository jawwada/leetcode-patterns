"""
Lowest Common Ancestor of a BST (LeetCode 235) - Medium
Area: trees
Key operations: compare both targets with the node, go left if both smaller, go right if both larger, stop at the split

Given a BST and two values p and q that are in it, return the value of their lowest common ancestor:
the deepest node that has both as descendants (a node counts as its own descendant).
Example: [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 3, q = 5 -> 4 (walk 6 -> 2 -> 4); p = 2, q = 8 -> 6
"""


# --- helpers ---
class TreeNode:
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None


def build_tree(values):
    """LeetCode level-order list, None = missing child; only real nodes consume children."""
    nodes = [TreeNode(v) if v is not None else None for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


# --- brute force ---
def brute_force(root, p, q):
    """Record the root -> p path and the root -> q path, then take the last value they share. O(h) time
    but stores both paths; the shared prefix is walked twice and only its last node matters."""
    def path(target):
        out, node = [], root
        while node.val != target:
            out.append(node.val)
            node = node.left if target < node.val else node.right
        return out + [node.val]

    lca = root.val
    for a, b in zip(path(p), path(q)):
        if a != b:
            break
        lca = a
    return lca


# --- optimal ---
def solve(root, p, q):
    """Walk down from the root: both targets smaller -> go left, both larger -> go right, otherwise the
    paths split here (or the node is p or q itself) and this is the LCA. O(h) time, O(1) space."""
    lo, hi = min(p, q), max(p, q)
    node = root
    while node:
        if hi < node.val:
            node = node.left
        elif lo > node.val:
            node = node.right
        else:
            return node.val


# --- demo ---
def demo():
    return solve(build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]), 3, 5)


# --- bugs ---
BUGS = [
    {
        "replace": "        if hi < node.val:",
        "with":    "        if hi <= node.val:",
        "fix": "go left only when both targets are strictly smaller; equal means this node is a target",
        "why": "When the node is q itself the walk steps past it into the left subtree: p = 0, q = 2 returns 0 instead of 2.",
        "decoys": [
            {"line": "        elif lo > node.val:", "change": "should be elif lo < node.val"},
            {"line": "    node = root", "change": "should start at root.left"},
            {"line": "            return node.val", "change": "should return node"},
        ],
    },
    {
        "replace": "    lo, hi = min(p, q), max(p, q)",
        "with":    "    lo, hi = p, q",
        "fix": "order the targets with min and max, p is not always the smaller one",
        "why": "With p > q the window is empty and both tests misfire: p = 8, q = 2 walks left from 6 and then off the tree, returning None instead of 6.",
        "decoys": [
            {"line": "        if hi < node.val:", "change": "should be if hi < node.val and lo < node.val"},
            {"line": "            node = node.right", "change": "should be node = node.right.left"},
            {"line": "    while node:", "change": "should be while node.left or node.right"},
        ],
    },
    {
        "replace": "            node = node.left",
        "with":    "            node = node.right",
        "fix": "both targets smaller than the node means they live in the left subtree",
        "why": "Turning the wrong way leaves the subtree that holds the targets: p = 3, q = 5 walks 6 -> 8 -> 9 -> None and returns None instead of 4.",
        "decoys": [
            {"line": "        elif lo > node.val:", "change": "should be elif lo >= node.val"},
            {"line": "    lo, hi = min(p, q), max(p, q)", "change": "should be max(p, q), min(p, q)"},
            {"line": "    node = root", "change": "should be node = root.val"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
