"""
Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105)  — Medium
Pattern: Recursive tree construction with index map

Problem
-------
Given the preorder and inorder traversals of a binary tree with unique
values, rebuild the tree.
Example: preorder=[3,9,20,15,7], inorder=[9,3,15,20,7]
-> [3,9,20,null,null,15,7].

Brute force
-----------
preorder[0] is the root. Find it in inorder with a linear search; the
elements left of it form the left subtree's inorder, the elements right
of it the right subtree's inorder; the next len(left) preorder elements
are the left subtree's preorder, the rest the right's. Recurse on the
sliced lists. O(n^2) time (linear search and list slicing at each of n
nodes; O(n) per level for a skewed tree) and O(n^2) space for the slices.
The repeated work is the search for the root inside inorder, and copying
sub-arrays that are only ever read.

From brute force to optimal
---------------------------
Two independent fixes. First, the linear search answers "where is value v
in inorder?", a question a hash map answers in O(1) after one O(n) pass.
Second, the slices exist only to delimit which part of inorder a subtree
owns; a pair of indices (lo, hi) carries the same information without
copying. The preorder side needs no bounds at all: nodes are consumed
strictly in preorder order, so a single running pointer suffices, because
the left subtree's recursion consumes exactly (mid - lo) preorder entries
before the right subtree starts. Invariant: build(lo, hi) consumes exactly
hi - lo preorder entries and returns the subtree whose inorder occupies
inorder[lo:hi].

Intuition
---------
Preorder tells you WHO the root is (first element); inorder tells you HOW
BIG the left subtree is (everything before the root). Those two facts
split the problem into two smaller identical ones. A hash map makes the
split O(1), and consuming preorder with a pointer keeps the two
traversals in sync without ever slicing.

Geometric view
--------------
Picture inorder as a horizontal line of values; the root splits it into a
left segment and a right segment. The recursion repeatedly cuts segments
at the next preorder value, left segment first. The preorder pointer
moves strictly rightward, one step per node created, while the inorder
window (lo, hi) shrinks around each subtree.

Steps
-----
1. index = {value: position in inorder}; pre = 0.
2. make(lo, hi): if lo >= hi return None.
3. root = TreeNode(preorder[pre]); pre += 1; mid = index[root.val].
4. root.left = make(lo, mid); root.right = make(mid + 1, hi).
5. Return make(0, n).

Complexity: O(n) time, O(n) space — each node is created once with O(1)
map lookups; the map holds n entries (plus O(h) stack).
Pitfalls: building the right subtree before the left (the preorder
pointer must consume the left subtree first); off-by-one on the inorder
bounds; forgetting that values must be unique for the map to be valid.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        index = {v: i for i, v in enumerate(inorder)}   # O(1) "where is the root in inorder?"
        self.pre = 0                                      # next unused preorder entry

        def make(lo: int, hi: int) -> Optional[TreeNode]:
            # builds the subtree whose inorder values occupy inorder[lo:hi]
            if lo >= hi:
                return None
            root = TreeNode(preorder[self.pre])
            self.pre += 1
            mid = index[root.val]
            root.left = make(lo, mid)          # consumes exactly mid - lo preorder entries
            root.right = make(mid + 1, hi)
            return root

        return make(0, len(inorder))


def brute_force(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    # Linear search for the root in inorder and slice both lists at every call: O(n^2).
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    mid = inorder.index(root.val)
    root.left = brute_force(preorder[1:mid + 1], inorder[:mid])
    root.right = brute_force(preorder[mid + 1:], inorder[mid + 1:])
    return root


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
    cases = [([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),
             ([-1], [-1], [-1]),
             ([1, 2], [2, 1], [1, 2]),
             ([1, 2], [1, 2], [1, None, 2]),
             ([1, 2, 4, 5, 3], [4, 2, 5, 1, 3], [1, 2, 3, 4, 5]),
             ([], [], [])]
    for pre, ino, want in cases:
        assert to_list(s.buildTree(pre, ino)) == want, (pre, ino)
        assert to_list(brute_force(pre, ino)) == want, (pre, ino)
    print("ok")
