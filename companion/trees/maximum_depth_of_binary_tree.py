"""
Maximum Depth of Binary Tree (LeetCode 104) - Easy
Chapter: trees
Pattern: Tree recursion (post-order)

Return the number of nodes on the longest root-to-leaf path of a binary tree.
An empty tree has depth 0.
Example: [3, 9, 20, None, None, 15, 7] -> 3  (the path 3 -> 20 -> 15)
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
def collect_paths(node, path, paths):
    """Record every root-to-leaf path as its own list of values."""
    if node is None:
        return
    path = path + [node.val]           # a fresh copy of the prefix at every node
    if node.left is None and node.right is None:
        paths.append(path)
    collect_paths(node.left, path, paths)
    collect_paths(node.right, path, paths)


def brute_force(root):
    """List every root-to-leaf path, then take the longest. O(n*h) time and space."""
    paths = []
    collect_paths(root, [], paths)
    longest = 0
    for path in paths:
        if len(path) > longest:
            longest = len(path)
    return longest


# --- optimal ---
def max_depth(root):
    """depth(node) = 1 + max(depth(left), depth(right)). O(n) time, O(h) stack."""
    if root is None:
        return 0
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    return 1 + max(left_depth, right_depth)    # the taller child decides


# --- try the brute force ---
print(brute_force(build_tree([3, 9, 20, None, None, 15, 7])))   # -> 3
print(brute_force(build_tree([1, None, 2])))                    # -> 2
print(brute_force(build_tree([])))                              # -> 0
print(brute_force(build_tree([1, 2, None, 3, None, 4])))        # -> 4


# --- try the optimal ---
print(max_depth(build_tree([3, 9, 20, None, None, 15, 7])))   # -> 3
print(max_depth(build_tree([1, None, 2])))                    # -> 2
print(max_depth(build_tree([])))                              # -> 0
print(max_depth(build_tree([1, 2, None, 3, None, 4])))        # -> 4
