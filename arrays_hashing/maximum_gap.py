"""
Maximum Gap (LeetCode 164)  — Hard
Pattern: Pigeonhole buckets (bucket sort without sorting)

Problem
-------
Given an unsorted integer array nums, return the maximum difference between two successive
elements in its sorted form, in linear time and linear extra space. Return 0 if the array has
fewer than two elements.
Example: nums = [3,6,9,1] -> 3 (sorted: 1,3,6,9; gaps 2,3,3).

Brute force
-----------
Sort the array and take the maximum adjacent difference. O(n log n) time, O(1) or O(n)
space depending on the sort. It is correct and what you should say first; the "waste" is
that sorting determines the full order of all n elements when we only need one number — the
largest gap — and the problem demands O(n).

From brute force to optimal
---------------------------
Let lo, hi be the min and max. The n - 1 sorted gaps sum to hi - lo, so the maximum gap is at
least the average, g = ceil((hi - lo) / (n - 1)). Partition [lo, hi] into buckets of width
w = max(1, floor((hi - lo) / (n - 1))) <= g. Two elements inside the same bucket differ by at
most w - 1 < g, so they can never form the maximum gap: the answer is always between the
largest value of one non-empty bucket and the smallest value of the next non-empty bucket.
We therefore need only each bucket's min and max, filled in one O(n) pass, and a second pass
over the buckets in order. There are at most n buckets, so time and space are O(n).

Intuition
---------
By pigeonhole, if n numbers spread across a range, at least one gap is at least the average
gap. Make the buckets narrower than that average and no two numbers in the same bucket can
be the extreme pair. The buckets impose "enough" order — which bucket comes before which —
without sorting inside them, and the inter-bucket boundaries are exactly where the big gap
hides.

Geometric view
--------------
Draw the number line from lo to hi divided into equal cells of width w. Drop each number into
its cell and keep only the leftmost and rightmost mark in each cell. Then walk the cells left
to right; the gap from one cell's rightmost mark to the next non-empty cell's leftmost mark
spans the empty cells in between. The widest such span is the answer.

Steps
-----
1. If n < 2 return 0; lo, hi = min, max; if lo == hi return 0.
2. width = max(1, (hi - lo) // (n - 1)); buckets = (hi - lo) // width + 1.
3. For each x: b = (x - lo) // width; update bucket_min[b], bucket_max[b].
4. prev = lo; for each non-empty bucket in order: best = max(best, bucket_min[b] - prev);
   prev = bucket_max[b].
5. Return best.

Complexity: O(n) time, O(n) space — one pass to fill at most n buckets, one pass to scan them.
Pitfalls: bucket width larger than the average gap (then two in-bucket elements could be the
answer); a zero width when hi - lo < n - 1 (clamp to 1); forgetting empty buckets while
scanning (skip them but keep prev); all-equal input.
"""
from typing import List


class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 2:
            return 0
        lo, hi = min(nums), max(nums)
        if lo == hi:
            return 0
        # width <= ceil((hi - lo) / (n - 1)) <= max gap, so the max gap
        # cannot be between two values in the same bucket
        width = max(1, (hi - lo) // (n - 1))
        count = (hi - lo) // width + 1
        bucket_min = [None] * count
        bucket_max = [None] * count
        for x in nums:
            b = (x - lo) // width
            bucket_min[b] = x if bucket_min[b] is None else min(bucket_min[b], x)
            bucket_max[b] = x if bucket_max[b] is None else max(bucket_max[b], x)
        best, prev_max = 0, lo
        for b in range(count):
            if bucket_min[b] is None:
                continue                 # empty bucket: the gap spans it
            best = max(best, bucket_min[b] - prev_max)
            prev_max = bucket_max[b]
        return best


def brute_force(nums: List[int]) -> int:
    ordered = sorted(nums)
    best = 0
    for a, b in zip(ordered, ordered[1:]):
        best = max(best, b - a)
    return best


if __name__ == "__main__":
    s = Solution()
    assert s.maximumGap([3, 6, 9, 1]) == 3
    assert s.maximumGap([10]) == 0
    assert s.maximumGap([1, 1, 1, 1]) == 0
    assert s.maximumGap([1, 10000000]) == 9999999
    assert s.maximumGap([1, 3, 100]) == 97
    import random
    random.seed(164)
    for _ in range(300):
        n = random.randint(0, 12)
        nums = [random.randint(0, random.choice([5, 50, 10 ** 6])) for _ in range(n)]
        assert s.maximumGap(nums) == brute_force(nums)
    print("ok")
