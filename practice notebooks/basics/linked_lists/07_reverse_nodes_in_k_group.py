"""
Reverse Nodes in k-Group (LeetCode 25) - Basics
Area: linked lists
Key operations: probe k nodes ahead, reverse one group with the next group as the initial prev, hook group_prev to the new head, advance group_prev to the old head

Reverse every k consecutive nodes of a singly linked list; a final group shorter than k is left as is.
Only node links may change, not values.
Example: 1 -> 2 -> 3 -> 4 -> 5, k = 2 -> 2 -> 1 -> 4 -> 3 -> 5
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
def brute_force(values: List[int], k: int) -> List[int]:
    """Reverse each full k-slice of a copied array. O(n) time, O(n) extra space."""
    out = list(values)
    for i in range(0, len(out) - k + 1, k):
        out[i:i + k] = out[i:i + k][::-1]
    return out


# --- optimal ---
def solve(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """Per group: find its k-th node (stop if missing), reverse it with prev seeded to the next group, re-hook. O(n), O(1)."""
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        tail = group_prev.next
        group_prev.next = kth
        group_prev = tail


# --- demo ---
def demo():
    return to_list(solve(build_list([1, 2, 3, 4, 5]), 2))


# --- bugs ---
BUGS = [
    {
        "replace": "        prev, cur = group_next, group_prev.next",
        "with":    "        prev, cur = None, group_prev.next",
        "fix": "seed prev with group_next so the reversed group's last node already points to the rest of the list",
        "why": "With prev = None the old group head ends up pointing to None and everything after the first group is lost: [2, 1] for 1..5, k = 2.",
        "decoys": [
            {"line": "        group_next = kth.next", "change": "should be kth.next.next"},
            {"line": "        tail = group_prev.next", "change": "should be tail = kth"},
            {"line": "        kth = group_prev", "change": "should start kth at group_prev.next"},
        ],
    },
    {
        "replace": "        while cur is not group_next:",
        "with":    "        while cur is not kth:",
        "fix": "the reversal must include kth itself; stop when cur reaches the node AFTER the group",
        "why": "Stopping at kth leaves the k-th node un-reversed, so the group is only partly flipped and its links no longer form the right order.",
        "decoys": [
            {"line": "            nxt = cur.next", "change": "should be nxt = cur.next.next"},
            {"line": "        group_prev.next = kth", "change": "should be group_prev.next = prev.next"},
            {"line": "                return dummy.next", "change": "should return head"},
        ],
    },
    {
        "replace": "        group_prev = tail",
        "with":    "        group_prev = kth",
        "fix": "after the flip the old group head is the group's tail; that node is the prev of the next group",
        "why": "kth is now the group's FIRST node, so the next round re-reads the same group from its head and the list is reversed back or loops.",
        "decoys": [
            {"line": "            cur.next = prev", "change": "should be prev.next = cur"},
            {"line": "            prev, cur = cur, nxt", "change": "should be prev, cur = nxt, cur"},
            {"line": "    group_prev = dummy", "change": "should be group_prev = head"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
