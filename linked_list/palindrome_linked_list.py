"""
Palindrome Linked List (LeetCode 234)  — Easy
Pattern: Find middle + reverse second half + interleave

Problem
-------
Return True if the singly linked list reads the same forwards and backwards.
Example: 1->2->2->1 -> True; 1->2 -> False.

Brute force
-----------
Copy the values into an array and check arr == arr[::-1] (or two indices from both ends).
O(n) time, O(n) space. The wasted work: we materialise the whole sequence only because a singly
linked list cannot be walked backwards — but we only need to walk the SECOND half backwards, and
that can be arranged by reversing it in place.

From brute force to optimal
---------------------------
The redundancy is O(n) memory for backward access. Observation: a palindrome check compares
position i with position n-1-i, i.e. the first half forward against the second half backward. If
we reverse the second half in place, "second half backward" becomes an ordinary forward walk. So:
find the middle with slow/fast pointers, reverse from the middle, then walk both halves in lock-
step comparing values. Optionally reverse again to restore the list. O(n) time, O(1) space.

Intuition
---------
Fold the list at its midpoint. After folding (reversing the back half), a palindrome has the two
halves lying on top of each other with equal values at every position. For odd lengths the middle
element is compared against nothing and can be ignored.

Geometric view
--------------
    1 -> 2 -> 3 -> 2 -> 1       slow stops at 3 (middle)
    1 -> 2 -> 3    1 -> 2       reverse from middle's next: tail half now reads 1,2,(3)
    ^              ^            compare pairwise: 1==1, 2==2 -> True

Steps
-----
1. slow = fast = head; while fast and fast.next: slow = slow.next; fast = fast.next.next.
2. Reverse the list starting at slow (the second half); call its head `second`.
3. first = head; while second: if first.val != second.val return False; advance both.
4. Return True.

Complexity: O(n) time, O(1) space — one pass to find the middle, one to reverse, one to compare.
Pitfalls: off-by-one in the middle (for odd n the reversed half may include the middle; the
comparison loop must be bounded by the shorter half, which is `while second`); mutating the input
without restoring if the interviewer asks for non-destructive behaviour.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head                   # 1) slow lands on the middle (or right-middle)
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next

        prev = None                          # 2) reverse from the middle onwards
        while slow:
            slow.next, prev, slow = prev, slow, slow.next

        first, second = head, prev           # 3) compare first half with reversed second half
        while second:                        # second half is the shorter (or equal) one
            if first.val != second.val:
                return False
            first, second = first.next, second.next
        return True


def brute_force(head: Optional[ListNode]) -> bool:
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]


def build(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 2, 1], True),
        ([1, 2], False),
        ([1], True),
        ([1, 2, 3, 2, 1], True),
        ([1, 2, 3, 3, 1], False),
        ([], True),
    ]
    for vals, want in cases:
        assert s.isPalindrome(build(vals)) == want
        assert brute_force(build(vals)) == want
    print("ok")
