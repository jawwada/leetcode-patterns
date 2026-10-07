## From Idea to Code

> An idea is one sentence. Code is a handful of decisions. Make the decisions first, in plain words, and typing becomes translation.

### Why you freeze

"I'll use a sliding window" sounds like a plan, but it leaves seven questions open: what do I store, what exactly does each variable mean, what must stay true, how does one new item change things, when do I write down the answer, what are the starting values, and what do I return if nothing works. If you try to answer all seven *while typing*, your working memory overflows and you freeze or write a bug.

The fix is to **separate deciding from typing**. Answer the seven questions first (out loud and as comments), then translate each answer into its line. Every section of this notebook fills in these seven decisions for its technique.

### The seven decisions

| # | Decision | Ask yourself | Typical answers |
|---|---|---|---|
| 1 | **State** | "If I stop after item *i*, what must I remember about items 0..i to carry on?" | a dict of counts, a best-so-far, a pointer, a stack of unresolved items, a visited set, a heap of candidates |
| 2 | **Definition** | "What exactly does each variable mean?" Write it as a comment. | `seen[v] = index of an earlier v`, `stack = indices of days still waiting`, `dist[u] = shortest distance found so far` |
| 3 | **Invariant** | "What is true every time the loop comes round?" | "the window has no repeats", "stack temperatures never increase", "the answer lies in [lo, hi]" |
| 4 | **Step** | "How does ONE new item / node / edge change the state?" | add it, then restore the invariant (pop, shrink, relax, union) |
| 5 | **Record** | "On which line do I *know* a piece of the answer?" | after the invariant is restored, at the moment of a pop, when the target is reached |
| 6 | **Init** | "What are the values before anything is processed?" | empty, 0, `math.inf`, a sentinel, a dummy node, the start node already in the queue |
| 7 | **Return** | "What comes back, including when nothing was found?" | `best`, `-1`, `[]`, `""`, translate `inf` |

Almost every interview solution has the same shape, so each decision lands in a predictable place. The tags in this notebook's code (`# STATE`, `# STEP`, `# FIX`, `# RECORD`, ...) point at exactly these lines:

```text
def solve(data):
    # INIT       the state before any item; its DEFINITION as a comment on this line
    for item in data:            # or: while queue / for child in children
        # STEP       fold the item into the state
        # FIX        while <invariant broken>: repair (pop / shrink / relax / union)
        # INVARIANT  true here every time (say it; assert it while practising)
        # RECORD     update the answer at the moment it is known
    # RETURN     the answer, translating "not found"
```

The **order** of STEP, FIX and RECORD is itself a decision: Two Sum records *before* its step, a shortest window records *inside* its fix, a next-greater stack records at each pop. In recursion the shape turns on its side: INIT is the base case, the "items" are the children, and RETURN is what a call hands back to its parent.

### Decision 1, State: what would you write on a notepad?

Solve a small example by hand, left to right, and notice what you jot down. That is your state. The state is the **smallest summary of the past that lets you continue**; if you feel you need the whole past, the trick has not been found yet.

| Problem | What you jot down by hand | State in code |
|---|---|---|
| Two Sum | "the numbers I have passed, and where" | `seen = {}` value → index |
| Best time to buy and sell | "the cheapest price so far" | one variable `cheapest` |
| Daily temperatures | "the days still waiting for a warmer day" | stack of indices |
| Valid parentheses | "the brackets still open, latest first" | stack of characters |
| Number of islands | "the cells I already painted" | visited set (or overwrite the grid) |
| Merge intervals | "the interval I am currently growing" | `merged[-1]` |
| k-th largest in a stream | "the k biggest so far, and the smallest of them" | min-heap of size k |
| Course schedule | "how many prerequisites each course still waits for" | indegree list + queue of ready courses |

### Decision 2, Definition: say exactly what a variable means

Most bugs are **definition drift**: you meant one thing and coded another. A precise comment next to each variable prevents it, and it is also the sentence you say to the interviewer. Binary search is the classic case: "the answer lies in `[lo, hi]` with `hi = len(a)` meaning *none*" forces every other line.

```python
def first_at_least(a, x):
    """Index of the first element >= x, or len(a) if there is none."""
    lo, hi = 0, len(a)               # DEFINITION: the answer is in [lo, hi]; hi = len(a) means "none"
    while lo < hi:                   # INVARIANT: more than one candidate is left
        mid = (lo + hi) // 2
        if a[mid] >= x:
            hi = mid                 # mid could be the answer: keep it in the range
        else:
            lo = mid + 1             # mid is too small: drop it
    return lo                        # RETURN: one candidate left


print(first_at_least([1, 3, 5], 4), first_at_least([1, 3, 5], 9), first_at_least([], 1))   # 2 3 0
assert all(first_at_least([1, 3, 3, 5], x) == bisect.bisect_left([1, 3, 3, 5], x) for x in range(7))
```

**Try it**
- Change `hi = mid` to `hi = mid - 1` and run `first_at_least([1, 3, 5], 3)`: 0 instead of 1. You threw away the answer, which the definition says must stay in the range.
- Mix two definitions: keep `hi = len(a)` but write `while lo <= hi`. `first_at_least([1, 3, 5], 9)` now reads `a[3]` (IndexError), and `x = 4` never stops (`lo = hi = 2` forever), so put `steps += 1; assert steps < 50` in the loop before you try it.
- The other consistent choice is `hi = len(a) - 1`, `while lo <= hi`, `hi = mid - 1`, with the answer tracked in a variable. Write it, and check it against `bisect.bisect_left` like the assert above.

### Decision 3, Invariant: the repair loop is the invariant, negated

Once you can say the invariant, the hardest line (the `while` condition) writes itself: it is the invariant, negated. The loop runs exactly while the invariant is broken.

| Invariant (true after the repair) | Repair loop |
|---|---|
| no repeated letter in the window | `while count[c] > 1:` |
| waiting temperatures never increase toward the top of the stack | `while stack and temps[stack[-1]] < t:` |
| every stored hit is younger than 300 seconds | `while hits and hits[0] <= t - 300:` |
| the heap holds at most k items | `if len(heap) > k: heappop(heap)` |
| the answer lies in `[lo, hi]` | `while lo < hi:` (stop when one candidate is left) |

While practising, `assert` the invariant right after the loop. A failing assert points at the exact step that broke it, long before the final answer looks wrong.

### Decisions 4 and 5, Step and Record: the order of two lines

The same lines in a different order give a different program. Two Sum is the smallest example: ask the past *before* joining it, or a number pairs with itself.

```python
def two_sum(nums, target):
    seen = {}                             # STATE + INIT: seen[value] = index of an EARLIER element
    for i, x in enumerate(nums):
        if target - x in seen:            # RECORD: ask the past first
            return [seen[target - x], i]
        seen[x] = i                       # STEP: then join the past
    return []                             # RETURN: no pair


def two_sum_insert_first(nums, target):   # the same lines, two of them swapped
    seen = {}
    for i, x in enumerate(nums):
        seen[x] = i
        if target - x in seen:
            return [seen[target - x], i]
    return []


print(two_sum([3, 2, 4], 6))                # [1, 2]
print(two_sum_insert_first([3, 2, 4], 6))   # [0, 0]  <- 3 + 3, using the same 3 twice
```

**Try it**
- Run both functions on `[3, 3], 6`. The correct one gives `[0, 1]`; the swapped one gives `[0, 0]` again. The definition says "EARLIER element", and the swapped order breaks it.
- Print `seen` just before the `return` in `two_sum([3, 2, 4], 6)`: `{3: 0, 2: 1}`. The current number is never inside; that is what "earlier" means.
- Turn it into *count all pairs*: `seen = Counter()`, then `pairs += seen[target - x]` and `seen[x] += 1` in the loop. `[1, 1, 1], 2` gives 3 pairs; swap the two lines and you get 6, because every number paired with itself.

| Order question | Rule of thumb | Where it matters |
|---|---|---|
| ask the past before joining it? | if the current item must not pair with itself: ask first, then join | Two Sum; subarray sum = 0 (`[1, -1, 1]` gives 5 instead of 2 if swapped); buy and sell when a loss is allowed (`[5, 3]` gives 0 instead of −2) |
| record before or after the fix? | *longest*: after the fix (valid now); *shortest*: inside it (valid until it breaks) | sliding windows |
| record at the pop or at the push? | record when an item's answer becomes known: *next* greater is known when the newcomer pops it; *previous* greater is known at the push, after the pops (what is left below is the answer) | daily temperatures; stock span |
| mark visited when enqueuing or popping? | BFS: when **enqueuing**, or a node enters the queue many times. Dijkstra is the exception: a node is final when it is *popped*, so skip stale pops | rotting oranges; network delay |

### Decisions 6 and 7, Init and Return: the empty past and the "not found" answer

**Init** is the state of the *empty past*: before any item, what is true? A running sum is 0, the cheapest price is `math.inf`, and the set of prefix sums already contains the empty prefix 0. **Return** translates placeholders back into what the problem asked for. Both decisions show up in Subarray Sum Equals K:

```python
def subarray_sum(nums, k):
    seen = Counter({0: 1})            # INIT: the empty prefix (sum 0) has been seen once
    prefix = count = 0
    for x in nums:
        prefix += x                   # STEP: running sum of everything so far
        count += seen[prefix - k]     # RECORD: earlier prefixes that cut out a sum of exactly k
        seen[prefix] += 1             # STEP: this prefix joins the past AFTER asking it
    return count                      # RETURN: 0 when nothing matched


print(subarray_sum([1, 1, 1], 2), subarray_sum([1, -1, 1], 0), subarray_sum([], 3))   # 2 2 0
```

**Try it**
- Start with `seen = Counter()` (no empty prefix): `[1, 1, 1], 2` gives 1 instead of 2. The subarray that starts at index 0 needed the empty prefix as its partner.
- Swap the RECORD line and the last STEP line: `[1, -1, 1], 0` gives 5 instead of 2, because every prefix now pairs with itself.
- Replace `Counter` with `defaultdict(int)` and print `len(seen)` at the end of `[1, 1, 1], 2`: 5 instead of 4. Reading a missing key of a `defaultdict` inserts it; a `Counter` read does not.

### Brute force first, then remove the repeated work

The safest route from idea to code goes through the brute force: it is easy to write correctly, it shows exactly which work repeats, and it becomes the tester for your optimal version.

```python
def max_profit_brute(prices):
    best = 0
    for j in range(len(prices)):              # sell on day j
        for i in range(j):                    # buy on day i: rescans every earlier day
            best = max(best, prices[j] - prices[i])
    return best


def max_profit(prices):
    best, cheapest = 0, math.inf              # STATE + INIT: cheapest = lowest price BEFORE today
    for p in prices:
        best = max(best, p - cheapest)        # RECORD: sell today, using the old state
        cheapest = min(cheapest, p)           # STEP: today joins the past
    return best                               # RETURN


random.seed(0)
for _ in range(300):                          # the habit: test optimal against brute force
    prices = [random.randint(0, 9) for _ in range(random.randint(0, 8))]
    assert max_profit(prices) == max_profit_brute(prices), prices
print(max_profit([7, 1, 5, 3, 6, 4]))         # 5
print("optimal agrees with brute force on 300 random inputs")
```

**Try it**
- The inner loop of the brute force recomputes `min(prices[:j])` every time. Point at the variable in `max_profit` that remembers it instead.
- Swap the two lines inside the loop of `max_profit` and rerun the cross-check: it still passes, because selling on the day you buy gives 0, which never beats a real answer. Not every swap is a bug; reason about *why*.
- Now allow a loss (you must buy and sell): start with `best = -math.inf`, swap the two lines, and run `[5, 3]`. You get 0 instead of −2. The same swap is now a bug, because "sell on the buy day" became a winning answer.
- Initialise `cheapest = 0` instead of `math.inf`: the cross-check fails at once (`[7, 5, 9, 3]` gives 9 instead of 4), because "buy at price 0" was never on offer.

### Skeleton first: three passes

When the code will not come, write it in three passes. Pass 1 is the plan in comments; pass 2 adds the structures and the loop with holes; pass 3 fills the holes. You never hold more than one decision in your head at a time.

```text
# pass 1: the plan
# answer[i] = days until warmer, 0 if never
# stack: the days still waiting
# for each day:
#     resolve every colder waiting day
#     then wait yourself
# return answer
```

```text
# pass 2: the shape
def daily_temperatures(temps):
    answer = [0] * len(temps)
    stack = []                        # indices, still waiting
    for i, t in enumerate(temps):
        while ...:                    # TODO: a colder day is waiting
            ...                       # TODO: resolve it
        stack.append(i)
    return answer
```

Pass 3 is the finished code in the first worked example below.

### Worked examples

The four examples below use techniques that have their own sections later. Read the first one closely now; skim the others and come back to them with their sections.

#### 1. Daily Temperatures (a stack of unresolved items)

*For each day, how many days until a warmer one (0 if never)?* `[73, 74, 75, 71, 69, 72, 76, 73] → [1, 1, 4, 2, 1, 1, 0, 0]`

| Decision | Answer |
|---|---|
| State | the days still waiting for a warmer day |
| Definition | `stack` holds **indices** (not temperatures: we need distances `i - j`) |
| Invariant | read from bottom to top, the waiting temperatures never increase (a warmer day would have resolved the colder ones above it; equal days may wait together) |
| Step | today pops every colder waiting day (the fix), then waits itself |
| Record | at the pop: day `j` waited `i - j` days |
| Init | `answer = [0] * n` (0 already means "never") |
| Return | `answer`; days left on the stack keep their 0 |

```python
def daily_temperatures(temps):
    answer = [0] * len(temps)                 # INIT: 0 = "no warmer day" unless resolved
    stack = []                                # STATE: indices of waiting days, temps never increasing
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t: # FIX: today resolves every colder waiting day
            j = stack.pop()
            answer[j] = i - j                 # RECORD at the pop
        stack.append(i)                       # STEP: today waits too
    return answer                             # RETURN: unresolved days keep 0


def trace_daily(temps):                       # the same code, printing a dry-run table
    answer, stack = [0] * len(temps), []
    print(f" i   t  resolved          waiting temps")
    for i, t in enumerate(temps):
        resolved = []
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
            resolved.append(f"day{j}:{i - j}")
        stack.append(i)
        print(f"{i:>2} {t:>3}  {', '.join(resolved):<17} {[temps[k] for k in stack]}")
    return answer


print(trace_daily([73, 74, 75, 71, 69, 72, 76, 73]))   # [1, 1, 4, 2, 1, 1, 0, 0]
```

**Try it**
- Read each row of the "waiting temps" column from left (bottom of the stack) to right (top): it never goes up. That is the invariant, visible.
- Change `<` to `<=` and run `daily_temperatures([70, 70, 71])`: you get `[1, 1, 0]` instead of `[2, 1, 0]`, because an equally warm day "resolved" day 0.
- Move `stack.append(i)` to *before* the `while` loop and run `daily_temperatures([73, 74])`: `[0, 0]`. Today now sits on top and blocks every comparison.
- Predict the output for a falling list `[5, 4, 3]`, then run it. Nothing is ever resolved, and the initial zeros are already the right answer.

#### 2. Rotting Oranges (BFS in rings)

*Each minute, rotten oranges rot their fresh neighbours. Minutes until none are fresh, or −1.*

| Decision | Answer |
|---|---|
| State | the queue of oranges that rotted in the last minute, plus a count of fresh ones |
| Definition | at the top of each `while` round, the queue holds exactly the oranges that rotted at minute `minutes` |
| Invariant | processing `len(queue)` items finishes one minute and leaves the next ring in the queue |
| Step | each rotten orange rots its fresh neighbours; mark them **when enqueuing**. Stop when nothing is fresh, or the last, empty ring would add a minute |
| Record | after a full ring, `minutes += 1` |
| Init | **all** rotten oranges in the queue at minute 0 (multi-source) |
| Return | `minutes` if no fresh orange is left, else −1 |

```python
def oranges_rotting(grid):
    R, C = len(grid), len(grid[0])
    queue = deque((r, c) for r in range(R) for c in range(C) if grid[r][c] == 2)  # INIT: all sources
    fresh = sum(row.count(1) for row in grid)          # STATE: fresh oranges left
    minutes = 0
    while queue and fresh:                             # one round = one minute; stop when none is fresh
        for _ in range(len(queue)):                    # exactly the oranges of minute `minutes`
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2                   # STEP: rot it, marking it when ENQUEUING
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1                                   # RECORD: a minute has passed
    return minutes if fresh == 0 else -1               # RETURN: unreachable fresh -> -1


print(oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))   # 4
print(oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))   # -1
print(oranges_rotting([[0, 2]]))                            # 0
print(oranges_rotting([[2, 1, 1, 1, 2]]))                   # 2  (both ends spread at once)
```

**Try it**
- Change `while queue and fresh:` to `while queue:` and rerun the first grid: 5 instead of 4. The last ring rots nothing, but it still counted a minute.
- Mark when *popping* instead: enqueue fresh neighbours without changing them, and after `popleft` write `if grid[r][c] == 1: grid[r][c] = 2; fresh -= 1`. The first grid gives 5 instead of 4, and count the appends: 9 for only 6 fresh oranges, because unmarked cells get queued twice.
- Seed the queue with only the *first* rotten orange on `[[2, 1, 1, 1, 2]]` (e.g. `deque([(0, 0)])`): 3 instead of 2. Multi-source BFS means every source starts at minute 0.
- Predict `oranges_rotting([[1]])` and `oranges_rotting([[0]])` before running (−1 and 0). Note the function changes `grid`: pass a copy if you need the grid afterwards.

#### 3. Diameter of a Binary Tree (return vs record)

*Longest path between any two nodes, counted in edges.* In tree recursion the key decision is **what a call RETURNS to its parent** versus **what it RECORDS globally**. They differ whenever the best path can bend at a node: a bent path is a candidate answer, but only a straight path can be extended by the parent.

```text
        1          height(2) = 2 nodes (2, 4): also 2 edges from 1 down that side
       / \         height(3) = 1 node  (3):    also 1 edge  from 1 down that side
      2   3        path bending at 1: 4-2-1-3 has 2 + 1 = 3 edges
     / \
    4   5          a height counted in NODES below a child = EDGES from the parent down that side
```

| Decision | Answer |
|---|---|
| State | `best`, the longest bent path seen anywhere |
| Definition | `height(node)` = number of nodes on the longest *downward* path from `node` |
| Invariant | when `height(node)` returns, every path inside its subtree has been considered for `best` |
| Step | combine the two children's heights |
| Record | `best = max(best, left + right)`: the path bending at this node has `left + right` edges |
| Init | the base case `height(None) = 0` |
| Return | `1 + max(left, right)` to the parent (only one side can continue upward; the `+ 1` is the node itself); `best` at the end |

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build(values):                            # LeetCode level order, None = missing child
    nodes = [TreeNode(v) if v is not None else None for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node:
            node.left, node.right = next(kids, None), next(kids, None)
    return nodes[0] if nodes else None


def diameter(root):
    best = 0                                  # STATE: longest bent path seen, in edges

    def height(node):                         # DEFINITION: nodes on the longest downward path
        nonlocal best
        if node is None:
            return 0                          # INIT: the base case
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)        # RECORD: the path that bends here
        return 1 + max(left, right)           # RETURN: only one side can go up

    height(root)
    return best


print(diameter(build([1, 2, 3, 4, 5])))                        # 3  (4-2-1-3)
print(diameter(build([1, 2, None, 3, 4, 5, None, None, 6])))   # 4  (5-3-2-4-6, not through the root)
print(diameter(build([])), diameter(build([1])))               # 0 0
```

**Try it**
- Return `1 + left + right` instead of `1 + max(left, right)` and run the first tree: 4 instead of 3. You told the parent it may extend a path that already bends, and no real path can do that.
- Record only at the root (`left + right` of the root) instead of at every node: the second tree gives 3 instead of 4, because its best path never touches the root.
- Delete the `nonlocal best` line: `UnboundLocalError`. Python treats `best` as a new local the moment you assign to it.
- Return `max(left, right)` (forget the `+ 1`): every height becomes 0 and the answer is 0. The `+ 1` is the node itself.

#### 4. Design a Hit Counter (from requirements to a class)

*`hit(t)` records a hit at second `t`; `count(t)` returns the hits in the last 300 seconds (`t-299 .. t`). Timestamps never go backwards.* Design questions use the same decisions, applied to the class:

| Decision | Answer |
|---|---|
| State | a deque of hit timestamps |
| Definition | `hits` = timestamps still inside the window, oldest at the left |
| Invariant | after `_expire(t)`, every stored timestamp is `> t - 300` |
| Step | `hit`: append, then expire; `count`: expire, then measure |
| Record | `count` returns `len(hits)` |
| Init | an empty deque |
| Return / edges | many hits in one second, `count` long after the last hit, a hit exactly 300 s old (expired) |

```python
class HitCounter:
    WINDOW = 300

    def __init__(self):
        self.hits = deque()                   # STATE: timestamps inside the window, oldest first

    def _expire(self, t):                     # FIX: restore the invariant for time t
        while self.hits and self.hits[0] <= t - self.WINDOW:
            self.hits.popleft()

    def hit(self, t):
        self.hits.append(t)                   # STEP
        self._expire(t)

    def count(self, t):
        self._expire(t)
        return len(self.hits)                 # RECORD / RETURN


hc = HitCounter()
for t in (1, 2, 3):
    hc.hit(t)
print(hc.count(4))                            # 3
hc.hit(300)
print(hc.count(300))                          # 4
print(hc.count(301))                          # 3  (the hit at second 1 is now 300 s old)
```

**Try it**
- Change `<=` to `<` in `_expire` and rerun: `count(301)` gives 4, so your window became 301 seconds wide. Boundary words ("in the past 300 seconds") decide `<` vs `<=`.
- Call `hc.count(10_000)`: 0, and the deque is empty afterwards. Expiring on reads keeps memory bounded too.
- Follow-up interviewers love: a million hits in the same second. Store `[t, count]` pairs: `hit` adds 1 to the last pair when `t` repeats (else appends `[t, 1]`) and does `total += 1`; `_expire` subtracts each popped pair's count from `total`; `count` returns `total`.
- What breaks if timestamps can arrive out of order? The "oldest at the left" definition fails; you would need a heap or a bucket per second.

### Your turn: Contains Duplicate II

*Is there a pair `i != j` with `nums[i] == nums[j]` and `|i - j| <= k`?* `[1, 2, 3, 1], k = 3 → True` · `[1, 2, 3, 1, 2, 3], k = 2 → False`

Fill in the seven decisions on paper first, then open the answers.

<details><summary>The seven decisions</summary>

| Decision | Answer |
|---|---|
| State | for every value seen so far, where it was last seen |
| Definition | `last[v]` = the **most recent** index of v (the nearest copy is the only one that matters) |
| Invariant | `last` describes exactly `nums[0 .. i-1]` |
| Step | after asking, `last[v] = i` (overwrite: the newest copy wins) |
| Record | if `v in last` and `i - last[v] <= k`: return True |
| Init | `last = {}` |
| Return | False when the loop ends |

</details>

Now write it in the cell below and run the cell; the checker tests fixed cases and 300 random inputs against a brute force.

```python
def contains_nearby_duplicate(nums, k):
    # write the seven decisions as comments first, then the code
    return None


def check_your_turn(fn):
    if fn([1, 2, 3, 1], 3) is None:
        print("not written yet: fill in contains_nearby_duplicate and run this cell again")
        return
    cases = [(([1, 2, 3, 1], 3), True), (([1, 0, 1, 1], 1), True),
             (([1, 2, 3, 1, 2, 3], 2), False), (([], 0), False), (([1, 1], 0), False)]
    for args, want in cases:
        got = fn(*args)
        print(("ok   " if got == want else "FAIL ") + f"{args} -> {got} (expected {want})")
    rng = random.Random(0)
    for _ in range(300):
        nums, k = [rng.randint(0, 3) for _ in range(rng.randint(0, 8))], rng.randint(0, 4)
        want = any(nums[i] == nums[j] for i in range(len(nums)) for j in range(i + 1, min(len(nums), i + k + 1)))
        if fn(nums, k) != want:
            print(f"FAIL on random input {nums}, k={k}: expected {want}")
            return
    print("all random checks pass")


check_your_turn(contains_nearby_duplicate)
```

**Try it**
- Write your solution, run the cell, and read the checker's lines. If a random case fails, trace that exact input with a state table.
- Use `last.setdefault(v, i)` (keeps the *first* index) instead of `last[v] = i`: the case `[1, 0, 1, 1], k = 1` fails. The Definition said *most recent*.
- Put the `last[v] = i` line before the check: every value now finds itself at distance 0, so `[1, 2], 0` would say True. Same lesson as Two Sum: ask the past, then join it.

<details><summary>One solution</summary>

```py
def contains_nearby_duplicate(nums, k):
    last = {}                                  # STATE: last[v] = most recent index of v
    for i, v in enumerate(nums):
        if v in last and i - last[v] <= k:     # RECORD: ask the past
            return True
        last[v] = i                            # STEP: join the past, newest copy wins
    return False                               # RETURN
```

</details>

### Words → Python

| When the idea says … | Write … |
|---|---|
| "for each item and its position" | `for i, x in enumerate(a):` |
| "have I seen x?" | `x in seen` with a `set` or `dict` (never a `list`) |
| "how many times" | `count = Counter(a)` or `count[x] += 1` with `defaultdict(int)` |
| "group by a key" | `groups = defaultdict(list); groups[key].append(x)` |
| "best so far" | `best = max(best, candidate)`, start from `0`, `-math.inf` or the first item |
| "repeatedly take the smallest" | `heapq.heappush(h, (priority, item))`, `heapq.heappop(h)` |
| "the k largest" | a min-heap capped at size k |
| "first position where the condition becomes true" | binary search template, or `bisect_left` |
| "nearest first" (unweighted) | `deque` BFS; weighted: a heap (Dijkstra) |
| "undo the last choice" | `path.pop()` right after the recursive call |
| "the most recent unresolved item" | `stack[-1]` |
| "the oldest item" | `queue.popleft()` |
| "neighbours in a grid" | `for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):` + bounds check |
| "are a and b connected?" with merges | union-find |
| "sum of a range" | `P = [0] + list(accumulate(a))`, then `sum(a[i:j]) == P[j] - P[i]` |
| "pairs from both ends" | `l, r = 0, len(a) - 1` |
| "in order of dependencies" | indegree counts + queue of ready nodes |
| "sort, but keep the original positions" | `order = sorted(range(n), key=lambda i: a[i])` |
| "sort by end, then by start" | `intervals.sort(key=lambda iv: (iv[1], iv[0]))` |
| "return the window, not its length" | record `best_left` together with `best_len` |
| "build a string" | collect parts in a list, then `"".join(parts)` |
| "a grid of zeros" | `[[0] * C for _ in range(R)]` |
| "nothing found yet" | `math.inf` / `-1` / `None`, translated at the end |

### Operation → data structure

When a design or an optimisation asks "make this operation fast", pick the structure by the operation, not by the problem's name. The four you will reach for most:

| I need to do this fast | Use |
|---|---|
| membership test, lookup by key, counting | `set` / `dict` / `Counter`: O(1) |
| the min or max, again and again, with inserts | heap: O(log n) |
| lookup + order by recency | `dict` + doubly linked list (or `OrderedDict`): O(1) |
| first index ≥ x in a sorted list, latest value at time t | `bisect`: O(log n) |

The full table, with the question each structure answers and how several structures stay in sync inside one class, is in [Design Problems](#s24).

### When the code still will not come

1. **Name the sub-steps** as helper functions (`neighbours(r, c)`, `is_valid()`, `_expire(t)`), write the main loop calling them, then implement each helper. Small named pieces are easier to get right and easier to explain.
2. **Shrink the input** until you can run it in your head (three items), and write the code for exactly one step of it.
3. **Say which decision you are stuck on.** "I'm not sure whether to record before or after shrinking" is a precise question; interviewers answer precise questions, and thinking out loud is how they see your reasoning.
