"""
Symmetric Tree (LeetCode 101)  — Easy
Pattern: Simultaneous tree recursion

Problem
-------
Return True if a binary tree is a mirror image of itself around its centre line.
Example: [1,2,2,3,4,4,3] -> True; [1,2,2,null,3,null,3] -> False.

Brute force
-----------
Do a level-order walk that lists every child slot of each level (None for a missing
child) and check that each level's list reads the same forwards and backwards.
O(n) time, O(w) space for the widest level. The waste: whole levels are materialised and
copied (values, None placeholders, a reversed copy) before any comparison happens, so a
mismatch deep in one corner is only noticed after every level above it is fully built.

From brute force to optimal
---------------------------
A level palindrome is just pairing slot k from the left with slot k from the right.
Observation: those pairs are generated recursively — mirror(a, b) holds iff a.val == b.val,
mirror(a.left, b.right) and mirror(a.right, b.left). Walking the two halves in lockstep
compares each mirror pair directly, needs no padding lists, and `and` short-circuits at the
first mismatch. Space drops to O(h). This is the original solution.

Intuition
---------
Symmetry is not a property of one subtree, it is a relation between two: the left subtree
must be the mirror of the right. So recurse on PAIRS of nodes, crossing over (outer with
outer, inner with inner) at every step.

Geometric view
--------------
Fold the tree along the vertical line through the root. Two fingers start on the root's
children and move in mirror image: one goes left while the other goes right. Every pair of
nodes the fingers touch together must land on top of each other with equal values.

Steps
-----
1. mirror(a, b): if a is None or b is None: return a is b.
2. Return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left).
3. Answer = mirror(root.left, root.right) (True for an empty tree).

Complexity: O(n) time, O(h) space — each mirror pair is compared once; recursion depth = height.
Pitfalls: Comparing left.left with right.left (that tests sameness, not mirroring); checking
only values level by level without None placeholders ([1,2,2,null,3,null,3] passes wrongly).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def mirror(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if a is None or b is None:
                return a is b                     # both missing -> mirror; one missing -> not
            return (a.val == b.val
                    and mirror(a.left, b.right)   # outer pair
                    and mirror(a.right, b.left))  # inner pair

        return root is None or mirror(root.left, root.right)


def brute_force(root: Optional[TreeNode]) -> bool:
    level = [root]
    while level:
        vals = [n.val if n else None for n in level]
        if vals != vals[::-1]:                    # each level (with None slots) must be a palindrome
            return False
        level = [c for n in level if n for c in (n.left, n.right)]
    return True


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
    cases = [([1, 2, 2, 3, 4, 4, 3], True), ([1, 2, 2, None, 3, None, 3], False), ([], True),
             ([1], True), ([1, 2, 2, 2, None, 2], False), ([1, 2, 3], False)]
    for vals, want in cases:
        assert s.isSymmetric(build(vals)) is want, vals
        assert brute_force(build(vals)) is want, vals
    print("ok")
