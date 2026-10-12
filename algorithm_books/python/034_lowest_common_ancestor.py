"""
Lowest Common Ancestor - Postorder Search in a Binary Tree

Given a binary tree and two of its nodes p and q, return the deepest node that
has both in its subtree (a node counts as its own ancestor):
[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p = 7, q = 8 -> 3.
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build a tree from a level-order list with None for missing children."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def find(root, val):
    """Return the node holding val, or None (values are unique)."""
    if root is None or root.val == val:
        return root
    left = find(root.left, val)
    if left is not None:
        return left
    return find(root.right, val)


# --- algorithm ---
def lowest_common_ancestor(root, p, q):
    """Postorder; report p, q or their meeting point upward. O(n) time."""
    if root is None or root is p or root is q:
        return root                     # nothing here, or a target itself
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left is not None and right is not None:
        return root                     # one target on each side: the LCA
    if left is not None:
        return left                     # pass the single report upward
    return right


# --- try it ---
root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
answer = lowest_common_ancestor(root, find(root, 7), find(root, 8))
print(answer.val)                       # -> 3
answer = lowest_common_ancestor(root, find(root, 6), find(root, 4))
print(answer.val)                       # -> 5
answer = lowest_common_ancestor(root, find(root, 5), find(root, 4))
print(answer.val)                       # -> 5
