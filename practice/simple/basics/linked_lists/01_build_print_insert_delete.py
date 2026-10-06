"""
Build, Print, Insert, Delete (basics: linked_lists)
Build a linked list, print it, insert a value at an index, and delete the first node with a value.
  build [1, 3], insert 2 at index 1, delete 1  ->  [1, 3], [1, 2, 3], [2, 3]

Idea: to relink a spot you need the node just BEFORE it. A dummy node in front of the head
      gives every spot one, so inserting at index 0 and deleting the head are not special cases.

Pseudocode:
  build(values):  head = None; for v in reversed(values): head = new node(v, head)
  to_list(head):  walk from head to the end, collect each val
  insert_at(head, index, val):
      prev = dummy (dummy.next = head); move prev index steps
      prev.next = new node(val, prev.next)                  # splice in
  delete_value(head, val):
      prev = dummy; move prev while prev.next is not None and prev.next.val != val
      if prev.next is not None: prev.next = prev.next.next  # skip over it
  insert_at and delete_value return dummy.next

Time O(n) per operation (the walk; the relink itself is O(1)), space O(1) extra.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def build(values):
    head = None
    for v in reversed(values):           # prepend from the back
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head:                          # walk to the end
        out.append(head.val)
        head = head.next
    return out


def insert_at(head, index, val):
    prev = dummy = ListNode(0, head)     # dummy sits before index 0
    for _ in range(index):               # stop on the node before the slot
        prev = prev.next
    prev.next = ListNode(val, prev.next)  # splice in
    return dummy.next


def delete_value(head, val):
    prev = dummy = ListNode(0, head)
    while prev.next and prev.next.val != val:
        prev = prev.next                 # stop before the first match
    if prev.next:                        # found it (no-op if absent)
        prev.next = prev.next.next       # skip over it
    return dummy.next


if __name__ == "__main__":
    head = build([1, 3])
    print(to_list(head))                 # [1, 3]
    head = insert_at(head, 1, 2)
    print(to_list(head))                 # [1, 2, 3]
    head = delete_value(head, 1)
    print(to_list(head))                 # [2, 3]
