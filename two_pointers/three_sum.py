"""
3Sum (LeetCode 15)  — Medium
Pattern: Sort + fixed element + converging two pointers

Problem
-------
Given an integer array nums, return all unique triplets [a, b, c] with a + b + c == 0.
The solution set must not contain duplicate triplets (order inside a triplet and order
of triplets do not matter).
Example: nums = [-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0, 1]].

Brute force
-----------
Three nested loops over i < j < k, test the sum, and insert the sorted triplet into a
set to kill duplicates. O(n^3) time, O(#answers) space. The wasted work: for every
fixed pair (i, j) the required third value is already known (-(nums[i] + nums[j])),
yet a whole loop searches for it; and duplicate triplets are generated many times
only to be thrown away by the set.

From brute force to optimal
---------------------------
Fix the first element nums[i]; the remainder is Two Sum with target -nums[i]. A hash
set makes that O(n) per i (O(n^2) total) but deduplication stays messy. Sorting first
solves both problems at once: on a sorted suffix the two-sum is a converging two
pointer walk (O(n) per i, O(1) extra space), and duplicates become ADJACENT, so they
are skipped by advancing past equal neighbours — for i, and for left/right after a
hit. Sorting costs O(n log n), dominated by the O(n^2) scan.

Intuition
---------
Reduce the dimension: 3Sum is n copies of 2Sum. Sorting turns each 2Sum into a
two-pointer sweep and makes duplicate values contiguous so skipping them is a local
check instead of a global set.

Geometric view
--------------
Picture the sorted array as a number line. A fixed anchor i sits at the left; two
pointers L (just right of i) and R (far right) move toward each other. Sum too small
-> L slides right; too big -> R slides left; exact -> record, then both slide past
any clones of their current values. Then the anchor steps right (skipping its own
clones) and the sweep repeats on the shorter suffix.

Steps
-----
1. Sort nums.
2. For i in range(n - 2): skip if nums[i] > 0 (no zero-sum possible) or nums[i] == nums[i-1].
3.   left = i + 1, right = n - 1; while left < right: total = nums[i] + nums[left] + nums[right].
4.   total < 0 -> left += 1; total > 0 -> right -= 1.
5.   total == 0 -> append triplet, then advance left past duplicates and right past duplicates.
6. Return the results.

Complexity: O(n^2) time, O(1) extra space ignoring the output and the sort's stack.
Pitfalls: skipping duplicates for i with nums[i] == nums[i+1] (that skips valid
triplets like [-1, -1, 2]) — compare with i - 1 instead; forgetting to move BOTH
pointers after a hit; using a set of tuples as a crutch when the interviewer wants
the adjacency argument.
"""
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result: List[List[int]] = []
        for i in range(n - 2):
            if nums[i] > 0:
                break                              # all later values are positive too
            if i > 0 and nums[i] == nums[i - 1]:
                continue                           # same anchor as before -> same triplets
            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1                  # skip clones of the value just used
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        return result


def brute_force(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    found = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in found]


def _normalize(triplets: List[List[int]]) -> List[List[int]]:
    return sorted(sorted(t) for t in triplets)


if __name__ == "__main__":
    s = Solution()
    assert _normalize(s.threeSum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
    assert s.threeSum([0, 1, 1]) == []
    assert s.threeSum([0, 0, 0]) == [[0, 0, 0]]
    assert _normalize(s.threeSum([-2, 0, 0, 2, 2])) == [[-2, 0, 2]]
    for case in ([-1, 0, 1, 2, -1, -4], [0, 1, 1], [0, 0, 0], [-2, 0, 0, 2, 2], [3, -2, 1, 0, -1, -1, 2]):
        assert _normalize(s.threeSum(list(case))) == _normalize(brute_force(list(case)))
    print("ok")
