"""
Reverse Linked List (LeetCode 206) - Easy
Chapter: linked_list
Pattern: In-place pointer reversal

Given the head of a singly linked list, reverse it and return the new head.
Example: 1 -> 2 -> 3 -> 4 -> 5 -> [5, 4, 3, 2, 1]
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


# --- brute force ---
def brute_force(head):
    """Copy the values out, reverse them, build a brand-new list. O(n) time, O(n) space."""
    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next
    values = values[::-1]          # reversed copy of the list
    return build_list(values)      # allocates n new nodes


# --- optimal ---
def reverse_linked_list(head):
    """Flip one next pointer at a time with three pointers. O(n) time, O(1) space."""
    prev = None
    cur = head
    while cur is not None:
        nxt = cur.next             # save the rest of the list before breaking the link
        cur.next = prev            # flip the arrow to point backwards
        prev = cur
        cur = nxt
    return prev                    # cur ran off the end, so prev is the new head


# --- try the brute force ---
print(list_to_array(brute_force(build_list([1, 2, 3, 4, 5]))))   # -> [5, 4, 3, 2, 1]
print(list_to_array(brute_force(build_list([1, 2]))))            # -> [2, 1]
print(list_to_array(brute_force(build_list([7]))))               # -> [7]
print(list_to_array(brute_force(build_list([]))))                # -> []


# --- try the optimal ---
print(list_to_array(reverse_linked_list(build_list([1, 2, 3, 4, 5]))))   # -> [5, 4, 3, 2, 1]
print(list_to_array(reverse_linked_list(build_list([1, 2]))))            # -> [2, 1]
print(list_to_array(reverse_linked_list(build_list([7]))))               # -> [7]
print(list_to_array(reverse_linked_list(build_list([]))))                # -> []
