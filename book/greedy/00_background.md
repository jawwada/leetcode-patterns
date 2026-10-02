# Greedy

*14 problems · Reading time ~16 min*

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
pref = list(accumulate(nums))          # pref[i] = sum(nums[:i+1])
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

1. **Maximum subarray**: the purest running-state carry; a negative prefix is dead weight, so drop it.
2. **Maximum product subarray**: the carry must hold two numbers because a negative flips the order.
3. **Jump game**: the reach invariant, where the reachable set is a prefix described by one integer.
4. **Jump game II**: the reach becomes BFS levels, each one an interval, and we count levels.
5. **Taps to water a garden**: turn intervals into jumps, then run Jump Game II with a failure case.
6. **Gas station**: a running sum with restart, plus an argument that skips whole blocks of failed starts.
7. **Partition labels**: each letter is a span; extend a required end and cut when the sweep catches it.
8. **Candy**: constraints from two directions, each settled by its own greedy pass and combined with `max`.
9. **Minimum operations to form an array**: count only the rises; a lower bound that is always achievable.
10. **Super washing machines**: two lower bounds (flow across a boundary, surplus at one machine), take the larger.
11. **Patching array**: a reach over subset sums; when a hole is forced, patch with the hole itself.
12. **Set intersection size at least two**: sort by end and place points as far right as possible, twice.
13. **Couples holding hands**: the greedy "fix the next couch" is optimal because the seating decomposes into cycles.
14. **Stamping the sequence**: greedy fails forwards but works backwards, peeling off the last stamp first.
