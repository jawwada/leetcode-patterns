"""
Linked List Cycle II (LeetCode 142) - Medium
Chapter: linked_list
Pattern: Floyd's tortoise and hare (fast/slow pointers)

Given the head of a linked list, return the node where the cycle begins, or None if there is
no cycle, without modifying the list and ideally in O(1) extra space.
Example: 3 -> 2 -> 0 -> -4 -> (back to 2) -> the node holding 2
"""


# --- helpers ---
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list_with_cycle(values, pos):
    """Build a list whose last node points back to index pos (pos = -1 means no cycle)."""
    nodes = []
    for value in values:
        nodes.append(ListNode(value))
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if len(nodes) > 0 and pos >= 0:
        nodes[-1].next = nodes[pos]
    if len(nodes) == 0:
        return None
    return nodes[0]


def node_value(node):
    """The node's value, or None when there is no node (so a result can be printed)."""
    if node is None:
        return None
    return node.val


# --- brute force ---
def brute_force(head):
    """Remember every node visited; the first repeat starts the cycle. O(n) time, O(n) space."""
    seen = set()
    node = head
    while node is not None:
        if node in seen:
            return node            # the first node reached twice is where the cycle starts
        seen.add(node)
        node = node.next
    return None                    # fell off the end: no cycle


# --- optimal ---
def linked_list_cycle_ii(head):
    """Race slow/fast to meet in the loop, then walk from head and meeting point. O(n), O(1)."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:           # they met: there is a cycle
            break
    if fast is None or fast.next is None:
        return None                # fast fell off the end: no cycle
    pointer = head
    while pointer is not slow:     # head and meeting point are equally far from the entrance
        pointer = pointer.next
        slow = slow.next
    return pointer


# --- try the brute force ---
print(node_value(brute_force(build_list_with_cycle([3, 2, 0, -4], 1))))    # -> 2
print(node_value(brute_force(build_list_with_cycle([1, 2], 0))))           # -> 1
print(node_value(brute_force(build_list_with_cycle([1, 2, 3, 4, 5], 4))))  # -> 5
print(node_value(brute_force(build_list_with_cycle([1, 2, 3], -1))))       # -> None


# --- try the optimal ---
print(node_value(linked_list_cycle_ii(build_list_with_cycle([3, 2, 0, -4], 1))))    # -> 2
print(node_value(linked_list_cycle_ii(build_list_with_cycle([1, 2], 0))))           # -> 1
print(node_value(linked_list_cycle_ii(build_list_with_cycle([1, 2, 3, 4, 5], 4))))  # -> 5
print(node_value(linked_list_cycle_ii(build_list_with_cycle([1, 2, 3], -1))))       # -> None
