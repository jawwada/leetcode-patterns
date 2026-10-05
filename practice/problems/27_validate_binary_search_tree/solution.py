"""
Validate Binary Search Tree (LeetCode 98) - Medium
Area: trees
Key operations: pass down an open window (lo, hi), check lo < val < hi, tighten hi going left and lo going right

Return True if the tree is a valid BST: every node is strictly greater than ALL values in its left
subtree and strictly less than ALL values in its right subtree (no duplicates).
Example: [5, 1, 4, None, None, 3, 6] -> False (3 sits under the right child but is < 5);
[2, 1, 3] -> True
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
def brute_force(root):
    """Collect the whole inorder sequence into a list, then check it is strictly increasing. O(n) time but
    O(n) extra space and a second pass over a copy; the optimal checks each node in place against bounds."""
    def inorder(node):
        return inorder(node.left) + [node.val] + inorder(node.right) if node else []

    vals = inorder(root)
    return all(a < b for a, b in zip(vals, vals[1:]))


# --- optimal ---
def solve(root):
    """Hand every node an open window (lo, hi) that all values in its subtree must lie in: going left
    tightens hi to the node's value, going right tightens lo. O(n) time, O(h) recursion stack."""
    def valid(node, lo, hi):
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)

    return valid(root, float("-inf"), float("inf"))


# --- demo ---
def demo():
    return solve(build_tree([5, 1, 4, None, None, 3, 6]))


# --- bugs ---
BUGS = [
    {
        "replace": "        if not (lo < node.val < hi):",
        "with":    "        if not (lo <= node.val <= hi):",
        "fix": "use strict comparisons, a value equal to a bound duplicates an ancestor",
        "why": "The bounds are ancestor values, so touching one means a duplicate: [2, 2, 2] is accepted as a BST.",
        "decoys": [
            {"line": "        if node is None:", "change": "should be if node is None or node.val is None"},
            {"line": "    return valid(root, float(\"-inf\"), float(\"inf\"))", "change": "should start with (root.val, inf)"},
            {"line": "            return True", "change": "should return False for an empty subtree"},
        ],
    },
    {
        "replace": "        return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)",
        "with":    "        return valid(node.left, lo, node.val) and valid(node.right, lo, hi)",
        "fix": "the right child's window is (node.val, hi): going right raises the lower bound",
        "why": "Without tightening lo, a small value hidden in a right subtree passes: [5, 4, 6, None, None, 3, 7] is accepted although 3 lies right of 5.",
        "decoys": [
            {"line": "        if not (lo < node.val < hi):", "change": "should compare only with the parent value"},
            {"line": "    def valid(node, lo, hi):", "change": "should take the parent node instead of bounds"},
            {"line": "            return False", "change": "should return None"},
        ],
    },
    {
        "replace": "        return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)",
        "with":    "        return valid(node.left, lo, node.val) or valid(node.right, node.val, hi)",
        "fix": "both subtrees must be valid, combine with and",
        "why": "With or, one valid subtree hides a broken one: [5, 1, 4, None, None, 3, 6] is accepted because the left subtree is fine.",
        "decoys": [
            {"line": "    return valid(root, float(\"-inf\"), float(\"inf\"))", "change": "should pass (0, inf)"},
            {"line": "        if node is None:", "change": "should be if not node.left and not node.right"},
            {"line": "        if not (lo < node.val < hi):", "change": "should be if lo < node.val < hi"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
