"""
Same Tree (LeetCode 100)  — Easy
Pattern: Simultaneous tree recursion

Problem
-------
Given two binary trees p and q, return True if they are structurally
identical and every corresponding node has the same value.
Example: p=[1,2,3], q=[1,2,3] -> True; p=[1,2], q=[1,null,2] -> False.

Brute force
-----------
Serialize both trees completely (e.g. preorder with a null marker for every
missing child), then compare the two lists. O(n + m) time and O(n + m)
space. The wasted work is finishing both serializations even when the trees
already differ at the root, and holding two full copies of the trees in
memory just to compare them element by element.

From brute force to optimal
---------------------------
The serialization compares position i of one list with position i of the
other; those positions correspond to the same place in both trees. So
instead of flattening first and comparing later, walk both trees in
lockstep and compare the nodes directly as you reach them. The recursion
can stop at the first mismatch and needs no auxiliary storage beyond the
call stack. The invariant: isSameTree(a, b) is True iff the subtrees
rooted at a and b are identical.

Intuition
---------
Two trees are identical iff their roots agree and their left subtrees are
identical and their right subtrees are identical. That recursive
definition is the algorithm. The base cases: two None nodes match; one
None and one real node do not.

Geometric view
--------------
Overlay the two trees on top of each other and trace them with two
fingers moving in sync: left-left, right-right. The moment one finger
lands on a node and the other on empty space (or on a different value),
stop and answer False.

Steps
-----
1. If either node is None, return True only if both are None.
2. If the values differ, return False.
3. Recurse on (p.left, q.left) and (p.right, q.right); both must be True.

Complexity: O(min(n, m)) time, O(h) space — stops at the first mismatch;
stack depth is the tree height.
Pitfalls: comparing values before checking for None; using `==` on nodes
instead of their .val; treating [1,2] and [1,null,2] as equal because they
have the same in-order values.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None or q is None:
            return p is q            # both None -> True, exactly one None -> False
        return (p.val == q.val
                and self.isSameTree(p.left, q.left)
                and self.isSameTree(p.right, q.right))


def brute_force(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    # Fully serialize both trees (preorder with null markers), then compare the lists.
    def serialize(node: Optional[TreeNode], out: List[Optional[int]]) -> None:
        if node is None:
            out.append(None)
            return
        out.append(node.val)
        serialize(node.left, out)
        serialize(node.right, out)

    a: List[Optional[int]] = []
    b: List[Optional[int]] = []
    serialize(p, a)
    serialize(q, b)
    return a == b


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
    cases = [([1, 2, 3], [1, 2, 3], True),
             ([1, 2], [1, None, 2], False),
             ([1, 2, 1], [1, 1, 2], False),
             ([], [], True),
             ([1], [], False)]
    for a, b, want in cases:
        assert s.isSameTree(build(a), build(b)) is want, (a, b)
        assert brute_force(build(a), build(b)) is want, (a, b)
    print("ok")
