"""
Binary Search on the Answer - Search a Monotone Yes/No Predicate

Koko eats k bananas per hour from a single pile; when fewer than k are left
in that pile she still spends the whole hour on it. Return the smallest k
that finishes every pile within h hours (h is at least the number of piles):
piles [3, 6, 7, 11], h 8 -> 4.
"""
import math                         # math.ceil rounds a division up


# --- algorithm ---
def can_finish(piles, h, speed):
    """The yes/no check: are all piles eaten within h hours? O(n)."""
    hours = 0
    for pile in piles:
        hours += math.ceil(pile / speed)    # a partial hour costs a full hour
    return hours <= h


def min_eating_speed(piles, h):
    """First speed in [1, max(piles)] where can_finish says yes.
    O(n log m) for m = max(piles)."""
    lo = 1                          # the slowest possible speed
    hi = max(piles)                 # one pile per hour: always fast enough
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(piles, h, mid):
            hi = mid                # mid works; a slower speed might too
        else:
            lo = mid + 1            # mid fails, and so does every speed below
    return lo


# --- try it ---
print(min_eating_speed([3, 6, 7, 11], 8))           # -> 4
print(min_eating_speed([30, 11, 23, 4, 20], 5))     # -> 30
print(min_eating_speed([30, 11, 23, 4, 20], 6))     # -> 23
print(can_finish([3, 6, 7, 11], 8, 3))              # -> False
