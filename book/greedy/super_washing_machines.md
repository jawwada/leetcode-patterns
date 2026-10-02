# Super Washing Machines

*LeetCode 517 · Hard · Pattern: Prefix-sum flow bound · Reading time ~9 min*

## What the problem is really asking

Washing machines stand in a row, machine `i` holding `machines[i]` dresses. In one move you choose any set of machines, and each chosen machine passes exactly one dress to a neighbour (left or right), all at the same time. Find the minimum number of moves that leaves every machine with the same count, or -1 if that is impossible.

The answer is a count of rounds, not a count of dresses moved. That is what makes it slippery. Many dresses travel in parallel in a single move, so the cost is set by whatever is the slowest, most congested part of the transfer. You need to find the bottleneck without simulating the schedule.

The impossibility check is easy: the final count per machine is `total / n`, which must be a whole number.

```text
machines = [1, 0, 5]     total 6, n 3, target 2

 move 0:  [1] [0] [5]
 move 1:  [1] [1] [4]    m2 -> m1
 move 2:  [2] [1] [3]    m1 -> m0, m2 -> m1  (parallel)
 move 3:  [2] [2] [2]    m2 -> m1
                         answer 3
```

Machine 2 has 3 dresses too many and can only release one per move, so 3 moves is a floor, and the schedule above meets it.

## Do it by hand first

Take `machines = [0, 0, 11, 5]`. Total 16, target 4. Write down how far each machine is from 4, the excess, and then ask, for each wall between two machines, how many dresses must cross that wall.

```text
machine:      m0   m1   m2   m3
load:          0    0   11    5
excess:       -4   -4   +7   +1
                 |    |    |
wall:           w0   w1   w2
left side
needs (net):    4    8    1
direction:     <-   <-   <-
```

Everything left of wall `w1` (machines m0 and m1) is short by 8 in total. Those 8 dresses can only arrive by crossing `w1`, and a single wall can carry at most one dress per move in a given direction (only m2 can push across it leftward, one dress at a time). So at least 8 moves.

Your hand was keeping a running total: the sum of excesses so far, which is the net number of dresses that must cross the wall right after the current machine. That running prefix sum is the whole data structure.

## The first honest attempt

Treat it as a shortest-path problem over states. A state is the tuple of loads; a move lets each machine independently send left, send right, or do nothing, so there are up to 3^n successor states. Breadth-first search from the input to the balanced state gives the exact answer.

```text
state [0,0,11,5] -> 3^4 = 81 choices per move
       \__ each one a new tuple, most of them
           shuffle dresses back and forth
level 1:  ~dozens of states
level 2:  hundreds ...
level 8:  the first balanced one
```

This is exponential in time and space. The repeated work is that BFS rediscovers, along every path, the same fact: the number of dresses crossing each wall is not a choice. It is fixed by the input. Different schedules only differ in when those crossings happen.

There are also two tempting wrong shortcuts, and each is wrong on a three-machine example.

```text
shortcut A: answer = max |prefix balance|
  [0,3,0]: balances -1, +1, 0 -> 1
  truth: 2 (m1 holds 2 extra, sheds 1 per move)

shortcut B: answer = max(|balance|, |excess|)
  [3,0,3]: |excess| of m1 = 2 -> 2
  truth: 1 (m0 and m2 both feed m1 in one move)
```

Shortcut A forgets that a single machine is also a bottleneck. Shortcut B treats a deficit like a surplus, but a hungry machine can receive from both sides in the same move, while a full machine can only give one dress per move.

## The turning point

**Claim: the answer is the maximum, over all positions, of the absolute prefix balance and of the positive excess of a single machine.**

Two lower bounds, both forced:

1. **Wall bound.** Let `balance_i` be the sum of excesses of machines `0..i`. If it is positive, that many dresses must leave the left block through wall `i`; if negative, that many must enter. Only the two machines touching the wall can move a dress across it, and the net flow per move is at most one in the needed direction. So moves are at least `|balance_i|`.
2. **Source bound.** A machine with excess `e > 0` must end up with `e` fewer dresses, and it can give away at most one per move. So moves are at least `e`. A deficit gives no such bound, because a machine can receive from both neighbours in one move.

The surprising part is that the larger of these bounds is always achievable. Intuitively, nothing else limits the schedule: in each move, every machine that still has outflow pending sends one dress toward a side that still needs it, and every tight wall and every tight source makes progress, so the maximum of all the bounds drops by one per move. The solution file's brute-force BFS checks this against random small inputs.

So the algorithm is one pass with a running balance:

```text
for load in machines:
    excess  = load - target
    balance += excess
    best = max(best, abs(balance), excess)
```

The geometric picture is a curve. Plot `balance` over the walls; its highest peak or deepest valley is the busiest wall. Overlay the excess bars; a single tall positive bar can poke above the curve. The answer is the tallest feature of either plot.

## Watch it work

Example: `machines = [0, 0, 11, 5]`. The solution returns 8.

Frame 1. Check feasibility and compute the target.

```text
load:    0   0  11   5     total 16, n 4
target = 4                 16 % 4 == 0 -> feasible
balance = 0, best = 0
```

Frame 2. Machine 0: excess -4, balance -4.

```text
load:    0   0  11   5
         ^
excess  -4
balance -4  -> |balance| 4
best = max(0, 4, -4) = 4
```

Four dresses must enter m0 across wall w0.

Frame 3. Machine 1: excess -4, balance -8.

```text
load:    0   0  11   5
             ^
excess      -4
balance     -8  -> |balance| 8
best = max(4, 8, -4) = 8
```

Eight dresses must cross w1 leftward: the busiest wall.

Frame 4. Machine 2: excess +7, balance -1.

```text
load:    0   0  11   5
                 ^
excess          +7   (source bound 7)
balance         -1
best = max(8, 1, 7) = 8
```

The big machine needs 7 moves just to shed its own surplus, but the wall still dominates.

Frame 5. Machine 3: excess +1, balance 0.

```text
load:    0   0  11   5
                     ^
excess              +1
balance              0   (books balance)
best = max(8, 0, 1) = 8
```

Frame 6. The picture behind the number.

```text
balance after each machine (walls):
  0 |-----------------------------
 -1 |                  *
 -4 |    *
 -8 |         *  <- deepest: 8
excess bars:  -4  -4  +7  +1
answer = max(8, 7) = 8
```

Across the frames, `best` was always the largest lower bound among the walls and machines seen so far. The final balance returning to 0 is a free sanity check: the total excess is zero once the target is right.

## Why it is correct

Lower bound. For every wall, `|balance_i|` dresses must cross it in net, and at most one net dress crosses per move. For every machine with excess `e`, it ends with `e` fewer dresses and loses at most one per move. Every schedule respects all these bounds, so it needs at least `B = max(all wall bounds, all source bounds)` moves.

Achievability. This is the greedy schedule, and its invariant is: "after `k` moves, every remaining wall bound and every remaining source bound is at most `B - k`." In each move, let every machine with dresses still owed to one side send one dress that way, and when a machine owes dresses to both sides, send toward the side whose wall carries the larger remaining requirement. The careful part of the proof, which the full argument handles case by case, is showing that a wall whose remaining flow equals the current maximum always gets a dress across it that move; the key fact is that the block on the owing side has a positive total excess, so some machine in it is sending, and flows pass through intermediate machines without stalling because a machine can receive and send in the same move. A machine whose excess equals the current maximum is sending by construction. So every tight quantity drops by one, and the maximum drops by exactly one per move. After `B` moves every bound is 0, which means every machine sits at the target.

The two must agree, so the minimum is exactly `B`. The brute-force BFS in the solution file confirms this on every random case up to four machines.

## Cost

Time O(n): one pass, constant work per machine.

Space O(1): `target`, `balance` and `best`. The BFS it replaces is exponential in both.

## Variations you will meet

- **One dress per move, only one machine moves at a time.** The cost becomes the total distance travelled, which is the sum of `|balance_i|` over walls rather than the max. Same prefix sums, `sum` instead of `max`.
- **Distribute Coins in Binary Tree.** The tree version of the "sum of flows" variant: each edge carries `|excess of the subtree below it|` coins, and the answer is the sum over edges, computed by post-order DFS.
- **Circular row, sum-of-distances version.** Walls form a ring, so the flow across one wall is a free variable `x`; every wall's flow becomes `balance_i - x`, and minimising the sum picks `x` as the median of the balances.
- **Deficit can only fill from one side.** Then deficits become a bound too, and you are back to shortcut B; reading which side of the inequality a machine is on is the whole problem.

## What to carry forward

When many things move in parallel, the answer is the worst bottleneck, and each bottleneck is a prefix sum (a wall) or a single item (a source); take the max of all forced lower bounds and argue the schedule meets it. The next problem also maintains a single prefix quantity, the reach of every buildable sum, and asks what to insert when that prefix stalls.
