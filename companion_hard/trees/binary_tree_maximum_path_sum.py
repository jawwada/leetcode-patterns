"""
Binary Tree Maximum Path Sum (LeetCode 124) - Hard
Chapter: trees
Pattern: Post-order height with side-channel answer

A path is any sequence of nodes connected by parent-child edges, each node used at most
once; it need not pass through the root or end at a leaf. Return the maximum sum of node
values over all non-empty paths.
Example: [-10, 9, 20, None, None, 15, 7] -> 42 via 15 -> 20 -> 7.
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
def gain(node):
    """Best sum of a path that starts at node and goes down one side, never below 0."""
    if node is None:
        return 0
    return node.val + max(gain(node.left), gain(node.right), 0)


def brute_force(root):
    """Try every node as the path's top, recomputing both downward gains each time. O(n^2)."""
    if root is None:
        return -math.inf                # math.inf: larger than any number
    here = root.val + max(gain(root.left), 0) + max(gain(root.right), 0)  # path bending at root
    return max(here, brute_force(root.left), brute_force(root.right))


# --- optimal ---
def gain_and_record(node, best):
    """Best downward path from node (never negative); records bending paths in best[0]."""
    if node is None:
        return 0
    left = max(gain_and_record(node.left, best), 0)      # a negative arm is simply left out
    right = max(gain_and_record(node.right, best), 0)
    best[0] = max(best[0], node.val + left + right)      # path bending at this node: a candidate
    return node.val + max(left, right)                   # only one arm continues up to the parent


def max_path_sum(root):
    """One post-order pass: each node's gain is computed once. O(n) time, O(h) stack."""
    best = [-math.inf]              # a one-item list so the helper can update it in place
    gain_and_record(root, best)
    return best[0]


# --- try the brute force ---
wide = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]
print(brute_force(build_tree([1, 2, 3])))                          # -> 6
print(brute_force(build_tree([-10, 9, 20, None, None, 15, 7])))    # -> 42
print(brute_force(build_tree([-2, -1, -3])))                       # -> -1
print(brute_force(build_tree(wide)))                               # -> 48


# --- try the optimal ---
wide = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]
print(max_path_sum(build_tree([1, 2, 3])))                         # -> 6
print(max_path_sum(build_tree([-10, 9, 20, None, None, 15, 7])))   # -> 42
print(max_path_sum(build_tree([-2, -1, -3])))                      # -> -1
print(max_path_sum(build_tree(wide)))                              # -> 48
