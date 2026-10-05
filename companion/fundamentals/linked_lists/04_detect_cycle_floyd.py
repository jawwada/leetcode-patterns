"""
Detect a Cycle with Floyd's Tortoise and Hare - Fundamentals
Chapter: fundamentals/linked_lists
Key operations: slow and fast meet inside the cycle, reset one pointer to head, step both by one

Given a list whose tail may point back to an earlier node, tell whether there is a cycle and return
the index of the node where it begins (-1 if none), in O(1) space. build_list(values, pos) links
the last node to the node at index pos (pos = -1 means no cycle).
Example: values [3, 2, 0, -4], pos 1 -> 1   (the tail -4 points back to 2)
"""


# --- helpers ---
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values, pos=-1):
    """Linked list from a Python list; the last node links back to index pos (-1: no cycle)."""
    nodes = []
    for value in values:
        nodes.append(ListNode(value))
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if len(nodes) > 0 and pos >= 0:
        nodes[-1].next = nodes[pos]          # close the cycle
    if len(nodes) == 0:
        return None
    return nodes[0]


def list_to_array(head):
    """Values in order, stopping at the first node seen twice so a cycle is printed once."""
    out = []
    seen = set()
    node = head
    while node is not None and node not in seen:
        seen.add(node)
        out.append(node.val)
        node = node.next
    return out


# --- algorithm ---
def meeting_point(head):
    """Slow steps 1, fast steps 2: they meet inside a cycle, or fast runs off the end. O(n)."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                    # compare the nodes with 'is': values may repeat
            return slow
    return None                             # fast reached the end: no cycle


def has_cycle(head):
    """A cycle exists exactly when the two pointers meet."""
    return meeting_point(head) is not None


def cycle_start_index(head):
    """From head and from the meeting point, step both by one; they meet at the cycle entry."""
    meet = meeting_point(head)
    if meet is None:
        return -1
    pointer = head                          # restart one pointer at the head, keep the other
    index = 0
    while pointer is not meet:
        pointer = pointer.next
        meet = meet.next
        index += 1
    return index


# --- try it ---
print(list_to_array(build_list([3, 2, 0, -4], 1)))     # -> [3, 2, 0, -4]
print(has_cycle(build_list([3, 2, 0, -4], 1)))         # -> True
print(cycle_start_index(build_list([3, 2, 0, -4], 1))) # -> 1
print(cycle_start_index(build_list([1, 2], 0)))        # -> 0
print(has_cycle(build_list([1, 2, 3])))                # -> False
print(cycle_start_index(build_list([1, 2, 3])))        # -> -1
print(cycle_start_index(build_list([])))               # -> -1
