"""
Subarrays with K Different Integers (LeetCode 992)  — Hard
Pattern: Exactly-K = atMost(K) - atMost(K-1) sliding window

Problem
-------
Given an integer array nums and an integer k, count the contiguous subarrays whose number
of distinct values is exactly k.
Example: nums = [1,2,1,2,3], k = 2 -> 7 ([1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2],
[1,2,1,2]).

Brute force
-----------
For every start i, extend j to the right while maintaining a set of the values seen; count
the subarray when the set has exactly k elements and stop once it exceeds k. O(n^2) time,
O(k) space. The wasted work is rebuilding the set from scratch for each start: the window
starting at i+1 shares all but one element with the one starting at i.

From brute force to optimal
---------------------------
A sliding window needs a monotone predicate: "at most k distinct" is monotone (shrinking a
window never adds distinct values), but "exactly k distinct" is not — a window may have
exactly k, a longer one k+1, and a still longer one... still k+1, so there is no single
left boundary to track. The fix is to count a monotone quantity and subtract:
exactly(k) = atMost(k) - atMost(k-1). atMost(k) is a textbook window: for each right end r,
advance l until the window has <= k distinct values; every window ending at r with start in
[l, r] qualifies, contributing r - l + 1. Two linear passes give the answer with no set
rebuilding; each index enters and leaves each window once.

Intuition
---------
Counting windows with "at most k" is easy because the valid starts for a fixed right end form
one contiguous range [l, r]. "Exactly k" is the thin band between "at most k" and "at most
k-1": every exactly-k window is an at-most-k window that is not an at-most-(k-1) window, so
the difference of the two counts is exactly what we want.

Geometric view
--------------
For each right edge r, picture a bar from l to r: the set of valid starts. For atMost(k)
that bar is the longest suffix with <= k distinct values; for atMost(k-1) it is a shorter
suffix nested inside it. The exactly-k windows ending at r are the starts between the two
left edges — the piece of the long bar that sticks out past the short bar.

Steps
-----
1. Define at_most(k): l = 0, counts = {}, total = 0.
2.   For each r: counts[nums[r]] += 1; while len(counts) > k: decrement counts[nums[l]],
     delete it when it hits 0, l += 1.
3.   total += r - l + 1 (every start in [l, r] is valid).
4. Return at_most(k) - at_most(k - 1).

Complexity: O(n) time, O(k) space — two passes, each pointer moves at most n steps per pass.
Pitfalls: trying to slide an "exactly k" window directly; forgetting to delete zero-count
keys so len(counts) over-reports distinct values; adding 1 instead of r - l + 1 per step.
"""
from collections import defaultdict
from typing import List


class Solution:
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        def at_most(limit: int) -> int:
            counts = defaultdict(int)
            left = total = 0
            for right, x in enumerate(nums):
                counts[x] += 1
                while len(counts) > limit:
                    y = nums[left]
                    counts[y] -= 1
                    if counts[y] == 0:
                        del counts[y]
                    left += 1
                total += right - left + 1   # every start in [left, right] works
            return total

        return at_most(k) - at_most(k - 1)


def brute_force(nums: List[int], k: int) -> int:
    count = 0
    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            if len(seen) > k:
                break
            if len(seen) == k:
                count += 1
    return count


if __name__ == "__main__":
    s = Solution()
    assert s.subarraysWithKDistinct([1, 2, 1, 2, 3], 2) == 7
    assert s.subarraysWithKDistinct([1, 2, 1, 3, 4], 3) == 3
    assert s.subarraysWithKDistinct([1, 1, 1], 1) == 6
    assert s.subarraysWithKDistinct([1, 2, 3], 4) == 0
    import random
    random.seed(992)
    cases = [([1, 2, 1, 2, 3], 2), ([1, 2, 1, 3, 4], 3), ([1, 1, 1], 1)]
    for _ in range(200):
        n = random.randint(1, 12)
        cases.append(([random.randint(1, 5) for _ in range(n)], random.randint(1, 5)))
    for nums, k in cases:
        assert s.subarraysWithKDistinct(nums, k) == brute_force(nums, k)
    print("ok")
