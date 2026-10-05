"""
Koko Eating Bananas (LeetCode 875) - Medium
Chapter: binary_search
Pattern: Binary search on the answer

piles[i] bananas sit in pile i. Each hour Koko picks one pile and eats up to k bananas from it;
a pile with fewer than k is finished in that hour. Return the minimum integer speed k that lets
her finish every pile within h hours.
Example: piles = [3, 6, 7, 11], h = 8 -> 4 (hours at k = 4: 1 + 2 + 2 + 3 = 8)
"""


# --- brute force ---
def brute_force(piles, h):
    """Try speed 1, 2, 3, ... and return the first that finishes in time. O(n * max(piles))."""
    speed = 1
    while True:
        hours = 0
        for pile in piles:
            hours += (pile + speed - 1) // speed   # pile / speed rounded up
        if hours <= h:
            return speed
        speed += 1


# --- optimal ---
def hours_needed(piles, speed):
    """Hours to finish every pile at this speed. O(n)."""
    hours = 0
    for pile in piles:
        hours += (pile + speed - 1) // speed   # pile / speed rounded up
    return hours


def koko_eating_bananas(piles, h):
    """Binary search the speed: 'finishes in time' reads False...True. O(n log max(piles))."""
    left = 1
    right = max(piles)                  # one pile per hour always works
    while left < right:
        mid = (left + right) // 2
        if hours_needed(piles, mid) <= h:
            right = mid                 # fast enough: mid may be the answer, try slower
        else:
            left = mid + 1              # too slow: every speed up to mid fails
    return left


# --- try the brute force ---
print(brute_force([3, 6, 7, 11], 8))          # -> 4
print(brute_force([30, 11, 23, 4, 20], 5))    # -> 30
print(brute_force([30, 11, 23, 4, 20], 6))    # -> 23
print(brute_force([5, 5, 5], 3))              # -> 5


# --- try the optimal ---
print(koko_eating_bananas([3, 6, 7, 11], 8))          # -> 4
print(koko_eating_bananas([30, 11, 23, 4, 20], 5))    # -> 30
print(koko_eating_bananas([30, 11, 23, 4, 20], 6))    # -> 23
print(koko_eating_bananas([5, 5, 5], 3))              # -> 5
