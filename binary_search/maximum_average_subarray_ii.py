"""
Maximum Average Subarray II (LeetCode 644)  — Hard
Pattern: Binary search on the answer

Problem
-------
Given an integer array `nums` and an integer `k`, find a contiguous subarray of length AT LEAST
k that has the maximum average value, and return that average (any answer within 1e-5 of the
true value is accepted).
Example: nums = [1,12,-5,-6,50,3], k = 4 -> 12.75  (subarray [12,-5,-6,50], average 51/4).

Brute force
-----------
Enumerate every start i, extend the end j to the right keeping a running sum, and whenever the
length j-i+1 >= k update best = max(best, sum / length). O(n^2) time, O(1) space. The waste:
there are Theta(n^2) subarrays and we evaluate every one, even though we only need to know
whether SOME subarray beats a threshold — a question that can be answered in one linear pass.

From brute force to optimal
---------------------------
The redundancy is computing the exact average of every subarray. Reframe as a decision problem:
"is there a subarray of length >= k with average >= x?" That predicate is monotone in x (if some
subarray averages >= x it also averages >= any smaller x), so the real answer is the boundary
of an F...FT...T sequence over the real line and binary search finds it to 1e-5 precision in
~35 probes. Each probe must be fast: average >= x  <=>  sum(nums[i] - x) >= 0 over the
subarray. Shift every element by -x, take prefix sums P, and the question becomes "is there
j - i >= k with P[j] - P[i] >= 0", i.e. "is P[j] >= min(P[0..j-k]) for some j". Carrying the
running minimum of the prefixes that are at least k behind answers it in O(n).

Intuition
---------
Subtracting the candidate average x from every element turns "average >= x" into "sum >= 0",
and "maximum sum subarray of length >= k" is a one-pass prefix-minimum scan (Kadane with a
delay of k). Wrap that O(n) yes/no check in a binary search over x between min(nums) and
max(nums) and the exact search over Theta(n^2) subarrays disappears.

Geometric view
--------------
Picture the real line from min(nums) to max(nums); every x is painted T if some long-enough
subarray averages at least x, F otherwise. The paint is a solid T block followed by a solid F
block, and lo/hi squeeze onto the T|F boundary. Inside each probe, picture the prefix-sum
curve of (nums[i] - x): the probe succeeds iff some point of the curve sits at or above a point
of the curve at least k steps to its left.

Steps
-----
1. lo = min(nums), hi = max(nums).
2. can(x): P[0] = 0, P[j] = P[j-1] + nums[j-1] - x; sweep j from k to n keeping
   min_prefix = min(P[0..j-k]); return True if any P[j] - min_prefix >= 0.
3. While hi - lo > 1e-6: mid = (lo+hi)/2; if can(mid): lo = mid else hi = mid.
4. Return lo.

Complexity: O(n log(R / eps)) time where R = max - min, O(n) space — ~35 probes of O(n) each.
Pitfalls: forgetting the "length >= k" constraint when taking the prefix minimum (the minimum
must lag by k); using the floor/ceil integer binary-search template on a real-valued answer;
subtracting x from the sum but not from the length (sum - x * len is the same thing).
"""
import random
from typing import List


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        def can(x: float) -> bool:
            # exists subarray of length >= k with average >= x
            # <=> exists j - i >= k with P[j] - P[i] >= 0 for P = prefix sums of (v - x)
            prefix = [0.0]
            for v in nums:
                prefix.append(prefix[-1] + v - x)
            min_prefix = 0.0                          # min of P[0..j-k]
            for j in range(k, len(nums) + 1):
                min_prefix = min(min_prefix, prefix[j - k])
                if prefix[j] - min_prefix >= 0:
                    return True
            return False

        lo, hi = float(min(nums)), float(max(nums))   # answer lies in [min, max]
        while hi - lo > 1e-6:                         # shrink to the T|F boundary
            mid = (lo + hi) / 2
            if can(mid):
                lo = mid                              # mid is achievable: look higher
            else:
                hi = mid                              # nobody reaches mid: look lower
        return lo


def brute_force(nums: List[int], k: int) -> float:
    best = float("-inf")
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):               # every subarray starting at i
            total += nums[j]
            if j - i + 1 >= k:
                best = max(best, total / (j - i + 1))
    return best


if __name__ == "__main__":
    s = Solution()
    assert abs(s.findMaxAverage([1, 12, -5, -6, 50, 3], 4) - 12.75) < 1e-5
    assert abs(s.findMaxAverage([5], 1) - 5.0) < 1e-5
    assert abs(s.findMaxAverage([-1, -2, -3], 2) - (-1.5)) < 1e-5     # all negative
    assert abs(s.findMaxAverage([4, 4, 4, 4], 2) - 4.0) < 1e-5        # constant array
    rng = random.Random(644)
    for _ in range(200):
        n = rng.randint(1, 12)
        nums = [rng.randint(-20, 20) for _ in range(n)]
        k = rng.randint(1, n)
        assert abs(s.findMaxAverage(nums, k) - brute_force(nums, k)) < 1e-5, (nums, k)
    print("ok")
