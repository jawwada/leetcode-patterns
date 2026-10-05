"""
Reverse Nodes in k-Group (LeetCode 25) - Fundamentals
Chapter: fundamentals/linked_lists
Key operations: probe k ahead, reverse one group with the next group as prev, re-hook, advance

Reverse every k consecutive nodes of a singly linked list; a final group shorter than k is left as
is. Only node links may change, not values. Per group: find its k-th node (stop if missing),
reverse it with prev seeded to the node after it, then hook the node before it to the new head.
Example: 1 -> 2 -> 3 -> 4 -> 5, k = 2 -> 2 -> 1 -> 4 -> 3 -> 5
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
def kth_node(node, k):
    """The node k steps after node, or None if the list ends first."""
    for _ in range(k):
        node = node.next
        if node is None:
            return None
    return node


def reverse_k_group(head, k):
    """Probe k ahead; reverse the group with prev seeded to the next group; re-hook. O(n), O(1)."""
    dummy = ListNode(0, head)
    group_prev = dummy                      # the node just before the current group
    while True:
        kth = kth_node(group_prev, k)
        if kth is None:                     # fewer than k nodes left: leave them as they are
            return dummy.next
        group_next = kth.next
        prev = group_next              # seed prev with the next group: the old head links to it
        cur = group_prev.next
        while cur is not group_next:        # the usual three-pointer reverse, stopped early
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        old_head = group_prev.next
        group_prev.next = kth               # kth is the reversed group's new head
        group_prev = old_head               # the old head is now the group's tail


# --- try it ---
print(list_to_array(reverse_k_group(build_list([1, 2, 3, 4, 5]), 2)))   # -> [2, 1, 4, 3, 5]
print(list_to_array(reverse_k_group(build_list([1, 2, 3, 4, 5]), 3)))   # -> [3, 2, 1, 4, 5]
print(list_to_array(reverse_k_group(build_list([1, 2, 3, 4]), 1)))      # -> [1, 2, 3, 4]
print(list_to_array(reverse_k_group(build_list([1, 2, 3, 4]), 4)))      # -> [4, 3, 2, 1]
print(list_to_array(reverse_k_group(build_list([1, 2]), 3)))            # -> [1, 2]
