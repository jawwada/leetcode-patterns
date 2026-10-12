"""
BST Search, Insert, Delete - Delete with the In-Order Successor

Search, insert and delete values in a binary search tree while keeping its
order (smaller to the left, larger to the right). Deleting 3 from
[5, 3, 6, 2, 4, None, 7] -> [5, 4, 6, 2, None, None, 7].
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build a tree from a level-order list with None for missing children."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    """Level-order list with None for gaps, trailing Nones removed."""
    values = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while values and values[-1] is None:
        values.pop()
    return values


# --- algorithm ---
def search(root, val):
    """Walk down one path: left if smaller, right if larger. O(h)."""
    node = root
    while node is not None and node.val != val:
        if val < node.val:
            node = node.left
        else:
            node = node.right
    return node                             # the node holding val, or None


def insert(root, val):
    """Descend to the empty spot where val belongs; hang a leaf there. O(h)."""
    if root is None:
        return TreeNode(val)                # the empty spot: a new leaf
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root                             # equal: already present


def delete(root, val):
    """Remove val; a node with two children takes its successor. O(h)."""
    if root is None:
        return None                         # val is not in the tree
    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:
        if root.left is None:               # leaf, or right child only
            return root.right
        if root.right is None:              # left child only
            return root.left
        successor = root.right              # two children: leftmost node
        while successor.left is not None:   # of the right subtree
            successor = successor.left
        root.val = successor.val            # copy it up...
        root.right = delete(root.right, successor.val)  # ...and remove it
    return root


# --- try it ---
root = build_tree([5, 3, 6, 2, 4, None, 7])
print(tree_to_list(search(root, 3)))        # -> [3, 2, 4]
root = delete(root, 3)
print(tree_to_list(root))                   # -> [5, 4, 6, 2, None, None, 7]
print(search(root, 3))                      # -> None
root = insert(root, 1)
print(tree_to_list(root))                   # -> [5, 4, 6, 2, None, None, 7, 1]
