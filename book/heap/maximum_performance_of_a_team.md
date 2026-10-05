# Maximum Performance of a Team

*LeetCode 1383 · Hard · Pattern: Sort by the bottleneck (efficiency desc) + min-heap of the top-k other values · Reading time ~11 min*

## The problem

n engineers have speed[i] and efficiency[i]. Choose at most k of them; a team's performance is (sum of speeds) *
(minimum efficiency). Return the maximum performance modulo 1e9+7.

```text
Example: speed=[2,10,3,1,5,8], efficiency=[5,4,3,9,7,2], k=2 ->
  60 (engineers 1 and 4: speeds 10+5=15, min efficiency 4).
```

## What the problem is really asking

You have `n` engineers. Engineer `i` has a `speed` and an `efficiency`. Pick a team of *at most* `k` of them. The team's performance is `(sum of the team's speeds) × (smallest efficiency on the team)`. Return the best performance, modulo `10^9 + 7`.

The answer is a number, but you are choosing a subset. The difficulty is that the two factors pull against each other. Adding a fast engineer raises the sum, but if they are inefficient they drag the minimum down, and the minimum multiplies *everyone's* speed. One weak link taxes the whole team.

Our example, with letters for engineers:

```text
 engineer     A    B    C    D    E    F
 speed        2   10    3    1    5    8
 efficiency   5    4    3    9    7    2        k = 2

 best team {B, E}: speeds 10 + 5 = 15, min eff = 4
 performance = 15 × 4 = 60
```

## Do it by hand first

Try to reason it out like a person. B is the fastest (10), but with efficiency 4, every team with B is multiplied by at most 4. D is the most efficient (9), but painfully slow.

A natural question to ask yourself: "If I insist the weakest link has efficiency *at least* 4, who am I allowed to hire?" Everyone with efficiency >= 4: D, E, A, B. Among them, take the two fastest: B (10) and E (5). Sum 15, times 4 is 60.

Ask the same question for each possible weakest link:

```text
 weakest link  eligible (eff >= link)     2 fastest   score
 D (eff 9)     D                          D            1×9 =  9
 E (eff 7)     D E                        E D          6×7 = 42
 A (eff 5)     D E A                      E A          7×5 = 35
 B (eff 4)     D E A B                    B E         15×4 = 60
 C (eff 3)     D E A B C                  B E         15×3 = 45
 F (eff 2)     D E A B C F                B F         18×2 = 36
```

The best row is 60. Two things your hand did: it walked through engineers from most efficient to least, so the eligible pool only ever *grew*; and in each row it kept "the k fastest people in the pool". The pool grows by one each row, and you only need its top `k` speeds. That is a size-`k` heap.

## The first honest attempt

Enumerate every team of size 1 to `k`, compute sum times min, keep the best. That is `C(n,1) + ... + C(n,k)` teams, exponential in `k`, and each costs `O(k)` to score.

The repeated work: the score of a team is governed by one person, the bottleneck. Many different teams share the same bottleneck, and for a fixed bottleneck the brute force tries every combination of teammates even though the right answer is obvious, namely the fastest eligible ones.

```text
 teams whose bottleneck is B (eff 4), k = 2:
   {B}     10×4 = 40
   {B,A}   12×4 = 48
   {B,D}   11×4 = 44
   {B,E}   15×4 = 60   <- the only one that matters
 each rebuilt from scratch, for every bottleneck
```

A better attempt: for each engineer as bottleneck, collect everyone at least as efficient, sort them by speed, and take the top `k - 1` plus the bottleneck. That is `n` candidates, each `O(n log n)`: `O(n^2 log n)`. Still wasteful: the eligible pool for consecutive bottlenecks differs by one person, yet we re-sort it every time.

## The turning point

**Claim: if you fix who the bottleneck is, the rest of the team is forced: the fastest engineers who are at least as efficient. So sweep the bottleneck from most efficient to least, and keep the top-`k` speeds of the growing pool in a min-heap.**

Justify each part.

*Fix the bottleneck.* Once you declare "the minimum efficiency is `e`", the multiplier is a constant, and the only thing left to maximise is the speed sum. Anyone with efficiency `>= e` can join without changing the multiplier. So take the fastest.

*Sweep in decreasing efficiency.* Sort engineers by efficiency, highest first. Standing on engineer `x`, everyone you have already passed has efficiency `>= x`'s. So "the eligible pool for bottleneck `x`" is simply "everyone visited so far". The pool grows by exactly one per step.

*Top `k` of a growing pool is a min-heap of size `k`.* This is the trick from Kth Largest Element in a Stream, the first problem in this chapter. Push each new speed; if the heap has more than `k` items, pop the smallest. The heap's root is the weakest kept speed, the one to evict next. Keep a running `total` of the heap's contents so the sum costs nothing to read.

*Score every step as `total × eff(x)`.* There is one subtlety. Sometimes `x`'s own speed is the one just evicted, so the heap's team does not contain `x`. Then `eff(x)` is not really that team's minimum; the team's true minimum is higher. That means the score we compute is *at most* that team's true performance. We never overestimate. And the team's true score was (or will be) counted exactly at its real bottleneck. So computing a slightly pessimistic score here is harmless.

Also note "at most `k`": the heap holds fewer than `k` speeds in the early steps, and those smaller teams are scored too. Nothing special is needed.

One trap: take the modulo only at the very end. The modulo destroys ordering, so comparing reduced values would pick the wrong team.

## Watch it work

Sorted by efficiency, descending: D(9,1), E(7,5), A(5,2), B(4,10), C(3,3), F(2,8). Notation: `name(eff, speed)`. The heap is a min-heap of speeds, smallest first; `k = 2`.

Frame 1: Visit D(9,1).

```text
 pool   D
 push 1           heap [1]          total 1
 score 1 × 9 = 9                    best 9
```

A team of one is allowed, so it is scored.

Frame 2: Visit E(7,5).

```text
 pool   D E
 push 5           heap [1, 5]       total 6
 score 6 × 7 = 42                   best 42
```

The heap is now full at size `k = 2`.

Frame 3: Visit A(5,2). Overflow: evict the slowest.

```text
 pool   D E A
 push 2           heap [1, 2, 5]    total 8
 pop 1            heap [2, 5]       total 7
 score 7 × 5 = 35                   best 42
```

D leaves the team; the multiplier dropped to 5, so this row loses to Frame 2.

Frame 4: Visit B(4,10).

```text
 pool   D E A B
 push 10          heap [2, 5, 10]   total 17
        2         <- root: slowest kept speed
       / \
      5   10      array [2, 5, 10]
 pop 2            heap [5, 10]      total 15
 score 15 × 4 = 60                  best 60
```

The heap holds E and B: the optimal team, scored at its true bottleneck.

Frame 5: Visit C(3,3). C itself is the slowest and is evicted at once.

```text
 pool   D E A B C
 push 3           heap [3, 5, 10]   total 18
 pop 3            heap [5, 10]      total 15
 score 15 × 3 = 45                  best 60
```

This is the pessimistic case: the team {E, B} is scored with C's efficiency 3, below its real 60.

Frame 6: Visit F(2,8).

```text
 pool   D E A B C F
 push 8           heap [5, 8, 10]   total 23
 pop 5            heap [8, 10]      total 18
 score 18 × 2 = 36                  best 60
```

The answer is 60.

Across frames: the heap always held the `k` largest speeds among the visited engineers, `total` always equalled the heap's sum, and the current efficiency was always `<=` the efficiency of everyone in the heap.

## Why it is correct

**Never overestimating.** At every step the heap's members were all visited, so all have efficiency `>= eff(x)`. Their real performance is `total × (their true minimum) >= total × eff(x)`. So every score we record is achieved by a real team of size at most `k`, and `best` is never larger than the true optimum.

**Reaching the optimum: the exchange argument.** Let `T*` be an optimal team. Among its members, let `b` be the one the sweep visits *last*. Because the sweep goes in decreasing efficiency, `b`'s efficiency is the minimum of `T*`, and every member of `T*` has been visited by the time we stand on `b`.

At that moment the heap holds the `k` fastest visited engineers. Compare `T*` with the heap. If `T*` contains someone `y` who is not in the heap, then the heap has `k` people, all at least as fast as `y`, and at most `k - 1` of them are in `T*`, so some heap member `z` is not in `T*`, with `speed(z) >= speed(y)`. Swap `y` out and `z` in. The speed sum does not drop, and since `z` was visited before or at `b`, `eff(z) >= eff(b)`, so the multiplier does not drop either. Repeat until the team's members are all in the heap. If the team is still smaller than the heap, adding the remaining heap members only adds speed without lowering the multiplier below `eff(b)`. So `total × eff(b)` at that step is at least `performance(T*)`. The algorithm scores exactly the left side at that step. Combined with "never overestimating", `best` equals the optimum.

## Cost

- **Time `O(n log n)`.** The sort is `O(n log n)`; each engineer does one push and at most one pop on a heap of size at most `k + 1`, so `O(n log k)` for the sweep.
- **Space `O(n + k)`.** The sorted pairs take `O(n)`; the heap itself takes `O(k)`.

The intermediate "re-sort the pool per bottleneck" version is `O(n^2 log n)`; brute force is exponential in `k`.

## Variations you will meet

- **Exactly `k` members instead of at most `k`.** Only score a step when the heap is full. Everything else stays.
- **Maximum Subsequence Score (LeetCode 2542).** Two arrays, pick exactly `k` indices, score is `sum(nums1) × min(nums2)`. It is the same problem with different names: sort by `nums2` descending, min-heap of `nums1`.
- **Minimum Cost to Hire K Workers (LeetCode 857).** The bottleneck is a wage-to-quality *ratio*, and you want the smallest total quality. Sort by ratio ascending, keep the `k` smallest qualities in a *max*-heap. The roles of "evict the weakest" flip because you are minimising.
- **The multiplier is a sum, not a min.** Then there is no bottleneck to fix and the sweep breaks; you need DP or a different decomposition.

## What to carry forward

When a score is "sum × min", decide the min first: sweep it in sorted order so the eligible pool only grows, and keep the best `k` of the pool in a capped heap. The next problem, Minimize Deviation in Array, also fixes the bottleneck first, but there the heap's root is the only element whose move can improve the answer, and we move it again and again.
