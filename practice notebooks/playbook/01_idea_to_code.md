## From Idea to Code

> An idea is one sentence. Code is a handful of decisions. Make the decisions first, in plain words, and typing becomes translation.

[Start Here](#s00) took you through the interview loop and the clue table to a chosen technique. This section is step 4 of that loop, the plan: how the chosen technique becomes lines of code, through seven decisions that every later section answers for its own technique.

### Why you freeze

"I'll use a sliding window" sounds like a plan. It is only an idea: it leaves seven questions open, from *what do I store* to *what do I return when nothing works*. Answer all seven *while typing* and your working memory overflows; you freeze, or you write a bug.

The fix is to **separate deciding from typing**. Answer the seven questions first, out loud and as comments, then translate each answer into its line. The rest of this section walks through the decisions one at a time on problems you may already know, then applies all seven to four whole problems.

### The seven decisions

The first two decisions say what you keep. **State** is what you must remember about items 0..i to carry on after stopping at item i: a dict of counts, a best so far, a pointer, a stack of unresolved items, a visited set, a heap of candidates. **Definition** says exactly what each variable means, written as a comment: `seen[v]` is the index of an earlier v, `stack` holds the indices of days still waiting, `dist[u]` is the shortest distance found so far.

The next two say how the state moves. **Invariant** is the sentence about the state that is true every time the loop comes round: the window has no repeats, the stack's temperatures never increase, the answer lies in `[lo, hi]`. **Step** is how one new item, node or edge changes the state: add it, then restore the invariant by popping, shrinking, relaxing or uniting.

The last three place the answer and the two ends of the loop. **Record** is the line on which you *know* a piece of the answer: after the invariant is restored, at the moment of a pop, when the target is reached. **Init** is the state before anything is processed: empty, 0, `math.inf`, a sentinel, a dummy node, the start node already in the queue. **Return** is what comes back, including when nothing was found: `best`, `-1`, `[]`, `""`, or `inf` translated into what the problem asked for.

Almost every interview solution has the same shape, so each decision lands in a predictable place. The tags in this playbook's code (`# STATE`, `# STEP`, `# FIX`, `# RECORD`, ...) point at exactly these lines:

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

The seven decisions name no Fix, yet the skeleton has a FIX line: some sections split Step into two halves, Step for taking the item and Fix for repairing the invariant. Some also merge State with Definition when the state is one structure.

The **order** of STEP, FIX and RECORD is itself a decision. Two Sum, which asks for two indices whose values add to a target, records *before* its step. A shortest window, the shortest subarray whose sum reaches a target, records *inside* its fix. A next-greater stack, which finds for each item the next bigger one, records at each pop.

In recursion the shape turns on its side: INIT is the base case, the "items" are the children, and RETURN is what a call hands back to its parent.

### Decision 1, State: what would you write on a notepad?

Everything else is phrased in terms of the state, so it comes first. Solve a small example by hand, left to right, and notice what you jot down. That is your state: the **smallest summary of the past that lets you continue**. If you feel you need the whole past, the trick has not been found yet.

In Two Sum you jot down the numbers you have passed and where you saw them: a dict `seen` from value to index. In Best Time to Buy and Sell Stock, where you buy on one day and sell on a later one for the best profit, you only ever need the cheapest price so far: one variable `cheapest`.

In Daily Temperatures, which asks for each day how many days until a warmer one, you keep the days still waiting for a warmer day: a stack of indices. In Valid Parentheses, which asks whether every bracket in a string is closed by its own kind in the right order, you keep the brackets still open, latest first: a stack of characters.

Number of Islands counts the groups of connected land cells in a grid, and what you track is the cells you already painted: a visited set, or the grid itself overwritten. Merge Intervals merges every pair of overlapping ranges, `[[1, 3], [2, 6], [8, 10]] → [[1, 6], [8, 10]]`, and you only hold the interval you are currently growing: `merged[-1]`.

Kth Largest Element in a Stream asks, after each new number, for the k-th largest seen so far, and you keep the k biggest so far and the smallest of them: a min-heap of size k. Course Schedule asks whether every course can be taken when some courses require others first, and you count how many prerequisites each course still waits for: an indegree list and a queue of the courses that are ready.

### Decision 2, Definition: say exactly what a variable means

Once you know what you store, say exactly what it means, because most bugs are **definition drift**: you meant one thing and coded another. A precise comment next to each variable prevents it, and it is also the sentence you say to the interviewer.

Binary search is the classic case. The function below finds the first index in a sorted list whose element is at least x, or `len(a)` if there is none: in `[1, 3, 5]`, the answer for 4 is 2 and for 9 it is 3. The definition "the answer is in `[lo, hi]`, and `hi = len(a)` means none" forces every other line: the loop runs while more than one candidate is left, a big-enough `mid` stays in the range, and a too-small `mid` is dropped.

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
- Change only the definition of `hi`: `lo, hi = 0, len(a) - 1` ("the last candidate") and nothing else. `first_at_least([1, 3, 5], 9)` returns 2 instead of 3: the code still runs, but `len(a)` no longer means "none", so a caller cannot tell "found at index 2" from "nothing qualifies". One changed definition silently changes what the return value means.
- Mix two definitions: keep `hi = len(a)` but write `while lo <= hi`. `first_at_least([1, 3, 5], 9)` now reads `a[3]`, an IndexError, and `x = 4` never stops, because `lo = hi = 2` forever. Put `steps += 1; assert steps < 50` in the loop before you try it.
- The other consistent choice is `hi = len(a) - 1`, `while lo <= hi`, `hi = mid - 1`, with the answer tracked in a variable. Write it, and check it against `bisect.bisect_left` like the assert above. The loop styles and what each mix-up breaks are taken apart in [Binary Search](#s09).

### Decision 3, Invariant: the repair loop is the invariant, negated

With the variables defined, say what must stay true about them. An invariant is a sentence about the state that holds every time the loop comes back to its top. Once you can say it, the hardest line, the `while` condition, writes itself: it is the invariant, negated, and the loop runs exactly while the invariant is broken.

Longest Substring Without Repeating Characters asks for the longest window with no letter twice, `"abcabcbb" → 3`. Its invariant, "no repeated letter in the window", negates into `while count[c] > 1:`, because only the new letter `c` can be the doubled one.

Stacks and queues read the same way. In Daily Temperatures, "the waiting temperatures never increase toward the top of the stack" becomes `while stack and temps[stack[-1]] < t:`. In Design Hit Counter, which counts the hits of the last 300 seconds, "every stored hit is younger than 300 seconds" becomes `while hits and hits[0] <= t - 300:`.

In Kth Largest Element in a Stream, "the heap holds at most k items" becomes `if len(heap) > k: heappop(heap)`, an `if` rather than a `while`, because one push breaks it by at most one. In binary search, "the answer lies in `[lo, hi]`" becomes `while lo < hi:`, which stops when one candidate is left.

While practising, `assert` the invariant right after the loop. A failing assert points at the exact step that broke it, long before the final answer looks wrong.

### Decisions 4 and 5, Step and Record: the order of two lines

Now the loop body: how one item changes the state, and on which line a piece of the answer is known. The same lines in a different order give a different program, and Two Sum is the smallest example.

Two Sum asks for the indices of two numbers that add up to a target, without using one number twice: `[3, 2, 4], 6 → [1, 2]`. The state is `seen`, a dict from each value to the index of an *earlier* element. Walk the list once; for each number, ask whether its partner `target - x` is already in `seen`, and only then let the number join. The second function has the same lines with two of them swapped, and it pairs 3 with itself.

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
- Try to rescue the swapped order with a guard, `if target - x in seen and seen[target - x] != i`, keeping `seen[x] = i` above it: `[3, 3], 6` now returns `[]`, because the second 3 overwrote the first one's index before asking. Order beats patching.

The same order question returns in every family, and the rule is always the same: record on the line where the answer is known. Ask the past before joining it whenever the current item must not pair with itself.

Two Sum follows that rule. So does Subarray Sum Equals K, which counts the subarrays that sum to k: with k = 0, `[1, -1, 1]` gives 5 instead of 2 if the two lines are swapped. So does buy-and-sell when a loss is allowed, where `[5, 3]` gives 0 instead of −2.

For a window, record after the fix when you want the *longest*, because the window is valid again only then, and inside the fix when you want the *shortest*, while the window is still valid.

For a stack, record at the moment an item's answer becomes known. The *next* greater element is known when the newcomer pops it, as in Daily Temperatures. The *previous* greater is known at the push, after the pops, because what is left below is the answer; that is Online Stock Span, which asks for each day how many consecutive days up to today had a price at most today's.

For a search, mark a node visited when **enqueuing** it in BFS, or it enters the queue many times; Rotting Oranges, the second worked example below, shows the cost. Dijkstra is the exception: a node is final when it is *popped*, so stale pops are skipped. Network Delay Time, which asks how long until a signal from one node has reached every node, is the standard example.

### Decisions 6 and 7, Init and Return: the empty past and the "not found" answer

The loop is written; what is left is its two ends. **Init** is the state of the *empty past*: before any item, what is true? A running sum is 0, the cheapest price is `math.inf`, and the set of prefix sums already contains the empty prefix 0. **Return** translates placeholders back into what the problem asked for: `inf` becomes 0 or −1, a pair never found becomes `[]`.

Subarray Sum Equals K shows both. It counts the contiguous subarrays that sum to exactly k, negative numbers allowed: `[1, 1, 1], k = 2 → 2`. A subarray sums to k exactly when the running sums at its two ends differ by k, so each new running sum `prefix` adds the number of earlier ones equal to `prefix - k`. Init counts the empty prefix 0 as seen, or every subarray that starts at index 0 is lost; the return is the count, 0 when nothing matched.

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
- Print `seen` at the end of `subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7)` (answer 4): `seen[14]` is 2, because `prefix` is 14 twice, and the stretch `[2, -3, 1]` between those two moments sums to 0. Equal running sums mark exactly the zero-sum stretches, and a later prefix of 21 would pair with both, which is why `seen` stores counts and not a set.

### Brute force first, then remove the repeated work

The safest route from idea to code goes through the brute force. It is easy to write correctly, it shows exactly which work repeats, and it becomes the tester for your optimal version.

Best Time to Buy and Sell Stock shows the route: buy on one day, sell on a later one, and return the best profit, or 0 if no trade makes money. On `[7, 1, 5, 3, 6, 4]` the answer is 5, buying at 1 and selling at 6. The brute force rescans every earlier day for each sell day; the optimal version keeps what that rescan computes, the cheapest price before today. The cell ends with the habit to keep: a cross-check of the two on 300 random inputs.

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
- Print `cheapest` at the top of the loop in `max_profit([7, 1, 5, 3, 6, 4])`: `inf 7 1 1 1 1`. Each value is the `min(prices[:j])` that the brute force's inner loop rescans for sell day j; the optimal version remembers it instead.
- Swap the two lines inside the loop of `max_profit` and rerun the cross-check: it still passes, because selling on the day you buy gives 0, which never beats a real answer. Not every swap is a bug; reason about *why*.
- Now allow a loss (you must buy and sell): start with `best = -math.inf`, swap the two lines, and run `[5, 3]`. You get 0 instead of −2. The same swap is now a bug, because "sell on the buy day" became a winning answer.
- Initialise `cheapest = 0` instead of `math.inf`: the cross-check fails on its second random input, `[7, 5, 9, 3]`, with 9 instead of 4, because "buy at price 0" was never on offer.

### Skeleton first: three passes

Even with the decisions made, the code may not come out in one go. Then write it in three passes: pass 1 is the plan in comments, pass 2 adds the structures and the loop with holes, pass 3 fills the holes. You never hold more than one decision in your head at a time. The example is Daily Temperatures, the first worked example below: for each day, how many days until a warmer one.

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

Now the seven decisions on four whole problems, one per family: a stack, a queue, a recursion and a class. Each uses a technique that has its own section later. Read the first one closely now; skim the others and come back to them with their sections.

**Daily Temperatures** asks, for each day, how many days you wait for a warmer one, or 0 if none ever comes: `[73, 74, 75, 71, 69, 72, 76, 73] → [1, 1, 4, 2, 1, 1, 0, 0]`. It comes first because its code is the finished third pass of the skeleton above, and its section is [Monotonic Stack](#s08).

The state is the days still waiting for a warmer day, and the definition is that `stack` holds their *indices*, not their temperatures, because the answer is a distance `i - j`. The invariant, read from the bottom of the stack to the top, is that the waiting temperatures never increase: a warmer day would already have resolved the colder ones above it, and equal days may wait together.

A step lets today pop every colder waiting day, which is the fix, and then today waits itself. The record happens at the pop, because that is the moment day `j` learns it waited `i - j` days. Init is `answer = [0] * n`, so 0 already means "never", and the return is `answer`, where the days left on the stack keep their 0.

Every day is pushed once and popped at most once, so the whole pass is O(n). The cell writes the seven decisions as code, then runs the same lines in a second function that prints a dry-run table, the state after every step, which is exactly what you would draw on the whiteboard.

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

**Rotting Oranges** asks how many minutes pass until no orange is fresh, or −1 if some orange can never rot. A grid holds empty cells (0), fresh oranges (1) and rotten ones (2), and every minute each rotten orange rots its four fresh neighbours: `[[2, 1, 1], [1, 1, 0], [0, 1, 1]] → 4`. It comes next because it makes the same decisions with a queue instead of a stack, and its section is [Graphs I](#s17).

Each minute is one ring of a breadth-first search, and the queue holds exactly the oranges that rotted in the minute before:

```text
minute 0      minute 1      minute 2      minute 3      minute 4
2 1 1         2 2 1         2 2 2         2 2 2         2 2 2
1 1 0         2 1 0         2 2 0         2 2 0         2 2 0
0 1 1         0 1 1         0 1 1         0 2 1         0 2 2
```

The state is the queue of oranges that rotted in the last minute, plus a count of the fresh ones. The definition: at the top of each `while` round, the queue holds exactly the oranges that rotted at minute `minutes`. The invariant: processing `len(queue)` items finishes one minute and leaves the next ring in the queue.

A step lets one rotten orange rot its fresh neighbours, and each neighbour is marked *when it is enqueued*. The rounds stop as soon as nothing is fresh, so that a last, empty ring does not add a minute, and the record is `minutes += 1` after each full ring. Init puts *all* rotten oranges in the queue at minute 0; several starting points in one queue is what multi-source means. The return is `minutes` if no fresh orange is left, else −1.

Every cell enters the queue at most once, so the time is O(rows × columns). The cell is the seven decisions in code, run on four grids: the example, a grid with an orange that no rot can reach, a grid with nothing fresh, and a row that rots from both ends at once.

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

**Diameter of a Binary Tree** asks for the number of edges on the longest path between any two nodes, a path that need not pass through the root: the tree `[1, 2, 3, 4, 5]` has diameter 3, the path 4-2-1-3. It comes third because it moves the decisions into recursion, and its section is [Trees](#s11).

In tree recursion the key decision is what a call *returns* to its parent versus what it *records* globally. They differ whenever the best path can bend at a node: a bent path is a candidate answer, but only a straight path can be extended by the parent.

```text
        1          height(2) = 2 nodes (2, 4): also 2 edges from 1 down that side
       / \         height(3) = 1 node  (3):    also 1 edge  from 1 down that side
      2   3        path bending at 1: 4-2-1-3 has 2 + 1 = 3 edges
     / \
    4   5          a height counted in NODES below a child = EDGES from the parent down that side
```

The state is `best`, the longest bent path seen anywhere. The definition: `height(node)` is the number of nodes on the longest downward path from `node`. The invariant: when `height(node)` returns, every path inside its subtree has been considered for `best`.

A step combines the two children's heights, and the record is `best = max(best, left + right)`, because the path bending at this node has `left + right` edges. Init is the base case, `height(None) = 0`. The return to the parent is `1 + max(left, right)`: only one side can continue upward, and the `+ 1` is the node itself. The function itself returns `best` at the end.

The cell first defines `TreeNode` and `build_tree`, which makes a tree from LeetCode's level-order list with `None` for a missing child, then measures three trees. In the second one the longest path, 5-3-2-4-6, never touches the root, which is why the record happens at every node and not only at the top.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_tree(values):                       # LeetCode level order, None = missing child
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


print(diameter(build_tree([1, 2, 3, 4, 5])))                        # 3  (4-2-1-3)
print(diameter(build_tree([1, 2, None, 3, 4, 5, None, None, 6])))   # 4  (5-3-2-4-6, not through the root)
print(diameter(build_tree([])), diameter(build_tree([1])))          # 0 0
```

**Try it**
- Return `1 + left + right` instead of `1 + max(left, right)` and run the first tree: 4 instead of 3. You told the parent it may extend a path that already bends, and no real path can do that.
- Record only at the root (`left + right` of the root) instead of at every node: the second tree gives 3 instead of 4, because its best path never touches the root.
- Delete the `nonlocal best` line: `UnboundLocalError`. Python treats `best` as a new local the moment you assign to it.
- Return `max(left, right)` (forget the `+ 1`): every height becomes 0 and the answer is 0. The `+ 1` is the node itself.

**Design Hit Counter** asks for a class with two methods: `hit(t)` records a hit at second `t`, and `count(t)` returns the hits in the last 300 seconds, `t-299 .. t`, where timestamps never go backwards. After hits at 1, 2, 3 and 300, `count(300)` is 4 and `count(301)` is 3, because the hit at second 1 is then 300 seconds old. It comes last because a design question applies the same decisions to a class, and its section is [Design Problems](#s24).

The state is a deque of hit timestamps, and the definition is that `hits` holds the timestamps still inside the window, oldest at the left. The invariant: after `_expire(t)`, every stored timestamp is `> t - 300`. A step in `hit` appends and then expires; in `count` it expires and then measures. The record is `len(hits)`, which `count` returns, and init is an empty deque.

The edges to say out loud are many hits in one second, a `count` long after the last hit, and a hit exactly 300 seconds old, which is expired. In the cell, `_expire` is the fix, written once and called by both methods, and the prints replay the example.

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
- The follow-up interviewers love is a million hits in the same second. Store `[t, count]` pairs and a running `total`: `hit` adds 1 to the last pair when `t` repeats, else appends `[t, 1]`, and `_expire` subtracts each popped pair's count from `total`. Hit 1,000 times at second 5: the deque holds one pair, and `count(5)` is 1000.
- Break the promise that timestamps never go backwards: on a fresh counter, `hit(100)`, `hit(1)`, then `count(350)` gives 2 instead of 1. The 1 sits behind the 100, where `_expire` never looks; "oldest at the left" no longer holds, and you would need a heap or a bucket per second.

### Your turn: Contains Duplicate II

Now the method on your own, on a problem small enough to finish in ten minutes. **Contains Duplicate II** asks whether some value appears twice within k positions of itself: a pair `i != j` with `nums[i] == nums[j]` and `|i - j| <= k`. `[1, 2, 3, 1], k = 3 → True` · `[1, 2, 3, 1, 2, 3], k = 2 → False`. Fill in the seven decisions on paper first, then open the answers.

<details><summary>The seven decisions</summary>

The state is, for every value seen so far, where it was last seen. The definition: `last[v]` is the **most recent** index of v, because the nearest copy is the only one that matters. The invariant: `last` describes exactly `nums[0 .. i-1]`. A step, after asking, sets `last[v] = i`, overwriting so that the newest copy wins. The record: if `v in last` and `i - last[v] <= k`, return True. Init is `last = {}`, and the return is False when the loop ends.

</details>

Write it in the cell below and run the cell. The checker prints every fixed case, then tests 300 random inputs against a brute force and names the first input where you differ.

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

Once the decisions are made, typing is translation, and this table is the dictionary: the phrase in your plan on the left, the Python on the right.

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

What each of these costs, and the traps around them: [Python Toolkit](#s02).

To make an operation fast, pick the structure by the operation, not by the problem's name. Membership, lookup by key and counting are a `set`, a `dict` or a `Counter`, O(1). The min or the max again and again, with inserts between, is a heap, O(log n). Lookup plus order by recency is a `dict` with a doubly linked list, or an `OrderedDict`, O(1). The first index ≥ x in a sorted list, or the latest value at time t, is `bisect`, O(log n).

Those are the four you will reach for most. The full table, with the question each structure answers and how several structures stay in sync inside one class, is in [Design Problems](#s24).

### When the code still will not come

Name the sub-steps as helper functions, `neighbours(r, c)`, `is_valid()`, `_expire(t)`: write the main loop calling them, then implement each helper. Small named pieces are easier to get right and easier to explain. Shrink the input until you can run it in your head, three items, and write the code for exactly one step of it.

And say which decision you are stuck on. "I'm not sure whether to record before or after shrinking" is a precise question; interviewers answer precise questions, and thinking out loud is how they see your reasoning.
