"""
Reverse Nodes in k-Group (LeetCode 25) - Hard
Chapter: linked_list
Pattern: In-place pointer reversal

Reverse the nodes of a linked list k at a time and return the new head; a final group with
fewer than k nodes keeps its order. Only the links may change, not the values.
Example: 1 -> 2 -> 3 -> 4 -> 5 with k = 2 -> [2, 1, 4, 3, 5]; with k = 3 -> [3, 2, 1, 4, 5].
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
def brute_force(head, k):
    """Copy the nodes into an array, reverse each full chunk, relink in array order. O(n) space."""
    nodes = []
    node = head
    while node is not None:
        nodes.append(node)
        node = node.next
    start = 0
    while start + k <= len(nodes):  # a full chunk of k remains
        lo = start
        hi = start + k - 1
        while lo < hi:  # reverse the chunk by swapping from both ends
            nodes[lo], nodes[hi] = nodes[hi], nodes[lo]
            lo += 1
            hi -= 1
        start += k
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if len(nodes) == 0:
        return None
    nodes[-1].next = None
    return nodes[0]


# --- optimal ---
def reverse_k_group(head, k):
    """Look ahead k nodes, reverse that block in place, reattach it. O(n) time, O(1) space."""
    dummy = ListNode(0, head)
    group_prev = dummy  # the node just before the current block
    while True:
        kth = group_prev
        for step in range(k):  # look ahead: is there a full block of k?
            kth = kth.next
            if kth is None:
                return dummy.next  # fewer than k nodes left, leave them as they are
        after = kth.next  # first node after the block
        prev = after  # the reversed block's tail must point to `after`
        cur = group_prev.next
        while cur is not after:  # the usual three-pointer reversal, stopped at the block end
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        old_head = group_prev.next  # the old block head is now the block tail
        group_prev.next = kth
        group_prev = old_head


# --- try the brute force ---
print(list_to_array(brute_force(build_list([1, 2, 3, 4, 5]), 2)))      # -> [2, 1, 4, 3, 5]
print(list_to_array(brute_force(build_list([1, 2, 3, 4, 5]), 3)))      # -> [3, 2, 1, 4, 5]
print(list_to_array(brute_force(build_list([1, 2, 3, 4, 5, 6]), 3)))   # -> [3, 2, 1, 6, 5, 4]
print(list_to_array(brute_force(build_list([1]), 1)))                  # -> [1]


# --- try the optimal ---
print(list_to_array(reverse_k_group(build_list([1, 2, 3, 4, 5]), 2)))      # -> [2, 1, 4, 3, 5]
print(list_to_array(reverse_k_group(build_list([1, 2, 3, 4, 5]), 3)))      # -> [3, 2, 1, 4, 5]
print(list_to_array(reverse_k_group(build_list([1, 2, 3, 4, 5, 6]), 3)))   # -> [3, 2, 1, 6, 5, 4]
print(list_to_array(reverse_k_group(build_list([1]), 1)))                  # -> [1]
