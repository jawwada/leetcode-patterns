"""
Design Skiplist (LeetCode 1206)  — Hard
Pattern: Multi-level sorted linked list with randomised express lanes

Problem
-------
Implement Skiplist with search(target) -> bool, add(num) and erase(num)
-> bool (False if num is absent). Duplicates may be added; erase removes
one copy. All three should run in O(log n) expected time without using
any built-in ordered structure.
Example: add 1, 2, 3; search(0) -> False; add 4; search(1) -> True;
erase(0) -> False; erase(1) -> True; search(1) -> False.

Brute force
-----------
Keep a sorted Python list. search scans (or bisects) for the value, add
scans to the insertion point and inserts, erase scans and deletes.
O(n) per operation, O(n) space. The wasted work is the walk: a sorted
linked list cannot jump, so finding position k costs k pointer steps,
and an array shifts every element after the insertion point on add and
erase.

From brute force to optimal
---------------------------
A sorted linked list is slow only because it cannot skip ahead. Add
"express lanes": every node gets a random height h (h = 1 with
probability 1/2, 2 with 1/4, ...) and participates in the lists of
levels 0..h-1. Level i therefore holds about n / 2^i nodes, and the top
level is a handful of widely spaced sentinels. A search starts at the
top level, moves right while the next value is smaller than the target,
and drops one level when it cannot move; each level costs O(1) expected
steps, so the whole descent is O(log n) expected. The descent also
records, per level, the last node visited (the "update" array); add
splices the new node in after update[i] at every level it occupies, and
erase unlinks it the same way. Randomisation replaces the rebalancing
that a tree needs: no rotations, only pointer splices. Using a seeded
random generator keeps runs reproducible, which matters for testing.

Intuition
---------
Think of a highway with a local road at level 0 and progressively sparser
express roads above it. To reach an exit you drive the fastest road that
does not overshoot, then take the next slower one, until the local road
delivers you to the exact spot. Coin flips decide which exits get which
roads, and on average that gives logarithmic travel.

Geometric view
--------------
Draw the levels as horizontal rows of a staircase diagram: level 0 is
the full sorted chain, each higher row keeps roughly half the nodes,
and a tall node is a column spanning several rows. A search is a path
that steps right along a row, then down a column, then right again,
zigzagging to the bottom-right. update[i] is the node where the path
turned downward on row i; new nodes are spliced in just after those
turning points.

Steps
-----
1. Node(val, height) has forward[0..height-1]; head is a sentinel of
   MAX_LEVEL height; level = current number of non-empty rows.
2. _path(target): from the top row down, move right while
   forward[i].val < target; record update[i] = last node on row i.
3. search: node after update[0] on row 0 equals target?
4. add: h = _random_level(); extend update with head if h > level;
   splice the new node after update[i] on rows 0..h-1.
5. erase: node = update[0].forward[0]; if not target return False;
   unlink it from every row it occupies; shrink level while the top
   row is empty; return True.

Complexity: O(log n) expected per operation, O(n) expected space — each
row is traversed O(1) expected steps and there are O(log n) rows; the
expected total number of pointers is 2n.
Pitfalls: using < vs <= inconsistently so duplicates break erase;
forgetting to extend update[] with head when the new node is taller than
the current level; unlinking a node only on row 0 (dangling pointers on
higher rows); unseeded randomness that makes failures irreproducible.
"""
import random
from typing import List, Optional


class _Node:
    __slots__ = ("val", "forward")

    def __init__(self, val: int, height: int):
        self.val = val
        self.forward: List[Optional["_Node"]] = [None] * height   # forward[i] = next node on row i


class Skiplist:
    MAX_LEVEL = 16                                     # enough for ~65k elements with p = 1/2
    P = 0.5

    def __init__(self):
        self.head = _Node(-1, self.MAX_LEVEL)          # sentinel, smaller than every value
        self.level = 1                                 # number of rows currently in use
        self.rng = random.Random(1206)                 # seeded: reproducible structure

    def _random_level(self) -> int:
        height = 1
        while height < self.MAX_LEVEL and self.rng.random() < self.P:
            height += 1
        return height

    def _path(self, target: int) -> List[_Node]:
        # update[i] = last node on row i whose value is < target (the point where we step down)
        update: List[_Node] = [self.head] * self.MAX_LEVEL
        node = self.head
        for i in range(self.level - 1, -1, -1):
            while node.forward[i] and node.forward[i].val < target:
                node = node.forward[i]
            update[i] = node
        return update

    def search(self, target: int) -> bool:
        node = self._path(target)[0].forward[0]
        return node is not None and node.val == target

    def add(self, num: int) -> None:
        update = self._path(num)
        height = self._random_level()
        self.level = max(self.level, height)           # update[] already holds head for new rows
        node = _Node(num, height)
        for i in range(height):                        # splice in after the turning point on each row
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def erase(self, num: int) -> bool:
        update = self._path(num)
        node = update[0].forward[0]
        if node is None or node.val != num:
            return False
        for i in range(len(node.forward)):             # node is the first >= num, so it follows update[i] on every row
            update[i].forward[i] = node.forward[i]
        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1                            # drop rows that became empty
        return True


class BruteForce:
    """Sorted Python list; every operation scans linearly and shifts elements: O(n)."""

    def __init__(self):
        self.items: List[int] = []

    def search(self, target: int) -> bool:
        return target in self.items

    def add(self, num: int) -> None:
        i = 0
        while i < len(self.items) and self.items[i] < num:   # linear walk to the insertion point
            i += 1
        self.items.insert(i, num)                              # O(n) shift

    def erase(self, num: int) -> bool:
        if num in self.items:
            self.items.remove(num)
            return True
        return False


if __name__ == "__main__":
    sl = Skiplist()
    sl.add(1)
    sl.add(2)
    sl.add(3)
    assert sl.search(0) is False
    sl.add(4)
    assert sl.search(1) is True
    assert sl.erase(0) is False
    assert sl.erase(1) is True
    assert sl.search(1) is False
    sl.add(5)                                  # duplicates: erase removes one copy at a time
    sl.add(5)
    assert sl.erase(5) is True
    assert sl.search(5) is True
    assert sl.erase(5) is True
    assert sl.search(5) is False
    assert sl.erase(5) is False
    assert Skiplist().search(7) is False       # empty list

    rng = random.Random(7)
    fast, slow = Skiplist(), BruteForce()
    for _ in range(3000):
        op, v = rng.random(), rng.randint(0, 40)
        if op < 0.45:
            fast.add(v)
            slow.add(v)
        elif op < 0.75:
            assert fast.erase(v) == slow.erase(v), v
        else:
            assert fast.search(v) == slow.search(v), v
    assert fast.level <= Skiplist.MAX_LEVEL
    print("ok")
