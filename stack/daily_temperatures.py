"""
Daily Temperatures (LeetCode 739)  — Medium
Pattern: Monotonic stack

Problem
-------
Given daily temperatures, return answer[i] = number of days until a strictly warmer
temperature, or 0 if none comes.
Example: [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0].

Brute force
-----------
For each day i scan forward to the first j > i with temperatures[j] > temperatures[i].
O(n^2) time, O(1) space. The wasted work: for a descending run like 75,71,69 the scan from
75 walks over 71 and 69 even though those days are themselves still waiting for a warmer
day, so they cannot possibly be the answer for 75.

From brute force to optimal
---------------------------
The redundancy is walking over days that are "still waiting". Observation: flip the
direction of the question -- instead of each day looking forward for its answer, let each
new day announce itself as the answer for all earlier, cooler days that are still waiting.
Those waiting days form a stack with strictly decreasing temperatures (a warmer waiting day
below a cooler one). When day i arrives, pop every waiting day cooler than it and set their
answers to i - j; then push i. Each day is pushed once and popped at most once.

Intuition
---------
Keep the unresolved days on a stack. A new temperature resolves exactly the unresolved days
that are colder than it -- and because the stack is sorted (cooler on top), those are a
contiguous run at the top.

Geometric view
--------------
Looking at the bar chart from the right, the unresolved days form a descending staircase.
A new taller bar arriving on the right "floods" every shorter step at the top of the stack:
each flooded step records how far it is from the flooding bar.

Steps
-----
1. answer = [0]*n, stack = [] (indices with decreasing temperatures).
2. For each i, t: while stack and temperatures[stack[-1]] < t: j = pop; answer[j] = i - j.
3. Push i.
4. Return answer (indices never popped keep 0).

Complexity: O(n) time, O(n) space — each index is pushed and popped at most once.
Pitfalls: Popping on <= instead of < (equal temperature is not "warmer"); storing
temperatures rather than indices (then the distance is lost).
"""
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = [0] * len(temperatures)
        stack = []                               # indices still waiting; temps decreasing
        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()                  # day j's first warmer day is today
                answer[j] = i - j
            stack.append(i)
        return answer


def brute_force(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    answer = [0] * n
    for i in range(n):
        for j in range(i + 1, n):                # rescans cooler days that are also waiting
            if temperatures[j] > temperatures[i]:
                answer[i] = j - i
                break
    return answer


if __name__ == "__main__":
    s = Solution()
    cases = [[73, 74, 75, 71, 69, 72, 76, 73], [30, 40, 50, 60], [30, 60, 90], [50, 50, 50], [90, 80, 70]]
    assert s.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert s.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert s.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    assert s.dailyTemperatures([50, 50, 50]) == [0, 0, 0]
    for c in cases:
        assert s.dailyTemperatures(c) == brute_force(c)
    print("ok")
