"""
Validate Binary Search Tree (LeetCode 98)  — Medium
Pattern: DFS with (low, high) bounds

Problem
-------
Return True if the tree is a valid BST: every node's value is strictly
greater than ALL values in its left subtree and strictly less than ALL
values in its right subtree.
Example: [2,1,3] -> True; [5,1,4,null,null,3,6] -> False (3 under 4 is < 5).

Brute force
-----------
At each node, collect every value in its left subtree and check they are
all < node.val, collect every value in its right subtree and check they
are all > node.val, then recurse into both children. O(n^2) time (each
node is scanned once per ancestor), O(n) space for the collected lists.
The repeated work is the scanning: a node deep in the tree is re-examined
by every one of its ancestors.

From brute force to optimal
---------------------------
An ancestor does not need to look at every descendant; it only needs to
hand down a constraint. A node is valid with respect to all its ancestors
iff low < node.val < high, where low is the nearest ancestor from which
we turned right and high the nearest from which we turned left. Those two
bounds are updated in O(1) when descending: going left tightens high to
node.val, going right tightens low to node.val. One traversal with the
bound pair replaces all the rescans. The invariant: every value in the
subtree rooted at node must lie strictly inside (low, high).

Intuition
---------
Checking only parent-child pairs is insufficient (the classic [5,4,6,
null,null,3,7] trap: 3 < 4 locally but 3 < 5 is violated). The fix is to
carry an open interval that accumulates every ancestor's constraint;
each node checks itself against the interval and narrows it for its
children. (Equivalent alternative: in-order traversal must be strictly
increasing.)

Geometric view
--------------
Picture each node receiving a window on the number line. The root's
window is (-inf, +inf). Stepping to a left child slides the right wall in
to the parent's value; stepping right slides the left wall. A node is
valid when it sits strictly inside its window; the windows only ever
shrink on the way down.

Steps
-----
1. valid(node, low, high): None -> True.
2. If not (low < node.val < high) return False.
3. Return valid(left, low, node.val) and valid(right, node.val, high).
4. Start with valid(root, -inf, +inf).

Complexity: O(n) time, O(h) space — each node checked once; stack depth h.
Pitfalls: only comparing with the direct parent; using <= (duplicates are
invalid); using sys.maxsize bounds that can collide with actual values
(use +/- infinity or None).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(node: Optional[TreeNode], low: float, high: float) -> bool:
            # every value in node's subtree must lie strictly inside (low, high)
            if node is None:
                return True
            if not (low < node.val < high):
                return False
            return valid(node.left, low, node.val) and valid(node.right, node.val, high)

        return valid(root, float("-inf"), float("inf"))


def brute_force(root: Optional[TreeNode]) -> bool:
    # At each node rescan its entire left and right subtrees: O(n^2).
    def all_values(node: Optional[TreeNode]) -> List[int]:
        if node is None:
            return []
        return [node.val] + all_values(node.left) + all_values(node.right)

    if root is None:
        return True
    if any(v >= root.val for v in all_values(root.left)):
        return False
    if any(v <= root.val for v in all_values(root.right)):
        return False
    return brute_force(root.left) and brute_force(root.right)


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
    cases = [([2, 1, 3], True),
             ([5, 1, 4, None, None, 3, 6], False),
             ([5, 4, 6, None, None, 3, 7], False),   # grandparent violation: 3 < 5 under the right subtree
             ([2, 2, 2], False),                     # duplicates are not allowed
             ([], True), ([1], True),
             ([3, 1, 5, 0, 2, 4, 6], True)]
    for vals, want in cases:
        assert s.isValidBST(build(vals)) is want, vals
        assert brute_force(build(vals)) is want, vals
    print("ok")
