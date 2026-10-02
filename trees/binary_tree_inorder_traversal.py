"""
Binary Tree Inorder Traversal (LeetCode 94)  — Easy
Pattern: Iterative traversal with an explicit stack

Problem
-------
Return the values of a binary tree in inorder: left subtree, then the node, then the right
subtree. The follow-up asks for an iterative solution.
Example: root = [1,null,2,3] -> [1,3,2].

Brute force
-----------
The first idea is the textbook recursion inorder(left); visit(node); inorder(right) — this
was the original solution. O(n) time, O(h) space on the call stack. Nothing is recomputed,
but the stack is hidden inside the interpreter: a skewed tree of 10^4+ nodes overflows
Python's recursion limit, and you cannot pause, resume or stop the traversal early.

From brute force to optimal
---------------------------
The recursion's only state is "which ancestors are still waiting to be visited". Each
pending frame is a node whose left subtree is in progress. Observation: that is exactly a
stack of nodes, and the frames are always created by sliding left. So simulate it: slide
left from the current node pushing every node on the way; when you hit None, pop — that
node's left side is done, so visit it — and continue from its right child. Same O(n) time
and O(h) space, but the stack is explicit, iterative, and pausable (the basis of BST
iterators and kth-smallest with early stop).

Intuition
---------
Inorder visits a node only after its whole left spine is finished. The stack holds the
left spine of the current position; popping means "left is done, my turn", and moving to
the right child starts a fresh left spine.

Geometric view
--------------
Picture a cursor descending the tree diagonally to the bottom-left, dropping a breadcrumb
(push) at every node. At the bottom it picks up the latest breadcrumb (pop, visit), takes
one step right, and dives bottom-left again. The output reads the tree left to right as if
projected onto the x-axis.

Steps
-----
1. stack = [], node = root, out = [].
2. While node or stack:
3.   While node: push node, node = node.left  (slide down the left spine).
4.   node = stack.pop(); out.append(node.val); node = node.right.
5. Return out.

Complexity: O(n) time, O(h) space — each node is pushed and popped once; the stack holds
one root-to-leaf spine.
Pitfalls: Loop condition `while stack` alone (the loop exits as soon as the stack empties,
e.g. after popping the root, skipping its right subtree); visiting a node when it is pushed
rather than popped (that gives preorder).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        out: List[int] = []
        stack: List[TreeNode] = []
        node = root
        while node or stack:
            while node:                   # slide down the left spine, leaving breadcrumbs
                stack.append(node)
                node = node.left
            node = stack.pop()            # left side finished: visit this node
            out.append(node.val)
            node = node.right             # then start the right subtree's left spine
        return out


def brute_force(root: Optional[TreeNode]) -> List[int]:
    out: List[int] = []

    def inorder(node: Optional[TreeNode]) -> None:   # call stack holds the pending nodes
        if node:
            inorder(node.left)
            out.append(node.val)
            inorder(node.right)

    inorder(root)
    return out


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
    cases = [([1, None, 2, 3], [1, 3, 2]), ([], []), ([1], [1]),
             ([4, 2, 6, 1, 3, 5, 7], [1, 2, 3, 4, 5, 6, 7]), ([1, 2, None, 3], [3, 2, 1])]
    for vals, want in cases:
        assert s.inorderTraversal(build(vals)) == want
        assert brute_force(build(vals)) == want
    print("ok")
