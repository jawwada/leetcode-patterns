"""
Subtree of Another Tree (LeetCode 572)  — Easy
Pattern: Tree serialization + substring search

Problem
-------
Return True if subRoot is identical (structure and values) to some
subtree of root, including possibly root itself.
Example: root=[3,4,5,1,2], subRoot=[4,1,2] -> True;
root=[3,4,5,1,2,null,null,null,null,0], subRoot=[4,1,2] -> False.

Brute force
-----------
For every node of root, run isSameTree(node, subRoot). O(m * n) time
(n nodes in root, m in subRoot), O(h) space. The repeated work is that
isSameTree re-walks the same region of root for many different starting
nodes: a node deep in root is compared against subRoot once for each
candidate ancestor whose comparison reaches it before failing.

From brute force to optimal
---------------------------
The redundancy is repeated comparison of overlapping regions, which is the
same redundancy naive substring search has. A tree flattened in preorder
with explicit null markers determines the tree uniquely, and the preorder
serialization of a subtree is a CONTIGUOUS substring of its parent's
serialization. So: serialize both once (O(n + m)) and ask whether the
small string occurs in the big one. Python's `in` uses a linear-time
two-way search for long needles (KMP gives the same guarantee), making the
whole thing O(n + m). The one subtlety is tokenization: prefix every value
with a delimiter so "2" does not match inside "12".

Intuition
---------
A subtree is a substring once the tree is written down in preorder with
nulls. Null markers are essential: without them [1,2] and [1,null,2]
would serialize identically. The delimiter before each token stops a
value from matching the tail of a longer value.

Geometric view
--------------
Flatten the big tree into a line of tokens by walking it preorder; the
small tree becomes a short line. Slide the short line along the long one
looking for an exact overlap, exactly like finding a word in a sentence.

Steps
-----
1. serialize(node): None -> ",#"; else "," + val + serialize(left) + serialize(right).
2. big = serialize(root), small = serialize(subRoot).
3. Return small in big.

Complexity: O(n + m) time, O(n + m) space — two serializations plus a
linear substring search.
Pitfalls: omitting null markers (structure lost); forgetting the delimiter
("2" inside "12"); comparing only values in in-order (structure lost).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serialize(node: Optional[TreeNode]) -> str:
            # ',' before every token and '#' for null keep "2" from matching inside "12"
            if node is None:
                return ",#"
            return f",{node.val}" + serialize(node.left) + serialize(node.right)

        return serialize(subRoot) in serialize(root)


def brute_force(root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
    # isSameTree started at every node of root: O(m * n).
    def same(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        if a is None or b is None:
            return a is b
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

    if root is None:
        return subRoot is None
    return (same(root, subRoot)
            or brute_force(root.left, subRoot)
            or brute_force(root.right, subRoot))


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
    cases = [([3, 4, 5, 1, 2], [4, 1, 2], True),
             ([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2], False),
             ([12], [2], False),                 # delimiter test: "2" must not match inside "12"
             ([1], [1], True),
             ([1, 1], [1], True),                # subtree is a leaf deeper down
             ([3, 4, 5, 1, 2], [4, 1], False)]   # [4,1] vs [4,1,2]: structure must match
    for a, b, want in cases:
        assert s.isSubtree(build(a), build(b)) is want, (a, b)
        assert brute_force(build(a), build(b)) is want, (a, b)
    print("ok")
