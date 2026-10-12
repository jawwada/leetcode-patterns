"""
Bucket Sort - Top K Frequent by Frequency Buckets

Return the k most frequent values of an array in any order (the answer is
unique), in O(n) instead of sorting by frequency:
[1, 1, 1, 2, 2, 3], k = 2 -> [1, 2].
"""


# --- algorithm ---
def top_k_frequent(nums, k):
    """Put each value in the bucket of its frequency, then read the buckets
    from the highest frequency down. O(n) time and space."""
    count = {}                              # value -> frequency
    for value in nums:
        count[value] = count.get(value, 0) + 1
    buckets = []                            # index = frequency
    for freq in range(len(nums) + 1):       # a frequency is at most n
        buckets.append([])
    for value in count:
        buckets[count[value]].append(value)
    result = []
    for freq in range(len(nums), 0, -1):    # most frequent first
        for value in buckets[freq]:
            result.append(value)
            if len(result) == k:
                return result
    return result


# --- try it ---
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))        # -> [1, 2]
print(top_k_frequent([4, 1, -1, 2, -1, 2, 3], 2))   # -> [-1, 2]
print(top_k_frequent([7, 7, 7], 1))                 # -> [7]
print(top_k_frequent([5], 1))                       # -> [5]
