# Squares of a Sorted Array
*LeetCode 977 · Easy · Pattern: Two pointers merging from both ends · Reading time ~5 min*

## What the problem is really asking

You get an array already sorted in non-decreasing order, possibly with negatives. Square every element and return the squares, also sorted. The answer is a new array of length n, and the follow-up asks for O(n) time.

The catch: squaring does not preserve order when negatives are present.

```text
nums:     -4   -1    0    3   10
squares:  16    1    0    9  100
          \______/  ^  \______/
          falling  min   rising
answer:    0    1    9   16  100
```

## Do it by hand first

Look at the squares row above. It is a valley: it falls from the left, bottoms out near zero, and rises to the right. If someone asked for the biggest square, you would not scan; you would glance at the two ends, `16` and `100`, and pick the bigger. Cross it off, and the remaining squares are still a valley, so the next biggest is again at one of the two ends.

```text
valley of squares (height = x*x)

 100 |                      *
     |
  16 |  *
   9 |                 *
   1 |       *
   0 |            *
     +--------------------------
       -4   -1    0    3   10
```

Your eyes tracked two things: the left end and the right end of what is not yet crossed off. That is two pointers, and the output fills from the largest down.

## The first honest attempt

Square everything and sort: `sorted(x * x for x in nums)`. O(n log n) time, and correct.

The waste is that sort throws away information it was handed for free. The input was sorted, so the squares are already two sorted runs: the negatives' squares in decreasing order and the non-negatives' squares in increasing order. Sorting rediscovers an order that was already there.

```text
squares:  [ 16   1 | 0   9  100 ]
            <------  ------->
            sorted   sorted
sort() compares across the whole array
as if it knew nothing.
```

## The turning point

**Claim: among the elements not yet placed, the largest square is always at one of the two ends.**

Why: the remaining elements form a contiguous sorted range `nums[L..R]`. The square is largest where the absolute value is largest. In a sorted range the most negative value is at `L` and the most positive is at `R`, and every element between them is closer to zero than one of those two. So the largest |x| is at `L` or `R`.

That gives the algorithm. Compare `|nums[L]|` with `|nums[R]|`. Write the bigger square into the last unfilled slot of the output, and move that pointer inward. Repeat until every slot is filled.

This is a merge of the two sorted runs from their large ends, and it never needs to find where the negatives stop.

Why not fill from the front? The smallest square sits at an unknown position in the middle; the ends only tell you about the maximum.

## Watch it work

`nums = [-4, -1, 0, 3, 10]`, output `res` of length 5, writer `wr` from 4 down to 0.

Frame 1. `|-4| = 4` vs `|10| = 10`: right wins. `res[4] = 100`, `R` moves to 3.

```text
nums: [ -4 | -1 |  0 |  3 | 10 ]
         L                  R
res:  [  . |  . |  . |  . | 100 ]
                             wr=4
```

Frame 2. `|-4| = 4` vs `|3| = 3`: left wins. `res[3] = 16`, `L` moves to 1.

```text
nums: [ -4 | -1 |  0 |  3 | 10 ]
         L             R
res:  [  . |  . |  . | 16 | 100 ]
                       wr=3
```

Frame 3. `|-1| = 1` vs `|3| = 3`: right wins. `res[2] = 9`, `R` moves to 2.

```text
nums: [ -4 | -1 |  0 |  3 | 10 ]
              L        R
res:  [  . |  . |  9 | 16 | 100 ]
                  wr=2
```

Frame 4. `|-1| = 1` vs `|0| = 0`: left wins. `res[1] = 1`, `L` moves to 2.

```text
nums: [ -4 | -1 |  0 |  3 | 10 ]
              L    R
res:  [  . |  1 |  9 | 16 | 100 ]
             wr=1
```

Frame 5. `L = R = 2`. `|0|` vs `|0|`: not strictly greater, so the right branch takes it. `res[0] = 0`, `R` moves to 1. Every slot is filled.

```text
nums: [ -4 | -1 |  0 |  3 | 10 ]
                   LR
res:  [  0 |  1 |  9 | 16 | 100 ]
        wr=0
```

Throughout, the slots right of `wr` held the largest squares in sorted order, and the unplaced inputs were exactly the contiguous range `nums[L..R]`.

## Why it is correct

Invariant before each step: `res[wr+1..n-1]` holds the squares of all elements outside `nums[L..R]`, in sorted order, and each of them is at least as large as every square inside `nums[L..R]`.

Initially nothing is placed. Each step takes the largest square inside the range (it is at an end, by the claim), writes it into `res[wr]`, which is just left of everything already placed and no larger than any of it, and shrinks the range by one. After n steps the range is empty and `res` is fully sorted.

The loop runs exactly n times because the writer counts down over every slot, so the "should it be `<` or `<=`" question that bites the while-loop version never arises.

## Cost

- Time: O(n). One comparison and one write per output slot.
- Space: O(n) for the output, which the problem requires; O(1) besides it.

## Variations you will meet

- **Sort Transformed Array (LeetCode 360)**: apply `a*x^2 + b*x + c` instead of `x^2`. If `a > 0` the curve is a valley and you fill from the back with the larger end; if `a < 0` it is a hill and you fill from the front with the smaller end. Same pointers, direction decided by the sign.
- **Merge Sorted Array (LeetCode 88)**: two sorted arrays, merge into the first one in place. Fill from the back so you never overwrite unread values; the same "largest first, from the end" trick.
- **Merge outward from the split point**: start both pointers at the boundary between negatives and non-negatives and fill from the front. Valid, but you must find the split first.

## What to carry forward

Sorted input plus a V-shaped transform means the extreme is always at an end, so peel it off and fill the output from the back. The next problem returns to a single array edited in place, with a writer that looks back into its own output to decide what to keep.
