"""
Binary Tree Cameras (LeetCode 968) - Hard
Chapter: trees
Pattern: Greedy post-order with 3-state return

A camera on a node monitors that node, its parent and its children. Return the minimum
number of cameras needed to monitor every node.
Example: [0, 0, None, 0, 0] returns 1: a camera on the middle node covers the root and both leaves.
"""
from collections import deque
from itertools import combinations


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
def collect(node, par, nodes, parent):
    """List every node and remember its parent."""
    if node is None:
        return
    nodes.append(node)
    parent[node] = par
    collect(node.left, node, nodes, parent)
    collect(node.right, node, nodes, parent)


def all_covered(nodes, parent, cameras):
    """True if every node has a camera on itself, its parent or one of its children."""
    for node in nodes:
        if node in cameras or parent[node] in cameras:
            continue
        if node.left in cameras or node.right in cameras:
            continue
        return False
    return True


def brute_force(root):
    """Try every subset of nodes as camera spots, smallest subsets first. O(2^n * n) time."""
    nodes = []
    parent = {}
    collect(root, None, nodes, parent)
    for size in range(len(nodes) + 1):
        for chosen in combinations(nodes, size):    # every way to pick size nodes
            if all_covered(nodes, parent, set(chosen)):
                return size                         # the first size that works is the minimum
    return 0


# --- optimal ---
NEEDS = 0           # not monitored: the parent must place a camera
COVERED = 1         # monitored, no camera here
HAS_CAMERA = 2


def dfs(node, count):
    """Report the subtree's state to the parent; count[0] holds the cameras placed so far."""
    if node is None:
        return COVERED                  # an empty child never asks for a camera: leaves say NEEDS
    left = dfs(node.left, count)
    right = dfs(node.right, count)
    if left == NEEDS or right == NEEDS:
        count[0] += 1                   # forced: a child is still dark, so the camera goes here
        return HAS_CAMERA
    if left == HAS_CAMERA or right == HAS_CAMERA:
        return COVERED                  # lit from below, no camera of our own
    return NEEDS                        # both children fine, nobody lights this node yet


def min_camera_cover(root):
    """Post-order greedy: place a camera only above an uncovered child. O(n) time, O(h) stack."""
    count = [0]                         # a one-item list so dfs can update it in place
    if dfs(root, count) == NEEDS:
        count[0] += 1                   # the root has no parent to defer to
    return count[0]


# --- try the brute force ---
print(brute_force(build_tree([0, 0, None, 0, 0])))                    # -> 1
print(brute_force(build_tree([0, 0, None, 0, None, 0, None, None, 0])))   # -> 2
print(brute_force(build_tree([0, 0, 0, 0, 0, 0, 0])))                 # -> 2
print(brute_force(build_tree([0, 0, 0, 0, None, None, 0, 0, None, None, 0])))   # -> 3


# --- try the optimal ---
print(min_camera_cover(build_tree([0, 0, None, 0, 0])))               # -> 1
print(min_camera_cover(build_tree([0, 0, None, 0, None, 0, None, None, 0])))   # -> 2
print(min_camera_cover(build_tree([0, 0, 0, 0, 0, 0, 0])))            # -> 2
print(min_camera_cover(build_tree([0, 0, 0, 0, None, None, 0, 0, None, None, 0])))   # -> 3
