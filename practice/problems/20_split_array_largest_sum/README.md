# Split Array Largest Sum (LeetCode 410)

**Area:** binary search · **Difficulty:** Medium-Hard · **Key operations:** binary search on the answer (a cap), greedy count of pieces under the cap, hi = mid when pieces <= k

## Problem

Given an array `nums` of non-negative integers and an integer `k`, split the array into `k` non-empty contiguous pieces so that the largest piece sum is as small as possible. Return that minimised largest sum.

## Example

```
nums = [7, 2, 5, 10, 8], k = 2   ->   18

[7, 2, 5] | [10, 8]      sums 14 | 18    largest 18   (best)
[7, 2] | [5, 10, 8]      sums  9 | 23    largest 23
[7, 2, 5, 10] | [8]      sums 24 |  8    largest 24
```

`nums = [1, 2, 3, 4, 5], k = 2` gives 9 (`[1, 2, 3] | [4, 5]`).

## Brute force

Choose `k - 1` cut positions among the `n - 1` gaps between elements, sum each piece, record the largest piece, and keep the placement with the smallest largest piece.

C(n-1, k-1) placements of O(n) each: exponential in general. The wasted work: almost every placement is hopeless (one giant piece) and is evaluated anyway, and placements that share a prefix of cuts re-sum the same pieces over and over.

## From brute force to optimal

Flip the question. "Make the largest piece as small as possible" is hard to construct directly. "Can every piece be kept at or under a budget `cap`?" is a yes/no question with a greedy answer: scan left to right, keep adding to the current piece while the sum stays `<= cap`, cut when the next element would overflow, and count the pieces. Greedy packing uses the fewest pieces possible for that cap, so `cap` is feasible exactly when `pieces(cap) <= k` (fewer than `k` pieces is fine: any piece can be split further).

`feasible(cap)` is monotone: raising the cap never needs more pieces. The answer lies in `[max(nums), sum(nums)]`: the largest element must fit in some piece, and the whole array in one piece is always possible. Binary search that range for the first feasible cap, paying one O(n) greedy scan per probe.

## Intuition

Picture the array as bars standing side by side and the cap as a horizontal water line. Pour from the left into a bucket; whenever the next bar would make the bucket spill over the line, start a new bucket. Fewer buckets as the line rises. The binary search raises and lowers the line until exactly `k` buckets (or fewer) suffice and one unit lower does not. That lowest line is the answer, and the buckets it produces are the optimal split.

## Walkthrough

`nums = [7, 2, 5, 10, 8]`, `k = 2`. Range `[max, sum] = [10, 32]`.

```
cap range [10..32]   mid = 21
    7 + 2 + 5 = 14, + 10 = 24 > 21 -> cut;  10 + 8 = 18 <= 21
    [7, 2, 5] | [10, 8]              2 pieces <= 2   feasible    hi = 21

cap range [10..21]   mid = 15
    7 + 2 + 5 = 14, + 10 > 15 -> cut;  10, + 8 = 18 > 15 -> cut;  8
    [7, 2, 5] | [10] | [8]           3 pieces > 2    too small   lo = 16

cap range [16..21]   mid = 18
    7 + 2 + 5 = 14, + 10 = 24 > 18 -> cut;  10 + 8 = 18 <= 18 (exactly at the cap)
    [7, 2, 5] | [10, 8]              2 pieces <= 2   feasible    hi = 18

cap range [16..18]   mid = 17
    7 + 2 + 5 = 14, + 10 > 17 -> cut;  10, + 8 = 18 > 17 -> cut;  8
    [7, 2, 5] | [10] | [8]           3 pieces > 2    too small   lo = 18

lo == hi == 18 -> answer 18
```

Cap 17 needs three pieces and cap 18 needs two, so 18 is the smallest feasible cap; the greedy pieces at cap 18 are the optimal split.

## Steps

1. `lo = max(nums)`, `hi = sum(nums)`.
2. `pieces(cap)`: `count = 1`, `cur = 0`; for each `x`: if `cur + x > cap` then `count += 1`, `cur = 0`; then `cur += x`. Return `count`.
3. While `lo < hi`: `mid = (lo + hi) // 2`; if `pieces(mid) <= k` then `hi = mid` else `lo = mid + 1`.
4. Return `lo`.

## Complexity

O(n log S) time with `S = sum(nums)`: about log S probes, each an O(n) greedy scan. O(1) extra space. No DP table: the monotone predicate plus the greedy check is the whole optimisation.

## Pitfalls

- **`>=` instead of `>` in the greedy cut.** A piece may sum to exactly the cap. Cutting early overcounts pieces, so feasible caps are rejected (`[9, 9, 9]`, `k = 2` gives 19 instead of 18).
- **`== k` instead of `<= k`.** Fewer pieces than `k` is still feasible because any piece can be split further; demanding exactly `k` makes the search drift upward (`[1, 4, 4]`, `k = 3` gives 9 instead of 4).
- **`lo = 0` instead of `max(nums)`.** A cap below the largest element is impossible, but the greedy still places that element and the count can look feasible; the search then returns a cap no split can meet.
- **`count` starting at 0.** The first piece exists before any cut. Starting at 0 undercounts and the answer comes out too small.
- **Returning `hi` with a `lo <= hi` loop.** Stick to one template: `while lo < hi`, `hi = mid` on feasible, `lo = mid + 1` on infeasible, return `lo`.
