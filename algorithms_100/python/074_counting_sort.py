"""
Counting Sort - Count, Prefix-Sum, Place

Sort integers that lie in a small range [low, high], negatives included,
without comparing them: [2, -1, 3, 2, 0, -1] -> [-1, -1, 0, 2, 2, 3].
"""


# --- algorithm ---
def counting_sort(nums):
    """Count each value, turn the counts into end positions, place each value.
    O(n + k) time and space for k = high - low + 1 possible values."""
    if len(nums) == 0:
        return []
    low = min(nums)
    high = max(nums)
    count = [0] * (high - low + 1)          # count[v - low] is for value v
    for value in nums:
        count[value - low] += 1
    for slot in range(1, len(count)):       # now: how many values are <= it
        count[slot] += count[slot - 1]
    result = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):  # right to left keeps it stable
        value = nums[i]
        count[value - low] -= 1             # the last free seat
        result[count[value - low]] = value
    return result


# --- try it ---
print(counting_sort([2, -1, 3, 2, 0, -1]))   # -> [-1, -1, 0, 2, 2, 3]
print(counting_sort([5, 3, 5, 1]))           # -> [1, 3, 5, 5]
print(counting_sort([4]))                    # -> [4]
print(counting_sort([]))                     # -> []
