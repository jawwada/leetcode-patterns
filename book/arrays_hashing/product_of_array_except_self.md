# Product of Array Except Self

*LeetCode 238 · Medium · Pattern: Prefix and suffix accumulation · Reading time ~6 min*

## What the problem is really asking

For each position `i`, output the product of every element except `nums[i]`. You may not use division, and you must run
in O(n). The follow-up asks for O(1) extra space, not counting the output array.

The answer is an array the same length as the input. Without the division ban this would be a one-liner: multiply
everything, then divide by each element. The ban is there to make you find the structure underneath, and it also saves
you from zeros, which division cannot handle.

```text
index:    0   1   2   3
nums:   [ 2,  3,  4,  5 ]
answer: [60, 40, 30, 24]

answer[1] = 2 * . * 4 * 5 = 40     (the 3 is left out)
```

## Do it by hand first

Compute `answer[2]` by hand. You cover the 4 with your thumb and multiply what is left: `2 * 3` on the left, `5` on the
right, `6 * 5 = 30`. Now `answer[3]`: cover the 5, multiply `2 * 3 * 4 = 24`, nothing on the right.

```text
             left of i   right of i
answer[2]:   [2  3] (4) [5]         6 * 5  = 30
answer[3]:   [2  3  4] (5) []      24 * 1  = 24
```

Notice that your thumb splits the array into a left block and a right block, and the left block for `i = 3` is the left
block for `i = 2` with one more element. Your hand kept a running product as it moved right. That is the seed: running
products from each end.

## The first honest attempt

For each `i`, loop over all `j != i` and multiply. Time O(n^2), space O(1) extra.

The waste: `answer[i]` and `answer[i + 1]` share `n - 2` of their factors. The brute force recomputes that shared product
from scratch every time.

```text
answer[1] = 2 * . * 4 * 5
answer[2] = 2 * 3 * . * 5
            ^       ^   both multiply 2 and 5 again
answer[3] = 2 * 3 * 4 * .
            ^^^^^ 2*3 computed for the third time
```

## The turning point

Claim: the product of everything except `i` equals (product of everything left of `i`) times (product of everything
right of `i`).

That sounds obvious, but it converts an exclusion problem into two inclusion problems, and inclusion over a prefix is
cheap. Define:

- `L[i]` = product of `nums[0..i-1]` (empty product = 1 for `i = 0`)
- `R[i]` = product of `nums[i+1..n-1]` (empty product = 1 for `i = n-1`)

Each one extends the previous: `L[i] = L[i-1] * nums[i-1]` and `R[i] = R[i+1] * nums[i+1]`. That is the background's
prefix-sum idea with multiplication instead of addition. Then `answer[i] = L[i] * R[i]`.

```text
index:   0    1    2    3
nums:  [ 2,   3,   4,   5 ]
L:     [ 1,   2,   6,  24 ]   build left -> right
R:     [60,  20,   5,   1 ]   build right -> left
L*R:   [60,  40,  30,  24 ]
```

Two O(n) passes and two extra arrays: O(n) time, O(n) space. To reach O(1) extra space, notice that we never need `L` and
`R` side by side as arrays. Write `L` straight into the output array. Then walk right to left with a single variable
`suffix` holding the current `R[i]`, multiply it into `answer[i]`, and only then fold `nums[i]` into `suffix`.

The order of those last two actions is the whole invariant, and it is clearest as code:

```python
for i in range(n - 1, -1, -1):
    answer[i] *= suffix   # suffix = product of nums[i+1:]
    suffix *= nums[i]     # now it covers nums[i:]
```

Swap the two lines and `answer[i]` includes `nums[i]`, which is exactly what the problem forbids. The same discipline
holds in the left pass: stamp `prefix` into `answer[i]` before multiplying `nums[i]` into it. This is check-then-insert
from two sum, in a different costume.

Zeros need no special handling. With one zero at index `z`, every `answer[i]` for `i != z` has the zero in its left or
right block and becomes 0, while `answer[z]` multiplies only the non-zeros. With two zeros everything is 0. The two-pass
method produces all of this automatically because nothing is ever divided out.

## Watch it work

`nums = [2, 3, 4, 5]`.

Frame 1

```text
index:   0   1   2   3
nums:  [ 2,  3,  4,  5 ]
answer [ 1,  2,  6, 24 ]    after the left pass
prefix ends at 120 (unused)
```

The left pass stamped `prefix` before multiplying, so `answer[i]` is the product strictly left of `i`.

Frame 2

```text
index:   0   1   2   3
answer [ 1,  2,  6, 24 ]
                     ^ i = 3   answer[3] *= 1 -> 24
suffix: 1 -> 5
```

Nothing is right of index 3, so it is multiplied by the empty product 1. Then 5 joins the suffix.

Frame 3

```text
index:   0   1   2   3
answer [ 1,  2, 30, 24 ]
                 ^ i = 2   answer[2] = 6 * 5 = 30
suffix: 5 -> 20
```

`answer[2]` gets the product right of it, 5. Then 4 joins: suffix is `4 * 5 = 20`.

Frame 4

```text
index:   0   1   2   3
answer [ 1, 40, 30, 24 ]
             ^ i = 1   answer[1] = 2 * 20 = 40
suffix: 20 -> 60
```

Left part 2, right part `4 * 5`. Then 3 joins the suffix.

Frame 5

```text
index:   0   1   2   3
answer [60, 40, 30, 24 ]
         ^ i = 0   answer[0] = 1 * 60 = 60
suffix: 60 -> 120 (unused)
return [60, 40, 30, 24]
```

Index 0 has nothing on its left, so it takes the full suffix.

Invariant across the right pass: just before index `i` is processed, `suffix` equals the product of `nums[i+1..n-1]` and
`answer[i]` equals the product of `nums[0..i-1]`.

## Why it is correct

After the left pass, `answer[i]` = product of `nums[0..i-1]` for every `i`, because `prefix` held exactly that when
it was stamped, and only then absorbed `nums[i]`.

In the right pass, `suffix` starts at 1 (the empty product right of `n - 1`). At step `i`, it equals the product of
`nums[i+1..n-1]`; multiplying it into `answer[i]` gives left times right, which is the product of every element except
`nums[i]`. Then multiplying `nums[i]` into `suffix` makes it the product of `nums[i..n-1]`, which is exactly what step
`i - 1` needs. By induction every entry ends correct.

## Cost

- Two arrays `L` and `R`: O(n) time, O(n) extra space.
- In-place in the output: O(n) time (two passes), O(1) extra space; the output array is not counted.

## Variations you will meet

- **Range sum query (immutable).** Precompute prefix sums once; any `sum(i..j)` is `P[j+1] - P[i]`. Subtraction works for
  sums; for products it would need division, which is why this problem uses the left-right split instead.
- **Trapping rain water.** Water above `i` depends on the max to its left and the max to its right: prefix max and suffix
  max arrays, the same two-sided accumulation with `max` in place of `*`.
- **Maximum product subarray.** Products again, but now contiguous and maximised; carry both the max and min product
  ending at `i` because a negative flips them.
- **Allowed division, with zeros.** Count zeros: two or more means all zeros; exactly one means only the zero's slot is
  nonzero; none means total divided by each element.

## What to carry forward

"Everything except `i`" is "everything left of `i`" combined with "everything right of `i`", and both are running
accumulations you stamp before you absorb. The next problem keeps the theme of not repeating work, but now the repeated
work is re-walking the same run from each of its members, and a set plus a start-of-run test removes it.
