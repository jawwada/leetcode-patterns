"""
Reverse Nodes in k-Group (LeetCode 25)  — Hard
Pattern: In-place pointer reversal

Problem
-------
Reverse the nodes of a linked list k at a time and return the modified list. Nodes left over at
the end (fewer than k) stay in their original order. Only links may change, not values.
Example: 1->2->3->4->5, k = 2 -> 2->1->4->3->5; k = 3 -> 3->2->1->4->5.

Brute force
-----------
Copy the nodes into an array, reverse each full chunk of k entries in place in the array (the
last partial chunk untouched), then relink next pointers in array order. O(n) time, O(n) space.
The wasted work: the array exists only so we can (a) know whether k nodes remain and (b) walk a
chunk backwards — both are achievable on the list itself with a lookahead and a local reversal.

From brute force to optimal
---------------------------
The redundancy is the O(n) buffer. Observation: reversing a k-block in place is the standard
three-pointer reversal, stopped after k flips; the only new requirement is knowing in advance
that k nodes exist (so a short tail is left alone) and re-attaching the reversed block to the
previous block's tail. So keep `group_prev` (the node before the block), look ahead k nodes to
find `kth`; if it is missing, stop. Reverse the block so that the first node becomes the block's
tail and points to the node after the block, then advance group_prev to that new tail.

Intuition
---------
Each block is a mini "reverse linked list" problem. The surrounding glue is: before reversing,
remember who comes after the block (`nxt`), and let the reversal's initial `prev` be `nxt` so the
block's new tail already points forward. After reversal, the old block head is the new tail; hook
the previous block to the new head (kth) and move on.

Geometric view
--------------
    D -> 1 -> 2 -> 3 -> 4 -> 5        k = 2
    gp   ^    kth  nxt
    D -> 2 -> 1 -> 3 -> 4 -> 5        block [1,2] reversed, 1 now points to nxt=3
              gp   ^    kth  nxt
    D -> 2 -> 1 -> 4 -> 3 -> 5        next block done; 5 alone (< k) is left as is

Steps
-----
1. dummy = ListNode(0, head); group_prev = dummy.
2. Loop: kth = group_prev advanced k times; if None, break.
3. nxt = kth.next; reverse nodes from group_prev.next to kth with prev initialised to nxt.
4. tmp = group_prev.next (old block head, now tail); group_prev.next = kth; group_prev = tmp.
5. Return dummy.next.

Complexity: O(n) time, O(1) space — each node is looked at twice (lookahead + reversal).
Pitfalls: reversing a short final block; losing the connection to the next block (initialise prev
to nxt, not None); forgetting to move group_prev to the old head which is now the block tail.
"""
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        group_prev = dummy
        while True:
            kth = group_prev                 # look ahead: is there a full block of k?
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next
            nxt = kth.next                   # first node after the block

            prev, cur = nxt, group_prev.next  # reverse the block; its tail must point to nxt
            while cur is not nxt:
                cur.next, prev, cur = prev, cur, cur.next

            tmp = group_prev.next            # old block head is the new block tail
            group_prev.next = kth
            group_prev = tmp


def brute_force(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    nodes = []
    while head:
        nodes.append(head)
        head = head.next
    for i in range(0, len(nodes) - k + 1, k):
        nodes[i:i + k] = nodes[i:i + k][::-1]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes:
        nodes[-1].next = None
    return nodes[0] if nodes else None


def build(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node: Optional[ListNode]) -> List[int]:
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5, 6], 3, [3, 2, 1, 6, 5, 4]),
        ([1], 1, [1]),
        ([], 2, []),
    ]
    for vals, k, want in cases:
        assert to_list(s.reverseKGroup(build(vals), k)) == want
        assert to_list(brute_force(build(vals), k)) == want
    print("ok")
