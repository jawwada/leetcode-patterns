"""
Merge Two Sorted Lists (LeetCode 21)
Splice two sorted linked lists into one sorted list and return its head.
  1->2->4 and 1->3->4  ->  1->1->2->3->4->4

Idea: both lists are already sorted, so the next node of the answer is always
      the smaller of the two front nodes. A dummy head avoids special-casing the start.

Pseudocode:
  dummy = tail = new node
  while l1 and l2:
      attach the smaller front node to tail, advance that list
      tail = tail.next
  attach whatever is left (l1 or l2)
  return dummy.next

Time O(m + n), space O(1).
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


def merge_two_lists(l1, l2):
    dummy = tail = ListNode()            # dummy sits before the answer
    while l1 and l2:
        if l1.val <= l2.val:             # take the smaller front node
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2                 # leftover is already sorted
    return dummy.next


if __name__ == "__main__":
    print(to_list(merge_two_lists(build([1, 2, 4]), build([1, 3, 4]))))  # [1, 1, 2, 3, 4, 4]
    print(to_list(merge_two_lists(build([]), build([0]))))              # [0]
