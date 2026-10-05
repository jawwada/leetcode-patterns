"""
BST Insert, Search, Delete - Fundamentals
Chapter: fundamentals/trees
Key operations: descend by comparison, attach a leaf, splice out a 0/1-child node, successor swap

Maintain a binary search tree (every value in the left subtree is smaller, in the right subtree
bigger; duplicates are ignored). Each operation walks one root-to-leaf path, so it costs O(height),
and the inorder traversal reads the values back in sorted order.
Example: insert 5, 3, 8, 1, 4, 9; search 4; delete 3; delete 5; search 3
-> searches [True, False], inorder [1, 4, 8, 9]
"""


# --- helpers ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# --- algorithm ---
def insert(root, val):
    """Descend by comparison; attach the new value as a leaf where the walk falls off. O(h)."""
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root                             # equal: a duplicate, nothing changes


def search(root, val):
    """Walk down one path: left when smaller, right when bigger. O(height)."""
    node = root
    while node is not None:
        if val == node.val:
            return True
        if val < node.val:
            node = node.left
        else:
            node = node.right
    return False


def smallest(node):
    """Leftmost node of a subtree: the inorder successor of the node above it."""
    while node.left is not None:
        node = node.left
    return node


def delete(root, val):
    """Find the node; 0 or 1 child: the child takes its place; 2 children: copy the successor."""
    if root is None:
        return None
    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    elif root.left is None:                 # at most one child: splice the node out
        return root.right
    elif root.right is None:
        return root.left
    else:
        successor = smallest(root.right)
        root.val = successor.val
        root.right = delete(root.right, successor.val)   # delete the SUCCESSOR's value, not val
    return root


def inorder(root):
    """Left, node, right: sorted order for a BST. O(n)."""
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def build_bst(values):
    """Insert the values one by one into an empty tree."""
    root = None
    for val in values:
        root = insert(root, val)
    return root


# --- try it ---
root = build_bst([5, 3, 8, 1, 4, 9])
print(inorder(root))                                   # -> [1, 3, 4, 5, 8, 9]
print(search(root, 4))                                 # -> True
root = delete(root, 3)
print(inorder(root))                                   # -> [1, 4, 5, 8, 9]
root = delete(root, 5)
print(inorder(root))                                   # -> [1, 4, 8, 9]
print(search(root, 3))                                 # -> False
print(inorder(build_bst([2, 2, 1])))                   # -> [1, 2]
print(inorder(delete(build_bst([1, 2, 3]), 2)))        # -> [1, 3]
print(inorder(delete(build_bst([2, 1, 3]), 2)))        # -> [1, 3]
