"""
Intersection of Two Linked Lists (LeetCode 160) - Easy
Chapter: linked_list
Pattern: Length alignment, then lockstep walk

Given the heads of two singly linked lists that may merge into a shared tail, return the first
node they have in common (the same node object, not just an equal value), or None. The lists
have no cycles and must not be modified.
Example: A = 4 -> 1 -> 8 -> 4 -> 5 and B = 5 -> 6 -> 1 -> 8 -> 4 -> 5 sharing 8 -> 4 -> 5 -> node 8
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


def join(head, tail):
    """Attach tail after the last node of head (head may be empty)."""
    if head is None:
        return tail
    node = head
    while node.next is not None:
        node = node.next
    node.next = tail
    return head


def build_two_lists(prefix_a, prefix_b, tail):
    """Two lists that end in the very same tail nodes: prefix_a + tail and prefix_b + tail."""
    shared = build_list(tail)
    head_a = join(build_list(prefix_a), shared)
    head_b = join(build_list(prefix_b), shared)
    return head_a, head_b


def node_value(node):
    """The node's value, or None when there is no node (so a result can be printed)."""
    if node is None:
        return None
    return node.val


# --- brute force ---
def brute_force(head_a, head_b):
    """For every node of A, scan all of B for that same node. O(m * n) time, O(1) space."""
    a = head_a
    while a is not None:
        b = head_b
        while b is not None:
            if a is b:             # the same node object, not just the same value
                return a
            b = b.next
        a = a.next
    return None


# --- optimal ---
def list_length(head):
    """Number of nodes in the list."""
    count = 0
    node = head
    while node is not None:
        count += 1
        node = node.next
    return count


def intersection_of_two_linked_lists(head_a, head_b):
    """Skip the longer list's extra prefix, then walk both in lockstep. O(m + n) time, O(1)."""
    len_a = list_length(head_a)
    len_b = list_length(head_b)
    a = head_a
    b = head_b
    for _ in range(len_a - len_b):     # only runs when A is longer
        a = a.next
    for _ in range(len_b - len_a):     # only runs when B is longer
        b = b.next
    while a is not b:                  # both are now the same distance from the end
        a = a.next
        b = b.next
    return a                           # the shared node, or None if they never meet


# --- try the brute force ---
head_a, head_b = build_two_lists([4, 1], [5, 6, 1], [8, 4, 5])
print(node_value(brute_force(head_a, head_b)))   # -> 8
head_a, head_b = build_two_lists([1, 9, 1], [3], [2, 4])
print(node_value(brute_force(head_a, head_b)))   # -> 2
head_a, head_b = build_two_lists([2, 6, 4], [1, 5], [])
print(node_value(brute_force(head_a, head_b)))   # -> None
head_a, head_b = build_two_lists([], [7, 7], [3])
print(node_value(brute_force(head_a, head_b)))   # -> 3


# --- try the optimal ---
head_a, head_b = build_two_lists([4, 1], [5, 6, 1], [8, 4, 5])
print(node_value(intersection_of_two_linked_lists(head_a, head_b)))   # -> 8
head_a, head_b = build_two_lists([1, 9, 1], [3], [2, 4])
print(node_value(intersection_of_two_linked_lists(head_a, head_b)))   # -> 2
head_a, head_b = build_two_lists([2, 6, 4], [1, 5], [])
print(node_value(intersection_of_two_linked_lists(head_a, head_b)))   # -> None
head_a, head_b = build_two_lists([], [7, 7], [3])
print(node_value(intersection_of_two_linked_lists(head_a, head_b)))   # -> 3
