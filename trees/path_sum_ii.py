"""
Path Sum II (LeetCode 113)  — Medium
Pattern: DFS backtracking with a shared path list

Problem
-------
Given a binary tree and targetSum, return every root-to-leaf path (as a list of node
values) whose values sum to targetSum.
Example: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22 ->
[[5,4,11,2],[5,8,4,5]].

Brute force
-----------
Build a fresh copy of the path at every node (path + [val]), collect every root-to-leaf
path, then sum each one and keep the matches. O(n * h) time and O(n * h) space even when
nothing matches. The waste: every internal node copies the whole prefix, and every leaf
re-sums a prefix that its ancestors already added up.

From brute force to optimal
---------------------------
Two redundancies. (1) Re-summing: carry the remaining target down the recursion so each
node does an O(1) subtraction and a leaf only checks remaining == 0. (2) Re-copying: all
paths share prefixes, so keep ONE mutable list — append the node on entry, pop it on exit
(backtracking) — and copy it only when a leaf actually matches. Copies are then paid only
for output, which is unavoidable. This is the original solution's shape (preorder, shared
path, pop on return).

Intuition
---------
The path list mirrors the recursion stack exactly: it always holds the values from the root
to the node currently being visited. Snapshot it at a matching leaf, and undo each append
on the way back so siblings see the right prefix.

Geometric view
--------------
Picture a cursor walking the tree's outline. Going down an edge pushes that node onto the
path; coming back up pops it. Whenever the cursor stands on a leaf with zero remaining
target, a photo of the current path goes into the answer.

Steps
-----
1. ans = [], path = [].
2. dfs(node, remaining): if node is None return; path.append(node.val); remaining -= val.
3. If node is a leaf and remaining == 0: ans.append(path[:]).
4. Else recurse into left and right with remaining.
5. path.pop() (backtrack). Return ans after dfs(root, targetSum).

Complexity: O(n * h) time worst case (copying up to n/2 matched paths of length h),
O(h) extra space besides the output — one shared path plus the recursion stack.
Pitfalls: Appending `path` itself instead of a copy (all answers end up as the same list);
forgetting to pop on every return path; checking the sum at internal nodes.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        ans: List[List[int]] = []
        path: List[int] = []

        def dfs(node: Optional[TreeNode], remaining: int) -> None:
            if node is None:
                return
            path.append(node.val)
            remaining -= node.val
            if node.left is None and node.right is None:
                if remaining == 0:
                    ans.append(path[:])          # snapshot; path keeps mutating
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)
            path.pop()                           # backtrack so siblings see the right prefix

        dfs(root, targetSum)
        return ans


def brute_force(root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
    paths: List[List[int]] = []

    def collect(node: Optional[TreeNode], path: List[int]) -> None:
        if node is None:
            return
        path = path + [node.val]                 # fresh copy at every node
        if node.left is None and node.right is None:
            paths.append(path)
        collect(node.left, path)
        collect(node.right, path)

    collect(root, [])
    return [p for p in paths if sum(p) == targetSum]


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
    big = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
    cases = [(big, 22, [[5, 4, 11, 2], [5, 8, 4, 5]]), ([1, 2, 3], 5, []), ([1, 2], 0, []),
             ([], 0, []), ([1, -2, -3, 1, 3, -2, None, -1], -1, [[1, -2, 1, -1]])]
    for vals, t, want in cases:
        assert s.pathSum(build(vals), t) == want, (vals, t)
        assert brute_force(build(vals), t) == want, (vals, t)
    print("ok")
