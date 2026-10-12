"""
Diameter and Max Path Sum - Postorder DFS That Returns a Height

The diameter of a binary tree is the number of edges on its longest path; the
max path sum is the largest total of values along any path of at least one
node: [1, 2, 3, 4, 5] -> diameter 3, [-10, 9, 20, None, None, 15, 7] -> 42.
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


# --- algorithm ---
def diameter(root):
    """Longest path in edges: every node offers left + right. O(n)."""
    best = [0]                              # a box every call can update
    height(root, best)
    return best[0]


def height(node, best):
    """Nodes on the longest downward path from node; record the bend here."""
    if node is None:
        return 0
    left = height(node.left, best)
    right = height(node.right, best)
    best[0] = max(best[0], left + right)    # the path that bends at node
    return 1 + max(left, right)             # only one arm continues upward


def max_path_sum(root):
    """Largest path sum in a non-empty tree; negative arms are cut. O(n)."""
    best = [root.val]                       # one node alone is a path
    gain(root, best)
    return best[0]


def gain(node, best):
    """Best sum of a downward path from node; record the bend here."""
    if node is None:
        return 0
    left = max(gain(node.left, best), 0)    # a negative arm is cut off
    right = max(gain(node.right, best), 0)
    best[0] = max(best[0], node.val + left + right)
    return node.val + max(left, right)


# --- try it ---
root = build_tree([1, 2, 3, 4, 5])
print(diameter(root))                       # -> 3
root = build_tree([-10, 9, 20, None, None, 15, 7])
print(max_path_sum(root))                   # -> 42
root = build_tree([1, 2, None, 3, 4, 5, None, None, 6])
print(diameter(root))                       # -> 4
print(max_path_sum(build_tree([-3, -1, -2])))   # -> -1
print(diameter(build_tree([7])))            # -> 0
