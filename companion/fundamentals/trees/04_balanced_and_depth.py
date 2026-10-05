"""
Balanced Binary Tree (LeetCode 110) - Fundamentals
Chapter: fundamentals/trees
Key operations: post-order height, pass -1 upward as soon as a subtree fails, abs(left - right) > 1

The depth (height) of a tree is 1 + the taller child's depth, computed bottom up. A tree is
height-balanced when at every node the two subtree heights differ by at most 1: the same bottom-up
walk returns the height, or -1 the moment any subtree fails, so the check costs one O(n) pass.
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


# --- algorithm ---
def max_depth(node):
    """Post-order: a node is one level above its taller child; an empty tree has depth 0. O(n)."""
    if node is None:
        return 0
    return 1 + max(max_depth(node.left), max_depth(node.right))


def checked_height(node):
    """The height of a balanced subtree, or -1 as soon as any subtree is unbalanced. O(n)."""
    if node is None:
        return 0
    left = checked_height(node.left)
    if left == -1:
        return -1                           # pass the failure straight up, no more work
    right = checked_height(node.right)
    if right == -1:
        return -1
    if abs(left - right) > 1:               # a difference of exactly 1 is still balanced
        return -1
    return 1 + max(left, right)


def is_balanced(root):
    """Balanced unless the height walk reported -1."""
    return checked_height(root) != -1


# --- try it ---
print(max_depth(build_tree([3, 9, 20, None, None, 15, 7])))      # -> 3
print(is_balanced(build_tree([3, 9, 20, None, None, 15, 7])))    # -> True
print(is_balanced(build_tree([1, 2, 2, 3, 3, None, None, 4, 4])))   # -> False
print(is_balanced(build_tree([1, 2])))                           # -> True
print(max_depth(build_tree([1, None, 2, None, 3])))              # -> 3
print(is_balanced(build_tree([1, None, 2, None, 3])))            # -> False
print(is_balanced(build_tree([])))                               # -> True
