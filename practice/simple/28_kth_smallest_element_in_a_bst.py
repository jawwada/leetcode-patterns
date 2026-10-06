"""
Kth Smallest Element in a BST (LeetCode 230)
Return the k-th smallest value (1-indexed) in a BST.
  [5, 3, 6, 2, 4, None, None, 1], k = 3  ->  3

Idea: inorder traversal of a BST visits values in sorted order.
      Do it iteratively with a stack and stop at the k-th pop.

Pseudocode:
  stack, node = [], root
  loop:
      push node and its whole left spine
      node = pop                       # next smallest
      k -= 1; if k == 0: return node.val
      node = node.right

Time O(h + k), space O(h).
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


def kth_smallest(root, k):
    stack, node = [], root
    while True:
        while node:                      # push the left spine
            stack.append(node)
            node = node.left
        node = stack.pop()               # next smallest value
        k -= 1
        if k == 0:
            return node.val
        node = node.right                # then its right subtree


if __name__ == "__main__":
    print(kth_smallest(build([3, 1, 4, None, 2]), 1))              # 1
    print(kth_smallest(build([5, 3, 6, 2, 4, None, None, 1]), 3))  # 3
