# Minimum Size Subarray Sum
*LeetCode 209 · Medium · Pattern: Variable-size sliding window · Reading time ~7 min*

## What the problem is really asking

You get an array of **positive** integers and a target. Find the shortest contiguous stretch whose sum is at least the target, and return its length. If even the whole array falls short, return 0.

The answer is a length, a single integer. Two things make it more than a one-liner. First, "contiguous" rules out picking the largest numbers freely. Second, we want the *shortest* stretch, which means we must somehow consider every stretch that qualifies without enumerating them all.

```text
target = 7
index:   0   1   2   3   4   5
nums:    2   3   1   2   4   3
                         [4   3]   sum 7, length 2  <- answer
             [3   1   2   4]       sum 10, length 4 (qualifies,
                                    but longer)
```

## Do it by hand first

Most people do this: start at the left, add numbers until the total reaches 7, note the length, then throw away the first number and see whether it still reaches 7.

```text
2            = 2
2 3          = 5
2 3 1        = 6
2 3 1 2      = 8   >= 7, length 4
  3 1 2      = 6   dropped the 2: too light, keep adding
  3 1 2 4    = 10  length 4
    1 2 4    = 7   length 3
      2 4    = 6   too light
      2 4 3  = 9   length 3
        4 3  = 7   length 2
          3  = 3   too light, array ends
```

What did your hand keep track of? A running total, and where the stretch starts. You never re-added numbers: you subtracted from the left and added on the right. That running sum with two ends is the window.

## The first honest attempt

For every start `i`, add `nums[i], nums[i+1], ...` until the sum reaches the target, record `j - i + 1`, and stop (going further only makes the stretch longer). That is O(n^2) time in the worst case and O(1) space.

The repeated work shows up when you line up consecutive starts:

```text
start 0:  2 + 3 + 1 + 2                -> 8
start 1:      3 + 1 + 2 + 4            -> 10
start 2:          1 + 2 + 4            -> 7
                  ^^^^^
     "3 + 1 + 2" and "1 + 2" were already added above
```

The sum for start `i+1` over the same range is just the old sum minus `nums[i]`. The brute force throws that away and starts at zero.

## The turning point

**Claim: because every number is positive, the window sum goes up when the right edge advances and goes down when the left edge advances, so neither edge ever needs to move backwards.**

Justify the two halves separately.

*The right edge never needs to retreat.* Suppose for the current `L` we found the first `R` where the sum reaches the target. Any shorter window starting at `L` ends before `R` and was already too light. So for this `L`, `R` is the best end.

*The left edge never needs to retreat.* Suppose `[L, R]` qualifies and we advance `L`. Could a later right edge `R' > R` ever want the old `L` back? A window `[L, R']` contains `[L+1, R']` plus one more element, so it is strictly longer, and if `[L+1, R']` qualifies we prefer it. If `[L+1, R']` does not qualify, then `[L, R']` might, but `[L, R]` is shorter still and we already recorded it. Either way the old `L` cannot produce a better answer.

That gives the "caterpillar" rule:

- Advance `R` one step and add `nums[R]` to `total`.
- While `total >= target`: record `R - L + 1`, subtract `nums[L]`, advance `L`.

The inner step is a `while`, not an `if`. One large number entering on the right can make several left elements removable at once, as frame 3 below shows.

The structure is just three integers: `L`, `total`, and `best`. No prefix array, no map. Positivity is doing all the work. (Zeros would be harmless; the sum would merely stop being strictly monotone.) If negatives were allowed, removing `nums[L]` could raise the sum, so stopping the shrink at the first too-light window would no longer be safe, and the method collapses. That case is problem 12 in this chapter.

## Watch it work

`target = 7`, `nums = [2, 3, 1, 2, 4, 3]`.

Frame 1

```text
 i:   0  1  2  3  4  5
     [2  3  1] 2  4  3
      L     R            total=6  best=inf
```

`R` walks from 0 to 2; the total never reaches 7, so `L` stays at 0.

Frame 2

```text
 i:   0  1  2  3  4  5
     [2  3  1  2] 4  3   total=8 >= 7: best=4
      L        R
      2 [3  1  2] 4  3   drop 2: total=6 < 7, stop
         L     R
```

`R = 3` makes the window qualify; we record length 4, drop the 2, and the window becomes too light.

Frame 3

```text
 i:   0  1  2  3  4  5
      2 [3  1  2  4] 3   total=10: record 4
         L        R
      2  3 [1  2  4] 3   total=7:  best=3
            L     R
      2  3  1 [2  4] 3   total=6 < 7, stop
               L  R
```

`R = 4` adds a 4; the `while` removes two elements, recording length 3 on the way.

Frame 4

```text
 i:   0  1  2  3  4  5
      2  3  1 [2  4  3]  total=9: record 3
               L     R
      2  3  1  2 [4  3]  total=7: best=2
                  L  R
      2  3  1  2  4 [3]  total=3 < 7, stop
                     L=R
```

`R = 5` adds a 3; shrinking finds `[4, 3]` of length 2. The array ends and the answer is 2.

Across every frame, at the moment the `while` stopped, the window `[L, R]` was too light but `[L-1, R]` was heavy enough. In other words, `L - 1` was the latest start that still worked for this `R`, and that start was recorded.

## Why it is correct

Fix any right edge `R`. Define `s(R)` as the largest `L` such that `sum(nums[L..R]) >= target`, if one exists. The shortest qualifying window ending at `R` is `[s(R), R]`.

Invariant: when iteration `R` begins, `L <= s(R)` (if `s(R)` exists). This holds because `L` moves past an index `i` only while `sum(nums[i..R_old]) >= target`, and since `R_old <= R`, positivity gives `sum(nums[i..R]) >= target` too, so `i <= s(R)`. Inside iteration `R`, the `while` advances `L` and records each qualifying window until the sum drops below target. The last recorded window is `[s(R), R]`, because that is exactly the last `L` for which the sum still reaches target.

So for every `R`, the shortest window ending at `R` was recorded. The overall shortest window ends somewhere, hence `best` is the true minimum. If nothing ever qualified, `best` stays infinite and we return 0.

## Cost

- Time O(n): `R` moves n times, `L` moves at most n times in total across all iterations, and each move is one addition or subtraction.
- Space O(1): `L`, `total`, `best`.

A second optimisation level is not needed for the positive case. The follow-up asks for an O(n log n) method: build prefix sums (which are strictly increasing because the numbers are positive) and, for each start, binary-search the first prefix that is at least `prefix[i] + target`. It is slower than the window but generalises the "monotone" idea to a lookup.

## Variations you will meet

- **O(n log n) follow-up.** Prefix sums plus `bisect_left`. The thinking shifts from "move two pointers" to "for each start, search for the earliest end in a sorted array".
- **Negative numbers allowed (LeetCode 862).** The window rule breaks. Keep prefix sums in a monotonic deque so you can still discard starts that can never be optimal. That is problem 12.
- **Exactly equal to target, any signs (LeetCode 560, count subarrays).** Not a window problem: prefix sums plus a hash map of seen prefixes.
- **Maximum sum of a window of fixed size k.** The degenerate case: both edges move together, add one and drop one per step.

## What to carry forward

Memory hook: positive numbers make the sum monotone in both edges, so grow until good enough and then shrink while still good enough, recording inside the shrink loop.

The next problem keeps the same two-pointer caterpillar but flips the goal: Longest Substring Without Repeating Characters wants the *longest* window that stays legal, so we record after shrinking instead of during it, and the left edge learns to jump.
