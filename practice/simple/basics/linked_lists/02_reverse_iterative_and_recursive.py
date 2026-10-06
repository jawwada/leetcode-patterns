"""
Reverse a Linked List, Iterative and Recursive (basics: linked_lists)
Reverse a singly linked list in place and return the new head.
  1 -> 2 -> 3 -> 4 -> 5  ->  5 -> 4 -> 3 -> 2 -> 1

Idea: iterative: walk once and flip each arrow to point backwards; save next before the flip.
      recursive: reverse everything after head first, then hang head behind its old next node.

Pseudocode:
  reverse_iterative(head):
      prev = None, cur = head
      while cur:
          nxt = cur.next            # save the rest
          cur.next = prev           # flip the arrow
          prev = cur; cur = nxt
      return prev

  reverse_recursive(head):
      if head is None or head.next is None: return head
      new_head = reverse_recursive(head.next)
      head.next.next = head         # old next now points back to head
      head.next = None              # head is the new tail
      return new_head

Time O(n) for both; space O(1) iterative, O(n) call stack recursive.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_iterative(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next                   # save the rest
        cur.next = prev                  # flip the arrow
        prev, cur = cur, nxt             # step forward
    return prev


def reverse_recursive(head):
    if head is None or head.next is None:
        return head                      # 0 or 1 node: already reversed
    new_head = reverse_recursive(head.next)  # reverse the rest first
    head.next.next = head                # old next points back to head
    head.next = None                     # head is the new tail
    return new_head


if __name__ == "__main__":
    print(to_list(reverse_iterative(build([1, 2, 3, 4, 5]))))  # [5, 4, 3, 2, 1]
    print(to_list(reverse_recursive(build([1, 2, 3, 4, 5]))))  # [5, 4, 3, 2, 1]
    print(to_list(reverse_recursive(build([]))))               # []
