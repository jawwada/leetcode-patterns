"""
Level Order and Height (basics: trees)
Return a binary tree's values level by level, and its height in levels (an empty tree has height 0).
  [3, 9, 20, None, None, 15, 7]  ->  levels [[3], [9, 20], [15, 7]], height 3

Idea: BFS with a queue. At the start of each round the queue holds exactly one level,
      so pop len(queue) nodes while their children line up behind them.
      One round = one level, so the height is just the number of rounds.

Pseudocode:
  queue = [root]
  while queue:
      level = []
      repeat len(queue) times:
          node = pop front; level.append(node.val)
          push node's children
      levels.append(level)
  return levels, len(levels)

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


def level_order_and_height(root):
    levels = []
    queue = deque([root] if root else [])
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
    return levels, len(levels)           # one round per level = the height


if __name__ == "__main__":
    root = build([3, 9, 20, None, None, 15, 7])
    print(level_order_and_height(root))                    # ([[3], [9, 20], [15, 7]], 3)
    print(level_order_and_height(build([1, 2, None, 3])))  # ([[1], [2], [3]], 3)
    print(level_order_and_height(build([])))               # ([], 0)
