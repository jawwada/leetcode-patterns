"""
Remove Duplicates from Sorted Array II (LeetCode 80)  — Medium
Pattern: Slow/fast pointers with look-back

Problem
-------
Given a sorted array, remove duplicates in place so that each value appears at most
twice, keeping relative order. Return the new length k; the first k slots must hold the
result. O(1) extra space.
Example: nums = [1, 1, 1, 2, 2, 3] -> k = 5, nums[:5] = [1, 1, 2, 2, 3].

Brute force
-----------
Walk the array; whenever a value has already appeared twice, delete that element with
list deletion (which shifts the whole tail left by one). O(n^2) time in the worst case
(many deletions, each O(n) shift), O(1) space. The waste is the shifting: each
deletion re-moves every element behind it, so a tail element may be moved many times
instead of once to its final position.

From brute force to optimal
---------------------------
Deleting in place shifts the tail repeatedly because we decide element-by-element. Flip
it around: instead of removing bad elements, COPY good elements forward to a write
pointer. A slow pointer `write` marks the next free slot in the output; a fast pointer
scans the input. An element is "good" if it does not create a third copy, and because
the array is sorted the third copy is detectable locally: nums[fast] is a third copy
exactly when it equals nums[write - 2]. Each element is read once and written at most
once — O(n), and the look-back needs no counter.

Intuition
---------
In a sorted array, equal values are contiguous, so "appears more than twice so far" is
the same as "equals the element two slots back in the output". The output prefix is
always valid, so the look-back is into trusted territory and a counter is unnecessary.
The same idea with `write - k` keeps at most k copies.

Geometric view
--------------
Two fingers on one row: `write` lags behind `read`. The region before `write` is the
finished, compacted output; between them is discarded junk; from `read` onward is
unread input. Each step `read` advances by one, and `write` advances only when the
value passes the look-back test, so the junk gap grows by the number of rejected
copies.

Steps
-----
1. If n <= 2, return n (nothing to remove).
2. write = 2.
3. For read in 2..n-1: if nums[read] != nums[write - 2], nums[write] = nums[read]; write += 1.
4. Return write.

Complexity: O(n) time, O(1) space — one pass, two indices.
Pitfalls: comparing against nums[read - 2] (the input) instead of nums[write - 2] (the
output); starting write at 0 or 1; off-by-one when n <= 2.
"""
from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums) <= 2:
            return len(nums)
        write = 2                      # first two elements are always kept
        for read in range(2, len(nums)):
            if nums[read] != nums[write - 2]:   # not a third copy in the OUTPUT
                nums[write] = nums[read]
                write += 1
        return write


def brute_force(nums: List[int]) -> int:
    i = 0
    while i < len(nums):
        if i >= 2 and nums[i] == nums[i - 1] == nums[i - 2]:
            del nums[i]                # shifts the whole tail left
        else:
            i += 1
    return len(nums)


if __name__ == "__main__":
    s = Solution()
    a = [1, 1, 1, 2, 2, 3]
    assert s.removeDuplicates(a) == 5 and a[:5] == [1, 1, 2, 2, 3]
    b = [0, 0, 1, 1, 1, 1, 2, 3, 3]
    assert s.removeDuplicates(b) == 7 and b[:7] == [0, 0, 1, 1, 2, 3, 3]
    c = [1, 1, 1, 1]
    assert s.removeDuplicates(c) == 2 and c[:2] == [1, 1]
    d = [1]
    assert s.removeDuplicates(d) == 1 and d == [1]
    for case in ([1, 1, 1, 2, 2, 3], [0, 0, 1, 1, 1, 1, 2, 3, 3], [1, 1, 1, 1], [1], [], [1, 2, 3]):
        x, y = list(case), list(case)
        kx, ky = s.removeDuplicates(x), brute_force(y)
        assert kx == ky and x[:kx] == y[:ky]
    print("ok")
