"""
Lowest Common Ancestor of a Binary Tree (LeetCode 236)  — Medium
Pattern: Post-order "found below me" recursion

Problem
-------
Given a binary tree (no ordering) and two nodes p and q that are both in
it, return their lowest common ancestor. A node may be its own ancestor.
Example: root=[3,5,1,6,2,0,8,null,null,7,4], p=5, q=1 -> 3; p=5, q=4 -> 5.

Brute force
-----------
Run one DFS to record the root->p path (a list of nodes), another to
record the root->q path, then walk both lists in parallel and return the
last node they share. O(n) time (two full traversals), O(n) space for the
paths and the stack. The wasted work: the tree is traversed twice, the
shared prefix of both paths is stored twice, and both paths are kept in
memory only to find where they first differ.

From brute force to optimal
---------------------------
Instead of asking "what is the path to p?" and "what is the path to q?"
separately, ask every subtree one question: "do you contain p or q, and
if so give me back the most relevant node?" A post-order recursion returns
p or q when it finds it, propagates that single hit upward, and when a
node receives hits from BOTH children it must be the split point, so it
returns itself from then on. One traversal, no stored paths. The invariant:
lowestCommonAncestor(node) returns None if the subtree has neither target,
the found target if it has exactly one, and the LCA if it has both.

Intuition
---------
The LCA is the first node (bottom-up) whose left and right subtrees each
contribute one of the targets, or that IS one of the targets while the
other lies beneath it. The recursion collapses each subtree into a single
"report" (None / p / q / LCA) and parents only combine two reports.

Geometric view
--------------
Picture two signals rising from p and q toward the root along their
ancestor chains. Each node forwards the signal it receives (or nothing).
The first node where the two signals meet is the LCA; above it, the node
simply forwards "LCA found" without further inspection.

Steps
-----
1. If root is None or root is p or root is q, return root.
2. left = recurse(root.left); right = recurse(root.right).
3. If both non-None: return root (the split point).
4. Else return whichever is non-None (or None).

Complexity: O(n) time, O(h) space — every node visited once; stack depth h.
Pitfalls: comparing node values instead of node identity (values may
repeat); returning early at the first found target and never checking
whether the other is below it (correct here only because both targets are
guaranteed to exist); confusing with the BST variant that uses values.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # returns p / q / their LCA if found in this subtree, else None
        if root is None or root is p or root is q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root          # p and q are on different sides: root is the split point
        return left or right     # both on one side (that side already reports the answer)


def brute_force(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    # Two full searches to record root->p and root->q paths, then compare the paths.
    def path_to(node: Optional[TreeNode], target: TreeNode, path: List[TreeNode]) -> bool:
        if node is None:
            return False
        path.append(node)
        if node is target or path_to(node.left, target, path) or path_to(node.right, target, path):
            return True
        path.pop()
        return False

    a: List[TreeNode] = []
    b: List[TreeNode] = []
    path_to(root, p, a)
    path_to(root, q, b)
    lca = None
    for x, y in zip(a, b):
        if x is not y:
            break
        lca = x
    return lca


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


def find(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Locate the node holding `val` (values unique in the tests)."""
    if root is None or root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)


if __name__ == "__main__":
    s = Solution()
    t = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    cases = [(t, 5, 1, 3), (t, 5, 4, 5), (t, 7, 4, 2), (t, 6, 8, 3), (build([1, 2]), 1, 2, 1)]
    for tree, pv, qv, want in cases:
        p, q = find(tree, pv), find(tree, qv)
        assert s.lowestCommonAncestor(tree, p, q).val == want, (pv, qv)
        assert brute_force(tree, p, q).val == want, (pv, qv)
    print("ok")
