---
rank: 5
slug: three_sum
---

Given an array of integers, return every unique triplet of values that sums to zero; the same triplet must not appear twice, whichever positions it comes from. In `[-1, 0, 1, 2, -1, -4]` the answer is `[[-1, -1, 2], [-1, 0, 1]]`.

The brute force tries all `n(n - 1)(n - 2) / 6` triples of positions, `O(n^3)`, and still needs a set to strip repeated triplets. Sorting first changes the shape of the problem. Fix the first value `nums[i]`; what remains is a pair in the sorted suffix that sums to `-nums[i]`, which is Two Sum II, solved by two pointers converging from the ends of the suffix. If the sum is too small, only moving `left` rightward can raise it, because every value to the left of `right` pairs with `nums[left]` for a sum no larger. If it is too big, only moving `right` leftward can lower it. Each comparison retires one value for good, so one sweep is `O(n)` and the whole search is `O(n²)`.

Sorting also tames the duplicates, because equal values now sit side by side. An `i` whose value equals the one before it would rediscover the same triplets, so it is skipped; after a hit, `left` steps past every copy of the value just used. The early exit comes free: once `nums[i] > 0`, all three values are positive and nothing later can reach zero. Picture `i` pinned at the left end while `left` and `right` squeeze the rest of the line from both sides.

```text
index      0    1    2    3    4    5
sorted    -4   -1   -1    0    1    2
 i  nums[i]  left  right   sum   action
 0    -4       1     5     -3    too small: left + 1
 0    -4       2     5     -3    too small: left + 1
 0    -4       3     5     -2    too small: left + 1
 0    -4       4     5     -1    too small: left + 1, pointers meet
 1    -1       2     5      0    record [-1, -1, 2], move both
 1    -1       3     4      0    record [-1, 0, 1], move both, pointers cross
 2    -1                         same value as nums[1]: skip
 3     0       4     5      3    too big: right - 1, pointers meet
```

```pseudo
FUNCTION ThreeSum(nums)
    nums ← sorted(nums)                    // equal values now sit together
    triplets ← empty list
    n ← len(nums)
    FOR i FROM 0 TO n - 3
        IF nums[i] > 0
            BREAK                          // smallest of the three is positive
        IF i > 0 AND nums[i] = nums[i - 1]
            CONTINUE                       // same first value, same triplets
        left ← i + 1
        right ← n - 1
        WHILE left < right                 // Two Sum II on nums[i+1..n-1]
            total ← nums[i] + nums[left] + nums[right]
            IF total < 0
                left ← left + 1            // too small: a bigger second value
            ELSE IF total > 0
                right ← right - 1          // too big: a smaller third value
            ELSE
                triplets.append([nums[i], nums[left], nums[right]])
                left ← left + 1
                right ← right - 1
                WHILE left < right AND nums[left] = nums[left - 1]
                    left ← left + 1        // skip repeats of the second value
    RETURN triplets
```

The sort costs `O(n log n)` and is dominated by the `n` linear sweeps, so the total is `O(n²)` time, and the only extra memory besides the output is the sorted copy. Reach for sort, fix one, converge two whenever a problem asks for pairs, triplets or quadruplets with a target sum and wants values rather than indices: 3Sum Closest keeps the nearest total instead of exact hits, and 4Sum wraps one more fixed loop around the same sweep. The classic mistake is skipping duplicates by looking ahead, `nums[i] = nums[i + 1]`, instead of back. On the example it skips the first `-1` and loses `[-1, -1, 2]`, whose second `-1` was needed at `left`.

*Practice:* LC 15 3Sum · LC 167 Two Sum II - Input Array Is Sorted · LC 16 3Sum Closest · LC 18 4Sum
