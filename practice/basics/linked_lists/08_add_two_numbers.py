"""
Add Two Numbers (LeetCode 2) - Basics
Area: linked lists
Key operations: walk two lists of unequal length, carry across digits, dummy head + tail, emit the final carry

Two non-negative integers are stored as linked lists of digits in reverse order (ones digit first).
Return their sum as a linked list in the same form. Each list has no leading zeros except the number 0.
Example: 2 -> 4 -> 3 (342) plus 5 -> 6 -> 4 (465) -> 7 -> 0 -> 8 (807)
"""
from typing import List, Optional


# --- helpers ---
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def build_list(values):
    dummy = tail = ListNode()
    for v in values:
        tail.next = tail = ListNode(v)
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def draw(head): return " -> ".join(map(str, to_list(head))) or "None"


# --- brute force ---
def brute_force(a: List[int], b: List[int]) -> List[int]:
    """Turn each digit list into an int, add, split the sum back into reversed digits. O(n + m), needs big ints."""
    total = int("".join(map(str, a[::-1]))) + int("".join(map(str, b[::-1])))
    return [int(d) for d in str(total)[::-1]]


# --- optimal ---
def solve(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """Schoolbook addition: per column, sum the digits present plus carry; digit = sum % 10, carry = sum // 10. O(max(n, m))."""
    dummy = tail = ListNode()
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


# --- demo ---
def demo():
    return to_list(solve(build_list([2, 4, 3]), build_list([5, 6, 4])))


# --- bugs ---
BUGS = [
    {
        "replace": "    while l1 or l2 or carry:",
        "with":    "    while l1 or l2:",
        "fix": "keep going while a carry is pending so the last column can create a new most significant digit",
        "why": "5 + 5 should give 0 -> 1; without the carry condition the loop stops after both lists end and returns [0].",
        "decoys": [
            {"line": "        total = carry", "change": "should be total = 0"},
            {"line": "            l1 = l1.next", "change": "should move l1 only if total < 10"},
            {"line": "        tail = tail.next", "change": "should be tail = dummy.next"},
        ],
    },
    {
        "replace": "        carry, digit = divmod(total, 10)",
        "with":    "        digit, carry = divmod(total, 10)",
        "fix": "divmod returns (quotient, remainder): the quotient is the carry, the remainder is the digit",
        "why": "With the pair swapped 7 + 5 writes digit 1 and carries 2; every column with a carry comes out wrong.",
        "decoys": [
            {"line": "    carry = 0", "change": "should be carry = 1"},
            {"line": "        tail.next = ListNode(digit)", "change": "should be ListNode(total)"},
            {"line": "            total += l2.val", "change": "should be total = l2.val"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
