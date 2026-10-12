"""
Reverse a Linked List - Three Pointers: prev, curr, next

Given the head of a singly linked list, reverse the list in place and return
the new head. As values: [1, 2, 3, 4, 5] -> [5, 4, 3, 2, 1].
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
    prev = None                     # head of the reversed part
    curr = head                     # head of the part still to reverse
    while curr is not None:
        next_node = curr.next       # save the rest before the cut
        curr.next = prev            # turn this arrow around
        prev = curr                 # the reversed part gains curr
        curr = next_node            # step into the saved rest
    return prev                     # curr ran off the end: prev is the new head


# --- try it ---
head = build_list([1, 2, 3, 4, 5])
print(to_list(reverse_list(head)))                  # -> [5, 4, 3, 2, 1]
print(to_list(reverse_list(build_list([1, 2]))))    # -> [2, 1]
print(to_list(reverse_list(build_list([7]))))       # -> [7]
print(to_list(reverse_list(None)))                  # -> []
