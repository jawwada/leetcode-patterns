"""
Koko Eating Bananas (LeetCode 875) - Medium
Area: binary search
Key operations: hours(speed) by ceiling division, binary search on the answer, hi = mid when feasible, lo = mid + 1 when not

piles[i] bananas sit in pile i. Each hour Koko picks one pile and eats up to k bananas from it
(if fewer remain she finishes the pile and waits for the hour to end). Return the minimum
integer speed k at which she finishes every pile within h hours.
Example: piles = [3, 6, 7, 11], h = 8 -> 4 (hours at speed 4: 1 + 2 + 2 + 3 = 8)
"""
from typing import List


# --- brute force ---
def brute_force(piles: List[int], h: int) -> int:
    """Try k = 1, 2, 3, ... and return the first speed whose total hours fit in h.
    O(n * max(piles)): every speed below the answer is checked although once a speed works all
    faster speeds work too, so most checks only confirm what a halving step could skip."""
    k = 1
    while sum((p + k - 1) // k for p in piles) > h:
        k += 1
    return k


# --- optimal ---
def solve(piles: List[int], h: int) -> int:
    """hours(k) never grows as k grows, so feasible(k) = hours(k) <= h reads F..F T..T over the
    speeds 1..max(piles): binary search for the first T. O(n log max(piles)) time, O(1) space."""
    def hours(speed: int) -> int:
        return sum((p + speed - 1) // speed for p in piles)  # ceil(p / speed) hours per pile

    lo, hi = 1, max(piles)  # speed max(piles) always works: one hour per pile
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo


# --- demo ---
def demo():
    return solve([3, 6, 7, 11], 8)


# --- bugs ---
BUGS = [
    {
        "replace": "        if hours(mid) <= h:",
        "with":    "        if hours(mid) < h:",
        "fix": "a speed that uses exactly h hours is feasible: compare with <=",
        "why": "Using every hour of the budget is allowed; with < the speed that needs exactly h hours is rejected and the answer is one too fast, [3, 6, 7, 11] with h = 8 gives 5 instead of 4.",
        "decoys": [
            {"line": "    lo, hi = 1, max(piles)  # speed max(piles) always works: one hour per pile", "change": "should be hi = sum(piles)"},
            {"line": "        mid = (lo + hi) // 2", "change": "should be (lo + hi + 1) // 2"},
            {"line": "    return lo", "change": "should return hi"},
        ],
    },
    {
        "replace": "            hi = mid",
        "with":    "            hi = mid - 1",
        "fix": "keep mid in the range: it is feasible and may be the answer, so hi = mid",
        "why": "A feasible mid can be the minimum speed; excluding it lets lo climb to an infeasible speed, [30, 11, 23, 4, 20] with h = 6 returns 22 instead of 23.",
        "decoys": [
            {"line": "            lo = mid + 1", "change": "should be lo = mid"},
            {"line": "    while lo < hi:", "change": "should be lo <= hi"},
            {"line": "        return sum((p + speed - 1) // speed for p in piles)  # ceil(p / speed) hours per pile", "change": "should be p // speed"},
        ],
    },
    {
        "replace": "            lo = mid + 1",
        "with":    "            lo = mid",
        "fix": "mid is too slow, so exclude it: lo = mid + 1",
        "why": "When hi == lo + 1, mid equals lo, so lo = mid never moves and the loop runs forever.",
        "decoys": [
            {"line": "            hi = mid", "change": "should be hi = mid + 1"},
            {"line": "        if hours(mid) <= h:", "change": "should be >= h"},
            {"line": "    lo, hi = 1, max(piles)  # speed max(piles) always works: one hour per pile", "change": "should be lo = 0"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
