"""
Symmetric Tree (LeetCode 101) - Easy
Chapter: trees
Pattern: Simultaneous tree recursion

Return True if a binary tree is a mirror image of itself around its centre line.
Example: [1, 2, 2, 3, 4, 4, 3] -> True; [1, 2, 2, None, 3, None, 3] -> False
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
def brute_force(root):
    """Each level, with None for missing slots, must be a palindrome. O(n) time and space."""
    level = [root]
    while len(level) > 0:
        vals = []
        for node in level:
            if node is None:
                vals.append(None)
            else:
                vals.append(node.val)
        if vals != vals[::-1]:          # the level must be a palindrome, empty slots included
            return False
        next_level = []
        for node in level:
            if node is not None:
                next_level.append(node.left)
                next_level.append(node.right)
        level = next_level
    return True


# --- optimal ---
def is_mirror(a, b):
    """True if subtree a is the mirror image of subtree b."""
    if a is None or b is None:
        return a is None and b is None     # both missing -> mirror; one missing -> not
    if a.val != b.val:
        return False
    return is_mirror(a.left, b.right) and is_mirror(a.right, b.left)   # outer pair, inner pair


def is_symmetric(root):
    """Walk the two halves in lockstep, comparing mirror pairs. O(n) time, O(h) stack."""
    if root is None:
        return True
    return is_mirror(root.left, root.right)


# --- try the brute force ---
print(brute_force(build_tree([1, 2, 2, 3, 4, 4, 3])))          # -> True
print(brute_force(build_tree([1, 2, 2, None, 3, None, 3])))    # -> False
print(brute_force(build_tree([])))                             # -> True
print(brute_force(build_tree([1, 2, 3])))                      # -> False


# --- try the optimal ---
print(is_symmetric(build_tree([1, 2, 2, 3, 4, 4, 3])))          # -> True
print(is_symmetric(build_tree([1, 2, 2, None, 3, None, 3])))    # -> False
print(is_symmetric(build_tree([])))                             # -> True
print(is_symmetric(build_tree([1, 2, 3])))                      # -> False
