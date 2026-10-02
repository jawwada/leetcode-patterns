"""
First Missing Positive (LeetCode 41)  — Hard
Pattern: Index as hash (in-place cyclic placement)

Problem
-------
Given an unsorted integer array nums, return the smallest positive integer that is
not present. Required: O(n) time and O(1) auxiliary space.
Example: nums = [3, 4, -1, 1] -> 2.   nums = [1, 2, 0] -> 3.   nums = [7, 8, 9] -> 1.

Brute force
-----------
Try candidate = 1, 2, 3, ... and for each candidate scan the whole array to see if it
is present; the first absent candidate is the answer. O(n^2) time, O(1) space. The
waste is the repeated membership scan: the array is re-read from scratch for every
candidate. A hash set fixes the time (O(n)) but spends O(n) extra space, which the
problem forbids.

From brute force to optimal
---------------------------
The key observation bounds the answer: with n elements, the answer is in 1..n+1
(if all of 1..n are present the answer is n+1; otherwise something in 1..n is
missing). So only values 1..n matter, and there are exactly n slots in the array —
the array itself can serve as the hash set, with value v "stored" by placing it at
index v - 1. One pass swaps each in-range value into its home slot (each swap puts at
least one value home, so total swaps are <= n). A second pass finds the first index i
whose slot does not hold i + 1; the answer is i + 1, or n + 1 if every slot is correct.

Intuition
---------
A permutation-like placement: if every value 1..n were present, sorting them into
slots 0..n-1 would be a perfect fit. Values out of range or duplicates have nowhere
to go and are simply left behind; the first slot whose occupant is wrong points at the
missing number.

Geometric view
--------------
Picture n numbered parking bays. Each car with a number 1..n drives to bay number-1,
kicking out whoever is there, who then drives to THEIR bay, and so on (a cycle). Cars
with numbers outside 1..n or duplicates never get a bay and are abandoned where they
stand. Walk the bays in order; the first bay without its matching car is the answer.

Steps
-----
1. n = len(nums). For each index i:
2.   while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i], swap nums[i] with nums[nums[i] - 1].
3. For each index i: if nums[i] != i + 1, return i + 1.
4. Return n + 1.

Complexity: O(n) time, O(1) extra space — each swap places one value in its final
slot, so at most n swaps overall across the while loops.
Pitfalls: the duplicate guard nums[nums[i]-1] != nums[i] (without it, duplicates loop
forever); using `if` instead of `while` (the swapped-in value also needs placing);
mutating the input when the interviewer asks you not to (ask first).
"""
from typing import List


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            # keep swapping until slot i holds a value that is out of range or already home
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                home = nums[i] - 1
                nums[i], nums[home] = nums[home], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1


def brute_force(nums: List[int]) -> int:
    candidate = 1
    while candidate in nums:
        candidate += 1
    return candidate


if __name__ == "__main__":
    s = Solution()
    assert s.firstMissingPositive([1, 2, 0]) == 3
    assert s.firstMissingPositive([3, 4, -1, 1]) == 2
    assert s.firstMissingPositive([7, 8, 9, 11, 12]) == 1
    assert s.firstMissingPositive([1, 1]) == 2
    assert s.firstMissingPositive([1]) == 2
    for case in ([1, 2, 0], [3, 4, -1, 1], [7, 8, 9, 11, 12], [1, 1], [1], [2, 2, 2, 1]):
        assert s.firstMissingPositive(list(case)) == brute_force(list(case))
    print("ok")
