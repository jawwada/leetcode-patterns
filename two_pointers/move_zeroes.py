"""
Move Zeroes (LeetCode 283)  — Easy
Pattern: Read/write pointers (stable compaction)

Problem
-------
Move all 0s in nums to the end in place, keeping the relative order of the non-zero
elements. Return nothing.
Example: nums = [0,1,0,3,12] -> [1,3,12,0,0].

Brute force
-----------
Bubble each zero rightward: whenever nums[i] == 0 and nums[i+1] != 0, swap them, and
repeat passes until nothing moves. O(n^2) time, O(1) space. The wasted work: a non-zero
value hops left one slot per pass, so it is moved up to (number of zeros before it) times
instead of jumping straight to its final slot.

From brute force to optimal
---------------------------
The redundancy is moving each non-zero one step at a time. Observation: the final slot of
the k-th non-zero is simply index k, because order is preserved and zeros fill the tail.
So keep a write pointer w = number of non-zeros placed so far; the read pointer r scans
left to right and, on each non-zero, swaps it into slot w and advances w. Invariant:
nums[0:w] holds the non-zeros seen so far in order, nums[w:r] are all zeros.

Intuition
---------
The array is being split into a "kept" prefix and a "zero" middle. Swapping (rather than
overwriting) carries the zero at w forward to r, so after one pass the zeros have collected
at the end with no second fill-in pass needed.

Geometric view
--------------
Two arrows move right. The read arrow r visits every cell; the write arrow w trails behind
it, advancing only when a non-zero is dropped at its position. The gap between w and r is
a growing bubble of zeros that slides toward the end of the array.

Steps
-----
1. w = 0.
2. For r in range(n): if nums[r] != 0, swap nums[w] and nums[r], then w += 1.
3. Done: nums[:w] are the non-zeros in order, nums[w:] are zeros.

Complexity: O(n) time, O(1) space — every index is read once and swapped at most once.
Pitfalls: Using remove/append in a loop (O(n^2) and mutates while iterating); building a
new list instead of modifying in place; sorting (breaks relative order).
"""
from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        w = 0                                   # next slot for a non-zero
        for r in range(len(nums)):
            if nums[r] != 0:
                nums[w], nums[r] = nums[r], nums[w]   # zero at w is carried forward to r
                w += 1


def brute_force(nums: List[int]) -> None:
    moved = True
    while moved:                                # one bubble pass per iteration
        moved = False
        for i in range(len(nums) - 1):
            if nums[i] == 0 and nums[i + 1] != 0:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                moved = True


if __name__ == "__main__":
    s = Solution()
    cases = [([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]), ([0], [0]), ([1, 2], [1, 2]),
             ([0, 0, 1], [1, 0, 0]), ([4, 0, 5, 0, 0, 6], [4, 5, 6, 0, 0, 0])]
    for nums, want in cases:
        a, b = nums[:], nums[:]
        s.moveZeroes(a)
        brute_force(b)
        assert a == want and b == want, nums
    print("ok")
