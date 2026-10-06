"""
Counting Sort and Bucket Sort (basics: sorting)
Sort small non-negative ints by counting them, and floats in [0, 1) by dropping them into buckets.
  counting_sort([2, 5, 3, 0, 2, 3, 0, 3])      ->  [0, 0, 2, 2, 3, 3, 3, 5]
  bucket_sort([0.78, 0.17, 0.39, 0.72, 0.26])  ->  [0.17, 0.26, 0.39, 0.72, 0.78]

Idea: use the value itself as an address instead of comparing items with each other.
      Counting sort: counts[v] = how often v occurs; walk counts in index order.
      Bucket sort: bucket int(x * n) grows with x, so sorted buckets joined in order are sorted.

Pseudocode:
  counting_sort(nums):
      counts = [0] * (max + 1); for x in nums: counts[x] += 1
      for v in 0..max: emit v, counts[v] times

  bucket_sort(xs):
      n = len(xs); make n empty buckets
      for x in xs: insert x into buckets[int(x * n)] at its sorted spot
      join the buckets in order

Time O(n + k) for counting (k = max value); O(n) expected for bucket when values are
spread evenly (O(n^2) if they all land in one bucket). Space O(n + k) and O(n).
"""


def counting_sort(nums):
    if not nums:
        return []
    counts = [0] * (max(nums) + 1)       # one slot per value 0..max
    for x in nums:
        counts[x] += 1
    out = []
    for v, c in enumerate(counts):       # values in increasing order
        out += [v] * c                   # emit v, c times
    return out


def bucket_sort(xs):
    n = len(xs)
    buckets = [[] for _ in range(n)]
    for x in xs:
        b = buckets[int(x * n)]          # bucket index grows with x
        i = len(b)
        while i > 0 and b[i - 1] > x:    # insertion sort: find x's spot
            i -= 1
        b.insert(i, x)
    out = []
    for b in buckets:
        out += b                         # bucket order = value order
    return out


if __name__ == "__main__":
    print(counting_sort([2, 5, 3, 0, 2, 3, 0, 3]))      # [0, 0, 2, 2, 3, 3, 3, 5]
    print(bucket_sort([0.78, 0.17, 0.39, 0.72, 0.26]))  # [0.17, 0.26, 0.39, 0.72, 0.78]
