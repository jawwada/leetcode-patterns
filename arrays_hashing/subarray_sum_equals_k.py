"""
Subarray Sum Equals K (LeetCode 560)  — Medium
Pattern: Prefix sum + hash map of counts

Problem
-------
Given an integer array nums (may contain negatives and zeros) and an integer k, return
the number of contiguous subarrays whose elements sum to k.
Example: nums = [1, 1, 1], k = 2 -> 2 (the subarrays [1,1] at 0..1 and 1..2).

Brute force
-----------
For every start i, extend an end j to the right while accumulating the running sum,
and count each time it equals k. O(n^2) time, O(1) space. (The triple loop that
re-sums each subarray is O(n^3) and strictly worse.) The repeated work is the
accumulation itself: the sum of nums[i..j] is recomputed for every i even though it
equals prefix[j+1] - prefix[i], two numbers we could have precomputed once.

From brute force to optimal
---------------------------
Rewrite the condition sum(i..j) == k as prefix[j+1] - prefix[i] == k, i.e.
prefix[i] == prefix[j+1] - k. For a fixed right end j, the question becomes "how many
earlier prefix sums equal exactly this value?" — a count lookup, which a hash map
answers in O(1). Sweep j left to right, maintain running prefix sum, and a dict
count-of-prefix-sums seen so far (seeded with {0: 1} for the empty prefix). Each step
adds counts[prefix - k] to the answer, then records the current prefix. Sliding
window does NOT work here because negatives break monotonicity; the hash map does
not need monotonicity.

Intuition
---------
Every subarray is a difference of two prefix sums. Counting subarrays with sum k is
counting pairs of prefix sums that differ by exactly k, and pairs with a fixed
difference are counted in one pass with a frequency map of values seen so far.

Geometric view
--------------
Plot the prefix sum as a staircase over positions 0..n. A subarray summing to k is a
pair of points on this staircase exactly k apart vertically with the left one earlier.
Walking right along the staircase, at each point look down by k and count how many
earlier points sit at that height.

Steps
-----
1. counts = {0: 1}; prefix = 0; answer = 0.
2. For each value v: prefix += v.
3. answer += counts.get(prefix - k, 0).
4. counts[prefix] = counts.get(prefix, 0) + 1.
5. Return answer.

Complexity: O(n) time, O(n) space — one pass; the dict holds at most n + 1 distinct
prefix sums.
Pitfalls: forgetting to seed counts[0] = 1 (misses subarrays starting at index 0);
updating counts BEFORE querying (counts the empty subarray when k == 0); trying a
sliding window with negative numbers.
"""
from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        counts = {0: 1}  # prefix sum -> how many times seen; empty prefix counts once
        prefix = 0
        answer = 0
        for v in nums:
            prefix += v
            answer += counts.get(prefix - k, 0)  # earlier prefixes that make a k-sum
            counts[prefix] = counts.get(prefix, 0) + 1
        return answer


def brute_force(nums: List[int], k: int) -> int:
    n = len(nums)
    answer = 0
    for i in range(n):
        running = 0
        for j in range(i, n):
            running += nums[j]
            if running == k:
                answer += 1
    return answer


if __name__ == "__main__":
    s = Solution()
    assert s.subarraySum([1, 1, 1], 2) == 2
    assert s.subarraySum([1, 2, 3], 3) == 2
    assert s.subarraySum([1, -1, 0], 0) == 3
    assert s.subarraySum([0, 0, 0, 0], 0) == 10
    assert s.subarraySum([-1, -1, 1], 0) == 1
    for nums, k in [([1, 1, 1], 2), ([1, 2, 3], 3), ([1, -1, 0], 0), ([0, 0, 0, 0], 0), ([-1, -1, 1], 0)]:
        assert s.subarraySum(nums, k) == brute_force(nums, k)
    print("ok")
