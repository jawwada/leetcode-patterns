"""
Gas Station (LeetCode 134)  — Medium
Pattern: Greedy running sum with restart

Problem
-------
n gas stations on a circle; gas[i] is fuel available at station i and cost[i] is fuel needed to
drive to station i+1. Starting with an empty tank, return the unique starting index from which
you can complete a full loop, or -1 if impossible.
Example: gas = [1,2,3,4,5], cost = [3,4,5,1,2] -> 3.

Brute force
-----------
Try every start s: simulate the loop, adding gas[i] - cost[i] at each station and failing if the
tank goes negative. O(n^2) time, O(1) space. The wasted work: when the simulation from s fails at
station f, we throw away everything learned and restart from s+1, even though every start in
(s, f] is also doomed — they reach f with less fuel than s did.

From brute force to optimal
---------------------------
The redundancy is re-simulating starts that are provably hopeless. Observation 1: if starting at
s the tank first goes negative after station f, then no start in s+1..f works either (the tank
at any intermediate station was >= 0 when coming from s, so starting there with 0 fuel is no
better). So jump the candidate start straight to f+1 — one scan. Observation 2: a solution exists
iff sum(gas) >= sum(cost); when it does, the only surviving candidate from the scan is the answer
(the problem guarantees uniqueness), so no second verification loop is needed.

Intuition
---------
Drive with a running tank. Whenever you run dry, you know none of the stations you passed since
your last restart can be the start, so restart at the next station. Keep a global total of
surplus; if it is negative, no start works; otherwise the last restart point is it.

Geometric view
--------------
Plot cumulative (gas - cost) around the circle. The valid start is the station right after the
GLOBAL MINIMUM of the cumulative curve: beginning there, the curve never dips below its start.
The greedy restart finds exactly that point in one pass.

    diff:  -2  -2  -2   3   3
    tank:  -2 | -2 | -2 | 3   6      '|' = tank < 0, restart at next station
    start:  1    2    3            -> candidate 3, total = 0 >= 0 -> answer 3

Steps
-----
1. total = tank = 0, start = 0.
2. For i in range(n): d = gas[i] - cost[i]; total += d; tank += d.
3. If tank < 0: start = i + 1; tank = 0.
4. Return start if total >= 0 else -1.

Complexity: O(n) time, O(1) space — one pass with three integers.
Pitfalls: trying to verify with a second loop (unnecessary given uniqueness); returning start when
total < 0; starting the restart at i instead of i+1.
"""
from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total = tank = start = 0
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total += diff
            tank += diff
            if tank < 0:                     # every start in [start, i] is doomed
                start, tank = i + 1, 0
        return start if total >= 0 else -1


def brute_force(gas: List[int], cost: List[int]) -> int:
    n = len(gas)
    for s in range(n):
        tank = 0
        for k in range(n):
            i = (s + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                break
        else:
            return s
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
        ([2, 3, 4], [3, 4, 3], -1),
        ([5], [4], 0),
        ([3, 1, 1], [1, 2, 2], 0),
        ([1, 2], [2, 1], 1),
    ]
    for g, c, want in cases:
        assert s.canCompleteCircuit(g, c) == want
        assert brute_force(g, c) == want
    print("ok")
