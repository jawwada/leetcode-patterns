"""
Minimum Number of Taps to Open to Water a Garden (LeetCode 1326) - Hard
Chapter: greedy
Pattern: Greedy reach (furthest reachable index)

A garden is the segment [0, n]. Tap i (0 <= i <= n) waters [i - ranges[i], i + ranges[i]].
Return the minimum number of taps to open so the whole garden is watered, or -1 if impossible.
Example: n = 5, ranges = [3,4,1,1,0,0] -> 1 (tap 1 waters [-3, 5]); n = 3, ranges = [0,0,0,0] -> -1
"""
from itertools import combinations   # every subset of a given size


# --- brute force ---
def brute_force(n, ranges):
    """Try every subset of taps by increasing size, check it waters all of [0, n]. O(2^n n)."""
    taps = list(range(n + 1))
    for size in range(0, n + 2):
        for chosen in combinations(taps, size):
            if waters_everything(n, ranges, chosen):
                return size                       # smallest size first: the first hit wins
    return -1


def waters_everything(n, ranges, chosen):
    wet = [False] * n                             # wet[p] = the unit segment [p, p + 1] is watered
    for i in chosen:
        left = max(0, i - ranges[i])
        right = min(n, i + ranges[i])
        for p in range(left, right):
            wet[p] = True
    for p in range(n):
        if not wet[p]:
            return False
    return True


# --- optimal ---
def min_taps(n, ranges):
    """reach[left] = furthest a tap starting at left waters; then jump like Jump Game II. O(n)."""
    reach = [0] * (n + 1)
    for i in range(n + 1):
        left = max(0, i - ranges[i])
        reach[left] = max(reach[left], i + ranges[i])
    taps = 0
    current_end = 0                               # everything up to here is wet with `taps` taps
    farthest = 0                                  # furthest point any tap seen so far can reach
    for i in range(n):                            # position n needs no tap beyond it
        farthest = max(farthest, reach[i])
        if i == current_end:                      # edge of the wet prefix: one more tap is needed
            if farthest <= i:
                return -1                         # nothing reaches past i: a dry gap
            taps += 1
            current_end = farthest
    return taps


# --- try the brute force ---
print(brute_force(5, [3, 4, 1, 1, 0, 0]))               # -> 1
print(brute_force(3, [0, 0, 0, 0]))                     # -> -1
print(brute_force(7, [1, 2, 1, 0, 2, 1, 0, 1]))         # -> 3
print(brute_force(8, [4, 0, 0, 0, 0, 0, 0, 0, 4]))      # -> 2


# --- try the optimal ---
print(min_taps(5, [3, 4, 1, 1, 0, 0]))                  # -> 1
print(min_taps(3, [0, 0, 0, 0]))                        # -> -1
print(min_taps(7, [1, 2, 1, 0, 2, 1, 0, 1]))            # -> 3
print(min_taps(8, [4, 0, 0, 0, 0, 0, 0, 0, 4]))         # -> 2
