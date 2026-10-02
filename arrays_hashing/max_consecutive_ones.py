"""
Max Consecutive Ones (LeetCode 485)  — Easy
Pattern: Running counter with reset

Problem
-------
Given a binary array nums, return the length of the longest run of consecutive 1s.
Example: nums = [1,1,0,1,1,1] -> 3 (the last three 1s).

Brute force
-----------
For every start index i, walk right while nums[j] == 1 and record the run length.
O(n^2) time, O(1) space. The wasted work: a run of k ones is re-walked from each of its
k starting positions, so the same 1s are counted again and again.

From brute force to optimal
---------------------------
The redundancy is restarting the count at every index inside a run that we have already
measured. Observation: the run ending at index j has length run(j-1) + 1 if nums[j] == 1,
and 0 otherwise — it depends only on the previous count. So one integer carried left to
right replaces the inner loop: increment on 1, reset on 0, and keep the best value seen.
Every element is touched exactly once.

Intuition
---------
A 0 is a wall: no run can cross it. Between walls the run just grows by one per step, so the
current run length is all the state we need, and the answer is the maximum it ever reaches.

Geometric view
--------------
Picture the array as a strip of tiles. A counter rides along the strip, climbing by one on
each 1 tile and dropping to the floor on each 0 tile. The answer is the highest peak of
that sawtooth.

Steps
-----
1. best = run = 0.
2. For each x: if x == 1, run += 1 and best = max(best, run); else run = 0.
3. Return best.

Complexity: O(n) time, O(1) space — single pass with two integers.
Pitfalls: Updating best only when a 0 appears (misses a run that ends at the last index);
forgetting to reset the counter on 0.
"""
from typing import List


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        best = run = 0
        for x in nums:
            if x == 1:
                run += 1
                best = max(best, run)   # update inside the run so a trailing run counts
            else:
                run = 0                 # a 0 breaks every run that crosses it
        return best


def brute_force(nums: List[int]) -> int:
    best = 0
    for i in range(len(nums)):
        j = i
        while j < len(nums) and nums[j] == 1:   # re-walks the same run from every start
            j += 1
        best = max(best, j - i)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 1, 0, 1, 1, 1], 3), ([1, 0, 1, 1, 0, 1], 2), ([0, 0], 0), ([1], 1), ([], 0)]
    for nums, want in cases:
        assert s.findMaxConsecutiveOnes(nums) == want
        assert brute_force(nums) == want
    print("ok")
