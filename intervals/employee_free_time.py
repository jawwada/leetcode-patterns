"""
Employee Free Time (LeetCode 759)  — Hard
Pattern: K-way merge of sorted interval lists with a min-heap, emitting gaps

Problem
-------
schedule[i] is the sorted, non-overlapping list of working intervals of employee i. Return the
finite intervals of positive length during which EVERY employee is free, in sorted order.
Example: [[[1,2],[5,6]],[[1,3]],[[4,10]]] -> [[3,4]].
[[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]] -> [[5,6],[7,9]].

Brute force
-----------
A common free interval must start at some employee's end time e and finish at some start time
s > e, with no interval of anyone covering a point strictly between them. Try every (end,
start) pair and check every interval: valid pairs are exactly the maximal gaps. With N total
intervals that is O(N^2) pairs times O(N) checking, O(N^3) time, O(N) space. The waste: the
check rescans all N intervals for every pair although, in time order, only the interval that
ends latest so far decides whether a gap opens before the next start.

From brute force to optimal
---------------------------
Redundancy one: gaps can be found with a single pass if all intervals are visited in start
order while tracking the furthest end seen; a gap opens whenever the next start exceeds that
end. Flattening and sorting everyone's intervals gives this in O(N log N). Redundancy two:
each employee's list is ALREADY sorted, so a full re-sort ignores the given structure. A
k-way merge replaces it: push each employee's first interval into a min-heap keyed by start,
pop the earliest, compare its start against the running furthest end (gap if larger), extend
the end, and push that employee's next interval. O(N log k) with k employees -- the same
mechanism as merging k sorted lists, with "emit a gap" instead of "append a node".

Intuition
---------
You need the union of everyone's busy time; the free time is its complement, minus the
unbounded ends. Intervals popped in start order from the heap arrive exactly like a single
merged sorted list. Keep "the latest moment anyone has been busy up to now" -- if the next
busy interval starts after that moment, the stretch in between is free for all.

Geometric view
--------------
k rows of bars (one row per employee) above a shared time axis; a min-heap triangle holds the
leftmost unprocessed bar from each row, earliest start at the apex. A sweep line sits at the
furthest right edge merged so far. Each pop takes the apex bar: if its left edge is beyond the
sweep line, the white space between them is a free interval; either way the sweep line jumps
to max(itself, the bar's right edge).

Steps
-----
1. heap = [(schedule[i][0].start, i, 0) for each non-empty employee i]; heapify.
2. Pop (start, i, j); if start > reach (and reach is initialised) emit Interval(reach, start).
3. reach = max(reach, schedule[i][j].end).
4. If j + 1 < len(schedule[i]) push (schedule[i][j+1].start, i, j+1).
5. Repeat until the heap is empty; return the emitted intervals.

Complexity: O(N log k) time, O(k) space — each of the N intervals passes through a heap of size
<= k; the output is not counted.
Pitfalls: Emitting zero-length gaps when an interval starts exactly when another ends; updating
reach with the popped interval's end without taking the max (an interval nested inside a longer
one would shrink the busy span); forgetting employees with empty schedules.
"""
import heapq
from typing import List


class Interval:
    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end


class Solution:
    def employeeFreeTime(self, schedule: List[List[Interval]]) -> List[Interval]:
        heap = [(emp[0].start, i, 0) for i, emp in enumerate(schedule) if emp]
        heapq.heapify(heap)                           # (start, employee, index): k-way merge
        free = []
        reach = None                                  # furthest end of busy time merged so far
        while heap:
            start, i, j = heapq.heappop(heap)
            iv = schedule[i][j]
            if reach is not None and start > reach:   # nobody is busy in (reach, start)
                free.append(Interval(reach, start))
            reach = iv.end if reach is None else max(reach, iv.end)
            if j + 1 < len(schedule[i]):
                heapq.heappush(heap, (schedule[i][j + 1].start, i, j + 1))
        return free


def brute_force(schedule: List[List[Interval]]) -> List[Interval]:
    # Every (end, start) pair is a candidate gap; keep it if no interval covers its interior.
    all_iv = [iv for emp in schedule for iv in emp]
    gaps = set()
    for a in all_iv:
        for b in all_iv:
            if a.end < b.start and all(iv.end <= a.end or iv.start >= b.start for iv in all_iv):
                gaps.add((a.end, b.start))
    return [Interval(s, e) for s, e in sorted(gaps)]


def build(raw: List[List[List[int]]]) -> List[List[Interval]]:
    return [[Interval(s, e) for s, e in emp] for emp in raw]


def to_list(ivs: List[Interval]) -> List[List[int]]:
    return [[iv.start, iv.end] for iv in ivs]


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]], [[3, 4]]),
        ([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]], [[5, 6], [7, 9]]),
        ([[[1, 2]], [[2, 3]]], []),                              # touching: zero-length gap, none
        ([[[1, 4]], [[2, 3]]], []),                              # nested
        ([[[1, 2]], [], [[5, 6]]], [[2, 5]]),                    # an employee with no shifts
    )
    for raw, want in cases:
        assert to_list(s.employeeFreeTime(build(raw))) == want, (raw, want)
        assert to_list(brute_force(build(raw))) == want, (raw, want)
    import random
    random.seed(759)
    for _ in range(200):
        raw = []
        for _ in range(random.randint(1, 4)):
            pts = sorted(random.sample(range(0, 30), 2 * random.randint(0, 3)))
            raw.append([[pts[i], pts[i + 1]] for i in range(0, len(pts), 2)])
        assert to_list(s.employeeFreeTime(build(raw))) == to_list(brute_force(build(raw))), raw
    print("ok")
