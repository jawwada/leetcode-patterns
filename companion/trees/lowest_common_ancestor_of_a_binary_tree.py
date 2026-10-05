"""
Lowest Common Ancestor of a Binary Tree (LeetCode 236) - Medium
Chapter: trees
Pattern: Post-order "found below me" recursion

Given a binary tree (no ordering) and two nodes p and q that are both in it, return their
lowest common ancestor; a node may be its own ancestor.
Example: root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p = 5, q = 1 -> 3; p = 5, q = 4 -> 5
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


def find_node(root, value):
    """Return the node holding value (values are unique in the demos)."""
    if root is None or root.val == value:
        return root
    found = find_node(root.left, value)
    if found is not None:
        return found
    return find_node(root.right, value)


# --- brute force ---
def path_to(node, target, path):
    """Fill path with the nodes from node down to target; True if target was found below."""
    if node is None:
        return False
    path.append(node)
    if node is target:
        return True
    if path_to(node.left, target, path):
        return True
    if path_to(node.right, target, path):
        return True
    path.pop()                  # target is not under this node: undo the step
    return False


def brute_force(root, p, q):
    """Two full searches record root->p and root->q, then compare the paths. O(n) time and space."""
    path_p = []
    path_q = []
    path_to(root, p, path_p)
    path_to(root, q, path_q)
    lca = None
    for i in range(min(len(path_p), len(path_q))):
        if path_p[i] is not path_q[i]:      # the paths split here
            break
        lca = path_p[i]
    return lca


# --- optimal ---
def lowest_common_ancestor(root, p, q):
    """Each subtree reports p, q, their LCA, or None. One post-order pass: O(n) time, O(h) stack."""
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left is not None and right is not None:
        return root             # p and q are on different sides: root is the split point
    if left is not None:
        return left             # both on the left: that side already knows the answer
    return right


# --- try the brute force ---
tree = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(brute_force(tree, find_node(tree, 5), find_node(tree, 1)).val)   # -> 3
print(brute_force(tree, find_node(tree, 5), find_node(tree, 4)).val)   # -> 5
print(brute_force(tree, find_node(tree, 7), find_node(tree, 4)).val)   # -> 2


# --- try the optimal ---
tree = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(lowest_common_ancestor(tree, find_node(tree, 5), find_node(tree, 1)).val)   # -> 3
print(lowest_common_ancestor(tree, find_node(tree, 5), find_node(tree, 4)).val)   # -> 5
print(lowest_common_ancestor(tree, find_node(tree, 7), find_node(tree, 4)).val)   # -> 2
