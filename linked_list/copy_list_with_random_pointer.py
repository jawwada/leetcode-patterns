"""
Copy List with Random Pointer (LeetCode 138)  — Medium
Pattern: Hash map old-node -> new-node (interleaved-clone variant for O(1) space)

Problem
-------
Each node has `val`, `next`, and `random` (pointing to any node or None). Return a deep copy: new
nodes whose next/random pointers point to NEW nodes with the same structure.
Example: [[7,null],[13,0],[11,4],[10,2],[1,0]] (val, random-index) -> an identical, independent list.

Brute force
-----------
First copy the list by `next` only. Then for every node, find its random target's position by
walking the original list from the head counting steps (O(n)), and walk the copy the same number
of steps to set the clone's random. O(n^2) time, O(1) extra space. The wasted work: recomputing
"which clone corresponds to this original node" by linear search, n times.

From brute force to optimal
---------------------------
The redundancy is the repeated original->clone lookup. Observation: that correspondence is a
function from node to node, so store it once in a hash map {original: clone}. Pass 1 creates a
clone per node and fills the map; pass 2 sets clone.next = map[orig.next] and clone.random =
map[orig.random]. O(n) time, O(n) space. The map can be eliminated entirely by interleaving: put
each clone directly after its original (A -> A' -> B -> B'), so map[X] is literally X.next; set
randoms via orig.next.random = orig.random.next; then unweave the two lists. O(1) extra space.

Intuition
---------
A deep copy needs a way to translate "pointer into the old graph" into "pointer into the new
graph". A dictionary is the obvious translator. The interleaving trick embeds the translator in
the list itself: the clone of X is always X.next.

Geometric view
--------------
    orig:   A ----> B ----> C         (random: A->C, B->A)
    weave:  A -> A' -> B -> B' -> C -> C'
            A'.random = A.random.next = C'
    split:  A -> B -> C        A' -> B' -> C'

Steps
-----
1. Weave: for each original node X, insert clone X' = Node(X.val) between X and X.next.
2. Randoms: for each X, if X.random: X.next.random = X.random.next.
3. Unweave: walk in pairs, restoring X.next = X'.next and setting X'.next = X'.next.next.
4. Return the first clone (head.next from before unweaving).

Complexity: O(n) time, O(1) extra space — three passes, no auxiliary map.
Pitfalls: forgetting None checks on random; corrupting the original list by not restoring its
next pointers (LeetCode checks this); with the map approach, forgetting `map[None] = None`.
"""
from typing import Dict, List, Optional, Tuple


class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if not head:
            return None
        node = head                          # 1) weave clones after originals
        while node:
            clone = Node(node.val, node.next)
            node.next = clone
            node = clone.next

        node = head                          # 2) clone.random = original.random's clone
        while node:
            if node.random:
                node.next.random = node.random.next
            node = node.next.next

        node, new_head = head, head.next     # 3) unweave both lists
        while node:
            clone = node.next
            node.next = clone.next
            if clone.next:
                clone.next = clone.next.next
            node = node.next
        return new_head


def brute_force(head: "Optional[Node]") -> "Optional[Node]":
    def index_of(target: "Optional[Node]") -> int:
        i, n = 0, head
        while n is not target:
            n, i = n.next, i + 1
        return i

    def nth(start: "Optional[Node]", k: int) -> "Optional[Node]":
        for _ in range(k):
            start = start.next
        return start

    dummy = Node(0)
    tail, node = dummy, head
    while node:                              # copy by next only
        tail.next = Node(node.val)
        tail, node = tail.next, node.next
    node, clone = head, dummy.next
    while node:                              # locate each random by position, O(n) each
        if node.random:
            clone.random = nth(dummy.next, index_of(node.random))
        node, clone = node.next, clone.next
    return dummy.next


def build(pairs: List[Tuple[int, Optional[int]]]) -> Optional[Node]:
    nodes = [Node(v) for v, _ in pairs]
    for i, (_, r) in enumerate(pairs):
        nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
        nodes[i].random = nodes[r] if r is not None else None
    return nodes[0] if nodes else None


def to_list(head: Optional[Node]) -> List[Tuple[int, Optional[int]]]:
    idx: Dict[int, int] = {}
    node, i = head, 0
    while node:
        idx[id(node)] = i
        node, i = node.next, i + 1
    out, node = [], head
    while node:
        out.append((node.val, idx[id(node.random)] if node.random else None))
        node = node.next
    return out


def shares_nodes(a: Optional[Node], b: Optional[Node]) -> bool:
    ids = set()
    while a:
        ids.add(id(a))
        a = a.next
    while b:
        if id(b) in ids:
            return True
        b = b.next
    return False


if __name__ == "__main__":
    s = Solution()
    cases = [
        [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)],
        [(1, 1), (2, 1)],
        [(3, None), (3, 0), (3, None)],
        [],
    ]
    for pairs in cases:
        orig = build(pairs)
        copy = s.copyRandomList(orig)
        assert to_list(copy) == pairs
        assert to_list(orig) == pairs          # original left intact
        assert not shares_nodes(orig, copy)    # deep copy: no shared nodes
        assert to_list(brute_force(build(pairs))) == pairs
    print("ok")
