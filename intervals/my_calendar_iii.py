"""
My Calendar III (LeetCode 732)  — Hard
Pattern: Difference array / prefix-sum sweep

Problem
-------
Implement MyCalendarThree. book(startTime, endTime) adds the half-open event [start, end) and
returns the maximum k such that some instant is covered by k events after this booking (the
largest k-booking so far). Events are never rejected.
Example: book(10,20) -> 1; book(50,60) -> 1; book(10,40) -> 2; book(5,15) -> 3;
book(5,10) -> 3; book(25,55) -> 3.

Brute force
-----------
Store every booked interval. After each booking, the maximum overlap is attained at some event
start, so for every start s count the intervals with start <= s < end and take the max.
O(n^2) per book, O(n^3) over n bookings, O(n) space. The wasted work: each start is compared
against every interval, although walking the boundaries in sorted order lets a single running
counter answer "how many events are open here" for all points at once.

From brute force to optimal
---------------------------
The redundancy is recounting from scratch at every candidate point. Observation: the overlap
count at any instant equals (#starts <= t) - (#ends <= t), so if you record +1 at each start and
-1 at each end in a map keyed by coordinate, then sweep the keys in sorted order while summing,
the running total IS the overlap at every boundary and its maximum is the answer. That is the
difference-array / prefix-sum idea applied to a sparse, unbounded coordinate space. Keep the
distinct boundaries in a sorted list (bisect.insort on insert) so each book is one O(n) sweep,
O(n^2) overall instead of O(n^3). The follow-up structure is a lazy segment tree over the
coordinate range (range add, global max) giving O(log C) per book, but the sweep is what you are
expected to produce first and it passes.

Intuition
---------
Overlap is a step function that goes up by one at every start and down by one at every end.
Store only the steps. Summing them left to right reconstructs the function, and its highest
step is the maximum k-booking.

Geometric view
--------------
Draw each event as a horizontal bar. Project the bar ends onto the time axis: every left end is
an up-tick, every right end a down-tick. Walk the axis once with a counter; the counter traces
the skyline of stacked bars, and the tallest point of that skyline is the answer.

Steps
-----
1. delta: dict coordinate -> net change (+1 per start, -1 per end); points: sorted list of
   distinct coordinates.
2. book(s, e): delta[s] += 1, delta[e] -= 1, insort each new coordinate into points.
3. Sweep points in order: active += delta[p]; best = max(best, active).
4. Return best.

Complexity: O(n) per book, O(n^2) total for n bookings, O(n) space —
            one sorted sweep over at most 2n boundaries per call.
Pitfalls: treating intervals as closed (book(5,10) after book(10,20) must not create an overlap
          at 10); re-sorting the keys on every call when an ordered insert suffices; returning
          the overlap at the new interval only instead of the global maximum.
"""
import random
from bisect import insort
from typing import List


class MyCalendarThree:
    def __init__(self):
        self.delta = {}       # boundary -> +1 for each start, -1 for each end
        self.points = []      # sorted distinct boundaries

    def book(self, startTime: int, endTime: int) -> int:
        for p, d in ((startTime, 1), (endTime, -1)):
            if p not in self.delta:
                self.delta[p] = 0
                insort(self.points, p)
            self.delta[p] += d
        best = active = 0
        for p in self.points:                 # prefix sum of the steps = overlap at p
            active += self.delta[p]
            best = max(best, active)
        return best


class BruteForce:
    """Store every interval; count containment at every start point. O(n^2) per book."""

    def __init__(self):
        self.events: List[tuple] = []

    def book(self, startTime: int, endTime: int) -> int:
        self.events.append((startTime, endTime))
        best = 0
        for s, _ in self.events:
            best = max(best, sum(1 for a, b in self.events if a <= s < b))
        return best


if __name__ == "__main__":
    cal = MyCalendarThree()
    assert cal.book(10, 20) == 1
    assert cal.book(50, 60) == 1
    assert cal.book(10, 40) == 2
    assert cal.book(5, 15) == 3
    assert cal.book(5, 10) == 3
    assert cal.book(25, 55) == 3
    touch = MyCalendarThree()
    assert touch.book(10, 20) == 1
    assert touch.book(20, 30) == 1              # edge: touching intervals do not overlap

    random.seed(732)
    fast, slow = MyCalendarThree(), BruteForce()
    for _ in range(300):
        s = random.randint(0, 100)
        e = random.randint(s + 1, 110)
        assert fast.book(s, e) == slow.book(s, e)
    print("ok")
