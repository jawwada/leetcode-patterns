"""
Linked List Cycle II (LeetCode 142)  — Medium
Pattern: Floyd's tortoise and hare (fast/slow pointers)

Problem
-------
Given the head of a linked list, return the node where a cycle begins, or None if there is no
cycle. Do not modify the list; aim for O(1) extra space.
Example: 3 -> 2 -> 0 -> -4 -> (back to 2) -> node with value 2.

Brute force
-----------
Walk the list storing every visited node in a set; the first node already in the set is the cycle
start (None if we reach the end). O(n) time, O(n) space. The wasted work: the set remembers every
node just to answer "have I been here?", when the shape of the structure (a rho: tail + loop) can
be probed with two pointers and arithmetic instead.

From brute force to optimal
---------------------------
The redundancy is the O(n) memory. Observation 1: a slow (1 step) and fast (2 step) pointer must
meet inside the loop if one exists, because once both are in the loop fast gains one step per
move on a finite circle. Observation 2: let the tail length be a and the meeting point be b steps
into the loop of length c. slow walked a+b, fast walked 2(a+b), so a+b = k*c, hence a = k*c - b:
walking a more steps from the meeting point lands exactly on the loop entrance. So reset one
pointer to head and advance both one step; they meet at the cycle start.

Intuition
---------
Phase 1 detects the loop with the classic race. Phase 2 uses the race result as a ruler: the
distance from head to the entrance equals the distance from the meeting point to the entrance
(mod the loop length), so two walkers at the same speed from those two points collide on the
entrance.

Geometric view
--------------
A rho shape: a straight tail of length a leading into a circle of length c.

    head --a--> E (entrance)
                 \\__ circle (c) __/   meeting point M is b steps past E

    slow from head, slow2 from M, both 1 step/turn -> they meet at E

Steps
-----
1. slow = fast = head. While fast and fast.next: slow += 1, fast += 2; if slow is fast: break.
2. If fast is None or fast.next is None: no cycle, return None.
3. ptr = head. While ptr is not slow: advance both by one.
4. Return ptr.

Complexity: O(n) time, O(1) space — two pointers, a constant number of passes.
Pitfalls: comparing by value instead of identity (`is`); checking `slow is fast` before the first
move (they start equal); forgetting that fast.next may be None when there is no cycle.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:            # phase 1: race until they meet or fall off
            slow, fast = slow.next, fast.next.next
            if slow is fast:
                break
        else:
            return None                      # loop ended without a meeting: no cycle

        ptr = head                           # phase 2: head and meeting point converge on entrance
        while ptr is not slow:
            ptr, slow = ptr.next, slow.next
        return ptr


def brute_force(head: Optional[ListNode]) -> Optional[ListNode]:
    seen = set()
    node = head
    while node:
        if id(node) in seen:
            return node
        seen.add(id(node))
        node = node.next
    return None


def build(vals: List[int], pos: int) -> Optional[ListNode]:
    nodes = [ListNode(v) for v in vals]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([3, 2, 0, -4], 1),
        ([1, 2], 0),
        ([1], -1),
        ([1, 2, 3, 4, 5], 4),
        ([1, 2, 3], -1),
    ]
    for vals, pos in cases:
        head = build(vals, pos)
        got = s.detectCycle(head)
        want = brute_force(head)
        assert got is want
        if pos == -1:
            assert got is None
        else:
            assert got.val == vals[pos]
    print("ok")
