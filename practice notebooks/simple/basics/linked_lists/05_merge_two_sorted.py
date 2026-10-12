"""
Merge Two Sorted Lists (basics: linked_lists)
Merge two sorted linked lists into one sorted list by relinking the existing nodes.
  1 -> 2 -> 4 and 1 -> 3 -> 4  ->  1 -> 1 -> 2 -> 3 -> 4 -> 4

Idea: both lists are sorted, so the next node of the answer is always the smaller front node.
      A dummy head gives the answer something to hang from; tail marks its last node.

Pseudocode:
  dummy = tail = new node
  while a and b:
      attach the smaller front node to tail (a wins ties), advance that list
      tail = tail.next
  tail.next = a or b              # attach the leftover whole
  return dummy.next

Time O(n + m), space O(1).
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


def merge_two_sorted(a, b):
    dummy = tail = ListNode()            # dummy sits before the answer
    while a and b:
        if a.val <= b.val:               # take the smaller front node
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next                 # tail stays on the last node
    tail.next = a or b                   # leftover is already sorted
    return dummy.next


if __name__ == "__main__":
    print(to_list(merge_two_sorted(build([1, 2, 4]), build([1, 3, 4]))))  # [1, 1, 2, 3, 4, 4]
    print(to_list(merge_two_sorted(build([5]), build([1, 2, 3]))))        # [1, 2, 3, 5]
    print(to_list(merge_two_sorted(build([]), build([0]))))               # [0]
