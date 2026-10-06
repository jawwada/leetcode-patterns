"""
Lowest Common Ancestor of a Binary Tree (basics: trees)
Return the lowest node that has both p and q in its subtree (a node counts as its own descendant).
  [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p = 5, q = 4  ->  5

Idea: post-order search. A call returns p or q if it meets one (or the LCA, once found).
      If the left and the right subtree BOTH report a find, the paths split at this node,
      so it is the LCA; otherwise pass up whichever side found something.

Pseudocode:
  lca(node):
      if node is None: return None
      if node.val == p or node.val == q: return node      # found a target
      left, right = lca(node.left), lca(node.right)
      if left is not None and right is not None: return node  # one target on each side
      return left if left is not None else right          # pass up what was found

Here p and q are values that are in the tree (LeetCode passes nodes).
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


def lowest_common_ancestor(root, p, q):
    def lca(node):
        if node is None:
            return None
        if node.val == p or node.val == q:   # found a target: report it up
            return node
        left = lca(node.left)
        right = lca(node.right)
        if left and right:               # one target on each side: they split here
            return node
        return left or right             # pass up whatever was found

    return lca(root).val


if __name__ == "__main__":
    root = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    print(lowest_common_ancestor(root, 5, 1))  # 3
    print(lowest_common_ancestor(root, 5, 4))  # 5
    print(lowest_common_ancestor(root, 7, 4))  # 2
