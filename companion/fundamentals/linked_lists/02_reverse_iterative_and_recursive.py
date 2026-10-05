"""
Reverse a Linked List, Iterative and Recursive - Fundamentals
Chapter: fundamentals/linked_lists
Key operations: save next before you cut, point cur back to prev, advance both, hang head behind

Reverse a singly linked list in place and return the new head. The iterative version walks three
pointers (prev, cur, nxt) in O(1) space; the recursive version reverses the rest first, then hooks
the current node behind its old next node.
Example: 1 -> 2 -> 3 -> 4 -> 5 becomes 5 -> 4 -> 3 -> 2 -> 1
"""


# --- helpers ---
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values):
    """Turn a Python list into a linked list and return its head."""
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def list_to_array(head):
    """Turn a linked list back into a Python list."""
    out = []
    node = head
    while node is not None:
        out.append(node.val)
        node = node.next
    return out


# --- algorithm ---
def reverse_iterative(head):
    """Three pointers: save next, point cur back at prev, advance both. O(n) time, O(1) space."""
    prev = None
    cur = head
    while cur is not None:
        nxt = cur.next                      # save the rest BEFORE cutting the link
        cur.next = prev                     # the cut: cur now points backwards
        prev = cur
        cur = nxt
    return prev                             # cur fell off the end: prev is the new head


def reverse_recursive(head):
    """Reverse everything after head, then hang head behind its old next node. O(n), O(n) stack."""
    if head is None or head.next is None:
        return head                         # an empty or single node is its own reverse
    new_head = reverse_recursive(head.next)
    head.next.next = head                   # the old next node is the tail of the reversed rest
    head.next = None                        # head becomes the new tail
    return new_head


# --- try it ---
print(list_to_array(reverse_iterative(build_list([1, 2, 3, 4, 5]))))   # -> [5, 4, 3, 2, 1]
print(list_to_array(reverse_recursive(build_list([1, 2, 3, 4, 5]))))   # -> [5, 4, 3, 2, 1]
print(list_to_array(reverse_iterative(build_list([1, 2]))))            # -> [2, 1]
print(list_to_array(reverse_recursive(build_list([1]))))               # -> [1]
print(list_to_array(reverse_iterative(build_list([]))))                # -> []
