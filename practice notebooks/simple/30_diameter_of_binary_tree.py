"""
Diameter of Binary Tree (LeetCode 543)
Return the number of edges on the longest path between any two nodes.
  [1, 2, 3, 4, 5]  ->  3   (4 -> 2 -> 1 -> 3)

Idea: the longest path bends at some node: left arm + right arm.
      One post-order pass returns each subtree's height and, while both arms
      are known, records left + right as a candidate.

Pseudocode:
  height(node):
      if node is None: return 0
      left, right = height(node.left), height(node.right)
      best = max(best, left + right)   # path bending here
      return 1 + max(left, right)

Time O(n), space O(h) recursion.
"""


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


def diameter_of_binary_tree(root):
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)   # path bending at this node
        return 1 + max(left, right)      # longest arm going up

    height(root)
    return best


if __name__ == "__main__":
    print(diameter_of_binary_tree(build([1, 2, 3, 4, 5])))  # 3
    print(diameter_of_binary_tree(build([1, 2])))           # 1
