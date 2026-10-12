"""
Capacity To Ship Packages Within D Days (basics: searches)
Return the smallest ship capacity that ships all packages, in order, within `days` days.
  weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days = 5  ->  15   (1+2+3+4+5 | 6+7 | 8 | 9 | 10)

Idea: binary search on the answer. A bigger ship never needs more days, so "fits in days"
      flips from False to True exactly once between max(weights) and sum(weights).
      Binary search for that flip, testing each guess with one greedy pass.

Pseudocode:
  lo, hi = max(weights), sum(weights)    # must lift the heaviest; one day for everything
  while lo < hi:
      mid = (lo + hi) // 2
      if can_ship(mid): hi = mid         # fits, try smaller (mid may be the answer)
      else:             lo = mid + 1     # too small
  return lo

  can_ship(cap): fill today's ship until the next package would overflow it,
                 then start a new day; fits if days used <= days

Time O(n log S) with S = sum(weights), space O(1).
"""


def can_ship(weights, days, cap):
    used, load = 1, 0                    # days used, weight on today's ship
    for w in weights:
        if load + w > cap:               # w would overflow: start a new day
            used += 1
            load = 0
        load += w
    return used <= days


def ship_within_days(weights, days):
    lo, hi = max(weights), sum(weights)  # the answer lies in [lo, hi]
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, days, mid):
            hi = mid                     # fits, try smaller (keep mid)
        else:
            lo = mid + 1                 # too small, go bigger
    return lo


if __name__ == "__main__":
    print(ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))  # 15
    print(ship_within_days([3, 2, 2, 4, 1, 4], 3))               # 6
    print(ship_within_days([1, 2, 3, 1, 1], 4))                  # 3
