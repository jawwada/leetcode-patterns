"""
Balanced Binary Tree (basics: trees)
Return True if, at every node, the heights of the two subtrees differ by at most 1.
  [3, 9, 20, None, None, 15, 7]  ->  True

Idea: one post-order pass. Each node returns its height, or -1 as soon as anything below it
      is unbalanced; the -1 is then passed straight up and no other heights are computed.

Pseudocode:
  height(node):
      if node is None: return 0
      left = height(node.left);   if left == -1: return -1
      right = height(node.right); if right == -1: return -1
      if abs(left - right) > 1: return -1
      return 1 + max(left, right)
  balanced = height(root) != -1

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


def is_balanced(root):
    def height(node):                    # height, or -1 if unbalanced below
        if node is None:
            return 0
        left = height(node.left)
        if left == -1:                   # stop early: already unbalanced
            return -1
        right = height(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:        # this node breaks the rule
            return -1
        return 1 + max(left, right)

    return height(root) != -1


if __name__ == "__main__":
    print(is_balanced(build([3, 9, 20, None, None, 15, 7])))      # True
    print(is_balanced(build([1, 2, 2, 3, 3, None, None, 4, 4])))  # False
    print(is_balanced(build([])))                                 # True
