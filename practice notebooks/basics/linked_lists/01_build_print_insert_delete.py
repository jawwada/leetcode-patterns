"""
Build, Print, Insert, Delete - Basics
Area: linked lists
Key operations: walk index steps from a dummy head, splice a node in, unlink the first node with a value

Start from an empty list and apply ops: ("insert", index, val) puts val at position index
(0 <= index <= length), ("delete", val) removes the first node holding val (no-op if absent).
Return the list after every op.
Example: [("insert", 0, 1), ("insert", 1, 3), ("insert", 1, 2), ("delete", 3), ("delete", 9)]
      -> [[1], [1, 3], [1, 2, 3], [1, 2], [1, 2]]
"""
from typing import List, Optional, Tuple


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

def draw(head): return " -> ".join(map(str, to_list(head))) or "empty"


# --- brute force ---
def brute_force(ops: List[Tuple]) -> List[List[int]]:
    """Do the same ops on a Python list; insert/remove shift elements, O(n) each."""
    lst, snapshots = [], []
    for op in ops:
        if op[0] == "insert":
            lst.insert(op[1], op[2])
        elif op[1] in lst:
            lst.remove(op[1])
        snapshots.append(list(lst))
    return snapshots


# --- optimal ---
def insert_at(head: Optional[ListNode], index: int, val: int) -> Optional[ListNode]:
    """Walk index steps from a dummy so prev is the node before the slot; splice after it. O(index)."""
    prev = dummy = ListNode(0, head)
    for _ in range(index):
        prev = prev.next
    prev.next = ListNode(val, prev.next)
    return dummy.next

def delete_val(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """Walk prev from a dummy until prev.next holds val; unlink it by skipping over it. O(n)."""
    prev = dummy = ListNode(0, head)
    while prev.next and prev.next.val != val:
        prev = prev.next
    if prev.next:
        prev.next = prev.next.next
    return dummy.next

def solve(ops: List[Tuple]) -> List[List[int]]:
    """Apply the ops on nodes; a dummy head makes index 0 and the head deletion ordinary cases."""
    head, snapshots = None, []
    for op in ops:
        if op[0] == "insert":
            head = insert_at(head, op[1], op[2])
        else:
            head = delete_val(head, op[1])
        snapshots.append(to_list(head))
    return snapshots


# --- demo ---
def demo():
    return solve([("insert", 0, 1), ("insert", 1, 3), ("insert", 1, 2), ("delete", 3), ("delete", 9)])


# --- bugs ---
BUGS = [
    {
        "replace": "    for _ in range(index):",
        "with":    "    for _ in range(index + 1):",
        "fix": "walk exactly index steps from the dummy; the dummy already counts as the node before index 0",
        "why": "One extra step lands prev on the node AT index, so the value goes one slot too far, and inserting at the end dereferences None.",
        "decoys": [
            {"line": "    prev.next = ListNode(val, prev.next)", "change": "should be ListNode(val, prev)"},
            {"line": "        prev.next = prev.next.next", "change": "should be prev = prev.next.next"},
            {"line": "        snapshots.append(to_list(head))", "change": "should append head"},
        ],
    },
    {
        "replace": "    while prev.next and prev.next.val != val:",
        "with":    "    while prev and prev.next.val != val:",
        "fix": "guard on prev.next, the node being inspected, not on prev",
        "why": "When val is absent prev reaches the last node, prev.next is None and .val raises; the no-op delete must stop one node earlier.",
        "decoys": [
            {"line": "    if prev.next:", "change": "should be if prev.next.val == val:"},
            {"line": "    head, snapshots = None, []", "change": "should start head at ListNode()"},
            {"line": "            head = delete_val(head, op[1])", "change": "should pass op[2]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
