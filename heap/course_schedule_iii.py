"""
Course Schedule III (LeetCode 630)  — Hard
Pattern: Sort by deadline + max-heap of taken durations (swap out the longest)

Problem
-------
Course i takes duration[i] days and must be finished on or before lastDay[i]. You start on
day 1 and take courses one at a time, back to back. Return the maximum number of courses you
can complete.
Example: [[100,200],[200,1300],[1000,1250],[2000,3200]] -> 3 (take 100, 1000, 200 in that
order; 2000 cannot fit). [[1,2]] -> 1. [[3,2],[4,3]] -> 0.

Brute force
-----------
Any feasible set of courses can be taken in deadline order (swapping two adjacent out-of-order
courses never breaks feasibility), so sort by deadline and try every subset: walk the subset
in that order, accumulate time, check each course meets its deadline, keep the largest
feasible subset. O(2^n * n) time -- exponential -- O(n) space. The waste: 2^n subsets are
checked although most differ only by swapping one long course for a shorter one, and the
sorted scan already tells us which course to drop.

From brute force to optimal
---------------------------
The redundancy is enumerating subsets when a single greedy pass decides membership. Step 1
(sorted greedy with a fix-up): scan courses by deadline, provisionally take each one; if the
running total exceeds its deadline, we must drop ONE course from the taken set -- dropping the
LONGEST taken course frees the most time, keeps the count maximal (we dropped one, we added
one), and makes every later deadline easier. Finding the longest by scanning the taken list
is O(n) per step, so O(n^2). Step 2: the only query on the taken set is "give me the longest",
so keep durations in a max-heap: push each course, and if time overflows pop the root and
subtract it. O(n log n). Invariant: after processing course i, the heap holds the largest
feasible set of courses among the first i, with the smallest total duration for that size.

Intuition
---------
Process deadlines in order so that "does this fit?" only depends on the total time already
committed. When a course does not fit, the count cannot grow, but we can still improve our
position: replace the longest course taken so far with this one if this one is shorter (the
pop-after-push handles both cases: if the new course is itself the longest, it gets popped
right back). Shorter total time now means more courses fit later. The count never decreases
and the total time is as small as possible for that count.

Geometric view
--------------
A timeline growing to the right; taken courses are bars laid end to end with their deadlines
as fences. A max-heap triangle beside the timeline holds the bar lengths with the longest at
the apex. When the stacked bars pass the current fence, the apex bar is pulled out and the
timeline shrinks back to the left -- the same number of bars, less total length.

Steps
-----
1. Sort courses by lastDay.
2. taken = [] (max-heap of durations via negation), time = 0.
3. For (d, last): push -d, time += d.
4. If time > last: pop the longest duration and subtract it from time.
5. Return len(taken).

Complexity: O(n log n) time, O(n) space — sort plus one push and at most one pop per course.
Pitfalls: Sorting by duration instead of deadline; dropping the current course instead of the
longest one; comparing time > last before adding the current course.
"""
import heapq
from typing import List


class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        courses.sort(key=lambda c: c[1])              # by deadline
        taken = []                                    # max-heap (negated) of durations we keep
        time = 0
        for duration, last in courses:
            heapq.heappush(taken, -duration)
            time += duration
            if time > last:                           # over the deadline: evict the longest course
                time += heapq.heappop(taken)          # popped value is negative
        return len(taken)


def brute_force(courses: List[List[int]]) -> int:
    # Exponential: try every subset in deadline order and keep the largest feasible one.
    cs = sorted(courses, key=lambda c: c[1])
    n, best = len(cs), 0
    for mask in range(1 << n):
        time, ok, count = 0, True, 0
        for i in range(n):
            if mask >> i & 1:
                time += cs[i][0]
                count += 1
                if time > cs[i][1]:
                    ok = False
                    break
        if ok:
            best = max(best, count)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]], 3),
        ([[1, 2]], 1),
        ([[3, 2], [4, 3]], 0),
        ([[5, 5], [4, 6], [2, 6]], 2),                # must swap out the 5 for the 2
        ([[7, 17], [3, 12], [10, 20], [9, 10], [5, 20], [10, 19], [4, 18]], 4),
    )
    for cs, want in cases:
        assert brute_force([c[:] for c in cs]) == want, (cs, want)
        assert s.scheduleCourse([c[:] for c in cs]) == want, (cs, want)
    import random
    random.seed(630)
    for _ in range(150):
        n = random.randint(1, 9)
        cs = [[random.randint(1, 10), random.randint(1, 25)] for _ in range(n)]
        assert s.scheduleCourse([c[:] for c in cs]) == brute_force(cs)
    print("ok")
