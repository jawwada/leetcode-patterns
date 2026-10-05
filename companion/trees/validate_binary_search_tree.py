"""
Validate Binary Search Tree (LeetCode 98) - Medium
Chapter: trees
Pattern: DFS with (low, high) bounds

Return True if a binary tree is a valid BST: every node's value is strictly greater than
all values in its left subtree and strictly less than all values in its right subtree.
Example: [2, 1, 3] -> True; [5, 1, 4, None, None, 3, 6] -> False (3 is right of 5)
"""
import math
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


# --- brute force ---
def all_values(node):
    """Every value in node's subtree, as a list."""
    if node is None:
        return []
    return [node.val] + all_values(node.left) + all_values(node.right)


def brute_force(root):
    """At each node rescan its whole left and right subtrees. O(n^2) worst case."""
    if root is None:
        return True
    for value in all_values(root.left):     # the same subtree is rescanned by every ancestor
        if value >= root.val:
            return False
    for value in all_values(root.right):
        if value <= root.val:
            return False
    return brute_force(root.left) and brute_force(root.right)


# --- optimal ---
def valid(node, low, high):
    """True if every value in node's subtree lies strictly inside (low, high)."""
    if node is None:
        return True
    if node.val <= low or node.val >= high:
        return False
    # going left tightens the upper bound, going right tightens the lower bound
    return valid(node.left, low, node.val) and valid(node.right, node.val, high)


def is_valid_bst(root):
    """Hand each node an allowed open interval instead of rescanning. O(n) time, O(h) stack."""
    return valid(root, -math.inf, math.inf)    # math.inf: no bound yet


# --- try the brute force ---
print(brute_force(build_tree([2, 1, 3])))                      # -> True
print(brute_force(build_tree([5, 1, 4, None, None, 3, 6])))    # -> False
print(brute_force(build_tree([2, 2, 2])))                      # -> False
print(brute_force(build_tree([3, 1, 5, 0, 2, 4, 6])))          # -> True


# --- try the optimal ---
print(is_valid_bst(build_tree([2, 1, 3])))                      # -> True
print(is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6])))    # -> False
print(is_valid_bst(build_tree([2, 2, 2])))                      # -> False
print(is_valid_bst(build_tree([3, 1, 5, 0, 2, 4, 6])))          # -> True
