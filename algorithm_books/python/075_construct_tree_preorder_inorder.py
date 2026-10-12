"""
Construct Binary Tree from Preorder and Inorder - Preorder Picks the Root, \
Inorder Splits the Rest

Given the preorder and inorder traversals of a binary tree whose values are
all different, rebuild the tree: preorder [3, 9, 20, 15, 7] and inorder
[9, 3, 15, 20, 7] -> [3, 9, 20, None, None, 15, 7] in level order.
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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
def construct_tree(preorder, inorder):
    """Map each value to its inorder index, then build the whole range.
    O(n) time and space."""
    position = {}                           # value -> index in inorder
    for i in range(len(inorder)):
        position[inorder[i]] = i
    pre_index = [0]                         # one box every call shares
    return build(preorder, position, pre_index, 0, len(inorder) - 1)


def build(preorder, position, pre_index, lo, hi):
    """Build the subtree holding inorder[lo..hi]; the next preorder value is
    its root."""
    if lo > hi:
        return None                         # empty range: no subtree here
    value = preorder[pre_index[0]]          # roots come in preorder
    pre_index[0] += 1
    root = TreeNode(value)
    mid = position[value]                   # the root splits inorder[lo..hi]
    root.left = build(preorder, position, pre_index, lo, mid - 1)
    root.right = build(preorder, position, pre_index, mid + 1, hi)
    return root


# --- try it ---
root = construct_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
print(tree_to_list(root))                   # -> [3, 9, 20, None, None, 15, 7]
root = construct_tree([1, 2, 4, 5, 3, 6], [4, 2, 5, 1, 6, 3])
print(tree_to_list(root))                   # -> [1, 2, 3, 4, 5, 6]
print(tree_to_list(construct_tree([1, 2], [2, 1])))     # -> [1, 2]
print(tree_to_list(construct_tree([1, 2], [1, 2])))     # -> [1, None, 2]
print(tree_to_list(construct_tree([], [])))             # -> []
