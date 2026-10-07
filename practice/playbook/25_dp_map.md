## Dynamic Programming: A Short Map (outside this interview's scope)

> Dynamic programming is brute-force recursion that refuses to solve the same subproblem twice. When a recursion keeps asking the same question with the same arguments, store each answer the first time (top-down memo), or fill a table in an order where every answer you need is already there (bottom-up).

**Why this section is short:** the interview this notebook prepares for excludes DP. This map exists so nothing in `dynamic_programming/` surprises you, and so you can recognise a DP problem and say so out loud.

**In this repo:** `dynamic_programming/` (8 problems)

### State and transition

| Word | What it means | In House Robber |
|---|---|---|
| **State** | the few numbers that say "where am I", such that the best answer from here depends on nothing else | `i`: houses `i, i+1, ...` are still to decide |
| **Transition** | how a state's answer is built from the answers of smaller states | `best(i) = max(best(i + 1), nums[i] + best(i + 2))`: skip house i, or rob it and skip its neighbour |
| **Base case** | the states you answer directly | `best(i) = 0` once `i >= n` |
| **Order** | bottom-up, solve every state before the states that need it | `i` from the right end leftwards (or, over prefixes, left to right) |
| **Answer** | the state that is the original question | `best(0)` |

### Recognising overlapping subproblems

Draw the brute-force recursion and look for repeated calls:

```text
                        best(0)
                 /                 \
            best(1)               best(2)          <- best(2) is solved here...
           /       \              /      \
      best(2)    best(3)      best(3)   best(4)    <- ...and here again; best(3) is already solved twice
```

The call tree grows like Fibonacci, yet it only ever asks n + 2 different questions, `best(0)` to `best(n + 1)` (the memo below counts 22 of them for 20 houses). **Few distinct arguments, many calls** is the signature of DP. Compare backtracking problems such as Subsets or N-Queens, where every path really is different and there is nothing to reuse.

### From backtracking to memo to table

The same recurrence three ways. The memo version is the brute force plus one decorator, which is why `lru_cache` is the bridge from backtracking: write the honest recursion first, then cache it. Only a recursion that **returns** its answer, computed from a few hashable arguments, can be cached. A backtracking search that appends to a shared `path` and records into a global cannot: rewrite it to return a value first.

```python
def rob_brute(nums):
    calls = 0

    def best(i):                              # the most money from houses i, i+1, ...
        nonlocal calls
        calls += 1
        if i >= len(nums):
            return 0
        return max(best(i + 1), nums[i] + best(i + 2))   # skip house i, or rob it and skip i+1

    return best(0), calls


def rob_memo(nums):
    @lru_cache(maxsize=None)                  # the memo: i -> best(i), each computed once
    def best(i):
        if i >= len(nums):
            return 0
        return max(best(i + 1), nums[i] + best(i + 2))

    return best(0), best.cache_info().misses  # misses = distinct states actually computed


def rob_table(nums):
    nxt1 = nxt2 = 0                           # best(i+1), best(i+2): the two answers to the right
    for x in reversed(nums):                  # bottom-up: from the last house leftwards
        nxt1, nxt2 = max(nxt1, x + nxt2), nxt1   # best(i) = max(skip x, rob x on top of best(i+2))
    return nxt1                               # best(0)


houses = [2, 7, 9, 3, 1] * 4                  # 20 houses
print(rob_brute(houses), rob_memo(houses), rob_table(houses))   # (45, 35421) (45, 22) 45
```

**Try it**
- Use `[2, 7, 9, 3, 1] * 5` (25 houses): the brute force makes 392,835 calls (11 times more for 5 more houses), while the memo computes 27 states.
- Split the tuple update in `rob_table` into `nxt1 = max(nxt1, x + nxt2)` and then `nxt2 = nxt1`: `rob_table([2, 7, 9, 3, 1])` returns 22 (every house, neighbours included) instead of 12. `nxt2` must become the *old* `nxt1`.
- The greedy "every other house" fails on `[2, 1, 1, 2]`: both alternating sums are 3, but `rob_table` finds 4 (the first and the last house).

The table version only works if every state is computed **before** it is read. In Coin Change, `dp[a]` reads `dp[a - c]`, a smaller amount, so the amounts go up. DP also arrives disguised as a graph problem: memoized DFS on a grid or a DAG (Longest Increasing Path in a Matrix, 329), or Coin Change as BFS over amounts, where each coin is an edge and the fewest coins is the fewest edges:

```python
def coin_change(coins, amount):
    dp = [0] + [math.inf] * amount               # dp[a] = fewest coins that make exactly a
    for a in range(1, amount + 1):               # small amounts first: every dp[a - c] is final
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)   # try every coin as the LAST coin
    return dp[amount] if dp[amount] != math.inf else -1


def coin_change_bfs(coins, amount):            # the same answer as a shortest path over amounts
    dist, queue = {0: 0}, deque([0])
    while queue:
        a = queue.popleft()
        if a == amount:
            return dist[a]
        for c in coins:
            if a + c <= amount and a + c not in dist:
                dist[a + c] = dist[a] + 1
                queue.append(a + c)
    return -1


print(coin_change([1, 2, 5], 11), coin_change([2], 3), coin_change([1, 3, 4], 6))   # 3 -1 2
print(coin_change_bfs([1, 2, 5], 11), coin_change_bfs([2], 3), coin_change_bfs([1, 3, 4], 6))   # 3 -1 2
```

**Try it**
- Greedy (largest coin first) on `[1, 3, 4]` and 6 takes 4 + 1 + 1, three coins; the table finds 3 + 3, two coins.
- Print `dp` for `coin_change([1, 2, 5], 11)`: `[0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3]`. Each cell is one more than its best neighbour `a - c`.
- Fill the amounts downwards (`range(amount, 0, -1)`): `coin_change([1, 2, 5], 11)` returns -1, because each cell read neighbours that were still `inf`.
- Compare both on random inputs: `all(coin_change(cs, a) == coin_change_bfs(cs, a) for ...)` holds. BFS reaches each amount first by the fewest edges, which is exactly the fewest coins.

### Say it in the interview (if DP shows up anyway)

> "The brute force tries both choices at every house, which is exponential. But the best total from house i onwards depends only on i, so there are just n distinct subproblems. I'll memoize the recursion, or replace it with a loop that keeps just the last two answers: O(n) time, O(1) space."

Point at the repeated call in your recursion tree; that sentence is the whole argument for DP.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Coin Change | `dynamic_programming/coin_change.py` | dp[a] = 1 + min over coins of dp[a − c]; fill amounts upwards (unbounded knapsack) |
| Decode Ways | `dynamic_programming/decode_ways.py` | dp[i] = dp[i−1] if the last digit is 1-9, plus dp[i−2] if the last two form 10-26 |
| House Robber | `dynamic_programming/house_robber.py` | best(i) = max(best(i+1), nums[i] + best(i+2)): skip it or rob it; two rolling values |
| Longest Common Subsequence | `dynamic_programming/longest_common_subsequence.py` | dp[i][j] over two prefixes: a match is the diagonal + 1, else max(up, left) |
| Longest Increasing Subsequence | `dynamic_programming/longest_increasing_subsequence.py` | tails[k] = the smallest tail of any increasing subsequence of length k+1; bisect_left gives O(n log n) |
| Min Cost Climbing Stairs | `dynamic_programming/min_cost_climbing_stairs.py` | dp[i] = min(dp[i−1] + cost[i−1], dp[i−2] + cost[i−2]); the top is index n |
| Partition Equal Subset Sum | `dynamic_programming/partition_equal_subset_sum.py` | can a subset reach total/2? 0/1 knapsack reachability, as a bitset shift per number |
| Target Sum | `dynamic_programming/target_sum.py` | count sign patterns per running sum: counts[s ± x] += counts[s], one layer per number |

### Self-check

1. What makes a problem DP rather than plain backtracking?
<details><summary>Answer</summary>Overlapping subproblems: the recursion's answer depends on a few arguments that take few distinct values, while the call tree revisits them exponentially often. Backtracking problems that list every subset or arrangement have no repeats to reuse, because the output itself is exponential.</details>

2. Why does Coin Change fill `dp` in increasing order of amount?
<details><summary>Answer</summary>Every transition reads <code>dp[a - c]</code>, a smaller amount. Going upwards guarantees those cells are final before <code>dp[a]</code> reads them; going downwards they are still infinity.</details>
