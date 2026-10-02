"""
Data Stream as Disjoint Intervals (LeetCode 352)  — Hard
Pattern: Sorted disjoint intervals with bisect

Problem
-------
Non-negative integers arrive one at a time. Implement SummaryRanges with addNum(value) and
getIntervals(), which returns the current set of values as a sorted list of disjoint closed
intervals [start, end] (consecutive integers are merged into one interval).
Example: add 1 -> [[1,1]]; add 3 -> [[1,1],[3,3]]; add 7 -> [[1,1],[3,3],[7,7]];
add 2 -> [[1,3],[7,7]]; add 6 -> [[1,3],[6,7]].

Brute force
-----------
Keep every value in a set. getIntervals sorts the set and walks it once, starting a new interval
whenever the next value is not previous + 1. O(1) addNum, O(n log n) per getIntervals, O(n) space.
The wasted work: every getIntervals call re-sorts and re-merges the whole stream from scratch,
even though a new value can change at most two neighbouring intervals.

From brute force to optimal
---------------------------
The redundancy is rebuilding the merged structure on every query. Observation: if the intervals
are kept disjoint and sorted at all times, a new value v interacts only with the interval whose
start is the largest start <= v (does it already contain v, or end exactly at v-1?) and the next
one (does it start exactly at v+1?). Store starts and ends as two parallel sorted lists and find
that neighbour with bisect_right(starts, v). Four cases: v already covered -> nothing; touches
both neighbours -> glue them into one; touches the left one -> extend its end; touches the right
one -> lower its start; otherwise insert [v, v]. getIntervals just zips the two lists, O(k) for
k intervals. In a balanced-tree language the insert is O(log n); Python's list insert is an O(n)
memmove, which is still far cheaper than the O(n log n) re-sort.

Intuition
---------
Maintain the answer incrementally. Because the intervals are disjoint and sorted, a new value can
only (a) fall inside one of them, (b) extend one by one unit, (c) bridge a gap of exactly one
between two of them, or (d) start a fresh singleton. Binary search finds the only candidate
neighbours in O(log n), so each addNum does constant work beyond the search.

Geometric view
--------------
Picture the number line with the intervals as solid segments. A new point lands either on a
segment (ignore), directly against the right end of a segment (segment grows right), directly
against the left end of a segment (grows left), against both (two segments fuse into one), or in
open space (new dot).

Steps
-----
1. starts, ends: parallel sorted lists of disjoint closed intervals.
2. addNum(v): i = bisect_right(starts, v); the candidate left interval is i-1.
3. If i > 0 and ends[i-1] >= v: already covered, return.
4. left = (i > 0 and ends[i-1] == v-1); right = (i < len and starts[i] == v+1).
5. Both: ends[i-1] = ends[i], delete interval i. Left only: ends[i-1] = v.
   Right only: starts[i] = v. Neither: insert v into both lists at i.
6. getIntervals: list(zip(starts, ends)).

Complexity: O(log n) search + O(n) list shift per addNum, O(k) getIntervals, O(k) space —
            bisect locates the only two intervals that can change.
Pitfalls: forgetting the "already covered" check (produces overlapping intervals); handling
          "touches both neighbours" as two separate extensions and leaving [1,3],[4,7] unmerged;
          using bisect_left and then reading the wrong neighbour when v equals an existing start.
"""
import random
from bisect import bisect_right
from typing import List


class SummaryRanges:
    def __init__(self):
        self.starts: List[int] = []   # sorted interval starts
        self.ends: List[int] = []     # parallel inclusive ends

    def addNum(self, value: int) -> None:
        i = bisect_right(self.starts, value)          # interval i-1 has the largest start <= value
        if i and self.ends[i - 1] >= value:           # already inside an interval
            return
        touch_left = i > 0 and self.ends[i - 1] == value - 1
        touch_right = i < len(self.starts) and self.starts[i] == value + 1
        if touch_left and touch_right:                # bridge a gap of exactly one
            self.ends[i - 1] = self.ends[i]
            del self.starts[i], self.ends[i]
        elif touch_left:
            self.ends[i - 1] = value
        elif touch_right:
            self.starts[i] = value
        else:
            self.starts.insert(i, value)
            self.ends.insert(i, value)

    def getIntervals(self) -> List[List[int]]:
        return [[s, e] for s, e in zip(self.starts, self.ends)]


class BruteForce:
    """Set of seen values; getIntervals re-sorts and re-merges everything, O(n log n)."""

    def __init__(self):
        self.seen = set()

    def addNum(self, value: int) -> None:
        self.seen.add(value)

    def getIntervals(self) -> List[List[int]]:
        out = []
        for v in sorted(self.seen):
            if out and out[-1][1] == v - 1:
                out[-1][1] = v
            else:
                out.append([v, v])
        return out


if __name__ == "__main__":
    sr = SummaryRanges()
    sr.addNum(1); assert sr.getIntervals() == [[1, 1]]
    sr.addNum(3); assert sr.getIntervals() == [[1, 1], [3, 3]]
    sr.addNum(7); assert sr.getIntervals() == [[1, 1], [3, 3], [7, 7]]
    sr.addNum(2); assert sr.getIntervals() == [[1, 3], [7, 7]]
    sr.addNum(6); assert sr.getIntervals() == [[1, 3], [6, 7]]
    sr.addNum(2); assert sr.getIntervals() == [[1, 3], [6, 7]]   # edge: duplicate value
    sr.addNum(4); sr.addNum(5)
    assert sr.getIntervals() == [[1, 7]]                         # edge: everything fuses

    random.seed(352)
    fast, slow = SummaryRanges(), BruteForce()
    for _ in range(2000):
        v = random.randint(0, 120)
        fast.addNum(v); slow.addNum(v)
        if random.random() < 0.2:
            assert fast.getIntervals() == slow.getIntervals()
    assert fast.getIntervals() == slow.getIntervals()
    print("ok")
