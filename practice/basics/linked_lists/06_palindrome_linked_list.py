"""
Palindrome Linked List (LeetCode 234) - Basics
Area: linked lists
Key operations: fast and slow to the middle, reverse the second half in place, walk both halves and compare

Return whether a singly linked list reads the same forwards and backwards, in O(n) time and O(1)
extra space: find the middle with fast/slow pointers, reverse the second half in place, then compare
it with the first half node by node.
Example: 1 -> 2 -> 2 -> 1 -> True ;  1 -> 2 -> 3 -> False
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
def brute_force(values: List[int]) -> bool:
    """Copy the values into an array and compare with its reverse. O(n) time, O(n) extra space."""
    return values == values[::-1]


# --- optimal ---
def solve(head: Optional[ListNode]) -> bool:
    """Middle by fast/slow, reverse from the middle on, compare the reversed half with the front. O(n), O(1)."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    prev, cur = None, slow
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left, right = left.next, right.next
    return True


# --- demo ---
def demo():
    return solve(build_list([1, 2, 2, 1]))


# --- bugs ---
BUGS = [
    {
        "replace": "        slow, fast = slow.next, fast.next.next",
        "with":    "        slow, fast = slow.next, fast.next",
        "fix": "fast moves two steps per round so slow stops at the middle",
        "why": "With both pointers moving one step, slow ends on the LAST node: only the two end values get compared and 1 -> 2 -> 3 -> 1 is called a palindrome.",
        "decoys": [
            {"line": "    while fast and fast.next:", "change": "should be while fast.next:"},
            {"line": "    prev, cur = None, slow", "change": "should start cur at slow.next"},
            {"line": "    return True", "change": "should return left is None"},
        ],
    },
    {
        "replace": "    left, right = head, prev",
        "with":    "    left, right = head, cur",
        "fix": "after the in-place reversal, prev is the head of the reversed half; cur has run off to None",
        "why": "right starts as None, the compare loop never runs and every list is reported as a palindrome.",
        "decoys": [
            {"line": "        cur.next = prev", "change": "should be prev.next = cur"},
            {"line": "        if left.val != right.val:", "change": "should be is not"},
            {"line": "        left, right = left.next, right.next", "change": "should move only right"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
