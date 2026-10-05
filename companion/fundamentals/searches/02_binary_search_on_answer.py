"""
Capacity To Ship Packages Within D Days (LeetCode 1011) - Fundamentals
Chapter: fundamentals/searches
Key operations: monotone can_ship(cap), search [max, sum], hi = mid if feasible else lo = mid + 1

Packages must be shipped in the given order within `days` days; each day one ship carries
consecutive packages up to its capacity. Return the smallest capacity that works. can_ship(cap) is
monotone: once a capacity works, every larger one works, so binary search finds the smallest one.
Example: weights [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days 5 -> 15 (loads 1..5 | 6,7 | 8 | 9 | 10)
"""


# --- algorithm ---
def can_ship(weights, days, cap):
    """Greedy: keep loading the current ship until the next package overflows it. O(n)."""
    ships = 1
    load = 0
    for w in weights:
        if load + w > cap:             # this package does not fit: start a new ship
            ships += 1
            load = 0
        load += w
    return ships <= days


def ship_within_days(weights, days):
    """Binary search the smallest feasible capacity in [max, sum] of weights. O(n log sum)."""
    lo = max(weights)                  # anything smaller cannot carry the heaviest package
    hi = sum(weights)                  # one ship takes everything, always feasible
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, days, mid):
            hi = mid                   # mid works; a smaller capacity might still work
        else:
            lo = mid + 1               # mid fails, so does everything below it
    return lo


# --- try it ---
print(ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))   # -> 15
print(ship_within_days([3, 2, 2, 4, 1, 4], 3))                # -> 6
print(ship_within_days([1, 2, 3, 1, 1], 4))                   # -> 3
print(can_ship([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 14))       # -> False
