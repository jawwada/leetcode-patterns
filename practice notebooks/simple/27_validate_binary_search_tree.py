"""
Validate Binary Search Tree (LeetCode 98)
Return True if the tree is a valid BST (left < node < right for whole subtrees).
  [5, 1, 4, None, None, 3, 6]  ->  False   (4 sits right of 5 but is smaller)

Idea: every node must fit in an open window (lo, hi) inherited from its ancestors.
      Going left tightens hi to the node's value; going right tightens lo.

Pseudocode:
  valid(node, lo, hi):
      if node is None: return True
      if not lo < node.val < hi: return False
      return valid(left, lo, node.val) and valid(right, node.val, hi)
  valid(root, -inf, +inf)

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


def is_valid_bst(root):
    def valid(node, lo, hi):
        if node is None:
            return True
        if not (lo < node.val < hi):     # outside its window
            return False
        return (valid(node.left, lo, node.val) and     # left: cap hi
                valid(node.right, node.val, hi))       # right: raise lo

    return valid(root, float("-inf"), float("inf"))


if __name__ == "__main__":
    print(is_valid_bst(build([2, 1, 3])))                     # True
    print(is_valid_bst(build([5, 1, 4, None, None, 3, 6])))   # False
    print(is_valid_bst(build([5, 4, 6, None, None, 3, 7])))   # False (3 < 5 in right subtree)
