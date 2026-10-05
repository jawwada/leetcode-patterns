"""
Remove Nth Node From End of List (LeetCode 19) - Medium
Chapter: linked_list
Pattern: Two pointers with fixed gap

Remove the n-th node from the end of a singly linked list and return the head; n is always
valid (1 <= n <= length).
Example: 1 -> 2 -> 3 -> 4 -> 5 with n = 2 -> [1, 2, 3, 5]
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
def brute_force(head, n):
    """Count the length, then walk to the node before the victim. O(L) time, two passes."""
    length = 0
    node = head
    while node is not None:
        length += 1
        node = node.next
    dummy = ListNode(0, head)      # lets us remove the first node like any other
    prev = dummy
    for _ in range(length - n):    # prev stops just before the node to remove
        prev = prev.next
    prev.next = prev.next.next     # skip over the victim
    return dummy.next


# --- optimal ---
def remove_nth_from_end(head, n):
    """Two pointers n + 1 apart: when the front falls off, the back is before the victim. O(L)."""
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy
    for _ in range(n + 1):         # open a gap of n + 1 links
        fast = fast.next
    while fast is not None:        # slide both until fast falls off the end
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next     # slow is just before the n-th node from the end
    return dummy.next


# --- try the brute force ---
print(list_to_array(brute_force(build_list([1, 2, 3, 4, 5]), 2)))   # -> [1, 2, 3, 5]
print(list_to_array(brute_force(build_list([1]), 1)))               # -> []
print(list_to_array(brute_force(build_list([1, 2]), 1)))            # -> [1]
print(list_to_array(brute_force(build_list([1, 2]), 2)))            # -> [2]


# --- try the optimal ---
print(list_to_array(remove_nth_from_end(build_list([1, 2, 3, 4, 5]), 2)))   # -> [1, 2, 3, 5]
print(list_to_array(remove_nth_from_end(build_list([1]), 1)))               # -> []
print(list_to_array(remove_nth_from_end(build_list([1, 2]), 1)))            # -> [1]
print(list_to_array(remove_nth_from_end(build_list([1, 2]), 2)))            # -> [2]
