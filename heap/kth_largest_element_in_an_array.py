"""
Kth Largest Element in an Array (LeetCode 215)  — Medium
Pattern: Quickselect (partition, recurse one side)

Problem
-------
Given an integer array nums and k, return the k-th largest element in sorted order (duplicates
count), without fully sorting.
Example: nums=[3,2,1,5,6,4], k=2 -> 5.  nums=[3,2,3,1,2,4,5,5,6], k=4 -> 4.

Brute force
-----------
Sort the array descending and return nums[k-1]. O(n log n) time, O(1) extra (in-place sort).
The waste: a full sort establishes the order of every pair of elements, but we only need to know
which single element lands at position k-1; the order within the left part and within the right
part is thrown away.

From brute force to optimal
---------------------------
The redundancy is sorting both halves of every partition when only one half can contain the
answer. Observation: one Lomuto/Hoare partition around a pivot puts the pivot at its final sorted
index p and tells us, in O(n), whether the target index is left of p, right of p, or equal to p.
So we can discard the other side entirely and recurse on one side only, shrinking the work
geometrically: n + n/2 + n/4 + ... = O(n) on average. (Heap alternative: a size-k min-heap gives
O(n log k) deterministically and is the right call for a stream; quickselect needs the whole
array in memory but is faster for one-off queries.)

Intuition
---------
Quicksort, but only follow the side that contains the index you care about. Target index for
"k-th largest" in ascending order is n - k. A random pivot keeps the expected depth O(log n)
and defeats adversarial inputs (sorted arrays would otherwise go O(n^2)).

Geometric view
--------------
The array is a shelf; each partition pass drops a pivot at its true slot and splits the shelf
into [smaller | pivot | larger]. The target slot n-k is marked; we keep only the segment that
contains the mark, so the live segment halves on average each round and eventually becomes a
single slot.

Steps
-----
1. target = n - k (index in ascending order).
2. While lo < hi: pick a random pivot, swap it to the end, partition so [lo..p-1] < pivot <= [p+1..hi].
3. If p == target return nums[p]; if p < target set lo = p + 1; else hi = p - 1.
4. When lo == hi, nums[lo] is the answer.

Complexity: O(n) average time (O(n^2) worst, mitigated by random pivot), O(1) space — iterative,
in place.
Pitfalls: Off-by-one on target (n-k, not k); not randomising the pivot; infinite loop if the
partition does not place the pivot at index p (it must be swapped into position after the scan).
"""
import random
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        target = len(nums) - k                    # index in ascending order
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            p = self._partition(nums, lo, hi)
            if p == target:
                return nums[p]
            if p < target:
                lo = p + 1                        # answer lies in the larger half
            else:
                hi = p - 1                        # answer lies in the smaller half
        return nums[lo]

    @staticmethod
    def _partition(nums: List[int], lo: int, hi: int) -> int:
        pivot_idx = random.randint(lo, hi)
        nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]
        pivot = nums[hi]
        store = lo                                # everything before store is < pivot
        for i in range(lo, hi):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]   # pivot lands at its final index
        return store


def brute_force(nums: List[int], k: int) -> int:
    return sorted(nums, reverse=True)[k - 1]   # full O(n log n) sort for one position


if __name__ == "__main__":
    s = Solution()
    assert s.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    assert s.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert s.findKthLargest([1], 1) == 1                       # single element
    assert s.findKthLargest([2, 2, 2, 2], 3) == 2              # all duplicates
    for _ in range(200):                                       # random cross-check vs brute force
        arr = [random.randint(-50, 50) for _ in range(random.randint(1, 30))]
        kk = random.randint(1, len(arr))
        assert s.findKthLargest(arr[:], kk) == brute_force(arr, kk)
    print("ok")
