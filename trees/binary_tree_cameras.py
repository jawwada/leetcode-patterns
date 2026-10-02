"""
Binary Tree Cameras (LeetCode 968)  — Hard
Pattern: Greedy post-order with 3-state return

Problem
-------
A camera placed on a node monitors that node, its parent and its
children. Return the minimum number of cameras needed to monitor every
node of the tree.
Example: [0,0,null,0,0] -> 1 (one camera on the middle node covers all).
Example: [0,0,null,0,null,0,null,null,0] -> 2.

Brute force
-----------
Try every subset of nodes as camera positions, check whether the subset
covers every node, and keep the smallest covering subset. O(2^n * n) time
(exponential), O(n) space. The wasted work: almost every subset is
hopeless, and the same local question ("is this subtree covered, does
it still need its parent?") is re-answered for every global subset that
shares the subtree's camera placement.

From brute force to optimal
---------------------------
The decision for a node only depends on what its children report, not on
the rest of the tree. So summarise each subtree by one of three states:
NEEDS (uncovered, parent must place a camera), COVERED (covered, no
camera here), HAS_CAMERA. Then the greedy rule: never put a camera on a
leaf, because its parent covers strictly more. Generalised: place a
camera only when a child says NEEDS. Pushing cameras up from the leaves
this way is optimal because a camera one level higher covers everything
the lower one would plus more. The null child reports COVERED so leaves
report NEEDS, which forces their parents to take the camera. Finally,
if the root itself reports NEEDS, add one camera for it.

Intuition
---------
Work bottom-up and be lazy: never take a camera until a child forces you
to. A child that is NEEDS forces a camera here; a child that HAS_CAMERA
makes you COVERED for free; if both children are merely COVERED, you are
NEEDS and defer to your own parent. Each camera is placed at the highest
node that can still cover the uncovered child, so none is wasted.

Geometric view
--------------
Picture light spreading upward from the leaves. A leaf is dark and shouts
"cover me" to its parent; the parent lights a camera, which also lights
its own parent and other children. The grandparent sees light coming
from below and stays dark but calm (COVERED) — it only needs a camera if
something above it is dark. Cameras end up on every other level of each
chain, which is the densest you can do with radius-1 lamps.

Steps
-----
1. States: 0 = NEEDS, 1 = COVERED, 2 = HAS_CAMERA. None returns COVERED.
2. dfs(node): l = dfs(left), r = dfs(right).
3. If l == 0 or r == 0: cameras += 1, return 2.
4. Else if l == 2 or r == 2: return 1.
5. Else return 0.
6. If dfs(root) == 0, cameras += 1. Return cameras.

Complexity: O(n) time, O(h) space — one post-order visit per node, the
recursion stack is the tree height.
Pitfalls: letting None report NEEDS (puts a camera on every leaf);
forgetting the final root check; treating COVERED and HAS_CAMERA as the
same state (a COVERED child does not cover its parent).
"""
from collections import deque
from itertools import combinations
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        NEEDS, COVERED, HAS_CAMERA = 0, 1, 2
        self.cameras = 0

        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return COVERED                     # null never asks for coverage -> leaves report NEEDS
            left, right = dfs(node.left), dfs(node.right)
            if left == NEEDS or right == NEEDS:
                self.cameras += 1                  # forced: a child is still dark
                return HAS_CAMERA
            if left == HAS_CAMERA or right == HAS_CAMERA:
                return COVERED                     # lit from below, no camera of our own
            return NEEDS                           # both children covered, nobody lights us

        if dfs(root) == NEEDS:
            self.cameras += 1                      # the root has no parent to defer to
        return self.cameras


def brute_force(root: Optional[TreeNode]) -> int:
    # Try every subset of nodes as camera positions, smallest first: O(2^n * n), exponential.
    nodes: List[TreeNode] = []
    parent = {}

    def collect(node: Optional[TreeNode], par: Optional[TreeNode]) -> None:
        if node:
            nodes.append(node)
            parent[node] = par
            collect(node.left, node)
            collect(node.right, node)

    collect(root, None)
    for k in range(len(nodes) + 1):
        for cams in combinations(nodes, k):
            cam_set = set(cams)
            if all(n in cam_set or parent[n] in cam_set
                   or n.left in cam_set or n.right in cam_set for n in nodes):
                return k
    return 0


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
    cases = [([0, 0, None, 0, 0], 1),
             ([0, 0, None, 0, None, 0, None, None, 0], 2),
             ([0], 1),                                              # single node needs its own camera
             ([0, 0], 1),
             ([0, 0, 0], 1),
             ([0, 0, 0, 0, 0, 0, 0], 2),                            # perfect tree of 7: both level-1 nodes
             ([0, 0, None, 0, None, 0, None, 0], 2),                # chain of 5
             ([0, 0, 0, 0, None, None, 0, 0, None, None, 0], 3)]
    for vals, want in cases:
        assert s.minCameraCover(build(vals)) == want, (vals, s.minCameraCover(build(vals)))
        assert brute_force(build(vals)) == want, vals
    print("ok")
