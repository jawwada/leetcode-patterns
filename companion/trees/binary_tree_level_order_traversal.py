"""
Binary Tree Level Order Traversal (LeetCode 102) - Medium
Chapter: trees
Pattern: BFS by level (queue snapshot)

Return the node values level by level, left to right, as a list of lists.
Example: [3, 9, 20, None, None, 15, 7] -> [[3], [9, 20], [15, 7]]
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


def collect_depth(node, depth, target, out):
    """Append the values of every node at exactly depth target, left to right."""
    if node is None:
        return
    if depth == target:
        out.append(node.val)
    else:
        collect_depth(node.left, depth + 1, target, out)
        collect_depth(node.right, depth + 1, target, out)


def brute_force(root):
    """One full walk of the tree per level. O(n*h) time."""
    result = []
    for depth in range(height(root)):
        level = []
        collect_depth(root, 0, depth, level)    # a full traversal per level
        result.append(level)
    return result


# --- optimal ---
def level_order(root):
    """A queue holds exactly one level at a time; its size says how many to pop. O(n) time."""
    if root is None:
        return []
    result = []
    queue = deque([root])
    while len(queue) > 0:
        level = []
        count = len(queue)                  # exactly the nodes of this level
        for _ in range(count):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:       # children line up behind, forming the next level
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(level)
    return result


# --- try the brute force ---
print(brute_force(build_tree([3, 9, 20, None, None, 15, 7])))   # -> [[3], [9, 20], [15, 7]]
print(brute_force(build_tree([1])))                             # -> [[1]]
print(brute_force(build_tree([])))                              # -> []
print(brute_force(build_tree([1, 2, 3, 4, None, None, 5])))     # -> [[1], [2, 3], [4, 5]]


# --- try the optimal ---
print(level_order(build_tree([3, 9, 20, None, None, 15, 7])))   # -> [[3], [9, 20], [15, 7]]
print(level_order(build_tree([1])))                             # -> [[1]]
print(level_order(build_tree([])))                              # -> []
print(level_order(build_tree([1, 2, 3, 4, None, None, 5])))     # -> [[1], [2, 3], [4, 5]]
