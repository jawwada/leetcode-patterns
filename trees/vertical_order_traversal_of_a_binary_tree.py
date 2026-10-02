"""
Vertical Order Traversal of a Binary Tree (LeetCode 987)  — Hard
Pattern: DFS with (column, row) coordinates, then group-sort

Problem
-------
Give the root the coordinate (row=0, col=0); a left child is at
(row+1, col-1), a right child at (row+1, col+1). Report the nodes column
by column from leftmost to rightmost; inside a column order by row, and
nodes sharing the same (row, col) are ordered by value.
Example: [3,9,20,null,null,15,7] -> [[9],[3,15],[20],[7]].
Example: [1,2,3,4,5,6,7] -> [[4],[2],[1,5,6],[3],[7]] (5 and 6 share
(2,0) and are sorted by value).

Brute force
-----------
First find the column range by a DFS that tracks min and max col. Then,
for every column c in that range, do a full DFS collecting the nodes
whose col == c as (row, val) pairs, sort them and emit. O(n * W + n log n)
time where W is the number of columns (up to n), O(n) space. The wasted
work is the repeated full traversal: every pass walks all n nodes to pick
out the few that belong to one column.

From brute force to optimal
---------------------------
Each node's column is known the moment we visit it, so one traversal can
drop every node into its bucket directly: a dict col -> list of
(row, val). That removes the W repeated walks. The remaining cost is
ordering: columns must come out left to right, and inside a column by
(row, val). Sorting each bucket on the (row, val) tuple handles both tie
rules at once, and sorting the dict keys orders the columns. Total
O(n log n) from the sorts; a BFS instead of DFS would give rows for free
but ties by value still need a sort, so the tuple sort is the simplest
correct form.

Intuition
---------
The problem is really "sort nodes by the key (col, row, val)" and then
group by col. Once every node carries its coordinate, the tree shape no
longer matters; a flat list of keyed records and one sort finishes it.

Geometric view
--------------
Draw the tree on graph paper: the root at the origin, each level one unit
lower, left children one unit left and right children one unit right.
Vertical lines x = c slice the tree into columns; reading each line from
top to bottom gives a column's contents, and two nodes landing on the
same grid point (like 5 and 6 under 2 and 3) are read smaller first.

Steps
-----
1. DFS(node, row, col): append (row, node.val) to cols[col].
2. Recurse left with (row+1, col-1) and right with (row+1, col+1).
3. For each col in sorted(cols): sort its list of (row, val) tuples.
4. Emit the values of each column in that order.

Complexity: O(n log n) time, O(n) space — one traversal plus sorting
every (row, val) record once overall.
Pitfalls: using a plain row-major BFS without sorting by value for
equal (row, col); sorting by value only (rows must dominate); using a
list indexed by col without offsetting negative columns.
"""
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        cols: Dict[int, List[Tuple[int, int]]] = defaultdict(list)   # col -> [(row, val)]

        def dfs(node: Optional[TreeNode], row: int, col: int) -> None:
            if node is None:
                return
            cols[col].append((row, node.val))
            dfs(node.left, row + 1, col - 1)
            dfs(node.right, row + 1, col + 1)

        dfs(root, 0, 0)
        # tuple sort = by row, then by value for nodes sharing the same (row, col)
        return [[val for _, val in sorted(cols[c])] for c in sorted(cols)]


def brute_force(root: Optional[TreeNode]) -> List[List[int]]:
    # One full traversal per column: find the column range, then re-walk the tree for each column.
    def span(node: Optional[TreeNode], col: int) -> Tuple[int, int]:
        if node is None:
            return (0, 0)
        l_lo, l_hi = span(node.left, col - 1)
        r_lo, r_hi = span(node.right, col + 1)
        return (min(col, l_lo, r_lo), max(col, l_hi, r_hi))

    def collect(node: Optional[TreeNode], row: int, col: int, want: int, out: List[Tuple[int, int]]) -> None:
        if node is None:
            return
        if col == want:
            out.append((row, node.val))
        collect(node.left, row + 1, col - 1, want, out)
        collect(node.right, row + 1, col + 1, want, out)

    if root is None:
        return []
    lo, hi = span(root, 0)
    result = []
    for c in range(lo, hi + 1):
        bucket: List[Tuple[int, int]] = []
        collect(root, 0, 0, c, bucket)
        result.append([val for _, val in sorted(bucket)])
    return result


def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """LeetCode level-order list (None = missing child) -> tree."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = deque([root]), 1
    while queue and i < len(vals):
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


if __name__ == "__main__":
    s = Solution()
    cases = [([3, 9, 20, None, None, 15, 7], [[9], [3, 15], [20], [7]]),
             ([1, 2, 3, 4, 5, 6, 7], [[4], [2], [1, 5, 6], [3], [7]]),
             ([1, 2, 3, 4, 6, 5, 7], [[4], [2], [1, 5, 6], [3], [7]]),   # same cell: smaller value first
             ([1], [[1]]),
             ([1, None, 2, None, 3], [[1], [2], [3]]),                     # right-leaning chain
             ([3, 1, 4, 0, 2, 2], [[0], [1], [3, 2, 2], [4]])]             # equal values on one cell
    for vals, want in cases:
        assert s.verticalTraversal(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
