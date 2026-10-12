"""
Palindrome Linked List (basics: linked_lists)
Return True if a linked list reads the same forwards and backwards, using O(1) extra space.
  1 -> 2 -> 2 -> 1  ->  True

Idea: find the middle with fast/slow pointers and reverse the second half in place.
      Then walk the front half and the reversed back half together, comparing values.

Pseudocode:
  slow = fast = head
  while fast and fast.next: slow 1 step, fast 2 steps    # slow ends at the middle
  reverse the list from slow on; right = its new head
  left = head
  while right:
      if left.val != right.val: return False
      move left and right 1 step
  return True

Time O(n), space O(1).
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def is_palindrome(head):
    slow = fast = head
    while fast and fast.next:            # find the middle
        slow, fast = slow.next, fast.next.next
    prev, cur = None, slow
    while cur:                           # reverse the second half
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    left, right = head, prev             # front half, reversed back half
    while right:
        if left.val != right.val:        # mismatch: not a palindrome
            return False
        left, right = left.next, right.next
    return True


if __name__ == "__main__":
    print(is_palindrome(build([1, 2, 2, 1])))     # True
    print(is_palindrome(build([1, 2, 3, 2, 1])))  # True
    print(is_palindrome(build([1, 2, 3])))        # False
