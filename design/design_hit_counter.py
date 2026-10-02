"""
Design Hit Counter (LeetCode 362)  — Medium
Pattern: Sliding window queue with running sum

Problem
-------
Implement HitCounter: hit(timestamp) records a hit, getHits(timestamp) returns the number of
hits in the past 300 seconds, i.e. with t in (timestamp - 300, timestamp]. Timestamps arrive in
non-decreasing order and several hits may share one timestamp.
Example: hit(1) hit(2) hit(3) getHits(4)->3 hit(300) getHits(300)->4 getHits(301)->3.

Brute force
-----------
Append every timestamp to a list; getHits(t) scans the whole list counting entries > t - 300.
O(n) per getHits and O(n) space that grows forever. The wasted work is re-counting hits that
are already known to be inside the window, and keeping hits that can never be counted again
(anything older than 300 s is dead weight).

From brute force to optimal
---------------------------
Because timestamps are non-decreasing, the list is sorted and the expired entries are always a
prefix. So a queue suffices: push new hits at the back, pop expired ones from the front, and
maintain a running total so getHits never counts. Each hit is pushed once and popped once, so
work is O(1) amortised. To bound memory even under bursts, collapse hits with the same
timestamp into one (timestamp, count) pair: the queue then holds at most 300 entries. The
tracker must remember only the hits inside the current window; everything older can be
forgotten the moment it leaves.

Intuition
---------
The window is "the last 300 seconds". Since time only moves forward, a hit that has expired
never becomes valid again, so evicting it is final. A queue is exactly the structure where you
add at one end and remove from the other in arrival order.

Geometric view
--------------
A conveyor of (timestamp, count) pairs:  front -> (1,1) (2,1) (3,1) (300,1) <- back, total 4
getHits(301): threshold 301-300 = 1, pop (1,1) -> total 3. The front marker only advances,
the back only grows; each pair crosses the window exactly once.

Steps
-----
1. window = deque of (timestamp, count); total = 0.
2. hit(t): if back has the same timestamp, increment its count; else append (t, 1). total += 1.
3. _evict(t): while front timestamp <= t - 300: pop it and subtract its count from total.
4. getHits(t): evict then return total.

Complexity: O(1) amortised time per operation, O(min(n, 300)) space — each pair is enqueued and dequeued once.
Pitfalls: window boundary (t - 300 is excluded, t itself included); forgetting to evict in
          getHits when no hit arrives; unbounded memory if same-timestamp hits aren't merged.
"""
import random
from collections import deque


class HitCounter:
    def __init__(self):
        self.window = deque()      # (timestamp, count), oldest at the front
        self.total = 0             # hits currently inside the 300 s window

    def _evict(self, timestamp: int) -> None:
        while self.window and self.window[0][0] <= timestamp - 300:
            self.total -= self.window.popleft()[1]

    def hit(self, timestamp: int) -> None:
        if self.window and self.window[-1][0] == timestamp:
            self.window[-1] = (timestamp, self.window[-1][1] + 1)
        else:
            self.window.append((timestamp, 1))
        self.total += 1
        self._evict(timestamp)

    def getHits(self, timestamp: int) -> int:
        self._evict(timestamp)
        return self.total


class BruteForce:
    """Append every timestamp; getHits re-scans the whole history, O(n)."""

    def __init__(self):
        self.hits = []

    def hit(self, timestamp: int) -> None:
        self.hits.append(timestamp)

    def getHits(self, timestamp: int) -> int:
        return sum(1 for t in self.hits if timestamp - 300 < t <= timestamp)


if __name__ == "__main__":
    h = HitCounter()
    h.hit(1)
    h.hit(2)
    h.hit(3)
    assert h.getHits(4) == 3
    h.hit(300)
    assert h.getHits(300) == 4
    assert h.getHits(301) == 3

    e = HitCounter()                       # edge: burst at one timestamp, then it all expires at once
    for _ in range(5):
        e.hit(10)
    assert e.getHits(10) == 5 and e.getHits(309) == 5 and e.getHits(310) == 0
    assert len(e.window) == 0

    random.seed(4)
    fast, slow = HitCounter(), BruteForce()
    t = 1
    for _ in range(2000):
        t += random.choice([0, 0, 1, 2, 50])
        if random.random() < 0.6:
            fast.hit(t)
            slow.hit(t)
        else:
            assert fast.getHits(t) == slow.getHits(t)
    print("ok")
