"""
Invert Binary Tree (LeetCode 226) - Easy
Chapter: trees
Pattern: Tree recursion (post-order)

Mirror a binary tree: swap every node's left and right children, all the way down,
and return the root.
Example: [4, 2, 7, 1, 3, 6, 9] -> [4, 7, 2, 9, 6, 3, 1]
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


def tree_to_list(root):
    """Tree -> level-order list with None for missing children, trailing Nones removed."""
    out = []
    queue = deque([root])
    while len(queue) > 0:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while len(out) > 0 and out[-1] is None:
        out.pop()
    return out


# --- brute force ---
def brute_force(root):
    """Build a brand-new mirrored copy of every node. O(n) time, O(n) extra space."""
    if root is None:
        return None
    copy = TreeNode(root.val)
    copy.left = brute_force(root.right)    # the copy's left is the mirror of the old right
    copy.right = brute_force(root.left)
    return copy


# --- optimal ---
def invert_tree(root):
    """Swap the two children of every node in place. O(n) time, O(h) stack."""
    if root is None:
        return None
    inverted_right = invert_tree(root.right)
    inverted_left = invert_tree(root.left)
    root.left = inverted_right     # swap in place: nothing is copied
    root.right = inverted_left
    return root


# --- try the brute force ---
print(tree_to_list(brute_force(build_tree([4, 2, 7, 1, 3, 6, 9]))))   # -> [4, 7, 2, 9, 6, 3, 1]
print(tree_to_list(brute_force(build_tree([2, 1, 3]))))               # -> [2, 3, 1]
print(tree_to_list(brute_force(build_tree([]))))                      # -> []
print(tree_to_list(brute_force(build_tree([1, None, 2]))))            # -> [1, 2]


# --- try the optimal ---
print(tree_to_list(invert_tree(build_tree([4, 2, 7, 1, 3, 6, 9]))))   # -> [4, 7, 2, 9, 6, 3, 1]
print(tree_to_list(invert_tree(build_tree([2, 1, 3]))))               # -> [2, 3, 1]
print(tree_to_list(invert_tree(build_tree([]))))                      # -> []
print(tree_to_list(invert_tree(build_tree([1, None, 2]))))            # -> [1, 2]
