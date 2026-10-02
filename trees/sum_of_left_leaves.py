"""
Sum of Left Leaves (LeetCode 404)  — Easy
Pattern: DFS carrying path state

Problem
-------
Given the root of a binary tree, return the sum of all left leaves: nodes with no
children that are the LEFT child of their parent. The root alone is not a left leaf.
Example: [3,9,20,null,null,15,7] -> 24 (9 and 15 are left leaves; 7 is a right leaf).

Brute force
-----------
Collect every leaf first, then for each leaf search the tree from the root again to find
its parent and check whether the leaf hangs off parent.left. Finding a parent is an O(n)
walk, so the total is O(n * leaves) = O(n^2) time, O(n) space. The waste: the parent was
right there when the DFS reached the leaf, and we threw that information away.

From brute force to optimal
---------------------------
The redundancy is re-discovering each leaf's parent with a fresh search from the root.
Observation: "is this a left child?" is decided by the edge we walked to get here, and a
DFS always knows that edge at the moment it steps down. So pass one boolean down the
recursion (True when stepping into .left, False for .right and the root). When a node
has no children, add its value iff the flag is True. One pass, O(n) time, O(h) stack.
(This is exactly the user's original pre-order approach, kept intact.)

Intuition
---------
Leaf-ness is a property of the node; left-ness is a property of the edge into it. A
pre-order DFS sees both at once if you carry the edge direction as a parameter.

Geometric view
--------------
Picture the tree with every edge labelled L or R. Walk down from the root; whenever you
reach a dead end, look at the label of the last edge you crossed. Sum the dead ends whose
last edge says L.

Steps
-----
1. dfs(node, is_left): if node is None return 0.
2. If node has no children, return node.val if is_left else 0.
3. Otherwise return dfs(node.left, True) + dfs(node.right, False).
4. Answer is dfs(root, False).

Complexity: O(n) time, O(h) space — each node visited once; recursion depth = height.
Pitfalls: counting a single-node root as a left leaf; counting left children that are not
leaves; counting right leaves.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode], is_left: bool) -> int:
            if node is None:
                return 0
            if node.left is None and node.right is None:
                return node.val if is_left else 0
            return dfs(node.left, True) + dfs(node.right, False)

        return dfs(root, False)  # the root is never a left leaf


def brute_force(root: Optional[TreeNode]) -> int:
    # Gather all leaves, then re-search from the root to find each leaf's parent: O(n^2).
    nodes, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        nodes.append(node)
        stack.extend(c for c in (node.left, node.right) if c)
    total = 0
    for leaf in (n for n in nodes if n.left is None and n.right is None):
        parent = next((p for p in nodes if p.left is leaf or p.right is leaf), None)
        if parent is not None and parent.left is leaf:
            total += leaf.val
    return total


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
    cases = [([3, 9, 20, None, None, 15, 7], 24),
             ([1], 0),                         # root alone is not a left leaf
             ([1, 2, 3, 4, 5], 4),
             ([1, None, 2, 3], 3),             # left leaf under a right child
             ([], 0)]
    for vals, want in cases:
        assert s.sumOfLeftLeaves(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
