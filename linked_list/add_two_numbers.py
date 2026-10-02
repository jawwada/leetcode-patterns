"""
Add Two Numbers (LeetCode 2)  — Medium
Pattern: Dummy head + carry (schoolbook addition over two lists)

Problem
-------
Two non-empty linked lists hold non-negative integers with digits in reverse order
(342 is 2 -> 4 -> 3). Return their sum as a linked list in the same format.
Example: (2->4->3) + (5->6->4) = (7->0->8), i.e. 342 + 465 = 807.

Brute force
-----------
Convert each list to a Python int by walking it, add the ints, then convert the sum back into a
list digit by digit. O(m + n) time, but it builds big integers proportional to the list length
and breaks the moment the digits exceed fixed-width integers in other languages. The wasted
work is the two conversions: we materialise whole numbers only to tear them apart again.

From brute force to optimal
---------------------------
Addition is already positional: digit i of the sum depends only on digit i of each input and the
carry from digit i-1. Since the lists store the least-significant digit first, we can add as we
walk, emitting one output node per step and carrying at most 1. No conversion, no big integers,
constant extra state.

Intuition
---------
Walk both lists in lockstep. At each step: total = a + b + carry; emit total % 10; carry =
total // 10. Keep going while either list has nodes OR a carry remains, so 999 + 1 grows a
fourth digit. A dummy head avoids special-casing the first node.

Geometric view
--------------
Picture the two lists as two rows of digits aligned at the left (the ones column). A single
cursor sweeps right across both rows and writes a third row beneath, with a 1-wide carry
sliding along above the cursor.

Steps
-----
1. dummy = ListNode(); tail = dummy; carry = 0.
2. While l1 or l2 or carry: sum the available digits and carry.
3. carry, digit = divmod(total, 10); append ListNode(digit); advance tail and the inputs.
4. Return dummy.next.

Complexity: O(max(m, n)) time, O(1) extra space (output excluded) — one pass, one node per digit.
Pitfalls: stopping when both lists end but a carry remains; dereferencing a list that already ended.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
        return dummy.next


def brute_force(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    def to_int(node):
        n, place = 0, 1
        while node:
            n += node.val * place
            place *= 10
            node = node.next
        return n
    total = to_int(l1) + to_int(l2)
    return build([int(c) for c in str(total)[::-1]])


def build(digits: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for d in digits:
        tail.next = ListNode(d)
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
    cases = [([2, 4, 3], [5, 6, 4], [7, 0, 8]), ([0], [0], [0]),
             ([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9], [8, 9, 9, 9, 0, 0, 0, 1])]
    for a, b, want in cases:
        assert to_list(s.addTwoNumbers(build(a), build(b))) == want
        assert to_list(brute_force(build(a), build(b))) == want
    print("ok")
