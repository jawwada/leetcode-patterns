"""
Reverse Linked List (LeetCode 206)  — Easy
Pattern: In-place pointer reversal

Problem
-------
Given the head of a singly linked list, reverse it and return the new head.
Example: 1 -> 2 -> 3 -> 4 -> 5 becomes 5 -> 4 -> 3 -> 2 -> 1.

Brute force
-----------
Walk the list copying values into a Python list, reverse that list, then build a brand-new linked
list from it. O(n) time, O(n) space. The wasted work: we allocate n new nodes (or an n-element
array) just to re-express an order that can be encoded by re-aiming the existing `next` pointers.

From brute force to optimal
---------------------------
The redundancy is the extra copy. Observation: reversing a list means every node's `next` should
point to its predecessor instead of its successor. We can do that in one pass if, at each node,
we remember the predecessor (`prev`) and save the successor (`nxt`) before overwriting `next`.
Three pointers (prev, cur, nxt) maintain the invariant "prev heads a fully reversed prefix, cur
heads the untouched suffix". When cur runs off the end, prev is the new head.

Intuition
---------
Flip one arrow at a time. The only danger is losing the rest of the list when you flip cur.next,
so stash cur.next first. After the loop, the list that used to hang off `head` now hangs off
`prev`.

Geometric view
--------------
Two chains meet at the boundary between prev and cur: a reversed chain growing leftward and an
untouched chain shrinking rightward.

    None <- 1 <- 2    3 -> 4 -> 5 -> None
            prev     cur  nxt

Each step detaches cur from the right chain and pushes it onto the left chain.

Steps
-----
1. prev = None, cur = head.
2. While cur: nxt = cur.next; cur.next = prev; prev = cur; cur = nxt.
3. Return prev.

Complexity: O(n) time, O(1) space — one pass, three pointers.
Pitfalls: overwriting cur.next before saving it (loses the tail); returning head instead of prev;
forgetting that the old head must end with next = None (handled since prev starts as None).
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, cur = None, head
        while cur:
            nxt = cur.next                   # save the rest before flipping the arrow
            cur.next = prev
            prev, cur = cur, nxt
        return prev


def brute_force(head: Optional[ListNode]) -> Optional[ListNode]:
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    dummy = ListNode()
    tail = dummy
    for v in reversed(vals):
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def build(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node: Optional[ListNode]) -> List[int]:
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


if __name__ == "__main__":
    s = Solution()
    for vals in ([1, 2, 3, 4, 5], [1, 2], [], [7]):
        want = vals[::-1]
        assert to_list(s.reverseList(build(vals))) == want
        assert to_list(brute_force(build(vals))) == want
    print("ok")
