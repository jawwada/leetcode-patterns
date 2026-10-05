"""
Counting Sort and Bucket Sort - Fundamentals
Chapter: fundamentals/sorting
Key operations: count by value, emit each value count times, bucket by int(x * n), sort buckets

Two non-comparison sorts. Counting sort for small non-negative ints: counts[v] is how often v
occurs, then walk the counts in order; O(n + k) with k the max value. Bucket sort for floats in
[0, 1): bucket index int(x * n) grows with x, so sorting each bucket and concatenating sorts all.
Example: [2, 5, 3, 0, 2, 3, 0, 3] -> [0, 0, 2, 2, 3, 3, 3, 5]
         [0.78, 0.17, 0.39, 0.26, 0.72] -> [0.17, 0.26, 0.39, 0.72, 0.78]
"""


# --- algorithm ---
def counting_sort(nums):
    """Index by value: counts[v] copies of v, emitted in index order. O(n + max)."""
    if not nums:
        return []
    counts = [0] * (max(nums) + 1)     # values run 0..max inclusive, so max + 1 slots
    for x in nums:
        counts[x] += 1
    out = []
    for value in range(len(counts)):
        for _ in range(counts[value]):
            out.append(value)
    return out


def bucket_sort(xs):
    """n buckets over [0, 1); int(x * n) grows with x, so bucket order is value order. O(n) avg."""
    n = len(xs)
    buckets = []
    for _ in range(n):
        buckets.append([])
    for x in xs:
        buckets[int(x * n)].append(x)
    out = []
    for bucket in buckets:
        out.extend(sorted(bucket))     # a bucket only groups nearby values; it still needs sorting
    return out


# --- try it ---
print(counting_sort([2, 5, 3, 0, 2, 3, 0, 3]))            # -> [0, 0, 2, 2, 3, 3, 3, 5]
print(counting_sort([1, 0]))                              # -> [0, 1]
print(bucket_sort([0.78, 0.17, 0.39, 0.26, 0.72]))        # -> [0.17, 0.26, 0.39, 0.72, 0.78]
print(bucket_sort([0.94, 0.21, 0.12, 0.23, 0.68, 0.11]))  # -> [0.11, 0.12, 0.21, 0.23, 0.68, 0.94]
