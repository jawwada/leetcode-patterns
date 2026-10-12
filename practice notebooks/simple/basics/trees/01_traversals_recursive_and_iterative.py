"""
Tree Traversals, Recursive and Iterative (basics: trees)
List a binary tree's preorder, inorder and postorder values, recursively and with a stack.
  [1, 2, 3, 4, 5, None, 6]  ->  preorder [1, 2, 4, 5, 3, 6], inorder [4, 2, 5, 1, 3, 6],
                                postorder [4, 5, 2, 6, 3, 1]

Idea: the orders differ only in WHEN a node is recorded: before, between or after its children.
      A stack can replace the recursion: preorder pushes right before left so left pops first;
      inorder runs down the left edge pushing nodes, pops one, records it, then goes right.

Pseudocode:
  walk(node):                                   # one recursive walk, all three orders
      if node is None: return
      preorder += node; walk(left); inorder += node; walk(right); postorder += node

  preorder_iterative(root):
      stack = [root]
      while stack: node = pop; record node; push node.right, then node.left

  inorder_iterative(root):
      stack = [], node = root
      while stack is not empty or node is not None:
          while node: push node; node = node.left   # run down the left edge
          node = pop; record node; node = node.right

Time O(n), space O(h) for the recursion or the stack.
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


def traversals_recursive(root):
    preorder, inorder, postorder = [], [], []

    def walk(node):
        if node is None:
            return
        preorder.append(node.val)        # before the children
        walk(node.left)
        inorder.append(node.val)         # between them
        walk(node.right)
        postorder.append(node.val)       # after them

    walk(root)
    return preorder, inorder, postorder


def preorder_iterative(root):
    out = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:                   # right goes in first ...
            stack.append(node.right)
        if node.left:                    # ... so left is on top and pops next
            stack.append(node.left)
    return out


def inorder_iterative(root):
    out, stack, node = [], [], root
    while stack or node:
        while node:                      # run down the left edge
            stack.append(node)
            node = node.left
        node = stack.pop()               # leftmost node not yet recorded
        out.append(node.val)
        node = node.right                # then its right subtree
    return out


if __name__ == "__main__":
    root = build([1, 2, 3, 4, 5, None, 6])
    print(traversals_recursive(root))
    # ([1, 2, 4, 5, 3, 6], [4, 2, 5, 1, 3, 6], [4, 5, 2, 6, 3, 1])
    print(preorder_iterative(root))      # [1, 2, 4, 5, 3, 6]
    print(inorder_iterative(root))       # [4, 2, 5, 1, 3, 6]
