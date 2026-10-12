"""
Middle of the Linked List with Fast and Slow Pointers (basics: linked_lists)
Return the middle node in one pass, without counting; for an even length return the second middle.
  1 -> 2 -> 3 -> 4 -> 5 -> 6  ->  node 4

Idea: fast moves two steps for every one step of slow, so when fast reaches the end
      slow is halfway. On an even length fast ends at None, leaving slow on the right middle.

Pseudocode:
  slow = fast = head
  while fast and fast.next:         # fast can still take two steps
      slow = slow.next
      fast = fast.next.next
  return slow

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


def middle_node(head):
    slow = fast = head
    while fast and fast.next:            # fast can still take two steps
        slow = slow.next                 # 1 step
        fast = fast.next.next            # 2 steps
    return slow                          # right middle on an even length


if __name__ == "__main__":
    print(middle_node(build([1, 2, 3, 4, 5])).val)     # 3
    print(middle_node(build([1, 2, 3, 4, 5, 6])).val)  # 4
    print(middle_node(build([])))                      # None
