"""
Two Sum (LeetCode 1)  — Easy
Pattern: Hash map complement lookup

Problem
-------
Given an integer array nums and an integer target, return the indices of the two
numbers that add up to target. Exactly one answer exists and you may not reuse an
element. Example: nums = [2, 7, 11, 15], target = 9 -> [0, 1] because 2 + 7 = 9.

Brute force
-----------
For every index i, scan every j > i and check nums[i] + nums[j] == target.
O(n^2) time, O(1) space. The wasted work is the inner scan: for a fixed nums[i] we
already know the ONE value we are looking for (target - nums[i]), yet we re-read the
whole suffix to find it.

From brute force to optimal
---------------------------
The inner loop answers a membership question: "is target - nums[i] somewhere in the
array, and at which index?" Membership + lookup-by-value is exactly what a hash map
does in O(1). So replace the scan with a dict from value -> index. To respect the
"no reuse" rule and avoid a second pass, build the dict lazily: before inserting
nums[i], ask whether its complement is already present. Any valid pair (i, j) with
i < j is caught when we reach j, because nums[i] was inserted earlier.

Intuition
---------
Each number has exactly one partner that would complete the sum. Remember every
number you have seen so far; when the current number's partner is among them, done.
One pass suffices because a pair is discovered by whichever member comes second.

Geometric view
--------------
Picture a cursor sweeping left to right over the array. Everything left of the
cursor sits in a "seen" bag keyed by value. At each step the cursor asks the bag
one question (complement present?) and then drops its own value in. The bag grows
by one per step and no element is visited twice.

Steps
-----
1. Create an empty dict seen: value -> index.
2. For each index i with value v, compute need = target - v.
3. If need is in seen, return [seen[need], i].
4. Otherwise store seen[v] = i and continue.

Complexity: O(n) time, O(n) space — one pass with O(1) dict operations per element.
Pitfalls: inserting before checking (pairs an element with itself, e.g. target 6 and
nums [3, ...]); returning values instead of indices; assuming the array is sorted.
"""
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  # value -> index of an earlier element
        for i, v in enumerate(nums):
            need = target - v
            if need in seen:
                return [seen[need], i]
            seen[v] = i
        return []


def brute_force(nums: List[int], target: int) -> List[int]:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


if __name__ == "__main__":
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s.twoSum([3, 2, 4], 6) == [1, 2]
    assert s.twoSum([3, 3], 6) == [0, 1]
    assert s.twoSum([-1, -2, -3, -4, -5], -8) == [2, 4]
    for nums, t in [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6), ([-1, -2, -3, -4, -5], -8)]:
        assert s.twoSum(nums, t) == brute_force(nums, t)
    print("ok")
