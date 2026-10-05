"""
Merge Two Sorted Lists (LeetCode 21) - Easy
Chapter: linked_list
Pattern: Dummy head + two-pointer merge

Merge two sorted linked lists into one sorted list by splicing their nodes together, and
return the head of the merged list.
Example: 1 -> 2 -> 4 and 1 -> 3 -> 4 -> [1, 1, 2, 3, 4, 4]
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
def brute_force(list1, list2):
    """Collect every value, sort, build a new list. O((m+n) log(m+n)) time, O(m+n) space."""
    values = []
    node = list1
    while node is not None:
        values.append(node.val)
        node = node.next
    node = list2
    while node is not None:
        values.append(node.val)
        node = node.next
    values.sort()                  # re-sorts data that was already sorted
    return build_list(values)


# --- optimal ---
def merge_two_sorted_lists(list1, list2):
    """Repeatedly take the smaller front node and splice it on. O(m+n) time, O(1) extra."""
    dummy = ListNode()             # placeholder in front of the result
    tail = dummy
    while list1 is not None and list2 is not None:
        if list1.val <= list2.val:
            tail.next = list1      # hook the smaller front node onto the result
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    if list1 is not None:          # one list ran out: attach the rest of the other whole
        tail.next = list1
    else:
        tail.next = list2
    return dummy.next


# --- try the brute force ---
a = build_list([1, 2, 4])
b = build_list([1, 3, 4])
print(list_to_array(brute_force(a, b)))                       # -> [1, 1, 2, 3, 4, 4]
a = build_list([5])
b = build_list([1, 2, 3])
print(list_to_array(brute_force(a, b)))                       # -> [1, 2, 3, 5]
print(list_to_array(brute_force(build_list([]), build_list([0]))))   # -> [0]
print(list_to_array(brute_force(build_list([]), build_list([]))))    # -> []


# --- try the optimal ---
a = build_list([1, 2, 4])
b = build_list([1, 3, 4])
print(list_to_array(merge_two_sorted_lists(a, b)))                       # -> [1, 1, 2, 3, 4, 4]
a = build_list([5])
b = build_list([1, 2, 3])
print(list_to_array(merge_two_sorted_lists(a, b)))                       # -> [1, 2, 3, 5]
print(list_to_array(merge_two_sorted_lists(build_list([]), build_list([0]))))   # -> [0]
print(list_to_array(merge_two_sorted_lists(build_list([]), build_list([]))))    # -> []
