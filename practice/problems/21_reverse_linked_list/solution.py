"""
Reverse Linked List (LeetCode 206) - Medium
Area: linked list
Key operations: save nxt, flip cur.next to prev, advance prev and cur, return prev

Given the head of a singly linked list, reverse it in place and return the new head.
Example: 1 -> 2 -> 3 -> 4 -> 5 becomes 5 -> 4 -> 3 -> 2 -> 1
"""
from typing import List, Optional


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
def brute_force(head: Optional[ListNode]) -> Optional[ListNode]:
    """Copy the values into an array, reverse it, build a fresh list. O(n) time and O(n) extra
    space: n new nodes are allocated to express an order the existing next pointers could hold."""
    return build_list(to_list(head)[::-1])


# --- optimal ---
def solve(head: Optional[ListNode]) -> Optional[ListNode]:
    """Walk the list once. At each node save its successor, point the node back at its predecessor,
    then step prev and cur forward. O(n) time, O(1) extra space."""
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


# --- demo ---
def demo():
    return to_list(solve(build_list([1, 2, 3, 4, 5])))


# --- bugs ---
BUGS = [
    {
        "replace": "        cur = nxt",
        "with":    "        cur = cur.next",
        "fix": "advance with the saved nxt: cur.next was just flipped to point backwards",
        "why": "After the flip cur.next is the previous node, so the walk goes backwards and stops at once; [1, 2, 3, 4, 5] returns the list [1].",
        "decoys": [
            {"line": "        nxt = cur.next", "change": "should be nxt = prev.next"},
            {"line": "        prev = cur", "change": "should be prev = nxt"},
            {"line": "    prev, cur = None, head", "change": "should be prev, cur = head, head.next"},
        ],
    },
    {
        "replace": "    return prev",
        "with":    "    return head",
        "fix": "return prev: when the loop ends prev is the last node visited, the new head",
        "why": "head still points at the original first node, which is now the tail with next None, so the result reads as the one-element list [1].",
        "decoys": [
            {"line": "        cur.next = prev", "change": "should be cur.next = nxt"},
            {"line": "        cur = nxt", "change": "should be cur = nxt.next"},
            {"line": "    while cur:", "change": "should be while cur and cur.next:"},
        ],
    },
    {
        "replace": "    while cur:",
        "with":    "    while cur.next:",
        "fix": "loop while cur itself exists; the last node also needs its pointer flipped",
        "why": "The last node is never flipped, so it is left out of the reversed list ([1, 2, 3] gives [2, 1]), and an empty list raises on None.next.",
        "decoys": [
            {"line": "        nxt = cur.next", "change": "should run after cur.next = prev"},
            {"line": "    return prev", "change": "should return prev.next"},
            {"line": "        prev = cur", "change": "should be prev = cur.next"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
