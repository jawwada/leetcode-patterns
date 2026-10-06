"""
Koko Eating Bananas (LeetCode 875)
Find the smallest eating speed k so all piles are finished within h hours.
  piles = [3, 6, 7, 11], h = 8  ->  4   (hours 1 + 2 + 2 + 3 = 8)

Idea: faster speed never needs more hours, so "fits in h" flips from False to True
      once. Binary search the speed between 1 and max(piles).

Pseudocode:
  lo, hi = 1, max(piles)
  while lo < hi:
      mid = (lo + hi) // 2
      if hours(mid) <= h: hi = mid     # fast enough, try slower
      else: lo = mid + 1               # too slow
  return lo
  hours(k) = sum of ceil(pile / k)

Time O(n log max), space O(1).
"""


def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum((p + mid - 1) // mid for p in piles)   # ceil(p / mid)
        if hours <= h:
            hi = mid                     # fast enough, try slower
        else:
            lo = mid + 1                 # too slow, go faster
    return lo


if __name__ == "__main__":
    print(min_eating_speed([3, 6, 7, 11], 8))         # 4
    print(min_eating_speed([30, 11, 23, 4, 20], 5))   # 30
    print(min_eating_speed([30, 11, 23, 4, 20], 6))   # 23
