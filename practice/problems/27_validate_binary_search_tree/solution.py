"""
Validate Binary Search Tree (LeetCode 98) - Medium
Area: trees
Key operations: pass down an open window (lo, hi), check lo < val < hi, tighten hi going left and lo going right

Return True if the tree is a valid BST: every node is strictly greater than ALL values in its left
subtree and strictly less than ALL values in its right subtree (no duplicates).
Example: [5, 1, 4, None, None, 3, 6] -> False (3 sits under the right child but is < 5);
[2, 1, 3] -> True
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
        log(f"node {node.val}: window ({lo}, {hi})")
        if not (lo < node.val < hi):
            log(f"    {node.val} is outside ({lo}, {hi}): not a BST")
            return False
        log(f"    ok; left child gets ({lo}, {node.val}), right child gets ({node.val}, {hi})")
        return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)

    return valid(root, float("-inf"), float("inf"))


# --- demo ---
def demo():
    return solve(build_tree([5, 1, 4, None, None, 3, 6]))


# --- tests ---
def tests():
    assert solve(build_tree([5, 1, 4, None, None, 3, 6])) is False
    assert solve(build_tree([2, 1, 3])) is True
    assert solve(build_tree([5, 4, 6, None, None, 3, 7])) is False   # 3 < 4 locally but 3 < 5 breaks the root
    assert solve(build_tree([5, 4, 6, None, None, 5, 7])) is False   # equal to an ancestor is invalid
    assert solve(build_tree([3, 1, 5, None, 4])) is False            # 4 > 1 locally but 4 > 3 breaks the root
    assert solve(build_tree([2, 2, 2])) is False                     # duplicates are not allowed
    assert solve(build_tree([2, 2])) is False
    assert solve(build_tree([])) is True
    assert solve(build_tree([1])) is True
    assert solve(build_tree([3, 1, 5, 0, 2, 4, 6])) is True
    assert solve(build_tree([5, 7, 8])) is False                     # left child larger than the root
    import random
    random.seed(0)

    def insert(node, v):
        if node is None:
            return TreeNode(v)
        if v < node.val:
            node.left = insert(node.left, v)
        else:
            node.right = insert(node.right, v)
        return node

    def nodes_of(node):
        return [node] + nodes_of(node.left) + nodes_of(node.right) if node else []

    for _ in range(200):
        root = None
        for v in random.sample(range(20), random.randint(0, 8)):
            root = insert(root, v)
        if root and random.random() < 0.6:
            random.choice(nodes_of(root)).val = random.randint(0, 19)   # may break the order, maybe deep down
        assert solve(root) is brute_force(root)
        root = build_tree([random.randint(0, 5) if random.random() < 0.8 else None for _ in range(random.randint(0, 7))])
        assert solve(root) is brute_force(root)


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
