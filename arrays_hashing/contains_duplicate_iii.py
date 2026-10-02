"""
Contains Duplicate III (LeetCode 220)  — Hard
Pattern: Sliding window of value buckets (width t + 1)

Problem
-------
Given an integer array nums and two integers indexDiff (k) and valueDiff (t), return True if
there exist two distinct indices i, j with |i - j| <= k and |nums[i] - nums[j]| <= t.
Example: nums = [1,2,3,1], k = 3, t = 0 -> True (nums[0] and nums[3] are equal, 3 apart).
nums = [1,5,9,1,5,9], k = 2, t = 3 -> False.

Brute force
-----------
For each i, compare nums[i] with each of the next k elements. O(n k) time, O(1) space. The
waste is that the k comparisons per index re-examine the same window contents: the window
for i + 1 differs from the window for i by one element, but we know nothing about the window's
values between steps and so must re-scan it.

From brute force to optimal
---------------------------
Step 1 (O(n k) -> O(n log k)): keep the last k values in a sorted container; for each new x
the only candidates are its predecessor and successor in that order (anything farther is at
least as far in value). Python has no balanced BST, so this needs bisect on a list (O(k)
insert) or a sorted-list library. Step 2 (O(n log k) -> O(n)): instead of exact order, use
value buckets of width t + 1: bucket(x) = x // (t + 1). Two values in the same bucket differ
by at most t, so a bucket collision is an immediate True. Two values with |a - b| <= t are
otherwise in adjacent buckets, so only buckets b - 1 and b + 1 need an explicit check. Keep
the buckets of the last k indices in a dict; because any bucket with two residents would have
returned True already, each bucket holds exactly one value and eviction is a single delete.

Intuition
---------
"Within t in value" is the hard part; "within k in index" is just a sliding window. Buckets of
width t + 1 turn the value test into a hashing problem: close values either share a bucket
(certainly within t) or sit in neighbouring buckets (maybe within t, so check the one value
there). It is the same pigeonhole trick as bucket sort, applied to a window rather than the
whole array.

Geometric view
--------------
Draw the number line divided into cells of width t + 1, and a time window of the last k
indices sliding over the array. Each value currently in the window lights up one cell. A new
value whose cell is already lit is a hit; otherwise look only at the two cells beside it.
When the window moves on, the departed value's cell goes dark.

Steps
-----
1. width = t + 1; buckets = {} mapping bucket id -> the one value living there.
2. For each index i with value x: b = x // width.
3.   If b in buckets: return True.
4.   For nb in (b - 1, b + 1): if nb in buckets and |buckets[nb] - x| <= t: return True.
5.   buckets[b] = x; if i >= k: delete the bucket of nums[i - k].
6. Return False.

Complexity: O(n) time, O(min(n, k)) space — each index does O(1) dict operations.
Pitfalls: width t instead of t + 1 divides by zero when t = 0 (t + 1 is the widest width
where a shared bucket still guarantees |a - b| <= t, and it works for every t >= 0); using int(x / width) instead of floor division for negatives; evicting nums[i - k]
one step too early or too late (the window must hold exactly k previous indices); k = 0 means
no valid pair.
"""
from typing import List


class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], indexDiff: int, valueDiff: int) -> bool:
        width = valueDiff + 1            # same bucket => |a - b| <= valueDiff
        buckets = {}                     # bucket id -> the single value in it
        for i, x in enumerate(nums):
            b = x // width               # floor division keeps negatives correct
            if b in buckets:
                return True
            for nb in (b - 1, b + 1):    # close values can only be in adjacent buckets
                if nb in buckets and abs(buckets[nb] - x) <= valueDiff:
                    return True
            buckets[b] = x
            if i >= indexDiff:           # keep only the last indexDiff indices
                del buckets[nums[i - indexDiff] // width]
        return False


def brute_force(nums: List[int], indexDiff: int, valueDiff: int) -> bool:
    for i in range(len(nums)):
        for j in range(i + 1, min(i + indexDiff, len(nums) - 1) + 1):
            if abs(nums[i] - nums[j]) <= valueDiff:
                return True
    return False


if __name__ == "__main__":
    s = Solution()
    assert s.containsNearbyAlmostDuplicate([1, 2, 3, 1], 3, 0) is True
    assert s.containsNearbyAlmostDuplicate([1, 5, 9, 1, 5, 9], 2, 3) is False
    assert s.containsNearbyAlmostDuplicate([1, 0, 1, 1], 1, 2) is True
    assert s.containsNearbyAlmostDuplicate([-3, 3], 2, 4) is False
    assert s.containsNearbyAlmostDuplicate([-3, 3], 2, 6) is True
    assert s.containsNearbyAlmostDuplicate([7], 1, 0) is False
    import random
    random.seed(220)
    for _ in range(400):
        nums = [random.randint(-10, 10) for _ in range(random.randint(1, 12))]
        k, t = random.randint(1, 6), random.randint(0, 5)
        assert s.containsNearbyAlmostDuplicate(nums, k, t) == brute_force(nums, k, t)
    print("ok")
