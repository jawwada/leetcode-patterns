"""
Diameter of Binary Tree (LeetCode 543)  — Easy
Pattern: Post-order height with side-channel answer

Problem
-------
The diameter is the number of EDGES on the longest path between any two
nodes; the path need not pass through the root.
Example: [1,2,3,4,5] -> 3 (4 -> 2 -> 1 -> 3 or 5 -> 2 -> 1 -> 3).

Brute force
-----------
For every node, the longest path that bends at that node is
height(left) + height(right). Compute height() from scratch at each node
and take the maximum over all nodes. O(n^2) time in the worst case (a
skewed tree makes height() cost O(n) for O(n) nodes), O(h) space. The
repeated work is height(): the height of a subtree is recomputed once for
every one of its ancestors.

From brute force to optimal
---------------------------
height(node) is already a post-order recursion that computes height(left)
and height(right) on the way; those two numbers are exactly what the
diameter-through-node formula needs. So instead of calling height() again
from the outside, update a running best = max(best, left + right) INSIDE
height(), while the values are at hand. Each node's height is then
computed exactly once, and the answer falls out as a side effect of one
pass. The invariant: when height(node) returns, best already accounts for
every path whose highest point is inside node's subtree.

Intuition
---------
Every path has a unique highest node where it "bends". The longest path
bending at node is its left height plus its right height. Compute heights
bottom-up and at each node try "left + right" as a candidate answer. The
height returned upward is 1 + max(left, right) because a path continuing
up through the parent can use only one arm.

Geometric view
--------------
Think of each node as a hinge with two arms hanging down. The arm lengths
are the subtree heights. Opening the hinge flat gives a path of length
left + right; the recursion measures both arms once per hinge and
remembers the widest opening.

Steps
-----
1. Define height(node): return 0 for None.
2. Recursively get left = height(node.left), right = height(node.right).
3. Update best = max(best, left + right)  (path bending at node, in edges).
4. Return 1 + max(left, right) to the parent.
5. Call height(root); answer is best.

Complexity: O(n) time, O(h) space — one post-order visit per node.
Pitfalls: counting nodes instead of edges (off by one); returning
left + right upward instead of 1 + max(left, right); forgetting that the
answer may not pass through the root.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.best = 0

        def height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            left, right = height(node.left), height(node.right)
            self.best = max(self.best, left + right)   # longest path that bends at `node`
            return 1 + max(left, right)                 # only one arm continues upward

        height(root)
        return self.best


def brute_force(root: Optional[TreeNode]) -> int:
    # Recompute both subtree heights from scratch at every node: O(n^2) on skewed trees.
    def height(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if root is None:
        return 0
    through_root = height(root.left) + height(root.right)
    return max(through_root, brute_force(root.left), brute_force(root.right))


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
    cases = [([1, 2, 3, 4, 5], 3), ([1, 2], 1), ([], 0), ([1], 0),
             ([1, None, 2, None, 3], 2),
             ([1, 2, None, 3, 4, 5, None, None, None, 6], 4)]   # longest path avoids the root
    for vals, want in cases:
        assert s.diameterOfBinaryTree(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
