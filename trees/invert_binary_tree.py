"""
Invert Binary Tree (LeetCode 226)  — Easy
Pattern: Tree recursion (post-order)

Problem
-------
Given the root of a binary tree, mirror it: every node's left and right
children are swapped, recursively. Return the root.
Example: [4,2,7,1,3,6,9] -> [4,7,2,9,6,3,1].

Brute force
-----------
Build a brand-new mirrored tree: for each node allocate a copy whose left
child is the mirror of the original right subtree and vice versa.
O(n) time, O(n) extra space. The wasted work is the allocation: every node
is copied although nothing about it changes except which pointer is called
"left" and which "right".

From brute force to optimal
---------------------------
The copy is redundant because node values never change; only the two child
pointers of each node need to trade places, and that is a local O(1)
operation. So one traversal that visits each node once and swaps its
children in place is sufficient. Recursion (or an explicit stack / queue)
is only the vehicle for reaching every node; the invariant is "when the
call on a node returns, its whole subtree is mirrored".

Intuition
---------
mirror(T) = node with children (mirror(T.right), mirror(T.left)). A tree is
mirrored exactly when every node has had its children swapped, so one swap
per node does the whole job. The order does not matter: swap first then
recurse, or recurse then swap, both are correct.

Geometric view
--------------
Fold the drawing of the tree along the vertical line through the root.
Every node keeps its depth; only its horizontal position flips. The
recursion walks down each path and flips the two "arms" of each node on
the way back up.

Steps
-----
1. If the node is None, return None (base case).
2. Recursively invert the right and left subtrees.
3. Assign node.left = inverted right, node.right = inverted left (tuple swap).
4. Return the node.

Complexity: O(n) time, O(h) space — each node is visited once; the recursion
stack is as deep as the tree height h.
Pitfalls: swapping with two plain assignments and losing one child (use a
tuple swap or a temp); forgetting the None base case.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        # tuple swap: both recursive results are computed before either pointer is overwritten
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root


def brute_force(root: Optional[TreeNode]) -> Optional[TreeNode]:
    # Allocate a mirrored copy of every node instead of swapping pointers in place.
    if root is None:
        return None
    copy = TreeNode(root.val)
    copy.left = brute_force(root.right)
    copy.right = brute_force(root.left)
    return copy


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


def to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Tree -> LeetCode level-order list with trailing Nones trimmed."""
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    s = Solution()
    assert to_list(s.invertTree(build([4, 2, 7, 1, 3, 6, 9]))) == [4, 7, 2, 9, 6, 3, 1]
    assert to_list(s.invertTree(build([2, 1, 3]))) == [2, 3, 1]
    assert to_list(s.invertTree(build([]))) == []
    assert to_list(s.invertTree(build([1, None, 2]))) == [1, 2]
    for vals in ([4, 2, 7, 1, 3, 6, 9], [2, 1, 3], [], [1, None, 2]):
        assert to_list(brute_force(build(vals))) == to_list(s.invertTree(build(vals)))
    print("ok")
