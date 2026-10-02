"""
Max Consecutive Ones III (LeetCode 1004)  — Medium
Pattern: Variable-size sliding window

Problem
-------
Given a binary array nums and an integer k, you may flip at most k zeros to ones. Return the
length of the longest run of consecutive ones achievable.
Example: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2 -> 6 (flip the two zeros at indices 4,5).

Brute force
-----------
For each start i, walk right counting zeros until the (k+1)-th zero, record the length.
O(n^2) time, O(1) space. The wasted work: start i+1 recounts the zeros in a stretch whose
zero count we already know (it differs by at most one from start i's).

From brute force to optimal
---------------------------
The redundancy is recounting zeros in an overlapping range. Observation: "at most k zeros"
is a monotone property of the window (sub-windows of a valid window are valid), so instead
of restarting, when the window gains a (k+1)-th zero we move left forward until one zero
drops out. A single integer `zeros` tracks the invariant, updated by +1/-1 as indices enter
and leave. Both edges move only rightwards, so the sweep is linear.

Intuition
---------
Reframe "flip at most k zeros" as "find the longest window containing at most k zeros".
Then it's a standard expand-right / shrink-left window with a zero counter.

Geometric view
--------------
An elastic band [L, R] over the bit string. R stretches it right; each 0 inside the band
is a "flip". When the band contains k+1 zeros, L drags right until a zero slips out the
left end. The widest the band ever gets is the answer.

Steps
-----
1. left = 0, zeros = 0, best = 0.
2. For each right: if nums[right] == 0, zeros += 1.
3. While zeros > k: if nums[left] == 0, zeros -= 1; left += 1.
4. best = max(best, right - left + 1). Return best.

Complexity: O(n) time, O(1) space — each index enters and leaves the window once.
Pitfalls: k = 0 must still work (window of pure ones); using `if` instead of `while` to
shrink (fine here since only one zero enters per step, but fragile); forgetting to count
the window after shrinking.
"""
from typing import List


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = zeros = best = 0
        for right, x in enumerate(nums):
            if x == 0:
                zeros += 1
            while zeros > k:                 # k+1 zeros inside: push left past one zero
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, right - left + 1)
        return best


def brute_force(nums: List[int], k: int) -> int:
    best = 0
    for i in range(len(nums)):
        zeros = 0                            # recounted from scratch for each start
        for j in range(i, len(nums)):
            zeros += nums[j] == 0
            if zeros > k:
                break
            best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2),
        ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3),
        ([0, 0, 0], 0),
        ([1, 1, 1], 0),
        ([0, 0, 0], 5),
    ]
    assert s.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert s.longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
    assert s.longestOnes([0, 0, 0], 0) == 0
    assert s.longestOnes([1, 1, 1], 0) == 3
    for c in cases:
        assert s.longestOnes(*c) == brute_force(*c)
    print("ok")
