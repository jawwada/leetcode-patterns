## Final Checklists

> The last mile: the edge cases to test, the bugs that cost interviews, how to test when you cannot run code, what to say, and how to spend the last week.

### Before you type: the 60-second check

- [ ] I restated the problem and confirmed the output format.
- [ ] I asked about size, value ranges, duplicates, negatives, empty input, sortedness.
- [ ] I wrote 2–3 tiny examples, one of them an edge case.
- [ ] I said the brute force and its complexity.
- [ ] I can say the seven decisions: state, definitions, invariant, step, record, init, return.
- [ ] I wrote them as comments, so the interviewer can follow and I cannot lose my place.
- [ ] The interviewer agreed with the approach before I started coding.

### Edge cases by input type

| Input | Test these |
|---|---|
| Array | empty · one item · two items · all equal · sorted / reverse sorted · negatives · zeros · duplicates · target absent · answer at index 0 or n−1 |
| Window / subarray | k = 0 · k ≥ n · target ≤ 0 · negatives (sliding windows break) |
| String | empty · one character · all the same character · odd / even length · spaces, punctuation, upper / lower case |
| Number | 0 · 1 · negative · 32-bit limits when the problem mentions them · division by zero · modulo of a negative |
| Linked list | empty · one node · two nodes · the head is removed · cycle back to the head · odd / even length |
| Tree | empty · one node · a skewed tree (deep recursion) · duplicate values in a BST · negative values · the target is the root |
| Graph | disconnected · self-loop · parallel edges · cycle · one node · target unreachable · directed vs undirected |
| Grid | 1×1 · one row or one column · all water / all land · start equals end · blocked start or end |
| Intervals | touching ends `[1,2],[2,3]` · one inside another · unsorted input · a single interval |
| Top-k / heap | k = 0 · k = n · ties |
| Binary search | target below all / above all · duplicates · length 1 · the answer is `lo` or `hi` itself |
| Design | capacity 0 or 1 · an operation on an empty structure · repeated keys · updates to an existing key · equal timestamps |

### The bug catalogue

**Python traps**

| Bug | Symptom | Fix |
|---|---|---|
| `[[0] * C] * R` | changing one row changes every row | `[[0] * C for _ in range(R)]` |
| `res.append(path)` in backtracking | every saved result is the same list, ending up empty or identical | `res.append(path[:])` |
| mutable default argument `def f(x, seen=[])` | state leaks between calls | `seen=None`, then `if seen is None: seen = []` |
| assigning to an outer variable inside a nested function | `UnboundLocalError` if the function also reads it first; a silent no-op if it only assigns | `nonlocal best` (or keep it in a list or attribute) |
| reading `d[x]` on a `defaultdict` | `x` is inserted with 0, so `len(d)` (a distinct count) grows | `d.get(x, 0)` or `x in d` |
| `a.sort()` used as a value | `None` | `sorted(a)` returns a list; `a.sort()` sorts in place |
| `max([])` / `min([])` | `ValueError` | `max(a, default=0)` |
| `mid = (lo + hi) / 2` | `TypeError: list indices must be integers` | `//` |
| `-7 // 2` expected −3 | Python floors: −4 | `int(-7 / 2)` truncates toward zero |
| heap of `(priority, payload)` with equal priorities and non-comparable payloads (dicts, nodes) | `TypeError: '<' not supported` | `(priority, counter, payload)` with a running counter |
| max-heap by pushing `-x`, forgetting to negate on pop | answers come out negative | `-heapq.heappop(h)` |
| `Counter` subtraction with `-` | zero and negative counts vanish | `c.subtract(other)` keeps them |
| string `+=` in a loop | can be O(n²) | collect parts, `"".join(parts)` |
| `list.pop(0)` / `x in list` in a loop | O(n²) time | `deque.popleft()` / a `set` |
| recursion deeper than about 1000 levels (the default limit) | `RecursionError` | iterate with an explicit stack |
| modifying a list or dict while iterating it | skipped items or `RuntimeError` | iterate over a copy, or collect changes first |
| reusing a grid or list that the function mutated | later tests see changed data | pass a copy |

**Algorithm traps**

| Bug | Symptom | Fix |
|---|---|---|
| `range(len(a) - 1)` when you meant every index | last item never processed | say the range out loud: "0 to n−1 inclusive" is `range(n)` |
| window length `right - left` | off by one | `right - left + 1` for an inclusive window |
| `if` where a `while` is needed | invariant restored only partly | ask "can one step be not enough?" |
| BFS marks visited when popping | nodes queued many times, slow or wrong counts | mark when **pushing** |
| graph DFS without a visited set | infinite recursion on a cycle | add `seen` before recursing |
| Dijkstra without `if d > dist[u]: continue` | stale entries reprocessed: slow, and wrong with some variants | skip stale pops |
| recording before the invariant is fixed | broken states counted | record after the fix (or inside it for "shortest") |
| `best = 0` for a maximum that can be negative | all-negative inputs return 0 | start from `-math.inf` or the first item |
| forgetting to `return` the recursive call's value | `None` bubbles up | `return helper(...)` |
| binary search with `lo = mid` and `mid = (lo + hi) // 2` | infinite loop when `hi = lo + 1` | `mid = (lo + hi + 1) // 2` there, or the `lo = mid + 1` template |

Several of these are easy to see for yourself:

```python
a = [3, 1, 2]
print(a.sort(), a)                         # None [1, 2, 3]   <- sort() sorts in place and returns None
grid = [[0] * 3] * 2
grid[0][0] = 9
print(grid)                                # [[9, 0, 0], [9, 0, 0]]   <- both rows are one list
print(-7 // 2, int(-7 / 2), -7 % 3)        # -4 -3 2
print(max([], default=0))                  # 0

res, path = [], []
for x in (1, 2):
    path.append(x)
    res.append(path)                       # appends the SAME list object twice
print(res)                                 # [[1, 2], [1, 2]]   <- needs path[:] (a copy)

d = defaultdict(int)
if d["ghost"] == 0:                        # reading a missing key INSERTS it
    pass
print(len(d))                              # 1

c = Counter("aab")
c.subtract(Counter("abbb"))                # subtract() keeps zero and negative counts
print(c, Counter("aab") - Counter("abbb")) # Counter({'a': 1, 'b': -2}) Counter({'a': 1})

h = []
heapq.heappush(h, (1, 0, {"job": "a"}))    # (priority, tie-breaker, payload)
heapq.heappush(h, (1, 1, {"job": "b"}))    # equal priority: the counter decides, dicts never compared
print(heapq.heappop(h)[2])                 # {'job': 'a'}
```

**Try it**
- Remove the tie-breakers (push `(1, {"job": "a"})` and `(1, {"job": "b"})`): `TypeError`, because with equal priorities Python compares the dicts. Plain integers as payloads would have been fine.
- Change `res.append(path)` to `res.append(path[:])`: `[[1], [1, 2]]`. This one line is the most common backtracking bug.
- Write `grid = [[0] * 3 for _ in range(2)]`, set `grid[0][0] = 9` again and print: only the first row changes.
- Predict `-7 % 3` and `7 % -3` before running (2 and −2: the result takes the sign of the divisor).

### Testing when you cannot run the code

In the interview you usually cannot execute anything, so testing means tracing:

1. **Pick the smallest input that makes every loop run zero times, once, and several times** (often 3–4 items).
2. **Write a state table as a comment under the code**: one column per variable, one row per iteration.
3. **Compare the last row with the expected answer, out loud.**
4. **Say each edge case** from the table above and walk only the lines it changes.

While **practising**, add the habit that catches what tracing misses: cross-check your solution against the brute force on many small random inputs. Small inputs mean a failure is small enough to trace by hand.

```python
import copy


def cross_check(fast, slow, make_input, trials=300, seed=0):
    """Run both solutions on random inputs; report the first input where they disagree."""
    rng = random.Random(seed)
    for t in range(trials):
        args = make_input(rng)
        got, want = fast(*copy.deepcopy(args)), slow(*copy.deepcopy(args))
        if got != want:
            print(f"mismatch on trial {t}: input={args}  fast={got}  slow={want}")
            return False
    print(f"{trials} random inputs agree")
    return True


def max_window_sum_brute(nums, k):            # every window of size k: slow but obviously right
    return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))


def max_window_sum_buggy(nums, k):            # best starts at 0
    best = window = 0
    for i, x in enumerate(nums):
        window += x
        if i >= k:
            window -= nums[i - k]             # the item k steps back leaves
        if i >= k - 1:
            best = max(best, window)
    return best


def max_window_sum(nums, k):                  # best starts at -inf
    best, window = -math.inf, 0
    for i, x in enumerate(nums):
        window += x
        if i >= k:
            window -= nums[i - k]
        if i >= k - 1:
            best = max(best, window)
    return best


small = lambda rng: ([rng.randint(-5, 5) for _ in range(rng.randint(3, 6))], rng.randint(1, 3))
_ = cross_check(max_window_sum_buggy, max_window_sum_brute, small)
_ = cross_check(max_window_sum, max_window_sum_brute, small)
```

**Try it**
- Read the mismatch the harness found: every window in that input has a negative sum, and `best = 0` claims a sum no window has. That is the "`best = 0` for a maximum that can be negative" row of the catalogue.
- Change the generator to `rng.randint(0, 5)` (no negatives) and rerun the buggy version: it passes. Your random inputs must be able to reach the edge cases, or the harness proves nothing.
- Raise the list length to 50 and break `max_window_sum` on purpose (e.g. drop the `window -= nums[i - k]` line): the mismatch it prints is much harder to trace by hand. That is why the generator starts small.
- Use `cross_check` for any problem in this notebook: write the brute force first, then the optimal, then check.

### Complexity at a glance

| Operation / algorithm | Time | Note |
|---|---|---|
| sort | O(n log n) | Timsort, stable |
| heap push / pop · heapify | O(log n) · O(n) | `heapq` |
| dict / set lookup, insert | O(1) average | |
| `x in list`, `list.pop(0)`, `list.insert(0, x)` | O(n) | use a set / deque |
| slicing `a[i:j]` · `"".join(parts)` | O(j − i) · O(total length) | slices copy |
| hidden costs | `Counter` equality O(alphabet) · `sorted(word)` as a key O(L log L) · substring keys O(L) | they multiply your loop |
| binary search · on the answer | O(log n) · O(log range × check) | |
| two pointers · sliding window · monotonic stack | O(n) | each index moves / is pushed once |
| BFS / DFS | O(V + E) | grid: O(R × C) |
| Dijkstra with a heap | O((V + E) log V) | non-negative weights |
| union-find with path compression and union by size | almost O(1) per operation | |
| topological sort | O(V + E) | |
| trie insert / search | O(word length) | |
| subsets · permutations | O(2ⁿ · n) · O(n! · n) | the output alone is that big |
| recursion | extra O(depth) space | the call stack counts |

### What to say

- **Opening:** "Let me restate it… Can the input be empty? Can values be negative or repeated? How large is n?"
- **Brute force:** "The straightforward way is … which is O(…) because for every … we rescan …"
- **Optimisation:** "The brute force repeats …; if I keep … then each step is O(1), so O(n) overall."
- **Before coding:** "Here's the plan in four comments… does that sound right? Shall I code it?"
- **While coding:** name the invariant ("after this loop the window has no repeats") and point at the line where you record the answer.
- **Stuck on the optimal:** "I'll code the brute force first as a correct baseline, then optimise the line that repeats work."
- **Stuck on a detail:** "Let me try a smaller example by hand" is always allowed; thinking out loud earns hints.
- **Testing:** "Let me trace the example… now the empty case… now the case where …"
- **Out of time:** "The remaining piece is …; I'd do it by …"
- **Closing:** time, space, and one follow-up you would handle ("if the input were a stream, I would …").

### The night-before list

Pick the **five** templates you are least sure of. Write each from memory in a plain editor (interviews are typed, without autocomplete), under three minutes each, saying the invariant out loud:

1. Two Sum with a dict (ask the past, then join it)
2. Sliding window, longest and shortest versions
3. Binary search "first index where the condition is true", and binary search on the answer
4. Monotonic stack: next greater element
5. BFS on a grid with levels (multi-source start)
6. DFS flood fill (recursive and with an explicit stack)
7. Topological sort with indegrees
8. Union-find with path compression
9. Dijkstra with the stale-entry check
10. Top-k with a size-k min-heap
11. Merge intervals
12. Backtracking: subsets, permutations, combinations with duplicates
13. Tree DFS that returns one thing and records another (diameter)
14. Trie insert and search
15. LRU cache with a dict and a doubly linked list

### A 7-day plan with this repo

Practise in `practice/simple/`: 25 minutes per problem, in a plain editor, talking out loud, and run the code only when you think it is finished.

| Day | Read | Practise |
|---|---|---|
| 1 | Start Here, From Idea to Code, Python Toolkit, Arrays & Hashing, Prefix Sums | `01` – `05` |
| 2 | Two Pointers, Sliding Window, Strings | `06` – `12`, `50` |
| 3 | Stacks & Queues, Monotonic Stack, Binary Search, Linked Lists | `13` – `23`, `25` |
| 4 | Trees, Tries, Heaps | `26` – `35` |
| 5 | Graphs I – III | `41` – `47`; redo your two slowest |
| 6 | Intervals & Sweep Line, Greedy, Backtracking, Design Problems | `24`, `36` – `40`, `48`, `49`; one 45-minute mock where someone else picks from the A-Z finder |
| 7 (light) | these checklists; the bits part of Math, Bits & Geometry; skim Matrices and Sorting & Selection | `practice/simple/basics/bits/`; two timed problems from your miss list; the night-before list; stop early |

Two daily habits make the plan stick: **every morning, spend 10 minutes cold-writing yesterday's two hardest templates from their seven decisions**, and **put every miss on a list that you redo two days later**. If the decisions come back, the code will too.
