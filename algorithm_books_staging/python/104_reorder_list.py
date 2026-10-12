"""
Reorder List - Find the Middle, Reverse, Weave

Reorder a singly linked list L0 L1 ... Ln in place into L0 Ln L1 Ln-1 L2 ...,
relinking the nodes rather than copying values. As values:
[1, 2, 3, 4, 5] -> [1, 5, 2, 4, 3].
"""


# --- helpers ---
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def build_list(values):
    """Build a linked list from a Python list and return its head."""
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def to_list(head):
    """Read a linked list back into a Python list."""
    values = []
    while head is not None:
        values.append(head.val)
        head = head.next
    return values


# --- algorithm ---
def reverse_list(head):
    """Turn every next arrow around in one walk. O(n) time, O(1) space."""
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next       # save the rest before the cut
        curr.next = prev
        prev = curr
        curr = next_node
    return prev


def reorder_list(head):
    """Find the middle, reverse the second half, weave the two halves.
    O(n) time, O(1) space."""
    if head is None:
        return
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next            # ends on the first half's last node
        fast = fast.next.next
    second = slow.next
    slow.next = None                # cut after the first half
    second = reverse_list(second)
    first = head
    while second is not None:       # the second half is never longer
        next_first = first.next     # save both rests before relinking
        next_second = second.next
        first.next = second
        second.next = next_first
        first = next_first
        second = next_second


# --- try it ---
head = build_list([1, 2, 3, 4, 5])
reorder_list(head)
print(to_list(head))                    # -> [1, 5, 2, 4, 3]
head = build_list([1, 2, 3, 4])
reorder_list(head)
print(to_list(head))                    # -> [1, 4, 2, 3]
head = build_list([7])
reorder_list(head)
print(to_list(head))                    # -> [7]
