"""
Diameter of Binary Tree (LeetCode 543) - Easy
Chapter: trees
Pattern: Post-order height with side-channel answer

The diameter of a binary tree is the number of edges on the longest path between any
two nodes; the path need not pass through the root.
Example: [1, 2, 3, 4, 5] -> 3  (the path 4 -> 2 -> 1 -> 3)
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
    """At each node the longest path bending there is height(left) + height(right). O(n^2) worst."""
    if root is None:
        return 0
    through_root = height(root.left) + height(root.right)   # heights recomputed for every node
    return max(through_root, brute_force(root.left), brute_force(root.right))


# --- optimal ---
def height_and_best(node):
    """Return (height of node's subtree, longest path inside it), both measured in one pass."""
    if node is None:
        return 0, 0
    left_height, left_best = height_and_best(node.left)
    right_height, right_best = height_and_best(node.right)
    through_node = left_height + right_height      # the path that bends at this node
    best = max(through_node, left_best, right_best)
    return 1 + max(left_height, right_height), best


def diameter_of_binary_tree(root):
    """One post-order pass computes each height exactly once. O(n) time, O(h) stack."""
    root_height, best = height_and_best(root)
    return best


# --- try the brute force ---
print(brute_force(build_tree([1, 2, 3, 4, 5])))            # -> 3
print(brute_force(build_tree([1, 2])))                     # -> 1
print(brute_force(build_tree([])))                         # -> 0
print(brute_force(build_tree([1, None, 2, None, 3])))      # -> 2


# --- try the optimal ---
print(diameter_of_binary_tree(build_tree([1, 2, 3, 4, 5])))            # -> 3
print(diameter_of_binary_tree(build_tree([1, 2])))                     # -> 1
print(diameter_of_binary_tree(build_tree([])))                         # -> 0
print(diameter_of_binary_tree(build_tree([1, None, 2, None, 3])))      # -> 2
