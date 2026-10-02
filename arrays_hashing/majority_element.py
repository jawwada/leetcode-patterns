"""
Majority Element (LeetCode 169)  — Easy
Pattern: Boyer-Moore voting

Problem
-------
Given an array of size n, return the element that appears more than n / 2 times. A
majority element always exists. Follow-up: O(n) time and O(1) space.
Example: nums = [2, 2, 1, 1, 1, 2, 2] -> 2.

Brute force
-----------
For each element, count its occurrences with a full scan and return it if the count
exceeds n / 2. O(n^2) time, O(1) space. The waste is re-counting: the same value is
counted again from scratch every time it appears, and we count candidates that could
never win. A Counter dict fixes time to O(n) but uses O(n) space.

From brute force to optimal
---------------------------
We do not need the exact counts of every value — only to identify the one value that
is in the strict majority. Observation: if you pair up each majority element with a
distinct non-majority element and cancel both, the majority still has leftovers,
because it has more than half. Boyer-Moore implements this cancellation in one pass
with two variables: a candidate and a count. Matching elements increment the count,
non-matching ones decrement (cancel against the candidate), and when the count hits
zero the next element becomes the new candidate. The majority survives all
cancellations, so whatever is the candidate at the end is the answer.

Intuition
---------
Think of the array as a vote. Every non-majority vote can knock out at most one
majority vote, and there are strictly fewer of them, so the majority candidate is
left standing. The count is just a tally of "unanswered votes" for the current
candidate.

Geometric view
--------------
Draw the array as a sequence of coloured blocks. Walk left to right carrying a stack
of blocks of ONE colour: same colour -> push; different colour -> pop one (they
annihilate). An empty stack takes the next block's colour. Since the majority colour
has more than half the blocks, it cannot be fully annihilated and tops the stack at
the end.

Steps
-----
1. candidate = None, count = 0.
2. For each v: if count == 0, candidate = v.
3. count += 1 if v == candidate else -1.
4. Return candidate (guaranteed by the majority assumption).

Complexity: O(n) time, O(1) space — one pass, two scalars.
Pitfalls: using this when a majority is NOT guaranteed (you must then do a second
verification pass); resetting candidate without resetting the count logic; the
count can legitimately hit zero many times mid-array.
"""
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate = nums[0]
        count = 0
        for v in nums:
            if count == 0:
                candidate = v           # previous candidate fully cancelled out
            count += 1 if v == candidate else -1
        return candidate


def brute_force(nums: List[int]) -> int:
    n = len(nums)
    for v in nums:
        occurrences = 0
        for w in nums:
            if w == v:
                occurrences += 1
        if occurrences > n // 2:
            return v
    return -1


if __name__ == "__main__":
    s = Solution()
    assert s.majorityElement([3, 2, 3]) == 3
    assert s.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2
    assert s.majorityElement([1]) == 1
    assert s.majorityElement([5, 1, 5, 1, 5]) == 5
    for case in ([3, 2, 3], [2, 2, 1, 1, 1, 2, 2], [1], [5, 1, 5, 1, 5]):
        assert s.majorityElement(case) == brute_force(case)
    print("ok")
