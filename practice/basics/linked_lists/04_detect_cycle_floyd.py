"""
Detect a Cycle with Floyd's Tortoise and Hare - Basics
Area: linked lists
Key operations: slow and fast meet inside the cycle, reset one pointer to head, step both by one to the entry

Given a list whose tail may point back to an earlier node, return the index of the node where the
cycle begins, or -1 if there is no cycle, in O(1) space. build_list(values, pos) links the last node
to the node at index pos (pos = -1 means no cycle).
Example: values [3, 2, 0, -4], pos 1  ->  1   (the tail -4 points back to 2)
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

def build_list(values, pos=-1):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]  # close the cycle
    return nodes[0] if nodes else None

def to_list(head):  # stops at the first node seen twice, so a cycle is drawn once
    out, seen = [], set()
    while head and head not in seen:
        seen.add(head)
        out.append(head.val)
        head = head.next
    return out


# --- brute force ---
def brute_force(head: Optional[ListNode]) -> int:
    """Remember every node with its index; the first node met twice is the entry. O(n) time, O(n) space."""
    seen = {}
    i = 0
    while head:
        if head in seen:
            return seen[head]
        seen[head] = i
        head, i = head.next, i + 1
    return -1


# --- optimal ---
def solve(head: Optional[ListNode]) -> int:
    """Floyd: fast (2 steps) catches slow (1 step) inside the cycle; then head and the meeting point advance by 1 and meet at the entry. O(n), O(1)."""
    log(f"list: {' -> '.join(map(str, to_list(head))) or 'empty'}")
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        log(f"  slow -> {slow.val}, fast -> {fast.val if fast else None}")
        if slow is fast:
            log(f"  meet at node {slow.val}: there is a cycle")
            break
    else:
        log("  fast ran off the end: no cycle")
        return -1
    ptr, index = head, 0
    while ptr is not slow:
        ptr, slow = ptr.next, slow.next
        index += 1
        log(f"  reset walk: ptr -> {ptr.val} (index {index}), slow -> {slow.val}")
    log(f"  ptr and slow meet at index {index}: the cycle entry")
    return index


# --- demo ---
def demo():
    return solve(build_list([3, 2, 0, -4], 1))


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # the demo already showed the trace; keep the test run silent
    assert solve(build_list([3, 2, 0, -4], 1)) == 1
    assert solve(build_list([1, 2], 0)) == 0          # tail points to head
    assert solve(build_list([1], 0)) == 0             # single node pointing to itself
    assert solve(build_list([1], -1)) == -1
    assert solve(build_list([], -1)) == -1
    assert solve(build_list([1, 2, 3, 4, 5], -1)) == -1
    assert solve(build_list([1, 1, 1], -1)) == -1     # equal values are not the same node
    assert solve(build_list([1, 1, 1], 2)) == 2
    import random
    rng = random.Random(7)
    for _ in range(200):
        a = [rng.randint(1, 3) for _ in range(rng.randint(0, 9))]
        pos = rng.randint(-1, len(a) - 1)
        head = build_list(a, pos)
        assert solve(head) == brute_force(head) == (pos if a else -1), (a, pos)


# --- bugs ---
BUGS = [
    {
        "replace": "        if slow is fast:",
        "with":    "        if slow.val == fast.val:",
        "fix": "compare node identity with `is`; two different nodes may hold the same value",
        "why": "On [1, 1, 1] with no cycle the values match after one step, a cycle is reported and the reset walk runs off the end.",
        "decoys": [
            {"line": "    slow = fast = head", "change": "should start fast at head.next"},
            {"line": "    while fast and fast.next:", "change": "should be while fast.next:"},
            {"line": "        return -1", "change": "should return 0"},
        ],
    },
    {
        "replace": "    ptr, index = head, 0",
        "with":    "    ptr, index = head.next, 1",
        "fix": "the reset pointer starts AT head with index 0; the distance head -> entry equals the distance meeting point -> entry",
        "why": "Starting one node in breaks the equal-distance argument: the two pointers chase each other around the cycle forever or meet at the wrong node.",
        "decoys": [
            {"line": "        ptr, slow = ptr.next, slow.next", "change": "should move slow two steps"},
            {"line": "    while ptr is not slow:", "change": "should be while ptr is not fast:"},
            {"line": "        index += 1", "change": "should come before the pointer move"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
