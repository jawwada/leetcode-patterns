---
rank: 40
slug: median_two_sorted_arrays
---

Given two sorted arrays `a` and `b` of lengths `m` and `n`, with at least one value between them, return the median of all `m + n` values in `O(log(m + n))` time. For `[1, 3, 8, 9, 15]` and `[7, 11, 18, 19, 21, 25]` the eleven values in order are `1 3 7 8 9 11 15 18 19 21 25`, so the median is `11`; with an even total it is the average of the two middle values.

The brute force merges the two arrays with two pointers up to the middle, `O(m + n)`. The logarithmic idea stops thinking about positions in the merged array and thinks about one cut through both arrays. The median splits all values into a left part of `half = ⌊(m + n + 1) / 2⌋` values and a right part, with every left value at most every right value. If the cut takes `i` values from `a`, it must take `j = half - i` from `b`, so the single number `i` describes the whole split. Each array is sorted on its own, so the cut is valid exactly when the two cross pairs agree: `a[i-1] ≤ b[j]` and `b[j-1] ≤ a[i]`, reading a missing neighbor at an edge as `-∞` or `∞`. The same tests say which way to move. When `a[i-1] > b[j]`, `a` gave too many values to the left and `i` must shrink; when `b[j-1] > a[i]`, it gave too few and `i` must grow. That is a binary search over `i` in `[0, m]`.

Search the shorter array: then `j = half - i` stays inside `[0, n]` for every `i`, which a cut through the longer array cannot promise. At the valid cut the median is the largest left value when the total is odd, because the left part holds the extra value, and the average of the largest left value and the smallest right value when the total is even.

```text
m = 5, n = 6, half = ⌊(5 + 6 + 1) / 2⌋ = 6 values in the left part
                   left │ right
step 1   lo = 0, hi = 5, i = 2, j = 4
   a:             1   3 │  8   9  15
   b:     7  11  18  19 │ 21  25
   a_left 3 ≤ b_right 21 ✓    b_left 19 ≤ a_right 8 ✗    → lo ← 3
step 2   lo = 3, hi = 5, i = 4, j = 2
   a:     1   3   8   9 │ 15
   b:             7  11 │ 18  19  21  25
   a_left 9 ≤ b_right 18 ✓    b_left 11 ≤ a_right 15 ✓   → valid cut
   11 values, odd: median = max(a_left, b_left) = max(9, 11) = 11
```

```pseudo
FUNCTION ValueAt(arr, k)                // -∞ before the start, ∞ past the end
    IF k < 0
        RETURN -∞
    IF k ≥ len(arr)
        RETURN ∞
    RETURN arr[k]

FUNCTION FindMedian(a, b)
    IF len(a) > len(b)
        swap(a, b)                      // search the shorter array
    m ← len(a)
    n ← len(b)
    half ← floor((m + n + 1) / 2)       // size of the left part
    lo ← 0
    hi ← m
    WHILE lo ≤ hi
        i ← floor((lo + hi) / 2)        // a[0..i-1] goes to the left part
        j ← half - i                    // b[0..j-1] fills the rest of it
        a_left ← ValueAt(a, i - 1)
        a_right ← ValueAt(a, i)
        b_left ← ValueAt(b, j - 1)
        b_right ← ValueAt(b, j)
        IF a_left ≤ b_right AND b_left ≤ a_right    // every left ≤ right
            IF (m + n) mod 2 = 1
                RETURN max(a_left, b_left)
            RETURN (max(a_left, b_left) + min(a_right, b_right)) / 2
        IF a_left > b_right
            hi ← i - 1                  // too much of a on the left
        ELSE
            lo ← i + 1                  // too little of a on the left
```

The range of `i` halves at every step, so the search costs `O(log min(m, n))` time and `O(1)` space, even better than the `O(log(m + n))` the problem demands. The signal is a median or a k-th smallest value across two sorted arrays under a logarithmic bound; across many sorted arrays, binary search on the value instead (#73). The classic mistakes are searching the longer array, which pushes `j` below `0` or past `n`, and dropping the infinities, which crashes or misjudges every cut at an edge, such as `i = 0` when all of `a` belongs on the right.

*Practice:* LC 4 Median of Two Sorted Arrays · LC 88 Merge Sorted Array · LC 295 Find Median from Data Stream
