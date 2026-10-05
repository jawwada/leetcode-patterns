# Max Consecutive Ones III
*LeetCode 1004 · Medium · Pattern: Variable-size sliding window · Reading time ~7 min*

## The problem

Given a binary array nums and an integer k, you may flip at most k zeros to ones. Return the length of the longest run
of consecutive ones achievable.

```text
Example: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2 -> 6 (flip the
  zeros at indices 4 and 5).
```

## What the problem is really asking

You have an array of 0s and 1s and a budget `k`. You may turn at most `k` zeros into ones. After doing so, what is the longest run of consecutive ones you can have?

The story talks about flipping, which tempts you to think about *which* zeros to flip. That is the trap: there are too many choices of k zeros. The answer is a length, and the real object is a contiguous stretch of the array. A stretch can be turned into all ones exactly when it contains at most `k` zeros. So the problem is: **find the longest subarray containing at most `k` zeros.**

```text
k = 1
index:  0  1  2  3  4  5  6  7
nums:   1  0  1  1  0  0  1  1
       [1  0  1  1]               one zero: flip it -> 1111
                                   length 4  <- answer
                [1  0  0  1  1]   two zeros: over budget
```

## Do it by hand first

Take `nums = [1,0,1,1,0,0,1,1]`, `k = 1`. Slide your finger right, keeping a stretch that has at most one zero.

```text
1          zeros 0   len 1
1 0        zeros 1   len 2
1 0 1      zeros 1   len 3
1 0 1 1    zeros 1   len 4   <- best
1 0 1 1 0  zeros 2   too many! drop from the left
           until a zero falls out:
    1 1 0  zeros 1   len 3
then next 0 arrives: zeros 2 again, drop 1, 1, 0
          0  zeros 1   len 1
          0 1 1      len 3
```

You tracked one number besides the stretch itself: how many zeros were inside. That counter is the entire summary.

## The first honest attempt

For each start `i`, walk right counting zeros, stop when the count reaches `k + 1`, record the length. O(n^2) time, O(1) space.

```text
start 0:  1 0 1 1 | 0        zeros: 0,1,1,1,2 stop
start 1:    0 1 1 | 0        zeros: 1,1,1,2 stop
start 2:      1 1 0 | 0      zeros: 0,0,1,2 stop
              ^^^
     every start recounts the same middle stretch
```

Start `i+1`'s zero count over any range differs from start `i`'s by exactly one thing: whether `nums[i]` was a zero. Recounting from scratch ignores that.

## The turning point

**Claim: "contains at most `k` zeros" is preserved by shrinking, so the longest legal window ending at `R+1` never starts before the longest legal window ending at `R`.**

Justification: if `[L, R]` has at most `k` zeros, every sub-window does too. Conversely, if `[L, R]` is illegal, so is any window containing it. Now suppose the best window ending at `R` starts at `L`. Then `[L-1, R]` is illegal (or `L = 0`), so `[L-1, R+1]` is illegal too. Hence the best start for `R+1` is at least `L`. The left edge only moves forward.

That turns the problem into the standard expand-right, shrink-left loop:

- Advance `R`; if `nums[R]` is 0, `zeros += 1`.
- While `zeros > k`: if `nums[L]` is 0, `zeros -= 1`; advance `L`.
- Record `R - L + 1`.

The window `[L, R]` and the integer `zeros` are the only state. The counter is updated by +1 when a zero enters on the right and -1 when a zero leaves on the left, so validity is a single comparison.

Notice how little the shape changed from the previous problem. There the rule was "no character appears twice" and the summary was a last-seen map. Here the rule is "at most k bad items" and the summary is one integer. Most "longest legal window" problems are this template with a different summary; the hard part is recognising the window behind the story.

A quieter observation, which pays off two problems from now: the `while` can be replaced by a single `if` that moves `L` exactly once. The window then never shrinks; it either grows or slides at its current width. It may become temporarily illegal, but its width is always a width that was legal at some earlier moment, and it only grows when the new window is legal. The answer is the final width. Longest Repeating Character Replacement relies on precisely this idea.

## Watch it work

`nums = [1, 0, 1, 1, 0, 0, 1, 1]`, `k = 1`.

Frame 1

```text
 i:   0  1  2  3  4  5  6  7
     [1  0  1  1] 0  0  1  1
      L        R              zeros=1  best=4
```

`R` walks 0 to 3; one zero enters at index 1, within budget. Length 4.

Frame 2

```text
 i:   0  1  2  3  4  5  6  7
      1  0 [1  1  0] 0  1  1
            L     R           zeros=1  len=3  best=4
```

`R = 4` brings a second zero; `L` steps past index 0 (a one) and index 1 (a zero), and `zeros` drops back to 1.

Frame 3

```text
 i:   0  1  2  3  4  5  6  7
      1  0  1  1  0 [0] 1  1
                     L=R      zeros=1  len=1  best=4
```

`R = 5` brings another zero; `L` must pass two ones and the zero at 4, landing on 5.

Frame 4

```text
 i:   0  1  2  3  4  5  6  7
      1  0  1  1  0 [0  1  1]
                     L     R  zeros=1  len=3  best=4
```

`R` walks 6 and 7, adding ones. The array ends; the answer is 4.

In every frame, after the `while` loop, the window held at most one zero, and `L` was as far left as possible for that `R`. Neither edge ever moved left.

## Why it is correct

Invariant after processing `R`: `[L, R]` is the longest window ending at `R` with at most `k` zeros, and `zeros` equals the number of zeros in it.

The counter part is bookkeeping: each index adds 1 when it enters if it is a zero and subtracts 1 when it leaves if it is a zero. For the window part, the claim above showed that the best start for `R` is at least the best start for `R - 1`, so starting the search from the old `L` loses nothing. The `while` advances `L` exactly until the window becomes legal, which is the leftmost legal start. Every optimal stretch ends at some `R`, and we recorded the best window for every `R`, so `best` is the answer.

Edge case `k = 0`: the rule becomes "no zeros", and the loop finds the longest run of ones, including 0 if the array is all zeros.

## Cost

- Time O(n): `R` advances n times; `L` advances at most n times in total.
- Space O(1): `L`, `zeros`, `best`.

## Variations you will meet

- **Max Consecutive Ones II (LeetCode 487, k = 1).** Same loop. A streaming follow-up asks you to handle input you cannot revisit: instead of reading `nums[L]` again, store the index of the last zero (or a queue of the last k zero positions) and jump `L` past the oldest one.
- **Longest subarray of 1s after deleting one element (LeetCode 1493).** `k = 1`, but the answer is `R - L` because the flipped element is deleted rather than kept.
- **Flip at most k ones to zeros** or any "at most k bad items" rule: replace the test `x == 0` with whatever "bad" means.
- **Count subarrays with at most k zeros.** Same window; add `R - L + 1` to the total at each step instead of taking a max. This counting move returns in Subarrays with K Different Integers.

## What to carry forward

Memory hook: "change at most k things to make a run" means "longest window with at most k bad items", and a bad-item counter is the whole summary.

The next problem, Fruit Into Baskets, keeps the "at most k" rule but counts *distinct values* instead of bad items, so the single counter grows into a count map whose number of keys is the rule.
