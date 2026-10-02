"""
Minimum Number of Taps to Open to Water a Garden (LeetCode 1326)  — Hard
Pattern: Greedy reach (furthest reachable index)

Problem
-------
A garden is the segment [0, n]. Tap i (0 <= i <= n) waters [i - ranges[i], i + ranges[i]].
Return the minimum number of taps to open so the whole garden is watered, or -1 if impossible.
Example: n = 5, ranges = [3,4,1,1,0,0] -> 1 (tap 1 waters [-3, 5]).
n = 3, ranges = [0,0,0,0] -> -1.

Brute force
-----------
Try every subset of taps in increasing size and check whether the union of their intervals covers
[0, n]. 2^(n+1) subsets, each checked in O(n), so exponential time and O(n) space. The wasted
work: a tap is useless unless it covers the leftmost still-dry point, and among taps that do,
only the one reaching furthest right matters — the subsets never exploit that.

From brute force to optimal
---------------------------
Reformulate: tap i is the interval [max(0, i - r), i + r]. Build reach[l] = the furthest right end
of any interval that starts at l (O(n)). Now standing at point l with everything to the left wet,
"jump" to reach[l] is exactly Jump Game II: positions reachable with j taps form a contiguous
prefix [0, cur_end], and the next tap extends it to the max of reach over that prefix. Scan i from
0 to n-1 maintaining farthest = max(reach[0..i]); whenever i == cur_end we must open another tap,
and if farthest == i nothing can get us past i, return -1. The two optimisation steps: subsets ->
interval covering sorted by start (O(n log n), the classic greedy) -> noticing the starts are
already bucketed by integer position, so a plain array replaces the sort (O(n)).

Intuition
---------
Convert each tap into "from position l you can jump to position reach[l]". Watering the whole
garden with the fewest taps is reaching index n with the fewest jumps. Each BFS level is the
prefix watered with j taps; the next level's right edge is the furthest any tap starting inside
the current prefix can reach.

Geometric view
--------------
Draw the garden as a number line and each tap as a horizontal bar. Walk left to right carrying
the current wet frontier cur_end. While walking you note the longest bar that starts at or before
your position; when you step onto cur_end you must open the tap owning that longest bar, and the
frontier jumps to its right end. If the longest bar does not extend past your position, the dry
point right after it can never be wetted.

Steps
-----
1. reach = [0] * (n + 1); for each tap i: l = max(0, i - ranges[i]); reach[l] = max(reach[l],
   i + ranges[i]).
2. taps = cur_end = farthest = 0.
3. For i in range(n): farthest = max(farthest, reach[i]).
4.   If i == cur_end: if farthest <= i return -1; taps += 1; cur_end = farthest.
5. Return taps.

Complexity: O(n) time, O(n) space — one pass to bucket intervals by start, one Jump Game II
            scan.
Pitfalls: not clamping the left end at 0 (negative indices wrap in Python); iterating to n
          inclusive and counting a spurious tap; checking farthest <= i AFTER incrementing taps
          (returns a count instead of -1); forgetting the single-point garden n = 0 needs 0 taps.
"""
from itertools import combinations
from typing import List


class Solution:
    def minTaps(self, n: int, ranges: List[int]) -> int:
        reach = [0] * (n + 1)                 # reach[l] = furthest right end of a tap starting at l
        for i, r in enumerate(ranges):
            left = max(0, i - r)
            reach[left] = max(reach[left], i + r)

        taps = cur_end = farthest = 0         # Jump Game II over reach[]
        for i in range(n):                    # position n itself needs no further tap
            farthest = max(farthest, reach[i])
            if i == cur_end:                  # end of the current wet prefix: must open a tap
                if farthest <= i:             # no tap gets past i -> dry gap
                    return -1
                taps += 1
                cur_end = farthest
        return taps


def brute_force(n: int, ranges: List[int]) -> int:
    """Try every subset of taps by increasing size (exponential), check coverage of [0, n]."""
    taps = list(range(n + 1))
    for size in range(0, n + 2):
        for chosen in combinations(taps, size):
            wet = [False] * n                       # wet[p] = unit segment [p, p+1] watered
            for i in chosen:
                for p in range(max(0, i - ranges[i]), min(n, i + ranges[i])):
                    wet[p] = True
            if all(wet):
                return size
    return -1


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        (5, [3, 4, 1, 1, 0, 0], 1),
        (3, [0, 0, 0, 0], -1),
        (7, [1, 2, 1, 0, 2, 1, 0, 1], 3),
        (8, [4, 0, 0, 0, 0, 0, 0, 0, 4], 2),
        (0, [0], 0),                              # edge: single-point garden
        (5, [0, 1, 0, 0, 1, 0], -1),             # edge: segment [2,3] stays dry
    ]
    for n, ranges, want in cases:
        assert s.minTaps(n, ranges) == want, (n, ranges)
        assert brute_force(n, ranges) == want, (n, ranges)

    random.seed(1326)
    for _ in range(300):
        n = random.randint(0, 8)
        ranges = [random.randint(0, 3) for _ in range(n + 1)]
        assert s.minTaps(n, ranges) == brute_force(n, ranges), (n, ranges)
    print("ok")
