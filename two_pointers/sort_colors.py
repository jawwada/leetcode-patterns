"""
Sort Colors (LeetCode 75)  — Medium
Pattern: Dutch national flag (three-way partition)

Problem
-------
Given an array containing only 0s, 1s and 2s, sort it in place so all 0s come first,
then 1s, then 2s. Do not use the library sort; aim for one pass with O(1) space.
Example: nums = [2, 0, 2, 1, 1, 0] -> [0, 0, 1, 1, 2, 2].

Brute force
-----------
Count the number of 0s, 1s and 2s in one pass, then overwrite the array with that many
of each in a second pass (counting sort). O(n) time, O(1) space, two passes. It is
correct and fast, but the second pass rewrites every cell, including the ones already
in place, and it does not generalise to records that carry data with their key. The
"wasted" work is the second full write pass.

From brute force to optimal
---------------------------
Instead of counting then rewriting, partition in a single pass by maintaining three
regions with invariants: nums[:low] are all 0, nums[low:mid] are all 1, nums[high+1:]
are all 2, and nums[mid:high+1] is unexplored. Examine nums[mid]: a 0 is swapped to
the low boundary (both low and mid advance), a 1 is already in place (mid advances),
a 2 is swapped to the high boundary (high retreats, mid stays because the swapped-in
value is unexplored). Each step shrinks the unexplored region by one, so one pass
and each element is moved at most twice.

Intuition
---------
Three-way partitioning is quicksort's partition step with two pivots at once. The
invariants make the array self-describing: whatever lands in the 0-zone or 2-zone is
final, and only the middle frontier needs inspection.

Geometric view
--------------
Picture the array as four coloured bands growing/shrinking: [0 0 0 | 1 1 | ? ? ? | 2 2].
`low` marks the end of the red band, `mid` the end of the white band (and the start
of the unknown band), `high` the start of the blue band. The unknown band is eaten
from the left by `mid` and from the right by `high` until they cross.

Steps
-----
1. low = mid = 0, high = n - 1.
2. While mid <= high:
3.   if nums[mid] == 0: swap(low, mid); low += 1; mid += 1.
4.   elif nums[mid] == 1: mid += 1.
5.   else: swap(mid, high); high -= 1  (do NOT advance mid).
6. Done — the array is sorted in place.

Complexity: O(n) time, O(1) space — one pass, each iteration shrinks the unknown
region by one.
Pitfalls: advancing mid after swapping with high (the swapped-in element is still
unexamined); loop condition mid < high instead of <= (misses the last element);
confusing which pointer moves on which value.
"""
from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        # invariant: nums[:low] == 0s, nums[low:mid] == 1s, nums[high+1:] == 2s
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1              # nums[mid] is new and unexamined, so mid stays


def brute_force(nums: List[int]) -> None:
    counts = [0, 0, 0]
    for v in nums:
        counts[v] += 1
    i = 0
    for colour in range(3):
        for _ in range(counts[colour]):
            nums[i] = colour
            i += 1


if __name__ == "__main__":
    s = Solution()
    a = [2, 0, 2, 1, 1, 0]
    s.sortColors(a)
    assert a == [0, 0, 1, 1, 2, 2]
    b = [2, 0, 1]
    s.sortColors(b)
    assert b == [0, 1, 2]
    c = [0]
    s.sortColors(c)
    assert c == [0]
    d = [2, 2, 2, 1, 1, 0, 0]
    s.sortColors(d)
    assert d == [0, 0, 1, 1, 2, 2, 2]
    for case in ([2, 0, 2, 1, 1, 0], [2, 0, 1], [0], [2, 2, 2, 1, 1, 0, 0], [1, 1, 1], []):
        x, y = list(case), list(case)
        s.sortColors(x)
        brute_force(y)
        assert x == y
    print("ok")
