"""
Balanced Binary Tree (LeetCode 110) - Easy
Chapter: trees
Pattern: Post-order height with side-channel answer

A binary tree is height-balanced if at every node the heights of the left and right
subtrees differ by at most 1. Return whether the tree is balanced.
Example: [3, 9, 20, None, None, 15, 7] -> True; [1, 2, 2, 3, 3, None, None, 4, 4] -> False
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


# --- brute force ---
def height(node):
    """Number of nodes on the longest path down from node."""
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def brute_force(root):
    """Compare the two subtree heights at every node, recomputing them each time. O(n^2) worst."""
    if root is None:
        return True
    if abs(height(root.left) - height(root.right)) > 1:   # heights recomputed at every level
        return False
    return brute_force(root.left) and brute_force(root.right)


# --- optimal ---
def checked_height(node):
    """Height of node's subtree if it is balanced, otherwise -1."""
    if node is None:
        return 0
    left = checked_height(node.left)
    if left < 0:
        return -1                       # something below is already unbalanced
    right = checked_height(node.right)
    if right < 0 or abs(left - right) > 1:
        return -1
    return 1 + max(left, right)


def is_balanced(root):
    """Fold the balance check into one height pass. O(n) time, O(h) stack."""
    return checked_height(root) >= 0


# --- try the brute force ---
print(brute_force(build_tree([3, 9, 20, None, None, 15, 7])))         # -> True
print(brute_force(build_tree([1, 2, 2, 3, 3, None, None, 4, 4])))     # -> False
print(brute_force(build_tree([])))                                    # -> True
print(brute_force(build_tree([1, 2, None, 3])))                       # -> False


# --- try the optimal ---
print(is_balanced(build_tree([3, 9, 20, None, None, 15, 7])))         # -> True
print(is_balanced(build_tree([1, 2, 2, 3, 3, None, None, 4, 4])))     # -> False
print(is_balanced(build_tree([])))                                    # -> True
print(is_balanced(build_tree([1, 2, None, 3])))                       # -> False
