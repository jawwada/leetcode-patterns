"""
Merge Two Sorted Lists (LeetCode 21)  — Easy
Pattern: Dummy head + two-pointer merge

Problem
-------
Merge two sorted linked lists into one sorted list by splicing their nodes together; return the
head of the merged list.
Example: 1->2->4 and 1->3->4 -> 1->1->2->3->4->4.

Brute force
-----------
Collect all values from both lists into an array, sort it, and build a new linked list.
O((m+n) log(m+n)) time, O(m+n) space. The wasted work: sorting ignores that each input is ALREADY
sorted — the only unknown is how the two sequences interleave — and allocating new nodes is
unnecessary when the originals can be re-linked.

From brute force to optimal
---------------------------
The redundancy is re-sorting sorted data. Observation: the smallest remaining element overall is
always one of the two list heads, so a single comparison decides the next output node. Keep a
`tail` pointer to the end of the merged list and append the smaller head, advancing that list.
A dummy node before the real head removes the "is this the first node?" special case. When one
list is exhausted, append the other list whole — it is already sorted.

Intuition
---------
Think of two sorted decks face-up; repeatedly take the smaller top card. Because we splice the
existing nodes rather than copy, the merge is in-place and O(1) extra space.

Geometric view
--------------
Three pointers: l1 and l2 on the fronts of the two input chains, tail on the end of the output
chain. Each step one of the input fronts is unhooked and hooked onto tail.

    out:  D -> 1 -> 1 -> 2        l1: 4 -> None
                        tail      l2: 3 -> 4 -> None

Steps
-----
1. dummy = ListNode(); tail = dummy.
2. While both l1 and l2: attach the smaller head to tail.next, advance that list, advance tail.
3. tail.next = l1 or l2 (whichever remains).
4. Return dummy.next.

Complexity: O(m+n) time, O(1) extra space — each node is visited once and re-linked.
Pitfalls: forgetting to attach the leftover list; losing the head without a dummy; using `<`
vs `<=` only affects stability (either is accepted here).
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next, list1 = list1, list1.next
            else:
                tail.next, list2 = list2, list2.next
            tail = tail.next
        tail.next = list1 or list2           # whichever list still has nodes
        return dummy.next


def brute_force(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    vals = []
    for node in (list1, list2):
        while node:
            vals.append(node.val)
            node = node.next
    dummy = ListNode()
    tail = dummy
    for v in sorted(vals):
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
    cases = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([5], [1, 2, 3], [1, 2, 3, 5]),
    ]
    for a, b, want in cases:
        assert to_list(s.mergeTwoLists(build(a), build(b))) == want
        assert to_list(brute_force(build(a), build(b))) == want
    print("ok")
