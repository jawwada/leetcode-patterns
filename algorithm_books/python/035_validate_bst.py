"""
Validate a Binary Search Tree - Carry the Allowed Range Down

Given the root of a binary tree, decide whether it is a valid BST: every value
in a node's left subtree is strictly smaller, every value in its right subtree
strictly larger. [2, 1, 3] -> True, [5, 4, 6, None, None, 3, 7] -> False.
"""
from collections import deque      # popleft is O(1)
import math                         # math.inf: no bound at the root


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


# --- algorithm ---
def is_valid_bst(root):
    """Start with no bounds; every node must fit its ancestors' range. O(n)."""
    return fits(root, -math.inf, math.inf)


def fits(node, low, high):
    """True if every value in this subtree is strictly between low and high."""
    if node is None:
        return True
    if node.val <= low or node.val >= high:
        return False                        # breaks a promise made higher up
    if not fits(node.left, low, node.val):  # left side: below node.val
        return False
    return fits(node.right, node.val, high)     # right side: above node.val


# --- try it ---
print(is_valid_bst(build_tree([2, 1, 3])))                      # -> True
print(is_valid_bst(build_tree([5, 4, 6, None, None, 3, 7])))    # -> False
print(is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6])))    # -> False
print(is_valid_bst(build_tree([2, 2, 2])))                      # -> False
print(is_valid_bst(build_tree([])))                             # -> True
