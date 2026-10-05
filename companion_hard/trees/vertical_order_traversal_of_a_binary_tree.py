"""
Vertical Order Traversal of a Binary Tree (LeetCode 987) - Hard
Chapter: trees
Pattern: DFS with (column, row) coordinates, then group-sort

The root is at (row 0, col 0); a left child sits at (row+1, col-1) and a right child at
(row+1, col+1). Report the nodes column by column from left to right. Within a column,
order by row, and break ties at the same (row, col) by value.
Example: [1, 2, 3, 4, 5, 6, 7] -> [[4], [2], [1, 5, 6], [3], [7]], since 5 and 6 share (2, 0).
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


def values_in_order(pairs):
    """Sort (row, value) pairs and return just the values: rows first, then values on a tie."""
    pairs.sort()
    values = []
    for row, value in pairs:
        values.append(value)
    return values


# --- brute force ---
def span(node, col):
    """(leftmost column, rightmost column) used anywhere in node's subtree; node exists."""
    lo = col
    hi = col
    if node.left is not None:
        left_lo, left_hi = span(node.left, col - 1)
        lo = min(lo, left_lo)
        hi = max(hi, left_hi)
    if node.right is not None:
        right_lo, right_hi = span(node.right, col + 1)
        lo = min(lo, right_lo)
        hi = max(hi, right_hi)
    return lo, hi


def collect(node, row, col, want, out):
    """Walk the whole subtree and keep only the nodes sitting in column want."""
    if node is None:
        return
    if col == want:
        out.append((row, node.val))
    collect(node.left, row + 1, col - 1, want, out)
    collect(node.right, row + 1, col + 1, want, out)


def brute_force(root):
    """One full traversal per column, each picking out that column's nodes. O(n * W) time."""
    if root is None:
        return []
    lo, hi = span(root, 0)
    result = []
    for col in range(lo, hi + 1):
        bucket = []
        collect(root, 0, 0, col, bucket)      # walks all n nodes to find the few in this column
        result.append(values_in_order(bucket))
    return result


# --- optimal ---
def dfs(node, row, col, cols):
    """Drop every node straight into its column's bucket as (row, value)."""
    if node is None:
        return
    if col not in cols:
        cols[col] = []
    cols[col].append((row, node.val))
    dfs(node.left, row + 1, col - 1, cols)
    dfs(node.right, row + 1, col + 1, cols)


def vertical_traversal(root):
    """One traversal buckets nodes by column; sort buckets and keys. O(n log n) time."""
    cols = {}                       # column -> list of (row, value)
    dfs(root, 0, 0, cols)
    result = []
    for col in sorted(cols):        # columns left to right
        result.append(values_in_order(cols[col]))   # tuple sort: by row, then by value
    return result


# --- try the brute force ---
print(brute_force(build_tree([3, 9, 20, None, None, 15, 7])))   # -> [[9], [3, 15], [20], [7]]
print(brute_force(build_tree([1, 2, 3, 4, 5, 6, 7])))           # -> [[4], [2], [1, 5, 6], [3], [7]]
print(brute_force(build_tree([1, 2, 3, 4, 6, 5, 7])))           # -> [[4], [2], [1, 5, 6], [3], [7]]
print(brute_force(build_tree([3, 1, 4, 0, 2, 2])))              # -> [[0], [1], [3, 2, 2], [4]]


# --- try the optimal ---
print(vertical_traversal(build_tree([3, 9, 20, None, None, 15, 7])))  # -> [[9], [3, 15], [20], [7]]
print(vertical_traversal(build_tree([1, 2, 3, 4, 5, 6, 7])))    # -> [[4], [2], [1, 5, 6], [3], [7]]
print(vertical_traversal(build_tree([1, 2, 3, 4, 6, 5, 7])))    # -> [[4], [2], [1, 5, 6], [3], [7]]
print(vertical_traversal(build_tree([3, 1, 4, 0, 2, 2])))       # -> [[0], [1], [3, 2, 2], [4]]
