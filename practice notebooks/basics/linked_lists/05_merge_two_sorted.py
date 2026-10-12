"""
Merge Two Sorted Lists - Basics
Area: linked lists
Key operations: dummy head, tail pointer, attach the smaller head and advance that list, attach the leftover

Merge two sorted singly linked lists into one sorted list by relinking the existing nodes.
A dummy node gives the result a head to hang off before the first real node is known; tail always
points at the last node attached.
Example: 1 -> 2 -> 4 and 1 -> 3 -> 4 -> 1 -> 1 -> 2 -> 3 -> 4 -> 4
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
    """Concatenate and sort, ignoring that both inputs are already sorted. O((n + m) log(n + m))."""
    return sorted(a + b)


# --- optimal ---
def solve(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    """Two-pointer merge: tail takes the smaller head each round; the remaining list is attached whole. O(n + m)."""
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


# --- demo ---
def demo():
    return to_list(solve(build_list([1, 2, 4]), build_list([1, 3, 4])))


# --- bugs ---
BUGS = [
    {
        "replace": "    tail.next = a or b",
        "with":    "    tail.next = a",
        "fix": "whichever list still has nodes is attached: `a or b` picks the non-empty one",
        "why": "When a runs out first the rest of b is dropped: 1 -> 2 merged with 3 -> 4 -> 5 gives [1, 2].",
        "decoys": [
            {"line": "        tail = tail.next", "change": "should be tail = tail.next.next"},
            {"line": "        if a.val <= b.val:", "change": "should be < so b wins ties"},
            {"line": "            b = b.next", "change": "should be b = tail.next"},
        ],
    },
    {
        "replace": "    while a and b:",
        "with":    "    while a or b:",
        "fix": "loop only while BOTH lists have a node to compare; the leftover is attached in one step after the loop",
        "why": "As soon as one list is exhausted the comparison dereferences None and raises AttributeError.",
        "decoys": [
            {"line": "            a = a.next", "change": "should be a = tail.next"},
            {"line": "            tail.next = b", "change": "should be tail = b"},
            {"line": "        tail = tail.next", "change": "should be tail = tail.next.next"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
