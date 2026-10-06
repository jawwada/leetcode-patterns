"""
Detect a Cycle with Floyd's Tortoise and Hare (basics: linked_lists)
Return the index of the node where the cycle begins, or -1 if there is no cycle, in O(1) space.
  [3, 2, 0, -4], tail links back to index 1  ->  1

Idea: inside a loop fast (2 steps) gains one node per round on slow (1 step), so they meet.
      Then a pointer restarted at head and slow, both moving 1 step, meet exactly at the entry
      (head -> entry is as long as meeting point -> entry, plus some whole loops).

Pseudocode:
  slow = fast = head
  while fast and fast.next:
      slow 1 step, fast 2 steps
      if slow is fast: break              # met inside the loop
  else: return -1                         # fast fell off the end: no cycle
  ptr = head, index = 0
  while ptr is not slow: move ptr and slow 1 step, index += 1
  return index

Time O(n), space O(1).
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def build(values, pos):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]      # tail links back to index pos
    return nodes[0] if nodes else None


def cycle_start_index(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                 # met inside the loop
            break
    else:
        return -1                        # fast fell off: no cycle
    ptr, index = head, 0
    while ptr is not slow:               # both 1 step until they meet
        ptr, slow = ptr.next, slow.next
        index += 1
    return index                         # they meet at the entry


if __name__ == "__main__":
    print(cycle_start_index(build([3, 2, 0, -4], 1)))  # 1
    print(cycle_start_index(build([1, 2], 0)))         # 0
    print(cycle_start_index(build([1, 2, 3], -1)))     # -1
