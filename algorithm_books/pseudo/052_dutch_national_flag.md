---
rank: 52
slug: dutch_national_flag
---

Given an array that holds only `0`, `1` and `2`, the three colors of the Dutch flag, sort it in place in a single pass with `O(1)` extra space. `[2, 0, 2, 1, 1, 0]` becomes `[0, 0, 1, 1, 2, 2]`.

Counting sort already does it in two passes: count the three values, then overwrite the array. The one-pass idea is to keep the array split into four regions at all times, with three pointers on the borders: `nums[0..low-1]` holds 0s, `nums[low..mid-1]` holds 1s, `nums[mid..high]` is still unseen, and `nums[high+1..n-1]` holds 2s. Each step classifies `nums[mid]`, the first unseen value. A `0` swaps with the first 1 at `low`, which grows the 0s and slides the block of 1s one step right, so `low` and `mid` both advance. A `1` is already in place, so only `mid` advances. A `2` swaps with the last unseen value at `high`, and `high` retreats.

The asymmetry is the whole subtlety. After a `0` swap, the value that comes back from `low` is a 1 that `mid` has already passed, or the 0 itself when there are no 1s yet, so `mid` may move on. After a `2` swap, the value that comes back from `high` has never been looked at, so `mid` must stay and examine it. The unseen middle shrinks by exactly one every step, and when it is empty the flag is sorted.

```text
 0s  │ 1s  │ unseen      │ 2s    low mid high   action
     │     │ 2 0 2 1 1 0 │        0   0    5    2: swap to high, high - 1
     │     │ 0 0 2 1 1   │ 2      0   0    4    0: swap to low, low + 1, mid + 1
 0   │     │ 0 2 1 1     │ 2      1   1    4    0: swap to low, low + 1, mid + 1
 0 0 │     │ 2 1 1       │ 2      2   2    4    2: swap to high, high - 1
 0 0 │     │ 1 1         │ 2 2    2   2    3    1: mid + 1
 0 0 │ 1   │ 1           │ 2 2    2   3    3    1: mid + 1
 0 0 │ 1 1 │             │ 2 2    2   4    3    mid > high: done
```

```pseudo
FUNCTION SortColors(nums)
    low ← 0                                // nums[0..low-1] are 0s
    mid ← 0                                // nums[low..mid-1] are 1s
    high ← len(nums) - 1                   // nums[high+1..n-1] are 2s
    WHILE mid ≤ high                       // nums[mid..high] is still unseen
        IF nums[mid] = 0
            swap(nums[low], nums[mid])
            low ← low + 1
            mid ← mid + 1                  // the block of 1s shifts right
        ELSE IF nums[mid] = 1
            mid ← mid + 1
        ELSE
            swap(nums[mid], nums[high])
            high ← high - 1                // mid stays: this value is unseen
```

The unseen region loses one element per step, so the sort takes exactly `n` steps, `O(n)` time with `O(1)` space and at most one swap per step. This is the three-way partition that rescues quicksort (#18) from repeated pivots: values less than, equal to and greater than the pivot play 0, 1 and 2, and the equal block never needs sorting again. Reach for it whenever an array must be split in place into two or three classes whose inner order does not matter, by parity, by sign or around a pivot; Partition Array According to Given Pivot keeps each class in its original order, which these swaps would scramble, so it fills the regions in separate passes instead. The classic mistake is advancing `mid` after swapping a `2` to the back: on `[1, 2, 0]` the `0` that comes forward is never examined, and the result is `[1, 0, 2]`.

*Practice:* LC 75 Sort Colors · LC 905 Sort Array By Parity · LC 2161 Partition Array According to Given Pivot
