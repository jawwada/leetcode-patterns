# Two Sum II - Input Array Is Sorted
*LeetCode 167 · Medium · Pattern: Converging two pointers on sorted input · Reading time ~7 min*

## The problem

Given a 1-indexed array sorted in non-decreasing order and a target, return the 1-based indices [i, j] with i < j of
the two numbers that sum to target. Exactly one solution exists and you must use O(1) extra space.

```text
Example: numbers = [2, 7, 11, 15], target = 9 -> [1, 2].
```

## What the problem is really asking

You get an array sorted in non-decreasing order and a target. Exactly one pair of positions `i < j` has `numbers[i] + numbers[j] == target`. Return those positions, **1-indexed**, using only O(1) extra space.

The answer is a pair of indices. The O(1) space rule is what makes it a real question: without it, the hash-map Two Sum from LeetCode 1 solves it in O(n). With it, the only thing you are allowed to lean on is that the array is sorted.

```text
index (1-based):  1    2    3    4    5    6
numbers:        [ 1 |  3 |  4 |  6 |  8 | 11 ]
target = 10                 \____/
                         4 + 6 = 10  -> [3, 4]
```

## Do it by hand first

Put a finger on the smallest number and one on the largest. `1 + 11 = 12`, too big. You would not try `3 + 11` next; that is even bigger. The only way to make the sum smaller is to give up the 11. Move the right finger to 8: `1 + 8 = 9`, too small. Now the only way up is to give up the 1, because pairing 1 with anything left of 8 is smaller still.

```text
 [ 1   3   4   6   8  11 ]
   L                   R    12 > 10, drop 11
   L               R        9 < 10,  drop 1
       L           R        11 > 10, drop 8
       L       R            9 < 10,  drop 3
           L   R            10 = 10  found
```

Each comparison made you give up one number for good. You tracked two positions and one comparison result. That is the whole algorithm.

## The first honest attempt

Check every pair: for each `i`, for each `j > i`, test the sum. O(n^2) time, O(1) space.

The waste is that the brute force ignores sorted order. Once `numbers[i] + numbers[j]` exceeds the target, every `j' > j` gives a larger sum, but the inner loop checks them anyway. And when it moves to `i + 1` it rechecks partners it already knew were hopeless.

```text
i = 0 (value 1):  try 3, 4, 6, 8, 11
i = 1 (value 3):  try 4, 6, 8, 11
                            ^^ ^^
              3 + 8 = 11 > 10 already,
              so 3 + 11 was never possible
```

## The turning point

**Claim: at any step, comparing `numbers[L] + numbers[R]` with the target proves that one of the two endpoints cannot be part of the answer, so that pointer can move inward permanently.**

Justify each case with sorted order:

- **Sum too big.** `numbers[R]` paired with the smallest remaining value is already too big. Every other remaining partner of `numbers[R]` is at least `numbers[L]`, so every pair using `R` is too big. Discard `R`: `R -= 1`.
- **Sum too small.** `numbers[L]` paired with the largest remaining value is still too small. Every other partner is at most `numbers[R]`, so every pair using `L` is too small. Discard `L`: `L += 1`.
- **Equal.** Done.

The monotone property doing the work is "sums grow when either index grows". Picture all pairs as an upper-triangular grid. Each comparison wipes out an entire row or column, not a single cell. The letters below mark which move killed which pair.

```text
 value:          3    4    6    8   11
 j:              1    2    3    4    5
 i=0 (1)         B    B    B    B    A
 i=1 (3)              D    D    C    A
 i=2 (4)                   *    C    A
 i=3 (6)                        C    A
 i=4 (8)                             A

 A: drop col 11   B: drop row 1   C: drop col 8
 D: drop row 3    *: (2,3) 4+6 = 10
```

There are n - 1 rows and n - 1 columns, so at most n - 1 moves happen before the pointers meet. Four moves here eliminated fourteen of fifteen pairs.

Why start at the two ends? Because that corner of the grid is the only place where one comparison is decisive in both directions: `L` is the smallest remaining value and `R` the largest. Starting anywhere else, "too big" would not tell you whether to move left or right.

## Watch it work

`numbers = [1, 3, 4, 6, 8, 11]`, target 10. Indices below are 0-based; the answer is reported +1.

Frame 1. `L = 0`, `R = 5`: `1 + 11 = 12 > 10`. Every pair with 11 is too big; `R = 4`.

```text
  [ 1 | 3 | 4 | 6 | 8 | 11 ]
    L                   R      sum 12 > 10
```

Frame 2. `1 + 8 = 9 < 10`. Every pair with 1 is too small; `L = 1`.

```text
  [ 1 | 3 | 4 | 6 | 8 | 11 ]
    L               R   x      sum 9 < 10
```

Frame 3. `3 + 8 = 11 > 10`. Drop 8; `R = 3`.

```text
  [ 1 | 3 | 4 | 6 | 8 | 11 ]
    x   L           R   x      sum 11 > 10
```

Frame 4. `3 + 6 = 9 < 10`. Drop 3; `L = 2`.

```text
  [ 1 | 3 | 4 | 6 | 8 | 11 ]
    x   L       R   x   x      sum 9 < 10
```

Frame 5. `4 + 6 = 10`. Return `[3, 4]`.

```text
  [ 1 | 3 | 4 | 6 | 8 | 11 ]
    x   x   L   R   x   x      sum 10: found
  answer (1-based): [3, 4]
```

Every `x` marks a value proven useless. In each frame, the answer pair, if it exists, lies inside `[L, R]`.

## Why it is correct

Invariant: if a valid pair exists, both of its indices lie in `[L, R]`.

It holds at the start because `[L, R]` is the whole array. Each move discards one endpoint only after proving, by the cases in the turning point, that every pair involving that endpoint and another index in `[L, R]` has the wrong sum. Pairs involving indices outside `[L, R]` were already excluded earlier. So the valid pair, which exists by the problem statement, stays inside the range.

The range shrinks by one per step, so the loop cannot run forever, and it cannot end with `L >= R` while the pair is still inside. So it ends at the pair.

Duplicates do not break this. With `[1, 2, 3, 4, 4, 9]` and target 8, the argument never needs values to be distinct, only non-decreasing.

## Cost

- Time: O(n). Each iteration moves one pointer inward; at most n - 1 iterations.
- Space: O(1). Two integers.

For comparison: brute force O(n^2) / O(1); hash map O(n) / O(n); binary search for each partner O(n log n) / O(1).

## Variations you will meet

- **Two Sum (LeetCode 1)**, unsorted, return original indices: sorting would lose the indices, so use a hash map of value to index. If you must use pointers, sort `(value, index)` pairs.
- **Count pairs with sum less than target**: when `numbers[L] + numbers[R] < target`, every `R' in (L, R]` also works with `L`, so add `R - L` and move `L`. The pruning now counts a whole row at once instead of discarding it.
- **Closest sum to target (Two Sum Closest)**: never return early; record `|sum - target|` at each step. The same discard argument holds because moving the wrong pointer only moves the sum further away.
- **3Sum and 4Sum**: fix one (or two) values with outer loops and run this walk inside. That is the next problem.

## What to carry forward

On sorted input, one comparison at the two ends deletes an entire row or column of the pair grid; say out loud which one and why before you move a pointer. The next problem fixes one element and runs exactly this walk on the rest, using sorted order a second time to skip duplicate answers.
