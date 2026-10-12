"""
BST Iterator - Controlled In-Order with a Stack

Design an iterator over a binary search tree: next() returns the next smallest
value and has_next() says whether any are left. Five calls to next() on
[7, 3, 15, None, None, 9, 20] -> 3, 7, 9, 15, 20.
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


# --- algorithm ---
class BSTIterator:
    """In-order iterator: the stack holds the nodes still waiting their turn."""

    def __init__(self, root):
        self.stack = []
        self.push_left(root)

    def push_left(self, node):
        """Push node and its left children; the smallest lands on top."""
        while node is not None:             # walk down the left spine
            self.stack.append(node)
            node = node.left

    def next(self):
        """Pop the smallest waiting node, then push the left spine of its
        right child. O(1) amortized, O(h) worst case."""
        node = self.stack.pop()             # the smallest value still waiting
        self.push_left(node.right)          # its successors live on the right
        return node.val

    def has_next(self):
        """True while some node is still waiting on the stack. O(1)."""
        return len(self.stack) > 0


def kth_smallest(root, k):
    """Call next() k times; the last value returned is the answer. O(h + k)."""
    iterator = BSTIterator(root)
    value = None
    for i in range(k):
        value = iterator.next()
    return value


# --- try it ---
iterator = BSTIterator(build_tree([7, 3, 15, None, None, 9, 20]))
print(iterator.next(), iterator.next(), iterator.has_next())   # -> 3 7 True
print(iterator.next(), iterator.next(), iterator.next())       # -> 9 15 20
print(iterator.has_next())                                     # -> False
root = build_tree([5, 3, 6, 2, 4, None, None, 1])
print(kth_smallest(root, 3))                                   # -> 3
