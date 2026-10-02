"""
Reorder List (LeetCode 143)  — Medium
Pattern: Find middle + reverse second half + interleave

Problem
-------
Given L0 -> L1 -> ... -> Ln, reorder it in place to L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...
Only node links may be changed, not values.
Example: 1->2->3->4->5 becomes 1->5->2->4->3.

Brute force
-----------
Copy all nodes into an array, then use two indices (front, back) to re-link nodes alternately
from each end. O(n) time, O(n) space. The wasted work: the array exists only to give us "walk
backwards from the end" — random access to the tail — which a singly linked list lacks but which
can be manufactured by reversing the second half.

From brute force to optimal
---------------------------
The redundancy is the O(n) index. Observation: the back half is consumed from the END toward the
middle, i.e. in reverse order; if we physically reverse the second half it becomes a normal
forward list that yields exactly the nodes we need, in order. So: (1) find the middle with
slow/fast pointers, (2) reverse the second half in place, (3) zip the two halves by alternately
splicing one node from each. Three O(n) passes, O(1) space, and all three are standard sub-
routines.

Intuition
---------
The target order is "first half forward" interleaved with "second half backward". Reversing the
second half converts "backward" into "forward", turning the problem into a plain merge of two
lists of equal (or off-by-one) length.

Geometric view
--------------
    1 -> 2 -> 3 -> 4 -> 5           slow stops at 3 (middle)
    1 -> 2 -> 3     5 -> 4          cut after middle, reverse second half
    1 -> 5 -> 2 -> 4 -> 3           zip: take from left, then from right

Steps
-----
1. slow = fast = head; advance fast two steps and slow one until fast.next is None or fast.next.next is None.
2. second = slow.next; slow.next = None (cut); reverse `second`.
3. first = head; while second: save nexts; first.next = second; second.next = first_next; advance both.

Complexity: O(n) time, O(1) space — three linear passes, pointer surgery only.
Pitfalls: not cutting the first half (slow.next = None) creates a cycle; off-by-one in the middle
finding so the first half is shorter than the second (zip must then end on the first half);
losing `first.next` before splicing.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return
        slow, fast = head, head              # 1) find middle (slow ends on last node of first half)
        while fast.next and fast.next.next:
            slow, fast = slow.next, fast.next.next

        second, slow.next = slow.next, None  # 2) cut and reverse second half
        prev = None
        while second:
            second.next, prev, second = prev, second, second.next

        first, second = head, prev           # 3) zip the halves
        while second:
            n1, n2 = first.next, second.next
            first.next, second.next = second, n1
            first, second = n1, n2


def brute_force(head: Optional[ListNode]) -> None:
    nodes = []
    node = head
    while node:
        nodes.append(node)
        node = node.next
    i, j = 0, len(nodes) - 1
    while i < j:
        nodes[i].next = nodes[j]
        i += 1
        if i == j:
            break
        nodes[j].next = nodes[i]
        j -= 1
    if nodes:
        nodes[i].next = None


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
        ([1, 2, 3, 4], [1, 4, 2, 3]),
        ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]),
        ([1], [1]),
        ([1, 2], [1, 2]),
        ([], []),
    ]
    for vals, want in cases:
        h = build(vals)
        s.reorderList(h)
        assert to_list(h) == want
        h2 = build(vals)
        brute_force(h2)
        assert to_list(h2) == want
    print("ok")
