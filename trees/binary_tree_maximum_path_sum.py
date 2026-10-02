"""
Binary Tree Maximum Path Sum (LeetCode 124)  — Hard
Pattern: Post-order height with side-channel answer

Problem
-------
A path is any sequence of nodes connected by parent-child edges, visiting
each node at most once; it need not pass through the root or end at a
leaf. Return the maximum sum of node values over all non-empty paths.
Example: [-10,9,20,null,null,15,7] -> 42 (15 -> 20 -> 7).

Brute force
-----------
Every path has a unique highest node ("top"). For each node as top, the
best path is node.val + best downward gain on the left + best downward
gain on the right (each gain clipped at 0). Compute gain() with a
standalone recursive function at every node and take the max over all
tops. O(n^2) time (gain() costs O(subtree) and is called once per
ancestor), O(h) space. The repeated work is gain(): the gain of a subtree
is recomputed for every ancestor that considers itself the top.

From brute force to optimal
---------------------------
gain(node) is itself a post-order recursion that computes gain(left) and
gain(right) on the way, and those are exactly the two numbers the
"node as top" formula needs. So evaluate the top-candidate INSIDE gain(),
update a global best, and return only the single-arm value
node.val + max(left, right, 0) to the parent. One pass, each node visited
once. The split matters: a path bending at node uses both arms, but a
path continuing up through the parent can use only one arm, so the
returned value and the recorded candidate are different quantities.

Intuition
---------
Two quantities per node: (1) the best path that BENDS at this node
(val + left gain + right gain) is a candidate answer; (2) the best path
that can be EXTENDED upward (val + the better single arm) is what we
return. Negative gains are clipped to 0: a bad subtree is simply left out
of the path. Initialise best to -infinity because a tree of all-negative
values must still return the largest single node.

Geometric view
--------------
Each node is a hinge with two arms hanging below. Measuring from the
leaves up, every arm reports the heaviest downward chain it can offer
(or 0 if all its chains are negative). Opening a hinge flat gives a
candidate path; folding it to one side gives what the hinge passes up.

Steps
-----
1. best = -inf. gain(node): None -> 0.
2. left = max(gain(node.left), 0); right = max(gain(node.right), 0).
3. best = max(best, node.val + left + right)  (path bending here).
4. Return node.val + max(left, right).
5. Call gain(root); return best.

Complexity: O(n) time, O(h) space — one post-order visit per node.
Pitfalls: returning left + right upward (a path cannot fork); initialising
best to 0 (fails for all-negative trees); forgetting to clip negative
gains to 0.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.best = float("-inf")             # not 0: an all-negative tree still has an answer

        def gain(node: Optional[TreeNode]) -> int:
            # best sum of a path that starts at `node` and goes DOWN one side (never negative)
            if node is None:
                return 0
            left = max(gain(node.left), 0)    # a negative arm is simply not used
            right = max(gain(node.right), 0)
            self.best = max(self.best, node.val + left + right)   # path bending at node
            return node.val + max(left, right)                     # only one arm continues up

        gain(root)
        return self.best


def brute_force(root: Optional[TreeNode]) -> int:
    # Every node as the path's top; recompute both downward gains from scratch: O(n^2).
    def gain(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return node.val + max(gain(node.left), gain(node.right), 0)

    if root is None:
        return float("-inf")
    here = root.val + max(gain(root.left), 0) + max(gain(root.right), 0)
    return max(here, brute_force(root.left), brute_force(root.right))


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
    cases = [([1, 2, 3], 6),
             ([-10, 9, 20, None, None, 15, 7], 42),
             ([-3], -3),                     # all negative: best is the single largest node
             ([2, -1], 2),
             ([-2, -1, -3], -1),
             ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 48)]   # 7-11-4-5-8-13
    for vals, want in cases:
        assert s.maxPathSum(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
