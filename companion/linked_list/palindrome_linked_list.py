"""
Palindrome Linked List (LeetCode 234) - Easy
Chapter: linked_list
Pattern: Find middle + reverse second half + interleave

Return True if a singly linked list reads the same forwards and backwards.
Example: 1 -> 2 -> 2 -> 1 -> True; 1 -> 2 -> False
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


# --- brute force ---
def brute_force(head):
    """Copy the values into a Python list and compare with its reverse. O(n) time, O(n) space."""
    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next
    return values == values[::-1]  # values[::-1] is the reversed copy


# --- optimal ---
def palindrome_linked_list(head):
    """Find the middle, reverse the second half in place, compare halves. O(n) time, O(1) space."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:   # 1) slow lands on the middle
        slow = slow.next
        fast = fast.next.next
    prev = None
    cur = slow
    while cur is not None:                              # 2) reverse from the middle onwards
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    first = head
    second = prev
    while second is not None:                           # 3) the reversed half is the shorter one
        if first.val != second.val:
            return False
        first = first.next
        second = second.next
    return True


# --- try the brute force ---
print(brute_force(build_list([1, 2, 2, 1])))      # -> True
print(brute_force(build_list([1, 2])))            # -> False
print(brute_force(build_list([1, 2, 3, 2, 1])))   # -> True
print(brute_force(build_list([1, 2, 3, 3, 1])))   # -> False


# --- try the optimal ---
print(palindrome_linked_list(build_list([1, 2, 2, 1])))      # -> True
print(palindrome_linked_list(build_list([1, 2])))            # -> False
print(palindrome_linked_list(build_list([1, 2, 3, 2, 1])))   # -> True
print(palindrome_linked_list(build_list([1, 2, 3, 3, 1])))   # -> False
