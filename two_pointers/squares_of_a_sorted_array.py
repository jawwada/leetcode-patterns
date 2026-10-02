"""
Squares of a Sorted Array (LeetCode 977)  — Easy
Pattern: Two pointers merging from both ends

Problem
-------
Given an integer array sorted in non-decreasing order (may contain negatives), return
an array of the squares of each number, also sorted in non-decreasing order, in O(n).
Example: nums = [-4, -1, 0, 3, 10] -> [0, 1, 9, 16, 100].

Brute force
-----------
Square every element and sort the result: sorted(x * x for x in nums). O(n log n)
time, O(n) space. The wasted work is the sort — it ignores that the input is already
sorted, which means the squares are already sorted in two separate pieces (the
negatives' squares decreasing, the non-negatives' squares increasing).

From brute force to optimal
---------------------------
Squaring folds the number line: |x| is largest at BOTH ends of a sorted array and
smallest somewhere in the middle. So the biggest square is either nums[0]^2 or
nums[-1]^2. Compare the two ends, write the larger square to the END of the output,
and move that pointer inward. This is a merge of two sorted sequences (the squares of
the negative part read right-to-left and of the non-negative part read left-to-right)
done without ever finding the split point — filling the output from the back makes the
split point irrelevant.

Intuition
---------
Sorted input + a V-shaped transform (x^2) means the output's maximum is always at one
of the two current ends. Repeatedly peel off the larger end into the output from the
back; what remains is still sorted with the same property.

Geometric view
--------------
Picture the parabola y = x^2 over the sorted inputs: a V shape. The two pointers L and
R sit on the arms of the V and descend toward the bottom, always lowering the higher
one. Each step emits the current higher point into the output array, which fills from
its right end toward the left.

Steps
-----
1. result = [0] * n; left = 0; right = n - 1; write = n - 1.
2. While left <= right: compare abs(nums[left]) and abs(nums[right]).
3.   Write the larger square to result[write]; move that pointer inward.
4.   write -= 1.
5. Return result.

Complexity: O(n) time, O(n) space for the output — one pass, each step places one value.
Pitfalls: filling the output front to back (the smallest square is NOT at an end);
loop condition < instead of <= (misses the last element); comparing values instead of
absolute values.
"""
from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * n
        left, right = 0, n - 1
        for write in range(n - 1, -1, -1):          # fill from the largest square down
            if abs(nums[left]) > abs(nums[right]):
                result[write] = nums[left] * nums[left]
                left += 1
            else:
                result[write] = nums[right] * nums[right]
                right -= 1
        return result


def brute_force(nums: List[int]) -> List[int]:
    return sorted(x * x for x in nums)


if __name__ == "__main__":
    s = Solution()
    assert s.sortedSquares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
    assert s.sortedSquares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
    assert s.sortedSquares([-5, -3, -1]) == [1, 9, 25]
    assert s.sortedSquares([1]) == [1]
    for case in ([-4, -1, 0, 3, 10], [-7, -3, 2, 3, 11], [-5, -3, -1], [1], [0, 0], [2, 3, 4]):
        assert s.sortedSquares(case) == brute_force(case)
    print("ok")
