"""
Cousins in Binary Tree (LeetCode 993)  — Easy
Pattern: DFS carrying path state

Problem
-------
In a binary tree with unique values, two nodes are cousins if they are at the same depth
but have different parents. Given values x and y, return whether their nodes are cousins.
Example: root = [1,2,3,null,4,null,5], x = 5, y = 4 -> True; root = [1,2,3,4], x = 4,
y = 3 -> False (depths 2 and 1).

Brute force
-----------
Answer four separate questions with four separate searches from the root: depth(x),
depth(y), parent(x), parent(y). Each search is O(n), so O(4n) time and O(h) space. The
waste: the same nodes are walked four times, and each walk rediscovers the depth and
parent of every node it passes even though one walk sees both facts for every node.

From brute force to optimal
---------------------------
Depth and parent are both "path state" that a DFS already knows when it arrives at a node:
the depth is one more than the caller's and the parent is the caller. Observation: carry
(parent, depth) as arguments and, when the node's value is x or y, record that pair. One
traversal fills in both records; then compare depth equal and parent different. This is
the original solution's single preorder walk, with the records kept in a small dict.

Intuition
---------
Cousin-ness only needs two facts per target node: how deep it is and who its parent is.
Both arrive for free as you walk down, so collect them for x and y in a single pass.

Geometric view
--------------
Picture the tree in horizontal layers. x and y must sit on the same horizontal line, but
hang from different branch points directly above them. One sweep down the tree tags each
of the two targets with its (layer, hook) pair.

Steps
-----
1. info = {}.
2. dfs(node, parent, depth): if node is None return; if node.val in (x, y):
   info[node.val] = (parent, depth); recurse into children with (node, depth + 1).
3. dfs(root, None, 0).
4. Return info[x] depth == info[y] depth and info[x] parent is not info[y] parent.

Complexity: O(n) time, O(h) space — one traversal; recursion depth = height.
Pitfalls: Treating siblings (same parent) as cousins; comparing parent values when you
could compare node identity; forgetting that the root has parent None.
"""
from collections import deque
from typing import Dict, List, Optional, Tuple


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        info: Dict[int, Tuple[Optional[TreeNode], int]] = {}   # val -> (parent, depth)

        def dfs(node: Optional[TreeNode], parent: Optional[TreeNode], depth: int) -> None:
            if node is None:
                return
            if node.val == x or node.val == y:
                info[node.val] = (parent, depth)
            dfs(node.left, node, depth + 1)
            dfs(node.right, node, depth + 1)

        dfs(root, None, 0)
        (px, dx), (py, dy) = info[x], info[y]
        return dx == dy and px is not py        # same layer, different hooks


def brute_force(root: Optional[TreeNode], x: int, y: int) -> bool:
    def depth(node, target, d=0):               # separate full search per question
        if node is None:
            return -1
        if node.val == target:
            return d
        return max(depth(node.left, target, d + 1), depth(node.right, target, d + 1))

    def parent(node, target):
        if node is None:
            return None
        for child in (node.left, node.right):
            if child and child.val == target:
                return node
        return parent(node.left, target) or parent(node.right, target)

    return depth(root, x) == depth(root, y) and parent(root, x) is not parent(root, y)


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
    cases = [([1, 2, 3, 4], 4, 3, False), ([1, 2, 3, None, 4, None, 5], 5, 4, True),
             ([1, 2, 3, None, 4], 2, 3, False), ([1, 2, 3, 4, 5, 6, 7], 4, 5, False),
             ([1, 2, 3, 4, 5, 6, 7], 5, 6, True)]
    for vals, x, y, want in cases:
        assert s.isCousins(build(vals), x, y) is want, (vals, x, y)
        assert brute_force(build(vals), x, y) is want, (vals, x, y)
    print("ok")
