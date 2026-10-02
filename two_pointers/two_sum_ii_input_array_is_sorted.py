"""
Two Sum II - Input Array Is Sorted (LeetCode 167)  — Medium
Pattern: Converging two pointers on sorted input

Problem
-------
Given a 1-indexed array sorted in non-decreasing order and a target, return the
1-based indices [i, j] (i < j) of the two numbers that sum to target. Exactly one
solution exists; use O(1) extra space.
Example: numbers = [2, 7, 11, 15], target = 9 -> [1, 2].

Brute force
-----------
Check every pair (i, j) with i < j. O(n^2) time, O(1) space. The wasted work is
ignoring the sort order: once numbers[i] + numbers[j] exceeds target, every j' > j
is also too big, yet the brute force keeps checking them. (A hash map gives O(n) but
O(n) space, which the problem rules out.)

From brute force to optimal
---------------------------
Because the array is sorted, the sum of the current pair tells us which direction to
move. Start with the smallest and largest elements. If their sum is too small, the
only way to increase it is to move the left pointer right (a bigger small number);
if too big, move the right pointer left. Each move permanently discards one element
as a possible partner: a too-small left element cannot pair with anything smaller
than the current right (those sums are even smaller), and symmetrically for right.
So n - 1 moves at most, O(n) time, O(1) space.

Intuition
---------
Sorted order lets a single comparison eliminate an entire element from
consideration, not just one pair. Two pointers converging from the ends therefore
examine O(n) pairs instead of O(n^2) while never skipping the answer.

Geometric view
--------------
Imagine the n x n grid of pairs (i, j). Sorted order means sums increase to the
right and downward. The two-pointer walk starts at the top-right corner (smallest i,
largest j) and at each step moves either down (i += 1) or left (j -= 1), tracing a
staircase that cuts the grid; every cell off the staircase has been proven too small
or too large.

Steps
-----
1. left = 0, right = n - 1.
2. While left < right: total = numbers[left] + numbers[right].
3.   If total == target, return [left + 1, right + 1].
4.   If total < target, left += 1; else right -= 1.

Complexity: O(n) time, O(1) space — each iteration moves one pointer inward.
Pitfalls: returning 0-based indices; using a hash map and violating the space
constraint; the argument for why the answer is never skipped (worth saying aloud).
"""
from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]   # 1-indexed answer
            if total < target:
                left += 1                      # need a bigger sum
            else:
                right -= 1                     # need a smaller sum
        return []


def brute_force(numbers: List[int], target: int) -> List[int]:
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
    return []


if __name__ == "__main__":
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert s.twoSum([2, 3, 4], 6) == [1, 3]
    assert s.twoSum([-1, 0], -1) == [1, 2]
    assert s.twoSum([1, 2, 3, 4, 4, 9, 56, 90], 8) == [4, 5]
    for nums, t in [([2, 7, 11, 15], 9), ([2, 3, 4], 6), ([-1, 0], -1), ([1, 2, 3, 4, 4, 9, 56, 90], 8)]:
        assert s.twoSum(nums, t) == brute_force(nums, t)
    print("ok")
