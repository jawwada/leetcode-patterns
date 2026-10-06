"""
Linked List Cycle II (LeetCode 142)
Return the node where the cycle begins, or None if there is no cycle.
  3->2->0->-4 -> back to 2  ->  node 2

Idea: slow (1 step) and fast (2 steps) must meet inside the loop if there is one.
      Then a pointer from the head and one from the meeting point, both 1 step,
      meet exactly at the cycle entry (the distances work out equal).

Pseudocode:
  slow = fast = head
  while fast and fast.next:
      slow 1 step, fast 2 steps
      if slow is fast: break           # met inside the loop
  else: return None                    # fast fell off: no cycle
  ptr = head
  while ptr is not slow: move both 1 step
  return ptr

Time O(n), space O(1).
"""


class ListNode:
    def __init__(self, val):
        self.val, self.next = val, None


def build(values, pos):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos >= 0:
        nodes[-1].next = nodes[pos]      # tail links back to index pos
    return nodes[0]


def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                 # met inside the loop
            break
    else:
        return None                      # no cycle
    ptr = head
    while ptr is not slow:               # both 1 step until they meet
        ptr, slow = ptr.next, slow.next
    return ptr                           # cycle entry


if __name__ == "__main__":
    print(detect_cycle(build([3, 2, 0, -4], 1)).val)  # 2
    print(detect_cycle(build([1, 2], 0)).val)         # 1
    print(detect_cycle(build([1], -1)))               # None
