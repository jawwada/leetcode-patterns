---
rank: 108
slug: counting_sort
---

Sort an array of integers whose values lie in a small range `[low, high]`, negatives included. `[2, -1, 3, 2, 0, -1]` becomes `[-1, -1, 0, 2, 2, 3]`.

Any sort that only compares pairs of values needs on the order of `n log n` comparisons in the worst case. Counting sort never compares: it uses each value as an array index. Count how often each value occurs in an array of `high - low + 1` slots, shifting by `low` so that the smallest value lands in slot 0 and negatives work. Then turn the counts into running totals: after the prefix sum, the slot of value v holds how many values are `≤ v`, which is exactly one past the last position v occupies in the sorted output. Finally walk the input from right to left; for each value, decrement its slot and write the value at that position.

Picture the output as a row of reserved seats. The prefix sums mark where each value's block of seats ends, and the copies of a value fill their block from the back. Because the input is read from the right, the last copy takes the last seat, so equal values keep their input order. That stability does not matter for bare integers, but it matters as soon as the integers are keys of larger records, and it is the whole reason radix sort works.

```text
nums = [2, -1, 3, 2, 0, -1]; low = -1, high = 3, so slot = value + 1
  value          -1    0    1    2    3
  count           2    1    0    2    1
  prefix sums     2    3    3    5    6      how many values are ≤ value
place from the right: decrement the slot, then write at it
  i = 5   -1    2 → 1   result[1] = -1      · -1  ·  ·  ·  ·
  i = 4    0    3 → 2   result[2] =  0      · -1  0  ·  ·  ·
  i = 3    2    5 → 4   result[4] =  2      · -1  0  ·  2  ·
  i = 2    3    6 → 5   result[5] =  3      · -1  0  ·  2  3
  i = 1   -1    1 → 0   result[0] = -1     -1 -1  0  ·  2  3
  i = 0    2    4 → 3   result[3] =  2     -1 -1  0  2  2  3
the 2 from index 0 sits before the 2 from index 3: input order kept
```

```pseudo
FUNCTION CountingSort(nums)
    IF len(nums) = 0
        RETURN empty list
    low ← min(nums)
    high ← max(nums)
    count ← array of high - low + 1 zeros  // count[v - low] is for value v
    FOR EACH value IN nums
        count[value - low] ← count[value - low] + 1
    FOR slot FROM 1 TO len(count) - 1      // now: how many values are ≤ it
        count[slot] ← count[slot] + count[slot - 1]
    result ← array of len(nums) zeros
    FOR i FROM len(nums) - 1 DOWNTO 0      // right to left keeps it stable
        value ← nums[i]
        count[value - low] ← count[value - low] - 1   // the last free seat
        result[count[value - low]] ← value
    RETURN result
```

A few passes over the n values and one over the `k = high - low + 1` slots give `O(n + k)` time and `O(n + k)` space. That beats `O(n log n)` only when k is not much larger than n; values spread over a range of a billion make the count array the bottleneck. Signals: small integer keys such as ages, grades or heights, or a tightly bounded value range in the constraints. Radix sort extends the idea to large keys: run a stable counting sort on the last digit, then on the next digit, up to the first. After the pass on digit d the numbers are sorted by their last d digits, because stability keeps the earlier order among numbers that tie on the new digit; with d digits in base b it costs `O(d(n + b))`, and it is the linear-time answer to Maximum Gap (LC 164). The classic mistake is forgetting the offset, sizing the count array `high + 1` and indexing it by the value itself: in Python a negative index does not fail, `count[-1]` silently counts into the last slot, and `[2, -1, 3, 2, 0, -1]` comes back as `[0, 2, 2, -1, 3, -1]`.

*Practice:* LC 912 Sort an Array · LC 1051 Height Checker · LC 274 H-Index · LC 164 Maximum Gap
