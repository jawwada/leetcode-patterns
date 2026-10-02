"""
Kth Smallest Element in a BST (LeetCode 230)  — Medium
Pattern: Iterative in-order traversal with early stop

Problem
-------
Given the root of a BST and an integer k, return the k-th smallest value
(1-indexed).
Example: [3,1,4,null,2], k=1 -> 1; [5,3,6,2,4,null,null,1], k=3 -> 3.

Brute force
-----------
Collect every value with any traversal into a list, sort it, and return
index k-1. O(n log n) time, O(n) space. The wasted work is twofold: the
sort ignores that the BST already orders the values, and all n values are
gathered when only the first k are needed.

From brute force to optimal
---------------------------
In-order traversal (left, node, right) of a BST visits values in sorted
order for free, so sorting is unnecessary. And because we can stop as
soon as the k-th node is emitted, we do not need to visit the rest of the
tree. An explicit stack makes the early stop clean: push the left spine,
pop (that is the next smallest), then move to the popped node's right
child and push its left spine. The invariant: the stack holds the
ancestors whose values are the next ones to be emitted, smallest on top.

Intuition
---------
A BST's in-order sequence IS the sorted order. Walk it lazily, counting
down k, and return the value when k hits zero. The iterative stack lets
us pause mid-traversal, which a plain recursive in-order cannot do
without a flag.

Geometric view
--------------
Picture the tree drawn with every node at the x-coordinate of its value.
In-order traversal is a left-to-right sweep. The stack is the chain of
nodes to the right-and-above of the sweep line that are still waiting to
be reported; each pop moves the sweep line one node to the right.

Steps
-----
1. stack = []; node = root.
2. Loop: while node, push node and go left.
3. node = stack.pop(); k -= 1; if k == 0 return node.val.
4. node = node.right; repeat.

Complexity: O(h + k) time, O(h) space — the left spine is pushed once
(h), then each of k pops does amortised O(1) work; the stack never
exceeds the height.
Pitfalls: visiting node before its left subtree (wrong order); treating k
as 0-indexed; using recursion and forgetting to stop once found.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack: List[TreeNode] = []
        node = root
        while True:
            while node:                   # dive left, stacking the ancestors
                stack.append(node)
                node = node.left
            node = stack.pop()            # next value in sorted order
            k -= 1
            if k == 0:
                return node.val
            node = node.right             # then its right subtree's left spine


def brute_force(root: Optional[TreeNode], k: int) -> int:
    # Dump every value, sort, index: O(n log n); ignores the BST ordering entirely.
    vals: List[int] = []

    def walk(node: Optional[TreeNode]) -> None:
        if node:
            vals.append(node.val)
            walk(node.left)
            walk(node.right)

    walk(root)
    return sorted(vals)[k - 1]


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
    cases = [([3, 1, 4, None, 2], 1, 1),
             ([5, 3, 6, 2, 4, None, None, 1], 3, 3),
             ([1], 1, 1),
             ([5, 3, 6, 2, 4, None, None, 1], 6, 6),   # k = n (largest)
             ([2, 1, 3], 2, 2)]
    for vals, k, want in cases:
        assert s.kthSmallest(build(vals), k) == want, (vals, k)
        assert brute_force(build(vals), k) == want, (vals, k)
    print("ok")
