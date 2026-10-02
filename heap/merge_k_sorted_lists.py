"""
Merge k Sorted Lists (LeetCode 23)  — Hard
Pattern: k-way merge with a heap (merge k sorted feeds)

Problem
-------
Given an array of k linked lists, each sorted ascending, merge them into one sorted linked list
and return its head.
Example: [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6].  [] -> [].  [[]] -> [].

Brute force
-----------
Walk every list, dump all N node values into one array, sort it, and rebuild a linked list.
O(N log N) time, O(N) space. The waste: the input is already k sorted runs, and a general sort
ignores that structure completely, re-comparing values whose relative order is already known.
(A second naive idea: each step scan the k current heads for the minimum: O(N * k).)

From brute force to optimal
---------------------------
The redundancy is comparing elements within the same list, which are already ordered. The only
real decision at each step is "which of the k current heads is smallest". The linear scan does
that in O(k); a min-heap holding exactly the k heads does it in O(log k) and, after we take the
smallest, we push that list's next node to restore the k-head invariant. N outputs x log k each
gives O(N log k), strictly better than both O(N log N) and O(N k).

Intuition
---------
Treat the k lists as k decks face-up; the heap holds the top card of each deck. Draw the smallest
top card, then flip the next card of that same deck onto the heap. Repeat until all decks are
empty.

Geometric view
--------------
k horizontal rows of nodes. A frontier of k pointers starts at the leftmost node of each row.
The heap triangle above the rows contains exactly the k pointed-at values with the smallest at
its apex. Pop the apex, advance that row's pointer one step right, push the newly exposed node.
The frontier sweeps right across all rows exactly once.

Steps
-----
1. Push (val, list_index, node) for the head of every non-empty list. The index breaks ties so
   nodes are never compared.
2. Pop the smallest; append its node to the output tail.
3. If that node has a next, push (next.val, i, next).
4. Repeat until the heap is empty; return dummy.next.

Complexity: O(N log k) time, O(k) heap space — the heap never exceeds k entries.
Pitfalls: Pushing (val, node) without a tiebreaker (ListNode is not comparable, TypeError on
equal values); not skipping empty lists; re-linking nodes instead of reusing them (fine, but
must still set tail.next = None at the end if reusing nodes).
"""
import heapq
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
        heapq.heapify(heap)                             # heap of the k current heads
        dummy = tail = ListNode()
        while heap:
            val, i, node = heapq.heappop(heap)          # globally smallest remaining node
            tail.next = node
            tail = node
            if node.next:                               # refill from the same list
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next


def brute_force(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    vals = []
    for node in lists:
        while node:
            vals.append(node.val)
            node = node.next
    vals.sort()                                         # ignores that each list is already sorted
    return build(vals)


def build(vals: List[int]) -> Optional[ListNode]:
    dummy = tail = ListNode()
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
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
        ([], []),
        ([[]], []),
        ([[], [1], []], [1]),                           # mostly empty lists
        ([[5], [1, 2, 3], [-1]], [-1, 1, 2, 3, 5]),
    ]
    for raw, want in cases:
        assert to_list(s.mergeKLists([build(r) for r in raw])) == want, raw
        assert to_list(brute_force([build(r) for r in raw])) == want, raw
    print("ok")
