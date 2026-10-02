"""
Maximum Running Time of N Computers (LeetCode 2141)  — Hard
Pattern: Binary search on the answer

Problem
-------
You have `n` computers and `batteries[i]` minutes of charge in battery i. A computer runs on one
battery at a time; you may swap batteries between computers at any integer minute, any number of
times, but a battery's charge is never pooled or recharged. Return the maximum number of minutes
you can keep ALL n computers running simultaneously.
Example: n = 2, batteries = [3,3,3] -> 4  (minutes 1-2: A,B; minute 3: A,C; minute 4: B,C —
each battery contributes 3 of the 2*4 = 8 battery-minutes needed, none is wasted).
Example: n = 2, batteries = [1,1,1,1] -> 2.

Brute force
-----------
Simulate minute by minute: each minute put the n batteries with the most remaining charge on the
computers (greedy by largest remaining is optimal), subtract 1 from each, stop when fewer than n
batteries have charge left. O(T * m log m) time where T is the answer (up to 10^14 / n), O(m)
space. The waste: the simulation re-sorts and re-decides every single minute, although the
outcome of the whole run is determined by a single inequality.

From brute force to optimal
---------------------------
The redundancy is stepping through every minute. Ask instead "can all n computers run for t
minutes?" This predicate is monotone (t feasible => t-1 feasible), so binary search over t
finds the largest True. For the check: in t minutes a single battery can contribute at most
min(b, t) minutes (a battery can only power one computer at a time, so t is a hard cap), and we
need n*t battery-minutes in total. So sum(min(b, t)) >= n*t is necessary; it is also sufficient
because the batteries can be laid out end to end along a strip of length n*t and cut into n
rows of length t — no battery of length <= t ever lands in the same row twice. One O(m) pass
per probe, log(sum/n) probes.

Intuition
---------
A battery longer than t is wasted beyond t, everything else is fully usable; so clamp each
battery to t and ask whether the clamped total covers n*t. The upper bound sum(batteries)//n is
the no-waste ceiling; binary search between 0 and that for the last t where the clamped total
still suffices.

Geometric view
--------------
Draw a strip n rows tall and t columns wide (n*t cells to fill). Lay batteries down one after
another, wrapping to the next row when a row fills; since every clamped battery has length
<= t, no battery can wrap onto itself, so the rows are valid schedules. Over t, feasible(t)
is TTT...TFFF...F; lo/hi squeeze onto the last T.

Steps
-----
1. lo = 0, hi = sum(batteries) // n (cannot do better than spending every minute).
2. can(t) = sum(min(b, t) for b in batteries) >= n * t.
3. While lo < hi: mid = (lo + hi + 1) // 2 (round up: we want the LAST True).
4. If can(mid): lo = mid else hi = mid - 1.
5. Return lo.

Complexity: O(m log(S / n)) time where S = sum(batteries), O(1) space — each probe is one pass.
Pitfalls: using mid = (lo+hi)//2 with lo = mid (infinite loop; this is the "last True"
template); forgetting the min(b, t) clamp (a 100-minute battery cannot power two computers at
once); 32-bit overflow in other languages (sum reaches 10^14).
"""
import heapq
import random
from typing import List


class Solution:
    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        def can(t: int) -> bool:
            # each battery gives at most t minutes to the n*t minute-slots
            return sum(min(b, t) for b in batteries) >= n * t

        lo, hi = 0, sum(batteries) // n          # hi: every minute of charge used, no waste
        while lo < hi:                           # find the LAST t with can(t)
            mid = (lo + hi + 1) // 2             # round up so lo = mid always progresses
            if can(mid):
                lo = mid                         # feasible: try longer
            else:
                hi = mid - 1                     # infeasible: must run shorter
        return lo


def brute_force(n: int, batteries: List[int]) -> int:
    heap = [-b for b in batteries]               # max-heap of remaining charge
    heapq.heapify(heap)
    minutes = 0
    while len(heap) >= n:                        # one minute per iteration
        used = [heapq.heappop(heap) for _ in range(n)]     # n fullest batteries
        for b in used:
            if b + 1 < 0:                        # still has charge after this minute
                heapq.heappush(heap, b + 1)
        minutes += 1
    return minutes


if __name__ == "__main__":
    s = Solution()
    assert s.maxRunTime(2, [3, 3, 3]) == 4
    assert s.maxRunTime(2, [1, 1, 1, 1]) == 2
    assert s.maxRunTime(1, [5]) == 5
    assert s.maxRunTime(3, [10, 10, 3, 5]) == 8          # one battery clamped to t
    assert s.maxRunTime(3, [1, 1, 1]) == 1
    assert s.maxRunTime(2, [100, 1]) == 1                # big battery cannot be split
    rng = random.Random(2141)
    for _ in range(200):
        n = rng.randint(1, 4)
        m = rng.randint(n, 7)
        batteries = [rng.randint(1, 15) for _ in range(m)]
        assert s.maxRunTime(n, batteries) == brute_force(n, batteries), (n, batteries)
    print("ok")
