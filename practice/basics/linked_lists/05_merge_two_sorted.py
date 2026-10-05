"""
Merge Two Sorted Lists - Basics
Area: linked lists
Key operations: dummy head, tail pointer, attach the smaller head and advance that list, attach the leftover

Merge two sorted singly linked lists into one sorted list by relinking the existing nodes.
A dummy node gives the result a head to hang off before the first real node is known; tail always
points at the last node attached.
Example: 1 -> 2 -> 4 and 1 -> 3 -> 4 -> 1 -> 1 -> 2 -> 3 -> 4 -> 4
"""
import sys
from typing import List, Optional

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
        log(f"compare a={a.val} b={b.val}: take {'a' if a.val <= b.val else 'b'}")
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
        log(f"    merged {draw(dummy.next)} | a left {draw(a)} | b left {draw(b)}")
    tail.next = a or b
    log(f"attach leftover {draw(a or b)}: {draw(dummy.next)}")
    return dummy.next


# --- demo ---
def demo():
    return to_list(solve(build_list([1, 2, 4]), build_list([1, 3, 4])))


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # the demo already showed the trace; keep the test run silent
    assert to_list(solve(build_list([1, 2, 4]), build_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert to_list(solve(None, None)) == []
    assert to_list(solve(None, build_list([0]))) == [0]
    assert to_list(solve(build_list([5]), None)) == [5]
    assert to_list(solve(build_list([1, 2, 3]), build_list([4, 5]))) == [1, 2, 3, 4, 5]  # one list exhausts first
    assert to_list(solve(build_list([4, 5]), build_list([1, 2, 3]))) == [1, 2, 3, 4, 5]
    assert to_list(solve(build_list([2, 2]), build_list([2]))) == [2, 2, 2]
    import random
    rng = random.Random(7)
    for _ in range(200):
        a = sorted(rng.randint(1, 9) for _ in range(rng.randint(0, 6)))
        b = sorted(rng.randint(1, 9) for _ in range(rng.randint(0, 6)))
        assert to_list(solve(build_list(a), build_list(b))) == brute_force(a, b), (a, b)


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
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
