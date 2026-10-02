"""
Sliding Window Maximum (LeetCode 239)  — Hard
Pattern: Monotonic deque

Problem
-------
Given nums and a window size k, return the maximum of every contiguous window of size k, in
order from left to right.
Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 -> [3,3,5,5,6,7].

Brute force
-----------
For each of the n-k+1 windows compute max(nums[i:i+k]). O(n*k) time, O(1) extra space.
The wasted work: adjacent windows overlap in k-1 elements, yet we rescan all k every time.
Most of those elements can never be a future maximum anyway.

From brute force to optimal
---------------------------
The redundancy is reconsidering elements that are already dominated. Observation: if
nums[j] <= nums[i] with j < i, then nums[j] leaves every future window before nums[i] does
and is never larger, so nums[j] is useless forever. Keep only the "useful" indices in a
deque whose values are strictly decreasing from front to back: the front is the current
window's max. Pushing a new element pops smaller ones from the back; the front is popped
when its index slides out of the window. Each index enters and leaves once, so O(n).

Intuition
---------
Maintain a shortlist of candidates that could still become a maximum. A newcomer kills
every older candidate that is not bigger than it; the oldest surviving candidate is the
window max, and it retires only when it falls out of the window.

Geometric view
--------------
Draw the bars. Standing at the newest bar and looking left, the candidates are the bars
visible as a descending staircase; anything hidden behind a taller, newer bar is gone. The
deque IS that staircase; the leftmost step is the max, and it crumbles when the window
edge passes it.

Steps
-----
1. dq = deque of indices (values decreasing front -> back), out = [].
2. For each i: pop from the back while nums[back] <= nums[i]; append i.
3. If dq[0] <= i - k, pop the front (it slid out).
4. Once i >= k-1, append nums[dq[0]] to out.
5. Return out.

Complexity: O(n) time, O(k) space — every index is pushed and popped at most once.
Pitfalls: Storing values instead of indices (can't tell when the max expires); popping the
front with `<` instead of `<=` on `i - k`; using `<` when evicting from the back (ties must
also be evicted, or the deque grows).
"""
from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque()                               # indices; values strictly decreasing
        out = []
        for i, x in enumerate(nums):
            while dq and nums[dq[-1]] <= x:        # x dominates older, smaller values
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:                     # front slid out of the window
                dq.popleft()
            if i >= k - 1:
                out.append(nums[dq[0]])
        return out


def brute_force(nums: List[int], k: int) -> List[int]:
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]   # rescans k per window


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 3, -1, -3, 5, 3, 6, 7], 3), ([1], 1), ([9, 8, 7, 6], 2), ([4, 4, 4], 2), ([1, 2, 3], 3)]
    assert s.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert s.maxSlidingWindow([1], 1) == [1]
    assert s.maxSlidingWindow([9, 8, 7, 6], 2) == [9, 8, 7]
    assert s.maxSlidingWindow([1, 2, 3], 3) == [3]
    for c in cases:
        assert s.maxSlidingWindow(*c) == brute_force(*c)
    print("ok")
