"""
Next Greater Element II (LeetCode 503)  — Medium
Pattern: Monotonic stack

Problem
-------
nums is circular (after the last element comes the first). For every index return the
first strictly greater value found by walking forward (wrapping around), or -1 if none.
Example: nums = [1,2,1] -> [2,-1,2]; nums = [1,2,3,4,3] -> [2,3,4,-1,4].

Brute force
-----------
For each i, step j = i+1, i+2, ... (mod n) for up to n-1 steps and stop at the first
nums[j] > nums[i]. O(n^2) time, O(1) extra space. The waste: a long descending run is
scanned again from every one of its elements, although one bigger value would answer all
of them at once.

From brute force to optimal
---------------------------
The redundancy is that every waiting index re-scans the same stretch of the array.
Observation: indices still waiting for an answer always have non-increasing values (if a
later one were bigger, it would have answered the earlier one). Keep those waiting indices
on a stack; each new value pops — and answers — every waiting index with a smaller value,
then waits itself. Circularity is handled with a second pass over the array that only
pops (it answers leftovers using values from the start, but pushes nothing new). Each
index is pushed once and popped at most once: O(n).

Intuition
---------
Think of each index as a person waiting for someone taller to appear to their right. The
waiting line is sorted tallest at the bottom, shortest on top, so a newcomer only has to
look at the top of the stack to settle everyone shorter than them. Wrapping around is
just "let the people at the start of the array walk past the line one more time".

Geometric view
--------------
Draw nums as bars. The stack holds a descending staircase of bars still looking right.
A new taller bar knocks down the lower steps of the staircase (assigning itself as their
answer) and becomes the new top step. The second lap re-uses bars from the left edge to
knock down what remains; bars left standing at the end (the global max) get -1.

Steps
-----
1. ans = [-1] * n, stack = [] (indices with values non-increasing bottom to top).
2. Pass 1, i = 0..n-1: while stack and nums[stack[-1]] < nums[i]: ans[stack.pop()] = nums[i];
   then push i.
3. Pass 2, i = 0..n-1: same popping loop, but no push (answers the wrap-around).
4. Return ans.

Complexity: O(n) time, O(n) space — each index is pushed once and popped at most once.
Pitfalls: Using <= when popping (equal values are not "greater"); pushing again in the
second pass (duplicates indices); storing values instead of indices on the stack.
"""
from typing import List


class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        stack: List[int] = []                 # indices waiting, values non-increasing
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                ans[stack.pop()] = nums[i]
            stack.append(i)
        for i in range(n):                    # wrap-around lap: answer leftovers, push nothing
            while stack and nums[stack[-1]] < nums[i]:
                ans[stack.pop()] = nums[i]
        return ans


def brute_force(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [-1] * n
    for i in range(n):
        for k in range(1, n):                 # re-walks the circle from every index
            if nums[(i + k) % n] > nums[i]:
                ans[i] = nums[(i + k) % n]
                break
    return ans


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 2, 1], [2, -1, 2]), ([1, 2, 3, 4, 3], [2, 3, 4, -1, 4]), ([5], [-1]),
             ([3, 3, 3], [-1, -1, -1]), ([5, 4, 3, 2, 1], [-1, 5, 5, 5, 5])]
    for nums, want in cases:
        assert s.nextGreaterElements(nums) == want, nums
        assert brute_force(nums) == want, nums
    print("ok")
