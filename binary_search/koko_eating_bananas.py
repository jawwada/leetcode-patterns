"""
Koko Eating Bananas (LeetCode 875)  — Medium
Pattern: Binary search on the answer

Problem
-------
`piles[i]` bananas are in pile i. Each hour Koko picks one pile and eats up to `k` bananas from it
(if the pile has fewer she finishes it and waits). Return the minimum integer speed `k` such that
she can eat every pile within `h` hours.
Example: piles = [3,6,7,11], h = 8 -> 4 (hours at k=4: 1+2+2+3 = 8).

Brute force
-----------
Try k = 1, 2, 3, ... and for each compute total hours = sum(ceil(p / k)); return the first k whose
hours <= h. O(max(piles) * n) time, O(1) space. The wasted work: we evaluate feasibility for every
speed in order, even though once a speed works every larger speed also works — most of those
checks are confirming something we could already infer.

From brute force to optimal
---------------------------
The redundancy is linear scanning of a predicate that is monotone: feasible(k) is False for small
k and flips to True exactly once, staying True forever (eating faster never takes more hours). A
monotone boolean sequence FFF...FTTT...T is "sorted", so we can binary search for the first T.
The search space is the answer itself, k in [1, max(piles)]; the comparison is replaced by a
feasibility check costing O(n). Total O(n log max(piles)).

Intuition
---------
Don't search the data — search the answer. If you can write a cheap `can(k)` that is monotone
in k, binary search finds the boundary between "cannot" and "can" in log steps. Here, any k >=
max(piles) trivially works (one hour per pile), so that is the upper bound.

Geometric view
--------------
Draw the speeds 1..max on a line; above each paint F or T for "finishes within h hours". The
picture is a solid block of F followed by a solid block of T. lo/hi squeeze onto the F|T
boundary: when mid is T we move hi to mid (mid might be the answer), when F we move lo to mid+1.

Steps
-----
1. lo = 1, hi = max(piles).
2. hours(k) = sum((p + k - 1) // k for p in piles)  (ceiling division).
3. While lo < hi: mid = (lo+hi)//2.
4. If hours(mid) <= h: hi = mid (feasible, try slower) else lo = mid + 1.
5. Return lo.

Complexity: O(n log M) time where M = max(piles), O(1) space — log M feasibility checks of O(n) each.
Pitfalls: using `//` without ceiling; setting lo = 0 (division by zero); using `hi = mid - 1` and
then returning hi; forgetting that `lo < hi` + `hi = mid` is the pattern for "first True".
"""
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def hours(k: int) -> int:
            return sum((p + k - 1) // k for p in piles)   # ceil(p / k)

        lo, hi = 1, max(piles)               # k = max(piles) always suffices
        while lo < hi:                       # find first k with hours(k) <= h
            mid = (lo + hi) // 2
            if hours(mid) <= h:
                hi = mid                     # feasible: answer is mid or slower
            else:
                lo = mid + 1                 # too slow: must eat faster
        return lo


def brute_force(piles: List[int], h: int) -> int:
    k = 1
    while True:
        if sum((p + k - 1) // k for p in piles) <= h:
            return k
        k += 1


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
        ([1], 1, 1),
        ([5, 5, 5], 3, 5),
    ]
    for piles, h, want in cases:
        assert s.minEatingSpeed(piles, h) == want
        assert brute_force(piles, h) == want
    print("ok")
