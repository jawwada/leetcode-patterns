"""
Count Good Nodes in Binary Tree (LeetCode 1448)  — Medium
Pattern: DFS carrying path state (running max)

Problem
-------
A node is "good" if no node on the path from the root to it has a value
greater than it (the root is always good). Count the good nodes.
Example: [3,1,4,3,null,1,5] -> 4 (3, 4, 5 and the deeper 3).

Brute force
-----------
DFS while carrying the full root->node path as a list; at every node call
max(path) over the whole list to decide if the node is good.
O(n * h) time and O(h^2) space (path copies). The repeated work is the
max() scan: the maximum of the path's prefix was already computed at the
parent, yet it is recomputed from scratch at every child.

From brute force to optimal
---------------------------
The decision at a node needs only ONE number about the path: its maximum.
That number is incremental: max(path + [v]) = max(max(path), v). So pass
the running maximum down the recursion instead of the path itself; each
child receives max(parent_max, parent.val) and compares its value against
it in O(1). Every node is visited once with constant work. The invariant:
path_max passed into dfs(node) is the largest value strictly above node.

Intuition
---------
"Good" means "a new record high along my root path". Track the record
high as you descend; a node is good when it ties or beats it, and then
it becomes the new record for everything below it.

Geometric view
--------------
Walk down each root-to-leaf path like a hiker tracking the highest
altitude reached so far. Every node whose altitude is at least the
current record is a new summit (good); the record only ever rises, so a
single integer riding along with the recursion suffices.

Steps
-----
1. dfs(node, path_max): if None return 0.
2. good = 1 if node.val >= path_max else 0.
3. path_max = max(path_max, node.val).
4. Return good + dfs(left, path_max) + dfs(right, path_max).
5. Start with dfs(root, root.val) (or -inf).

Complexity: O(n) time, O(h) space — one visit per node; stack depth h.
Pitfalls: using > instead of >= (equal values are good); updating the max
before comparing the node; sharing a mutable max across siblings.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node: Optional[TreeNode], path_max: int) -> int:
            if node is None:
                return 0
            good = 1 if node.val >= path_max else 0   # ties count as good
            path_max = max(path_max, node.val)
            return good + dfs(node.left, path_max) + dfs(node.right, path_max)

        return dfs(root, root.val)


def brute_force(root: TreeNode) -> int:
    # Carry the whole root->node path and rescan it with max() at every node: O(n * h).
    def dfs(node: Optional[TreeNode], path: List[int]) -> int:
        if node is None:
            return 0
        path = path + [node.val]
        good = 1 if node.val >= max(path) else 0
        return good + dfs(node.left, path) + dfs(node.right, path)

    return dfs(root, [])


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
    cases = [([3, 1, 4, 3, None, 1, 5], 4),
             ([3, 3, None, 4, 2], 3),
             ([1], 1),
             ([9, None, 3, 6], 1),            # 9 blocks everything below it
             ([2, None, 2, None, 2], 3)]      # ties along the path all count
    for vals, want in cases:
        assert s.goodNodes(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
