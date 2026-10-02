"""
Candy (LeetCode 135)  — Hard
Pattern: Two-pass greedy (left-to-right, right-to-left constraints)

Problem
-------
Children stand in a line with ratings. Each child gets at least one candy, and a child with a
higher rating than an immediate neighbour must get more candies than that neighbour. Return
the minimum total number of candies.
Example: ratings = [1,0,2] -> 5 (candies [2,1,2]). ratings = [1,2,2] -> 4 ([1,2,1]).

Brute force
-----------
Give everyone 1 candy, then repeatedly sweep the line: whenever a child is rated higher than
a neighbour but does not have more candy, raise them to neighbour + 1. Stop when a full sweep
changes nothing. Each sweep is O(n) and a strictly increasing run of length n can need O(n)
sweeps to propagate, so O(n^2) time, O(n) space. The waste is propagating a constraint one
cell per sweep when a single ordered pass could carry it the whole way.

From brute force to optimal
---------------------------
The constraints come in two independent families: "higher than my left neighbour -> more than
them" and "higher than my right neighbour -> more than them". Each family on its own is
solved by one directional pass: scanning left to right, if r[i] > r[i-1] set c[i] = c[i-1] + 1
else 1 — this is the minimal assignment satisfying only the left constraints. Scanning right
to left does the same for the right constraints. A child must satisfy both, so the smallest
value that works is the maximum of the two passes; taking the max never breaks either family
because each pass's value is already >= what its family requires and raising a child only
helps its own constraints while the neighbour's requirement was computed against the
neighbour's own (unchanged) pass value. Two linear passes, O(n), and the result is provably
minimal because every candy count equals the length of some increasing chain that forces it.

Intuition
---------
Think of each rating peak as the top of a hill. The number of candies a child needs equals the
longer of the two strictly increasing slopes that end at them: the climb from the left and the
climb from the right. One left-to-right pass measures the left climb, one right-to-left pass
measures the right climb, and the child takes the longer one. Nothing less would break a
neighbour rule; nothing more is required.

Geometric view
--------------
Plot ratings as terrain. The left pass paints a staircase rising along every ascending stretch
and dropping back to 1 whenever the terrain fails to rise. The right pass paints the mirror
staircase for descending stretches. Overlay the two: the final candy profile is the upper
envelope of both staircases, so a peak between two long slopes gets the taller of the two
stairs meeting under it.

Steps
-----
1. candies = [1] * n.
2. For i in 1..n-1: if ratings[i] > ratings[i-1]: candies[i] = candies[i-1] + 1.
3. For i in n-2..0: if ratings[i] > ratings[i+1]: candies[i] = max(candies[i], candies[i+1] + 1).
4. Return sum(candies).

Complexity: O(n) time, O(n) space — two linear passes over one auxiliary array.
Pitfalls: overwriting instead of taking max in the second pass (breaks left constraints at
peaks); giving equal ratings equal candy (equal neighbours have no constraint; the right-side
run restarts at 1); trying a single pass that tracks slopes — correct but fiddly to get right
under interview pressure.
"""
from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        candies = [1] * n
        for i in range(1, n):                        # satisfy "more than left neighbour"
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        for i in range(n - 2, -1, -1):               # satisfy "more than right neighbour"
            if ratings[i] > ratings[i + 1]:
                # max keeps the left-pass value where it is already larger
                candies[i] = max(candies[i], candies[i + 1] + 1)
        return sum(candies)


def brute_force(ratings: List[int]) -> int:
    n = len(ratings)
    candies = [1] * n
    changed = True
    while changed:                                   # repeat until no rule is violated
        changed = False
        for i in range(n):
            for j in (i - 1, i + 1):
                if 0 <= j < n and ratings[i] > ratings[j] and candies[i] <= candies[j]:
                    candies[i] = candies[j] + 1
                    changed = True
    return sum(candies)


if __name__ == "__main__":
    s = Solution()
    assert s.candy([1, 0, 2]) == 5
    assert s.candy([1, 2, 2]) == 4
    assert s.candy([1]) == 1
    assert s.candy([5, 4, 3, 2, 1]) == 15
    assert s.candy([1, 3, 2, 2, 1]) == 7
    assert s.candy([2, 2, 2]) == 3
    import random
    random.seed(135)
    for _ in range(300):
        ratings = [random.randint(0, 5) for _ in range(random.randint(1, 15))]
        assert s.candy(ratings) == brute_force(ratings)
    print("ok")
