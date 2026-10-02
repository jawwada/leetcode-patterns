"""
Car Fleet (LeetCode 853)  — Medium
Pattern: Monotonic stack

Problem
-------
n cars drive toward target along a one-lane road; car i starts at position[i] with speed[i].
A faster car that catches a slower one must slow down and travel with it as a fleet (they
count as one). Return the number of fleets that arrive at the target.
Example: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3] -> 3.

Brute force
-----------
Compute each car's solo arrival time t_i = (target - p_i) / v_i. Car i is a fleet leader iff
no car ahead of it (larger position) has t_j >= t_i, since any such j would be caught (or
would be inside a fleet that is caught). Check every car against every car ahead: O(n^2)
time, O(1) space. The wasted work: "max arrival time among cars ahead" is recomputed from
scratch for each car instead of being carried along.

From brute force to optimal
---------------------------
The redundancy is re-deriving the slowest car ahead. Observation: sort cars by position
descending (closest to target first); then "cars ahead" is exactly the prefix already
processed, and the quantity we need is the arrival time of the fleet immediately ahead. Keep
a stack of fleet arrival times: if the current car's time is larger than the top it can never
catch that fleet and starts a new one (push); otherwise it merges and contributes nothing.
The stack is strictly increasing bottom to top, each car is handled once -- O(n log n) for
the sort, O(n) for the sweep.

Intuition
---------
Position in the queue is decided by the sort; whether you form your own fleet is decided
purely by comparing your solo arrival time with the fleet right in front of you. If you'd
arrive later, nobody ahead slows you down; if you'd arrive sooner, you get stuck behind them.

Geometric view
--------------
Draw each car as a line in a (time, position) plot from (0, p_i) to (t_i, target). Two lines
that cross before the target merge into one. Processing from the front, the stack holds the
arrival times of the surviving lines; a new line that would hit the target earlier than the
one in front gets absorbed, one that hits later stands alone.

Steps
-----
1. Pair positions with speeds; sort by position descending.
2. stack = [] of arrival times.
3. For each (pos, spd): time = (target - pos) / spd; if stack is empty or time > stack[-1],
   push time (new fleet); else skip (merges into the fleet ahead).
4. Return len(stack).

Complexity: O(n log n) time, O(n) space — dominated by the sort.
Pitfalls: Integer division of times; sorting ascending and then comparing with the wrong
neighbour; forgetting that merging with the fleet ahead means inheriting ITS time, not yours
(the stack top is left unchanged, which encodes exactly that).
"""
from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)   # closest to target first
        stack = []                                          # arrival times of fleet leaders
        for pos, spd in cars:
            time = (target - pos) / spd
            if not stack or time > stack[-1]:               # slower than the fleet ahead
                stack.append(time)
            # else: catches the fleet ahead and merges, inheriting its arrival time
        return len(stack)


def brute_force(target: int, position: List[int], speed: List[int]) -> int:
    n = len(position)
    fleets = 0
    for i in range(n):
        t_i = (target - position[i]) / speed[i]
        leader = True
        for j in range(n):                                  # rescans every car ahead of i
            if position[j] > position[i] and (target - position[j]) / speed[j] >= t_i:
                leader = False
        fleets += leader
    return fleets


if __name__ == "__main__":
    s = Solution()
    cases = [(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), (10, [3], [3]), (100, [0, 2, 4], [4, 2, 1]), (10, [6, 8], [3, 2]), (10, [0, 4, 2], [2, 1, 3])]
    assert s.carFleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
    assert s.carFleet(10, [3], [3]) == 1
    assert s.carFleet(100, [0, 2, 4], [4, 2, 1]) == 1
    assert s.carFleet(10, [6, 8], [3, 2]) == 2
    for c in cases:
        assert s.carFleet(*c) == brute_force(*c)
    print("ok")
