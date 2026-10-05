"""
Lowest Common Ancestor of a BST (LeetCode 235) - Medium
Chapter: trees
Pattern: BST ordered descent

Given a binary search tree and two of its nodes p and q, return their lowest common
ancestor: the deepest node that has both as descendants (a node counts as its own descendant).
Example: root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 2, q = 8 -> 6; p = 2, q = 4 -> 2
"""
from collections import deque


# --- helpers ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(vals):
    """Level-order list (None = missing child) -> tree, the LeetCode input format."""
    if len(vals) == 0 or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])          # deque: popleft is O(1)
    i = 1
    while len(queue) > 0 and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def find_node(root, value):
    """Return the node holding value in a BST (used to pick p and q for the demos)."""
    node = root
    while node is not None and node.val != value:
        if value < node.val:
            node = node.left
        else:
            node = node.right
    return node


# --- brute force ---
def path_to(root, target):
    """Walk down from the root to target using the BST order; return the nodes passed."""
    path = []
    node = root
    while node is not target:
        path.append(node)
        if target.val < node.val:
            node = node.left
        else:
            node = node.right
    path.append(target)
    return path


def brute_force(root, p, q):
    """Record both root-to-node paths, return the last node they share. O(h) time and space."""
    path_p = path_to(root, p)
    path_q = path_to(root, q)
    lca = root
    for i in range(min(len(path_p), len(path_q))):
        if path_p[i] is not path_q[i]:      # the paths split here
            break
        lca = path_p[i]
    return lca


# --- optimal ---
def lowest_common_ancestor(root, p, q):
    """Descend once; the first node whose value sits between the two is the split. O(h), O(1)."""
    low = min(p.val, q.val)
    high = max(p.val, q.val)
    node = root
    while node is not None:
        if high < node.val:
            node = node.left            # both targets are to the left
        elif low > node.val:
            node = node.right           # both targets are to the right
        else:
            return node                 # low <= node.val <= high: they split here
    return None


# --- try the brute force ---
tree = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
print(brute_force(tree, find_node(tree, 2), find_node(tree, 8)).val)   # -> 6
print(brute_force(tree, find_node(tree, 2), find_node(tree, 4)).val)   # -> 2
print(brute_force(tree, find_node(tree, 3), find_node(tree, 5)).val)   # -> 4


# --- try the optimal ---
tree = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
print(lowest_common_ancestor(tree, find_node(tree, 2), find_node(tree, 8)).val)   # -> 6
print(lowest_common_ancestor(tree, find_node(tree, 2), find_node(tree, 4)).val)   # -> 2
print(lowest_common_ancestor(tree, find_node(tree, 3), find_node(tree, 5)).val)   # -> 4
