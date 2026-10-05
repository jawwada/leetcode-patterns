"""
Split Array Largest Sum (LeetCode 410) - Hard
Chapter: binary_search
Pattern: Binary search on the answer

Split nums into k non-empty contiguous pieces so that the largest piece sum is as small as
possible, and return that smallest possible largest sum.
Example: nums = [7, 2, 5, 10, 8], k = 2 -> 18 (pieces [7, 2, 5] and [10, 8])
"""
import math                            # math.inf is a number bigger than everything


# --- brute force ---
def brute_force(nums, k):
    """Try every place to end the first piece and recurse on the rest. Exponential time."""
    return best_split(nums, 0, k)


def best_split(nums, start, pieces):
    """Smallest possible largest sum when nums[start:] is cut into `pieces` pieces."""
    if pieces == 1:
        return sum(nums[start:])              # the last piece takes everything that is left
    best = math.inf
    piece_sum = 0
    for end in range(start, len(nums) - pieces + 1):   # leave room for the other pieces
        piece_sum += nums[end]
        rest = best_split(nums, end + 1, pieces - 1)
        best = min(best, max(piece_sum, rest))
    return best


# --- optimal ---
def pieces_needed(nums, cap):
    """Greedy: fewest pieces when no piece may sum above cap. O(n) time."""
    count = 1
    current = 0
    for value in nums:
        if current + value > cap:         # this value would spill over: start a new piece
            count += 1
            current = 0
        current += value
    return count


def split_array(nums, k):
    """Binary search the cap: the smallest cap that needs at most k pieces. O(n log S)."""
    left = max(nums)                      # every element must fit in some piece
    right = sum(nums)                     # one piece holds everything
    while left < right:
        mid = (left + right) // 2
        if pieces_needed(nums, mid) <= k:
            right = mid                   # cap mid works: try a smaller cap
        else:
            left = mid + 1
    return left


# --- try the brute force ---
print(brute_force([7, 2, 5, 10, 8], 2))       # -> 18
print(brute_force([1, 2, 3, 4, 5], 2))        # -> 9
print(brute_force([1, 4, 4], 3))              # -> 4
print(brute_force([2, 3, 1, 2, 4, 3], 6))     # -> 4


# --- try the optimal ---
print(split_array([7, 2, 5, 10, 8], 2))       # -> 18
print(split_array([1, 2, 3, 4, 5], 2))        # -> 9
print(split_array([1, 4, 4], 3))              # -> 4
print(split_array([2, 3, 1, 2, 4, 3], 6))     # -> 4
