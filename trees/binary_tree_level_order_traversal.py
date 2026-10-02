"""
Binary Tree Level Order Traversal (LeetCode 102)  — Medium
Pattern: BFS by level (queue snapshot)

Problem
-------
Return the node values level by level, left to right, as a list of lists.
Example: [3,9,20,null,null,15,7] -> [[3],[9,20],[15,7]].

Brute force
-----------
Compute the height h, then for each depth d = 0..h-1 run a fresh DFS over
the whole tree collecting nodes whose depth equals d. O(n * h) time
(O(n^2) for a skewed tree), O(h) stack space. The repeated work is the
traversal: every DFS pass walks ALL n nodes but keeps only the ones on a
single level, so each node is visited h times.

From brute force to optimal
---------------------------
The brute force re-discovers the nodes of level d+1 while it is already
standing on level d (they are the children of what it just collected).
So keep them: a FIFO queue naturally holds "the frontier" in left-to-right
order, and if we remember how many nodes were in the queue when a level
started, popping exactly that many yields one complete level while their
children accumulate behind. Every node is enqueued and dequeued once. The
invariant: at the top of the outer loop the queue contains exactly the
nodes of one level, in left-to-right order.

Intuition
---------
BFS visits nodes in distance order. The only extra trick for grouping is
the level snapshot: len(queue) at the start of a round is the size of the
current level, because all of its nodes are already there and none of
their children have been added yet.

Geometric view
--------------
Picture a horizontal line sweeping down the drawing of the tree one row
at a time. The queue is the set of nodes currently on the line; each round
replaces the line's nodes by their children, left to right, so the next
row is already in order.

Steps
-----
1. If root is None return []. queue = deque([root]).
2. While queue is non-empty: size = len(queue); level = [].
3. Pop size nodes, appending each value to level and enqueueing its
   non-None children.
4. Append level to the result.

Complexity: O(n) time, O(w) space — each node enqueued once; the queue
holds at most one level (width w, up to n/2).
Pitfalls: reading len(queue) inside the loop (it changes as children are
added); enqueueing None children; forgetting the empty-tree case.
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        result: List[List[int]] = []
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):       # snapshot: exactly the nodes of this level
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result


def brute_force(root: Optional[TreeNode]) -> List[List[int]]:
    # For each depth d run a fresh DFS that collects nodes at exactly depth d: O(n * h).
    def height(node: Optional[TreeNode]) -> int:
        return 0 if node is None else 1 + max(height(node.left), height(node.right))

    def collect(node: Optional[TreeNode], depth: int, target: int, out: List[int]) -> None:
        if node is None:
            return
        if depth == target:
            out.append(node.val)
        else:
            collect(node.left, depth + 1, target, out)
            collect(node.right, depth + 1, target, out)

    result = []
    for d in range(height(root)):
        level: List[int] = []
        collect(root, 0, d, level)
        result.append(level)
    return result


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
    cases = [([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
             ([1], [[1]]), ([], []),
             ([1, 2, 3, 4, None, None, 5], [[1], [2, 3], [4, 5]]),
             ([1, None, 2, None, 3], [[1], [2], [3]])]
    for vals, want in cases:
        assert s.levelOrder(build(vals)) == want, vals
        assert brute_force(build(vals)) == want, vals
    print("ok")
