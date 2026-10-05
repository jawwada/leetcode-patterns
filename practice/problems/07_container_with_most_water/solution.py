"""
Container With Most Water (LeetCode 11) - Medium
Area: two pointers
Key operations: pointers at both ends, area = shorter wall * width, move the shorter side inward

Given heights of n vertical lines at x = 0..n-1, choose two lines that together with the x-axis
form the container holding the most water: area = min(h[i], h[j]) * (j - i). Return that area.
Example: height = [1, 8, 6, 2, 5, 4, 8, 3, 7] -> 49 (walls at index 1 and 8: min(8, 7) * 7)
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(height: List[int]) -> int:
    """Evaluate every pair i < j. O(n^2): once the shorter of two walls is known, every pair that
    keeps that wall and is narrower is provably worse, yet all of them are still evaluated."""
    n = len(height)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            best = max(best, min(height[i], height[j]) * (j - i))
    return best


# --- optimal ---
def solve(height: List[int]) -> int:
    """Start with the widest container and record its area; then move the shorter wall inward, since
    every container that keeps the shorter wall is narrower and no taller. O(n) time, O(1) space."""
    lo, hi = 0, len(height) - 1
    best = 0
    log("height  " + "".join(f"{h:4d}" for h in height))
    while lo < hi:
        area = min(height[lo], height[hi]) * (hi - lo)
        best = max(best, area)
        log("        " + "".join("  L " if j == lo else "  R " if j == hi else "  ~ " if lo < j < hi else "    " for j in range(len(height))))
        log(f"    L={lo} ({height[lo]}) R={hi} ({height[hi]}): area = min({height[lo]}, {height[hi]}) * {hi - lo} = {area:3d}, best {best}")
        if height[lo] < height[hi]:
            lo += 1
            log(f"    left wall is shorter -> drop it, L -> {lo}")
        else:
            hi -= 1
            log(f"    right wall is shorter or equal -> drop it, R -> {hi}")
    return best


# --- demo ---
def demo():
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    return solve(height)


# --- tests ---
def tests():
    assert solve([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert solve([1, 1]) == 1
    assert solve([4, 3, 2, 1, 4]) == 16
    assert solve([1, 2, 1]) == 2
    assert solve([2, 3, 10, 5, 7, 8, 9]) == 36
    assert solve([5, 5, 5, 5]) == 15
    assert solve([5]) == 0
    assert solve([]) == 0
    import random
    for _ in range(200):
        a = [random.randint(0, 9) for _ in range(random.randint(0, 10))]
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "        if height[lo] < height[hi]:",
        "with":    "        if height[lo] > height[hi]:",
        "fix": "move the pointer on the shorter wall",
        "why": "Moving the taller wall keeps the short one, so the height stays capped while the width shrinks: on the example the wall of height 1 is kept to the end and the answer is far below 49.",
        "decoys": [
            {"line": "    lo, hi = 0, len(height) - 1", "change": "should be lo, hi = 0, len(height)"},
            {"line": "    while lo < hi:", "change": "should loop while lo <= hi"},
            {"line": "        best = max(best, area)", "change": "should be best = area"},
        ],
    },
    {
        "replace": "        area = min(height[lo], height[hi]) * (hi - lo)",
        "with":    "        area = max(height[lo], height[hi]) * (hi - lo)",
        "fix": "the water level is the shorter wall: min",
        "why": "Water spills over the shorter wall; with max the example gives 8 * 8 = 64 at the first step instead of 49.",
        "decoys": [
            {"line": "    best = 0", "change": "should start at min(height)"},
            {"line": "            hi -= 1", "change": "should be hi = lo + 1"},
            {"line": "    return best", "change": "should return the last area"},
        ],
    },
    {
        "replace": "        area = min(height[lo], height[hi]) * (hi - lo)",
        "with":    "        area = min(height[lo], height[hi]) * (hi - lo + 1)",
        "fix": "the width is hi - lo, not the column count",
        "why": "Counting both end columns inflates every area by one wall height: [1, 1] gives 2 instead of 1.",
        "decoys": [
            {"line": "        if height[lo] < height[hi]:", "change": "should compare with <= instead of <"},
            {"line": "            lo += 1", "change": "should be lo += 2"},
            {"line": "    lo, hi = 0, len(height) - 1", "change": "should be lo, hi = 1, len(height) - 1"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
