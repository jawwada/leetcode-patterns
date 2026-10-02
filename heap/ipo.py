"""
IPO (LeetCode 502)  — Hard
Pattern: Sort by threshold + max-heap of unlocked candidates

Problem
-------
You have capital w and may run at most k projects. Project i needs capital[i] >= current
capital to start and pays profits[i] (pure profit, added to your capital when done). Pick at
most k distinct projects, one after another, to maximise final capital.
Example: k=2, w=0, profits=[1,2,3], capital=[0,1,1] -> 4 (do project 0 to reach w=1, then
project 2 for +3).

Brute force
-----------
Greedy with a full rescan: k times, scan all n projects, find the affordable unpicked one with
the largest profit, take it. O(k*n) time, O(n) space for the picked set. (Trying all orderings
is exponential and pointless: capital only grows, so a project that is affordable now stays
affordable.) The waste is that every round re-examines every project, re-discovering the
same affordable set plus a few newly unlocked projects.

From brute force to optimal
---------------------------
The redundancy is rescanning projects whose status never changes: once affordable, a project
stays affordable forever because capital is non-decreasing. Observation: the affordable set
only GROWS, and it grows in capital order. So sort projects by required capital and keep a
pointer; each round, advance the pointer to push every newly affordable project's profit into
a max-heap. The heap then answers "best affordable project" in O(log n) instead of O(n). Each
project is pushed once and popped at most once, giving O((n + k) log n). If the heap is ever
empty we cannot afford anything and stop early.

Intuition
---------
Capital is a key that unlocks projects; keys only get stronger. The heap is the pile of
unlocked projects; the best move is always the biggest profit in that pile because profit is
pure gain and does not disable any other option. Doing the biggest unlocked profit first
unlocks at least as much as any other choice would (exchange argument).

Geometric view
--------------
Projects as points on a capital axis, sorted left to right. A vertical bar at position w
sweeps right as capital grows; every point it passes is dropped into a max-heap triangle whose
apex is the largest profit seen so far. Each round: move the bar right over newly affordable
points, pop the apex, add it to w, repeat k times.

Steps
-----
1. Pair projects as (capital, profit) and sort by capital; i = 0.
2. Repeat up to k times:
   a. While i < n and projects[i].capital <= w: push -profit onto the heap, i += 1.
   b. If heap is empty, break (nothing affordable, and nothing will become affordable).
   c. w += -heappop(heap).
3. Return w.

Complexity: O((n + k) log n) time, O(n) space — each project pushed once, k pops; heap holds <= n.
Pitfalls: Re-sorting or rescanning every round; forgetting the early break when the heap is
empty (would pop from an empty heap or loop uselessly); using a min-heap or forgetting to
negate profits.
"""
import heapq
from typing import List


class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        projects = sorted(zip(capital, profits))      # by required capital
        unlocked = []                                 # max-heap (negated) of affordable profits
        i, n = 0, len(projects)
        for _ in range(k):
            while i < n and projects[i][0] <= w:      # w only grows, so i only moves right
                heapq.heappush(unlocked, -projects[i][1])
                i += 1
            if not unlocked:                          # nothing affordable now or ever
                break
            w -= heapq.heappop(unlocked)              # add the largest affordable profit
        return w


def brute_force(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    # k rounds; each round rescans all projects for the best affordable unpicked one.
    done = [False] * len(profits)
    for _ in range(k):
        best = -1
        for j in range(len(profits)):
            if not done[j] and capital[j] <= w and (best < 0 or profits[j] > profits[best]):
                best = j
        if best < 0:
            break
        done[best] = True
        w += profits[best]
    return w


if __name__ == "__main__":
    s = Solution()
    cases = (
        ((2, 0, [1, 2, 3], [0, 1, 1]), 4),
        ((3, 0, [1, 2, 3], [0, 1, 2]), 6),
        ((1, 0, [1, 2, 3], [1, 1, 2]), 0),           # nothing affordable
        ((10, 0, [1, 2, 3], [0, 1, 1]), 6),          # k larger than n
        ((2, 5, [4, 9, 1], [10, 2, 3]), 18),
    )
    for args, want in cases:
        assert s.findMaximizedCapital(*args) == want, (args, want)
        assert brute_force(*args) == want, (args, want)
    import random
    random.seed(502)
    for _ in range(200):
        n = random.randint(1, 8)
        p = [random.randint(0, 10) for _ in range(n)]
        c = [random.randint(0, 10) for _ in range(n)]
        k, w = random.randint(1, 8), random.randint(0, 5)
        assert s.findMaximizedCapital(k, w, p, c) == brute_force(k, w, p, c)
    print("ok")
