"""
Recover Binary Search Tree (LeetCode 99) - Hard
Chapter: trees
Pattern: Inorder traversal with previous-node pointer

Exactly two nodes of a BST had their values swapped by mistake. Restore the tree without
changing its structure, by swapping the two values back.
Example: [3, 1, 4, None, None, 2] becomes [2, 1, 4, None, None, 3] because 2 and 3 were swapped.
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
def inorder(node, nodes):
    """Append the nodes of node's subtree to nodes in inorder (sorted for a valid BST)."""
    if node is None:
        return
    inorder(node.left, nodes)
    nodes.append(node)
    inorder(node.right, nodes)


def brute_force(root):
    """Collect inorder, sort the values, write them back in inorder. O(n log n) time, O(n) space."""
    nodes = []
    inorder(root, nodes)
    values = []
    for node in nodes:
        values.append(node.val)
    values.sort()                           # re-sorts a list that is already almost sorted
    for i in range(len(nodes)):
        nodes[i].val = values[i]            # rewrites every value; only two actually change


# --- optimal ---
def recover_tree(root):
    """Iterative inorder; every dip (prev > node) exposes a culprit. O(n) time, O(h) stack."""
    first = None
    second = None
    prev = None
    stack = []
    node = root
    while len(stack) > 0 or node is not None:
        while node is not None:             # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and prev.val > node.val:   # a dip in what should be increasing
            if first is None:
                first = prev                # the bump: larger value of the FIRST dip
            second = node                   # the pit: smaller value of the LAST dip
        prev = node
        node = node.right
    first.val, second.val = second.val, first.val


# --- try the brute force ---
tree = build_tree([3, 1, 4, None, None, 2])
brute_force(tree)
print(tree_to_list(tree))               # -> [2, 1, 4, None, None, 3]
tree = build_tree([1, 2])
brute_force(tree)
print(tree_to_list(tree))               # -> [2, 1]
tree = build_tree([4, 6, 2, 1, 3, 5, 7])
brute_force(tree)
print(tree_to_list(tree))               # -> [4, 2, 6, 1, 3, 5, 7]


# --- try the optimal ---
tree = build_tree([3, 1, 4, None, None, 2])
recover_tree(tree)
print(tree_to_list(tree))               # -> [2, 1, 4, None, None, 3]
tree = build_tree([1, 2])
recover_tree(tree)
print(tree_to_list(tree))               # -> [2, 1]
tree = build_tree([4, 6, 2, 1, 3, 5, 7])
recover_tree(tree)
print(tree_to_list(tree))               # -> [4, 2, 6, 1, 3, 5, 7]
