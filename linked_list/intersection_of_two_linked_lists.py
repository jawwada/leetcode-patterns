"""
Intersection of Two Linked Lists (LeetCode 160)  — Easy
Pattern: Length alignment, then lockstep walk

Problem
-------
Given the heads of two singly linked lists that may merge into a shared tail, return the
first node they have in common (by identity, not value), or None. The lists have no cycles
and must not be modified.
Example: A = 4->1->8->4->5, B = 5->6->1->8->4->5 sharing the tail 8->4->5 -> node 8.

Brute force
-----------
For every node of A, walk all of B and check whether that exact node appears.
O(m*n) time, O(1) space. The wasted work: B is re-scanned from its head for every node of
A, even though once the shared tail starts the two lists move in perfect step.

From brute force to optimal
---------------------------
The redundancy is searching B from scratch for each node of A. Observation: after the
merge point both lists share the exact same tail, so the only difference between them is
the length of their private prefixes, |m - n|. If we advance the longer list's pointer by
that difference, both pointers are the same distance from the end, and walking them in
lockstep makes them land on the merge node at the same moment (or both reach None).
Two length counts plus one lockstep walk replace the nested scan; no hash set is needed.

Intuition
---------
Shared tails line up from the right. Counting lengths lets us line the lists up from the
left as well, so "same node" becomes a simple equality check at each step.

Geometric view
--------------
Draw the lists as a Y: two arms joining into one stem. Slide the longer arm's pointer down
until both pointers are equally far from the bottom of the Y; then drop them together one
step at a time. They collide exactly at the fork.

Steps
-----
1. Count m = len(A), n = len(B).
2. Advance the head of the longer list by |m - n| nodes.
3. Walk a and b together until a is b; return a (None if they never meet).

Complexity: O(m + n) time, O(1) space — each list is walked at most twice.
Pitfalls: Comparing node values instead of node identity; forgetting the no-intersection
case (both pointers reach None together, which the loop handles); modifying the lists.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        def length(node: Optional[ListNode]) -> int:
            count = 0
            while node:
                count, node = count + 1, node.next
            return count

        m, n = length(headA), length(headB)
        a, b = headA, headB
        for _ in range(m - n):        # skip the longer private prefix
            a = a.next
        for _ in range(n - m):
            b = b.next
        while a is not b:             # equal distance to the end now: lockstep walk
            a, b = a.next, b.next
        return a


def brute_force(headA: ListNode, headB: ListNode) -> Optional[ListNode]:
    a = headA
    while a:
        b = headB
        while b:                      # rescans all of B for every node of A
            if a is b:
                return a
            b = b.next
        a = a.next
    return None


def build(prefix_a: List[int], prefix_b: List[int], tail: List[int]):
    """Return (headA, headB, first shared node) for lists prefix_a+tail and prefix_b+tail."""
    def chain(vals, rest):
        head = rest
        for v in reversed(vals):
            node = ListNode(v)
            node.next = head
            head = node
        return head

    shared = chain(tail, None)
    return chain(prefix_a, shared), chain(prefix_b, shared), shared


if __name__ == "__main__":
    s = Solution()
    cases = [([4, 1], [5, 6, 1], [8, 4, 5]),
             ([1, 9, 1], [3], [2, 4]),
             ([2, 6, 4], [1, 5], []),
             ([], [7, 7], [3]),
             ([], [], [1])]
    for pa, pb, tail in cases:
        ha, hb, shared = build(pa, pb, tail)
        assert s.getIntersectionNode(ha, hb) is shared
        assert brute_force(ha, hb) is shared
    print("ok")
