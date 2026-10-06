"""
Split Array Largest Sum (LeetCode 410)
Split nums into k contiguous pieces so the largest piece sum is as small as possible.
  nums = [7, 2, 5, 10, 8], k = 2  ->  18   ([7, 2, 5] | [10, 8])

Idea: guess a cap on the piece sum. Greedily fill pieces up to the cap and count
      them; a bigger cap never needs more pieces, so binary search the cap.

Pseudocode:
  lo, hi = max(nums), sum(nums)
  while lo < hi:
      cap = (lo + hi) // 2
      if pieces_needed(cap) <= k: hi = cap   # cap works, try smaller
      else: lo = cap + 1
  return lo
  pieces_needed(cap): start new piece when adding x would exceed cap

Time O(n log sum), space O(1).
"""


def split_array(nums, k):
    def pieces_needed(cap):
        pieces, current = 1, 0
        for x in nums:
            if current + x > cap:        # x doesn't fit: start a new piece
                pieces += 1
                current = 0
            current += x
        return pieces

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        cap = (lo + hi) // 2
        if pieces_needed(cap) <= k:
            hi = cap                     # cap works, try smaller
        else:
            lo = cap + 1                 # too many pieces, raise cap
    return lo


if __name__ == "__main__":
    print(split_array([7, 2, 5, 10, 8], 2))  # 18
    print(split_array([1, 2, 3, 4, 5], 2))   # 9
    print(split_array([1, 4, 4], 3))         # 4
