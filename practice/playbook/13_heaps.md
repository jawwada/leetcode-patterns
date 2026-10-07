## Heaps

> A heap is a pile that always hands you the smallest item first. It keeps only a *partial* order, every parent at most its children, which is exactly enough to read the minimum in O(1) and to add or remove an item in O(log n).

**Reach for it when** you need the smallest or largest item *again and again* while items keep arriving or leaving: **top k, k-th largest, k closest**, **merge k sorted** lists, the **median of a stream**, "always process the cheapest / earliest / most frequent next", scheduling with deadlines or cooldowns, or growing a frontier from its lowest point, which is the shape of Dijkstra's algorithm in [Graphs III](#s19).

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

Ask a plain list for its smallest item and it scans everything, O(n), every time you ask. Sort the list first and you pay O(n log n) for an order you mostly never use. A heap keeps just enough order to answer one question, "what is the smallest?", and repairs that order along a single root-to-leaf path after each change: O(1) to peek, O(log n) to push or pop.

Capped at k items, a heap answers "the top k of n" in O(n log k) time and O(k) memory, even on a stream too big to store.

`heapify` builds a heap from a whole list in O(n), not O(n log n). It sifts each parent *down*, and a node can only sink as far as its height: half the nodes are leaves that never move, a quarter sink at most one level, an eighth at most two, and that sum stays below n.

Python's `heapq` keeps a min-heap in a plain list, and [Python Toolkit](#s02) already shows its everyday calls: push, pop, `heapify`, `nlargest`, negation for a max-heap, and a counter in the tuple so that a tie never compares the payload. Three more calls earn their place in this section. `heappushpop` pushes and then pops in a single sift, `heapreplace` pops first and then pushes, and `merge` is a ready-made, lazy k-way merge of sorted lists, the second template below.

```python
h = [2, 5, 8]
print(heapq.heappushpop(h, 0), h)                        # 0 [2, 5, 8]  push, then pop
h = [2, 5, 8]
print(heapq.heapreplace(h, 0), h)                        # 2 [0, 5, 8]  pop, then push
print(list(heapq.merge([1, 4, 5], [1, 3, 4], [2, 6])))   # [1, 1, 2, 3, 4, 4, 5, 6]
```

**Try it**
- Run `heapq.heappushpop(h, 9)` on a fresh `h = [2, 5, 8]`: it returns 2 and leaves `[5, 9, 8]`. The newcomer stays and the weakest leaves, which is the keep-k template below in one call.
- Call `heapq.heapreplace([], 1)`: `IndexError`, because it pops before it pushes. `heapq.heappushpop([], 1)` returns 1, because it pushes first.
- Feed `merge` a list that is not sorted: `list(heapq.merge([3, 1], [2]))` gives `[2, 3, 1]`. It trusts every input to be sorted and never checks.
- Replace `list(...)` with `next(...)` in the last line: it prints 1. `merge` hands out one item per request, so it also merges streams too long to hold.

### From idea to code

*Keep the candidates in a heap keyed by "who should go next"; pop the best, deal with it, push any new candidates it creates; and when only the best k matter, let the heap throw out its weakest member whenever it holds k + 1.*

Start with the question the k *largest* raise: why a *min*-heap? Each newcomer asks one thing, "am I better than the weakest of the k?" The weakest of the k largest is their minimum, so the minimum must sit on top, and a min-heap puts it there. A max-heap of all n items would also work, popped k times, but it holds all n: O(n) memory, and useless on a stream. When the largest must sit on top instead, push `-key` and read `-heap[0]`.

Two templates cover the whole section. The first keeps the k best, as in Kth Largest Element in an Array, the k-th largest value of a list, in Kth Largest Element in a Stream, the same after every `add`, and in K Closest Points to Origin, the k points nearest the origin.

Its **State** is a min-heap of the k largest items seen so far, and its **Definition** gives the root its meaning: `heap[0]` is the weakest of them. The **Invariant**, true after every step, is that the heap holds exactly the k largest items seen so far, or all of them while fewer than k have arrived. A **Step** pushes the newcomer; if that makes k + 1, the **Fix** pops the weakest of them, which may be the newcomer itself.

The **Record** is the root: after the fix, `heap[0]` is the k-th largest so far, which is exactly what Kth Largest Element in a Stream returns at the end of each `add`. The **Init** is an empty heap. The **Return** is the root, or the heap's items, sorted first when order matters, because a heap keeps only a partial order.

The second template takes the next item from a frontier, as in Merge k Sorted Lists, which merges k sorted lists into one. Its state is one candidate per source, for a merge the tuple `(value, list i, index j)`, so that the root is the next item overall. The invariant is that every item not yet popped is in the heap or waits behind one in its own list.

A step pops the root and records it at once, because pops come out in sorted order. The fix pushes the popped item's successor, the next item of the same list, and the invariant holds again. Init is `heapify` on one head per list, in O(n). The return is the sequence of pops, or the value recorded when the target shows up; a pop needed from an empty heap means the input was impossible, −1 or `""`.

The same loop drives two Hard problems at the end of the section: one finger per list finds the smallest range that covers k lists, and a wall that starts at the border measures the water a height map traps. The flood records earlier, at the push, because a cell's level is final the moment it is first reached.

The order of the two lines is a decision too. Push first, then evict: the heap compares the newcomer with the weakest of the k for you, and if the newcomer is the weakest of the k + 1, it is the one that leaves. Evict first and you throw out a kept item before anyone has checked that the newcomer is better. In the merge the order is pop, record, refill, because only after the pop do you know which list needs a new head.

The cell below holds both templates. `k_largest` returns the k largest numbers of a list, largest first: `[3, 1, 5, 12, 2, 11]` with k = 3 gives `[12, 11, 5]`. `merge_sorted` is a k-way merge, which merges k sorted lists into one sorted list by always taking the smallest head: `[[1, 4, 5], [1, 3, 4], [2, 6]]` becomes `[1, 1, 2, 3, 4, 4, 5, 6]`. The list index sits in the middle of each tuple so that equal values never compare the payload.

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

The trace runs the template's own two lines, push then evict, and says who left at each step. Once the heap holds k items its root is a doorman: a newcomer stays only if it beats the root, and then the root leaves. Watch `[3, 1, 5, 12, 2, 11]` with k = 3 fill up for three steps and then bounce or admit each newcomer.

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
- Rewrite the FIX compare-first: `if len(heap) < k: heapq.heappush(heap, x)` / `elif x > heap[0]: heapq.heapreplace(heap, x)`. The `root` column is the same at every step, but a newcomer that can't beat the root never enters. With `>=` in place of `>`, `[5, 5, 5, 5]` and k = 2 swap equal values in and out for nothing.
- Read the `heap=` column: it need not be sorted (`[3, 12, 5]`), yet once the heap is full, `root` is always the k-th largest so far.

### Where it goes wrong

The heap's rules are few, so nearly every bug is one of these eight.

1. **Ties compare the payload.** `(dist, node)` raises `TypeError` the first time two distances are equal and the nodes can't be compared: `heapq.heappush([(1, {"id": 1})], (1, {"id": 2}))` crashes on the two dicts, as the two `Job`s crash in [Python Toolkit](#s02). Push `(dist, i, node)` with a unique `i`, the list index or a running counter.
2. **Negating only half of the time.** Push `-x`, read `-heap[0]`, negate what you pop. In the median finder below, dropping the minus in step 2 (`heappush(self.high, heappop(self.low))`) makes `median()` return −5.0 after `add(5)`. A missing minus gives a silently wrong answer, never an error.
3. **The wrong heap for top-k.** k largest → *min*-heap capped at k; k smallest or k closest → *max*-heap capped at k. The other way round evicts your best items: `[3, 1, 5]`, k = 1, with a max-heap keeps 1.
4. **Changing a key that is already in the heap.** The heap never notices: `h = [[1, "a"], [2, "b"]]; h[1][0] = 0; heapq.heappop(h)` returns `[1, "a"]`. Push a fresh entry instead and skip the stale one when it surfaces: that is lazy deletion, which asks right after each pop whether the entry is still valid.
5. **Popping an empty heap.** `IndexError`. IPO, which picks the most profitable projects the capital can afford, crashes below on `max_capital(1, 0, [5], [1])` without its `if not heap: break`. An empty heap is often the "impossible" answer.
6. **`heappush` onto a list that is not a heap.** `heapq` never checks: `h = [5, 1]; heapq.heappush(h, 3)` leaves `h[0] == 3`, not 1. Call `heapify` once first.
7. **Using what `heapify` returns.** It works in place and returns `None`: `h = heapq.heapify([3, 1]); h[0]` raises `TypeError: 'NoneType' object is not subscriptable`.
8. **Two successors per pop.** Find K Pairs with Smallest Sums (373), the k pairs with the smallest sums from two sorted lists, and Kth Smallest Element in a Sorted Matrix (378), whose rows and columns are sorted, both walk a grid of sorted values. Pushing both `(i + 1, j)` and `(i, j + 1)` after every pop reaches the same cell twice: with `nums1 = nums2 = [1, 2]` and k = 5, the pair `[2, 2]` comes out twice. Seed one head per row and only move right, or keep a `seen` set.

### Edge cases to say out loud

k = 0 · k ≥ n · duplicates (they count separately) · empty lists among the k lists · all lists empty · equal keys with uncomparable payloads · negatives under negation · an even count for the median (average, as a float) · the heap running dry before you are done (impossible input). The cell checks the cases that apply to the two templates.

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
- Merge k Sorted Lists (23) passes linked-list nodes: push `(node.val, i, node)` and refill with `node.next`. Drop the `i` and merge two lists whose heads are equal: `TypeError`, because Python then compares two `ListNode`s.

### Variations

Every variation keeps one of the two loops, push-and-evict or pop-and-refill, and changes one thing: the key, the number of heaps, or what waits beside the heap.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Keep the k best** | min-heap capped at k for the k largest; max-heap, negated, for the k smallest or closest; Maximum Performance of a Team, which picks at most k engineers to maximise speed sum × minimum efficiency, sorts by efficiency and keeps the k best speeds | Kth Largest Element in an Array (215), Kth Largest Element in a Stream (703), K Closest Points to Origin (973), Maximum Performance of a Team (1383) |
| **Custom order** | strings can't be negated: a class with `__lt__` where "less" means "worse", or heapify all `(-count, word)` and pop k | Top K Frequent Words (692): the k most frequent words, ties alphabetical |
| **Two heaps** | max-heap for the low half, min-heap for the high half; the median sits at the roots | Find Median from Data Stream (295): the median after every new number; Sliding Window Median (480): the median of every window of k numbers, in [Sliding Window](#s06) |
| **Cooldown** | max-heap of counts plus a FIFO queue, or one held item, of what can't be used yet; Rearrange String k Distance Apart wants equal letters at least k apart, so its queue has length k | Task Scheduler (621): the least time to run tasks with a cooldown; Reorganize String (767): no two equal letters side by side; Rearrange String k Distance Apart (358) |
| **K-way merge** | the template: one head per sorted list, pop the smallest, push its successor; Design Twitter's news feed merges the followed users' tweet lists, newest first, and stops after 10 pops; K-th Smallest Prime Fraction merges the sorted rows of fractions arr[i] / arr[j] | Merge k Sorted Lists (23), Design Twitter (355), K-th Smallest Prime Fraction (786) |
| **Two orders at once** | Meeting Rooms III gives each meeting the lowest free room, or delays it until one frees up: one heap of free rooms by id, one of busy rooms by end time | Meeting Rooms III (2402) |
| **Shrink the max** | Minimize Deviation in Array may halve evens and double odds to shrink max − min: a max-heap, since only lowering the max can shrink the gap, with the min tracked beside it | Minimize Deviation in Array (1675) |
| *Second pass:* **unlock, then take the best** | sort by the unlock key, push everything unlocked, pop the best when you must choose | IPO (502); Minimum Number of Refueling Stops (871): the fewest stops on the way to a target; Single-Threaded CPU (1834): the order in which one CPU runs its tasks, always the shortest one that has arrived |
| *Second pass:* **take now, regret later** | take every item; when a limit breaks, pop the worst item you took | Course Schedule III (630): the most courses that meet their deadlines; Furthest Building You Can Reach (1642): how far a fixed stock of bricks and ladders carries you up a row of buildings |
| *Second pass:* **lazy deletion** | leave dead entries in; pop them only when they reach the top | The Skyline Problem (218): the outline of a row of buildings; Sliding Window Median (480); Minimum Interval to Include Each Query (1851): the smallest interval holding each query point, in [Intervals & Sweep Line](#s14) |
| *Second pass:* **lowest frontier first** | heap of frontier cells keyed by level or distance, the Dijkstra shape | Trapping Rain Water II (407): the water a 2-D height map holds; Network Delay Time (743): how long a signal takes to reach every node, in [Graphs III](#s19) |
| *Second pass:* **merge + running max** | the range `[heap min, running max]` covers every list; advance the min | Smallest Range Covering Elements from K Lists (632): the shortest range holding a number of every list |

The template kept the k largest; the k *closest* are its mirror image. K Closest Points to Origin asks for the k points nearest the origin, so `[[1, 3], [-2, 2]]` with k = 1 gives `[[-2, 2]]`. Cap a *max*-heap at k: its root is the farthest point you kept, and a newcomer stays only if it is closer. Squared distances keep the order of distances, so no square root is needed.

Top K Frequent Words asks for the k most frequent words, ties broken alphabetically: `["i", "love", "leetcode", "i", "love", "coding"]` with k = 2 gives `["i", "love"]`. Words cannot be negated, so each entry gets a `__lt__` in which "less" means "worse", fewer copies or a later word, and the same push-and-evict loop works. When k is small it is simpler to heapify all `(-count, word)` pairs and pop k times, O(m + k log m) for m distinct words.

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
- Run `k_closest([[1, 1]], 5)`: `[[1, 1]]`. With k above the number of points the cap is never reached, and no special case is needed.

One heap holds one end of the order; the median needs both ends at once. Find Median from Data Stream adds numbers one at a time and asks for the median after each add: after 1 and 2 it is 1.5, after 3 it is 2.0. The median lives at the seam between the smaller half and the larger half, so keep the smaller half in a max-heap and the larger half in a min-heap, and the middle numbers sit at the two roots.

```text
   low (max-heap, stored negated)        high (min-heap)
   1   3   [5]          |                [15]   20
             ^ largest small number       ^ smallest large number
   invariant: every low <= every high, and len(low) is len(high) or len(high) + 1
   median: -low[0] when the count is odd (here 5), else the mean of the two roots
```

`add` keeps both rules in three steps, without a comparison of its own: the number joins the small half, the largest small number crosses the seam, and if the large half is now the bigger one, its smallest number crosses back. `median` then reads only the roots.

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

The next variation puts a queue beside the heap, for items that are the best but may not be used yet. Task Scheduler runs one task per tick or idles, with equal tasks at least n ticks apart, and asks for the least total time: `AAABBB` with n = 2 takes 8 ticks, `A B _ A B _ A B`. Always run the ready task with the most copies left, because it is the one that would otherwise force idle ticks at the end.

A task that just ran waits n ticks on a FIFO conveyor belt; tasks leave the belt in the order they got on, so only its front needs checking. The release comes *after* the run: a task whose cooldown ends with this tick may run from the next tick on.

Reorganize String asks for a rearrangement with no two equal neighbours, `aab` to `aba` and `aaab` to `""`, and it is the same machine with a cooldown of one turn. The belt shrinks to a single `held` letter, pushed back only after the next letter has been chosen.

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

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic. The skyline sweeps like [Intervals & Sweep Line](#s14), and IPO, refuelling and Course Schedule III are greedy with regret from [Greedy](#s15): read those first.

The first pattern lets a heap sit beside a sort, so that a greedy choice is made from the right candidates, or can be undone. Sort by the key that *unlocks* options, capital, position or deadline; sweep; push each unlocked option into a heap keyed by its *value*; and pop only when you must choose, or when you must undo a choice.

IPO starts you with capital w and lets you run at most k projects, each needing a minimum capital and paying a profit, to end as rich as possible: k = 2, w = 0, profits `[1, 2, 3]` and capital `[0, 1, 1]` end with 4. Before each choice, push every project the capital now affords, then run the most profitable one.

Minimum Number of Refueling Stops drives a car with some starting fuel toward a target past stations `[position, fuel]`, and asks for the fewest stops, or −1: target 100 with 10 fuel and stations `[[10, 60], [20, 30], [30, 30], [60, 40]]` needs 2. There the fix comes before the step, because you may only take fuel from stations you have actually reached.

Course Schedule III takes courses `[duration, last day]` back to back from day 1 and asks for the most courses that meet their deadlines: `[[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]` allows 3. It takes every course in deadline order and, when a deadline breaks, regrets the longest course taken.

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
    courses = sorted(courses, key=lambda c: c[1])        # INIT: by deadline
    taken, time = [], 0                                  # STATE: max-heap (negated) of taken durations; time = their sum
    for duration, last_day in courses:
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

A heap can't remove an item from its middle; lazy deletion says you don't have to. The Skyline Problem asks for the outline of buildings `[left, right, height]` standing on a shared ground line, as the list of points where the outline's height changes, ending at height 0: `[[2, 9, 10], [3, 7, 15]]` gives `[[2, 10], [3, 15], [7, 10], [9, 0]]`. Sweep the edges left to right with a max-heap of the live buildings.

```text
 15           +-----------+              buildings [2,9,10] [3,7,15] [5,12,12]
 12           |           +--------------+
 10        +--+                          |        sweep the edges left to right;
  0  ------+                             +-----   live = max-heap of (height, right end)
           2  3           7              12       key point = where the top height changes
```

A building that has ended stays in the heap as a dead entry until it reaches the top, because the top is the only thing you ever read. That is why the fix runs before the record reads the top, and why the ground, `(0, math.inf)`, sits in the heap from the start: it never ends, so there is always a top to read.

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

The second template, pop the lowest and push its successors, becomes a flood when the frontier is a wall. Trapping Rain Water II asks how much water a 2-D height map holds after rain, when water can only escape over the border: the map in the picture below traps 4. Water in a cell can rise only as high as the lowest wall on its best escape route to the border.

```text
heights            level the water reaches     trapped = level - height
1 4 3 1 3 2        1 4 3 1 3 2                 . . . . . .
3 2 1 3 2 4   ->   3 3 3 3 3 4          ->     . 1 2 0 1 .      total 4
2 3 3 2 3 1        2 3 3 2 3 1                 . . . . . .
```

So start with the border as the wall, always breach the wall at its *lowest* cell, and let the neighbour behind it fill up to that level and join the wall. It is Dijkstra with `max` in place of `+`, the shape you meet again in [Graphs III](#s19).

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
- Print `level, r, c` for each pop on the first grid: the levels never go down. That monotone order, never decreasing, is what makes each cell's level final when it is first reached.
- Run `trap_rain_water([[5, 1, 5]])`: 0. A grid with fewer than 3 rows or columns has no inside, because every cell is on the border.

The last pattern is the merge template with one more number beside the heap. Smallest Range Covering Elements from K Lists asks for the smallest `[a, b]` that contains at least one number from each of k sorted lists: for `[[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]` it is `[20, 24]`.

Put one finger on each list. The fingered values cover every list, and they span `[min, max]`. The only way to shrink that range is to raise the min, and only the finger *on* the min can do it: advance it, update the running max, and stop when some list runs out.

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

> "Sorting everything costs O(n log n) and orders items I'm going to throw away. I only need the k best, so I keep a min-heap capped at k: its root is the weakest of my k, and every newcomer only has to beat that root. Anything that leaves was beaten by k numbers still in the heap, so it can't be in the top k.
>
> Each step is O(log k): O(n log k) time, O(k) space, and it works on a stream. For k sorted lists I keep one head per list: every pop is the next item overall, O(N log k)."

While coding, point at the `if len(heap) > k` line and say the invariant: "after this line the heap holds exactly the k largest so far, and `heap[0]` is the k-th largest". In a merge, point at the refill right after the pop: "the list I just took from gets its next item in, so every list always has its head in the heap". And say why the tuple has an index in the middle: "so ties never compare the payload".

Likely follow-ups and your answers:

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

3. For the k closest points, why cap a max-heap at k instead of heapifying all n into a min-heap?
<details><summary>Answer</summary>The capped max-heap's root is the farthest point kept, so each newcomer is compared once, with that root, and memory stays O(k): O(n log k) time, and it works on a stream. Heapifying all n takes O(n) memory and O(n + k log n) time, and it needs every point up front.</details>

4. In the median finder, why does every number go into `low` first and then move `low`'s maximum to `high`?
<details><summary>Answer</summary>That two-step dance keeps the ordering rule without any comparisons of your own: whatever crosses the seam is the largest of the small half (including the new number), so every number in <code>low</code> stays at most every number in <code>high</code>. Step 3 then fixes only the sizes.</details>
