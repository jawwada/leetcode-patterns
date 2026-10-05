"""
Closest Binary Search Tree Value II (LeetCode 272) - Hard
Chapter: trees
Pattern: Two lazy inorder iterators (predecessor / successor stacks)

Given a BST, a float target and an integer k (at most the number of nodes), return the k
values closest to target, in any order.
Example: root = [4, 2, 5, 1, 3], target = 3.714286, k = 2 -> [4, 3].
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
def inorder(node, vals):
    """Append every value of node's subtree to vals in sorted (inorder) order."""
    if node is None:
        return
    inorder(node.left, vals)
    vals.append(node.val)
    inorder(node.right, vals)


def brute_force(root, target, k):
    """List all n values, sort them by distance to target, keep k. O(n log n) time, O(n) space."""
    vals = []
    inorder(root, vals)
    by_distance = []
    for value in vals:
        by_distance.append((abs(value - target), value))
    by_distance.sort()                      # all n sorted, although only k matter
    out = []
    for distance, value in by_distance[:k]:
        out.append(value)
    return out


# --- optimal ---
def next_pred(pred):
    """Pop the largest value <= target, then expose the next largest below it."""
    node = pred.pop()
    child = node.left                       # everything smaller lives in the left subtree
    while child is not None:
        pred.append(child)
        child = child.right                 # ... and its largest is down the right spine
    return node.val


def next_succ(succ):
    """Pop the smallest value > target, then expose the next smallest above it."""
    node = succ.pop()
    child = node.right
    while child is not None:
        succ.append(child)
        child = child.left
    return node.val


def closest_k_values(root, target, k):
    """Two stacks walk away from target like sorted streams; merge k steps. O(h + k) time."""
    pred = []                               # nodes <= target, top is the largest of them
    succ = []                               # nodes > target, top is the smallest of them
    node = root
    while node is not None:                 # one root-to-leaf search path fills both stacks
        if node.val <= target:
            pred.append(node)
            node = node.right
        else:
            succ.append(node)
            node = node.left
    out = []
    for step in range(k):
        if len(succ) == 0:
            out.append(next_pred(pred))
        elif len(pred) > 0 and target - pred[-1].val <= succ[-1].val - target:
            out.append(next_pred(pred))     # the predecessor side is closer (or tied)
        else:
            out.append(next_succ(succ))
    return out


# --- try the brute force ---
big = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
print(sorted(brute_force(build_tree([4, 2, 5, 1, 3]), 3.714286, 2)))   # -> [3, 4]
print(sorted(brute_force(build_tree([4, 2, 5, 1, 3]), 0.5, 2)))        # -> [1, 2]
print(sorted(brute_force(build_tree([4, 2, 5, 1, 3]), 9.0, 3)))        # -> [3, 4, 5]
print(sorted(brute_force(build_tree(big), 6.5, 4)))                    # -> [5, 6, 7, 8]


# --- try the optimal ---
big = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
print(sorted(closest_k_values(build_tree([4, 2, 5, 1, 3]), 3.714286, 2)))   # -> [3, 4]
print(sorted(closest_k_values(build_tree([4, 2, 5, 1, 3]), 0.5, 2)))        # -> [1, 2]
print(sorted(closest_k_values(build_tree([4, 2, 5, 1, 3]), 9.0, 3)))        # -> [3, 4, 5]
print(sorted(closest_k_values(build_tree(big), 6.5, 4)))                    # -> [5, 6, 7, 8]
