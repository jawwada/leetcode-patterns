"""
Merge Two Sorted Lists (LeetCode 21) - Medium
Area: linked list
Key operations: dummy head, tail pointer, attach the smaller front node, advance that list, attach the leftover

Merge two sorted linked lists into one sorted list by splicing their nodes together; return the
head of the merged list.
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


def build_list(values: List[int]) -> Optional[ListNode]:
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(node: Optional[ListNode]) -> List[int]:
    return [] if node is None else [node.val] + to_list(node.next)


# --- brute force ---
def brute_force(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """Collect every value, sort, build a new list. O((m+n) log(m+n)) time, O(m+n) space: the sort
    ignores that both inputs are already sorted, and new nodes replace ones that could be relinked."""
    return build_list(sorted(to_list(l1) + to_list(l2)))


# --- optimal ---
def solve(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """A dummy node starts the output and tail is always its last node. Each step moves the smaller
    front node behind tail and advances that list; the leftover list is attached whole.
    O(m + n) time, O(1) extra space."""
    dummy = ListNode()
    tail = dummy
    while l1 and l2:
        log(f"l1: {' -> '.join(map(str, to_list(l1)))} -> None   l2: {' -> '.join(map(str, to_list(l2)))} -> None")
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
            log(f"    {tail.next.val} <= {l2.val}: take the front of l1")
        else:
            tail.next = l2
            l2 = l2.next
            log(f"    {l1.val} > {tail.next.val}: take the front of l2")
        tail = tail.next
        log("    merged: dummy -> " + " -> ".join(map(str, to_list(dummy.next)[:len(to_list(dummy.next)) - len(to_list(tail.next))])) + f"   (tail = {tail.val})")
    tail.next = l1 or l2
    log(f"one list is empty: attach the rest {to_list(l1 or l2)} behind tail")
    log(f"merged list: {' -> '.join(map(str, to_list(dummy.next)))} -> None")
    return dummy.next


# --- demo ---
def demo():
    return to_list(solve(build_list([1, 2, 4]), build_list([1, 3, 4])))


# --- tests ---
def tests():
    assert to_list(solve(build_list([1, 2, 4]), build_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert solve(None, None) is None  # both empty
    assert to_list(solve(None, build_list([0]))) == [0]
    assert to_list(solve(build_list([0]), None)) == [0]
    assert to_list(solve(build_list([5]), build_list([1, 2, 3]))) == [1, 2, 3, 5]  # l2 runs out last
    assert to_list(solve(build_list([1, 2, 3]), build_list([5]))) == [1, 2, 3, 5]  # l1 runs out first
    assert to_list(solve(build_list([1, 1]), build_list([1]))) == [1, 1, 1]  # duplicates
    a, b = build_list([1, 3]), build_list([2])
    merged = solve(a, b)
    assert merged is a and a.next is b  # in place: the original nodes are relinked
    import random
    rng = random.Random(21)
    for _ in range(200):
        x = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
        y = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
        assert to_list(solve(build_list(x), build_list(y))) == to_list(brute_force(build_list(x), build_list(y))), (x, y)


# --- bugs ---
BUGS = [
    {
        "replace": "    while l1 and l2:",
        "with":    "    while l1 or l2:",
        "fix": "loop only while both lists have a front node to compare: l1 and l2",
        "why": "Once one list is exhausted the comparison reads .val on None and raises; the leftover must be attached whole after the loop instead.",
        "decoys": [
            {"line": "        tail = tail.next", "change": "should be tail = tail.next.next"},
            {"line": "    tail.next = l1 or l2", "change": "should be tail.next = l1 and l2"},
            {"line": "    return dummy.next", "change": "should return tail"},
        ],
    },
    {
        "replace": "    tail.next = l1 or l2",
        "with":    "    tail.next = l1",
        "fix": "attach whichever list still has nodes: l1 or l2",
        "why": "When l1 runs out first, l1 is None and the rest of l2 is dropped; [1, 2, 3] merged with [5] gives [1, 2, 3].",
        "decoys": [
            {"line": "        if l1.val <= l2.val:", "change": "should be l1.val < l2.val"},
            {"line": "    tail = dummy", "change": "should be tail = dummy.next"},
            {"line": "            l2 = l2.next", "change": "should run before tail.next = l2"},
        ],
    },
    {
        "replace": "    return dummy.next",
        "with":    "    return dummy",
        "fix": "the dummy is a placeholder; the merged list starts at dummy.next",
        "why": "Returning the dummy puts its value 0 at the front of the result, so [1, 2, 4] merged with [1, 3, 4] reads [0, 1, 1, 2, 3, 4, 4].",
        "decoys": [
            {"line": "            tail.next = l1", "change": "should be tail = l1"},
            {"line": "        tail = tail.next", "change": "should be removed"},
            {"line": "    dummy = ListNode()", "change": "should be ListNode(l1.val)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
