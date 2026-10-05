# Product of Array Except Self (LeetCode 238)

**Area:** arrays & hashing · **Difficulty:** Medium · **Key operations:** left sweep stamping prefix products, right sweep multiplying in a running suffix product

## Problem

Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of every element of `nums` except `nums[i]`. Division is not allowed, the solution must run in O(n), and the output array does not count as extra space.

## Example

```
nums   = [ 1,  2,  3,  4]
answer = [24, 12,  8,  6]
```

`answer[1] = 1 * 3 * 4 = 12`.

## Brute force

For each `i`, multiply every element whose index is not `i`.

O(n²) time, O(1) extra space. The wasted work shows up when you compare neighbours: `answer[i]` and `answer[i + 1]` share `n - 2` factors, yet that shared product is rebuilt from scratch for every position.

## From brute force to optimal

"Everything except `i`" is "everything left of `i`" times "everything right of `i`". Both halves are running products: the product of the left part grows by one factor as `i` moves right, the product of the right part grows by one factor as `i` moves left. So two linear sweeps build all the answers.

To get O(1) extra space, write the left products straight into `answer` during the first sweep, then do the second sweep right to left carrying the right product in a single variable and multiplying it into the stamped value. No division means zeros need no special case.

## Intuition

Picture two arrows sweeping over the array from opposite ends. The left arrow drags along a growing product of everything behind it and *stamps* that product into each cell as it passes, before picking up the cell's own value. The right arrow does the same from the other side, but *multiplies* its product into the stamped value instead of overwriting it. Every cell ends up holding (product of its left) times (product of its right), and its own value was never multiplied in by either arrow.

## Walkthrough

```
nums     1   2   3   4

left sweep, prefix = product of nums[0..i-1], stamped into answer[i]
  i=0  answer[0] = 1    prefix *= 1 -> 1     answer [1, 1, 1, 1]
  i=1  answer[1] = 1    prefix *= 2 -> 2     answer [1, 1, 1, 1]
  i=2  answer[2] = 2    prefix *= 3 -> 6     answer [1, 1, 2, 1]
  i=3  answer[3] = 6    prefix *= 4 -> 24    answer [1, 1, 2, 6]

right sweep, suffix = product of nums[i+1..n-1], multiplied into answer[i]
  i=3  answer[3] *= 1  -> 6     suffix *= 4 -> 4      answer [1, 1, 2, 6]
  i=2  answer[2] *= 4  -> 8     suffix *= 3 -> 12     answer [1, 1, 8, 6]
  i=1  answer[1] *= 12 -> 12    suffix *= 2 -> 24     answer [1, 12, 8, 6]
  i=0  answer[0] *= 24 -> 24    suffix *= 1 -> 24     answer [24, 12, 8, 6]
```

After the left sweep `answer = [1, 1, 2, 6]` is the array of left products; the right sweep multiplies in `[24, 12, 4, 1]` element by element.

## Steps

1. `answer = [1] * n`, `prefix = 1`.
2. Left sweep, `i = 0 .. n-1`: `answer[i] = prefix`, then `prefix *= nums[i]`.
3. `suffix = 1`.
4. Right sweep, `i = n-1 .. 0`: `answer[i] *= suffix`, then `suffix *= nums[i]`.
5. Return `answer`.

## Complexity

O(n) time: two passes. O(1) extra space: two scalars; the output array is required anyway.

## Pitfalls

- **Multiplying self in.** `answer[i] = prefix * nums[i]` stamps a product that includes `nums[i]`, giving `[24, 24, 24, 24]`. Stamp first, then update the carry.
- **Right sweep stops early.** `range(n - 1, 0, -1)` never visits index 0, so `answer[0]` stays 1. The stop value of `range` is exclusive: use `-1`.
- **Overwriting instead of multiplying.** `answer[i] = suffix` discards the left half, giving `[24, 12, 4, 1]`. Use `*=`.
- **Reaching for division.** Total product divided by `nums[i]` breaks on zeros and violates the constraint; the two-sweep method handles any number of zeros without special cases.
