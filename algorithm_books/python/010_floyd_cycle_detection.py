"""
Floyd's Tortoise and Hare - Detect a Cycle and Find Its Entry

Given the head of a linked list whose tail may link back to an earlier node,
return the node where the cycle begins (None if there is no cycle) in O(1)
extra space: values 1..7, tail linked to index 2 -> the node with value 3.
"""


# --- helpers ---
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def build_cycle_list(values, pos):
    """Build a list whose tail links back to index pos (-1: no cycle)."""
    if len(values) == 0:
        return None
    nodes = []
    for value in values:
        nodes.append(ListNode(value))
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]     # close the loop
    return nodes[0]


# --- algorithm ---
def meeting_point(head):
    """Slow steps 1, fast steps 2; they meet only inside a cycle. O(n)."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:            # the same node, not just an equal value
            return slow
    return None                     # fast fell off the end: no cycle


def cycle_entry(head):
    """From head and from the meeting point, 1 step each: they meet at the
    entry. O(n) time, O(1) space."""
    meet = meeting_point(head)
    if meet is None:
        return None
    from_head = head
    from_meet = meet
    while from_head is not from_meet:   # both are a steps from the entry
        from_head = from_head.next
        from_meet = from_meet.next
    return from_head


# --- try it ---
head = build_cycle_list([1, 2, 3, 4, 5, 6, 7], 2)
print(meeting_point(head).val)                          # -> 6
print(cycle_entry(head).val)                            # -> 3
print(cycle_entry(build_cycle_list([3, 2, 0, -4], 1)).val)  # -> 2
print(cycle_entry(build_cycle_list([1, 2, 3], -1)))     # -> None
