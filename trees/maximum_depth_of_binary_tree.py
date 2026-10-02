"""
Maximum Depth of Binary Tree (LeetCode 104)  — Easy
Pattern: Tree recursion (post-order)

Problem
-------
Return the number of nodes on the longest root-to-leaf path.
Example: [3,9,20,null,null,15,7] -> 3 (3 -> 20 -> 15).

Brute force
-----------
Enumerate every root-to-leaf path as an explicit list of values, then take
the longest. O(n*h) time and space because each of up to n/2 leaves copies
a path of length up to h. The wasted work is materialising the paths: we
only ever need their LENGTH, and all paths through a node share the same
prefix that gets copied again and again.

From brute force to optimal
---------------------------
The redundancy is the repeated prefix: every leaf under a node re-counts
the same ancestors. The observation is that the depth of a subtree depends
only on the depths of its two child subtrees: depth(node) =
1 + max(depth(left), depth(right)). That gives a post-order recursion in
which each node is visited exactly once and returns a single integer,
so no path storage at all. The invariant: the value returned for a node
is the height of its subtree.

Intuition
---------
A tree's height is one more than the taller of its two subtrees. Recursion
computes heights bottom-up: leaves report 1, a None child reports 0, and
each parent adds one to the larger report. The longest path is picked by
the max() at every level.

Geometric view
--------------
Picture water filling the tree from the leaves upward: each node is
labelled with the height of the tallest column beneath it. The root's
label is the answer. The recursion goes down one path at a time and the
labels bubble up as the calls return.

Steps
-----
1. If the node is None, return 0.
2. Compute the depth of the left and of the right subtree recursively.
3. Return 1 + the larger of the two.

Complexity: O(n) time, O(h) space — one visit per node, recursion depth h
(O(n) for a skewed tree).
Pitfalls: returning 1 for a None node (off by one); mixing up "depth in
nodes" (this problem) with "depth in edges".
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


def brute_force(root: Optional[TreeNode]) -> int:
    # Materialise every root-to-leaf path as a list, then take the longest: O(n*h).
    paths: List[List[int]] = []

    def walk(node: Optional[TreeNode], path: List[int]) -> None:
        if node is None:
            return
        path = path + [node.val]          # copies the shared prefix for every descendant
        if node.left is None and node.right is None:
            paths.append(path)
        walk(node.left, path)
        walk(node.right, path)

    walk(root, [])
    return max((len(p) for p in paths), default=0)


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
    cases = [([3, 9, 20, None, None, 15, 7], 3), ([1, None, 2], 2), ([], 0), ([1], 1),
             ([1, 2, None, 3, None, 4], 4)]
    for vals, want in cases:
        assert s.maxDepth(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
