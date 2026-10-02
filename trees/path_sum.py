"""
Path Sum (LeetCode 112)  — Easy
Pattern: DFS carrying path state

Problem
-------
Given a binary tree and targetSum, return True if some root-to-leaf path has node values
summing to targetSum. A leaf has no children; an empty tree has no paths.
Example: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22 -> True
(5 -> 4 -> 11 -> 2).

Brute force
-----------
Enumerate every root-to-leaf path as an explicit list of values, then sum each list and
compare. O(n * h) time (each of up to n/2 leaves copies and re-sums a path of length h),
O(n * h) space for the stored paths. The waste: the prefix shared by sibling paths is
copied and re-added for every leaf below it.

From brute force to optimal
---------------------------
The only thing a leaf needs from its path is the total, and the total of a child's path is
the parent's total plus the child's value. Observation: pass that running number down the
recursion instead of the whole list — each node does O(1) work and shares its prefix sum
with both subtrees. Checking only at leaves (both children None) enforces "root-to-leaf",
and an `or` short-circuits as soon as one path matches. This is the original solution's
preorder idea, with the early exit added.

Intuition
---------
Instead of carrying the running sum, carry the remaining amount: subtract each node's value
on the way down. At a leaf the question becomes "is the remainder exactly zero?".

Geometric view
--------------
Picture water poured in at the root with targetSum units; every node on the way drinks its
value. A leaf where the water level is exactly 0 is a hit. The DFS explores branches left
first and stops the moment one leaf reports a hit.

Steps
-----
1. If root is None: return False.
2. remaining = targetSum - root.val.
3. If root is a leaf: return remaining == 0.
4. Return hasPathSum(left, remaining) or hasPathSum(right, remaining).

Complexity: O(n) time, O(h) space — each node visited at most once; recursion depth = height.
Pitfalls: Accepting a match at an internal node (must be a leaf); returning True for an
empty tree with targetSum 0; pruning when the running sum exceeds target (values can be
negative).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        remaining = targetSum - root.val
        if root.left is None and root.right is None:    # only leaves end a path
            return remaining == 0
        return (self.hasPathSum(root.left, remaining)
                or self.hasPathSum(root.right, remaining))


def brute_force(root: Optional[TreeNode], targetSum: int) -> bool:
    paths: List[List[int]] = []

    def collect(node: Optional[TreeNode], path: List[int]) -> None:
        if node is None:
            return
        path = path + [node.val]                         # copies the shared prefix each time
        if node.left is None and node.right is None:
            paths.append(path)
        collect(node.left, path)
        collect(node.right, path)

    collect(root, [])
    return any(sum(p) == targetSum for p in paths)


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
    big = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]
    cases = [(big, 22, True), ([1, 2, 3], 5, False), ([], 0, False), ([1, 2], 1, False),
             ([-2, None, -3], -5, True), (big, 26, True), (big, 18, True), (big, 23, False)]
    for vals, t, want in cases:
        assert s.hasPathSum(build(vals), t) is want, (vals, t)
        assert brute_force(build(vals), t) is want, (vals, t)
    print("ok")
