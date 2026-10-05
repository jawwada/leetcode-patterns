# 3Sum (LeetCode 15)

**Area:** two pointers · **Difficulty:** Medium-Hard · **Key operations:** sort, fix the anchor i, converge lo/hi on the suffix, skip equal neighbours

## Problem

Given an integer array, return every unique triplet `[a, b, c]` with `a + b + c == 0`. The order of the triplets and of the numbers inside them does not matter, and no triplet may appear twice.

## Example

```
nums   = [-1, 0, 1, 2, -1, -4]
answer = [[-1, -1, 2], [-1, 0, 1]]
```

## Brute force

Three nested loops over `i < j < k`, test the sum, and insert the sorted triplet into a set to kill duplicates.

O(n³) time, O(#answers) space. Two wastes: for a fixed pair the third value is already known, `-(a + b)`, yet a whole loop searches for it; and duplicate triplets are generated many times only to be discarded by the set.

## From brute force to optimal

Fix the first element; the rest is Two Sum with target `-nums[i]`. A hash set makes that O(n) per anchor, but deduplication stays messy. **Sorting first solves both problems at once.** On a sorted suffix the two-sum is a converging two-pointer walk: sum too small, move the left pointer right; too big, move the right pointer left; zero, record it and move both. And sorting makes equal values *adjacent*, so a duplicate triplet can only arise from an anchor equal to the previous anchor, or from a left pointer landing on the same value it just used. Both are skipped with a one-line comparison against the neighbour. Sorting costs O(n log n), dominated by the O(n²) scan.

## Intuition

Reduce the dimension: 3Sum is n copies of 2Sum. Picture the sorted array as a number line with an anchor `i` at the left and two pointers `L` (just right of `i`) and `R` (far right) walking toward each other. The sum tells you which way to go: too negative means you need a bigger number, so `L` steps right; too positive, `R` steps left. When they hit zero you record the triplet and step *both*, because the same `L` with a different `R` cannot sum to zero again. The duplicate skips just step over clones of a value already used, which sorting conveniently placed side by side.

## Walkthrough

```
sorted      -4  -1  -1   0   1   2
index        0   1   2   3   4   5

i=0 (-4)     i   L               R     -4 + -1 + 2 = -3 < 0  -> L right
             i       L           R     -4 + -1 + 2 = -3 < 0  -> L right
             i           L       R     -4 +  0 + 2 = -2 < 0  -> L right
             i               L   R     -4 +  1 + 2 = -1 < 0  -> L right, L meets R, done

i=1 (-1)         i   L           R     -1 + -1 + 2 =  0      -> record [-1, -1, 2], move both
                 i       L   R         -1 +  0 + 1 =  0      -> record [-1, 0, 1], move both
                                       L meets R, done

i=2 (-1)     nums[2] == nums[1] -> same anchor as before, skip

i=3 (0)                  i   L   R      0 +  1 + 2 =  3 > 0  -> R left, L meets R, done

result [[-1, -1, 2], [-1, 0, 1]]
```

Note how the skip at `i=2` compares with the *previous* anchor: `i=1` was allowed to use the second `-1` as its `L`, which is what produced `[-1, -1, 2]`.

## Steps

1. Sort `nums`; `result = []`.
2. For `i` in `0 .. n-3`: if `i > 0` and `nums[i] == nums[i-1]`, skip (same anchor as before).
3. `lo = i + 1`, `hi = n - 1`; while `lo < hi`: `total = nums[i] + nums[lo] + nums[hi]`.
4. `total < 0`: `lo += 1`. `total > 0`: `hi -= 1`.
5. `total == 0`: append the triplet, move both pointers, then step `lo` past values equal to `nums[lo-1]` and `hi` past values equal to `nums[hi+1]`.
6. Return `result`.

## Complexity

O(n²) time: O(n log n) for the sort plus an O(n) two-pointer walk for each of n anchors. O(1) extra space beyond the output (and the sort).

## Pitfalls

- **Skipping the anchor by looking forward.** `nums[i] == nums[i + 1]` skips the *first* copy of a repeated value, so a triplet that needs two copies is lost: the example returns only `[-1, 0, 1]`. Compare with `nums[i - 1]`.
- **Skipping `lo` by looking forward.** `nums[lo] == nums[lo + 1]` does not step past the value just recorded, so the same triplet is recorded again: `[-2, 0, 0, 2, 2]` returns `[-2, 0, 2]` twice. Compare with `nums[lo - 1]`.
- **`lo <= hi`.** The pointers may coincide and one element is used twice: `[-2, 1, 3]` returns `[[-2, 1, 1]]`. Stop when they meet.
- **Moving only one pointer after a hit.** It still works (the next sum is non-zero and the other pointer moves), but it wastes a step and makes the duplicate-skip reasoning harder to defend.
- **Falling back to a set of tuples.** It removes duplicates, but the interviewer wants the adjacency argument, which is what sorting bought you.
