# Maximum Product Subarray

*LeetCode 152 · Medium · Pattern: Running max & min carry (Kadane variant) · Reading time ~7 min*

## What the problem is really asking

Same shape as Maximum Subarray, with multiplication instead of addition: choose one unbroken, non-empty stretch of the
array so that the product of its elements is as large as possible, and return that product.

The answer is again one number standing for a pair of endpoints. What makes it hard is sign. With sums, a negative
running total was always bad news. With products, a very negative running product is a hidden treasure: one more negative
number turns it into a very large positive one. Zeros add a second twist, since anything times zero is zero, so a zero
walls the array into independent pieces.

```text
index:   0   1   2   3   4
nums:  [ 2, -5, -2, -4,  3 ]
                 [---------]
               -2 * -4 * 3 = 24     <- answer 24
```

## Do it by hand first

Multiply left to right and watch what each new number does.

Start at 2. Times -5 gives -10, the worst product around. A sum-minded person would throw -10 away. But then -2 arrives,
and -10 times -2 is 20. The "worst" product was the one worth keeping. Next comes -4: 20 times -4 is -80, terrible, but
the stretch `[-2]` that ended one step earlier, times -4, is 8. And at the end, 8 times 3 is 24.

```text
nums:          2    -5    -2    -4     3
biggest end:   2    -5    20     8    24
smallest end:  2   -10    -2   -80  -240
                      \   /  \   /
                       swap   swap      a negative x
                                        trades the roles
```

Your hand had to keep track of two things at every position: the biggest product of a stretch ending here AND the
smallest one. Whenever a negative number arrived, the smallest became the candidate for biggest, and vice versa.

## The first honest attempt

Fix every start `i`, extend the end `j` to the right multiplying into a running product, and keep the maximum. That is
O(n^2) time and O(1) space.

The repeated work is the same as in Maximum Subarray. The products ending at `j` are all "some product ending at `j - 1`,
times `nums[j]`", but the brute force rebuilds each one from its own start:

```text
products ending at j = 3 (x = -4):
  start 0:  2 -5 -2 -4   = -80
  start 1:    -5 -2 -4   = -40
  start 2:       -2 -4   =   8   <- biggest ending at 3
  start 3:          -4   =  -4
            each row re-multiplies the shared tail
```

The natural fix is to copy Kadane: carry only "the biggest product ending here". It fails immediately. At `j = 2` the
biggest product ending at index 1 is -5 (the stretch `[-5]`), and -5 times -2 is 10; but the true best ending at 2 is 20,
built from the stretch `[2, -5]` whose product, -10, was the SMALLEST, not the biggest. Carrying only the max discarded the
one value that mattered.

## The turning point

Claim: the largest and smallest products of a stretch ending at `j` are each one of only three numbers: `x` alone,
`x * hi`, or `x * lo`, where `hi` and `lo` are the largest and smallest products ending at `j - 1`.

Justify it. Any stretch ending at `j` is either `[x]` or (a stretch ending at `j - 1`) times `x`. Multiplying by a fixed
`x` is monotone: if `x > 0` it preserves order, so the biggest product times `x` stays biggest and the smallest stays
smallest; if `x < 0` it reverses order, so the smallest times `x` becomes the biggest and the biggest times `x` becomes the
smallest; if `x = 0` everything becomes 0. In every case, the extremes of the new set come from the extremes of the old
set. The middle values can never become extremes. So two numbers summarise everything that ever needs to be known.

The update is a three-way comparison, and both new values must come from the OLD pair:

```python
cands = (x, hi * x, lo * x)
hi, lo = max(cands), min(cands)
best = max(best, hi)
```

The candidate `x` alone does the job that "restart" did in Kadane. After a zero, `hi = lo = 0`, and the next element `x`
beats `0 * x`, so the run restarts on the other side of the wall automatically.

Picture two lines riding over the array, `hi` on top and `lo` on the bottom. A positive number stretches them apart; a
negative number mirrors them across zero (top becomes bottom) and then stretches; a zero collapses both onto zero. The
answer is the highest point the top line ever touches.

## Watch it work

`nums = [2, -5, -2, -4, 3]`. Start with `hi = lo = best = 2`.

Frame 1

```text
nums:  [ 2, -5, -2, -4,  3 ]
             ^ x = -5
cands: x=-5  hi*x=-10  lo*x=-10
hi = -5   lo = -10   best = 2
```

A negative arrives; the smallest product ending here is the whole stretch `[2, -5]`.

Frame 2

```text
nums:  [ 2, -5, -2, -4,  3 ]
                 ^ x = -2
cands: x=-2  hi*x=10  lo*x=20
hi = 20   lo = -2   best = 20
```

The old `lo` (-10) times a negative becomes the new `hi`: the swap that plain Kadane misses.

Frame 3

```text
nums:  [ 2, -5, -2, -4,  3 ]
                     ^ x = -4
cands: x=-4  hi*x=-80  lo*x=8
hi = 8    lo = -80   best = 20
```

Another swap: the old `lo` (-2, the stretch `[-2]`) produces the new `hi` of 8.

Frame 4

```text
nums:  [ 2, -5, -2, -4,  3 ]
                         ^ x = 3
cands: x=3   hi*x=24   lo*x=-240
hi = 24   lo = -240  best = 24  -> return 24
```

A positive keeps the order; `hi` grows to 24 from the stretch `[-2, -4, 3]`.

At every frame, `hi` and `lo` were the largest and smallest products over all stretches ending exactly at the pointer,
and `best` was the largest product of any stretch seen so far. Each negative `x` swapped which carried value fed the top.

## Why it is correct

The invariant: after index `j`, `hi` is the maximum and `lo` the minimum product over all stretches ending at `j`, and
`best` is the maximum product over all stretches ending anywhere in `[0, j]`.

Base case `j = 0`: the only stretch is `[nums[0]]`, and all three variables equal it.

Step: assume the invariant at `j - 1`. The set of products ending at `j` is `{x} ∪ {p * x : p ending at j - 1}`. The
function `p -> p * x` is monotone (increasing for `x > 0`, decreasing for `x < 0`, constant for `x = 0`), so its maximum
and minimum over a set of `p` values are attained at that set's maximum or minimum, which are `hi` and `lo`. Adding `x`
itself as a third candidate covers the one-element stretch. So `max(cands)` and `min(cands)` are exactly the new extremes,
and `best` absorbs the new `hi`. At the last index, `best` is the answer.

This is the same "carry the summary of everything ending here" invariant as Kadane. What changed is the size of the
summary needed to stay correct under the operation: addition is order-preserving for every `x`, so one number suffices;
multiplication can reverse order, so you need both ends.

## Cost

- **Time O(n):** one pass, a constant number of multiplications and comparisons per element.
- **Space O(1):** three integers, `hi`, `lo` and `best`.

An alternative O(n), O(1) solution scans prefix products from the left and from the right, resetting at zeros. It works
because inside a zero-free block, the best product is always a prefix or a suffix of that block (with an even number of
negatives take the whole block; with an odd number, drop everything up to the first or after the last negative).

## Variations you will meet

- **Return the stretch itself.** Track the start index alongside each of `hi` and `lo`; when `x` alone wins, the start is
  `j`, otherwise it is inherited from whichever of `hi` and `lo` produced the winner.
- **Subarray product less than k (LeetCode 713).** With all-positive values the product only grows as the stretch
  grows, so the problem becomes a sliding window rather than a carry.
- **Maximum absolute sum of any subarray (LeetCode 1749).** Run Kadane for the largest sum and for the smallest sum at the
  same time; the answer is the larger magnitude. Whenever the answer can come from either extreme, carry both.
- **Overflow in other languages.** Python integers never overflow; in Java or C++ the intermediate `lo * x` can exceed 64
  bits on adversarial inputs, so interviewers sometimes ask how you would guard it.

## What to carry forward

When a step can flip the order of your candidates, carry both the best and the worst, because the worst is one sign
change away from being the best. The next problem leaves sums and products behind but keeps the one-pass carry: the state
becomes the furthest index you can reach.
