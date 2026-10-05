"""
Add Two Numbers (LeetCode 2) - Medium
Chapter: linked_list
Pattern: Dummy head + carry

Two non-empty linked lists store non-negative integers with their digits in reverse order
(342 is stored as 2 -> 4 -> 3). Return the sum as a linked list in the same format.
Example: (2 -> 4 -> 3) + (5 -> 6 -> 4) -> [7, 0, 8], since 342 + 465 = 807
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
def list_to_int(head):
    """Read the whole number out of a list that stores the ones digit first."""
    number = 0
    place = 1                      # 1, 10, 100, ...
    node = head
    while node is not None:
        number += node.val * place
        place *= 10
        node = node.next
    return number


def brute_force(l1, l2):
    """Turn both lists into integers, add, split the sum back into digits. O(m+n) time."""
    total = list_to_int(l1) + list_to_int(l2)
    digits = []
    while total >= 10:
        digits.append(total % 10)  # peel off the ones digit
        total = total // 10
    digits.append(total)
    return build_list(digits)


# --- optimal ---
def add_two_numbers(l1, l2):
    """Schoolbook addition while walking both lists with a carry. O(max(m, n)) time, O(1)."""
    dummy = ListNode()
    tail = dummy
    carry = 0
    while l1 is not None or l2 is not None or carry != 0:   # a final carry adds a digit
        total = carry
        if l1 is not None:
            total += l1.val
            l1 = l1.next
        if l2 is not None:
            total += l2.val
            l2 = l2.next
        carry = total // 10        # 0 or 1
        digit = total % 10
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next


# --- try the brute force ---
a = build_list([2, 4, 3])
b = build_list([5, 6, 4])
print(list_to_array(brute_force(a, b)))                                 # -> [7, 0, 8]
print(list_to_array(brute_force(build_list([0]), build_list([0]))))     # -> [0]
print(list_to_array(brute_force(build_list([9, 9, 9]), build_list([1]))))   # -> [0, 0, 0, 1]


# --- try the optimal ---
a = build_list([2, 4, 3])
b = build_list([5, 6, 4])
print(list_to_array(add_two_numbers(a, b)))                                 # -> [7, 0, 8]
print(list_to_array(add_two_numbers(build_list([0]), build_list([0]))))     # -> [0]
print(list_to_array(add_two_numbers(build_list([9, 9, 9]), build_list([1]))))   # -> [0, 0, 0, 1]
