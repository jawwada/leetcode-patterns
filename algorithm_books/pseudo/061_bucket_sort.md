---
rank: 61
slug: bucket_sort
---

Given an array and an integer `k`, return the `k` most frequent values in any order; the answer is guaranteed to be unique. In `[1, 1, 1, 2, 2, 3]` with `k = 2` the answer is `[1, 2]`.

Counting the frequencies with a map is the easy part. Ordering the distinct values by count with a sort costs `O(d log d)` for d distinct values, and the size-k heap of #19 costs `O(d log k)`. Bucket sort removes the comparisons altogether: a frequency is a whole number between 1 and n, so it can serve directly as an array index. Make `n + 1` empty buckets, drop each distinct value into `buckets[count[value]]`, and walk the buckets from n down to 1, collecting values until k of them are in hand. The bucket index already is the order, so nothing inside a bucket needs sorting.

Picture a shelf with one slot per possible frequency. Every distinct value lands in the slot of its own count, and reading the shelf from the right end reads the values from most to least frequent.

```text
nums = [1, 1, 1, 2, 2, 3], k = 2      count = {1: 3, 2: 2, 3: 1}
  freq      0     1     2     3     4     5     6
  bucket   [ ]   [3]   [2]   [1]   [ ]   [ ]   [ ]
           ←────────────────────────────────────── read from freq 6 down
  freq 6, 5, 4: empty
  freq 3: take 1      result [1]
  freq 2: take 2      result [1, 2]      k values: return
```

```pseudo
FUNCTION TopKFrequent(nums, k)
    count ← empty map                       // value → frequency
    FOR EACH value IN nums
        count[value] ← count.get(value, 0) + 1
    buckets ← empty list                    // index = frequency
    FOR freq FROM 0 TO len(nums)            // a frequency is at most n
        buckets.append(empty list)
    FOR EACH value IN count
        buckets[count[value]].append(value)
    result ← empty list
    FOR freq FROM len(nums) DOWNTO 1        // most frequent first
        FOR EACH value IN buckets[freq]
            result.append(value)
            IF len(result) = k
                RETURN result
    RETURN result
```

Counting takes `O(n)`, filling the buckets `O(d)`, and the walk visits at most `n + 1` buckets and takes k values, so the whole job is `O(n)` time and `O(n)` space. Signals: top k frequent, sort by frequency, and in general any sort key that is a small whole number bounded by n. General bucket sort spreads values over equal-width ranges instead of exact keys: n numbers spread evenly over `[low, high)` go into n buckets of width `(high - low) / n`, each bucket catches about one value, a tiny sort inside each bucket is cheap, and reading the buckets in order gives the sorted array in expected `O(n)`. Maximum Gap (LC 164) uses such buckets for a pigeonhole argument: the largest gap between sorted neighbors is at least the average gap `(max - min) / (n - 1)`, so with buckets no wider than that it never falls inside one bucket, and only each bucket's minimum and maximum matter. The classic mistake is making n buckets instead of `n + 1`: when one value fills the whole array, as in `[7, 7, 7]`, its frequency is 3 and `buckets[3]` does not exist.

*Practice:* LC 347 Top K Frequent Elements · LC 451 Sort Characters By Frequency · LC 692 Top K Frequent Words · LC 164 Maximum Gap
