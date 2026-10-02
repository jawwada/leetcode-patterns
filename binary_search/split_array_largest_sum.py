"""
Split Array Largest Sum (LeetCode 410)  — Hard
Pattern: Binary search on the answer

Problem
-------
Split the array nums into k non-empty contiguous subarrays so that the largest subarray sum is as
small as possible; return that minimised largest sum.
Example: nums = [7,2,5,10,8], k = 2 -> 18 (split [7,2,5] | [10,8]).
nums = [1,2,3,4,5], k = 2 -> 9 ([1,2,3] | [4,5]).

Brute force
-----------
Enumerate every placement of k-1 cut points among the n-1 gaps (itertools.combinations), compute
the k piece sums for each, and keep the smallest maximum. C(n-1, k-1) placements, each costing
O(n), so exponential in general (O(n^k)); O(k) space per placement. The wasted work: almost every
placement is hopeless and we evaluate it anyway, and placements that share a prefix of cuts
re-sum the same pieces again and again.

From brute force to optimal
---------------------------
Instead of searching over placements, search over the ANSWER. The feasibility predicate
"can the array be split into at most k pieces with every piece sum <= cap?" is monotone: if cap
works, every larger cap works. And it is easy to decide greedily: scan left to right, keep adding
to the current piece while the sum stays <= cap, cut when it would exceed, and count the pieces.
Fewest pieces for a given cap is what greedy produces, so pieces(cap) <= k iff cap is feasible.
The answer lies in [max(nums), sum(nums)]; binary search on that range with the O(n) greedy check
gives O(n log(sum)). No DP table is needed: the structure of the problem (monotone predicate +
greedy decision) is the whole optimisation.

Intuition
---------
Flip the question. "Minimise the largest piece" is hard to construct directly, but "could every
piece fit under a budget cap?" is a yes/no question with an obvious greedy answer: pack greedily
and count pieces. Yes/no answers over a monotone range are found by binary search.

Geometric view
--------------
Picture the array as bars laid side by side and cap as a horizontal water line. Pour from the
left: start a new bucket whenever the running sum would spill over the line. Fewer buckets as
the line rises. Binary search raises or lowers the line until exactly k buckets suffice and one
unit lower does not.

Steps
-----
1. lo = max(nums) (every element must fit), hi = sum(nums) (one piece).
2. pieces(cap): count = 1, cur = 0; for x: if cur + x > cap: count += 1, cur = 0; cur += x.
3. While lo < hi: mid = (lo + hi) // 2; if pieces(mid) <= k: hi = mid else lo = mid + 1.
4. Return lo.

Complexity: O(n log S) time with S = sum(nums), O(1) space — ~log S feasibility scans of O(n).
Pitfalls: starting lo at 0 instead of max(nums) (greedy then produces pieces that still exceed
          cap); using pieces(mid) == k instead of <= k (fewer pieces can always be split further);
          an off-by-one in the search that returns an infeasible cap.
"""
from itertools import combinations
from typing import List


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def pieces_needed(cap: int) -> int:
            """Greedy: fewest pieces with every piece sum <= cap."""
            count, cur = 1, 0
            for x in nums:
                if cur + x > cap:          # would spill over: start a new piece
                    count += 1
                    cur = 0
                cur += x
            return count

        lo, hi = max(nums), sum(nums)      # feasible answers live in [lo, hi]
        while lo < hi:
            mid = (lo + hi) // 2
            if pieces_needed(mid) <= k:    # mid works -> try smaller
                hi = mid
            else:
                lo = mid + 1
        return lo


def brute_force(nums: List[int], k: int) -> int:
    """Try every placement of k-1 cuts (exponential), keep the smallest largest piece."""
    n = len(nums)
    best = float("inf")
    for cuts in combinations(range(1, n), k - 1):
        bounds = (0, *cuts, n)
        largest = max(sum(nums[a:b]) for a, b in zip(bounds, bounds[1:]))
        best = min(best, largest)
    return best


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([7, 2, 5, 10, 8], 2, 18),
        ([1, 2, 3, 4, 5], 2, 9),
        ([1, 4, 4], 3, 4),
        ([5], 1, 5),                  # edge: single element
        ([2, 3, 1, 2, 4, 3], 6, 4),   # edge: k == n -> max element
    ]
    for nums, k, want in cases:
        assert s.splitArray(nums, k) == want, (nums, k)
        assert brute_force(nums, k) == want, (nums, k)

    random.seed(410)
    for _ in range(300):
        nums = [random.randint(0, 20) for _ in range(random.randint(1, 9))]
        k = random.randint(1, len(nums))
        assert s.splitArray(nums, k) == brute_force(nums, k), (nums, k)
    print("ok")
