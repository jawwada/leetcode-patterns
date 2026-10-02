"""
Remove Nth Node From End of List (LeetCode 19)  — Medium
Pattern: Two pointers with fixed gap

Problem
-------
Remove the n-th node from the end of a singly linked list and return the head. n is valid
(1 <= n <= length).
Example: 1->2->3->4->5, n = 2 -> 1->2->3->5.

Brute force
-----------
Pass 1: count the length L. Pass 2: walk to node L-n-1 and unlink its successor. O(n) time,
O(1) space but two full traversals. The wasted work: the first pass exists only to translate
"n from the end" into "L-n from the start"; we traverse every node twice to learn one number.

From brute force to optimal
---------------------------
The redundancy is the counting pass. Observation: we do not need L itself, only a pointer that is
exactly n nodes behind the tail. If a `fast` pointer starts n+1 steps ahead of `slow` and both
move at the same speed, then when fast reaches None, slow is n+1 from the end — i.e. the
predecessor of the node to delete. The gap acts as a ruler carried along the list. A dummy head
lets the same code delete the first node.

Intuition
---------
Carry a measuring stick of length n+1 along the list. When its front end falls off the end, its
back end is on the node just before the one to delete. One pass, no counting.

Geometric view
--------------
    D -> 1 -> 2 -> 3 -> 4 -> 5 -> None        n = 2
    s              f                           gap of n+1 = 3 links
              s              f                 slide together ...
                   s                   f       fast off the end: slow.next is the victim
    D -> 1 -> 2 -> 3 ------> 5                 slow.next = slow.next.next

Steps
-----
1. dummy = ListNode(0, head); slow = fast = dummy.
2. Advance fast n+1 times.
3. While fast: advance slow and fast together.
4. slow.next = slow.next.next.
5. Return dummy.next.

Complexity: O(n) time, O(1) space — a single pass with two pointers.
Pitfalls: deleting the head without a dummy; advancing fast only n times (then slow lands ON
the victim rather than before it); not handling a single-node list.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        slow = fast = dummy
        for _ in range(n + 1):               # open a gap of n+1 links
            fast = fast.next
        while fast:                          # slide both until fast falls off the end
            slow, fast = slow.next, fast.next
        slow.next = slow.next.next           # slow is just before the victim
        return dummy.next


def brute_force(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    length = 0
    node = head
    while node:
        length += 1
        node = node.next
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(length - n):
        prev = prev.next
    prev.next = prev.next.next
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
    cases = [
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),
        ([1], 1, []),
        ([1, 2], 1, [1]),
        ([1, 2], 2, [2]),
    ]
    for vals, n, want in cases:
        assert to_list(s.removeNthFromEnd(build(vals), n)) == want
        assert to_list(brute_force(build(vals), n)) == want
    print("ok")
