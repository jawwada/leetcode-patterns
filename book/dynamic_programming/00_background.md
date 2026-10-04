# Dynamic Programming (outside the brief)

*8 problems · Reading time ~24 min*

## Why this chapter exists

A note before anything else: this chapter is carried over from your old repository, and it sits outside your interview brief, which explicitly excludes dynamic programming. It is here for completeness, so the book does not silently drop eight problems you once solved, and because the habit it teaches (name the state, then fill a table) sharpens your thinking about recursion, backtracking and greedy, all of which are in scope. If you are short on time, this is the chapter to skip.

Dynamic programming answers questions of the form "what is the best / how many / is it possible" over an exponential space of choices, when the choices made so far can be summarised by a small key. The eight problems fall into four families:

- **Walk a line, look back one or two cells** (Min Cost Climbing Stairs, House Robber, Decode Ways): the state is a position in an array or string, and each cell depends on its two predecessors, exactly like Fibonacci.
- **Fill an amount with pieces** (Coin Change): the state is a remaining amount; every coin is a possible last step.
- **Track which sums are reachable** (Partition Equal Subset Sum, Target Sum): the state is (how many items processed, running sum); one asks "possible?", the other asks "how many ways?".
- **Compare or scan sequences** (Longest Common Subsequence, Longest Increasing Subsequence): the state is a pair of prefixes, or "subsequence ending here", and the last problem shows how a cleverer structure beats the plain table.

## What it is

Start with the recursion you would write first for Min Cost Climbing Stairs: `f(i)` is the cheapest way from stair `i` to the top, and from stair `i` you may step to `i+1` or `i+2`. So `f(i) = cost[i] + min(f(i+1), f(i+2))`. Draw the calls for six stairs:

```text
                         f(0)
                /                    \
            f(1)                      f(2)*
          /      \                  /      \
      f(2)*       f(3)+         f(3)+      f(4)
     /    \       /    \        /   \      /  \
  f(3)+  f(4)  f(4)   f(5)   f(4) f(5)  f(5) f(6)
   ...    ...   ...    ...    ...  ...   ...

  *  f(2) is solved twice      + f(3) is solved three times
  the whole tree has 41 calls for only 8 distinct i (0..7)
```

The tree is exponential (it grows like Fibonacci, about 1.6^n nodes) but it contains only n+1 different questions. The same subtree, `f(3)` with everything beneath it, is rebuilt from scratch every time it appears. That is the defining smell of DP: **overlapping subproblems**. The second ingredient is **optimal substructure**: the best answer to `f(i)` is built from the best answers to smaller questions, so solving each smaller question once is enough.

### Memoisation: cache the tree

Keep the recursion, add a dictionary. Before computing `f(i)`, look it up; after computing it, store it. Now the second time `f(3)` is requested, the whole subtree collapses to a lookup:

```text
  memo (dict keyed by i)            the tree after caching
  +-----+-------+                          f(0)
  |  i  | f(i)  |                        /      \
  +-----+-------+                    f(1)      [f(2)] hit
  |  6  |   0   |                   /    \
  |  7  |   0   |               f(2)    [f(3)] hit
  |  4  |  ...  |              /    \
  | ... |  ...  |          f(3)    [f(4)] hit
  +-----+-------+          ...
                       each i expands once: n+1 nodes
```

Top-down memoisation is the easiest way to turn a brute force into DP: the code barely changes. The costs are a call stack as deep as the longest chain (Python's default limit is about 1000) and dictionary overhead on every call.

### Tabulation: fill the table in dependency order

Flip the direction. `f(i)` needs `f(i+1)` and `f(i+2)`, so if you compute from the top stair downwards, every dependency is ready when you need it. No recursion, no stack, just a loop over an array:

```text
  index:    0     1     2     3     4     5     6
  table:  [ ? ] [ ? ] [ ? ] [ ? ] [ ? ] [ ? ] [ 0 ]   base
                                       <-- fill this way
  each cell reads the two cells to its right
  (f(6) = f(7) = 0: standing past the last stair)
```

The book's solutions mostly use the mirrored form, "cheapest cost to stand on step i", filled left to right. Same idea: the order of the loop is the topological order of the dependency graph.

### The method: four steps, then a fifth

Every DP in this chapter is designed with the same checklist:

1. **State.** What does one cell mean, in words? "dp[i] = best loot from the first i houses." If you cannot say it in one sentence, the rest will not work.
2. **Recurrence.** How is one cell computed from smaller cells? Almost always by asking "what was the last decision?" (last coin, last house robbed or skipped, last one or two digits).
3. **Base cases.** The cells that need no recurrence: the empty prefix, amount 0, sum 0.
4. **Order.** A loop order in which every cell's inputs are already filled.
5. **Space reduction.** Look at which cells the recurrence actually reads. If it reads only the previous one or two cells, keep two variables; if it reads only the previous row, keep one or two rows.

### 1-D and 2-D tables

```text
 1-D: state = one index                 (stairs, robber, decode,
                                          coin change)
   dp: [d0][d1][d2][d3][d4] ...
              ^   ^   |
              +---+---+  dp[i] reads dp[i-1], dp[i-2]

 2-D: state = two indices               (LCS; subset sums as
                                          item x sum)
            j=0  j=1  j=2  j=3
   i=0    [  0 ][  0 ][  0 ][  0 ]
   i=1    [  0 ][ UL ][ U  ][    ]
   i=2    [  0 ][ L  ][ X  ][    ]    X reads up (U), left (L)
   i=3    [  0 ][    ][    ][    ]    and up-left (UL)
   fill row by row, left to right
```

A 2-D table whose cells read only the row above can be squeezed into one or two rows. That is the space reduction step for LCS and for the subset-sum problems.

## Operations and what they cost

| Operation | Cost | Why |
|---|---|---|
| Brute-force recursion | exponential | every branch re-solves shared subtrees |
| Memoised recursion | states x work per state | each state expands once, rest are lookups |
| Tabulation | states x work per state | one loop iteration per cell |
| Space of full table | number of states | one cell each |
| Rolling variables / rows | width of dependency | keep only what the recurrence reads |
| Reconstructing the choices | O(length of answer) | walk back through the table from the answer cell |

The rule of thumb for cost is always **(number of states) x (transitions per state)**. Coin change: `amount + 1` states, `k` coins each, so O(amount x k). LCS: `(m+1)(n+1)` states, O(1) each.

The non-trivial operation is the rolling update. Here it is for a Fibonacci-style recurrence, keeping two variables `a = dp[i-2]` and `b = dp[i-1]`:

```text
 before step i:     a = dp[i-2]     b = dp[i-1]
 compute:           new = combine(a, b)
 shift:             a <- b          b <- new
 after step i:      a = dp[i-1]     b = dp[i]

   ... [dp[i-2]][dp[i-1]][ new ] ...
          a        b
                  a        b         (window slides right)
```

Python's `a, b = b, combine(a, b)` evaluates the right side first, so the shift is safe in one line.

## The invariant

**When a cell is written, every cell it reads already holds its final, correct value, and the cell itself will never change again.**

That is the whole correctness of tabulation. The loop order is chosen to protect it.

```text
 legal (coin change, a ascending):
   dp: [0][1][2][1][1][?]          computing dp[5]
        ^           ^              reads dp[4], dp[2], dp[1]:
                                   all final already

 illegal (0/1 subset sum, sweeping t UPWARD in one row):
   reach after item 5:   t=5 set (from t=0)
   ...then t=10 reads t=5, which was set in THIS item's pass
   => item 5 used twice: 0 -> 5 -> 10   WRONG for 0/1 items
```

The illegal picture is the most common DP bug: reading a cell that was already overwritten in the current round. Fix it by changing the loop direction or by writing into a fresh row.

## How to picture it

Picture the recursion tree folded into a **directed acyclic graph**: every distinct subproblem is one node, and arrows point to the subproblems it depends on. Memoisation walks that graph depth-first from the top; tabulation sweeps it in topological order from the bottom. Either way each node is visited once.

```text
  recursion tree (exponential)      folded DAG (linear)

          f0                        f0 -> f1 -> f2 -> f3 -> f4
         /  \                        \_____^\____^\____^
       f1    f2                       (each node also skips one)
      / \    / \
    f2  f3  f3  f4
```

For 2-D problems the DAG is a grid, and the answer is a path from one corner to the other (LCS draws it as a staircase of diagonal steps).

### DP versus greedy

Greedy commits to the locally best choice and never looks back. DP is what you need when the best choice now depends on the future. House Robber: robbing the richest house in sight forbids its neighbours, which might sum to more. Coin Change with coins `[1, 3, 4]` and amount 6: greedy takes 4, then 1, then 1 (three coins), but 3 + 3 is two coins. The local choice "take the biggest coin" was fine only for special coin systems. When you can build a small counterexample to the greedy rule, the problem wants DP; when you can prove an exchange argument, greedy is enough and cheaper.

## Advanced patterns

The four-step method gets you through any problem whose state is handed to you. The patterns below are what you need when it is not: when you have to invent the state, choose between near-identical loop orders that count different things, or notice that the table itself is the bottleneck. Each one shows up in this chapter, and each is the main idea of a well-known harder problem outside it.

### 1. State design: remember exactly what the future needs

**When it shows up**: the natural index `i` is not enough because a decision made at `i` restricts what is allowed later (a neighbour you robbed, a stock you hold, a cooldown day). Signs: your recursion wants an extra argument, or the greedy counterexample hinges on "what happened just before".

**The intuition**: a DP state is a summary of the past that is *exactly* as detailed as the future requires. Too coarse, and two pasts with different futures share one cell, so the cell's value is wrong for one of them. Too fine, and you multiply the table for nothing. So ask: "if two different histories end at the same `i`, what must they agree on for their best futures to be identical?" In House Robber the answer is "whether house `i` was robbed", which gives two numbers per index, `rob[i]` and `skip[i]`. The chapter's solution then folds that flag away (it is implied by stepping to `i-2`), which is the opposite move: deleting a component that does not change the answer. Designing a state is doing both, adding what the future depends on and dropping what it does not.

```text
 nums:        2     7     9     3     1
 rob[i]:      2     7    11    10    12
 skip[i]:     0     2     7    11    11

 rob[i]  = skip[i-1] + nums[i]    neighbour must be skipped
 skip[i] = max(rob[i-1], skip[i-1])
 answer  = max(12, 11) = 12       (2 + 9 + 1)
```

Read the table as a two-state machine walking right: each column holds one number per state, and arrows only go from the previous column. Once you see states this way, "Best Time to Buy and Sell Stock with Cooldown" is three states (holding, just sold, resting) and "House Robber III" is the same pair returned from every tree node instead of every index.

**Where you'll use it**: House Robber (the flag, and why it can be dropped), Decode Ways (the state is a prefix length, not a position, which is what makes `dp[0] = 1` meaningful), Longest Increasing Subsequence (the O(n^2) state "LIS that *ends at* `i`" exists because "LIS of the first `i`" cannot tell you whether `nums[i]` extends it). Beyond the chapter: Best Time to Buy and Sell Stock with Cooldown (LC 309).

### 2. The knapsack family: direction and nesting decide what you count

**When it shows up**: items with sizes and a capacity, target or amount: coins, numbers, weights. The questions differ in two switches: may an item be used again, and do different orders of the same items count as different answers?

**The intuition**: in a one-row knapsack, the loop over the sum reads cells that are either from the previous item's pass or already updated in this item's pass. Ascending sweep: you read updated cells, so the current item can be stacked again (unbounded). Descending sweep: you read only old cells, so each item is used at most once (0/1). That is the first switch. The second is which loop is outside. With items outside, every combination is built in one fixed item order (all 1s before any 2s), so `{1, 2}` is counted once. With the amount outside, every cell considers every item as the *last* one, so `1+2` and `2+1` are different paths into the cell and both get counted. Same recurrence, same table size, different question answered.

```text
 coins [1, 2], ways to make amount a     a:  0  1  2  3  4

 items outside (combinations):
   after coin 1                              1  1  1  1  1
   after coin 2                              1  1  2  2  3
   a=4: {1111, 112, 22}                               -> 3

 amount outside (ordered sequences):         1  1  2  3  5
   a=4: 1111 112 121 211 22                           -> 5
```

The two switches give a 2x2 grid worth memorising: 0/1 + combinations (Partition Equal Subset Sum, descending), unbounded + combinations (Coin Change II, items outside, ascending), unbounded + sequences (Combination Sum IV, amount outside). For a *minimum* such as Coin Change, order does not matter at all, since the fewest coins is the same set whichever order you add them, so either nesting works.

**Where you'll use it**: Coin Change (unbounded, ascending), Partition Equal Subset Sum (0/1, the descending trap), Target Sum (0/1 counting, after the subset rewrite). Beyond: Coin Change II (LC 518) versus Combination Sum IV (LC 377).

### 3. Same DAG, different operators: optimise, count, decide

**When it shows up**: the problem asks "minimum", "number of ways" or "is it possible" over the same space of choices. Recognising that these are one computation with different arithmetic saves you designing three DPs.

**The intuition**: every DP in this chapter is a walk over the folded DAG from "How to picture it": a cell combines the cells it has edges from. What changes is how you combine. To optimise, you take `min` over incoming edges and add the edge's cost. To count, you `+` over incoming edges (each path ends with exactly one last edge, so the groups are disjoint and their counts add). To decide, you `or` over incoming edges. The structure, base cases and loop order stay put; only the operators move. The catch is in counting: the "last step" cases must be disjoint and must cover everything, or you double-count. An optimising DP forgives overlapping cases (a `min` taken twice is still the min); a counting DP does not.

```text
 amounts 0..4, edges +1 and +2 (coins [1, 2])

        +1     +1     +1     +1
     0 ---> 1 ---> 2 ---> 3 ---> 4
     |      |      ^      ^      ^
     |      +----- | +2 --+      |
     +----- +2 ----+      |      |
                   +----- +2 ----+

 min coins    (min, +1):   0   1   1   2   2
 # sequences  (+):         1   1   2   3   5
 reachable    (or):        T   T   T   T   T
```

The count row is Fibonacci because the DAG is the stairs DAG. That is not a coincidence: Climbing Stairs, Decode Ways (with gates removing edges) and ordered coin sequences are all path counts on this one picture.

**Where you'll use it**: Min Cost Climbing Stairs and Coin Change (min), Decode Ways and Target Sum (count), Partition Equal Subset Sum (decide). Beyond: Unique Paths (LC 62) is the counting twin of Minimum Path Sum (LC 64) on a grid.

### 4. Sets of reachable values: bitsets, sparse maps and rewrites

**When it shows up**: the state is "which sums (or totals, or balances) can be reached after the first `i` items", the values are integers, and their range is bounded by something like the total sum. Constraints such as `sum(nums) <= 20000` are the tell.

**The intuition**: a layer of a subset DP is really a *set* of reachable sums, and how you store that set is a design choice. A boolean row indexed by sum is the textbook form. A Python big integer whose bit `s` means "sum `s` is reachable" does the whole layer update, "old set united with old set shifted by `x`", in one shift and one or, 64 sums per machine word, and it cannot fall into the reuse trap because the shift reads the old value. When values can be negative or most sums are unreachable, a dictionary from sum to count stores only the live cells and needs no offset. And sometimes algebra shrinks the set before you start: in Target Sum, "assign signs to reach `target`" becomes "pick a subset summing to `(total + target) / 2`", which turns a range of `2 x total + 1` sums into half of `total`.

```text
 nums = [1, 5, 11, 5], target 11; bit s = "sum s reachable"

 sum:     0 1 2 3 4 5 6 7 8 9 10 11
 start    1 . . . . . . . . .  .  .
 +1       1 1 . . . . . . . .  .  .
 +5       1 1 . . . 1 1 . . .  .  .
 +11      1 1 . . . 1 1 . . .  .  1
 +5       1 1 . . . 1 1 . . .  1  1   bit 11 set -> True

 each row = previous | (previous << x)    (bits > 11 dropped)
```

**Where you'll use it**: Partition Equal Subset Sum (bitset), Target Sum (sparse dictionary of counts, and the `P = (total + target) / 2` rewrite). Beyond: Tallest Billboard (LC 956, Hard) keeps a dictionary from height *difference* to best height, the same sparse-map idea with a cleverer key.

### 5. The two-sequence grid, and walking back for the answer

**When it shows up**: two strings or arrays and a question about aligning them: common subsequence, edits, interleaving, matching a pattern. The state is a pair of prefix lengths `(i, j)`.

**The intuition**: any alignment of two sequences is a monotone path through an `(m+1) x (n+1)` grid from the top-left to the bottom-right. A diagonal step pairs `a[i-1]` with `b[j-1]`; a down step skips a character of `a`; a right step skips one of `b`. Every two-sequence problem is "best path through this grid" with different prices on the three kinds of step: LCS pays +1 for a matching diagonal, Edit Distance pays 1 for each skip or mismatched diagonal. The table holds the best score to each cell, and because the answer is a path, you can recover it by starting at the bottom-right corner and asking at each cell which neighbour produced its value. That walk-back is how you return the actual subsequence or the actual edit script, not just its length.

```text
 a = "abcde" (rows), b = "ace" (cols); * = match taken

          ""   a   c   e
     ""    0   0   0   0
     a     0  *1   1   1
     b     0  ^1   1   1
     c     0   1  *2   2
     d     0   1  ^2   2
     e     0   1   2  *3     start here, walk back

 at e/e: match, go up-left; at d/c: up (2) beats left (1);
 at c/c: match; at b/a: up; at a/a: match  -> "ace"
```

The walk-back needs the full table, so it costs O(m x n) space; the one-row squeeze from the LCS problem gives the length only. Hirschberg's trick recovers the path in linear space, but that is past what interviews ask.

**Where you'll use it**: Longest Common Subsequence. Beyond: Edit Distance (LC 72) and Distinct Subsequences (LC 115, Hard: a *counting* walk on the same grid, pattern 3 applied to pattern 5).

### 6. Dominance: replace the table scan with a better structure

**When it shows up**: the recurrence is `dp[i] = best over all j < i that satisfy some condition`, so each cell scans all earlier cells and the DP is O(n^2) with `n` up to 10^5.

**The intuition**: the scan wastes time on candidates that can never win. If candidate A is at least as good as B in value *and* at least as easy to extend, B is dominated and can be thrown away for good. After throwing away every dominated candidate, the survivors usually line up in sorted order, and a sorted structure can be searched in O(log n) instead of scanned. In Longest Increasing Subsequence the candidates for "length `L`" are all runs of length `L`, and the one with the smallest tail dominates the rest. Keep only that one per length and the tails form a strictly increasing array: binary search finds where a new value belongs. The DP table is still there in spirit (the array index is the length), but each cell holds only the undominated candidate.

```text
 nums: 10   9   2   5   3   7  101  18

 O(n^2) table, dp[i] = LIS ending at i:
 dp:    1   1   1   2   2   3   4    4    (each cell scans left)

 tails after each x (smallest tail per length):
   10 -> [10]            3   -> [2, 3]
    9 -> [9]             7   -> [2, 3, 7]
    2 -> [2]            101  -> [2, 3, 7, 101]
    5 -> [2, 5]          18  -> [2, 3, 7, 18]   length 4
```

The same move appears with other structures: a monotonic deque when the condition is "j within the last k" (Constrained Subsequence Sum), a heap when you need the best of a changing set, a Fenwick tree when you need the best over values below `x` with counts attached.

**Where you'll use it**: Longest Increasing Subsequence. Beyond: Russian Doll Envelopes (LC 354, Hard), which is LIS after a sort with a descending tie-break, and Constrained Subsequence Sum (LC 1425, Hard) with a monotonic deque.

## Signals in a problem statement

- "Minimum cost / maximum value / number of ways" over a sequence of choices.
- "How many ways to decode / climb / reach" with choices that overlap (a 1-step and a 2-step move).
- "Can it be partitioned", "is there a subset summing to", "assign + or -": reachable sums.
- Two strings and the words "subsequence", "edit", "common": a 2-D table over prefixes.
- Constraints like `n <= 1000` with `amount <= 10^4`: the product of dimensions is the budget.
- You wrote a backtracking solution and noticed the same `(index, something)` arguments repeat.

Counter-signals:

- "List all" the solutions: the output itself is exponential, so you need backtracking, not DP.
- A provable exchange argument or sorted structure: greedy.
- "Contiguous subarray with sum/condition": prefix sums or a sliding window, usually not DP.
- `n <= 20` with a set-of-items state: bitmask DP, or plain backtracking.

## Python toolbox

Memoisation is one decorator:

```python
from functools import lru_cache   # or functools.cache

@lru_cache(maxsize=None)
def f(i):                 # arguments must be hashable
    if i >= n: return 0
    return cost[i] + min(f(i + 1), f(i + 2))
```

Deep recursion needs `sys.setrecursionlimit`, which is a hint to switch to tabulation. Tables and rolling state:

```python
dp = [0] + [float("inf")] * amount     # 1-D with base case
grid = [[0] * (n + 1) for _ in range(m + 1)]  # NOT [[0]*(n+1)]*(m+1)
a, b = b, min(a, b) + x                # rolling pair, one line
reach |= reach << x                    # big-int bitset of sums
from collections import defaultdict    # sparse sum -> count maps
from bisect import bisect_left         # patience sorting (LIS)
```

## Mistakes people make

1. **Building a 2-D list with `[[0] * n] * m`.** Every row is the same object. Use a comprehension.
2. **Off-by-one between prefix length and index.** `dp[i]` usually means "first i items", so the item is `nums[i-1]`. Write the state sentence down and check it.
3. **Wrong loop direction in a 1-row knapsack.** 0/1 items must sweep the sum downward (or use a fresh row); unbounded items sweep upward.
4. **Missing base case for the empty prefix.** Decode Ways needs `dp[0] = 1`: the empty string has one decoding.
5. **Returning the sentinel.** Coin Change must turn "infinity" into `-1`.
6. **Overwriting a value you still need in a rolling update.** In single-row LCS the up-left value is destroyed; save it in a temporary first.
7. **Trusting greedy without a proof.** Try two or three tiny inputs by hand before committing.
8. **Memo key too small.** If the result depends on `(i, remaining)`, caching on `i` alone returns stale answers.
9. **Memoising mutable arguments.** `lru_cache` cannot hash a list; pass an index or a tuple.

## The journey ahead

The eight problems climb in three stages. The first stage teaches the method on the smallest possible state, a single index. The second changes what the state *is*, from a position to a quantity, and that brings in the knapsack questions of reuse and counting. The third adds a second dimension and then shows the table being beaten.

### Warm-up: one index, look back two

**Min Cost Climbing Stairs.** The puzzle is small enough to solve by hand, which is the point: you can watch the recursion tree blow up on six stairs and then watch it collapse into a row of numbers. The question to ask is where "the top" is (one past the last stair) and why the first two steps are free. It teaches the four steps in their cleanest form and the two-variable roll that every 1-D problem after it reuses.

**House Robber.** Same shape, but now each cell is a decision, and the obvious greedy ("rob the richest house you can") looks plausible: on `[2, 7, 9, 3, 1]` it even finds the optimum, 12. Then `[2, 3, 2]` breaks it (greedy takes 3, the answer is 4), and hunting for that counterexample by hand is the exercise. The new idea is phrasing the decision about the *last* house, where both options are already priced, and noticing that the original memo key had a flag it did not need: your first lesson in state design.

**Decode Ways.** The recurrence looks identical to stairs, but the answer is a count, not a minimum, and zeros turn transitions on and off. The trap is `"06"` and `"30"`: a naive version happily decodes them. The new ideas are counting with disjoint cases, and a base case (`dp[0] = 1` for the empty prefix) that feels arbitrary until you see it is "one way to finish when nothing is left".

### The state becomes a quantity: knapsack

**Coin Change.** Greedy fails again (coins `[1, 3, 4]`, amount 6), but now the state is no longer a position in the input: it is an amount of money, and every coin is a candidate last step. That makes each cell try `k` transitions instead of two, and it makes the problem a shortest path on a number line. It is the first unbounded knapsack and the first time the loop order "ascending amounts" is a topological order you have to justify.

**Partition Equal Subset Sum.** It sounds like a search over all 2^n subsets, and the curious question is why it is not: because you only care which *sums* are reachable, and there are at most `total / 2` of those. Each number may be used once, so the one-row update must sweep downward, and getting it backwards silently turns the problem into Coin Change. Then the row becomes the bits of one integer, and the whole layer update is `reach |= reach << x`.

**Target Sum.** Same layers over sums, but every number is forced in, with a sign, and the question is how many ways. Two new things appear: sums can go negative, which pushes you from an array to a dictionary, and the answer is a count, so booleans become integers. The algebraic rewrite to a subset count is the puzzle's second door; finding it is a good test of whether the previous problem sank in.

### Two sequences, and beating the table

**Longest Common Subsequence.** The first genuinely 2-D state: a pair of prefixes, one from each string. The tension is in the mismatch case, where it is not obvious that dropping one of the last two characters loses nothing; the "crossing lines" argument settles it. It teaches the grid picture behind every alignment problem and the one-row squeeze, with its own version of the overwrite trap (the diagonal).

**Longest Increasing Subsequence.** It looks like a one-sequence problem that should be easy, yet the natural state, "best of the first `i`", does not work, and the one that does, "best ending at `i`", costs O(n^2). The chapter ends by beating its own method: a dominance argument keeps one candidate per length, the survivors are sorted, and binary search does in O(log n) what the table did in O(n). It is the lesson to carry into any DP that feels too slow: look for candidates that can never win.
