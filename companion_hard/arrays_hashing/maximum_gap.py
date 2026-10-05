"""
Maximum Gap (LeetCode 164) - Hard
Chapter: arrays_hashing
Pattern: Pigeonhole buckets

Given an unsorted integer array, return the largest difference between two neighbours in
its sorted order, in linear time; return 0 if there are fewer than two elements.
Example: [3, 6, 9, 1] -> 3 (sorted 1, 3, 6, 9 has gaps 2, 3, 3).
"""


# --- brute force ---
def brute_force(nums):
    """Sort, then take the largest neighbour difference. O(n log n) time, O(n) space."""
    ordered = sorted(nums)
    best = 0
    for i in range(1, len(ordered)):
        gap = ordered[i] - ordered[i - 1]
        best = max(best, gap)
    return best


# --- optimal ---
def maximum_gap(nums):
    """Buckets narrower than the answer: only gaps between buckets matter. O(n) time and space."""
    n = len(nums)
    if n < 2:
        return 0
    lo = min(nums)
    hi = max(nums)
    # the max gap is at least the average gap, so it never sits inside one bucket of this width
    width = max(1, (hi - lo) // (n - 1))
    count = (hi - lo) // width + 1
    bucket_min = [None] * count
    bucket_max = [None] * count
    for x in nums:
        b = (x - lo) // width
        if bucket_min[b] is None or x < bucket_min[b]:
            bucket_min[b] = x
        if bucket_max[b] is None or x > bucket_max[b]:
            bucket_max[b] = x
    best = 0
    prev_max = lo
    for b in range(count):
        if bucket_min[b] is None:
            continue  # empty bucket: the gap spans it
        best = max(best, bucket_min[b] - prev_max)
        prev_max = bucket_max[b]
    return best


# --- try the brute force ---
print(brute_force([3, 6, 9, 1]))     # -> 3
print(brute_force([10]))             # -> 0
print(brute_force([1, 1, 1, 1]))     # -> 0
print(brute_force([1, 3, 100]))      # -> 97


# --- try the optimal ---
print(maximum_gap([3, 6, 9, 1]))     # -> 3
print(maximum_gap([10]))             # -> 0
print(maximum_gap([1, 1, 1, 1]))     # -> 0
print(maximum_gap([1, 3, 100]))      # -> 97
