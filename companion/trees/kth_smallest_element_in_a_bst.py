"""
Kth Smallest Element in a BST (LeetCode 230) - Medium
Chapter: trees
Pattern: Iterative in-order traversal with early stop

Given the root of a BST and an integer k, return the k-th smallest value (1-indexed).
Example: [3, 1, 4, None, 2], k = 1 -> 1; [5, 3, 6, 2, 4, None, None, 1], k = 3 -> 3
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
def collect_values(node, vals):
    """Append every value in the subtree, in any order."""
    if node is None:
        return
    vals.append(node.val)
    collect_values(node.left, vals)
    collect_values(node.right, vals)


def brute_force(root, k):
    """Dump every value, sort, index. O(n log n) time; ignores that the BST is already ordered."""
    vals = []
    collect_values(root, vals)
    vals.sort()
    return vals[k - 1]


# --- optimal ---
def kth_smallest(root, k):
    """Iterative in-order walk that stops at the k-th visited node. O(h + k) time, O(h) space."""
    stack = []
    node = root
    while True:
        while node is not None:         # slide left: the smallest unvisited value ends on top
            stack.append(node)
            node = node.left
        node = stack.pop()              # the next value in sorted order
        k = k - 1
        if k == 0:
            return node.val
        node = node.right


# --- try the brute force ---
print(brute_force(build_tree([3, 1, 4, None, 2]), 1))                  # -> 1
print(brute_force(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3))      # -> 3
print(brute_force(build_tree([5, 3, 6, 2, 4, None, None, 1]), 6))      # -> 6
print(brute_force(build_tree([2, 1, 3]), 2))                           # -> 2


# --- try the optimal ---
print(kth_smallest(build_tree([3, 1, 4, None, 2]), 1))                  # -> 1
print(kth_smallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3))      # -> 3
print(kth_smallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 6))      # -> 6
print(kth_smallest(build_tree([2, 1, 3]), 2))                           # -> 2
