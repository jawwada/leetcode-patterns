# Greedy

*14 problems · Reading time ~22 min*

## The chapter

A greedy algorithm commits to the locally best choice at each step and never revisits it. This chapter teaches which
greedy rules survive and how to argue why: running-state carries, reach and frontier arguments, intervals swept in
order, constraints satisfied from both sides, and exchange arguments where any other plan can be rewritten into the
greedy one without getting worse.

Problems, in reading order:

1. [Maximum Subarray](maximum_subarray.md) · Medium
2. [Maximum Product Subarray](maximum_product_subarray.md) · Medium
3. [Jump Game](jump_game.md) · Medium
4. [Jump Game II](jump_game_ii.md) · Medium
5. [Minimum Number of Taps to Open to Water a Garden](minimum_number_of_taps_to_open_to_water_a_garden.md) · Hard
6. [Gas Station](gas_station.md) · Medium
7. [Partition Labels](partition_labels.md) · Medium
8. [Candy](candy.md) · Hard
9. [Minimum Number of Increments on Subarrays to Form a Target Array](min_number_operations.md) · Hard
10. [Super Washing Machines](super_washing_machines.md) · Hard
11. [Patching Array](patching_array.md) · Hard
12. [Set Intersection Size At Least Two](set_intersection_size_at_least_two.md) · Hard
13. [Couples Holding Hands](couples_holding_hands.md) · Hard
14. [Stamping The Sequence](stamping_the_sequence.md) · Hard

## Why this chapter exists

Some optimisation problems look like they need a search over every possible plan, yet the best plan can be built one
decision at a time, never revisiting a choice. A greedy algorithm bets on exactly that: at each step, take the option that
looks best right now, commit, and move on. When the bet is justified you replace an exponential search, or a quadratic DP,
with a single pass and a couple of variables.

The catch is that the bet is usually wrong. Most "obvious" greedy rules fail on some small input, and the whole skill in
this chapter is knowing which rules survive and being able to say why. The fourteen problems fall into a few families:

- **Running-state carry.** Walk left to right carrying one or two numbers that summarise the best thing ending here
  (maximum subarray, maximum product subarray, gas station).
- **Reach and frontier.** The set of things you can already do is a prefix `[0, reach]`; each element pushes the frontier
  out (jump game, jump game II, taps to water a garden, patching array).
- **Intervals swept in order.** Each element owns a span; sweep and cut or place points where spans force you to
  (partition labels, set intersection size at least two).
- **Constraints from both sides.** Each child is bound by a left neighbour and a right neighbour; satisfy each side in its
  own pass, then combine (candy).
- **Count the unavoidable.** The answer is a lower bound you can prove nothing beats, and then show is achievable
  (minimum operations to form an array, super washing machines).
- **Structure hiding under the greedy.** Fixing one couple at a time is optimal because the seating forms cycles
  (couples holding hands); stamping becomes greedy only when you run time backwards (stamping the sequence).

## What it is

Think of any optimisation problem as a tree of decisions. The root is "nothing decided yet". Each level fixes one more
choice. A leaf is a complete plan with a cost. Brute force walks the whole tree. Dynamic programming walks it but merges
identical subtrees. Greedy walks exactly one root-to-leaf path: at each node it picks the child that looks locally best
and never comes back.

```text
                 start
             /     |     \
          c=4     c=3     c=1      <- greedy takes the biggest
         / | \     ...     ...
      c=1 ...                       coins {1,3,4}, amount 6
       |
      c=1   leaf: 4+1+1 = 3 coins   <- greedy's only leaf
                                     optimal leaf: 3+3 = 2 coins
```

That drawing is the reason greedy is "usually wrong". Coin change with denominations `{1, 3, 4}` and amount 6: grabbing the
biggest coin gives `4 + 1 + 1`, three coins, while `3 + 3` uses two. The locally best choice (4) cut off the branch that held
the global best. Nothing in the greedy rule even noticed.

So a greedy algorithm is only half an algorithm. The other half is a proof that the path it walks reaches an optimal leaf.
In interviews and in this chapter, two proof tools do almost all of the work.

**Tool 1: the exchange argument.** Take any optimal solution OPT. Look at the first place it disagrees with what greedy did.
Swap OPT's choice for greedy's choice, and show the cost does not get worse and the plan stays legal. Repeat until OPT
has become greedy's plan. Since every swap kept it optimal, greedy is optimal.

The classic picture is interval scheduling (pick the most non-overlapping meetings; greedy takes the one that ends
earliest). Say OPT starts with meeting `o` and greedy starts with `g`, where `g` ends no later than `o`:

```text
time ->   0    2    4    6    8    10
greedy g  [=====]                       ends at 3
OPT    o  [=========]                   ends at 5
OPT next            [=====]  [====]     start >= 5

swap o -> g:
new OPT   [=====]   [=====]  [====]     g ends at 3 <= 5,
                                        so every later meeting
cost: same count, still legal           still fits
```

Replacing `o` by `g` frees time, never consumes it, so the swapped plan is still feasible and has the same number of
meetings. The cost never rose. That is the whole proof shape: swap, then check "legal and no worse".

**Tool 2: a maintained invariant.** Instead of comparing to OPT, keep one fact true after every step that, at the end,
directly is the answer. The most common in this chapter is a **reach**: "every position in `[0, reach]` is reachable
(or every sum in `[1, reach]` is buildable), and nothing beyond `reach` is yet". If each step preserves that sentence, you
never need to remember how you got there, which is why the whole state shrinks to one integer.

```text
positions:   0  1  2  3  4  5  6  7
reach = 4:  [#  #  #  #  #] .  .  .
             ^ known reachable ^  unknown

the invariant: no holes inside the shaded prefix
```

Two shapes of greedy problem keep appearing, and recognising which one you face tells you what the state is.

**Running-state carry.** The input is already in the order that matters (an array you cannot reorder). You sweep once and
carry a tiny summary: the best sum ending here, the largest and smallest product ending here, the fuel in the tank, the
furthest index reachable. Each new element updates the summary in O(1). The proof is usually an invariant on the carry.

```text
input:   x0   x1   x2   x3   x4  ...
          \    \    \    \    \
carry:   s0 -> s1 -> s2 -> s3 -> s4      s_k = f(s_{k-1}, x_k)
                                        answer read off the s's
```

**Sort then sweep.** The input is a bag (a set of intervals, people, tasks) and you are free to process it in any order.
You pick the order that makes the greedy choice obvious: sort by end, by start, by deadline, by ratio. Then one sweep
decides each item in turn. The proof is usually an exchange argument that justifies the sort key.

```text
bag:     [3,7] [1,3] [8,9] [2,4]
sort by end:
         [1,3] [2,4] [3,7] [8,9]
          --sweep, decide each-->
```

**How to test a greedy quickly.** Before proving anything, try to break it. Write the brute force (all subsets, all
orders, all starts) and compare on every input of size up to about 6 with values in `0..3`. That is a few thousand cases
and runs in under a second. If greedy is wrong, the failing case is tiny and usually tells you why. By hand, the
counterexamples that kill bad greedies have a recognisable look: one big item that blocks two medium ones (the coin
example), a tie broken the wrong way, a negative number that flips which candidate is best, and a short first step that
leaves you stranded. Spend two minutes on these before you spend twenty on a proof.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| Update a running carry | O(1) | one `max`/`min` on a couple of scalars |
| Extend a reach / frontier | O(1) | `reach = max(reach, i + jump)` |
| Full linear sweep | O(n) | each element is decided once, never revisited |
| Sort the bag first | O(n log n) | comparison sort; usually dominates |
| Precompute last occurrence | O(n) | one pass filling a small map |
| Two directional passes | O(n) | left-to-right then right-to-left, combined |
| Bucket by integer key instead of sort | O(n + range) | keys are small integers, so an array replaces the sort |
| Brute-force checker for testing | O(2^n) or O(n!) | only on tiny inputs, never submitted |

The carry update, drawn for the best-sum-ending-here carry of Kadane's algorithm:

```text
carry before: cur = -1        next x = 4
options:      extend: cur + x = 3
              restart:       x = 4    <- bigger
carry after:  cur = 4
```

The reach extension, drawn on `nums = [2, 3, 1]` while standing at index 1:

```text
index:     0   1   2   3   4
nums:      2   3   1
reach=2:  [#   #   #]  .   .
               ^ i=1, i + nums[i] = 4
reach=4:  [#   #   #   #   #]
```

The two-pass combine, drawn on ratings `[1, 3, 2]`:

```text
ratings:   1   3   2
left  ->:  1   2   1      rises from the left
right <-:  1   2   1      rises from the right
max:       1   2   1      satisfies both sides
```

## The invariant

Every correct greedy protects some version of one sentence: **the choices made so far can still be extended to an optimal
solution.** The exchange argument proves it by turning OPT into greedy one swap at a time; the reach invariant proves it
by saying exactly which states are still possible.

For the reach family the sentence becomes concrete: "the reachable set is exactly the prefix `[0, reach]`". A legal state
and an illegal one, on `nums = [3, 2, 1, 0, 4]`:

```text
LEGAL (after scanning i = 0..3):
index:    0  1  2  3  4
nums:     3  2  1  0  4
reach=3: [#  #  #  #] .      prefix, no holes; i=4 > reach
                             -> correctly report "stuck"

ILLEGAL (what a buggy update produces):
index:    0  1  2  3  4
         [#  #  #  #] .
                      ^ code "jumped from" index 4 anyway
reach=8:  ...........#       frontier claims 8, but 4 was
                             never reached: hole at 4
```

The illegal state is the bug of updating the frontier before checking whether you are allowed to stand where you are. Once
a hole sneaks into the prefix, the single integer no longer describes the reachable set, and every later answer is fiction.

For the carry family the sentence is "after index `j`, `cur` equals the best value of anything that ends exactly at `j`".
A legal carry never discards a candidate that could still win; an illegal one (resetting to 0 instead of to `x`, say)
invents an empty subarray the problem never allowed.

## How to picture it

Carry one image: **a frontier moving right that never retreats.** The sweep pointer walks along a number line; behind it,
every decision is final; just ahead, a shaded region shows what the past already makes possible. Greedy is safe exactly
when nothing to the right can ever make you regret something to the left.

```text
decided, frozen     frontier       not yet seen
 ###########|=========>|. . . . . . . . . . . .
            i        reach

regret-free: no later element changes a frozen choice
```

For sort-then-sweep problems, picture the same line, but now the items are bars you laid down in sorted order, and the
exchange argument is literally sliding one bar into another's slot and checking that nothing collides.

## Advanced patterns

The basic material above gets you through the Mediums: carry a summary, extend a reach, sort and sweep. The Hard problems
in this chapter ask for something more. You still make one decision at a time, but you have to know *what quantity* to
make greedy about, and you have to be able to defend the choice in a sentence. The seven patterns below are the ones the
Hard problems lean on. Each builds on the exchange argument and the reach invariant; none of them is a new data
structure.

### Greedy stays ahead

**When it shows up.** You place things one at a time (points, pins, jumps, taps, arrows) and want the fewest, and the
items can be sorted so that every later item ends no earlier than the current one.

**The intuition.** The exchange argument rewrites OPT into greedy one swap at a time. "Stays ahead" is the same idea seen
as a race: pick a measure of progress, and show by induction that after every step greedy's measure is at least OPT's.
If greedy is never behind, it can never need more steps. The art is picking the measure. For covering problems it is
"how far right the covered prefix reaches"; for pin placement it is "how far right my most recent pins sit", because when
intervals are sorted by end, a pin further right lies inside every later interval that a pin further left lies inside,
and possibly more. That dominance fact also tells you the rule: place each new pin as far right as the current interval
allows, at its end. Ties need care, and the measure tells you how to break them (Set Intersection sorts equal ends by
start descending so the narrower interval is handled first).

```text
value:       1   2   3   4   5
[1,3]        [=======]                 sorted: end asc,
[1,4]        [===========]                     start desc
[3,5]                [=======]
[2,5]            [===========]

greedy pins:     *   *       *         {2, 3, 5}
another OPT:     *   *   *             {2, 3, 4}

after [3,5]: greedy's top two (3, 5) >= OPT's (3, 4)
             greedy is ahead, so it never pays more: 3 pins
```

**Where you'll use it.** Set Intersection Size At Least Two (the measure is the two largest pins), Jump Game II and
Minimum Number of Taps (after `k` jumps or taps, greedy's covered prefix is the longest possible). Beyond the chapter:
Minimum Number of Arrows to Burst Balloons (LeetCode 452) is the one-pin version.

### Frontier levels: BFS without a queue

**When it shows up.** "Minimum number of steps / jumps / taps to get from 0 to `n`" on a line, where each position
lets you advance to any point up to some limit.

**The intuition.** Think of it as BFS: level `k` is every index reachable in exactly `k` jumps and no fewer. On a line,
with "jump up to `nums[i]`", the set reachable within `k` jumps is a prefix `[0, end_k]`, so each BFS level is an
*interval* `(end_{k-1}, end_k]`. You never need a queue. Scan `i` left to right, keep `farthest = max(i + nums[i])` over
the current level, and when `i` reaches `cur_end` the level is complete: count a jump and set `cur_end = farthest`. If at
that moment `farthest <= i`, the next level is empty and the goal is unreachable. Interval-covering problems reduce to
this by bucketing: for each left end `l`, store the furthest right end of any interval starting there, and that array is
a jump array, built in O(n) with no sort.

```text
nums = [2, 3, 1, 1, 4]
index:     0    1    2    3    4
           |----|----|----|----|
level 0:  [0]                        cur_end = 0
level 1:       [1 ...2]              from 0: farthest = 2
level 2:                 [3 ...4]    from 1: farthest = 4
                                     goal 4 in level 2: 2 jumps

taps n=6, ranges=[1,2,0,1,0,2,0] bucketed by left end:
left end l:   0  1  2  3  4  5  6
reach[l]:     3  0  4  6  4  0  6    -> 2 taps (1 then 5)
```

**Where you'll use it.** Jump Game II (the pattern in its pure form) and Minimum Number of Taps to Open to Water a
Garden (bucket taps into a reach array, then add the impossibility check). Beyond the chapter: Video Stitching (LeetCode
1024) is the same reduction with clips instead of taps.

### Reach over sums: patch with the hole

**When it shows up.** "Every value in `[1, n]` must be formable as a sum of some elements", "fewest numbers to add",
with a sorted input.

**The intuition.** The Jump Game reach returns, but now it is a reach over subset sums: "every value in `[1, reach]` can
be built, and `reach + 1` cannot yet". Adding a number `x <= reach + 1` glues the old bar to a copy shifted by `x`, so the
bar becomes `[1, reach + x]` with no hole. If the next number is bigger than `reach + 1`, then `reach + 1` can never be
built from the array, so something must be added; any useful patch must be at most `reach + 1`, and the biggest such
patch, `reach + 1` itself, buys the longest bar: `[1, 2 * reach + 1]`. A longer bar is never worse in the future (it
accepts every element a shorter one accepts), which is the monotonicity fact that makes the choice safe. Because each
patch more than doubles the bar, the patch count is at most about `log2 n`.

```text
nums = [1, 5, 10], n = 20
next x   test x <= reach+1   action      reach
  -             -            start         0
  1        1 <= 1   yes      take 1        1
  5        5 <= 2   no       patch 2       3
  5        5 <= 4   no       patch 4       7
  5        5 <= 8   yes      take 5       12
 10       10 <= 13  yes      take 10      22 >= 20 done
patches: 2
```

**Where you'll use it.** Patching Array. Beyond the chapter: Maximum Number of Consecutive Values You Can Make (LeetCode
1798) is the same bar with no patches allowed.

### Count the forced work: lower bounds that are achievable

**When it shows up.** "Minimum number of operations" where one operation moves one unit to a neighbour, or raises a
contiguous range by one, and the answer is a single number rather than a plan.

**The intuition.** Simulating the operations is hopeless; counting what they *must* do is easy. Find a quantity that one
operation can change by at most 1 and that has to change by a known total; that total is a lower bound. For range
increments, look at differences between neighbours: one operation raises exactly one difference by 1, so the sum of the
rises is a lower bound. For moving dresses between washing machines, look at a wall between machines: the prefix
balance (surplus to the left of the wall) must cross it, at most one per move; and a machine with surplus `e` can only
shed one per move. Then the second half: show the bound is achievable, usually by an explicit construction (stack bricks
layer by layer; let every machine with a debt send one dress per move). Gas Station reads the same prefix-balance curve:
the start is just after its lowest point, because every start inside a failed block fails no later than the block did.

```text
range increments, target = [3, 1, 1, 2]
height 3   [#]                  rises: 3, -, -, +1
height 2   [#]       [#]        answer = 3 + 1 = 4
height 1   [#  #  #  #]         one stroke per brick row
index       0  1  2  3

washing machines [1, 0, 5], target 2 each
machine:      1     0     5
excess:      -1    -2    +3
wall:            w0    w1
balance:         -1    -3     3 dresses must cross w1
bound = max(|-1|, |-3|, source +3) = 3 moves
```

**Where you'll use it.** Minimum Number of Increments on Subarrays to Form a Target Array, Super Washing Machines, and in
a gentler form Gas Station. Beyond the chapter: Distribute Coins in Binary Tree (LeetCode 979) counts flow across every
tree edge the same way.

### Settle each direction separately, then combine with max

**When it shows up.** Each element is constrained by both neighbours ("more than a neighbour with a higher rating"), and
a single left-to-right pass keeps getting fixed up after the fact.

**The intuition.** Split the constraints into two families: those that point left and those that point right. Each
family is a set of chains running in one direction, so one pass in that direction settles it minimally: the value at `i`
must be at least the length of the chain ending at `i`. That makes `L[i]` and `R[i]` lower bounds on *any* valid answer,
so `max(L[i], R[i])` is a lower bound too. The remaining check is that taking the max at one element never breaks a rule
at its neighbour, and it does not, because raising a value can only help the rule where that value is supposed to be the
larger one. The answer is the upper envelope of two staircases.

```text
ratings:  1  2  5  4  3  1
L  ->  :  1  2  3  1  1  1     rising run ending here
R  <-  :  1  1  4  3  2  1     falling run starting here
max    :  1  2  4  3  2  1     total 13
                ^ the peak needs 4: its right slope wins
```

**Where you'll use it.** Candy. Beyond the chapter: Trapping Rain Water (LeetCode 42) combines a left-max pass and a
right-max pass with `min` instead of `max`.

### Run time backwards

**When it shows up.** Operations overwrite earlier ones (stamps, paint, layers), so the forward question "which choice
will survive?" needs foresight you do not have.

**The intuition.** Forward, an early press can be hidden later, so you cannot tell whether it was a good idea. Backward,
the *last* press is fully visible in the target: it is a window that matches the stamp exactly. Peel it, turn its letters
into wildcards, and look again. Peeling only adds wildcards, and a wildcard matches anything, so every window that matched
before still matches after. The set of options only grows, which means there is no order to regret, and greedy "peel any
matching window" is safe. Reversing time turned a choice with hidden consequences into one with monotone, visible
consequences.

```text
stamp "abc", target "ababc"
backward:
  a b a b c     window at 2 is "abc"  -> peel
  a b ? ? ?     window at 0 is "ab?"  -> peel (? = any)
  ? ? ? ? ?     all erased, peel order [2, 0]
forward = reverse: press 0 -> "abc??", press 2 -> "ababc"
```

**Where you'll use it.** Stamping the Sequence. Beyond the chapter: Broken Calculator (LeetCode 991) is greedy only
when you walk from the target back to the start.

### Find the cycles under the swaps

**When it shows up.** "Minimum number of swaps" to fix an arrangement where every item has exactly one right place or
one right partner.

**The intuition.** Draw a graph whose nodes are the things that must be fixed (couples) and whose edges are the slots
(couches) joining them. Every node has degree exactly 2, so the graph is a set of disjoint cycles. A swap can raise the
number of cycles by at most one, and the solved state has one cycle per couple, so you need at least `n - cycles` swaps.
The greedy swap "bring this person's partner over" always splits one couple off its cycle, raising the count by exactly
one, so it meets the bound no matter which couch you fix first. The greedy is not clever; the structure makes every
reasonable move optimal. Union-find counts the cycles without tracing them.

```text
row:      [0 2 | 3 4 | 5 6 | 7 1]
couples:   0 1   1 2   2 3   3 0      couple of p is p // 2
couch:      A     B     C     D

graph:   c0 ---A--- c1 ---B--- c2
          |                     |
          +---D--- c3 ---C------+

1 cycle of 4 couples -> 4 - 1 = 3 swaps
```

**Where you'll use it.** Couples Holding Hands. Beyond the chapter: Minimum Number of Operations to Sort a Binary Tree by
Level (LeetCode 2471) uses the same "swaps = length minus cycles" count on a permutation.

## Signals in a problem statement

- "Maximum/minimum sum or product of a **contiguous** subarray" with one pass expected: running-state carry.
- "Can you reach the end", "**minimum number of jumps / taps / patches** to cover `[0, n]`": reach and frontier.
- "Every value in `[1, n]` must be formable": a reach over sums.
- "Starting point on a **circle**", "complete the loop": running sum with restart.
- "Each letter/item may appear in at most one part", "as many parts as possible": spans and last occurrences.
- "Each child must get more than a neighbour with a higher rating": two passes.
- "Minimum number of operations" where an operation affects a contiguous range by one: count rises or flows across
  boundaries.
- Intervals plus "smallest set of points hitting every interval": sort by end, place points as far right as possible.
- `n` up to `10^5` and an O(n^2) DP is the obvious solution: suspect a greedy hiding in the DP.

Counter-signals:

- "Count the number of ways": greedy picks one plan, it cannot count plans. Use DP.
- Arbitrary coin denominations, knapsack weights, "choose a subset with total exactly k": greedy fails, use DP.
- Small `n` (`<= 20`) with "return all": backtracking.
- If two minutes of hand-made counterexamples break your rule, stop proving and switch technique.

## Python toolbox

Sorting with a key, including a tie-break that reverses one field:

```python
iv.sort(key=lambda p: (p[1], -p[0]))  # end asc, start desc
```

Running carries with multiple assignment (both right sides use the OLD values):

```python
hi, lo = max(x, hi * x, lo * x), min(x, hi * x, lo * x)
```

Last occurrence of each element in one comprehension (later indices overwrite earlier):

```python
last = {c: i for i, c in enumerate(s)}
```

Prefix sums and the two-pass pattern:

```python
from itertools import accumulate
pref = list(accumulate(nums))  # pref[i] = sum(nums[:i+1])
left = [1] * n
for i in range(1, n):
    if r[i] > r[i - 1]:
        left[i] = left[i - 1] + 1
```

A brute-force checker for testing a greedy on tiny inputs:

```python
from itertools import product
for arr in product(range(4), repeat=5):
    assert greedy(list(arr)) == brute(list(arr)), arr
```

## Mistakes people make

- **Trusting a greedy rule because it worked on the sample.** Fix: run it against a brute force on all tiny inputs first.
- **Initialising a best-so-far to 0.** All-negative input then returns 0, an empty answer. Fix: start from `nums[0]`.
- **Resetting a carry to 0 instead of to the current element.** Same bug in disguise. Fix: `cur = max(x, cur + x)`.
- **Updating `hi` before computing `lo` from it.** Fix: compute both from the old pair in one tuple assignment.
- **Extending reach before checking `i > reach`.** You jump from an index you never reached. Fix: check, then extend.
- **Looping to the last index in a jump-count scan.** It counts one jump too many when you land exactly on the end. Fix:
  iterate `range(n - 1)`.
- **Sorting by the wrong key or breaking ties the wrong way.** Fix: write the exchange argument; it tells you the key.
- **Restarting at `i` instead of `i + 1`.** The station that broke the tank cannot be the start. Fix: `start = i + 1`.
- **Forgetting the impossibility case.** Return `-1` when no tap passes the dry point or total fuel is negative.
- **Negative indices wrapping silently in Python.** `reach[i - r]` with `i - r < 0` writes to the end. Fix: clamp at 0.

## The journey ahead

The order runs from one-variable carries to problems where the greedy is the last, smallest step after you have found
the real structure. Each problem reuses something from the one before it and adds one idea.

### Warm-up: carry one running state

**Maximum Subarray.** The naive version tries every start and end, O(n^2). The puzzle is what you can forget: a prefix
whose sum is negative can only drag down anything that extends it, so you drop it and restart. This is the purest
running-state carry, one number per index, and the place to learn the "start from `nums[0]`, not 0" discipline.

**Maximum Product Subarray.** Copy Kadane, replace `+` with `*`, and a single negative number breaks it: the smallest
product so far becomes the largest the moment you multiply by a negative. The new idea is that the carry must be wide
enough to survive the worst case, so it holds two numbers, the max and the min ending here, updated together.

### The reach: one integer describes a prefix

**Jump Game.** It looks like a graph search over jumps, and a DFS would work, but the reachable set has no holes: it is
always a prefix `[0, reach]`. That one observation shrinks the whole search to an integer and introduces the reach
invariant the rest of the chapter keeps returning to.

**Jump Game II.** Now count the fewest jumps. A greedy "jump as far as you can" fails; the honest way is BFS, and the
surprise is that every BFS level is an interval of indices. The new idea is closing a level when the scan reaches its
end, so BFS runs with two integers and no queue.

**Minimum Number of Taps to Open to Water a Garden.** The input is a bag of intervals, which seems to demand a sort.
Bucketing each tap by its left end turns the bag into a jump array, and the problem becomes Jump Game II with a new
failure mode: a level that cannot get past its own end means part of the garden stays dry forever.

### Sweeps with a budget or a span

**Gas Station.** The brute force tries every start and drives around, O(n^2). The new idea is discarding starts in
whole blocks: if the tank runs dry at station `i` starting from `s`, every start between `s` and `i` fails too, so the
next candidate is `i + 1`. Paired with "total gas >= total cost", one pass with a running sum decides it.

**Partition Labels.** Cut a string into as many pieces as possible with each letter in one piece. Each letter becomes a
span from its first to last occurrence, and the sweep keeps a required end that grows whenever a letter inside the
current piece reaches further. The cut happens exactly when the scan catches up with that end, the reach idea applied to
overlapping spans.

### Lower bounds you can prove, then reach

**Candy.** Every child is constrained by both neighbours, and a single pass keeps having to go back and fix earlier
children. The new idea is splitting the rules by direction: one pass settles the left rules, one settles the right, and
the per-child `max` satisfies both without breaking either.

**Minimum Number of Increments on Subarrays to Form a Target Array.** Simulating range increments looks expensive and
ambiguous. Looking at differences between neighbours shows that one operation can create at most one unit of rise, so
the answer is the first height plus the sum of rises. This is the first problem where the answer is a lower bound you
prove first and then show is achievable.

**Super Washing Machines.** The same lower-bound habit, with two bounds instead of one: the net dresses that must cross
each wall (a prefix balance, as in Gas Station) and the surplus a single machine must shed one at a time. The puzzle is
why the larger bound is always achievable, and the answer is that every tight bound makes progress on every move.

### The Hard end: the structure under the greedy

**Patching Array.** The reach from Jump Game returns, now over subset sums. When a gap is forced, which number should you
add? The hole itself, `reach + 1`, because it is the largest patch that closes the gap and so buys the longest bar. The
new idea is an exchange argument backed by monotonicity: a longer bar is never worse later.

**Set Intersection Size At Least Two.** Pins must hit every interval twice. Sorting by end and placing pins as far right
as possible is the classic one-pin greedy; the new difficulties are carrying the two largest pins as state, and a tie
rule (start descending) without which the greedy double-counts. The proof is greedy stays ahead.

**Couples Holding Hands.** A greedy "fix each couch by fetching the partner" looks too simple to be optimal, and a
curious person asks whether the order of fixes matters. It does not, because the seating is a union of cycles and every
greedy swap splits off exactly one couple. The new idea is that the proof lives in a graph you build, and union-find
counts it.

**Stamping the Sequence.** Forward, every stamp may be partly hidden by later ones, and no local rule can tell which
press to make first. Backward, the last press is visible and peeling it only creates wildcards, so options never shrink.
The chapter ends on its most general lesson: if a greedy needs foresight in one direction, try the other.
