"""
Binary Tree Inorder Traversal (LeetCode 94) - Easy
Chapter: trees
Pattern: Iterative traversal with an explicit stack

Return the values of a binary tree in inorder: left subtree, then the node, then the
right subtree. The follow-up asks for an iterative solution.
Example: [1, None, 2, 3] -> [1, 3, 2]
"""
from collections import deque


# --- helpers ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(vals):
    """Level-order list (None = missing child) -> tree, the LeetCode input format."""
    if len(vals) == 0 or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])          # deque: popleft is O(1)
    i = 1
    while len(queue) > 0 and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


# --- brute force ---
def inorder(node, out):
    """Left subtree, then the node, then the right subtree; the call stack remembers the way."""
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)


def brute_force(root):
    """Textbook recursion. O(n) time, O(h) hidden stack (overflows on very tall trees)."""
    out = []
    inorder(root, out)
    return out


# --- optimal ---
def inorder_traversal(root):
    """Replace the call stack with an explicit stack of nodes. O(n) time, O(h) space."""
    out = []
    stack = []
    node = root
    while node is not None or len(stack) > 0:
        while node is not None:         # slide down the left spine, remembering each node
            stack.append(node)
            node = node.left
        node = stack.pop()              # its left side is finished: visit it
        out.append(node.val)
        node = node.right               # then do the same inside the right subtree
    return out


# --- try the brute force ---
print(brute_force(build_tree([1, None, 2, 3])))              # -> [1, 3, 2]
print(brute_force(build_tree([])))                           # -> []
print(brute_force(build_tree([4, 2, 6, 1, 3, 5, 7])))        # -> [1, 2, 3, 4, 5, 6, 7]
print(brute_force(build_tree([1, 2, None, 3])))              # -> [3, 2, 1]


# --- try the optimal ---
print(inorder_traversal(build_tree([1, None, 2, 3])))              # -> [1, 3, 2]
print(inorder_traversal(build_tree([])))                           # -> []
print(inorder_traversal(build_tree([4, 2, 6, 1, 3, 5, 7])))        # -> [1, 2, 3, 4, 5, 6, 7]
print(inorder_traversal(build_tree([1, 2, None, 3])))              # -> [3, 2, 1]
