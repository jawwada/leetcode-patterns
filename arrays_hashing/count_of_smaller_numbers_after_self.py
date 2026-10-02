"""
Count of Smaller Numbers After Self (LeetCode 315)  — Hard
Pattern: Merge sort counting

Problem
-------
Given an integer array nums, return an array counts where counts[i] is the number of
elements to the right of i that are strictly smaller than nums[i].
Example: nums = [5,2,6,1] -> [2,1,1,0] (right of 5: 2 and 1 are smaller; right of 2: 1;
right of 6: 1; right of 1: nothing).

Brute force
-----------
For each i, scan every j > i and count nums[j] < nums[i]. O(n^2) time, O(1) extra space.
The wasted work is comparing every pair individually: once we know the suffix nums[i+1:]
in sorted order, the count for i is a single rank query, yet the brute force rediscovers
that order one comparison at a time for every i.

From brute force to optimal
---------------------------
The count for i depends only on how nums[i] ranks among the elements to its right. Merge
sort builds exactly that information bottom-up. Sort indices (not values) so that each
element keeps its identity. When merging a sorted left half with a sorted right half, every
element in the right half has a larger original index than every element in the left half.
At the moment a left element is emitted, all right-half elements already emitted are
strictly smaller than it and lie to its right in the original array, so add their number
(j - mid) to its count. Ties are handled by emitting the left element first when values are
equal, so equal elements are not counted. Each merge level is O(n) and there are log n
levels, so O(n log n). Alternative with the same bound: scan from the right and query a
Binary Indexed Tree over compressed values ("how many inserted values are < nums[i]").

Intuition
---------
"Smaller and to the right" is an inversion count per element. Merge sort is the natural
inversion counter because the merge step compares two sorted runs where every element of
one run precedes every element of the other in index order — the position relation is fixed,
so the value comparison is all that remains. The counts accumulate across levels without any
pair ever being compared twice.

Geometric view
--------------
Picture the index array being split into halves down to singletons and merged back up. At
each merge, two sorted rails are zipped together; a pointer j walks the right rail. Whenever
the left rail's head is emitted, the j right-rail items already passed form a block of
strictly smaller, later-indexed elements, and that block's size is stamped onto the left
head's original position.

Steps
-----
1. idx = [0..n-1], counts = [0]*n; sort idx by nums with a hand-written merge sort.
2. In merge(lo, mid, hi): i = lo, j = mid.
3.   While both halves remain: if nums[idx[j]] < nums[idx[i]] emit idx[j], j += 1;
     else counts[idx[i]] += j - mid, emit idx[i], i += 1.
4.   Flush the left remainder, adding j - mid to each; flush the right remainder.
5.   Write the merged order back into idx[lo:hi].
6. Return counts.

Complexity: O(n log n) time, O(n) space — log n merge levels, each O(n), plus the index/merge buffers.
Pitfalls: sorting values instead of indices (you lose where each count belongs); counting
equal elements as smaller (take the left element first on ties); forgetting to add j - mid
to the left remainder after the right half is exhausted.
"""
from typing import List


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        n = len(nums)
        counts = [0] * n
        idx = list(range(n))             # sort indices so each element keeps its identity

        def sort(lo: int, hi: int) -> None:
            if hi - lo <= 1:
                return
            mid = (lo + hi) // 2
            sort(lo, mid)
            sort(mid, hi)
            merged = []
            i, j = lo, mid
            while i < mid and j < hi:
                if nums[idx[j]] < nums[idx[i]]:
                    merged.append(idx[j])
                    j += 1
                else:
                    # the j - mid right-half elements already emitted are smaller
                    # and come after idx[i] in the original order
                    counts[idx[i]] += j - mid
                    merged.append(idx[i])
                    i += 1
            while i < mid:
                counts[idx[i]] += j - mid
                merged.append(idx[i])
                i += 1
            merged.extend(idx[j:hi])
            idx[lo:hi] = merged

        sort(0, n)
        return counts


def brute_force(nums: List[int]) -> List[int]:
    counts = []
    for i in range(len(nums)):
        smaller = 0
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[i]:
                smaller += 1
        counts.append(smaller)
    return counts


if __name__ == "__main__":
    s = Solution()
    assert s.countSmaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert s.countSmaller([-1]) == [0]
    assert s.countSmaller([-1, -1]) == [0, 0]
    assert s.countSmaller([]) == []
    assert s.countSmaller([3, 3, 2, 1]) == [2, 2, 1, 0]
    import random
    random.seed(315)
    for _ in range(300):
        nums = [random.randint(-6, 6) for _ in range(random.randint(0, 15))]
        assert s.countSmaller(nums) == brute_force(nums)
    print("ok")
