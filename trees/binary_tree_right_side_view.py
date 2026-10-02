"""
Binary Tree Right Side View (LeetCode 199)  — Medium
Pattern: DFS with depth (first-visit per level)

Problem
-------
Standing to the right of the tree, return the values you can see from top
to bottom: the rightmost node of every level.
Example: [1,2,3,null,5,null,4] -> [1,3,4]; [1,null,3] -> [1,3].

Brute force
-----------
Do a full level-order traversal that stores every node of every level
(a list of lists), then keep the last element of each list.
O(n) time, O(n) space. The wasted work is storing all n values when only
one per level (h values) is ever used; everything but the last entry of
each level is thrown away.

From brute force to optimal
---------------------------
We only need the FIRST node reached on each level if we visit right
children before left children. A DFS that carries its depth and goes
right-first reaches, for every depth d, the rightmost node of depth d
before any other node of that depth. So "depth == len(view)" means
"nobody has claimed this level yet": record the value. Space drops to the
recursion stack O(h) plus the h answers. The invariant: view[d] is the
rightmost node among all depth-d nodes visited so far, and right-first
order guarantees the first one visited is the rightmost overall.

Intuition
---------
Right-first preorder DFS reaches each level's rightmost node before any
other node of that level. The length of the answer list doubles as "the
next unseen depth", so no extra bookkeeping is required.

Geometric view
--------------
Shine a light from the right: each level's rightmost node casts the only
visible silhouette. The DFS hugs the right edge of the drawing first, then
back-fills deeper levels that the right spine does not reach (e.g. node 4
hanging under 2's right child when 3 has no children).

Steps
-----
1. view = []; dfs(root, 0).
2. dfs(node, depth): if None return; if depth == len(view) append node.val.
3. dfs(node.right, depth+1) then dfs(node.left, depth+1).
4. Return view.

Complexity: O(n) time, O(h) space — every node visited once; stack depth h.
Pitfalls: visiting left first (records the left view); returning the right
spine only (misses deeper nodes reachable only through a left child);
mutating the depth counter instead of passing it down.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        view: List[int] = []

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if node is None:
                return
            if depth == len(view):        # first node reached at this depth
                view.append(node.val)
            dfs(node.right, depth + 1)    # right first so it claims the level
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return view


def brute_force(root: Optional[TreeNode]) -> List[int]:
    # Full level-order listing of every node, then keep only the last value per level.
    if root is None:
        return []
    levels, frontier = [], [root]
    while frontier:
        levels.append([n.val for n in frontier])
        nxt = []
        for n in frontier:
            if n.left:
                nxt.append(n.left)
            if n.right:
                nxt.append(n.right)
        frontier = nxt
    return [level[-1] for level in levels]


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
    cases = [([1, 2, 3, None, 5, None, 4], [1, 3, 4]),
             ([1, None, 3], [1, 3]), ([], []),
             ([1, 2, 3, 4], [1, 3, 4]),                   # deepest level only under the left child
             ([1, 2, None, 3, None, 4], [1, 2, 3, 4])]
    for vals, want in cases:
        assert s.rightSideView(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
