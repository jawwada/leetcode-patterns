"""
Level Order and Height - Fundamentals
Chapter: fundamentals/trees
Key operations: range(len(queue)) drains one level, popleft, push children, levels count as height

Return the values of a binary tree level by level, and its height counted in levels (number of
nodes on the longest root-to-leaf path; an empty tree has height 0). The queue holds exactly one
level at a time: drain the nodes in it when the level starts, their children form the next level.
Example: [3, 9, 20, None, None, 15, 7] -> levels [[3], [9, 20], [15, 7]], height 3
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
def level_order(root):
    """BFS where the queue holds exactly one level; drain len(queue) nodes per round. O(n)."""
    levels = []
    queue = deque()                     # deque: popleft is O(1)
    if root is not None:
        queue.append(root)
    while len(queue) > 0:
        level = []
        for _ in range(len(queue)):     # only the nodes present when the level starts
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:   # the children join the queue for the next round
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        levels.append(level)
    return levels


def height(root):
    """Height in levels = number of BFS rounds; an empty tree has height 0, a single node 1."""
    return len(level_order(root))


# --- try it ---
print(level_order(build_tree([3, 9, 20, None, None, 15, 7])))   # -> [[3], [9, 20], [15, 7]]
print(height(build_tree([3, 9, 20, None, None, 15, 7])))        # -> 3
print(level_order(build_tree([1, None, 2, None, 3])))           # -> [[1], [2], [3]]
print(height(build_tree([1])))                                  # -> 1
print(level_order(build_tree([])))                              # -> []
print(height(build_tree([])))                                   # -> 0
