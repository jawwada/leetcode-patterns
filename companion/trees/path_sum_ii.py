"""
Path Sum II (LeetCode 113) - Medium
Chapter: trees
Pattern: DFS backtracking with a shared path list

Given a binary tree and target_sum, return every root-to-leaf path (as a list of node
values) whose values add up to target_sum.
Example: root = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], target_sum = 22
-> [[5, 4, 11, 2], [5, 8, 4, 5]]
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
def collect_paths(node, path, paths):
    """Record every root-to-leaf path as its own list of values."""
    if node is None:
        return
    path = path + [node.val]           # a fresh copy of the prefix at every node
    if node.left is None and node.right is None:
        paths.append(path)
    collect_paths(node.left, path, paths)
    collect_paths(node.right, path, paths)


def brute_force(root, target_sum):
    """Collect every root-to-leaf path, then keep those that sum to the target. O(n*h)."""
    paths = []
    collect_paths(root, [], paths)
    matching = []
    for path in paths:
        if sum(path) == target_sum:    # every path is summed from scratch
            matching.append(path)
    return matching


# --- optimal ---
def dfs(node, remaining, path, answers):
    """Walk down with one shared path; remaining is what is still needed to hit the target."""
    if node is None:
        return
    path.append(node.val)
    remaining = remaining - node.val
    if node.left is None and node.right is None:
        if remaining == 0:
            answers.append(path[:])          # copy: path keeps changing after this
    else:
        dfs(node.left, remaining, path, answers)
        dfs(node.right, remaining, path, answers)
    path.pop()                               # backtrack so siblings see the right prefix


def path_sum(root, target_sum):
    """One shared path with backtracking; copy only on a match. O(n) time plus the output."""
    answers = []
    dfs(root, target_sum, [], answers)
    return answers


# --- try the brute force ---
big = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
print(brute_force(build_tree(big), 22))                 # -> [[5, 4, 11, 2], [5, 8, 4, 5]]
print(brute_force(build_tree([1, 2, 3]), 5))            # -> []
print(brute_force(build_tree([]), 0))                   # -> []
small = [1, -2, -3, 1, 3, -2, None, -1]
print(brute_force(build_tree(small), -1))               # -> [[1, -2, 1, -1]]


# --- try the optimal ---
big = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
print(path_sum(build_tree(big), 22))                 # -> [[5, 4, 11, 2], [5, 8, 4, 5]]
print(path_sum(build_tree([1, 2, 3]), 5))            # -> []
print(path_sum(build_tree([]), 0))                   # -> []
small = [1, -2, -3, 1, 3, -2, None, -1]
print(path_sum(build_tree(small), -1))               # -> [[1, -2, 1, -1]]
