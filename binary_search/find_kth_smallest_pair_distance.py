"""
Find K-th Smallest Pair Distance (LeetCode 719)  — Hard
Pattern: Binary search on the answer + two-pointer counting

Problem
-------
The distance of a pair (i, j), i < j, is |nums[i] - nums[j]|. Return the k-th smallest distance
among all n(n-1)/2 pairs.
Example: nums = [1,3,1], k = 1 -> 0  (distances 2, 0, 2; sorted 0,2,2; the 1st is 0).
Example: nums = [1,6,1], k = 3 -> 5.

Brute force
-----------
Generate all n(n-1)/2 pair distances, sort them, return index k-1. O(n^2 log n) time, O(n^2)
space — n = 10^4 gives 5*10^7 distances. The waste: we materialise and fully sort every
distance although we only need to know how many fall at or below a threshold.

From brute force to optimal
---------------------------
Step 1 (sort the data, not the pairs): after sorting nums, "how many pairs have distance <= d?"
is answerable in O(n) with two pointers: for each right end r, advance l while
nums[r] - nums[l] > d; every l..r-1 pairs with r, so count += r - l. l never moves backwards, so
the pass is linear. Step 2 (search the answer): count(d) is monotone non-decreasing in d, and
the k-th smallest distance is exactly the smallest d with count(d) >= k. Distances are integers
in [0, max - min], so binary search over that range costs log(range) O(n) probes, replacing the
O(n^2) enumeration entirely.

Intuition
---------
"K-th smallest of an implicit multiset" is a binary-search-on-value problem whenever you can
count elements <= v quickly. Sorting makes the pairs with small distance cluster together
(close in index), which is what lets a sliding window count them without listing them.

Geometric view
--------------
Draw the sorted values on a number line. For a threshold d, slide a window [l, r] whose span
nums[r] - nums[l] stays <= d: each time r steps right, l catches up until the span fits, and the
r - l elements inside pair with r. Over d on another line, count(d) rises in steps; paint
count(d) >= k as F...FT...T and binary search the first T.

Steps
-----
1. Sort nums; lo = 0, hi = nums[-1] - nums[0].
2. count(d): l = 0; for r in range(n): while nums[r] - nums[l] > d: l += 1; total += r - l.
3. While lo < hi: mid = (lo+hi)//2; if count(mid) >= k: hi = mid else lo = mid + 1.
4. Return lo.

Complexity: O(n log n + n log R) time where R = max - min, O(1) extra space (sort in place).
Pitfalls: counting pairs with distance < d instead of <= d (off-by-one shifts the answer); using
a heap of size k (O(n^2 log k), too slow); forgetting that lo = 0 must be allowed (duplicates
give distance 0).
"""
import random
from typing import List


class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        nums.sort()

        def count(d: int) -> int:                # pairs with distance <= d
            total = l = 0
            for r in range(len(nums)):
                while nums[r] - nums[l] > d:     # shrink until the window spans <= d
                    l += 1
                total += r - l                   # every index in [l, r) pairs with r
            return total

        lo, hi = 0, nums[-1] - nums[0]           # answer is an integer in this range
        while lo < hi:                           # first d with count(d) >= k
            mid = (lo + hi) // 2
            if count(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo


def brute_force(nums: List[int], k: int) -> int:
    dists = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):        # every pair, materialised
            dists.append(abs(nums[i] - nums[j]))
    dists.sort()
    return dists[k - 1]


if __name__ == "__main__":
    s = Solution()
    assert s.smallestDistancePair([1, 3, 1], 1) == 0
    assert s.smallestDistancePair([1, 1, 1], 2) == 0
    assert s.smallestDistancePair([1, 6, 1], 3) == 5
    assert s.smallestDistancePair([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18) == 2
    assert s.smallestDistancePair([1, 100], 1) == 99          # single pair
    rng = random.Random(719)
    for _ in range(200):
        n = rng.randint(2, 9)
        nums = [rng.randint(0, 20) for _ in range(n)]
        k = rng.randint(1, n * (n - 1) // 2)
        assert s.smallestDistancePair(list(nums), k) == brute_force(nums, k), (nums, k)
    print("ok")
