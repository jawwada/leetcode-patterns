"""
BST Insert, Search, Delete - Basics
Area: trees
Key operations: descend by comparison, attach a new leaf, splice out a node with 0 or 1 child, replace a 2-child node by its inorder successor

Apply a sequence of insert / search / delete operations to an initially empty binary search tree
(duplicates are ignored). Return the search results and the final inorder traversal, which must be sorted.
Example: insert 5, 3, 8, 1, 4, 9; search 4; delete 3; delete 5; search 3
-> searches [True, False], inorder [1, 4, 8, 9]
"""
import bisect


def show(node):
    """Trace only: 5(3(1, 4), 8(., 9)) with . for a missing child."""
    if node is None:
        return "."
    if node.left is None and node.right is None:
        return str(node.val)
    return f"{node.val}({show(node.left)}, {show(node.right)})"


# --- helpers ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


# --- brute force ---
def brute_force(ops):
    """Keep a sorted Python list: insort, membership, remove. O(n) per operation instead of O(height)."""
    vals, found = [], []
    for op, v in ops:
        if op == "insert":
            if v not in vals:
                bisect.insort(vals, v)
        elif op == "search":
            found.append(v in vals)
        elif v in vals:
            vals.remove(v)
    return found, vals


# --- optimal ---
def insert(root, v):
    if root is None:
        return TreeNode(v)
    if v < root.val:
        root.left = insert(root.left, v)
    elif v > root.val:
        root.right = insert(root.right, v)
    return root


def search(root, v):
    while root and root.val != v:
        root = root.left if v < root.val else root.right
    return root is not None


def delete(root, v):
    if root is None:
        return None
    if v < root.val:
        root.left = delete(root.left, v)
    elif v > root.val:
        root.right = delete(root.right, v)
    elif root.left is None or root.right is None:
        return root.left or root.right
    else:
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root


def inorder(n): return inorder(n.left) + [n.val] + inorder(n.right) if n else []


def solve(ops):
    """Each op descends one root-to-leaf path: O(height) per op, O(n) for the final inorder."""
    root, found = None, []
    for op, v in ops:
        if op == "search":
            found.append(search(root, v))
        else:
            root = insert(root, v) if op == "insert" else delete(root, v)
    return found, inorder(root)


# --- demo ---
def demo():
    return solve([("insert", v) for v in (5, 3, 8, 1, 4, 9)] + [("search", 4), ("delete", 3), ("delete", 5), ("search", 3)])


# --- bugs ---
BUGS = [
    {
        "replace": "        root.right = delete(root.right, succ.val)",
        "with":    "        root.right = delete(root.right, v)",
        "fix": "after copying the successor's value here, delete the SUCCESSOR's value from the right subtree",
        "why": "v is no longer in the right subtree, so nothing is removed and the successor's value now appears twice: delete 3 in 5(3(1, 4), 8) leaves 4 twice.",
        "decoys": [
            {"line": "        succ = root.right", "change": "should be root.left"},
            {"line": "        root.val = succ.val", "change": "should be succ.val = root.val"},
            {"line": "        return root.left or root.right", "change": "should return root"},
        ],
    },
    {
        "replace": "    elif root.left is None or root.right is None:",
        "with":    "    elif root.left is None and root.right is None:",
        "fix": "splice out the node when it has AT MOST one child (either side missing)",
        "why": "A node with exactly one child falls into the two-children branch and succ = root.right is None when only the left child exists: deleting 2 in 1 -> 2 -> 3 raises.",
        "decoys": [
            {"line": "        root.right = insert(root.right, v)", "change": "should be else: duplicates go right"},
            {"line": "        while succ.left:", "change": "should be while succ.right"},
            {"line": "        return None", "change": "should return root"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
