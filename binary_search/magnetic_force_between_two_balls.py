"""
Magnetic Force Between Two Balls (LeetCode 1552)  — Medium
Pattern: Binary search on the answer

Problem
-------
There are baskets at distinct integer positions. Place m balls in m different baskets so
that the minimum distance between any two balls is as large as possible; return it.
Example: position = [1,2,3,4,7], m = 3 -> 3 (balls at 1, 4, 7).

Brute force
-----------
Sort the positions, then try every candidate gap d = 1, 2, ..., (max - min) and keep the
largest d for which a greedy left-to-right placement fits m balls. O(n log n + R * n) time
with R = max - min (up to 1e9), O(1) extra space. The waste: feasibility is monotone in d,
yet we test every d one by one instead of jumping.

From brute force to optimal
---------------------------
Two observations. (1) Checking a fixed d is easy greedily: put the first ball in the
leftmost basket and every next ball in the first basket at least d past the previous one;
placing a ball as early as possible never hurts later balls. (2) If gap d is achievable
then every smaller gap is too, so feasible(d) is True...True False...False over d. The
answer is the last True, and a monotone predicate can be searched by halving the range
[1, max - min]: O(n log R) checks instead of O(n R). This is the original solution's
approach.

Intuition
---------
Turn "maximise the minimum gap" into a yes/no question "can I keep every gap >= d?". The
yes/no question has a cheap greedy answer and a monotone shape, so binary search finds the
largest yes.

Geometric view
--------------
Picture baskets as dots on a number line. For a trial d, drop a ball on the leftmost dot,
then hop right to the first dot at least d away, and so on. Large d makes long hops and
runs out of line before m balls; small d fits easily. Binary search slides d to the exact
edge where the hops still fit.

Steps
-----
1. Sort positions. lo = 1, hi = pos[-1] - pos[0], ans = 1.
2. fits(d): count = 1, last = pos[0]; for p in pos: if p - last >= d: count += 1, last = p.
   Return count >= m.
3. While lo <= hi: mid = (lo + hi) // 2; if fits(mid): ans = mid, lo = mid + 1;
   else hi = mid - 1.
4. Return ans.

Complexity: O(n log n + n log R) time, O(n) space for the sorted copy — log R greedy checks.
Pitfalls: Forgetting to sort; binary searching over indices instead of distances; using
> d instead of >= d in the greedy check.
"""
from typing import List


class Solution:
    def maxDistance(self, position: List[int], m: int) -> int:
        pos = sorted(position)

        def fits(d: int) -> bool:          # greedy: drop each ball as early as allowed
            count, last = 1, pos[0]
            for p in pos[1:]:
                if p - last >= d:
                    count, last = count + 1, p
            return count >= m

        lo, hi, ans = 1, pos[-1] - pos[0], 1
        while lo <= hi:                    # find the last d where fits(d) is True
            mid = (lo + hi) // 2
            if fits(mid):
                ans, lo = mid, mid + 1
            else:
                hi = mid - 1
        return ans


def brute_force(position: List[int], m: int) -> int:
    pos = sorted(position)
    best = 1
    for d in range(1, pos[-1] - pos[0] + 1):   # tries every gap, one at a time
        count, last = 1, pos[0]
        for p in pos[1:]:
            if p - last >= d:
                count, last = count + 1, p
        if count >= m:
            best = d
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 2, 3, 4, 7], 3, 3), ([5, 4, 3, 2, 1, 1000000000], 2, 999999999),
             ([1, 2], 2, 1), ([1, 5, 9, 20], 4, 4), ([79, 74, 57, 22], 4, 5)]
    for pos, m, want in cases:
        assert s.maxDistance(pos, m) == want
        if max(pos) - min(pos) <= 1000:          # brute force is O(R * n)
            assert brute_force(pos, m) == want
    print("ok")
