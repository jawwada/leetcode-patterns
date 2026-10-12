"""
Remove Nth Node From End of List (LeetCode 19)
Remove the n-th node from the end of a linked list and return the head.
  1->2->3->4->5, n = 2  ->  1->2->3->5

Idea: keep two pointers n + 1 links apart. When fast falls off the end,
      slow sits just before the node to delete. A dummy head lets us delete the head too.

Pseudocode:
  slow = fast = dummy (dummy.next = head)
  move fast n + 1 steps
  while fast: move both 1 step
  slow.next = slow.next.next          # skip the victim
  return dummy.next

Time O(n) one pass, space O(1).
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n + 1):               # open a gap of n + 1
        fast = fast.next
    while fast:                          # slide until fast falls off
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next           # skip the victim
    return dummy.next


if __name__ == "__main__":
    print(to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)))  # [1, 2, 3, 5]
    print(to_list(remove_nth_from_end(build([1]), 1)))              # []
    print(to_list(remove_nth_from_end(build([1, 2]), 2)))           # [2]
