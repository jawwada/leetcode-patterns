"""
Recover Binary Search Tree (LeetCode 99)  — Hard
Pattern: Inorder traversal with previous-node pointer

Problem
-------
Exactly two nodes of a BST had their values swapped by mistake. Restore
the tree without changing its structure (swap the two values back).
Example: [1,3,null,null,2] -> [3,1,null,null,2]: 1 and 3 were swapped.
Example: [3,1,4,null,null,2] -> [2,1,4,null,null,3]: 2 and 3 were swapped.

Brute force
-----------
Collect the inorder sequence into a list, sort a copy, and compare: the
two positions where list and sorted copy differ are the swapped values.
Then walk the tree again and overwrite those two nodes. O(n log n) time,
O(n) space. The wasted work is the sort and the extra list: a sorted
sequence with two swapped elements is "almost sorted", so a full sort
recomputes order we already know, and storing all n values is unnecessary
when the inorder walk can inspect adjacent pairs as it produces them.

From brute force to optimal
---------------------------
Inorder of a valid BST is strictly increasing, so every adjacent pair has
prev < cur. Swapping two values breaks this at one or two places. If the
swapped nodes are inorder-adjacent (e.g. 1,3,2,4 from 1,2,3,4) there is a
single "dip" 3 > 2, and the culprits are exactly that pair. If they are
far apart (e.g. 1,5,3,4,2,6 from 1,2,3,4,5,6) there are two dips: 5 > 3
and 4 > 2; the first culprit is the LARGER element of the first dip (5),
the second is the SMALLER element of the last dip (2). Both cases are
covered by one rule: on each dip, set first = prev if not already set,
and always set second = cur. The traversal only needs the previous node,
not the whole sequence, so O(h) stack is the only extra space. (Morris
traversal, which threads right pointers through predecessors, brings
that to O(1) but is rarely expected in an interview.)

Intuition
---------
The inorder walk is a ruler laid along the tree; a swap shows up as one
or two places where the ruler reads backwards. The larger value of the
first dip has been pushed too far left; the smaller value of the last
dip has been pushed too far right. Swap those two values back.

Geometric view
--------------
Flatten the BST into its inorder line. A valid BST is a rising staircase.
Two swapped values create a staircase with a bump (one high step that
should be later) and a pit (one low step that should be earlier). The
first falling edge sits just after the bump; the last falling edge sits
just before the pit. Grab the bump and the pit and exchange them.

Steps
-----
1. Iterative inorder with a stack; keep prev (last visited node).
2. On visiting cur: if prev and prev.val > cur.val, that is a dip.
3. On a dip: if first is None, first = prev. Always set second = cur.
4. Continue the walk; at the end swap first.val and second.val.

Complexity: O(n) time, O(h) space — one inorder pass; the explicit stack
holds at most one root-to-leaf path.
Pitfalls: stopping after the first dip (misses the far-apart case);
setting second = prev instead of cur; swapping nodes instead of values
(structure must be preserved); forgetting the adjacent case where the
same dip supplies both culprits.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        first = second = prev = None
        stack: List[TreeNode] = []
        node = root
        while stack or node:
            while node:                            # go as far left as possible
                stack.append(node)
                node = node.left
            node = stack.pop()
            if prev and prev.val > node.val:       # a "dip" in what should be increasing
                if first is None:
                    first = prev                   # the bump: larger value of the first dip
                second = node                      # the pit: smaller value of the LAST dip
            prev = node
            node = node.right
        first.val, second.val = second.val, first.val


def brute_force(root: Optional[TreeNode]) -> None:
    # Inorder -> list, sort a copy, diff the two; then rewrite the tree in inorder. O(n log n).
    def inorder(node: Optional[TreeNode], out: List[TreeNode]) -> None:
        if node:
            inorder(node.left, out)
            out.append(node)
            inorder(node.right, out)

    nodes: List[TreeNode] = []
    inorder(root, nodes)
    target = sorted(n.val for n in nodes)
    for node, want in zip(nodes, target):
        node.val = want                            # only the two swapped positions actually change


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
    """Tree -> LeetCode level-order list with trailing Nones stripped."""
    out: List[Optional[int]] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 3, None, None, 2], [3, 1, None, None, 2]),
             ([3, 1, 4, None, None, 2], [2, 1, 4, None, None, 3]),
             ([1, 2], [2, 1]),                                      # adjacent swap: a single dip
             # root 6 swapped with deepest leaf 1: inorder 6 2 3 4 1 7 8 -> two far-apart dips
             ([1, 2, 7, 6, 4, None, 8, None, None, 3, 5], [6, 2, 7, 1, 4, None, 8, None, None, 3, 5]),
             # siblings 2 and 6 swapped: inorder 1 6 3 4 5 2 7 -> dips 6>3 and 5>2
             ([4, 6, 2, 1, 3, 5, 7], [4, 2, 6, 1, 3, 5, 7])]
    for vals, want in cases:
        t = build(vals)
        s.recoverTree(t)
        assert to_list(t) == want, (vals, to_list(t))
        t = build(vals)
        brute_force(t)
        assert to_list(t) == want, vals
    print("ok")
