"""
Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)  — Medium
Pattern: BST ordered descent

Problem
-------
Given a BST and two of its nodes p and q, return their lowest common
ancestor: the deepest node that has both p and q as descendants (a node
counts as its own descendant).
Example: root=[6,2,8,0,4,7,9,null,null,3,5], p=2, q=8 -> 6; p=2, q=4 -> 2.

Brute force
-----------
Record the root->p path and the root->q path as lists (each found by
descending the BST), then walk both lists in parallel and return the last
node they share. O(h) time, O(h) space. The wasted work: two separate
descents that cover the same prefix, plus storing both paths just to find
where they diverge.

From brute force to optimal
---------------------------
The two paths are identical until the first node where p and q fall on
different sides, and that node is exactly the LCA. In a BST "which side"
is decided by comparing values: if both p.val and q.val are smaller than
node.val, both paths go left; if both are larger, both go right;
otherwise they split here (or node IS one of them). So a single descent
from the root that stops at the first split finds the LCA with O(1) extra
space and no path storage. The invariant: the current node is an ancestor
of both p and q.

Intuition
---------
In a BST the LCA is the first node on the way down from the root whose
value lies between p.val and q.val (inclusive). Above it both targets are
on the same side; below it they are separated.

Geometric view
--------------
Think of the BST drawn on a number line: every node splits its interval
into "less than me" (left) and "greater than me" (right). Walk down while
the interval [min(p,q), max(p,q)] sits wholly on one side; the first node
whose value falls inside that interval is the answer.

Steps
-----
1. lo, hi = min(p.val, q.val), max(p.val, q.val); node = root.
2. While node: if hi < node.val go left; elif lo > node.val go right;
   else return node.

Complexity: O(h) time, O(1) space — one pointer walks a single root-to-LCA
path; h is the height (log n if balanced, n if skewed).
Pitfalls: using strict inequalities for the split (the LCA may be p or q
itself); applying this value-based trick to a non-BST (it needs the
ordering invariant).
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
        lo, hi = min(p.val, q.val), max(p.val, q.val)
        node = root
        while node:
            if hi < node.val:
                node = node.left          # both targets lie in the left subtree
            elif lo > node.val:
                node = node.right         # both lie in the right subtree
            else:
                return node               # lo <= node.val <= hi: they split here
        return None


def brute_force(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    # Record the full root->p and root->q paths, then take the last node they share.
    def path_to(target: TreeNode) -> List[TreeNode]:
        path, node = [], root
        while node is not target:
            path.append(node)
            node = node.left if target.val < node.val else node.right
        path.append(node)
        return path

    a, b = path_to(p), path_to(q)
    lca = root
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
    """Locate the node holding `val` in a BST."""
    while root and root.val != val:
        root = root.left if val < root.val else root.right
    return root


if __name__ == "__main__":
    s = Solution()
    t = build([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    cases = [(t, 2, 8, 6), (t, 2, 4, 2), (t, 3, 5, 4), (t, 0, 9, 6), (build([2, 1]), 2, 1, 2)]
    for tree, pv, qv, want in cases:
        p, q = find(tree, pv), find(tree, qv)
        assert s.lowestCommonAncestor(tree, p, q).val == want, (pv, qv)
        assert brute_force(tree, p, q).val == want, (pv, qv)
    print("ok")
