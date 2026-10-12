"""
Binary Tree Level Order Traversal (LeetCode 102)
Return the node values level by level, left to right.
  [3, 9, 20, None, None, 15, 7]  ->  [[3], [9, 20], [15, 7]]

Idea: BFS with a queue. At the start of each round the queue holds exactly
      one level, so pop len(queue) nodes while their children line up behind.

Pseudocode:
  queue = [root]
  while queue:
      level = []
      repeat len(queue) times:
          node = pop front; level.append(node.val)
          push node's children
      levels.append(level)

Time O(n), space O(width).
"""
from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build(values):
    """LeetCode level-order list (None = missing child) -> root."""
    nodes = [TreeNode(v) if v is not None else None for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


def level_order(root):
    if root is None:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):      # exactly one level
            node = queue.popleft()
            level.append(node.val)
            if node.left:                # children wait behind this level
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels


if __name__ == "__main__":
    print(level_order(build([3, 9, 20, None, None, 15, 7])))  # [[3], [9, 20], [15, 7]]
    print(level_order(build([1])))                            # [[1]]
    print(level_order(build([])))                             # []
