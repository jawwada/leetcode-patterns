"""
Build, Print, Insert, Delete - Fundamentals
Chapter: fundamentals/linked_lists
Key operations: walk index steps from a dummy, splice a node in, unlink the first node with val

Build a singly linked list from a Python list, print it back, insert a value at a position
(0 <= index <= length) and delete the first node holding a value (no-op if absent). A dummy node in
front of the head makes "insert at 0" and "delete the head" ordinary cases.
Example: insert 1 at 0, 3 at 1, 2 at 1; delete 3; delete 9 ->
[1], [1, 3], [1, 2, 3], [1, 2], [1, 2]
"""


# --- helpers ---
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# --- algorithm ---
def build_list(values):
    """Append each value after a moving tail; the dummy's next is the head. O(n)."""
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next                    # the tail always points at the last node
    return dummy.next


def list_to_array(head):
    """Walk node to node until None, collecting the values. O(n)."""
    out = []
    node = head
    while node is not None:
        out.append(node.val)
        node = node.next
    return out


def insert_at(head, index, val):
    """Walk index steps from a dummy so prev is the node before the slot, then splice in. O(i)."""
    dummy = ListNode(0, head)               # the dummy makes index 0 an ordinary case
    prev = dummy
    for _ in range(index):
        prev = prev.next
    prev.next = ListNode(val, prev.next)    # the new node takes over prev's old next
    return dummy.next


def delete_value(head, val):
    """Walk prev until prev.next holds val, then skip over that node. O(n); no-op if absent."""
    dummy = ListNode(0, head)               # the dummy makes deleting the head an ordinary case
    prev = dummy
    while prev.next is not None and prev.next.val != val:
        prev = prev.next
    if prev.next is not None:
        prev.next = prev.next.next          # unlink by skipping over the node
    return dummy.next


# --- try it ---
head = insert_at(None, 0, 1)
print(list_to_array(head))                                 # -> [1]
head = insert_at(head, 1, 3)
print(list_to_array(head))                                 # -> [1, 3]
head = insert_at(head, 1, 2)
print(list_to_array(head))                                 # -> [1, 2, 3]
head = delete_value(head, 3)
print(list_to_array(head))                                 # -> [1, 2]
head = delete_value(head, 9)
print(list_to_array(head))                                 # -> [1, 2]
print(list_to_array(build_list([4, 5, 6])))                # -> [4, 5, 6]
print(list_to_array(delete_value(build_list([7, 8]), 7)))  # -> [8]
print(list_to_array(insert_at(build_list([7, 8]), 2, 9)))  # -> [7, 8, 9]
