"""
Range Module (LeetCode 715)  — Hard
Pattern: Sorted disjoint intervals with bisect

Problem
-------
Track half-open ranges [left, right) of real numbers. addRange(l, r) marks the range as tracked,
removeRange(l, r) untracks it, queryRange(l, r) returns True iff every point of [l, r) is
currently tracked. All three operations interleave arbitrarily.
Example: addRange(10,20); removeRange(14,16); queryRange(10,14) -> True;
queryRange(13,15) -> False; queryRange(16,17) -> True.

Brute force
-----------
Keep every tracked integer point in a set (or a boolean array over the coordinate range).
addRange inserts r - l points, removeRange deletes them, queryRange checks them one by one.
O(r - l) per operation and O(coordinate range) space; with coordinates up to 1e9 both blow up.
The wasted work: a tracked region is a handful of contiguous blocks, but we touch every single
point inside a block instead of its two boundaries.

From brute force to optimal
---------------------------
The redundancy is representing a contiguous block point by point. Observation: the tracked set is
always a union of DISJOINT intervals, so it is fully described by its sorted boundaries
[l0, r0, l1, r1, ...]. Store exactly that flat sorted list. Then the parity of an index tells
you what the number line looks like there: a boundary at an even index opens a tracked block, an
odd index closes one, and a point x whose bisect position is odd lies inside a block. Adding
[l, r) becomes: find the slice of boundaries inside [l, r] with two bisects, delete them, and
re-insert l only if l was in a gap (even position) and r only if r was in a gap. removeRange is
the mirror image (re-insert when the position is odd). queryRange is "both ends fall inside the
same block": bisect_right(l) == bisect_left(r) and that index is odd. Each operation is two
binary searches plus one list splice, O(log n + n) worst case but O(log n) for the searches.

Intuition
---------
A union of disjoint intervals on a line is nothing but an alternating sequence of
open/close boundaries. Adding or removing a range can only destroy the boundaries strictly inside
it and create at most two new ones at its ends. Parity of the insertion position tells you whether
each end sits in tracked or untracked territory, which decides whether that end becomes a new
boundary.

Geometric view
--------------
Picture the number line with the tracked blocks as solid segments. addRange(l, r) lays a new
solid segment on top: everything under it merges into one block, so all interior boundaries
vanish. The new block starts at l if l was in a gap, otherwise at the start of the block l
already lies in; same for r. removeRange cuts the same slice out and leaves a boundary at l / r
only when that end was inside a block.

Steps
-----
1. ends = flat sorted list [l0, r0, l1, r1, ...]; even index = block start, odd = block end.
2. addRange: i = bisect_left(ends, l), j = bisect_right(ends, r); new boundaries = [l if i even]
   + [r if j even]; ends[i:j] = new.
3. removeRange: same i, j; new boundaries = [l if i odd] + [r if j odd]; ends[i:j] = new.
4. queryRange: i = bisect_right(ends, l), j = bisect_left(ends, r); return i == j and i odd.

Complexity: O(log n) search + O(n) list splice per op, O(n) space for n disjoint blocks —
            each op does two bisects and one slice assignment.
Pitfalls: mixing up bisect_left/bisect_right at the ends (touching blocks must merge on add,
          queryRange(l, r) must accept a block ending exactly at r); forgetting half-open
          semantics (removeRange(14,16) must leave 16 tracked); treating the list as pairs and
          hand-merging neighbours instead of using the parity trick.
"""
import random
from bisect import bisect_left, bisect_right


class RangeModule:
    def __init__(self):
        self.ends = []   # sorted boundaries [l0, r0, l1, r1, ...] of disjoint half-open ranges

    def addRange(self, left: int, right: int) -> None:
        i = bisect_left(self.ends, left)      # left == existing end -> i odd, blocks merge
        j = bisect_right(self.ends, right)    # right == existing start -> j odd, blocks merge
        new = []
        if i % 2 == 0:                        # left falls in a gap: it opens the merged block
            new.append(left)
        if j % 2 == 0:                        # right falls in a gap: it closes the merged block
            new.append(right)
        self.ends[i:j] = new                  # every boundary strictly inside is swallowed

    def queryRange(self, left: int, right: int) -> bool:
        i = bisect_right(self.ends, left)
        j = bisect_left(self.ends, right)
        return i == j and i % 2 == 1          # both ends inside the same tracked block

    def removeRange(self, left: int, right: int) -> None:
        i = bisect_left(self.ends, left)
        j = bisect_right(self.ends, right)
        new = []
        if i % 2 == 1:                        # left was inside a block: that block now ends here
            new.append(left)
        if j % 2 == 1:                        # right was inside a block: a block restarts here
            new.append(right)
        self.ends[i:j] = new


class BruteForce:
    """Set of every tracked integer point; O(right - left) per operation."""

    def __init__(self):
        self.points = set()

    def addRange(self, left: int, right: int) -> None:
        self.points.update(range(left, right))

    def queryRange(self, left: int, right: int) -> bool:
        return all(x in self.points for x in range(left, right))

    def removeRange(self, left: int, right: int) -> None:
        self.points.difference_update(range(left, right))


if __name__ == "__main__":
    rm = RangeModule()
    rm.addRange(10, 20)
    rm.removeRange(14, 16)
    assert rm.queryRange(10, 14) is True
    assert rm.queryRange(13, 15) is False
    assert rm.queryRange(16, 17) is True
    rm.addRange(14, 16)                       # fills the hole: blocks must merge back
    assert rm.ends == [10, 20]
    assert rm.queryRange(10, 20) is True
    rm.addRange(20, 25)                       # touching block merges
    assert rm.ends == [10, 25]
    rm.removeRange(10, 25)
    assert rm.ends == [] and rm.queryRange(10, 11) is False   # edge: empty module

    random.seed(715)
    fast, slow = RangeModule(), BruteForce()
    for _ in range(3000):
        l = random.randint(0, 60)
        r = random.randint(l + 1, 64)
        op = random.random()
        if op < 0.4:
            fast.addRange(l, r); slow.addRange(l, r)
        elif op < 0.7:
            fast.removeRange(l, r); slow.removeRange(l, r)
        else:
            assert fast.queryRange(l, r) == slow.queryRange(l, r)
    print("ok")
