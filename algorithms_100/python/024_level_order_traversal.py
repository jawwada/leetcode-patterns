"""
Binary Tree Level-Order Traversal - BFS One Level at a Time

Given the root of a binary tree, return its values level by level, each level
read left to right: the tree [3, 9, 20, None, None, 15, 7] ->
[[3], [9, 20], [15, 7]].
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
def level_order(root):
    """BFS; the queue length at the top of each round is one level. O(n)."""
    levels = []
    if root is None:
        return levels
    queue = deque([root])
    while queue:
        size = len(queue)               # snapshot: exactly this level's nodes
        level = []
        for i in range(size):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:   # children join the back of the queue
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        levels.append(level)            # the level is complete
    return levels


# --- try it ---
root = build_tree([3, 9, 20, None, None, 15, 7])
print(level_order(root))                # -> [[3], [9, 20], [15, 7]]
root = build_tree([1, 2, 3, 4, None, None, 5])
print(level_order(root))                # -> [[1], [2, 3], [4, 5]]
print(level_order(build_tree([1])))     # -> [[1]]
print(level_order(build_tree([])))      # -> []
