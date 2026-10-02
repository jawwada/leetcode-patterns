"""
Balanced Binary Tree (LeetCode 110)  — Easy
Pattern: Post-order height with side-channel answer

Problem
-------
A tree is height-balanced if, at EVERY node, the heights of the left and
right subtrees differ by at most 1. Return True if the tree is balanced.
Example: [3,9,20,null,null,15,7] -> True; [1,2,2,3,3,null,null,4,4] -> False.

Brute force
-----------
At each node compute height(left) and height(right) with a standalone
height() function, check |difference| <= 1, then recurse into both
children. O(n^2) worst case (skewed tree: height() costs O(n) at each of
O(n) nodes), O(h) space. The repeated work is height(): a subtree's height
is recomputed once for each of its ancestors.

From brute force to optimal
---------------------------
height() already visits the children before the parent, so the two numbers
the balance check needs are produced inside the recursion anyway. Fold the
check into height() and make the function return a sentinel (-1) the
moment any subtree is found to be unbalanced; every ancestor just passes
the -1 upward without further work. Each node is now visited once. The
invariant: height(node) returns the true height if node's subtree is
balanced, otherwise -1.

Intuition
---------
Balance is a local property (difference of two child heights) that must
hold everywhere. A post-order traversal naturally computes child heights
before looking at the parent, so each node can both check itself and
report its height upward in one step. A single bad node poisons the whole
answer, so short-circuit with -1 instead of carrying a separate flag.

Geometric view
--------------
Picture the tree as a mobile hanging from the root: each node balances two
arms. Measure arms from the bottom up; the first node whose arms differ by
2 or more "breaks" the mobile and the break propagates straight to the top.

Steps
-----
1. Define height(node): None -> 0.
2. left = height(node.left); if left == -1 return -1 (early exit).
3. right = height(node.right); if right == -1 or |left - right| > 1 return -1.
4. Return 1 + max(left, right).
5. Answer is height(root) != -1.

Complexity: O(n) time, O(h) space — one post-order visit per node.
Pitfalls: checking only the root (balance must hold at every node);
forgetting to propagate the -1 sentinel; an empty tree is balanced.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node: Optional[TreeNode]) -> int:
            # height of a balanced subtree, or -1 as soon as any subtree is unbalanced
            if node is None:
                return 0
            left = height(node.left)
            if left < 0:
                return -1
            right = height(node.right)
            if right < 0 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return height(root) >= 0


def brute_force(root: Optional[TreeNode]) -> bool:
    # Standalone height() recomputed at every node: O(n^2) worst case.
    def height(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if root is None:
        return True
    if abs(height(root.left) - height(root.right)) > 1:
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
    cases = [([3, 9, 20, None, None, 15, 7], True),
             ([1, 2, 2, 3, 3, None, None, 4, 4], False),
             ([], True), ([1], True), ([1, 2, None, 3], False),
             ([1, 2, 2, 3, None, None, 3, 4, None, None, 4], False)]   # root balanced, deeper node not
    for vals, want in cases:
        assert s.isBalanced(build(vals)) is want, vals
        assert brute_force(build(vals)) is want, vals
    print("ok")
