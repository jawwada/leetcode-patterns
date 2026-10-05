# IPO

*LeetCode 502 · Hard · Pattern: Sort by threshold + max-heap of unlocked candidates · Reading time ~9 min*

## The problem

You have capital w and may run at most k projects. Project i needs capital[i] <= your current capital to start and
pays profits[i], which is added to your capital when done. Pick at most k distinct projects one after another to
maximise final capital.

```text
Example: k=2, w=0, profits=[1,2,3], capital=[0,1,1] -> 4
  (project 0 lifts w to 1, then project 2 adds 3).
```

## What the problem is really asking

You start with capital `w`. There are `n` projects. Project `i` can only be started if your current capital is at least `capital[i]`, and finishing it adds `profits[i]` to your capital. Starting a project costs nothing, since the capital is a threshold and not a price. You may do at most `k` distinct projects, one after another. Maximise your final capital.

The answer is one number, the capital after choosing an ordered set of at most `k` projects. Two forces pull against each other. Big profits are what you want, but you can only reach some projects after your capital has grown. A small early project may be the key that unlocks a big later one.

```text
k = 3, w = 0
project:   A    B    C    D
capital:   0    1    1    4      (threshold to start)
profit:    1    2    3    5

best: A (w 0->1), C (w 1->4), D (w 4->9)   answer 9
```

## Do it by hand first

Put the projects on a number line by threshold. Your capital is a vertical bar on the same line. Everything to the left of the bar is affordable.

```text
capital axis:
   0         1         2         3         4
   A         B,C                           D
   |
   w=0      only A is left of the bar -> do A (+1)

   0         1         2         3         4
   A         B,C                           D
             |
             w=1   A,B,C unlocked; A used.
                   pick the bigger of B(2), C(3) -> C
```

Doing it by hand, you notice three things. The bar only moves right, because profits are non-negative, so a project once affordable stays affordable. At each turn you pick the biggest profit among the unlocked projects you have not used, since nothing is gained by holding back. And the set of unlocked projects only grows, picking up new projects in threshold order as the bar passes them.

Your hand kept a pile of "unlocked, not yet done" projects and kept pulling the biggest out of it, while a pointer into the threshold-sorted list added newcomers to the pile. The pile is a max-heap, and the pointer is a sort plus an index.

## The first honest attempt

Greedy with a full rescan. Repeat `k` times: scan all `n` projects, find the unused one with `capital <= w` and the largest profit, do it. That is O(k n) time.

A more naive candidate tries every ordered choice of `k` projects, which is exponential. Even the rescan wastes most of its time:

```text
round 1 scans: A B C D   affordable: A          take A
round 2 scans: A B C D   affordable: B C        take C
round 3 scans: A B C D   affordable: B D        take D
               ^ ^
   A, B re-examined every round, though their status
   (affordable or not) cannot change once decided
```

The rescan re-learns, every round, which projects are affordable. But affordability only ever flips from "no" to "yes", and it flips in threshold order. It also re-finds the best affordable profit from scratch, when the candidate set changed only by a few additions and one removal.

## The turning point

**Claim: at every round, doing the most profitable affordable project is optimal, and because capital never decreases, the affordable set only grows, in order of threshold.**

The second half is just "profits are non-negative". The first half is an exchange argument, given in full in the next section. In short, the biggest affordable profit leaves you with the most capital, and more capital never shrinks your future options.

That splits the problem into two small machines:

- **The unlock sweep.** Sort projects by threshold once. Keep an index `i`. Before each round, advance `i` while `projects[i].capital <= w`, pushing each newly affordable profit into the heap. `i` never moves left, so across the whole run each project is pushed once.
- **The choice.** A **max-heap of profits** (negated for `heapq`) of unlocked, unused projects. Pop the top and add it to `w`.

If the heap is empty at the start of a round, nothing is affordable. Since `w` will not grow without doing a project, nothing ever will be, so stop early. This also handles `k` larger than the number of reachable projects.

```text
sorted by capital:  (0,A:1) (1,B:2) (1,C:3) (4,D:5)
                     ----------- i moves right only --->
heap: profits of everything left of i, minus those used
```

## Watch it work

`k = 3`, `w = 0`. Projects sorted by capital are `A(0,1)`, `B(1,2)`, `C(1,3)`, `D(4,5)`, written `name(capital, profit)`. The heap holds profits and is drawn by true value (stored negated).

Frame 1: start. Nothing is unlocked yet.

```text
sorted:  A(0,1)  B(1,2)  C(1,3)  D(4,5)
         ^ i=0
heap: (empty)   array: [ ]        w = 0   rounds left 3
```

Frame 2: round 1 sweep. `A` needs 0 <= 0, so push 1. `B` needs 1 > 0, so stop.

```text
sorted:  A(0,1)  B(1,2)  C(1,3)  D(4,5)
                 ^ i=1
heap:      1     array: [1]       w = 0
```

Pop 1, `w = 1`. Only one choice was possible, but it was the key.

Frame 3: round 2 sweep. `B` (1 <= 1) and `C` (1 <= 1) are unlocked. `D` needs 4, so stop.

```text
sorted:  A(0,1)  B(1,2)  C(1,3)  D(4,5)
                                 ^ i=3
heap:      3
          /
         2       array: [3, 2]    w = 1
```

`C` was pushed after `B` and sifted up past it, because 3 > 2.

Frame 4: round 2 choice. Pop 3, `w = 1 + 3 = 4`. `B` stays in the heap for later.

```text
heap:      2     array: [2]       w = 4   rounds left 1
```

The unused `B` is not discarded. It stays unlocked forever.

Frame 5: round 3 sweep. `D` needs 4 <= 4, so push 5. `i` reaches the end.

```text
sorted:  A(0,1)  B(1,2)  C(1,3)  D(4,5)
                                         ^ i=4 (end)
heap:      5
          /
         2       array: [5, 2]    w = 4
```

Frame 6: round 3 choice. Pop 5, `w = 9`. `k` rounds are used, so return 9.

```text
heap:      2     array: [2]       w = 9   rounds left 0
answer: 9
```

Across the frames, `i` only moved right and every project left of `i` was either in the heap or already done. The heap top was always the best affordable unused profit, and `w` never decreased.

## Why it is correct

**Exchange argument.** Suppose at some round, with capital `w`, greedy picks `p` (largest affordable profit), and some optimal plan instead picks `q` with `profit(q) <= profit(p)`, both affordable at `w`.

- If the optimal plan uses `p` at a later round, swap the two positions. After the swapped step your capital is `w + profit(p) >= w + profit(q)`. At every later step, capital is at least what it was in the original plan, so every later project is still affordable. The final total is the same multiset of profits, so the final capital is unchanged.
- If the optimal plan never uses `p`, replace `q` with `p`. Capital at every later step is greater by `profit(p) - profit(q) >= 0`, so all later projects remain affordable and the final capital does not drop.

Either way, there is an optimal plan that agrees with greedy at this round. Applying the argument round by round turns any optimal plan into the greedy one without losing value.

**The data structures implement greedy exactly.** Invariant before each pop: the heap holds exactly the profits of projects with `capital <= w` that have not been done. The sweep adds every project whose threshold `w` has now reached. Because `w` only grows and the list is sorted, no project left of `i` can ever become unaffordable, and none right of `i` is affordable. Popping removes the one we do.

**Early stop.** An empty heap means no affordable project, so `w` cannot change, and no later round can do anything.

## Cost

- **Time: O(n log n + k log n).** Sorting is O(n log n). Each project is pushed at most once, and there are at most `k` pops, each O(log n).
- **Space: O(n)** for the sorted pairs and the heap.

The rescan brute force was O(k n). The heap version wins whenever `k` is large. When `k` is tiny (say 1), the rescan's O(n) is actually fine, but the heap version is never much worse.

## Variations you will meet

- **Projects cost capital** (you pay `capital[i]` and get back `capital[i] + profit[i]`). If the payout always covers the cost, nothing changes. If it does not, capital can drop, affordability is no longer monotone, and the sweep breaks. That becomes a knapsack-style DP.
- **Maximum Performance of a Team / Course Schedule III.** These use the same shape later in the chapter: sort by one key, sweep, and keep a heap over the second key of what the sweep has admitted. Spot the "two attributes, one is a gate" structure.
- **Minimum Number of Refueling Stops (LeetCode 871).** The mirror image. Fuel is the sweep bar, stations you pass are unlocked into a max-heap, and you pop the biggest only when you are about to run dry. That is "use the best unlocked option lazily" instead of "k times eagerly".
- **Return the chosen projects, not just the capital.** Store `(-profit, index)` in the heap and record indices as you pop.

## What to carry forward

When a threshold quantity only grows, sort candidates by threshold and sweep a pointer, so each one is admitted exactly once. Then a max-heap over the admitted pool answers "best available now", and an exchange argument shows that taking it greedily is safe.

The next problem, Minimum Number of Refueling Stops, keeps this sweep-and-heap machine but delays the choice. You drive as far as your fuel allows, admitting stations into the heap as you pass them, and only pop the biggest when you would otherwise stall.
