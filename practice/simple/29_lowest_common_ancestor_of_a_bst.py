"""
Lowest Common Ancestor of a BST (LeetCode 235)
Return the lowest node that has both p and q in its subtree (a node counts as its own descendant).
  [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 2, q = 8  ->  6

Idea: walk down from the root. If both values are smaller go left, if both are
      larger go right. Otherwise p and q split here (or one of them is here): that's the LCA.

Pseudocode:
  node = root
  while node:
      if p < node.val and q < node.val: node = node.left     # both smaller
      elif p > node.val and q > node.val: node = node.right  # both larger
      else: return node

Here p and q are values (LeetCode passes nodes: use p.val, q.val).
Time O(h), space O(1).
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


def lowest_common_ancestor(root, p, q):
    node = root
    while node:
        if p < node.val and q < node.val:    # both on the left
            node = node.left
        elif p > node.val and q > node.val:  # both on the right
            node = node.right
        else:                                # paths split here
            return node


if __name__ == "__main__":
    root = build([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    print(lowest_common_ancestor(root, 2, 8).val)  # 6
    print(lowest_common_ancestor(root, 2, 4).val)  # 2
    print(lowest_common_ancestor(root, 3, 5).val)  # 4
