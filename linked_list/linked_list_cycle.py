"""
Linked List Cycle (LeetCode 141)  — Easy
Pattern: Floyd's tortoise and hare (fast/slow pointers)

Problem
-------
Given the head of a singly linked list, return True if some node can be reached again by
following next pointers (the list has a cycle), else False.
Example: 3->2->0->-4 with -4.next = node 2 -> True; 1 -> None -> False.

Brute force
-----------
Walk the list and remember every node visited in a hash set; seeing a node twice means a
cycle, reaching None means none. O(n) time but O(n) extra space. The waste: we store the
whole path just to answer a yes/no question about whether the walk ever loops.

From brute force to optimal
---------------------------
The set exists only to detect "we are going around in circles". Observation: inside a
cycle of length c, a pointer moving 2 steps per tick gains exactly 1 step per tick on a
pointer moving 1 step, so the gap between them shrinks by one each tick and must hit 0
within c ticks — they meet. Without a cycle the fast pointer simply falls off the end.
So two pointers replace the whole visited set: O(1) space, still O(n) time.
(The original solution started fast two nodes ahead and checked before moving; the
standard form below starts both at head and checks after moving, same idea.)

Intuition
---------
On a straight road the faster runner just finishes; on a circular track the faster runner
must eventually lap the slower one. Meeting = cycle, falling off = no cycle.

Geometric view
--------------
Draw the list as the letter rho (a tail leading into a loop). Slow and fast enter the loop;
think of fast as chasing slow around the circle, closing the gap by one node per tick until
they land on the same node.

Steps
-----
1. slow = fast = head.
2. While fast and fast.next: slow = slow.next, fast = fast.next.next.
3. If slow is fast: return True.
4. Loop exited: fast hit the end, return False.

Complexity: O(n) time, O(1) space — fast catches slow within one lap of the cycle.
Pitfalls: Checking slow is fast before the first move (they start equal); not guarding
fast.next before fast.next.next; comparing values instead of node identity.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
            if slow is fast:          # fast lapped slow inside the loop
                return True
        return False                  # fast fell off the end: the list is a straight line


def brute_force(head: Optional[ListNode]) -> bool:
    seen = set()
    node = head
    while node:
        if id(node) in seen:          # remembers every node just to spot a repeat
            return True
        seen.add(id(node))
        node = node.next
    return False


def build(vals: List[int], pos: int) -> Optional[ListNode]:
    """Build a list; if pos >= 0 the tail links back to the node at index pos."""
    nodes = [ListNode(v) for v in vals]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


if __name__ == "__main__":
    s = Solution()
    cases = [([3, 2, 0, -4], 1, True), ([1, 2], 0, True), ([1], -1, False),
             ([], -1, False), ([1], 0, True), ([1, 2, 3, 4, 5], -1, False)]
    for vals, pos, want in cases:
        head = build(vals, pos)
        assert s.hasCycle(head) is want
        assert brute_force(head) is want
    print("ok")
