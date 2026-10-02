# Coin Change

*LeetCode 322 · Medium · Pattern: Unbounded knapsack (min coins per amount) · Reading time ~6 min*

## What the problem is really asking

You have coin denominations, as many of each as you like, and a target amount. Return the fewest coins that add up to exactly the amount, or -1 if no combination does. Amount 0 needs 0 coins.

The answer is a minimum count. What makes it hard is that the obvious greedy, "take the biggest coin that fits", is wrong for many coin systems, and the number of multisets of coins summing to the amount is enormous.

```text
 coins = [1, 3, 4], amount = 6

 greedy (biggest first):  4 + 1 + 1   -> 3 coins
 best:                    3 + 3       -> 2 coins

 number line:  0 ---3---> 3 ---3---> 6     2 jumps
               0 ----4----> 4 -1-> 5 -1-> 6   3 jumps
```

## Do it by hand first

Build up from small amounts. For each amount, ask: what could the last coin have been? If the last coin was `c`, the rest is the amount `a - c`, which you already solved.

```text
 amount:     0   1   2   3   4   5   6
 fewest:     0   1   2   1   1   2   2
                                     ^
   6: last coin 1 -> fewest(5)+1 = 3
      last coin 3 -> fewest(3)+1 = 2   <- best
      last coin 4 -> fewest(2)+1 = 3
```

Your hand kept one number per amount, and to fill amount `a` it looked back at `a-1`, `a-3`, `a-4`: one look-back per coin. That row is the table, and "try each coin as the last one" is the recurrence.

## The first honest attempt

The recursion follows directly: `f(a) = 1 + min(f(a - c))` over coins `c <= a`, with `f(0) = 0`, and infinity when no coin fits.

```text
                          f(6)
             -1 /         -3 |         \ -4
            f(5)            f(3)        f(2)  <--
       -1 / -3 |  \ -4    -1/ \-3       -1 |
       f(4)   f(2)  f(1)  f(2) f(0)      f(1)
              ^             ^
          f(2) solved three times already, and
          each copy rebuilds its own subtree
```

The tree branches `k` ways (one per coin) and can be `amount` levels deep (using only 1s), so its size is up to `k^amount`. The waste: `f(a)` depends only on the amount `a`, not on which coins were spent to get down to it. Paths 6-4, 6-3-1, and 6-1-3 all land on `f(2)`, and each one solves it again from scratch.

There is also no greedy shortcut. Greedy picks the largest coin `4` at amount 6 and commits; it cannot know that leaving 2 is worse than leaving 3. The best first coin depends on what the remainder will cost, which is information from the future. That is exactly the gap DP fills.

## The turning point

**Claim: an optimal set of coins for amount `a` has some last coin `c`, and removing it leaves an optimal set for `a - c`.**

If the remaining coins for `a - c` were not optimal, replace them with a smaller set for `a - c`, add `c` back, and you have a smaller set for `a`, a contradiction. So the best for `a` is "one coin, plus the best for what is left", minimised over the possible last coins.

- **State:** `dp[a]` = fewest coins summing to exactly `a` (infinity if impossible).
- **Recurrence:** `dp[a] = 1 + min(dp[a - c] for c in coins if c <= a)`.
- **Base:** `dp[0] = 0`.
- **Order:** `a = 1, 2, ..., amount` ascending, so every `dp[a - c]` (a smaller amount) is final when read.
- **Answer:** `dp[amount]`, or -1 if it is still infinity.

The solution uses `amount + 1` as infinity: no answer can need more than `amount` coins (that would be all 1s), so `amount + 1` is safely "impossible" and keeps everything an integer.

Why is this called **unbounded** knapsack? Because a coin can be used again and again. When `dp[a]` uses coin `c`, it reads `dp[a - c]`, which may itself have used `c`. Nothing stops reuse, and nothing should. Compare that with the next problem, where each number may be used at most once and the loop must be arranged to forbid reuse.

A useful second picture: amounts are nodes on a number line, and each coin is an edge jumping `c` to the right. `dp[a]` is the fewest jumps from 0 to `a`: an unweighted shortest path. Breadth-first search from 0 would find the same answer layer by layer. The table works because every edge points rightward, so ascending order is a topological order.

```text
   +1   +1   +1   +1   +1   +1
 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
 |              ^              ^
 +----- +3 -----+----- +3 -----+
 (+4 edges too: 0->4, 1->5, 2->6)
```

## Watch it work

`coins = [1, 3, 4]`, `amount = 6`, infinity shown as `inf` (the code stores 7).

**Frame 1.** Base, then `a = 1`: only coin 1 fits, `dp[0] + 1 = 1`. `a = 2`: only coin 1, `dp[1] + 1 = 2`.

```text
 a:     0    1    2    3    4    5    6
 dp:  [ 0 ][ 1 ][ 2 ][inf][inf][inf][inf]
```

Small amounts can only be made of 1s.

**Frame 2.** `a = 3`: coin 1 gives `dp[2]+1 = 3`, coin 3 gives `dp[0]+1 = 1`. Keep 1.

```text
 a:     0    1    2    3    4    5    6
 dp:  [ 0 ][ 1 ][ 2 ][ 1 ][inf][inf][inf]
        ^              |
        +---- +3 ------+
```

A single 3-coin beats three 1s.

**Frame 3.** `a = 4`: coin 1 gives `dp[3]+1 = 2`, coin 3 gives `dp[1]+1 = 2`, coin 4 gives `dp[0]+1 = 1`. Keep 1.

```text
 a:     0    1    2    3    4    5    6
 dp:  [ 0 ][ 1 ][ 2 ][ 1 ][ 1 ][inf][inf]
```

**Frame 4.** `a = 5`: coin 1 gives `dp[4]+1 = 2`, coin 3 gives `dp[2]+1 = 3`, coin 4 gives `dp[1]+1 = 2`. Keep 2.

```text
 a:     0    1    2    3    4    5    6
 dp:  [ 0 ][ 1 ][ 2 ][ 1 ][ 1 ][ 2 ][inf]
```

Two different last coins tie; either 4+1 or 1+4 is fine.

**Frame 5.** `a = 6`: coin 1 gives `dp[5]+1 = 3`, coin 3 gives `dp[3]+1 = 2`, coin 4 gives `dp[2]+1 = 3`. Keep 2.

```text
 a:     0    1    2    3    4    5    6
 dp:  [ 0 ][ 1 ][ 2 ][ 1 ][ 1 ][ 2 ][ 2 ] <- answer
                      ^                |
                      +----- +3 -------+
```

The answer 2 comes through amount 3, the remainder greedy never considered.

Invariant across frames: every cell left of the current amount held its final minimum, and each new cell read only those finished cells.

## Why it is correct

Induction on `a`. Assume `dp[b]` is the true minimum for every `b < a`. Every way to make `a` has a last coin `c`; the cheapest way with that last coin costs `1 + dp[a - c]` by the exchange argument above; the minimum over `c` covers every possibility. If no coin fits or every `dp[a - c]` is infinity, `dp[a]` stays infinity, correctly meaning "impossible". Ascending order guarantees the assumption holds at every step.

## Cost

- **Brute force:** up to O(k^amount) time, O(amount) stack.
- **Table:** O(amount x k) time (amount cells, k coins each), O(amount) space. The memoised recursion has the same cost but can hit Python's recursion limit for large amounts; the loop cannot.

## Variations you will meet

- **Coin Change II (LC 518), count the combinations:** replace `min` with `+`, and put the coin loop *outside* the amount loop so each combination is counted once regardless of order (amount-outside counts ordered sequences instead).
- **Perfect Squares (LC 279):** the coins are 1, 4, 9, 16, ...; identical recurrence.
- **Combination Sum IV (LC 377):** counts ordered sequences, so the amount loop goes outside.
- **Reconstruct the coins:** store the winning last coin per amount and follow it back from `amount` to 0.

## What to carry forward

"What was the last coin?" turns an exponential search into one look-back per coin per amount; ascending amounts make every look-back final. The next problem keeps a table indexed by sums, but each number may be used only once, and the question becomes yes or no.
