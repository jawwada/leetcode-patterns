"""
Add Two Numbers (basics: linked_lists)
Two numbers are stored as digit lists, ones digit first; return their sum stored the same way.
  2 -> 4 -> 3 (342) + 5 -> 6 -> 4 (465)  ->  7 -> 0 -> 8 (807)

Idea: schoolbook addition, and the lists already start at the ones column. Walk both lists
      together, write total % 10 and carry total // 10; keep going while a carry is left.

Pseudocode:
  dummy = tail = new node; carry = 0
  while l1 or l2 or carry:
      total = carry + (l1.val if l1 exists) + (l2.val if l2 exists); advance those lists
      carry, digit = divmod(total, 10)
      tail.next = new node(digit); tail = tail.next
  return dummy.next

Time O(max(n, m)), space O(1) extra besides the output list.
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


def add_two_numbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:             # a last carry makes a new digit
        total = carry
        if l1:                           # lists may have different lengths
            total += l1.val
            l1 = l1.next
        if l2:
            total += l2.val
            l2 = l2.next
        carry, digit = divmod(total, 10)  # 12 -> carry 1, digit 2
        tail.next = ListNode(digit)      # append the digit
        tail = tail.next
    return dummy.next


if __name__ == "__main__":
    print(to_list(add_two_numbers(build([2, 4, 3]), build([5, 6, 4]))))  # [7, 0, 8]
    print(to_list(add_two_numbers(build([9, 9]), build([1]))))           # [0, 0, 1]
    print(to_list(add_two_numbers(build([0]), build([0]))))              # [0]
