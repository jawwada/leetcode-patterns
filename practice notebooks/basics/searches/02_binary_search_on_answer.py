"""
Capacity To Ship Packages Within D Days (LeetCode 1011) - Basics
Area: searches
Key operations: monotone feasible(cap), search the answer range [max, sum], hi = mid when feasible, lo = mid + 1 when not

Packages must be shipped in the given order within `days` days; each day one ship carries consecutive
packages up to its capacity. Return the smallest capacity that works. feasible(cap) is monotone: once a
capacity works, every larger one works, so binary search finds the smallest feasible capacity.
Example: weights [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days 5 -> 15 (loads 1..5 | 6,7 | 8 | 9 | 10)
"""
from typing import List


# --- brute force ---
def brute_force(weights: List[int], days: int) -> int:
    """Try every capacity from max(weights) upward and count days greedily. O(sum * n); the search over capacities is linear."""
    for cap in range(max(weights), sum(weights) + 1):
        used, load = 1, 0
        for w in weights:
            if load + w > cap:
                used, load = used + 1, 0
            load += w
        if used <= days:
            return cap


# --- optimal ---
def feasible(weights, days, cap):
    """Greedy: keep loading the current ship until the next package overflows it. O(n)."""
    loads = [0]
    for w in weights:
        if loads[-1] + w > cap:
            loads.append(0)
        loads[-1] += w
    return len(loads) <= days


def solve(weights, days):
    """Binary search the smallest feasible capacity in [max(weights), sum(weights)]. O(n log sum)."""
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(weights, days, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# --- demo ---
def demo():
    return solve([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)


# --- bugs ---
BUGS = [
    {
        "replace": "        if loads[-1] + w > cap:",
        "with":    "        if loads[-1] + w >= cap:",
        "fix": "start a new ship only when the package would OVERFLOW the capacity; an exact fill is allowed",
        "why": "A ship filled exactly to cap is counted as overflowing, so one extra day is needed: [2, 3, 2, 3] in 2 days answers 6 instead of 5.",
        "decoys": [
            {"line": "        loads[-1] += w", "change": "should be loads.append(w)"},
            {"line": "    return len(loads) <= days", "change": "should be < days"},
            {"line": "    loads = [0]", "change": "should start as []"},
        ],
    },
    {
        "replace": "            hi = mid",
        "with":    "            hi = mid - 1",
        "fix": "a feasible mid may itself be the answer, so keep it in the range: hi = mid",
        "why": "Excluding a feasible mid throws away the smallest feasible capacity: [1, 2, 3, 1, 1] in 4 days returns 4 instead of 3.",
        "decoys": [
            {"line": "            lo = mid + 1", "change": "should be lo = mid"},
            {"line": "    lo, hi = max(weights), sum(weights)", "change": "should start lo at 1"},
            {"line": "    while lo < hi:", "change": "should be lo <= hi"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
