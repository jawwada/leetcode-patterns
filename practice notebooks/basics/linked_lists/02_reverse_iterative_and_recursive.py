"""
Reverse a Linked List, Iterative and Recursive - Basics
Area: linked lists
Key operations: save next before you cut, point cur back to prev, advance prev and cur, unwind recursion and hang head after its old next

Reverse a singly linked list in place and return the new head. The iterative version walks three
pointers (prev, cur, nxt) in O(1) space; the recursive version reverses the rest first, then hooks the
current node behind its old next node.
Example: 1 -> 2 -> 3 -> 4 -> 5 -> 5 -> 4 -> 3 -> 2 -> 1
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
def brute_force(values: List[int]) -> List[int]:
    """Copy the values into a Python list and reverse it. O(n) time, O(n) extra space."""
    return values[::-1]


# --- optimal ---
def solve(head: Optional[ListNode]) -> Optional[ListNode]:
    """Iterative: nxt = cur.next (save), cur.next = prev (cut), both advance. O(n) time, O(1) space."""
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev

def reverse_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse everything after head, then make head's old next point back to head. O(n) time, O(n) stack."""
    if head is None or head.next is None:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


# --- demo ---
def demo():
    reverse_recursive(build_list([1, 2, 3, 4, 5]))  # traced for comparison
    return to_list(solve(build_list([1, 2, 3, 4, 5])))


# --- bugs ---
BUGS = [
    {
        "replace": "        prev, cur = cur, nxt",
        "with":    "        prev, cur = cur, cur.next",
        "fix": "advance cur to the saved nxt; after the cut, cur.next already points backwards",
        "why": "cur.next was just redirected to prev, so cur walks back to prev (or stops at None after the first node): the result is [1] for 1 -> 2 -> 3.",
        "decoys": [
            {"line": "        nxt = cur.next", "change": "should be nxt = cur.next.next"},
            {"line": "        cur.next = prev", "change": "should be prev.next = cur"},
            {"line": "    return prev", "change": "should return head"},
        ],
    },
    {
        "replace": "    head.next.next = head",
        "with":    "    new_head.next = head",
        "fix": "hang head after its OLD next (head.next), which is the tail of the reversed rest, not after new_head",
        "why": "new_head is the far end of the reversed rest; hooking head there drops the middle: 1 -> 2 -> 3 becomes [3, 1].",
        "decoys": [
            {"line": "    if head is None or head.next is None:", "change": "should be only head is None"},
            {"line": "    new_head = reverse_recursive(head.next)", "change": "should recurse on head"},
            {"line": "    head.next = None", "change": "should be head.next = new_head"},
        ],
    },
    {
        "replace": "    return prev",
        "with":    "    return cur",
        "fix": "the loop ends with cur = None; prev is the last node moved, which is the new head",
        "why": "cur is always None when the loop stops, so every non-empty list reverses to nothing.",
        "decoys": [
            {"line": "    prev, cur = None, head", "change": "should be prev, cur = head, head.next"},
            {"line": "        nxt = cur.next", "change": "should be nxt = prev"},
            {"line": "    while cur:", "change": "should be while cur and cur.next:"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
