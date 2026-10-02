# Target Sum

*LeetCode 494 · Medium · Pattern: Count ways per reachable sum · Reading time ~6 min*

## What the problem is really asking

Put a `+` or a `-` in front of every number, evaluate the expression, and count how many of the `2^n` sign assignments give exactly `target`. Different positions count as different assignments even when the numbers are equal, and `+0` and `-0` are two different assignments.

The answer is a count. What makes it hard is that `2^n` grows quickly (n is up to 20, so about a million patterns, and in variants far more), and nothing about the order of the numbers lets you prune: any prefix can still be repaired by later signs.

```text
 nums = [1, 1, 1, 1, 1], target = 3

   -1 +1 +1 +1 +1 = 3
   +1 -1 +1 +1 +1 = 3
   +1 +1 -1 +1 +1 = 3       one '-' among five 1s:
   +1 +1 +1 -1 +1 = 3       5 positions -> answer 5
   +1 +1 +1 +1 -1 = 3
```

## Do it by hand first

Move a token along a number line. It starts at 0; each number pushes it left or right by that amount. Instead of following every path separately, write on each point how many paths are standing there after each number.

```text
 sum:        -3  -2  -1   0   1   2   3
 start:                   1
 after 1:             1       1
 after 2:         1       2       1
 after 3:     1       3       3       1
```

Your hand stopped tracking individual sign strings the moment two of them landed on the same point; it just added their counts. That is Pascal's triangle, and the map "sum -> number of ways" is the state.

## The first honest attempt

Recursion over the index and the running sum: `ways(i, s) = ways(i+1, s + nums[i]) + ways(i+1, s - nums[i])`, and at the end, 1 if `s == target` else 0. It enumerates all `2^n` sign patterns.

```text
                       ways(0, 0)
                 +1 /             \ -1
            ways(1, 1)            ways(1, -1)
           +1/      \-1          +1/       \-1
     ways(2,2)   ways(2,0)   ways(2,0)   ways(2,-2)
                     ^           ^
          "+1 -1" and "-1 +1" reach the same state
          and each solves the remaining 3 numbers alone
```

The waste: the number of ways to finish depends only on `(i, s)`, where you are and what the running sum is, not on the signs that got you there. The running sum lies between `-total` and `+total`, so there are at most `n x (2 x total + 1)` distinct states, yet the tree can visit them exponentially often.

## The turning point

**Claim: after processing the first `i` numbers, all you need is a count for each reachable running sum; the next number splits every count into two and merges equal sums by adding.**

Every sign pattern of `nums[:i+1]` is a sign pattern of `nums[:i]` followed by `+x` or `-x`. So a pattern ends at sum `s'` after `i+1` numbers exactly when its prefix ended at `s' - x` (and chose `+`) or at `s' + x` (and chose `-`). The two groups are disjoint (different last sign), so the counts add.

- **State:** `counts_i[s]` = number of sign patterns of `nums[:i]` whose sum is `s`.
- **Recurrence:** for each `(s, c)` in `counts_i`: `counts_{i+1}[s + x] += c` and `counts_{i+1}[s - x] += c`.
- **Base:** `counts_0 = {0: 1}` (no numbers, one empty pattern, sum 0).
- **Order:** one layer per number, left to right; each layer reads only the previous one.
- **Answer:** `counts_n.get(target, 0)`.

This is the previous problem's layered sums with two changes. First, the cell holds a count instead of a boolean, so "OR" becomes "+". Second, sums can be negative. An array would need an offset of `total` to index them; the solution instead uses a dictionary, which also stays small when few sums are reachable. And because each layer is built into a fresh dictionary `nxt`, there is no loop-direction trap: the old layer is never modified while being read.

There is a well-known algebraic shortcut too. Call `P` the sum of the numbers given `+` and `N` the sum given `-`. Then `P - N = target` and `P + N = total`, so `P = (total + target) / 2`. The question becomes "how many subsets sum to `P`?", a counting version of the previous problem's 0/1 knapsack, with one row swept downward. It needs two guards: `total + target` must be even and non-negative, otherwise the answer is 0. The dictionary version needs no guards, which is why the solution prefers it.

## Watch it work

`nums = [1, 1, 1, 1, 1]`, `target = 3`. Each frame shows the dictionary as counts on a number line.

**Frame 1.** Start `{0: 1}`, then the first 1 splits it.

```text
 sum:    -5  -4  -3  -2  -1   0   1   2   3   4   5
 i=0:                         1
 i=1:                     1       1
```

Two patterns: `+1` and `-1`.

**Frame 2.** Second 1: sum 0 is reached from 1 (via -1) and from -1 (via +1), so it merges to 2.

```text
 sum:    -5  -4  -3  -2  -1   0   1   2   3   4   5
 i=2:                 1       2       1
```

Four patterns now live in three entries.

**Frame 3.** Third 1: counts `1, 3, 3, 1`.

```text
 sum:    -5  -4  -3  -2  -1   0   1   2   3   4   5
 i=3:             1       3       3       1
```

**Frame 4.** Fourth 1: counts `1, 4, 6, 4, 1`.

```text
 sum:    -5  -4  -3  -2  -1   0   1   2   3   4   5
 i=4:         1       4       6       4       1
```

Sixteen patterns, five dictionary entries.

**Frame 5.** Fifth 1: counts `1, 5, 10, 10, 5, 1`. Read the entry at 3.

```text
 sum:    -5  -4  -3  -2  -1   0   1   2   3   4   5
 i=5:     1       5      10      10       5       1
                                          ^
                                   target 3 -> 5
```

Thirty-two patterns collapsed into six numbers; the answer is 5.

Invariant across frames: the counts in each layer always added up to `2^i`, and each entry was the exact number of sign patterns of the first `i` numbers ending at that sum.

## Why it is correct

Induction on `i`. If `counts_i` is exact, then every pattern of length `i+1` is counted exactly once in `counts_{i+1}`: it is found under its prefix's sum, pushed by its last sign to its own sum, and no other prefix or sign produces the same pattern. Patterns with different sums are never mixed; patterns with the same sum are added, which is exactly what "count" means. After `n` layers, the entry at `target` counts the assignments that evaluate to `target`.

The zero case falls out naturally: `x = 0` sends each count to `s + 0` and to `s - 0`, the same key twice, doubling it, which matches the two distinct assignments `+0` and `-0`.

## Cost

- **Brute force:** O(2^n) time, O(n) stack.
- **Layered dictionary:** at most `2 x total + 1` keys per layer, so O(n x total) time and O(total) space.
- **Subset-count rewrite:** O(n x P) time, O(P) space with one downward-swept row, roughly half the range.

## Variations you will meet

- **Subset-count form directly ("number of subsets summing to K"):** the rewrite above with `dp[s] += dp[s - x]`, swept downward.
- **Ones and Zeroes (LC 474):** two capacities instead of one sum; the table becomes 2-D per item, still swept downward.
- **Expression with `*` or concatenation:** sums no longer summarise the state; that is backtracking (Expression Add Operators).
- **Count modulo 10^9+7:** counts in similar problems explode; reduce at every addition.

## What to carry forward

When many paths land on the same state, store the number of paths there and add, never enumerate; booleans become counts and OR becomes plus. The next problem leaves one-dimensional sums behind: its state is a pair of positions in two strings, and the table becomes a true 2-D grid.
