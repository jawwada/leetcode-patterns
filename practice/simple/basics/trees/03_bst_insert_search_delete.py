"""
BST Insert, Search, Delete (basics: trees)
Insert, search and delete values in a binary search tree (inserting a duplicate does nothing).
  insert 5, 3, 8, 1, 4, 9; delete 3; delete 5  ->  inorder [1, 4, 8, 9]

Idea: smaller values go left, larger go right, so every operation walks one root-to-leaf path.
      Deleting a node with 0 or 1 child: lift that child into its place. With 2 children: copy in
      the inorder successor (leftmost node of the right subtree), then delete the successor instead.

Pseudocode:
  insert(node, v): if node is None: return TreeNode(v)
                   recurse left if v < node.val, right if v > node.val; return node
  search(node, v): while node is not None and node.val != v: go left or right
                   return node is not None
  delete(node, v):
      if node is None: return None
      if v < node.val: node.left = delete(node.left, v)
      elif v > node.val: node.right = delete(node.right, v)
      elif node.left is None or node.right is None: return the other child   # 0 or 1 child
      else: node.val = successor value; node.right = delete(node.right, successor value)
      return node

Time O(h) per operation (h = height: log n when balanced, n for a chain), space O(h).
"""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def insert(node, v):
    if node is None:                     # empty spot: the new leaf goes here
        return TreeNode(v)
    if v < node.val:
        node.left = insert(node.left, v)
    elif v > node.val:                   # equal: a duplicate, ignore it
        node.right = insert(node.right, v)
    return node


def search(node, v):
    while node is not None and node.val != v:
        node = node.left if v < node.val else node.right
    return node is not None


def delete(node, v):
    if node is None:                     # v is not in the tree
        return None
    if v < node.val:
        node.left = delete(node.left, v)
    elif v > node.val:
        node.right = delete(node.right, v)
    elif node.left is None or node.right is None:
        return node.left or node.right   # 0 or 1 child: lift it up
    else:
        succ = node.right                # 2 children: the successor is the
        while succ.left:                 # leftmost node of the right subtree
            succ = succ.left
        node.val = succ.val
        node.right = delete(node.right, succ.val)  # remove the copied value
    return node


def inorder(node):                       # sorted order for a BST
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)


if __name__ == "__main__":
    root = None
    for v in [5, 3, 8, 1, 4, 9]:
        root = insert(root, v)
    print(inorder(root), search(root, 4))  # [1, 3, 4, 5, 8, 9] True
    root = delete(root, 3)                 # 2 children: successor 4 takes its place
    root = delete(root, 5)                 # the root: successor 8 takes its place
    print(inorder(root), search(root, 3))  # [1, 4, 8, 9] False
