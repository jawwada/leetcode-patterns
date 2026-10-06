"""
Reverse Nodes in k-Group (basics: linked_lists)
Reverse every k consecutive nodes by relinking; a last group shorter than k stays as it is.
  1 -> 2 -> 3 -> 4 -> 5, k = 2  ->  2 -> 1 -> 4 -> 3 -> 5

Idea: one group at a time: check that k nodes exist, then reverse them with prev starting
      at the next group, so the flipped group is already linked to the rest of the list.
      Finally hook the node before the group to the group's new first node.

Pseudocode:
  dummy.next = head; group_prev = dummy
  loop:
      kth = walk k steps from group_prev; if it runs off the end: return dummy.next
      group_next = kth.next
      reverse the nodes group_prev.next .. kth, with prev starting at group_next
      group_tail = group_prev.next        # old first node, now last
      group_prev.next = kth               # kth is now first
      group_prev = group_tail

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


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy                   # node just before the group
    while True:
        kth = group_prev
        for _ in range(k):               # are there k more nodes?
            kth = kth.next
            if kth is None:
                return dummy.next        # short last group stays as is
        group_next = kth.next
        prev, cur = group_next, group_prev.next  # prev starts at the next group
        while cur is not group_next:     # flip the arrows inside the group
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        group_tail = group_prev.next     # old first node, now last
        group_prev.next = kth            # kth is now first
        group_prev = group_tail          # step to the next group


if __name__ == "__main__":
    print(to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 2)))  # [2, 1, 4, 3, 5]
    print(to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 3)))  # [3, 2, 1, 4, 5]
    print(to_list(reverse_k_group(build([1, 2, 3, 4]), 4)))     # [4, 3, 2, 1]
