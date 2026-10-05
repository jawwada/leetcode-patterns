"""
Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105) - Medium
Chapter: trees
Pattern: Recursive tree construction with index map

Given the preorder and inorder traversals of a binary tree with unique values, rebuild
the tree.
Example: preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7] -> [3, 9, 20, None, None, 15, 7]
"""
from collections import deque


# --- helpers ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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
def brute_force(preorder, inorder):
    """preorder[0] is the root; find it in inorder, slice both lists, recurse. O(n^2) time."""
    if len(preorder) == 0:
        return None
    root = TreeNode(preorder[0])
    mid = inorder.index(root.val)              # linear scan for the root
    left_size = mid                            # everything left of the root in inorder
    left_pre = preorder[1:1 + left_size]           # slice copies at every call
    right_pre = preorder[1 + left_size:len(preorder)]
    root.left = brute_force(left_pre, inorder[0:mid])
    root.right = brute_force(right_pre, inorder[mid + 1:len(inorder)])
    return root


# --- optimal ---
def make(pre_queue, index, lo, hi):
    """Build the subtree whose inorder values are inorder[lo:hi], eating preorder front to back."""
    if lo >= hi:
        return None
    root = TreeNode(pre_queue.popleft())       # the next preorder value is always the next root
    mid = index[root.val]
    root.left = make(pre_queue, index, lo, mid)         # uses exactly mid - lo preorder values
    root.right = make(pre_queue, index, mid + 1, hi)
    return root


def construct_tree(preorder, inorder):
    """Hash map for the root's position, index bounds instead of slices. O(n) time and space."""
    index = {}
    for i in range(len(inorder)):
        index[inorder[i]] = i
    pre_queue = deque(preorder)        # deque: popleft is O(1)
    return make(pre_queue, index, 0, len(inorder))


# --- try the brute force ---
pre, ino = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
print(tree_to_list(brute_force(pre, ino)))                  # -> [3, 9, 20, None, None, 15, 7]
print(tree_to_list(brute_force([1, 2], [1, 2])))                     # -> [1, None, 2]
print(tree_to_list(brute_force([1, 2, 4, 5, 3], [4, 2, 5, 1, 3])))   # -> [1, 2, 3, 4, 5]
print(tree_to_list(brute_force([], [])))                             # -> []


# --- try the optimal ---
pre, ino = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
print(tree_to_list(construct_tree(pre, ino)))                  # -> [3, 9, 20, None, None, 15, 7]
print(tree_to_list(construct_tree([1, 2], [1, 2])))                     # -> [1, None, 2]
print(tree_to_list(construct_tree([1, 2, 4, 5, 3], [4, 2, 5, 1, 3])))   # -> [1, 2, 3, 4, 5]
print(tree_to_list(construct_tree([], [])))                             # -> []
