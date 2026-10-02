# House Robber

*LeetCode 198 · Medium · Pattern: 1-D DP over prefixes (Fibonacci-style) · Reading time ~6 min*

## What the problem is really asking

A row of houses, house `i` holding `nums[i]` money. You may rob any set of houses as long as no two chosen houses are next to each other (adjacent houses share an alarm). Return the most money you can take.

The answer is one number: the maximum sum over all "no two adjacent" subsets of indices. There are Fibonacci-many such subsets, and the hard part is that every choice has a side effect on the neighbour, so you cannot judge a house in isolation.

```text
 house:    0     1     2     3     4
 money:  [ 2 ] [ 7 ] [ 9 ] [ 3 ] [ 1 ]
           X           X           X      2 + 9 + 1 = 12
                 X           X            7 + 3     = 10
 X = robbed; no two X's touch
```

## Do it by hand first

Walk down the street with a notepad. At each house, write "the most I could have by now". At house 0 that is 2. At house 1 you either keep the 2 or take the 7 instead: 7. At house 2 you either keep the 7 (skip house 2) or take 9 on top of the best you had two houses back (2): 11.

```text
 house:        0    1    2    3    4
 money:        2    7    9    3    1
 best so far:  2    7   11   11   12
                         ^
         skip -> 7, or rob 9 + best-two-back 2 -> 11
```

Your notepad only ever looked at the last two entries. That is the seed: a row of running bests, each computed from the two before it.

## The first honest attempt

Two greedy ideas come first, and both fail.

```text
 "rob every other house" (evens vs odds):
   [2, 1, 1, 2]  evens 2+1 = 3, odds 1+2 = 3, best is 2+2 = 4

 "always grab the richest remaining house":
   [3, 4, 3]     grabs 4, blocks both 3s -> 4, best is 3+3 = 6
```

A local choice ("this house is big") cannot see that it blocks two houses whose sum is bigger. That is the textbook signal that the problem needs DP, not greedy.

The honest brute force is the decision recursion: `rob(i)` = the best from house `i` onward = `max(rob(i+1), nums[i] + rob(i+2))`. Skip house `i`, or take it and jump past its neighbour. Past the end the answer is 0.

```text
                       rob(0)
             skip /            \ take 2
             rob(1)             rob(2)   <-- here
       skip /     \ take 7     /     \
       rob(2)      rob(3)   rob(3)   rob(4)
       ^ and here, the same suffix [9, 3, 1] re-solved
```

Each call branches twice, so the tree has about 1.6^n nodes. The waste is that `rob(i)` depends only on `i`, the suffix of houses still ahead, not on which houses you robbed to get there. Yet the "take house 0" branch and the "skip house 0, skip house 1" branch both arrive at `rob(2)` and solve it twice. Further down, `rob(3)` is solved three times, `rob(4)` five times: the Fibonacci numbers again.

## The turning point

**Claim: the best loot from the first `i` houses is either the best from the first `i-1` houses, or `nums[i-1]` plus the best from the first `i-2` houses.**

Consider an optimal plan for the first `i` houses and look at the last house, `i-1`.

- If the plan skips it, the plan is just a plan for the first `i-1` houses, and it must be an optimal one (otherwise swap in a better one and the total improves).
- If the plan robs it, house `i-2` is forbidden, so the rest of the plan lives in the first `i-2` houses, and again it must be optimal there.

There is no third case. So with the four steps:

- **State:** `dp[i]` = most money from the first `i` houses.
- **Recurrence:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])`.
- **Base:** `dp[0] = 0` (no houses), and `dp[1] = nums[0]` follows from the recurrence if `dp[-1]` is treated as 0.
- **Order:** left to right.
- **Space:** only `dp[i-1]` and `dp[i-2]` are read, so keep two variables, `prev1` and `prev2`, starting at 0, 0.

Notice how the decision structure changed. The brute force asked "rob or skip?" and explored both futures. The DP asks the same question but about the *last* house, where both answers are already computed and you can simply take the larger. The future no longer needs exploring because it has been summarised by a number.

There is a quiet subtlety the original memoised version in the repo carried: it keyed on `(i, canRob)`, a flag for whether the previous house was robbed. That flag is the same information as "jump to `i+2` after a rob", so the DP needs only `i`. When you design a memo key, ask whether each component really changes the answer or is implied by the others.

## Watch it work

`nums = [2, 7, 9, 3, 1]`. The pair `(prev2, prev1)` is the best up to two houses back and one house back.

**Frame 1.** Before anything: `(prev2, prev1) = (0, 0)`. House 0 holds 2: `max(0, 0 + 2) = 2`.

```text
 money:  [ 2 ] [ 7 ] [ 9 ] [ 3 ] [ 1 ]
 best:     2
 (prev2, prev1) = (0, 2)
```

With one house, rob it.

**Frame 2.** House 1 holds 7: `max(skip 2, rob 0 + 7) = 7`.

```text
 money:  [ 2 ] [ 7 ] [ 9 ] [ 3 ] [ 1 ]
 best:     2     7
 (prev2, prev1) = (2, 7)
```

Robbing 7 beats keeping 2; the plan is now {house 1}.

**Frame 3.** House 2 holds 9: `max(skip 7, rob 2 + 9) = 11`.

```text
 money:  [ 2 ] [ 7 ] [ 9 ] [ 3 ] [ 1 ]
 best:     2     7    11
 (prev2, prev1) = (7, 11)
```

The plan switched to {0, 2}: the earlier choice of 7 was abandoned without any backtracking.

**Frame 4.** House 3 holds 3: `max(skip 11, rob 7 + 3) = 11`.

```text
 money:  [ 2 ] [ 7 ] [ 9 ] [ 3 ] [ 1 ]
 best:     2     7    11    11
 (prev2, prev1) = (11, 11)
```

Skipping wins; robbing 3 would cost us the 9.

**Frame 5.** House 4 holds 1: `max(skip 11, rob 11 + 1) = 12`.

```text
 money:  [ 2 ] [ 7 ] [ 9 ] [ 3 ] [ 1 ]
 best:     2     7    11    11    12  <- answer
 (prev2, prev1) = (11, 12)
```

The plan is {0, 2, 4} for 12.

Invariant across frames: `prev1` was always the true best for the houses seen so far and `prev2` the true best for all but the last one. The "plan" behind `prev1` changed freely (Frame 3), which is exactly what greedy could not do.

## Why it is correct

By induction. Before house `i` is processed, `prev2 = dp[i-1]` and `prev1 = dp[i]` in prefix terms are correct. The case split on the last house (robbed or skipped) covers every legal plan, and each case's best is built from an optimal smaller plan by the exchange argument above, so `max(prev1, prev2 + x)` is the true optimum for the longer prefix. The shift `prev2, prev1 = prev1, new` restores the invariant. After the last house, `prev1` is the answer.

The one-line update must compute the new value from the *old* `prev1` and `prev2`; Python's tuple assignment guarantees this.

## Cost

- **Brute force:** O(1.6^n) time, O(n) stack.
- **Memoised recursion or full table:** O(n) time, O(n) space.
- **Rolling pair:** O(n) time, O(1) space, one pass with two variables.

## Variations you will meet

- **House Robber II (LC 213), houses in a circle:** the first and last are adjacent. Run the linear DP twice, once without the first house and once without the last, and take the larger.
- **House Robber III (LC 337), houses on a binary tree:** the state moves to a node and returns a pair (best if robbed, best if not); parents combine children's pairs.
- **Delete and Earn (LC 740):** bucket equal values, then picking value `v` forbids `v-1` and `v+1`, which is House Robber over the value line.
- **Return which houses:** keep the full table and walk back from the end, taking house `i-1` whenever `dp[i] != dp[i-1]`.

## What to carry forward

Ask about the last item: skipped means "best of one shorter", taken means "it plus best of two shorter". The next problem keeps the two-back shape but counts instead of maximising, and adds validity checks that can turn either look-back off.
