"""
Number of Recent Calls (LeetCode 933)  — Easy
Pattern: Sliding time window with a deque

Problem
-------
RecentCounter.ping(t) records a request at time t (ms) and returns how many requests happened
in the inclusive window [t - 3000, t]. Calls arrive with strictly increasing t.
Example: ping(1) -> 1; ping(100) -> 2; ping(3001) -> 3; ping(3002) -> 3 (t=1 is now too old).

Brute force
-----------
Store every timestamp in a list and, on each ping, count how many are >= t - 3000. O(n) per
ping and O(n) space for the whole history. The wasted work: a timestamp that fell out of the
window is re-examined on every later ping even though, with increasing t, it can never come
back into range.

From brute force to optimal
---------------------------
Because t only grows, the window's left edge t - 3000 only moves right. So a timestamp that is
too old now is too old forever, and old timestamps are always at the front (oldest first).
Keep a deque: append t at the back, then pop from the front while the front < t - 3000. The
answer is simply the deque's length. Each timestamp is appended once and popped at most once,
so the total work is O(n) across all pings.

Intuition
---------
Monotone time turns "count in range" into "maintain the range". Expiry happens in arrival
order, so the oldest element is always the next to leave, which is exactly what a queue's
front gives you.

Geometric view
--------------
A number line of timestamps with a bracket 3001 ms wide whose right edge sits on the newest
ping. Each ping slides the bracket right; dots that fall off its left edge are popped from the
deque and never looked at again. The deque is precisely the dots inside the bracket.

Steps
-----
1. q = deque().
2. ping(t): q.append(t).
3. While q[0] < t - 3000: q.popleft().
4. Return len(q).

Complexity: O(1) amortised per ping, O(W) space — W = max pings within 3000 ms; each t is
            pushed once and popped once.
Pitfalls: window is inclusive: evict only when q[0] < t - 3000 (not <=); scanning the whole
          history instead of stopping at the first in-window timestamp.
"""
import random
from collections import deque


class RecentCounter:
    def __init__(self):
        self.q = deque()

    def ping(self, t: int) -> int:
        self.q.append(t)
        while self.q[0] < t - 3000:     # oldest first, so expiry is always at the front
            self.q.popleft()
        return len(self.q)


class BruteForce:
    """Keep every timestamp; count the in-window ones on each ping, O(n)."""

    def __init__(self):
        self.times = []

    def ping(self, t: int) -> int:
        self.times.append(t)
        return sum(1 for x in self.times if x >= t - 3000)


if __name__ == "__main__":
    rc = RecentCounter()
    assert rc.ping(1) == 1
    assert rc.ping(100) == 2
    assert rc.ping(3001) == 3
    assert rc.ping(3002) == 3

    e = RecentCounter()                 # edge: exactly 3000 apart is still inside
    assert e.ping(0) == 1 and e.ping(3000) == 2 and e.ping(3001) == 2

    random.seed(933)
    for _ in range(30):
        fast, slow, t = RecentCounter(), BruteForce(), 0
        for _ in range(300):
            t += random.randint(1, 1500)
            assert fast.ping(t) == slow.ping(t)
    print("ok")
