"""
Middle of the Linked List with Fast and Slow Pointers - Fundamentals
Chapter: fundamentals/linked_lists
Key operations: slow moves one, fast moves two, stop when fast or fast.next is None

Return the middle node of a singly linked list in one pass without counting. For an even length
there are two middles; `while fast and fast.next` stops slow on the second one (the right middle).
Example: 1 -> 2 -> 3 -> 4 -> 5 -> 3;  1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 4
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
def middle_node(head):
    """Slow steps 1, fast steps 2; when fast cannot take two more steps, slow is the middle."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:   # fast needs two more nodes to keep going
        slow = slow.next
        fast = fast.next.next
    return slow


# --- try it ---
print(middle_node(build_list([1, 2, 3, 4, 5])).val)             # -> 3
print(middle_node(build_list([1, 2, 3, 4, 5, 6])).val)          # -> 4
print(list_to_array(middle_node(build_list([1, 2, 3, 4]))))     # -> [3, 4]
print(middle_node(build_list([7])).val)                         # -> 7
print(middle_node(build_list([])))                              # -> None
