# Dynamic Programming (outside the brief)

*8 problems · Reading time ~14 min*

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

1. **Min Cost Climbing Stairs**: the cleanest Fibonacci-shaped table; learn the four steps and the two-variable roll.
2. **House Robber**: the same shape, but each cell is a decision (rob or skip) and greedy visibly fails.
3. **Decode Ways**: counting instead of optimising, with validity guards that switch transitions on and off.
4. **Coin Change**: the state becomes an amount and each cell tries every coin as the last step (unbounded knapsack).
5. **Partition Equal Subset Sum**: each item usable once (0/1 knapsack), a yes/no table over sums, and the bitset trick.
6. **Target Sum**: the same layered sums, but counting ways and allowing negative sums with a dictionary.
7. **Longest Common Subsequence**: the first true 2-D table, over two prefixes, with a one-row squeeze.
8. **Longest Increasing Subsequence**: an O(n^2) DP that patience sorting beats with a smarter structure in O(n log n).
