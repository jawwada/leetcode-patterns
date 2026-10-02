"""
Reverse Pairs (LeetCode 493)  — Hard
Pattern: Merge sort counting

Problem
-------
Given an integer array nums, count the reverse pairs: index pairs i < j with
nums[i] > 2 * nums[j].
Example: nums = [1,3,2,3,1] -> 2 (pairs (1,4): 3 > 2*1 and (3,4): 3 > 2*1).

Brute force
-----------
Check every pair i < j and test nums[i] > 2 * nums[j]. O(n^2) time, O(1) space. The waste is
that the test is a rank query in disguise — for a fixed i we only need "how many later
elements are < nums[i] / 2" — and the brute force answers it by touching every later element
rather than exploiting any ordering.

From brute force to optimal
---------------------------
Split the array in half. Pairs entirely inside one half are counted recursively; only the
cross pairs (i in the left half, j in the right half) remain, and for those the index
condition i < j is automatic. If both halves are sorted, the cross count is a two-pointer
walk: for each left value x in increasing order, the right values with 2 * r < x form a
prefix of the sorted right half, and that prefix only grows as x grows, so the right pointer
never moves backwards — O(left + right) per merge. After counting, merge the two halves to
hand a sorted array up to the parent. Each level does O(n) work and there are log n levels.
This is the same skeleton as counting inversions; only the comparison (x > 2r instead of
x > r) differs, which is why the counting pass must be separate from the merge pass.

Intuition
---------
Sorting destroys index order, but a reverse pair only needs i < j, and merge sort offers a
moment where index order is known for free: everything in the left half precedes everything
in the right half. At that moment both halves are sorted, so the question "how many right
elements does this left element dominate by a factor of two?" is a monotone sweep, not a
scan. Divide, count across the cut, conquer.

Geometric view
--------------
Lay the sorted left half above the sorted right half. A pointer j on the lower rail advances
while 2 * right[j] < left[i]; as i steps right on the upper rail, j can only step right too
— the two pointers trace a monotone staircase, and the area under it (sum of j over all i)
is the number of cross pairs. Then the rails are zipped into one sorted rail for the level
above.

Steps
-----
1. sort(arr) returns (sorted arr, reverse pairs inside arr); singletons return (arr, 0).
2. Recurse on both halves: left, a and right, b.
3. j = 0; for x in left: while j < len(right) and 2 * right[j] < x: j += 1; count += j.
4. Merge left and right into a sorted list (heapq.merge or a manual zip).
5. Return (merged, a + b + count); the answer is the count for the whole array.

Complexity: O(n log n) time, O(n) space — log n levels, each with a linear count and a linear merge.
Pitfalls: moving the right pointer backwards or restarting it for every left element (that is
O(n^2) again); doing the counting during the merge, where the merge comparison (x <= r) is
not the pair comparison (x > 2r); off-by-one with the strict inequality for negative values.
"""
from heapq import merge
from typing import List, Tuple


class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        def sort(arr: List[int]) -> Tuple[List[int], int]:
            if len(arr) <= 1:
                return arr, 0
            mid = len(arr) // 2
            left, a = sort(arr[:mid])
            right, b = sort(arr[mid:])
            count = a + b
            j = 0                        # right[:j] are exactly the r with 2r < x
            for x in left:               # x increases, so j never moves back
                while j < len(right) and 2 * right[j] < x:
                    j += 1
                count += j
            return list(merge(left, right)), count

        return sort(nums)[1]


def brute_force(nums: List[int]) -> int:
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > 2 * nums[j]:
                count += 1
    return count


if __name__ == "__main__":
    s = Solution()
    assert s.reversePairs([1, 3, 2, 3, 1]) == 2
    assert s.reversePairs([2, 4, 3, 5, 1]) == 3
    assert s.reversePairs([]) == 0
    assert s.reversePairs([5]) == 0
    assert s.reversePairs([-5, -3, -1, 0]) == 1   # only -5 > 2 * -3
    import random
    random.seed(493)
    for _ in range(300):
        nums = [random.randint(-10, 10) for _ in range(random.randint(0, 15))]
        assert s.reversePairs(nums) == brute_force(nums)
    print("ok")
