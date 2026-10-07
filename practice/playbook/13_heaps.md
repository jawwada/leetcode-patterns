## Heaps

> A heap is a pile that always hands you the smallest item first. It keeps only a *partial* order (every parent ≤ its children), which is exactly enough to read the minimum in O(1) and to add or remove an item in O(log n).

**Reach for it when** you need the smallest or largest item *again and again* while items keep arriving or leaving: **top k, k-th largest, k closest**, **merge k sorted** lists, the **median of a stream**, "always process the cheapest / earliest / most frequent next", scheduling with deadlines or cooldowns, or growing a frontier from its lowest point (Dijkstra-style).

**In this repo:** `heap/` (20 problems) · bank: `practice/simple/32_k_closest_points_to_origin.py`, `practice/simple/33_task_scheduler.py`, `practice/simple/34_find_median_from_data_stream.py`, `practice/simple/35_merge_k_sorted_lists.py` · basics: `practice/simple/basics/heaps/` (`01_heapify_by_hand.py`, `02_push_and_pop_by_hand.py`, `03_top_k_with_size_k_min_heap.py`, `04_max_heap_by_negation_and_tuples.py`, `05_kth_largest_in_a_stream.py`, `06_merge_k_sorted_arrays.py`), `practice/simple/basics/sorting/04_heap_sort.py`

### The picture

```text
the list:  [1, 3, 2, 7, 4, 9, 5]       node i has children 2i+1 and 2i+2, parent (i-1)//2

the tree:          1                   the only rule: every parent <= its children
                 /   \                 -> the smallest is always heap[0]
                3     2                -> nothing else is in order: heap[1] = 3 is not the
               / \   / \                  second smallest (2 is), heap[-1] = 5 is not the
              7   4 9   5                 largest (9 is)

push 0:  append it as the last leaf, then swap it UP while its parent is bigger
         [1, 3, 2, 7, 4, 9, 5, 0]  ->  0 passes 7, 3, 1  ->  [0, 1, 2, 3, 4, 9, 5, 7]
pop:     take heap[0], move the last leaf to the root, swap it DOWN toward its smaller child
         both walk a single root-to-leaf path: at most log2(n) swaps
```

**Why it is fast:** the brute-force answer to "give me the smallest" is a scan, O(n) every time you ask, or a full sort, O(n log n), most of whose order you never use. A heap keeps just enough order to answer one question (what is the smallest?) and repairs it along one path after each change: O(1) to peek, O(log n) to push or pop. Capped at k items, it answers "top k of n" in O(n log k) time and O(k) memory, even on a stream you can't store. `heapify` builds a heap from a whole list in O(n), not O(n log n): it sifts each parent *down*, and a node can only sink as far as its height. Half the nodes are leaves that don't move, a quarter sink at most one level, an eighth at most two, and that sum stays below n.

### heapq in one cell

Python's `heapq` works on a plain list, and its classic functions give you a **min**-heap. Everything else (max-heaps, priorities, ties) is done with what you push.

```python
h = []
for x in [5, 1, 2, 8]:
    heapq.heappush(h, x)                     # O(log n): append, then sift up
print(h, h[0])                               # [1, 5, 2, 8] 1   (only h[0] has a meaning)
print(heapq.heappop(h), h)                   # 1 [2, 5, 8]

nums = [4, 1, 7, 3]
heapq.heapify(nums)                          # O(n), in place, returns None
print(nums)                                  # [1, 3, 7, 4]

mx = [-x for x in [4, 1, 7, 3]]              # max-heap: store -x ...
heapq.heapify(mx)
print(-heapq.heappop(mx), -mx[0])            # 7 4   ... and negate on the way out

jobs = [(2, "write"), (1, "deploy"), (2, "test")]
heap = []
for order, (prio, name) in enumerate(jobs):
    heapq.heappush(heap, (prio, order, name))   # tuples compare left to right: order breaks ties
print([heapq.heappop(heap)[2] for _ in range(3)])   # ['deploy', 'write', 'test']

try:
    heapq.heappush([(1, {"id": 1})], (1, {"id": 2}))   # equal priorities -> Python compares the dicts
except TypeError as e:
    print("TypeError:", e)                   # '<' not supported between instances of 'dict' and 'dict'
print(heapq.nlargest(2, [4, 1, 7, 3]), heapq.nsmallest(2, [4, 1, 7, 3]))   # [7, 4] [1, 3]
print(list(heapq.merge([1, 4, 5], [1, 3, 4], [2, 6])))    # [1, 1, 2, 3, 4, 4, 5, 6]  (lazy k-way merge)
```

**Try it**
- Print `h[1]` and `sorted(h)[1]` right after the four pushes: 5 versus 2. Only `h[0]` is guaranteed; to read the k smallest in order, pop k times or sort.
- Push `(prio, name)` without `order`: it still runs (names are strings), but the tie now comes out alphabetically, `['deploy', 'test', 'write']`, not in arrival order.
- Push `(1, {"id": 1})` and then `(2, {"id": 2})` into an empty heap: no error. The dicts are only compared when two priorities tie, which is why this bug hides until the first tie.
- Predict, then run: `heapq.heappushpop([2, 5, 8], 0)` returns 0 (push first, so 0 comes straight back out) and `heapq.heapreplace([2, 5, 8], 0)` returns 2 (pop first, then push).

### From idea to code

**The idea in one sentence:** *keep the candidates in a heap keyed by "who should go next"; pop the best, deal with it, push any new candidates it creates; and when only the best k matter, let the heap throw out its weakest member whenever it holds k + 1.*

**Why a min-heap for the k *largest*?** Each newcomer asks one question: "am I better than the weakest of the k?" The weakest of the k largest is their *minimum*, so the minimum must sit on top. A max-heap of all n items would also work (pop k times), but it holds all n: O(n) memory, and useless for a stream.

| Decision | Keep the k best (215, 703, 973) | Next from a frontier (23, 632, 407) |
|---|---|---|
| **State / Definition** | `heap` = min-heap of the k largest so far; `heap[0]` = the weakest of them | `heap` = one candidate per source that could come next, e.g. `(value, list i, index j)` |
| **Invariant** | after the fix, the heap holds the k largest items seen so far (all of them while fewer than k have arrived) | every item not yet popped is in the heap or waits behind one (later in the same list), so the root is the next item overall |
| **Step** | push the newcomer | pop the root: it is the next item overall |
| **Fix** | `if len(heap) > k: heappop(heap)`: the weakest of k + 1 leaves, maybe the newcomer itself | push the popped item's successor: its list's next item, its unvisited neighbours |
| **Record** | `heap[0]` is the k-th largest (in Kth Largest in a Stream: `return heap[0]` at the end of `add`) | right after each pop, because pops come out in order (or when an item is first reached, if its value is final then: Trapping Rain Water II banks water at the push) |
| **Init** | `heap = []` | `heapify` one head per list, or the whole border, in O(n) |
| **Return** | the heap's items (in heap order: sort them if order matters) or `heap[0]` | the pops, or the value recorded when the target shows up; needing a pop from an empty heap means "impossible" (−1, `""`) |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "the smallest candidate" (just look) | `heap[0]` |
| "take the smallest out" | `heapq.heappop(heap)` |
| "add a candidate; ties go to the earlier one" | `heapq.heappush(heap, (key, i, item))` |
| "the largest instead" | push `-key`; the largest is `-heap[0]` |
| "keep only the k largest" | `heappush(heap, x)`, then `if len(heap) > k: heappop(heap)` |
| "the k-th largest so far" | `heap[0]` of that size-k min-heap |
| "push, then pop" / "pop, then push" (one call) | `heapq.heappushpop(heap, x)` / `heapq.heapreplace(heap, x)` |
| "the next item from the list I just used" | `if j + 1 < len(lists[i]): heappush(heap, (lists[i][j + 1], i, j + 1))` |

**Push first, then evict.** The heap compares the newcomer with the weakest of the k for you: if the newcomer is the weakest of the k + 1, it is the one that leaves. Evicting first throws out a kept item before anyone has checked that the newcomer is better. In the merge the order is pop, record, refill: only after the pop do you know which list needs a new head.

```python
def k_largest(nums, k):
    heap = []                                # STATE + INIT: min-heap of the k largest so far; heap[0] = the weakest
    for x in nums:
        heapq.heappush(heap, x)              # STEP: x joins the candidates
        if len(heap) > k:                    # FIX: k + 1 candidates, the weakest leaves (maybe x itself)
            heapq.heappop(heap)
    return sorted(heap, reverse=True)        # RETURN: the k largest, largest first


def merge_sorted(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]   # STATE + INIT: (value, list i, index j), one head per list
    heapq.heapify(heap)
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)      # STEP: the smallest head is the next item overall
        out.append(val)                      # RECORD: pops come out in sorted order
        if j + 1 < len(lists[i]):            # FIX: list i lost its head; its next item takes the seat
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out                               # RETURN


print(k_largest([3, 1, 5, 12, 2, 11], 3))            # [12, 11, 5]
print(merge_sorted([[1, 4, 5], [1, 3, 4], [2, 6]]))  # [1, 1, 2, 3, 4, 4, 5, 6]
```

**Try it**
- Change `if len(heap) > k:` to `>=` and rerun: `[12, 11]`. The heap is now capped at k − 1.
- Evict first: replace the two lines in the loop with `if len(heap) == k: heapq.heappop(heap)` followed by `heapq.heappush(heap, x)`. `k_largest([5, 1], 1)` returns `[1]`: the 5 was thrown out before anyone checked that 1 is worse.
- Print `heap` at the top of the `while` loop in `merge_sorted`: it never holds more than 3 entries, one per list. That is where O(N log k) comes from.
- Remove `if lst` from the first line of `merge_sorted` and call `merge_sorted([[], [2]])`: `IndexError`, because an empty list has no head.

### Watch it work

The trace runs the template's own two lines, push then evict, and says who left. Once the heap holds k items, its root is a doorman: a newcomer stays only if it beats the root, and then the root leaves.

```python
def trace_k_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)                                   # STEP
        gone = heapq.heappop(heap) if len(heap) > k else None     # FIX
        note = ("filling up" if gone is None else
                "bounced: x was the weakest" if gone == x else f"{gone} leaves")
        print(f"x={x:<3} heap={str(heap):<12} root={heap[0]:<3} {note}")


trace_k_largest([3, 1, 5, 12, 2, 11], 3)
```

**Try it**
- Run it with `k = 1`: the heap is a single "best so far", and the root only climbs (3, then 5, then 12).
- Run `[1, 2, 3, 4, 5]` and then `[5, 4, 3, 2, 1]` with `k = 2`: once the heap is full, every newcomer stays on the rising list and every newcomer bounces on the falling one. Same O(n log k) bound, very different traffic.
- Rewrite the FIX compare-first: `if len(heap) < k: heapq.heappush(heap, x)` / `elif x > heap[0]: heapq.heapreplace(heap, x)`. The `root` column is the same at every step, but a newcomer that can't beat the root never enters. (With `>=` there, `[5, 5, 5, 5]`, k = 2 swaps equal values in and out for nothing.)
- Read the `heap=` column: it need not be sorted (`[3, 12, 5]`), yet once the heap is full, `root` is always the k-th largest so far.

### Where it goes wrong

1. **Ties compare the payload.** `(dist, node)` raises `TypeError` the first time two distances are equal and the nodes can't be compared: that is the `{"id": ...}` error in the heapq cell. Push `(dist, i, node)` with a unique `i`, the list index or a running counter.
2. **Negating only half of the time.** Push `-x`, read `-heap[0]`, negate what you pop. In the median finder below, dropping the minus in step 2 (`heappush(self.high, heappop(self.low))`) makes `median()` return −5.0 after `add(5)`. A missing minus gives a silently wrong answer, never an error.
3. **The wrong heap for top-k.** k largest → *min*-heap capped at k; k smallest or k closest → *max*-heap capped at k. The other way round evicts your best items: `[3, 1, 5]`, k = 1, with a max-heap keeps 1.
4. **Changing a key that is already in the heap.** The heap never notices: `h = [[1, "a"], [2, "b"]]; h[1][0] = 0; heapq.heappop(h)` returns `[1, "a"]`. Push a fresh entry instead and skip the stale one when it surfaces (lazy deletion: right after a pop, ask "is this entry still valid?").
5. **Popping an empty heap.** `IndexError`. IPO below crashes on `max_capital(1, 0, [5], [1])` without its `if not heap: break`. An empty heap is often the "impossible" answer.
6. **`heappush` onto a list that is not a heap.** `heapq` never checks: `h = [5, 1]; heapq.heappush(h, 3)` leaves `h[0] == 3`, not 1. Call `heapify` once first.
7. **Using what `heapify` returns.** It works in place and returns `None`: `h = heapq.heapify([3, 1]); h[0]` raises `TypeError: 'NoneType' object is not subscriptable`.
8. **Two successors per pop.** In a grid of sorted sums (373, 378), pushing both `(i + 1, j)` and `(i, j + 1)` after every pop reaches the same cell twice: with `nums1 = nums2 = [1, 2]` and k = 5, the pair `[2, 2]` comes out twice. Seed one head per row and only move right, or keep a `seen` set.

### Edge cases to say out loud

k = 0 · k ≥ n · duplicates (they count separately) · empty lists among the k lists · all lists empty · equal keys with uncomparable payloads · negatives under negation · an even count for the median (average, as a float) · the heap running dry before you are done (impossible input).

```python
assert k_largest([5, 5, 5], 2) == [5, 5]                  # duplicates count separately
assert k_largest([2, 1], 5) == [2, 1]                     # k >= n: keep everything
assert k_largest([4, 1], 0) == []                         # k = 0: everything leaves again
assert k_largest([], 3) == []
assert k_largest([-1, -7, -3], 2) == [-1, -3]
assert merge_sorted([]) == [] and merge_sorted([[], []]) == []
assert merge_sorted([[1, 1], [1]]) == [1, 1, 1]           # equal heads: the list index breaks the tie
assert merge_sorted([[-3, 0], [-5], [7]]) == [-5, -3, 0, 7]
print("edge cases pass")
```

**Try it**
- Predict, then add: `assert k_largest([2, 9, 4], 3) == [9, 4, 2]` (k = n gives the input sorted, largest first).
- Why does `merge_sorted([[1, 1], [1]])` never compare anything but numbers? Print the heap after `heapify`: `[(1, 0, 0), (1, 1, 0)]`; the second field already differs.
- LeetCode 23 passes linked-list nodes: push `(node.val, i, node)` and refill with `node.next`. Drop the `i` and merge two lists whose heads are equal: `TypeError`, because Python then compares two `ListNode`s.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Keep the k best** | min-heap capped at k for the k largest; max-heap (negate) for the k smallest / closest; 1383 sorts by the bottleneck, then keeps the k best speeds | 215, 703, 973, 1383 |
| **Custom order** | strings can't be negated: a class with `__lt__` ("less" = worse), or heapify all `(-count, word)` and pop k | 692 |
| **Two heaps** | max-heap for the low half, min-heap for the high half; the median sits at the roots | 295, 480 |
| **Cooldown** | max-heap of counts + a FIFO queue (or one held item) of what can't be used yet | 621, 767, 358 |
| **K-way merge** | the template: one head per sorted list; pop the smallest, push its successor | 23, 355, 786 |
| **Two orders at once** | one heap of free rooms by id, one of busy rooms by end time | 2402 |
| **Shrink the max** | max-heap; only lowering the max can shrink max − min; track the min beside it | 1675 |
| *Stretch:* **unlock, then take the best** | sort by the unlock key, push everything unlocked, pop the best when you must choose | 502, 871, 1834 |
| *Stretch:* **take now, regret later** | take every item; when a limit breaks, pop the worst item you took | 630, 1642 |
| *Stretch:* **lazy deletion** | leave dead entries in; pop them only when they reach the top | 218, 480, 1851 |
| *Stretch:* **lowest frontier first** | heap of frontier cells keyed by level or distance (Dijkstra shape) | 407, 743 |
| *Stretch:* **merge + running max** | the range `[heap min, running max]` covers every list; advance the min | 632 |

**Keep k, mirror image.** For the k *closest*, cap a *max*-heap at k: its root is the farthest point you kept, and a newcomer stays only if it is closer. Words can't be negated, so Top K Frequent Words gives its entries a `__lt__` where "less" means "worse"; then the same push-and-evict loop works. (Simpler when k is small: heapify all `(-count, word)` and pop k times, O(m + k log m).)

```python
def k_closest(points, k):
    heap = []                                # STATE: max-heap via (-dist, x, y); root = the farthest kept
    for x, y in points:
        heapq.heappush(heap, (-(x * x + y * y), x, y))   # STEP: squared distance, same order, no sqrt
        if len(heap) > k:                    # FIX: the farthest of k + 1 leaves
            heapq.heappop(heap)
    return sorted([x, y] for _, x, y in heap)            # RETURN (sorted only for a stable printout)


class Entry:                                 # "less" means "worse": fewer copies, or same count and later word
    def __init__(self, count, word):
        self.count, self.word = count, word

    def __lt__(self, other):
        if self.count != other.count:
            return self.count < other.count
        return self.word > other.word


def top_k_words(words, k):
    heap = []                                # STATE: min-heap of the k best words; root = the worst kept
    for word, count in Counter(words).items():
        heapq.heappush(heap, Entry(count, word))         # STEP
        if len(heap) > k:                    # FIX: the worst of k + 1 leaves
            heapq.heappop(heap)
    return [e.word for e in sorted(heap, reverse=True)]  # RETURN: best first


print(k_closest([[3, 3], [5, -1], [-2, 4]], 2))                            # [[-2, 4], [3, 3]]
print(top_k_words(["i", "love", "leetcode", "i", "love", "coding"], 2))    # ['i', 'love']
```

**Try it**
- Drop the minus in `k_closest` (push `(x * x + y * y, x, y)`): you get the 2 *farthest* points, `[[-2, 4], [5, -1]]`, because the root is now the closest point and it is the one evicted.
- Run `top_k_words(["b", "a", "b", "a"], 1)`: `['a']`. Both words appear twice, and on a tie the later word, `'b'`, is the "worse" one at the root.
- Flip the tie rule in `__lt__` to `self.word < other.word` and rerun that call: `['b']`, the wrong word. The root must be the word you would throw out first.
- `k_closest([[1, 1]], 5)` returns `[[1, 1]]`: the cap is simply never reached.

**Two heaps (running median).** The median lives at the seam between the smaller half and the larger half. Keep the smaller half in a max-heap and the larger half in a min-heap, and the middle numbers sit at the two roots.

```text
   low (max-heap, stored negated)        high (min-heap)
   1   3   [5]          |                [15]   20
             ^ largest small number       ^ smallest large number
   invariant: every low <= every high, and len(low) is len(high) or len(high) + 1
   median: -low[0] when the count is odd (here 5), else the mean of the two roots
```

```python
class MedianFinder:
    def __init__(self):
        self.low = []                        # STATE: max-heap (stored negated), the smaller half
        self.high = []                       # STATE: min-heap, the larger half

    def add(self, x):
        heapq.heappush(self.low, -x)                         # STEP: 1. x joins the small half
        heapq.heappush(self.high, -heapq.heappop(self.low))  # FIX: 2. the largest small crosses the seam
        if len(self.high) > len(self.low):                   # FIX: 3. keep len(low) >= len(high)
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):   # RETURN: odd count, the extra number sits in low
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2    # RETURN: even count, the mean of the roots


mf, medians = MedianFinder(), []
for x in [5, 15, 1, 3]:
    mf.add(x)
    medians.append(mf.median())
print(medians)                               # [5.0, 10.0, 5.0, 4.0]
```

**Try it**
- After each `add`, print `sorted(-v for v in mf.low)` and `sorted(mf.high)`: `[5] []`, `[5] [15]`, `[1, 5] [15]`, `[1, 3] [5, 15]`. Every small number is at most every large one.
- Delete step 3 and rerun: the very first `median()` raises `IndexError`. Step 2 moved the 5 into `high`, and `low` is empty.
- On a fresh `MedianFinder()`, change `/ 2` to `// 2` and add 1, then 2: the median prints `1` instead of `1.5`.
- Predict the medians for `[5, 4, 3, 2, 1]` before running: `[5.0, 4.5, 4.0, 3.5, 3.0]`.

**Cooldown: heap + queue (Task Scheduler, Reorganize String).** Always run the ready task with the most copies left: it is the one that would otherwise force idle ticks at the end. A task that just ran waits n ticks on a FIFO "conveyor belt"; tasks leave the belt in the order they got on, so only its front needs checking. The release comes *after* the run: a task whose cooldown ends with this tick may run from the next tick on. Reorganize String is the same machine with a cooldown of one turn, so the belt shrinks to a single `held` letter, pushed back only after the next letter has been chosen.

```python
def least_interval(tasks, n):
    heap = [-c for c in Counter(tasks).values()]   # STATE: -copies left of the tasks ready now (max-heap)
    heapq.heapify(heap)
    cooling = deque()                        # STATE: (tick its cooldown ends, -copies left), oldest first
    time = 0                                 # INIT  (every task with copies left is in exactly one of the two)
    while heap or cooling:
        time += 1                            # one tick
        if heap:
            left = heapq.heappop(heap) + 1   # STEP: run the top (stored negated: +1 means one copy fewer)
            if left:                         # copies remain: it cools down for n ticks
                cooling.append((time + n, left))
        else:
            time = cooling[0][0]             # nothing is ready: skip the idle ticks at once
        if cooling and cooling[0][0] == time:     # FIX: the front's cooldown ends with this tick
            heapq.heappush(heap, cooling.popleft()[1])
    return time                              # RETURN


def reorganize(s):                           # 767: no two equal letters side by side
    heap = [(-c, ch) for ch, c in Counter(s).items()]   # STATE: max-heap of copies left
    heapq.heapify(heap)
    out, held = [], None                     # STATE: held = the letter just placed, sitting out one turn
    while heap:
        c, ch = heapq.heappop(heap)          # STEP: most copies left among the allowed letters
        out.append(ch)
        if held:
            heapq.heappush(heap, held)       # FIX: last turn's letter may be used again
        held = (c + 1, ch) if c + 1 < 0 else None
    return "" if held else "".join(out)      # RETURN: a letter still waiting would have to repeat


print(least_interval(["A", "A", "A", "B", "B", "B"], 2))   # 8   (A B _ A B _ A B)
print(least_interval(["A", "A", "A", "A", "B", "C"], 2))   # 10  (A B C A _ _ A _ _ A)
print(reorganize("aab"), repr(reorganize("aaab")), reorganize("aaabb"))   # aba '' ababa
```

**Try it**
- Change `(time + n, left)` to `(time + n - 1, left)`: the first call prints 6 instead of 8. Off by one on the ready time silently shrinks the cooldown to n − 1.
- Delete the `else` branch: the answers stay the same, but `least_interval(["A", "A"], 10**6)` now loops a million times; with the jump it returns 1000002 after three loops.
- Check the first call against the counting formula `(most - 1) * (n + 1) + ties` (`most` = the top count, `ties` = how many tasks have it): (3 − 1) × 3 + 2 = 8. The formula needs a `max(len(tasks), ...)` guard; the simulation does not.
- In `reorganize`, push the letter straight back instead of holding it (`heapq.heappush(heap, (c + 1, ch))` right after placing it, when copies remain): `"aab"` comes out as `"aab"`.

#### Stretch: hard heap patterns

The four patterns below are Hard problems built from the same two templates. Learn the core above first; come back here once those feel automatic.

**Greedy + heap: unlock, then take the best; or take now, regret later.** Sort by the key that *unlocks* options (capital, position, deadline), sweep, push each unlocked option into a heap keyed by its *value*, and pop only when you must choose, or when you must undo a choice. In the refuelling loop the FIX comes before the STEP: you may only take fuel from stations you have actually reached.

```python
def max_capital(k, w, profits, capital):                 # IPO (502)
    projects = sorted(zip(capital, profits))             # INIT: unlock order, cheapest first
    heap, i = [], 0                                      # STATE: max-heap (negated) of affordable profits
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w: # FIX: heap = every affordable, unused project
            heapq.heappush(heap, -projects[i][1])
            i += 1
        if not heap:                                     # nothing affordable, now or ever
            break
        w += -heapq.heappop(heap)                        # STEP: do the most profitable one
    return w                                             # RETURN


def min_refuel_stops(target, fuel, stations):            # (871) fuel = how far we can drive
    passed, stops = [], 0                                # STATE: max-heap (negated) of fuel we drove past
    for pos, gas in stations + [[target, 0]]:            # the target is the last "station"
        while fuel < pos:                                # FIX: stuck before pos, refuel retroactively
            if not passed:
                return -1                                # RETURN: nothing left to take
            fuel += -heapq.heappop(passed)               # the biggest station behind us
            stops += 1                                   # RECORD
        heapq.heappush(passed, -gas)                     # STEP: we reached pos, its fuel is an option
    return stops                                         # RETURN


def schedule_course(courses):                            # (630) courses = [duration, last_day]
    taken, time = [], 0                                  # STATE: max-heap (negated) of taken durations; time = their sum
    for duration, last_day in sorted(courses, key=lambda c: c[1]):   # INIT: by deadline
        heapq.heappush(taken, -duration)                 # STEP: take it now ...
        time += duration
        if time > last_day:                              # FIX: ... regret, drop the LONGEST course taken
            longest = -heapq.heappop(taken)
            time -= longest
    return len(taken)                                    # RETURN


print(max_capital(2, 0, [1, 2, 3], [0, 1, 1]))                                 # 4
print(min_refuel_stops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]))     # 2
print(schedule_course([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]))  # 3
```

**Try it**
- In `min_refuel_stops`, move `heapq.heappush(passed, -gas)` *above* the `while` loop and run `min_refuel_stops(100, 1, [[10, 100]])`: 1 instead of −1. The car refuelled at a station it never reached.
- In `schedule_course`, drop the *shortest* course instead (push `duration` without the minus, pop the root): `schedule_course([[5, 5], [4, 6], [2, 6]])` gives 1 instead of 2. Dropping the longest frees the most time.
- Remove the `if not heap: break` from `max_capital` and run `max_capital(1, 0, [5], [1])`: `IndexError`, since nothing is affordable with 0 capital.
- Print `-passed[0]` each time a stop is taken in the 100-mile example: 60, then 40. The decision is postponed until the car would run dry, and then it is easy.

**Lazy deletion (the skyline).** A heap can't remove an item from its middle. Lazy deletion says you don't have to: leave the dead entry in and throw it away when it reaches the top, because the top is the only thing you ever read. That is also why the FIX must run before the RECORD reads the top.

```text
 15           +-----------+              buildings [2,9,10] [3,7,15] [5,12,12]
 12           |           +--------------+
 10        +--+                          |        sweep the edges left to right;
  0  ------+                             +-----   live = max-heap of (height, right end)
           2  3           7              12       key point = where the top height changes
```

```python
def skyline(buildings):
    events = sorted([(l, -h, r) for l, r, h in buildings] +    # INIT: left edge (x, -height, right);
                    [(r, 0, 0) for l, r, h in buildings])      #   a right edge sorts after lefts at x
    live = [(0, math.inf)]                   # STATE: max-heap of (-height, right); the ground never ends
    points = []
    for x, neg_h, right in events:
        while live[0][1] <= x:               # FIX: the tallest has already ended, delete it now
            heapq.heappop(live)
        if neg_h:                            # STEP: a left edge, this building goes live
            heapq.heappush(live, (neg_h, right))
        height = -live[0][0]
        if not points or points[-1][1] != height:   # RECORD: the outline changes here
            points.append([x, height])
    return points                            # RETURN


print(skyline([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]))
# [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]
```

**Try it**
- Change `<=` to `<` in the `while` and run `skyline([[0, 2, 3], [2, 4, 1]])`: `[[0, 3], [4, 1]]` instead of `[[0, 3], [2, 1], [4, 0]]`. A building that ends at x does not cover x.
- Remove the `points[-1][1] != height` test (append on every event): the output gains repeats like `[5, 15]` and `[9, 12]`, points where the height did not change.
- Print `x, sorted(live)` right after the `while`: at x = 9 the building `[2, 9, 10]` has ended, yet `(-10, 9)` is still in the heap under the taller `(-12, 12)`. It is harmless there, and it is popped at x = 12 when it surfaces.

**Lowest frontier first (Trapping Rain Water II).** Water in a cell can rise only as high as the lowest wall on its best escape route to the border. Start with the border as the wall, always breach the wall at its *lowest* cell, and let the neighbour behind it fill up to that level and join the wall. It is Dijkstra with `max` in place of `+` ([Graphs III](#s19)).

```text
heights            level the water reaches     trapped = level - height
1 4 3 1 3 2        1 4 3 1 3 2                 . . . . . .
3 2 1 3 2 4   ->   3 3 3 3 3 4          ->     . 1 2 0 1 .      total 4
2 3 3 2 3 1        2 3 3 2 3 1                 . . . . . .
```

```python
def trap_rain_water(height):
    m, n = len(height), len(height[0])
    wall = [(height[r][c], r, c) for r in range(m) for c in range(n)
            if r in (0, m - 1) or c in (0, n - 1)]   # STATE + INIT: (level, r, c) of the wall, the border first
    heapq.heapify(wall)
    seen = {(r, c) for _, r, c in wall}      # STATE: cells already in the wall (or retired)
    water = 0
    while wall:
        level, r, c = heapq.heappop(wall)    # STEP: the wall's lowest cell, water escapes here first
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))           # mark when pushing, as in BFS
                water += max(0, level - height[nr][nc])                    # RECORD: it fills up to level
                heapq.heappush(wall, (max(level, height[nr][nc]), nr, nc)) # FIX: then it joins the wall
    return water                             # RETURN


print(trap_rain_water([[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]))   # 4
print(trap_rain_water([[3, 3, 3, 3, 3], [3, 2, 2, 2, 3], [3, 2, 1, 2, 3],
                       [3, 2, 2, 2, 3], [3, 3, 3, 3, 3]]))                          # 10
```

**Try it**
- Push the neighbour's own height instead of `max(level, height[nr][nc])`: the second grid gives 2 instead of 10. A cell that just filled up rejoins the wall at its low floor height, so its neighbours are filled from that "hole" instead of from the real wall.
- Replace the heap with a FIFO queue (`deque`, `popleft`, `append`): the first grid gives 5 instead of 4. Without "lowest first", a cell gets filled from a wall that is not its real bottleneck.
- Print `level, r, c` for each pop on the first grid: the levels never go down. That monotone order is what makes each cell's level final when it is first reached.
- A grid with fewer than 3 rows or columns has no inside: `trap_rain_water([[5, 1, 5]])` is 0.

**Merge + running max (smallest range covering k lists).** Put one finger on each sorted list. The fingered values cover every list, and they span `[min, max]`. The only way to shrink that range is to raise the min, and only the finger *on* the min can do it: advance it, update the running max, and stop when some list runs out.

```python
def smallest_range(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]   # STATE + INIT: one finger (value, list, index) per list
    heapq.heapify(heap)
    hi = max(lst[0] for lst in lists)        # STATE: the rightmost finger (a running max)
    best = [-math.inf, math.inf]
    while True:
        lo, i, j = heapq.heappop(heap)       # STEP: the leftmost finger
        if hi - lo < best[1] - best[0]:      # RECORD before moving it (< keeps the earliest start)
            best = [lo, hi]
        if j + 1 == len(lists[i]):           # list i is used up: no later range covers it
            return best                      # RETURN
        nxt = lists[i][j + 1]
        hi = max(hi, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))    # FIX: list i gets its next finger


print(smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]))   # [20, 24]
print(smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))                        # [1, 1]
```

**Try it**
- Move the "used up" check above the RECORD lines and run `smallest_range([[1], [2], [3]])`: `[-inf, inf]` instead of `[1, 3]`. The last range was never recorded.
- Change `<` to `<=` and run `smallest_range([[1, 3], [2, 4]])`: `[3, 4]` instead of `[1, 2]`. Equal widths must keep the earliest start.
- Delete `hi = max(hi, nxt)`: the first example returns `[20, 5]`, an upside-down "range". `hi` froze at the first fingers' maximum; the right end must follow every new finger.

### Say it in the interview

> "Sorting everything costs O(n log n) and orders items I'm going to throw away. I only need the k best, so I keep a min-heap capped at k: its root is the weakest of my k, and every newcomer only has to beat that root. Anything that leaves was beaten by k numbers still in the heap, so it can't be in the top k. Each step is O(log k): O(n log k) time, O(k) space, and it works on a stream. For k sorted lists I keep one head per list: every pop is the next item overall, O(N log k)."

While coding, point at the `if len(heap) > k` line and say the invariant: "after this line the heap holds exactly the k largest so far, and `heap[0]` is the k-th largest". In a merge, point at the refill right after the pop: "the list I just took from gets its next item in, so every list always has its head in the heap". And say why the tuple has an index in the middle: "so ties never compare the payload". Likely follow-ups and your answers:

- *Faster?* → quickselect: O(n) on average, but it needs all the data in memory ([Sorting & Selection](#s23)).
- *k is close to n?* → keep the n − k smallest in a max-heap instead, or heapify everything and pop k times: O(n + k log n).
- *Sorted output?* → pop the k items: O(k log k).
- *Ties or a custom order?* → tuple keys, or a class with `__lt__`.
- *Priorities change?* → push a fresh entry and skip stale ones when they are popped.
- *The data is spread over many machines?* → top k on each machine, then a k-way merge of those lists.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Course Schedule III | `heap/course_schedule_iii.py` | sort by deadline, take every course; past the deadline, drop the longest taken (max-heap) |
| Design Twitter | `heap/design_twitter.py` | each user's tweets are already sorted by time: the feed is a k-way merge, stopped after 10 pops |
| Find Median from Data Stream | `heap/find_median_from_data_stream.py` · `practice/simple/34_find_median_from_data_stream.py` | max-heap of the low half, min-heap of the high half, sizes within 1; the median sits at the roots |
| IPO | `heap/ipo.py` | sort by capital; push newly affordable profits into a max-heap; take the top k times |
| K Closest Points to Origin | `heap/k_closest_points_to_origin.py` · `practice/simple/32_k_closest_points_to_origin.py` | max-heap capped at k on squared distance; the root is the farthest point kept |
| Kth Largest Element in a Stream | `heap/kth_largest_element_in_a_stream.py` | min-heap capped at k; its root is the k-th largest after every add |
| Kth Largest Element in an Array | `heap/kth_largest_element_in_an_array.py` | min-heap capped at k for O(n log k), or quickselect toward index n − k for O(n) average |
| K-th Smallest Prime Fraction | `heap/kth_smallest_prime_fraction.py` | each numerator is a sorted row of fractions: k-way merge, pop k − 1 times |
| Maximum Performance of a Team | `heap/maximum_performance_of_a_team.py` | sort by efficiency, high first (it is the current minimum); min-heap of the k best speeds with a running sum |
| Meeting Rooms III | `heap/meeting_rooms_iii.py` | two heaps: free room ids, busy (end, room); free ended rooms first; a delayed meeting keeps its length |
| Merge k Sorted Lists | `heap/merge_k_sorted_lists.py` · `practice/simple/35_merge_k_sorted_lists.py` | heap of the k heads as (val, i, node); pop the smallest, push its next |
| Minimize Deviation in Array | `heap/minimize_deviation_in_array.py` | double every odd so only halving is left; halve the max (max-heap) and track the min; stop at an odd max |
| Minimum Number of Refueling Stops | `heap/minimum_number_of_refueling_stops.py` | drive past stations into a max-heap; when stuck, retroactively take the biggest |
| Rearrange String k Distance Apart | `heap/rearrange_string_k_distance_apart.py` | max-heap by count + FIFO cooldown queue of length k; an empty heap mid-way means impossible |
| Reorganize String | `heap/reorganize_string.py` | possible iff top count ≤ (n + 1) // 2; place the most frequent letter, holding the last one out a turn |
| Smallest Range Covering Elements from K Lists | `heap/smallest_range_covering_elements_from_k_lists.py` | one finger per list: heap gives the min, a running max the max; advance the min until a list runs out |
| Task Scheduler | `heap/task_scheduler.py` · `practice/simple/33_task_scheduler.py` | run the ready task with most copies left (max-heap); park it in a FIFO cooldown queue |
| The Skyline Problem | `heap/the_skyline_problem.py` | sweep the edges; max-heap of live (height, right) with lazy deletion; emit when the top height changes |
| Top K Frequent Words | `heap/top_k_frequent_words.py` | size-k heap whose root is the worst word (`__lt__`: fewer copies, or later word); or heapify (−count, word), pop k |
| Trapping Rain Water II | `heap/trapping_rain_water_ii.py` | the border is a wall; breach its lowest cell (min-heap); neighbours fill to that level and join the wall |

### Self-check

1. You want the 10 largest numbers of a stream of a billion. Which heap, which size, and what does its root mean?
<details><summary>Answer</summary>A min-heap capped at 10. Its root is the smallest of the 10 largest seen so far (the 10th largest), so a new number stays only if it beats the root, and then the root is popped. O(log 10) per number and O(10) memory.</details>

2. Why does the keep-k template push first and evict second?
<details><summary>Answer</summary>After the push the heap holds k + 1 candidates, and popping removes the weakest of all of them, which may be the newcomer itself. Evicting first removes a kept item before the newcomer has been compared with anything: <code>k_largest([5, 1], 1)</code> would keep 1.</details>

3. `heapq.heappush(heap, (dist, node))` works on small tests and then crashes with `TypeError`. Why, and what is the fix?
<details><summary>Answer</summary>When two distances are equal, Python compares the next tuple field, the nodes, and they don't support <code>&lt;</code>. Put a unique tie-breaker before the payload: <code>(dist, i, node)</code> with a list index or a running counter.</details>

4. In the median finder, why does every number go into `low` first and then move `low`'s maximum to `high`?
<details><summary>Answer</summary>That two-step dance keeps the ordering rule without any comparisons of your own: whatever crosses the seam is the largest of the small half (including the new number), so every number in <code>low</code> stays at most every number in <code>high</code>. Step 3 then fixes only the sizes.</details>
