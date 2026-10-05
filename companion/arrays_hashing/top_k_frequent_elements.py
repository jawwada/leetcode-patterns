"""
Top K Frequent Elements (LeetCode 347) - Medium
Chapter: arrays_hashing
Pattern: Frequency count + bucket sort

Given an integer array nums and an integer k, return the k most frequent elements in
any order; the answer is guaranteed to be unique.
Example: nums = [1, 1, 1, 2, 2, 3], k = 2 -> [1, 2].
"""


# --- helpers ---
def count_values(nums):
    """Return a dict value -> how many times it appears."""
    freq = {}
    for value in nums:
        freq[value] = freq.get(value, 0) + 1
    return freq


# --- brute force ---
def brute_force(nums, k):
    """Count, then sort every distinct value by frequency. O(n log n) time, O(n) space."""
    freq = count_values(nums)
    pairs = []
    for value in freq:
        pairs.append((freq[value], value))
    pairs.sort(reverse=True)  # highest frequency first
    result = []
    for i in range(k):
        result.append(pairs[i][1])
    return result


# --- optimal ---
def top_k_frequent(nums, k):
    """Bucket values by frequency, read buckets from the top. O(n) time, O(n) space."""
    freq = count_values(nums)
    buckets = []  # buckets[c] holds the values that appear exactly c times
    for _ in range(len(nums) + 1):
        buckets.append([])
    for value in freq:
        buckets[freq[value]].append(value)
    result = []
    for count in range(len(nums), 0, -1):  # walk from the highest frequency down
        for value in buckets[count]:
            result.append(value)
            if len(result) == k:
                return result
    return result


# --- try the brute force ---
print(sorted(brute_force([1, 1, 1, 2, 2, 3], 2)))            # -> [1, 2]
print(sorted(brute_force([1], 1)))                           # -> [1]
print(sorted(brute_force([4, 4, 4, 5, 5, 6, 6, 6, 6], 2)))   # -> [4, 6]
print(sorted(brute_force([7, 7, 7, 7], 1)))                  # -> [7]


# --- try the optimal ---
print(sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)))            # -> [1, 2]
print(sorted(top_k_frequent([1], 1)))                           # -> [1]
print(sorted(top_k_frequent([4, 4, 4, 5, 5, 6, 6, 6, 6], 2)))   # -> [4, 6]
print(sorted(top_k_frequent([7, 7, 7, 7], 1)))                  # -> [7]
