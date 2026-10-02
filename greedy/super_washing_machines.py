"""
Super Washing Machines (LeetCode 517)  — Hard
Pattern: Prefix-sum flow bound

Problem
-------
n washing machines in a row hold machines[i] dresses. In one move you may pick ANY number of
machines and have each pass ONE dress to an adjacent machine at the same time. Return the
minimum number of moves to equalise all machines, or -1 if impossible.
Example: [1,0,5] -> 3 ([1,0,5] -> [1,1,4] -> [2,1,3] -> [2,2,2]). [0,3,0] -> 2. [0,2,0] -> -1.

Brute force
-----------
BFS over machine states: from a state, every machine independently chooses to send one dress
left, right, or nothing (3^n combinations, legal only if it holds a dress), apply all choices
simultaneously, and stop at the first balanced state. The state space is every composition of the
total into n parts, so the search is exponential in both time and space. The wasted work: the
search re-discovers that the only quantity that matters is how many dresses must cross each
boundary between neighbours, which is fixed by the input before any move is made.

From brute force to optimal
---------------------------
Let target = total / n (impossible unless divisible). Two lower bounds, both exact. (1) Boundary
flow: the net number of dresses that must cross the boundary after machine i is the prefix sum
balance_i = sum(machines[0..i]) - (i+1) * target. Only one dress crosses a given boundary per
move in a given direction, so moves >= max |balance_i|. (2) Single source: a machine with
excess e = machines[i] - target passes exactly ONE dress per move, so it needs at least e moves
to shed its surplus: moves >= max e. A machine with a deficit is not a bound, because it can
receive from both neighbours in the same move. The larger of the two bounds is achievable (standard
constructive argument: every move, every machine with positive excess passes one dress toward the
side whose flow is still pending), so the answer is max over i of max(|balance_i|, excess_i).
That is one prefix-sum pass, O(n) time, O(1) space; the exponential search collapsed to a running
sum because flow across each boundary is determined, not chosen.

Intuition
---------
Think of the row as a pipeline. The imbalance to the left of each boundary must physically pass
through that boundary one dress per move, so the biggest left/right imbalance is a floor on the
moves. Separately, an overloaded machine can only shed one dress per move, so its surplus is also
a floor. Nothing else constrains the schedule, so the answer is the larger floor.

Geometric view
--------------
Plot the running balance (prefix excess) as a curve over the boundaries. Its highest peak or
deepest trough is the busiest boundary: that many dresses must march across it. Overlay the
per-machine excess bars; a single tall bar may also dominate because it drains one at a time.
The answer is the tallest feature on either plot.

Steps
-----
1. total = sum(machines); if total % n: return -1; target = total // n.
2. balance = 0; best = 0.
3. For each load: excess = load - target; balance += excess;
   best = max(best, abs(balance), excess).
4. Return best.

Complexity: O(n) time, O(1) space — a single prefix-sum pass.
Pitfalls: taking max(|balance|) only ([0,3,0] gives 1 instead of 2: the middle machine must shed
          2 dresses one per move); taking abs(excess) instead of excess ([3,0,3] gives 2 instead
          of 1: the middle deficit of 2 fills from both sides in one move); forgetting the
          divisibility check.
"""
from collections import deque
from itertools import product
from typing import List


class Solution:
    def findMinMoves(self, machines: List[int]) -> int:
        total, n = sum(machines), len(machines)
        if total % n:
            return -1
        target = total // n
        best = balance = 0
        for load in machines:
            excess = load - target
            balance += excess                 # net dresses that must cross the boundary to the right
            best = max(best, abs(balance), excess)   # a deficit can fill from both sides at once
        return best


def brute_force(machines: List[int]) -> int:
    """BFS over states; each move = every machine sends 0/1 dress left or right. Exponential."""
    n = len(machines)
    if sum(machines) % n:
        return -1
    goal = tuple([sum(machines) // n] * n)
    start = tuple(machines)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == goal:
            return dist[cur]
        options = [(0,) + ((-1, 1) if cur[i] else ()) for i in range(n)]   # -1 left, +1 right
        for choice in product(*options):
            nxt = list(cur)
            for i, d in enumerate(choice):
                if d and 0 <= i + d < n:
                    nxt[i] -= 1
                    nxt[i + d] += 1
            nxt = tuple(nxt)
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                queue.append(nxt)
    return -1


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([1, 0, 5], 3),
        ([0, 3, 0], 2),
        ([0, 2, 0], -1),
        ([4], 0),                 # edge: single machine
        ([0, 0, 11, 5], 8),       # single-excess bound dominates
        ([3, 0, 3], 1),           # edge: deficit fills from both sides in one move
    ]
    for machines, want in cases:
        assert s.findMinMoves(machines) == want, machines
        assert brute_force(machines) == want, machines

    random.seed(517)
    for _ in range(60):
        n = random.randint(1, 4)
        machines = [random.randint(0, 4) for _ in range(n)]
        assert s.findMinMoves(machines) == brute_force(machines), machines
    print("ok")
