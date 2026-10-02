# Create Maximum Number

*LeetCode 321 · Hard · Pattern: Monotonic stack + greedy merge · Reading time ~12 min*

## What the problem is really asking

You have two arrays of digits, `nums1` (length `m`) and `nums2` (length `n`), and a target length `k <= m + n`. Pick `k` digits in total from the two arrays, keeping each array's digits in their original relative order, and interleave them however you like. Make the resulting `k`-digit number as large as possible. Return its digits.

The answer is a list of digits, compared lexicographically: the first digit matters more than everything after it combined. That single fact drives the whole solution. What makes it hard is that three decisions are tangled together: how many digits to take from each array, which ones, and in what interleaving.

```text
nums1 = 3 4 6 5             k = 5
nums2 = 9 1 2 5 8 3

take from nums1: . . 6 5     (2 digits)
take from nums2: 9 . . . 8 3 (3 digits)
interleave:      9 8 6 5 3   <- answer
                 ^ ^     ^  from nums2
                     ^ ^    from nums1
```

## Do it by hand first

Start with a smaller question: from `nums2 = 9 1 2 5 8 3` alone, keep 3 digits to make the biggest number. You can delete 3 digits. Read left to right and keep the digits you have so far on a pad.

```text
read 9: pad 9               (deletions left 3)
read 1: pad 9 1             1 < 9, keep for now
read 2: 2 > 1 -> erase 1    pad 9 2      (left 2)
read 5: 5 > 2 -> erase 2    pad 9 5      (left 1)
read 8: 8 > 5 -> erase 5    pad 9 8      (left 0)
read 3: no deletions left   pad 9 8 3
```

Your instinct was: whenever a bigger digit shows up and you can still afford to delete, erase the smaller digits just before it, because the bigger digit will then occupy a more significant position. You only ever erased from the end of the pad. The pad stayed in non-increasing order as long as deletions were available. That pad is a monotonic stack, and the only thing you counted was the deletion budget.

Now the second half by hand: you have picked `6 5` from `nums1` and `9 8 3` from `nums2`. Zip them: at each step take the larger front digit. `9` vs `6`: take 9. `8` vs `6`: take 8. `3` vs `6`: take 6. `3` vs `5`: take 5. Then 3. Result `9 8 6 5 3`. And the question of how many digits from each array? Try all splits; there are at most `k + 1`.

## The first honest attempt

Enumerate everything: for each split `i` (digits from `nums1`), every subsequence of size `i` of `nums1`, every subsequence of size `k - i` of `nums2`, and every order-preserving interleaving of the two; keep the lexicographically largest. That is exponential: up to `2^m * 2^n * C(k, i)` candidates. Correct for arrays of length 5, useless beyond.

```text
split i=2, nums1 picks:   34 36 35 46 45 65
           nums2 picks:   912 915 918 ... 983
           interleavings of each pair: C(5,2)=10
                          ~~~~~~~~~~~~~~~~~~~~~
"best 3 digits of nums2" is re-derived inside
every pairing, though it does not depend on nums1
```

The waste: the best subsequence of one array does not depend on what you pick from the other. For a fixed split, nums2's 3 digits are always `9 8 3`, no matter what nums1 contributes. The brute force recomputes it for every partner and every interleaving, and drags along subsequences that are already beaten in their first digit.

## The turning point

**Claim: for a fixed split, the answer is `merge(best(nums1, i), best(nums2, k - i))`, where `best` is a monotonic-stack greedy and `merge` is a greedy zip that breaks ties by comparing the remaining tails.**

There are three pieces.

**1. Splits are independent; try all of them.** For `i` from `max(0, k - n)` to `min(k, m)`, take `i` digits from `nums1` and `k - i` from `nums2`. At most `k + 1` candidates; keep the largest.

**2. `best(nums, t)`: the largest subsequence of length `t`.** You may drop `d = len(nums) - t` digits. Walk the array with a stack. Before pushing digit `x`, while you still have drops left and the top is smaller than `x`, pop it and spend a drop. Then push `x`. At the end, if drops were left over (the input was, say, increasing at the tail), cut the stack to its first `t` digits.

Why popping is right: if the top `y` is smaller than `x` and you can afford to drop `y`, then `x` slides one place left into `y`'s position. Every number that keeps `y` in that position starts with the same prefix and then `y`, while the number with `x` there has the same prefix and then `x > y`. Lexicographically the second wins, whatever follows. So dropping `y` is never worse.

**3. `merge(a, b)`: the largest interleaving.** At each step take the front digit of whichever list is lexicographically larger *as a whole remaining tail*. If the fronts differ, that is just the bigger front digit. If they are equal, the tie must be broken by looking further:

```text
a = 6 7        b = 6 0 4
fronts equal (6 vs 6). compare tails:
  [6,7] > [6,0,4]  -> take a's 6 first
result: 6 7 6 0 4   (correct)

heads-only, taking b's 6 first:
        6 6 7 0 4   (smaller: 6 6 < 6 7)
```

Taking from `a` first exposes its 7 sooner; taking from `b` would expose a 0. Comparing whole tails (Python's list comparison does exactly this) picks the stream whose next differing digit is larger.

The monotonic stack is the heart of piece 2. Notice how it differs from the rest of the chapter: in Daily Temperatures and the histograms a pop *recorded an answer* for the popped element; here a pop *deletes* it, and the budget `d` limits how many deletions we may make.

## Watch it work

`nums1 = [3,4,6,5]`, `nums2 = [9,1,2,5,8,3]`, `k = 5`. We follow split `i = 2` in detail: `best(nums2, 3)` with drop budget `6 - 3 = 3`. The staircase lists the stack bottom-first, one `#` per unit of the digit's value. All states below are from running the solution's `pick` and `merge`.

Frame 1 — read 9 and 1; nothing to pop (1 < 9).

```text
nums2: 9 1 2 5 8 3
         ^          drops left: 3
staircase:
  9 |#########
  1 |#              <- top
```

A non-increasing staircase, exactly like the waiting days of Daily Temperatures.

Frame 2 — read 2: 1 < 2 and a drop is left, so pop 1.

```text
nums2: 9 1 2 5 8 3
           ^        drops left: 2
pop 1 (dropped for good)
staircase:
  9 |#########
  2 |##             <- top
```

Frame 3 — read 5: pop 2.

```text
nums2: 9 1 2 5 8 3
             ^      drops left: 1
pop 2
staircase:
  9 |#########
  5 |#####          <- top
```

Frame 4 — read 8: pop 5; the budget is now spent.

```text
nums2: 9 1 2 5 8 3
               ^    drops left: 0
pop 5; 9 > 8 stops the loop anyway
staircase:
  9 |#########
  8 |########       <- top
```

Frame 5 — read 3: no drops left, push.

```text
nums2: 9 1 2 5 8 3
                 ^  drops left: 0
staircase:
  9 |#########
  8 |########
  3 |###            <- top
best(nums2, 3) = 9 8 3
```

Frame 6 — `best(nums1, 2)` with budget 2: 4 pops 3, 6 pops 4, 5 is pushed.

```text
nums1: 3 4 6 5      drops: 2 -> 1 -> 0
read 3: [3]   read 4: pop 3 -> [4]
read 6: pop 4 -> [6]   read 5: [6 5]
staircase:
  6 |######
  5 |#####          <- top
best(nums1, 2) = 6 5
```

Frame 7 — merge `6 5` with `9 8 3` by comparing tails.

```text
a = 6 5     b = 9 8 3     out
[6,5]   vs [9,8,3] -> b   9
[6,5]   vs [8,3]   -> b   9 8
[6,5]   vs [3]     -> a   9 8 6
[5]     vs [3]     -> a   9 8 6 5
[]      vs [3]     -> b   9 8 6 5 3
```

Frame 8 — every split, then the max.

```text
i  best(nums1,i)  best(nums2,5-i)  merged
0  -              9 2 5 8 3        9 2 5 8 3
1  6              9 5 8 3          9 6 5 8 3
2  6 5            9 8 3            9 8 6 5 3  <- max
3  4 6 5          9 8              9 8 4 6 5
4  3 4 6 5        9                9 3 4 6 5
```

Inside each `best` call the staircase never rose while drops remained, and every popped digit was gone for good the moment it was popped. Splits 0 and 1 show the budget at work: with more digits required from `nums2`, fewer can be dropped, so weaker digits like 2 and 5 survive.

## Why it is correct

**`best` — the popped element's fate is fixed at pop time.** Claim: whenever we pop `y` because `x > y` arrives and a drop is available, some optimal length-`t` subsequence does not contain this `y`. Exchange argument: say the stack below `y` holds `s` digits, so `y` occupies output slot `s`. Any candidate that keeps this `y` has the same `s`-digit prefix and then `y`. Now build a rival: the same prefix, then `x` in slot `s`, then any digits after `x` to fill the remaining `t - s - 1` slots. Enough digits exist, because a drop is still available: the digits from `x` onward number at least the slots still to fill. The rival agrees with every `y`-candidate on the prefix and then has `x > y`, so it is strictly larger whatever follows. Hence no optimal answer keeps a popped `y`; its fate is sealed at pop time and never revisited. Pushes are equally safe: when we push without popping, either the top is at least `x` (dropping the top could not raise that position) or the budget is spent (we must keep everything that remains). Finally, the stack holds at least `t` digits because we drop at most `d`; truncating to the first `t` removes the smallest-impact tail when the budget was not fully used, which can only be the least significant positions.

**`merge`.** Invariant: the output so far is a prefix of the best interleaving. At each step, if the fronts differ, the bigger front must come next, since any interleaving putting the smaller digit here loses at this position. If the fronts are equal, both choices write the same digit now; what differs is which digits become available next. Taking from the lexicographically larger tail keeps available the stronger continuation: any interleaving that starts by taking from the smaller tail can be matched digit for digit by one taking from the larger tail, until the first difference, where the larger tail offers the bigger digit. So the greedy choice never loses.

**Splits.** For a fixed number `i` of digits from `nums1`, the best final number uses `best(nums1, i)` and `best(nums2, k - i)`: replacing either chosen subsequence with a lexicographically larger one of the same length never makes the best merge smaller. Trying every feasible `i` and keeping the maximum covers the optimum.

## Cost

Time O(k * (m + n + k^2)): there are at most `k + 1` splits; each runs two stack passes, O(m + n), and a merge of length `k` whose tail comparisons can cost O(k) each, so O(k^2) per merge in the worst case.

Space O(m + n + k): the two stacks and the merged candidate.

The brute force is exponential. Replacing the tail-slice comparison with an index-based comparison that stops at the first difference avoids the copying but keeps the same worst case; a suffix-array merge reduces the merge to O(k).

## Variations you will meet

- **Remove K Digits** (LeetCode 402). The single-array version for the *smallest* number: pop while the top is *larger* than the incoming digit, then strip leading zeros. It is piece 2 alone, with the comparison flipped.
- **Smallest Subsequence of Distinct Characters** (LeetCode 1081, and 316). The stack may pop a character only if it appears again later, and each character must appear exactly once. The "budget" becomes a per-character remaining count.
- **Most competitive subsequence** (LeetCode 1673). Smallest length-`k` subsequence of one array; exactly `best` with a flipped comparison.
- **Largest number by merging two strings** (LeetCode 1754). Merge alone, no picking: the tail-comparison rule is the entire solution.

## What to carry forward

A monotonic stack with a deletion budget picks the best subsequence: a bigger digit pops smaller ones before it while you can still afford to drop them, and a pop is final. When two streams must be zipped, break ties by comparing what remains, not just the heads.

This closes the chapter. You have seen the stack in its three roles: matching (brackets and expressions, where a pop closes a group), answering (next greater, fleets, histograms, where a pop fixes the popped element's answer), and choosing (this problem, where a pop discards). Faced with a fresh problem, ask which of the three the pop should mean.
