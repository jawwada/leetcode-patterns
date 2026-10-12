# Min Cost Climbing Stairs

*LeetCode 746 · Easy · Pattern: 1-D DP over prefixes (Fibonacci-style) · Reading time ~5 min*

## The problem

cost[i] is the price of stepping on stair i; after paying you may climb one or two stairs, and you may start on stair
0 or 1. Return the minimum cost to reach the top, one position past the last stair.

```text
Example: [10,15,20] -> 15 (start on stair 1, pay 15, jump two to
  the top).
```

## What the problem is really asking

A staircase has a price tag on every step: `cost[i]` is what you pay to stand on step `i`. Once you have paid, you may climb one or two steps. You may begin on step 0 or step 1 for free. The "top" is the floor just past the last step. Find the cheapest total.

The answer is a single number, a minimum over all legal paths. The difficulty is that the number of paths explodes (each step offers two moves), while a choice that looks cheap now can force you onto an expensive step later.

```text
 cost:    1   100    1    1   100    1   | top
 step:    0    1     2    3    4     5   |  6
          *          *    *          *   -> paid 1+1+1+1 = 4
 path: start 0, +2 -> 2, +1 -> 3, +2 -> 5, +1 -> top
```

## Do it by hand first

Walk up the stairs from the bottom and, under each step, write the cheapest way to arrive there without having paid that step yet. Steps 0 and 1 are free to arrive at. For every later step, you either came from one below (and paid it) or from two below (and paid that).

```text
 step i:          0    1    2    3    4    5    6(top)
 cost[i]:         1  100    1    1  100    1
 cheapest here:   0    0    1    2    2    3    4
                            ^
             step 2: from 1 costs 0+100, from 0 costs 0+1 -> 1
```

Your hand kept one number per step, and to fill a box it only looked at the two boxes to its left. That row of boxes is the DP table; the "look two back" is the recurrence.

## The first honest attempt

Say it as recursion: the cheapest way from step `i` to the top is `cost[i]` plus the cheaper of continuing from `i+1` or from `i+2`. Anything at or past the top costs 0. Answer: the smaller of starting at 0 or at 1.

It is correct and exponential: two calls per call, a Fibonacci-shaped tree of about 1.6^n nodes. For six steps the tree from step 0 alone has 41 calls, though only eight distinct step numbers exist.

```text
                    f(0)
              /             \
          f(1)              f(2)  <-- solved here...
         /    \            /    \
     f(2)     f(3)      f(3)    f(4)
     ^ ...and here, from scratch, with its whole subtree
```

The waste is plain: `f(2)` is solved once directly and again inside `f(1)`, and `f(3)` three times.

## The turning point

**Claim: the cheapest cost to stand on step `i` depends only on the cheapest costs to stand on `i-1` and `i-2`.**

Any path that reaches step `i` makes its last move from `i-1` or from `i-2`. Whatever happened before that last move is a path to `i-1` (or `i-2`), and it might as well be the cheapest one: swapping in a cheaper prefix can only lower the total. So:

- **State:** `dp[i]` = cheapest cost to stand on position `i`, not yet having paid `cost[i]`.
- **Recurrence:** `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`.
- **Base cases:** `dp[0] = dp[1] = 0`, because you may start on either for free.
- **Order:** `i = 2 .. n` left to right; the answer is `dp[n]`, the top.
- **Space:** each cell reads only the two before it, so keep two rolling values `a = dp[i-2]` and `b = dp[i-1]`.

## Watch it work

`cost = [1, 100, 1, 1, 100, 1]`, n = 6.

**Frame 1.** Start: `a = dp[0] = 0`, `b = dp[1] = 0`.

```text
 pos:   0    1    2    3    4    5    6
 dp:  [ 0 ][ 0 ][   ][   ][   ][   ][   ]
        a    b
```

Both starting steps are free.

**Frame 2.** i = 2: from 1 costs `0 + 100`, from 0 costs `0 + 1`. New `b = 1`.

```text
 dp:  [ 0 ][ 0 ][ 1 ][   ][   ][   ][   ]
             a    b
```

The 100 on step 1 is avoided by jumping over it.

**Frame 3.** i = 3: from 2 costs `1 + 1 = 2`, from 1 costs `0 + 100`. i = 4: from 3 costs `2 + 1 = 3`, from 2 costs `1 + 1 = 2`. Now `a = 2`, `b = 2`.

```text
 dp:  [ 0 ][ 0 ][ 1 ][ 2 ][ 2 ][   ][   ]
                       a    b
```

Step 4 is reached most cheaply by a two-step jump from step 2.

**Frame 4.** i = 5: from 4 costs `2 + 100`, from 3 costs `2 + 1 = 3`. i = 6: from 5 costs `3 + 1 = 4`, from 4 costs `2 + 100`. Final `b = 4`.

```text
 dp:  [ 0 ][ 0 ][ 1 ][ 2 ][ 2 ][ 3 ][ 4 ]
                                 a    b  <- answer
```

Both 100s were jumped over; the top costs 4.

Across frames, `a` and `b` always held the final answers for the two positions just behind `i`, and once a cell was written it never changed.

## Why it is correct

Induction on `i`. Before step `i`, `a` and `b` are the true minimum costs to stand on `i-2` and `i-1`. Every way to stand on `i` ends with a move from one of those, paying that step's cost, and the cheapest such way uses the cheapest prefix. So the minimum of the two candidates is the true `dp[i]`. The shift then restores the invariant for `i+1`. At `i = n` the top's cost is in `b`.

## Cost

- **Time O(n):** one pass, constant work per position.
- **Space O(1):** two rolling numbers; the full table would be O(n) and the memoised recursion O(n) plus stack.

## Variations you will meet

- **Climbing Stairs (LC 70):** count paths instead of minimising: replace `min` with `+` and the costs with nothing. It is literally Fibonacci.
- **Steps of size 1..k:** each cell reads the last `k` cells; keep a deque or a sliding minimum.
- **Return the path:** keep the full table and walk back from `n`, choosing whichever predecessor produced the minimum.

## What to carry forward

A position's best cost is built from its last move; keep two numbers and slide them up the stairs. The next problem keeps this exact two-back shape but turns each cell into a decision, rob or skip, where taking one house forbids its neighbour.
