"""
Maximum Performance of a Team (LeetCode 1383)  — Hard
Pattern: Sort by the bottleneck (efficiency desc) + min-heap of the top-k other values

Problem
-------
n engineers have speed[i] and efficiency[i]. Choose at most k of them; a team's performance is
(sum of speeds) * (minimum efficiency). Return the maximum performance modulo 1e9+7.
Example: speed=[2,10,3,1,5,8], efficiency=[5,4,3,9,7,2], k=2 -> 60 (engineers 2 and 5: speeds
10+5=15, min efficiency 4).

Brute force
-----------
Enumerate every subset of size 1..k, compute sum(speed) * min(efficiency), keep the best.
O(C(n,1) + ... + C(n,k)) subsets -- exponential in k -- times O(k) per subset, O(k) space.
The waste: the product is governed by a single bottleneck engineer (the one with the minimum
efficiency), yet subsets with the same bottleneck are enumerated over and over, each
rebuilding a speed sum from scratch, when for a fixed bottleneck the best team is simply the
k-1 fastest engineers with efficiency >= the bottleneck's.

From brute force to optimal
---------------------------
Redundancy one: for a fixed minimum-efficiency engineer e, the optimal team is forced: e plus
the up-to-(k-1) fastest engineers among those at least as efficient. That reduces 2^n subsets
to n candidates, each costing O(n log n) to sort by speed -> O(n^2 log n). Redundancy two:
if we visit engineers in DEcreasing efficiency, the pool "at least as efficient as e" is
exactly the engineers already visited, so the pool only grows by one per step. We just need
"the top k speeds in a growing pool" -- a min-heap of size k: push each speed, and if the
heap exceeds k, pop the smallest (subtracting it from a running sum). At each step the
candidate performance is running_sum * efficiency[e]. O(n log n) total. Note the heap may
hold k speeds while e's own speed was popped; that is fine because the team it represents
has min efficiency >= efficiency[e], so its real performance is at least as large and it was
(or will be) scored at its true bottleneck.

Intuition
---------
Decide the bottleneck first. Sort engineers by efficiency descending so that when you stand
on engineer e, everyone before you is at least as efficient and therefore free to join
without lowering the minimum. Among those, you want the k-1 largest speeds (plus e), and a
size-k min-heap keeps exactly the k largest speeds seen so far. Score every position; the
true optimum has SOME bottleneck, and when the sweep reaches that engineer the heap holds the
best possible teammates.

Geometric view
--------------
Engineers on a horizontal axis sorted by efficiency, high on the left. A sweep line moves
right; its position fixes the multiplier (the efficiency at the line). Left of the line is
the eligible pool, and a triangle (min-heap) hovering above it keeps the k tallest speed bars
from that pool, with the shortest kept bar at the apex ready to be ejected. Performance at
each step = (height of kept bars) * (efficiency at the line).

Steps
-----
1. Pair (efficiency, speed) and sort by efficiency descending.
2. speeds = [] (min-heap), total = 0, best = 0.
3. For each (e, s): push s, total += s.
4. If len(speeds) > k: total -= heappop(speeds).
5. best = max(best, total * e).
6. Return best % (10^9 + 7).

Complexity: O(n log n) time, O(k) space — sort plus one push and at most one pop per engineer.
Pitfalls: Taking the modulo before the max comparison (modulo destroys ordering); sorting
by efficiency ascending; using a max-heap (we evict the SMALLEST speed); forgetting that the
team may have fewer than k members.
"""
import heapq
from typing import List


class Solution:
    def maxPerformance(self, n: int, speed: List[int], efficiency: List[int], k: int) -> int:
        engineers = sorted(zip(efficiency, speed), reverse=True)   # bottleneck first
        speeds = []                                                # min-heap of kept speeds
        total = best = 0
        for eff, spd in engineers:
            heapq.heappush(speeds, spd)
            total += spd
            if len(speeds) > k:
                total -= heapq.heappop(speeds)                     # evict the slowest
            best = max(best, total * eff)                          # eff is the min so far
        return best % (10 ** 9 + 7)


def brute_force(n: int, speed: List[int], efficiency: List[int], k: int) -> int:
    # Exponential: every subset of size 1..k, score = sum(speed) * min(efficiency).
    from itertools import combinations
    best = 0
    for size in range(1, k + 1):
        for team in combinations(range(n), size):
            perf = sum(speed[i] for i in team) * min(efficiency[i] for i in team)
            best = max(best, perf)
    return best % (10 ** 9 + 7)


if __name__ == "__main__":
    s = Solution()
    cases = (
        ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2), 60),
        ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 3), 68),
        ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 4), 72),
        ((1, [7], [3], 1), 21),                                   # single engineer
        ((3, [1, 1, 1], [10, 10, 10], 5), 30),                    # k larger than n
    )
    for args, want in cases:
        assert s.maxPerformance(*args) == want, (args, want)
        assert brute_force(*args) == want, (args, want)
    import random
    random.seed(1383)
    for _ in range(200):
        n = random.randint(1, 8)
        sp = [random.randint(1, 20) for _ in range(n)]
        ef = [random.randint(1, 20) for _ in range(n)]
        k = random.randint(1, n)
        assert s.maxPerformance(n, sp, ef, k) == brute_force(n, sp, ef, k)
    print("ok")
