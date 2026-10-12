"""
Reverse Linked List (LeetCode 206)
Reverse a singly linked list and return the new head.
  1 -> 2 -> 3 -> 4 -> 5  ->  5 -> 4 -> 3 -> 2 -> 1

Idea: walk the list once, flipping each node's next pointer to point backwards.
      Save the next node first so the rest of the list isn't lost.

Pseudocode:
  prev = None, cur = head
  while cur:
      nxt = cur.next      # save the rest
      cur.next = prev     # flip the arrow
      prev = cur; cur = nxt
  return prev

Time O(n), space O(1).
"""


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


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


def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next                   # save the rest
        cur.next = prev                  # flip the arrow
        prev, cur = cur, nxt             # step forward
    return prev


if __name__ == "__main__":
    print(to_list(reverse_list(build([1, 2, 3, 4, 5]))))  # [5, 4, 3, 2, 1]
    print(to_list(reverse_list(build([1, 2]))))           # [2, 1]
    print(to_list(reverse_list(build([]))))               # []
