"""
Closest Binary Search Tree Value II (LeetCode 272)  — Hard
Pattern: Two lazy inorder iterators (predecessor / successor stacks)

Problem
-------
Given a BST, a float target and an integer k, return the k values in the
tree closest to target (any order). k is at most the number of nodes.
Example: root=[4,2,5,1,3], target=3.714286, k=2 -> [4,3].
Example: root=[1], target=0.0, k=1 -> [1].

Brute force
-----------
Inorder the whole tree into a sorted list of n values, sort that list by
|value - target|, and take the first k. O(n log n) time, O(n) space. The
wasted work is twofold: we materialise all n values when only k matter,
and we re-sort a list that inorder already delivered sorted; the k
nearest values to target are simply a contiguous window of that sorted
list around target.

From brute force to optimal
---------------------------
Step one, O(n): since inorder is sorted, the answer is a window of k
consecutive values straddling target. Keep a deque of the last k values
seen; when the next value is closer than the deque's front, pop the front
and push the new one; once the next value is farther than the front, the
window can only get worse, so stop. Still O(n) worst case because the
window may sit at the far right. Step two, O(h + k): do not walk the whole
inorder. Build two lazy iterators from the root search path: a
"predecessor" stack holding every node <= target on the path (its top is
the largest such node, and advancing it means taking the top's left
subtree's rightmost chain) and a "successor" stack of nodes > target
(top is the smallest, advanced symmetrically). Then merge like two sorted
lists: k times, pop whichever top is closer to target and refill it. Each
stack is a standard iterative inorder iterator, so every refill costs
amortised O(1) and the whole query is O(h + k).

Intuition
---------
Target splits the sorted inorder sequence into a left half (predecessors,
read right-to-left) and a right half (successors, read left-to-right).
Both halves are sorted by distance to target as you move away from it, so
the k closest values are obtained by a k-step merge of the two halves.
Two iterators give exactly those two halves lazily, without listing them.

Geometric view
--------------
Stand on the number line at target. The BST's inorder values sit on the
line; walking from the root to target leaves a trail of nodes, some to the
left (pred stack) and some to the right (succ stack). Each stack is a
flashlight pointing away from target that illuminates one value at a
time; k times, read the nearer lit value and step that flashlight one
value further out.

Steps
-----
1. Walk from root toward target: push nodes with val <= target on pred,
   others on succ (standard BST descent).
2. next_pred(): pop top p; walk p.left then repeatedly .right, pushing each
   onto pred. Return p.val. next_succ() mirrors it.
3. Repeat k times: if succ is empty or (pred non-empty and target - pred.top
   <= succ.top - target) take from pred, else from succ.
4. Return the collected values.

Complexity: O(h + k) time, O(h) space — the initial descent is O(h), each
of the k steps is amortised O(1), and both stacks hold at most one
root-to-leaf path.
Pitfalls: refilling the stack with the wrong subtree (pred must go left
then all the way right); putting nodes equal to target on both stacks
(duplicates); walking the whole tree with an inorder list (O(n), the
interviewer asks for the follow-up).
"""
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def closestKValues(self, root: Optional[TreeNode], target: float, k: int) -> List[int]:
        pred: List[TreeNode] = []                  # nodes <= target; top is the largest of them
        succ: List[TreeNode] = []                  # nodes >  target; top is the smallest of them
        node = root
        while node:                                # the search path splits into the two stacks
            if node.val <= target:
                pred.append(node)
                node = node.right
            else:
                succ.append(node)
                node = node.left

        def next_pred() -> int:                    # pop the largest, then expose the next largest
            node = pred.pop()
            child = node.left
            while child:
                pred.append(child)
                child = child.right
            return node.val

        def next_succ() -> int:                    # pop the smallest, then expose the next smallest
            node = succ.pop()
            child = node.right
            while child:
                succ.append(child)
                child = child.left
            return node.val

        out: List[int] = []
        for _ in range(k):                         # k-way merge of two sorted streams
            if not succ or (pred and target - pred[-1].val <= succ[-1].val - target):
                out.append(next_pred())
            else:
                out.append(next_succ())
        return out


def brute_force(root: Optional[TreeNode], target: float, k: int) -> List[int]:
    # Inorder every value into a list, sort all n of them by distance to target, keep k: O(n log n).
    vals: List[int] = []

    def inorder(node: Optional[TreeNode]) -> None:
        if node:
            inorder(node.left)
            vals.append(node.val)
            inorder(node.right)

    inorder(root)
    vals.sort(key=lambda v: abs(v - target))
    return vals[:k]


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
    cases = [([4, 2, 5, 1, 3], 3.714286, 2, [3, 4]),
             ([1], 0.0, 1, [1]),
             ([4, 2, 5, 1, 3], 3.714286, 5, [1, 2, 3, 4, 5]),          # k = n: everything
             ([4, 2, 5, 1, 3], 0.5, 2, [1, 2]),                        # target left of every value
             ([4, 2, 5, 1, 3], 9.0, 3, [3, 4, 5]),                     # target right of every value
             ([8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15], 6.5, 4, [5, 6, 7, 8]),
             ([2, 1, 3], 2.0, 1, [2])]                                 # exact hit sits on pred stack
    for vals, target, k, want in cases:
        assert sorted(s.closestKValues(build(vals), target, k)) == want, (vals, target, k)
        assert sorted(brute_force(build(vals), target, k)) == want, (vals, target, k)
    print("ok")
