"""
Middle of the Linked List with Fast and Slow Pointers - Basics
Area: linked lists
Key operations: slow moves one, fast moves two, stop when fast or fast.next is None

Return the middle node of a singly linked list in one pass without counting. For an even length
there are two middles; return the second one (the right middle), which is what
`while fast and fast.next` gives for free.
Example: 1 -> 2 -> 3 -> 4 -> 5 -> 3 ;  1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 4
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

def draw(head, **marks):  # "1 -> 2(slow) -> 3(fast)"
    parts = []
    while head:
        tag = ",".join(k for k, n in marks.items() if n is head)
        parts.append(f"{head.val}({tag})" if tag else str(head.val))
        head = head.next
    return " -> ".join(parts) or "None"


# --- brute force ---
def brute_force(values: List[int]) -> Optional[int]:
    """Count the nodes, then walk to index n // 2: two passes. O(n)."""
    return values[len(values) // 2] if values else None


# --- optimal ---
def solve(head: Optional[ListNode]) -> Optional[ListNode]:
    """Slow steps 1, fast steps 2; when fast cannot take two more steps, slow is the middle. O(n), one pass."""
    slow = fast = head
    log(f"start: {draw(head, slow=slow, fast=fast)}")
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        log(f"step:  {draw(head, slow=slow, fast=fast)}   fast={'None' if fast is None else fast.val}")
    log(f"stop: fast is {'None (even length: slow is the right middle)' if fast is None else 'the last node (odd length)'}; middle = {slow.val if slow else None}")
    return slow


# --- demo ---
def demo():
    return solve(build_list([1, 2, 3, 4, 5, 6])).val


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # the demo already showed the trace; keep the test run silent
    assert solve(build_list([1, 2, 3, 4, 5])).val == 3
    assert solve(build_list([1, 2, 3, 4, 5, 6])).val == 4      # even length: the right middle
    assert to_list(solve(build_list([1, 2, 3, 4]))) == [3, 4]  # the node, with its tail intact
    assert solve(None) is None
    assert solve(build_list([7])).val == 7
    assert solve(build_list([7, 8])).val == 8
    assert solve(build_list([5, 5, 5])).val == 5
    import random
    rng = random.Random(7)
    for _ in range(200):
        a = [rng.randint(1, 9) for _ in range(rng.randint(0, 10))]
        mid = solve(build_list(a))
        assert (mid.val if mid else None) == brute_force(a), a
        assert to_list(mid) == a[len(a) // 2:], a


# --- bugs ---
BUGS = [
    {
        "replace": "    while fast and fast.next:",
        "with":    "    while fast.next and fast.next.next:",
        "fix": "test fast itself first: it is None after an even-length list, and the loop must run while fast can take two steps",
        "why": "Dropping the `fast` check crashes on an empty list and stops one step early on even lengths, returning the LEFT middle (2 for 1 -> 2 -> 3 -> 4).",
        "decoys": [
            {"line": "        slow = slow.next", "change": "should be slow = slow.next.next"},
            {"line": "    slow = fast = head", "change": "should start fast at head.next"},
            {"line": "    return slow", "change": "should return fast"},
        ],
    },
    {
        "replace": "        fast = fast.next.next",
        "with":    "        fast = fast.next",
        "fix": "fast must move two nodes per step so that slow covers exactly half the distance",
        "why": "With both pointers moving one step the loop runs to the end and slow stops on the last node, not the middle.",
        "decoys": [
            {"line": "    while fast and fast.next:", "change": "should be while fast.next:"},
            {"line": "        slow = slow.next", "change": "should move slow only when fast is not None"},
            {"line": "    return solve(build_list([1, 2, 3, 4, 5, 6])).val", "change": "should return the node"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
