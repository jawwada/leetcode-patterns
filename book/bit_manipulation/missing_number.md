# Missing Number

*LeetCode 268 · Easy · Pattern: XOR cancellation · Reading time ~5 min*

## What the problem is really asking

The array holds `n` distinct numbers drawn from the `n + 1` possible values `0, 1, ..., n`. Exactly one value is absent. Return it, in linear time and constant extra space. The answer is a single integer in `[0, n]`, and it may be `n` itself or `0`.

Unlike Single Number, nothing in the array appears twice. The pairs we need for cancellation are not in the input, so we have to supply them ourselves.

```text
nums = [3, 0, 1]   n = 3   range = {0, 1, 2, 3}

range : 0  1  2  3
array : 0  1  .  3
              ^ nobody -> 2
```

## Do it by hand first

On paper you would write the full range 0..n in one row and the array in another, then tick each array value off the range row. The unticked value is the answer.

```text
range row:  0  1  2  3
            x  x     x     ticked by array values 0, 1, 3
                  ^ unticked: 2
```

What you kept track of was "which values of the range have been matched". Each value of the range gets matched by one array element, except one. That is the Single Number picture: put the range row and the array row together, and every value appears twice except the missing one.

## The first honest attempt

For each candidate `v` in `0..n`, scan the array for it; return the first `v` you do not find. O(n²) time. Sorting and walking is O(n log n). A hash set is O(n) time but O(n) space.

```text
v = 0: scan 3 0 1 -> found
v = 1: scan 3 0 1 -> found
v = 2: scan 3 0 1 -> missing  -> answer
each scan re-reads the whole array; the scan
for v = 0 teaches nothing to the scan for v = 1
```

The waste is n + 1 independent membership tests over the same data. We need one pass that can absorb every value and remember, in constant space, the one that was never matched.

## The turning point

**Claim: XOR of all numbers `0..n` together with all array values equals the missing number.**

Put the two rows side by side as one multiset. Every value that is present appears twice, once from the range and once from the array. The missing value appears only once, from the range. XOR erases pairs, so it leaves the missing value. This is exactly Single Number on a list we never build.

To do it in one pass, use the indices as the range row. Indices run from 0 to n - 1, so the only range value without an index is `n` itself. Start the accumulator at `n`, then for each position fold in both the index and the value:

```python
acc = len(nums)            # n has no index slot
for i, v in enumerate(nums):
    acc ^= i ^ v
```

The arithmetic twin is `n(n+1)/2 - sum(nums)`. It is equally valid in Python, but in fixed-width languages the sum can overflow, while XOR never leaves the bit width. XOR is also the version that shows you understand cancellation.

## Watch it work

`nums = [3, 0, 1]`, `n = 3`. Two-bit columns.

```text
Frame 1   seed
  acc = n = 3 = 1 1
  range values folded: {3}   array values folded: {}
```
3 is the one range value with no index, so it is folded in first.

```text
Frame 2   i = 0, v = 3     acc ^= 0 ^ 3
  acc = 1 1 ^ 0 0 ^ 1 1 = 0 0   (0)
  folded: range {3,0}  array {3}
```
The array's 3 cancels the seed 3; index 0 contributes nothing visible yet.

```text
Frame 3   i = 1, v = 0     acc ^= 1 ^ 0
  acc = 0 0 ^ 0 1 ^ 0 0 = 0 1   (1)
  folded: range {3,0,1}  array {3,0}
```
The array's 0 cancels index 0; index 1 is now waiting.

```text
Frame 4   i = 2, v = 1     acc ^= 2 ^ 1
  acc = 0 1 ^ 1 0 ^ 0 1 = 1 0   (2)
  folded: range {3,0,1,2}  array {3,0,1}
```
The array's 1 cancels index 1; index 2 has no partner, so the answer is 2.

At every frame, `acc` equalled the XOR of the range values folded so far that had not yet been matched by an array value, and of array values not yet matched by a range value. At the end only the unmatched range value is left.

## Why it is correct

Let `R = {0, ..., n}` and `A` be the array. The accumulator ends as the XOR over `R` and `A` together, because the seed supplies `n`, the loop supplies indices `0..n-1`, and the loop supplies every array value. Since `A = R \ {m}` for the missing `m`, every element of `A` appears twice in the combined list and `m` appears once. Pairs XOR to 0 regardless of order, so the result is `m`. The cases `m = 0` (all of 1..n present) and `m = n` (all of 0..n-1 present) need no special handling.

## Cost

- Time: O(n). One pass, two XORs per element.
- Space: O(1). One accumulator.

## Variations you will meet

- **Sum formula**: `n*(n+1)//2 - sum(nums)`. Same O(n)/O(1), and safe in Python. Mention the overflow issue for Java/C.
- **First Missing Positive** (LeetCode 41): values are arbitrary and duplicates are allowed, so cancellation fails. Use the array itself as a hash table with cyclic placement.
- **Find the Duplicate Number** (LeetCode 287): one value repeated, possibly many times. XOR fails, because there are more than two copies. Use Floyd's cycle detection or binary search on counts.
- **Two missing numbers**: XOR gives `a ^ b`. Split by any set bit of it, as in Single Number III, and XOR each group with its share of the range.

## What to carry forward

When the pairs are not in the input, build them: XOR indices against values, and seed with the one index that has no slot. The next problem stops cancelling whole numbers and reads just the last two bits to decide a move, letting a carry clear a run of 1s at once.
