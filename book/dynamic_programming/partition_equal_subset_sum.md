# Partition Equal Subset Sum

*LeetCode 416 · Medium · Pattern: 0/1 knapsack reachability (bitset) · Reading time ~7 min*

## What the problem is really asking

Given positive integers, can you split them into two groups with equal sums? Every number goes into exactly one group.

Rephrase it once and the problem shrinks. If the total is odd, no split exists. If it is even, the two groups each sum to `total / 2`, and choosing one group decides the other. So the real question is: **does some subset sum to exactly `target = total / 2`?** The answer is a yes/no. What makes it hard is that there are `2^n` subsets, and no ordering or greedy rule tells you which numbers to pick.

```text
 nums = [1, 5, 11, 5]     total = 22, target = 11

   group A: [1, 5, 5]  = 11
   group B: [11]       = 11      -> True

 nums = [1, 2, 3, 5]      total = 11 (odd) -> False at once
```

## Do it by hand first

Process the numbers one at a time and keep a list of every sum you could have made so far. Start with only 0 (the empty subset). Each new number `x` lets every old sum `s` either stay (skip `x`) or become `s + x` (take `x`).

```text
 start           sums: {0}
 take/skip 1     sums: {0, 1}
 take/skip 5     sums: {0, 1, 5, 6}
 take/skip 11    sums: {0, 1, 5, 6, 11, 12, 16, 17}
                                    ^^ target 11 reachable
```

Your hand did not remember *which* numbers made each sum, only *whether* the sum was possible. That set of reachable sums is the entire state you need.

## The first honest attempt

Recursion on the next index and the remaining target: `can(i, t)` = can some subset of `nums[i:]` sum to `t`? Take `nums[i]` (ask `can(i+1, t - nums[i])`) or skip it (ask `can(i+1, t)`). Success at `t == 0`, failure when `t < 0` or the numbers run out.

That explores all `2^n` take/skip patterns. The repeated work is that different histories land on the same pair `(i, t)`:

```text
 nums = [1, 2, 3, 4, 6, 4]   target 10

 history A: take 1, take 2, skip 3   -> at i=3, t = 7
 history B: skip 1, skip 2, take 3   -> at i=3, t = 7
                                         |
         both now ask: can [4, 6, 4] make 7?
         both explore up to 8 patterns from scratch
```

Once you are at index `i` with `t` left, the past is irrelevant. There are only `n x (target + 1)` such pairs, but the recursion can visit each many times.

## The turning point

**Claim: the set of sums reachable with the first `i+1` numbers is the set reachable with the first `i`, united with that same set shifted up by `nums[i]`.**

Every subset of the first `i+1` numbers either excludes `nums[i]` (so its sum is in the old set) or includes it (so its sum is an old sum plus `nums[i]`). That is the recurrence; the answer is whether `target` ends up in the set.

- **State:** `reach_i` = set of sums some subset of `nums[:i]` can make.
- **Recurrence:** `reach_{i+1} = reach_i  U  (reach_i + nums[i])`.
- **Base:** `reach_0 = {0}`.
- **Order:** numbers in any order, one layer per number.
- **Answer:** `target in reach_n`. Sums above `target` can be ignored since all numbers are positive.

As a table this is 2-D, item by sum, each row reading only the row above. The space squeeze to one boolean row has a trap, the most important lesson in this problem:

```text
 one row, sweep t UPWARD, adding x = 5:
   t=5:  can[5] |= can[0]  -> True   (just set)
   t=10: can[10] |= can[5] -> True   WRONG: used 5 twice

 one row, sweep t DOWNWARD, adding x = 5:
   t=10: can[10] |= can[5] -> old value of can[5]
   t=5:  can[5]  |= can[0] -> True   (set after t=10 read it)
```

Sweeping upward reads cells already updated for the current number, which silently allows reuse: that is the *unbounded* knapsack of Coin Change. Sweeping downward reads only cells from the previous layer: each number used at most once, the **0/1 knapsack**.

The solution goes one step further and stores the whole row as the bits of a Python integer: bit `s` is 1 if sum `s` is reachable. "Shift every reachable sum up by `x` and unite" becomes one line:

```python
reach |= reach << x      # bit s set <=> some subset sums to s
```

The shift creates the "take x" copy from the old value of `reach` in a single operation, so the reuse trap cannot happen, and the machine processes 64 sums per word.

## Watch it work

`nums = [1, 5, 11, 5]`, target 11. The row shows bits 0..22, `#` for reachable.

```text
 sum:   0         1         2
        01234567890123456789012
```

**Frame 1.** Start: `reach = 1`, only sum 0.

```text
 reach: #......................     {0}
```

The empty subset makes 0.

**Frame 2.** `x = 1`: shift copy by 1 and OR.

```text
 old:   #......................
 <<1:   .#.....................
 new:   ##.....................     {0,1}
```

**Frame 3.** `x = 5`: shift by 5 and OR.

```text
 old:   ##.....................
 <<5:   .....##................
 new:   ##...##................     {0,1,5,6}
```

**Frame 4.** `x = 11`: shift by 11 and OR. Bit 11 lights up (the subset {11} alone).

```text
 old:   ##...##................
 <<11:  ...........##...##.....
 new:   ##...##....##...##.....     {0,1,5,6,11,12,16,17}
                   ^ bit 11
```

**Frame 5.** `x = 5`: shift by 5 and OR. Bit 11 also comes from 6 + 5 = {1,5,5}, and bit 22 (everything) appears.

```text
 old:   ##...##....##...##.....
 <<5:   .....##...##....##...##
 new:   ##...##...###...##...##
                   ^ bit 11 set -> True
```

Invariant across frames: after processing a number, the lit bits were exactly the subset sums of the numbers seen so far, each number counted at most once.

## Why it is correct

By induction on the layer. Before number `x`, `reach` holds exactly the subset sums of the earlier numbers. After `reach | (reach << x)`, a bit is set iff it was a subset sum without `x` or is one plus `x`, which is exactly the subset sums including the new number as an option. Since `reach << x` is computed from the old value before the OR, `x` is added at most once. At the end, bit `target` is set iff some subset sums to `target`, and then its complement sums to `total - target = target`.

## Cost

- **Brute force:** O(2^n) time, O(n) stack.
- **Boolean table or one row:** O(n x target) time, O(target) space.
- **Bitset:** the same O(n x total) bit operations, but about 64 per machine word, so roughly O(n x total / 64) time and O(total) bits. With `n <= 200` and values `<= 100`, total is at most 20,000 bits.

This is pseudo-polynomial: it depends on the numeric value of the sum, not just `n`. Huge values would make the table impractical, which is why the problem caps them.

## Variations you will meet

- **Subset Sum / "is there a subset summing to K":** drop the halving step; the same row.
- **Last Stone Weight II (LC 1049):** find the reachable sum closest to `total / 2`; scan the final row downward from `target`.
- **Partition to K Equal Sum Subsets (LC 698):** with k groups the sums no longer summarise the state; use backtracking with pruning or bitmask DP over used items.
- **0/1 knapsack with values:** the cell holds "best value for weight `w`" instead of a boolean, still swept downward.

## What to carry forward

Forget which items made a sum; keep only which sums are reachable, add each item once (downward sweep or shift of the old row). The next problem walks the same layered sums but with plus or minus signs, and asks how many ways reach the target instead of whether one does.
