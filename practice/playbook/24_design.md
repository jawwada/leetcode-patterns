## Design Problems: From Requirements to Classes

> A design problem is a contract: a list of operations, each with a price ("O(1)", "O(log n)"). Give every operation a structure that answers its question at that price, write down the one sentence that keeps the structures in sync, and the methods nearly write themselves.

**Reach for it when** the prompt says *Design ...* or *Implement a class ...*, describes a **tracker, counter, rate limiter, cache or store**, lists method signatures, or puts a cost on every call ("each in O(1)", "many queries after one construction").

**In this repo:** `design/` (22 problems) · bank: `practice/simple/24_lru_cache.py` · basics: `practice/simple/basics/stacks/01_array_stack_and_queue_via_two_stacks.py` · design classes taught in other sections: Min Stack (`stack/min_stack.py`, `practice/simple/14_min_stack.py`), `queues/number_of_recent_calls.py`, `queues/design_circular_queue.py`, `queues/design_circular_deque.py` and `queues/implement_queue_using_stacks.py` in [Stacks & Queues](#s07); MedianFinder (`heap/find_median_from_data_stream.py`, `practice/simple/34_find_median_from_data_stream.py`), `heap/design_twitter.py` and `heap/kth_largest_element_in_a_stream.py` in [Heaps](#s13); `intervals/my_calendar_iii.py` in [Intervals](#s14); `tries/implement_trie_prefix_tree.py`, `tries/design_search_autocomplete_system.py` and `tries/stream_of_characters.py` in [Tries](#s12); `trees/serialize_and_deserialize_binary_tree.py` in [Trees](#s11)

### The picture

```text
THE METHOD, drawn for LRU Cache

  operation    price   the question it asks       the structure that answers it
  get(key)     O(1)    where is key's entry?      dict key -> node
                       make it the newest         list: unlink, push after HEAD
  put(key, v)  O(1)    where is key's entry?      dict;  make it the newest: list
  evict        O(1)    who is the oldest?         list: TAIL.prev;  forget it everywhere: del map[node.key]

  map   { 1: *, 2: *, 3: * }      each * points straight at a node in the list
  list  HEAD <-> [3] <-> [1] <-> [2] <-> TAIL
                 newest           oldest: evicted next
  the sentence that ties them: the keys in the dict are exactly the nodes in the list,
  and the list order is the recency order
```

Why it is fast: the brute force keeps one list of `(key, value)` pairs in recency order, so every `get` scans it (O(n)) and moving a pair to the front shifts everything behind it (O(n)). The dict removes the scan. The doubly linked list removes the shift: a node knows both of its neighbours, so unlinking it is two pointer writes, and the dict hands us the node directly.

### From idea to code

**The idea in one sentence:** *for each operation, ask which question it must answer and pick the structure that answers it at the required price; then write the invariant that keeps all the structures describing the same items.*

The method, in the order you work (with a 25-minute budget):

0. **Pin down the requirements (2-3 min)** and write the answers as the class docstring. Do timestamps only increase? Can two events share one? Can a write correct an earlier one? What does a query return when nothing matches? Which call is the most frequent? Is memory or capacity bounded, and can capacity be 0?
1. **List the operations and their price.**
2. **Pick one structure per question** (the table below). Usually one dict is the **source of truth** and every other structure is an **index** that answers one query fast.
3. **Write the invariant** that keeps the indexes in agreement with the truth, as a comment in `__init__`.
4. **Name the helpers and give each a one-line contract** (`_expire(t)`: afterwards every stored event is younger than the window). Write the public methods as helper calls, then fill in the helper bodies.
5. **Trace 4-5 calls**, printing the structures after each.
6. **Walk the edge cases out loud**, then state the cost of each operation and the memory.

```text
 0-3   requirements -> docstring        3-6   operation -> question -> structure, with costs
 6-8   invariant + helper names         8-18  public methods as helper calls, then helper bodies
18-23  trace 4-5 calls, printing the structures        23-25  edge cases, cost per operation, memory
```

**Who pays, the write or the read?** Keep the answer up to date on every write when reads must be O(1) (MovingAverage's total, Bitset's count of ones, LFU's `min_freq`, StockPrice's `latest`). Leave the cleanup to the reads when writes must stay cheap (HitCounter's expiry, a heap's stale tops). Say which one you chose.

**Source of truth + indexes.** One dict holds the truth; every other structure is an index for one query, updated eagerly (LRU relinks a node on every use) or validated lazily (a heap entry that disagrees with the dict is stale and skipped). The invariant always says the same thing: *the indexes agree with the truth*. LRU, LFU, RandomizedSet and Stock Price below are this one recipe.

| I need to do this fast | The question it answers | Use | Cost |
|---|---|---|---|
| lookup by key, membership | "where is x? have I seen x?" | `dict` / `set` | O(1) |
| count occurrences | "how many x so far?" | `Counter` / `dict` | O(1) per update |
| min or max, with inserts | "what is the smallest now?" | heap | O(log n) |
| min or max, with inserts and arbitrary deletes or corrections | "what is the smallest *live* item?" | heap + lazy deletion (skip stale tops) | O(log n) amortized |
| min or max of a sliding window | "what is the max of the last k?" | monotonic deque | O(1) amortized |
| next greater / previous smaller | "who resolves me?" | monotonic stack | O(1) amortized |
| median of a stream | "what is the middle?" | two heaps | O(log n) |
| events inside a time window | "how many in the last w seconds?" | `deque` + a running total | O(1) amortized |
| first position ≥ x in a sorted list | "where would x go?" | `bisect` | O(log n) |
| "the value as of time t" | "what was the last write at or before t?" | per-key list of (t, value) + `bisect` | O(log n) |
| a sorted set of disjoint intervals | "which intervals touch x?" | sorted list(s) + `bisect` | O(log n) search, O(n) insert |
| range sum, no updates / with point updates | "what is sum(a[i:j])?" | prefix sums / Fenwick tree | O(1) / O(log n) |
| "are a and b connected?" with merges | "same group?" | union-find | almost O(1) |
| prefix lookups among many words | "which words start with p?" | trie of dicts | O(length) |
| add and remove at both ends | "oldest? newest?" | `deque` | O(1) |
| undo, nesting, most recent | "what is the latest unresolved item?" | `list` as a stack | O(1) |
| lookup + order by recency | "which key was used longest ago?" | `dict` + doubly linked list, or `OrderedDict` | O(1) |
| a uniformly random element, with deletes | "pick any stored item" | dense `list` + `dict` value → index (swap with last) | O(1) |
| min or max of counts that change by ±1 | "which key has the smallest count?" | count buckets + a pointer to the min or max count | O(1) |

"Amortized O(1)" means: one call may do a lot of work (pop many expired events), but every item is added once and removed at most once, so n calls cost O(n) in total.

### Worked example: Stock Price Fluctuation (2034)

*A stream of `update(timestamp, price)` records; some records are corrections of an earlier timestamp. Answer `current()` (the price at the latest timestamp), `maximum()` and `minimum()` over the current prices.*

**Step 0, by asking:** can an update correct a past timestamp? *Yes*, so a price can go stale. Do timestamps arrive in order? *No*, so "current" means the largest timestamp seen, not the last call. Which call dominates? *All four are frequent*, so none of them may scan.

| Operation | The question it asks | Structure |
|---|---|---|
| `update(t, p)` | what is the price at t now? | dict `price`: t → latest price (the truth) |
| `current()` | which t is the latest? | `latest`, kept current on every write |
| `maximum()` / `minimum()` | which live price is the largest / smallest? | max-heap of `(-p, t)` / min-heap of `(p, t)`, stale entries skipped |

| Decision | Stock Price |
|---|---|
| **State** | `price` (the source of truth), `latest`, and two heaps as indexes: `hi` for the max, `lo` for the min |
| **Definition** | `price[t]` = the latest price recorded for t; a heap entry `(±p, t)` is live iff `p == price[t]` |
| **Invariant** | every live `(t, price[t])` is in both heaps; any other entry is stale, and reads pop stale tops first (the FIX) |
| **Step** | `update`: overwrite the truth, push one entry into each heap; the old entry for t silently becomes stale |
| **Record** | `latest = max(latest, t)` on every write, so `current()` is O(1) |
| **Init** | an empty dict, `latest = 0`, two empty heaps |
| **Return / edge cases** | `current()` reads `price[latest]`; a correction of the latest timestamp; a correction that moves the max; many corrections of one t (memory) |

```python
class StockPrice:
    """update(t, price) may correct an earlier t; current(), maximum(), minimum()."""

    def __init__(self):
        self.price = {}                      # STATE (source of truth): timestamp -> latest price
        self.latest = 0                      # STATE: the largest timestamp seen
        self.hi, self.lo = [], []            # STATE (indexes): heaps of (-price, t) and (price, t), may hold stale entries
        # INVARIANT: every (t, price[t]) is in both heaps; an entry whose price != self.price[t] is stale

    def _top(self, heap, sign):              # FIX: drop stale tops until the top is live
        while sign * heap[0][0] != self.price[heap[0][1]]:
            heapq.heappop(heap)
        return sign * heap[0][0]

    def update(self, t, p):
        self.price[t] = p                    # STEP: the truth changes first; a correction overwrites
        self.latest = max(self.latest, t)    # RECORD: kept current so current() is O(1)
        heapq.heappush(self.hi, (-p, t))     # the old entry for t, if any, is now stale
        heapq.heappush(self.lo, (p, t))

    def current(self):
        return self.price[self.latest]       # RETURN

    def maximum(self):
        return self._top(self.hi, -1)

    def minimum(self):
        return self._top(self.lo, 1)


s = StockPrice()
s.update(1, 10)
s.update(2, 5)
print(s.current(), s.maximum())              # 5 10
s.update(1, 3)                               # correction: 10 was wrong
print(len(s.hi), s.maximum(), len(s.hi))     # 3 5 2   (the stale 10 was popped on the way)
s.update(4, 2)
print(s.minimum(), s.current())              # 2 2
```

**Try it**
- Trust the top: make `_top` simply `return sign * heap[0][0]` and rerun. After the correction `maximum()` says 10, a price that no longer exists.
- Clean with `if` instead of `while` and run the updates (1, 10), (2, 9), (1, 1), (2, 2): `maximum()` is 9 instead of 2. Two stale entries were stacked on top, and one pop removed only the first.
- Memory: correct the same timestamp 1,000 times on a fresh `StockPrice`, then compare `len(s.hi)` (1,000) with `len(s.price)` (1). A common fix: rebuild both heaps from `price` when they grow past twice its size.

### Your turn: a per-user rate limiter

*`RateLimiter(limit, window)`; `allow(user, t)` returns whether the request is accepted. Each user may have at most `limit` **accepted** requests in any `window` seconds, i.e. with timestamps in `(t - window, t]`; refused requests don't count. Calls arrive with non-decreasing `t`.*

Run the method on paper first: what do you remember per user, what can you forget and when, and who pays (the write or the read)? Then fill in the class and run the cell; the checker runs a fixed case and 300 random sequences against a brute force.

```python
class RateLimiter:
    def __init__(self, limit, window):
        pass                                     # your state here

    def allow(self, user, t):
        return None                              # replace with your code


def check_rate_limiter(cls):
    if cls(2, 10).allow("a", 1) is None:
        print("not written yet: fill in RateLimiter and run this cell again")
        return
    rl, calls = cls(2, 10), [("a", 1), ("a", 2), ("a", 3), ("b", 3), ("a", 11), ("a", 12)]
    got, want = [rl.allow(u, t) for u, t in calls], [True, True, False, True, True, True]
    print(("ok   " if got == want else "FAIL ") + f"fixed case -> {got} (expected {want})")
    rng = random.Random(0)
    for _ in range(300):
        limit, window, t, accepted = rng.randint(1, 3), rng.randint(1, 6), 0, []
        rl = cls(limit, window)
        for _ in range(rng.randint(1, 25)):
            t += rng.randint(0, 3)
            user = rng.choice("ab")
            want = sum(1 for u, s in accepted if u == user and s > t - window) < limit
            if want:
                accepted.append((user, t))
            if rl.allow(user, t) != want:
                print(f"FAIL: limit={limit}, window={window}, request ({user!r}, {t}): expected {want}")
                return
    print("all random checks pass")


check_rate_limiter(RateLimiter)
```

**Try it**
- Write your solution, run the cell, and read the checker's lines. If a random case fails, replay that sequence by hand with your structures printed.
- Remember every request, accepted or not: the fixed case fails with `[True, True, False, True, False, False]`. A refused request must not use up the budget.
- Expire with `<` instead of `<=` (keep timestamps equal to `t - window`): the fixed case fails at `("a", 11)`. The window is `(t - window, t]`, so a request exactly `window` seconds old no longer counts.

<details><summary>One solution</summary>

```py
class RateLimiter:
    """Sliding log per user: remember only ACCEPTED requests, forget them once they leave the window."""

    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.log = defaultdict(deque)            # STATE: user -> accepted timestamps, oldest first

    def allow(self, user, t):
        q = self.log[user]
        while q and q[0] <= t - self.window:     # FIX: the read pays for the cleanup
            q.popleft()
        if len(q) < self.limit:
            q.append(t)                          # STEP: only accepted requests count
            return True
        return False                             # RETURN
```

Each accepted request is appended once and popped once: O(1) amortized per call, O(limit) memory per active user (a user who goes quiet keeps an empty deque; delete it when it empties if memory matters).

</details>

### The tracker family

Google-style "implement a tracker" questions are small design problems over a **stream of events**: hits, log lines, values, check-ins, writes. Each comes down to two questions: *what must I remember to answer the queries?* and *what can I forget, and when?*

**Time windows.** Time only moves forward, so an event that left the window is gone for good. The HitCounter here is the follow-up from [From Idea to Code](#s01): a million hits in one second must not mean a million deque entries, so equal timestamps share one `(t, count)` pair, and a running `total` answers `getHits` without counting.

```python
class Logger:                                    # print each message at most once per 10 seconds
    def __init__(self):
        self.next_ok = {}                        # STATE: message -> earliest time it may print again

    def shouldPrintMessage(self, timestamp, message):
        if timestamp < self.next_ok.get(message, 0):
            return False                         # RETURN: still inside its 10-second gate
        self.next_ok[message] = timestamp + 10   # STEP: printed now, so close the gate until t + 10
        return True


class MovingAverage:                             # average of the last `size` values
    def __init__(self, size):
        self.size, self.window, self.total = size, deque(), 0   # STATE: the last `size` values and their sum

    def next(self, val):
        self.window.append(val)                  # STEP
        self.total += val                        # RECORD: the running sum, kept current on every write
        if len(self.window) > self.size:
            self.total -= self.window.popleft()  # FIX: one value in, one value out
        return self.total / len(self.window)     # RETURN: divide by the CURRENT length (warm-up)


class HitCounter:                                # hits in the last 300 seconds, any number per second
    def __init__(self):
        self.window = deque()                    # STATE: (timestamp, hits at that second), oldest first
        self.total = 0                           # STATE: INVARIANT total == sum of the counts in window

    def _expire(self, now):                      # FIX: forget seconds that left the window, for good
        while self.window and self.window[0][0] <= now - 300:
            self.total -= self.window.popleft()[1]

    def hit(self, timestamp):
        if self.window and self.window[-1][0] == timestamp:
            self.window[-1] = (timestamp, self.window[-1][1] + 1)   # STEP: same second, bump its count
        else:
            self.window.append((timestamp, 1))   # STEP: a new second
        self.total += 1                          # RECORD: kept current on every write
        self._expire(timestamp)

    def getHits(self, timestamp):
        self._expire(timestamp)
        return self.total                        # RETURN


log = Logger()
print([log.shouldPrintMessage(t, "foo") for t in (1, 3, 11)])   # [True, False, True]
avg = MovingAverage(3)
print([round(avg.next(v), 2) for v in (1, 10, 3, 5)])           # [1.0, 5.5, 4.67, 6.0]
hits = HitCounter()
for t in (1, 1, 1, 2, 300):
    hits.hit(t)
print(hits.getHits(300), hits.getHits(301), len(hits.window))  # 5 2 2
```

**Try it**
- O(1) memory, the next follow-up: two 300-slot lists `times` and `counts` indexed by `t % 300`. On `hit(t)`, if `times[i] != t` reset the slot to `t, 0`; then add 1. `getHits(t)` sums `counts[i]` over the slots with `t - times[i] < 300`. Check it against `HitCounter` on random non-decreasing timestamps: the same answers, with 600 numbers of memory however long it runs.
- Hit 1,000 times at the same second on a fresh `HitCounter`: `len(window)` is 1.
- After the cell, `log.shouldPrintMessage(21, "foo")` is `True` (exactly 10 seconds after the print at 11). Change `<` to `<=` in the check and rerun: `[True, False, False]`, the call at 11 is wrongly refused.
- In `MovingAverage.next`, divide by `self.size` instead: the first two answers become 0.33 and 3.67 instead of 1.0 and 5.5. During warm-up the window is not full yet.

**Versions over time.** If writes arrive in time order (ask!), each per-key history is sorted for free, and "the value as of time t" is a `bisect_right` followed by one step back. Snapshot Array (1146) is the same idea per index: each cell keeps a list of `(snap_id, value)` pairs (overwriting the last pair when it is written twice in one snapshot), and `get(i, snap)` bisects for `(snap, math.inf)`.

```python
class TimeMap:
    """get(key, t): the value with the largest timestamp <= t, or "".
    Asked first: do set() timestamps only increase? Yes, so appending keeps each history sorted."""

    def __init__(self):
        self.times = defaultdict(list)           # STATE: key -> timestamps, increasing
        self.values = defaultdict(list)          # STATE: key -> values, aligned with times

    def set(self, key, value, timestamp):
        self.times[key].append(timestamp)        # STEP: appending keeps the history sorted
        self.values[key].append(value)

    def get(self, key, timestamp):
        hist = self.times.get(key, [])           # .get: a read must not create an entry
        i = bisect.bisect_right(hist, timestamp) # first time > timestamp
        return self.values[key][i - 1] if i else ""   # RETURN: one step back = last time <= timestamp


tm = TimeMap()
tm.set("foo", "bar", 1)
tm.set("foo", "bar2", 4)
print(tm.get("foo", 1), tm.get("foo", 3), tm.get("foo", 4), repr(tm.get("foo", 0)))   # bar bar bar2 ''
```

**Try it**
- Use `bisect_left` in `TimeMap.get` and rerun: exact timestamps are skipped, so `get("foo", 1)` comes back empty and `get("foo", 4)` returns `bar`.
- Read with `self.times[key]` instead of `self.times.get(key, [])`: `tm.get("nope", 5)` still returns `''`, but now `"nope" in tm.times` is `True`. On a `defaultdict`, every key ever asked about leaves an empty list behind.
- If `set` may arrive out of order, insert instead of appending: `i = bisect.bisect_right(self.times[key], timestamp)`, then `insert(i, ...)` into both lists. Reads stay O(log n); each write becomes O(n).

**Two lifetimes.** Some data lives briefly (an open journey), some lives forever but compresses (a route's total time and trip count): give each lifetime its own structure. Browser History (1472) splits the same way: the list of pages lives on, while "clear the forward history" is a bound (`last = cur`) rather than a deletion, so `back(k)` and `forward(k)` are index arithmetic, `max(0, cur - k)` and `min(last, cur + k)`.

```python
class UndergroundSystem:
    def __init__(self):
        self.open_trips = {}                     # STATE: id -> (start station, check-in time), short-lived
        self.stats = {}                          # STATE: (start, end) -> [total time, trips], kept forever

    def checkIn(self, id, stationName, t):
        self.open_trips[id] = (stationName, t)   # STEP

    def checkOut(self, id, stationName, t):
        start, t0 = self.open_trips.pop(id)      # STEP: the journey is over, forget it
        cell = self.stats.setdefault((start, stationName), [0, 0])
        cell[0] += t - t0                        # RECORD: running totals, kept current on every write
        cell[1] += 1

    def getAverageTime(self, startStation, endStation):
        total, trips = self.stats[(startStation, endStation)]
        return total / trips                     # RETURN


u = UndergroundSystem()
u.checkIn(45, "Leyton", 3)
u.checkIn(27, "Leyton", 10)
u.checkOut(45, "Waterloo", 15)
u.checkOut(27, "Waterloo", 20)
print(u.getAverageTime("Leyton", "Waterloo"), u.open_trips)   # 11.0 {}
```

**Try it**
- In `checkOut`, read with `self.open_trips[id]` instead of `pop`: the average is unchanged, but `u.open_trips` keeps both finished journeys forever.
- `u.getAverageTime("Waterloo", "Leyton")` raises `KeyError`: a route is an ordered pair, so the dict key is the tuple `(start, end)`.
- Use `//` instead of `/` and record trips of 12 and 9 minutes on a fresh route: 10 instead of 10.5.

### Caches: LRU, then LFU

LRU (146) is the method's showcase: two structures, one invariant, three helpers. The same design, sentence by sentence:

| In words | In code |
|---|---|
| "find the key's node" | `node = self.map.get(key)` |
| "take it out of the line" | `node.prev.next, node.next.prev = node.next, node.prev` |
| "put it at the front (newest)" | `node.prev, node.next = self.head, self.head.next`, then `self.head.next.prev = node` and `self.head.next = node` |
| "the oldest item" | `self.tail.prev` |
| "forget it completely" | unlink it and `del self.map[victim.key]` (this is why a node stores its key) |
| "too full" | `len(self.map) > self.cap` |
| "an empty list with no None checks" | `self.head.next, self.tail.prev = self.tail, self.head` |

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key, self.val = key, val            # the key lets eviction delete the map entry
        self.prev = self.next = None


class LRUCache:
    """get(key), put(key, value): both O(1). When full, evict the least recently used key."""

    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                            # STATE + INIT (truth): key -> Node
        self.head, self.tail = Node(), Node()    # STATE + INIT (index): sentinels; head.next newest, tail.prev oldest
        self.head.next, self.tail.prev = self.tail, self.head
        # INVARIANT: the keys in map are exactly the nodes between head and tail, and len(map) <= cap

    def _unlink(self, node):                     # contract: node leaves the list, its neighbours are joined
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):                 # contract: node becomes the newest
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _evict(self):                            # contract: the oldest key is forgotten everywhere
        victim = self.tail.prev
        self._unlink(victim)
        del self.map[victim.key]

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1                            # RETURN: missing key
        self._unlink(node)                       # STEP: a read is a use, so move it to the front
        self._push_front(node)
        return node.val                          # RETURN

    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.val = value                     # STEP: update AND refresh
            self._unlink(node)
        else:
            node = self.map[key] = Node(key, value)   # STEP: a new key
        self._push_front(node)
        if len(self.map) > self.cap:             # FIX: restore len(map) <= cap (insert first: capacity 0 also works)
            self._evict()


cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))                              # 1
cache.put(3, 3)                                  # evicts 2: key 1 was used more recently
print(cache.get(2))                              # -1
cache.put(4, 4)                                  # evicts 1
print(cache.get(1), cache.get(3), cache.get(4))  # -1 3 4
```

**Try it**
- Delete the line `del self.map[victim.key]` and rerun: the second print shows `2` instead of `-1`. The dict still points at a node that left the list; the invariant broke, and the answer is wrong without any error.
- Swap the last two lines of `_push_front` and rerun: the cell prints `1`, then `2` instead of `-1`, then crashes with `KeyError: 1`. After `self.head.next = node`, the line `self.head.next.prev = node` points the node at itself. (Swap them back before the trace below: on the broken list its walk would never end.)
- Move the two eviction lines above `self._push_front(node)` (evict first, as `practice/simple/24_lru_cache.py` does) and run `LRUCache(0).put(1, 1)`: `AttributeError`. In an empty list `tail.prev` is the head sentinel, whose `prev` is `None`. With capacity ≥ 1 both orders work.
- Predict, then check: `c = LRUCache(2)`, `put(1, 1)`, `put(2, 2)`, `put(1, 10)`, `put(3, 3)`. Key 2 is evicted, because updating key 1 also refreshed it: `c.get(2)` is -1 and `c.get(1)` is 10.

### Watch it work

The list from newest to oldest after each call:

```python
def recency(c):                                  # keys from newest to oldest
    keys, node = [], c.head.next
    while node is not c.tail:
        keys.append(node.key)
        node = node.next
    return keys


c = LRUCache(2)
for op, *args in [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3),
                  ("get", 2), ("put", 1, 10), ("get", 3)]:
    result = getattr(c, op)(*args)
    call = f"{op}({', '.join(map(str, args))})"
    print(f"{call:10} -> {str(result):4}  newest..oldest {recency(c)}")
```

**Try it**
- Add `("put", 4, 4)` at the end of the list and predict which key leaves before running: 1, because `get(3)` made 3 the newest.
- Print `sorted(c.map)` next to `recency(c)`: always the same keys. That is the invariant, made visible.
- Run it with `LRUCache(1)`: the list never holds more than one key, and every `get` returns -1, because each one asks for a key that the previous `put` pushed out.

**LFU (460)** changes one requirement: evict the key with the **fewest uses**, and among those the least recently used one. Run the method again: `freq_of` (key → count) is the truth; `bucket` (count → `OrderedDict` of keys, oldest first) is the index that answers "who is oldest among the rarest?"; one integer `min_freq` says which bucket that is.

**Invariant:** every key lives in exactly one bucket, `bucket[freq_of[key]]`, and `min_freq` is the smallest non-empty bucket whenever the cache is not empty. One integer can track the minimum because counts only ever go **up by one**: the minimum changes when a brand-new key arrives (it becomes 1), or when the last key of the minimum bucket moves up (it becomes `min_freq + 1`, exactly where that key went). An eviction can empty the lowest floor too, but it only happens right before a new key arrives, so the first case covers it.

```text
counts as floors, each floor a queue (oldest on the left):

freq 1: [2]        freq 2: [1, 3]        min_freq = 1
get(2):   2 climbs to floor 2; floor 1 is now empty and was the min   ->  min_freq = 2
freq 2: [1, 3, 2]                        min_freq = 2
put(4) when full: evict the oldest on the lowest floor (1), THEN 4 enters floor 1   ->  min_freq = 1
freq 1: [4]        freq 2: [3, 2]
```

```python
class LFUCache:
    """get, put in O(1). When full, evict the least frequently used key; ties -> least recently used."""

    def __init__(self, capacity):
        self.cap = capacity
        self.freq_of = {}                            # STATE (truth): key -> use count
        self.bucket = defaultdict(OrderedDict)       # STATE (index): count -> {key: value}, oldest first
        self.min_freq = 0                            # STATE: the smallest non-empty count
        # INVARIANT: key lives only in bucket[freq_of[key]]; min_freq = smallest non-empty bucket

    def _touch(self, key):                           # contract: one more use of key; returns its value
        f = self.freq_of[key]
        value = self.bucket[f].pop(key)
        if not self.bucket[f]:
            del self.bucket[f]
            if self.min_freq == f:
                self.min_freq = f + 1                # the min floor emptied: key went to f + 1
        self.bucket[f + 1][key] = value              # STEP: newest on its new floor
        self.freq_of[key] = f + 1
        return value

    def _evict(self):                                # FIX: make room, the oldest of the rarest leaves
        victim, _ = self.bucket[self.min_freq].popitem(last=False)
        if not self.bucket[self.min_freq]:
            del self.bucket[self.min_freq]
        del self.freq_of[victim]

    def get(self, key):
        if key not in self.freq_of:
            return -1
        return self._touch(key)                      # RETURN

    def put(self, key, value):
        if self.cap == 0:                            # edge: nothing can ever be stored
            return
        if key in self.freq_of:
            self._touch(key)                         # an update is a use too
            self.bucket[self.freq_of[key]][key] = value
            return
        if len(self.freq_of) == self.cap:
            self._evict()                            # evict FIRST: the newcomer must not be the victim
        self.bucket[1][key] = value                  # STEP: a new key starts on floor 1
        self.freq_of[key] = 1
        self.min_freq = 1                            # RECORD: a new key always has the smallest count


lfu = LFUCache(2)
lfu.put(1, 1)
lfu.put(2, 2)
print(lfu.get(1))                                # 1    (now key 1 has 2 uses, key 2 has 1)
lfu.put(3, 3)                                    # evicts 2, the key with the fewest uses
print(lfu.get(2), lfu.get(3))                    # -1 3
lfu.put(4, 4)                                    # 1 and 3 both have 2 uses; 1 is older -> evicted
print(lfu.get(1), lfu.get(3), lfu.get(4))        # -1 3 4
```

**Try it**
- Insert before evicting: move the eviction below the three insert lines (as `if len(self.freq_of) > self.cap: self._evict()`) and rerun. The last line prints `1 3 -1` instead of `-1 3 4`: the newcomer 4 sat alone on floor 1, so it was evicted instead of key 1.
- Delete `self.min_freq = 1` at the end of `put` and rerun: `KeyError: 'dictionary is empty'` at the first eviction. `min_freq` was still 0, a floor with no keys.
- Add `print({f: list(b) for f, b in lfu.bucket.items()}, lfu.min_freq)` after every call and watch keys climb one floor per use.

**RandomizedSet (380)** is the same recipe for uniform random picks: a dense list answers `getRandom` (`random.choice` needs no holes), a dict value → index answers membership, and a delete moves the last value into the hole so the list stays dense.

```python
class RandomizedSet:
    def __init__(self):
        self.vals = []                           # STATE (index): dense list, so random.choice is uniform
        self.pos = {}                            # STATE (truth): value -> its index in vals
        # INVARIANT: vals[pos[v]] == v for every stored v

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)           # STEP
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i, last = self.pos[val], self.vals[-1]
        self.vals[i], self.pos[last] = last, i   # STEP: move the last value into the hole
        self.vals.pop()
        del self.pos[val]                        # AFTER the move: works even when val is the last one
        return True

    def getRandom(self):
        return random.choice(self.vals)          # RETURN


random.seed(0)
rs = RandomizedSet()
print(rs.insert(5), rs.insert(8), rs.insert(2), rs.remove(5), rs.vals, rs.pos)   # True True True True [2, 8] {8: 1, 2: 0}
print(sorted({rs.getRandom() for _ in range(50)}))                              # [2, 8]
```

**Try it**
- Move `del self.pos[val]` up, before the line that fills the hole, then remove the only element: `r = RandomizedSet(); r.insert(1); r.remove(1)`. Now `r.pos` is `{1: 0}`, a ghost entry, and `r.insert(1)` returns `False`.
- `Counter(rs.getRandom() for _ in range(3000))`: each of the two values comes up about 1,500 times.
- Delete the line `del self.pos[val]` and rerun: `rs.pos` still lists 5, so `rs.insert(5)` returns `False` although `getRandom` can never return 5. The index (`vals`) and the truth (`pos`) disagree.

### Where it goes wrong

1. **The node does not store its key.** Eviction finds `tail.prev` but cannot delete it from the dict.
2. **Updating the truth and forgetting an index** (or the other way round). Every helper must leave the invariant true: unlink *and* `del map[key]`, pop the deque *and* subtract from the total.
3. **Pointer order in `_push_front`.** Set the node's own two pointers first, then `head.next.prev = node`, then `head.next = node`; swapping the last two points the node at itself.
4. **`put` of an existing key that only updates the value.** It must refresh recency (LRU) or count as a use (LFU) as well.
5. **Insert-then-evict in LFU.** The newcomer has the smallest count and can evict itself. LFU must evict first; LRU may do either.
6. **Forgetting a running value on a write** (`min_freq = 1`, `latest`, `total`), so a read answers with stale data.
7. **Trusting a lazily deleted heap top**, or cleaning it with `if` instead of `while`.
8. **Window boundaries.** "The last 300 seconds" is `(t - 300, t]`: pop while `timestamp <= now - 300`. A logger's "10 seconds" allows the same message again at exactly `t + 10`.
9. **`bisect_left` for "as of time t".** Use `bisect_right` (or probe with `(t, inf)`), or an exact match is skipped.
10. **Reads that write.** `self.times[key]` on a `defaultdict` inside a query creates an entry for every key ever asked about: read with `.get(key, [])`.
11. **Swap-with-last deletion in the wrong order.** Write `pos[last] = i` before `del pos[val]`, or removing the last element leaves a ghost.
12. **Class-level state and name clashes.** `seen = set()` in the class body is shared by every instance; an attribute named like a method hides the method ([Python Toolkit](#s02)).

### Edge cases to say out loud

Capacity 0 and 1 · `get` of a missing key · `put` of an existing key (refresh, no eviction) · an empty structure · a burst of events at one timestamp · a query before the first timestamp · a correction of the latest timestamp · removing the only (= last) element.

```python
c = LRUCache(1)
c.put(5, 5)
c.put(5, 6)                                      # update an existing key: no eviction
assert c.get(5) == 6
z = LRUCache(0)                                  # capacity 0: insert, then evict at once
z.put(1, 1)
assert z.get(1) == -1 and z.map == {}
lf = LFUCache(1)
lf.put(1, 1)
lf.get(1)                                        # key 1 now has 2 uses
lf.put(2, 2)                                     # evicts 1, not the newcomer
assert lf.get(1) == -1 and lf.get(2) == 2 and LFUCache(0).get(3) == -1
assert TimeMap().get("missing", 9) == ""
burst = HitCounter()
for _ in range(5):
    burst.hit(10)
assert burst.getHits(309) == 5 and burst.getHits(310) == 0 and len(burst.window) == 0
sp = StockPrice()
sp.update(5, 7)
sp.update(5, 1)                                  # correct the latest timestamp itself
assert sp.current() == 1 and sp.maximum() == 1 and sp.minimum() == 1
r = RandomizedSet()
assert r.insert(7) and r.remove(7) and r.vals == [] and r.pos == {}   # remove the only (= last) element
print("edge cases pass")
```

**Try it**
- An LFU tie: `f = LFUCache(2)`, `put(1, 1)`, `put(2, 2)`, `get(1)`, `get(2)`, `put(3, 3)`. Both old keys have 2 uses, so the least recently used one (1) leaves: `f.get(1), f.get(2), f.get(3)` gives `-1 2 3`.
- What should `HitCounter().getHits(5)` return with no hits at all? Predict, then assert it (0).
- A window of one is always the latest value: `m1 = MovingAverage(1)`, then `[m1.next(v) for v in (4, -2)]` is `[4.0, -2.0]`.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Heap + lazy deletion** | the dict is the truth; heap entries that disagree with it are skipped when they surface | Stock Price Fluctuation (2034), Number Container System (2349), Food Rating System (2353) |
| **A heap of free items** | the smallest free seat or id is the heap's top; freeing pushes it back | Seat Reservation Manager (1845) |
| **Counters per line** | row, column and both diagonal sums; a move updates at most 4 counters, a win is a counter reaching ±n | Design Tic-Tac-Toe (348) |
| **Deque + set** | the snake's body is a deque (head in, tail out) plus a set for O(1) self-collision checks | Design Snake Game (353) |
| **Count buckets in a linked list** | LRU's list, but each node is a *count* holding a set of keys; ±1 moves a key to the neighbouring bucket | All O'one Data Structure (432) |
| **Heap of candidates, validated lazily** | a min-heap of indices that may have room; check the top before trusting it | Dinner Plate Stacks (1172) |
| **Heaps + version stamps** | every state change pushes a fresh entry; stale entries are skipped when they surface | Design Movie Rental System (1912) |
| **Sorted boundaries + bisect** | intervals stay disjoint and sorted; a change only touches its neighbours | Range Module (715), Data Stream as Disjoint Intervals (352) |
| **Hashing by hand** | an array of short chains at `hash(key) % B`; double B and rehash when chains get long | Design HashMap (706) |
| **Trie of dicts** | each path component is an edge; a node is a directory (children) or a file (content) | Design In-Memory File System (588) |
| **Express lanes** | a sorted linked list plus random-height towers; a search drops a level when it cannot move right | Design Skiplist (1206) |
| **Positions + random sampling** | value → sorted positions; sample a few indices, verify each with two bisects | Online Majority Element In Subarray (1157) |
| **Fenwick tree** | point update and prefix sum in O(log n) per axis; a rectangle is 4 prefixes | Range Sum Query 2D - Mutable (308) |
| **A cursor and a logical end** | back/forward are index arithmetic; visit overwrites and moves the end | Design Browser History (1472) |
| **A snapshot next to each entry** | push (value, min so far) together | Min Stack (155), in [Stacks & Queues](#s07) |
| **Two heaps around the middle** | a max-heap for the low half, a min-heap for the high half, sizes within one | Find Median from Data Stream (295), in [Heaps](#s13) |

Follow-ups interviewers like: **memory** (the Logger's dict keeps every message forever; a deque of `(t, message)` lets you delete entries older than 10 seconds), **O(1)-memory windows** (HitCounter's 300-slot arrays, above), and **concurrency** (guard each public method with one `threading.Lock`, so no caller sees the truth and an index half-updated).

An **iterator with lookahead** (Peeking Iterator, 284) keeps the next item in a buffer, refilled by `next(self.it)` inside `try / except StopIteration`, plus a separate `done` flag: `hasNext()` must return `not self.done`, never `self.buffered is not None`, because `None` and `0` are real items. Flatten Nested List Iterator (341) and Zigzag Iterator (281) use the same buffer, with `hasNext` doing the work of finding the next real item.

A **token bucket** is the rate limiter that allows bursts: instead of remembering requests it keeps two numbers, and each call adds the refill a timer would have added:

```python
class TokenBucket:                               # up to `capacity` tokens, refilled at `rate` per second
    def __init__(self, capacity, rate):
        self.capacity, self.rate = capacity, rate
        self.tokens, self.last = capacity, 0     # STATE: tokens left, as of time self.last

    def allow(self, t):
        self.tokens = min(self.capacity, self.tokens + (t - self.last) * self.rate)   # FIX: lazy refill
        self.last = t
        if self.tokens >= 1:
            self.tokens -= 1                     # STEP: spend one token
            return True
        return False


tb = TokenBucket(capacity=2, rate=0.5)           # one new token every 2 seconds
print([tb.allow(t) for t in (0, 0, 0, 1, 2, 2, 6)])   # [True, True, False, False, True, False, True]
```

**Try it**
- Set `self.last = t` *before* computing the refill: `[True, True, False, False, False, False, False]`. The refill always saw `t - last == 0`.
- Drop the `min(self.capacity, ...)` cap and call `allow(100)` five times on a fresh bucket: all `True`, because 100 quiet seconds banked 52 tokens. The cap is what limits a burst.
- Compare with the sliding log of the RateLimiter above: the log is exact but remembers up to `limit` timestamps per user; the bucket remembers two numbers and allows short bursts.

### Stretch (Hard)

Three designs that are rarer in interviews, each teaching one trick.

**One stack per frequency** (Maximum Frequency Stack, 895): keep `freq[val]` and one stack per frequency, `group[f]`, holding the values in the order they *reached* f. A value pushed three times sits on floors 1, 2 and 3, so popping the top floor's stack is exactly "the most frequent, most recent value loses one copy"; when that stack empties, `max_freq -= 1` is always right, because frequencies are reached one step at a time.

**A lazy flag** (Design Bitset, 2166): flipping every bit is a change of *viewpoint*, not of data. Keep the physical `bits`, one `flipped` flag and a count of `ones`; the bit you see is `bits[i] ^ flipped`. `fix(i)` toggles only when the visible bit is 0 (and adds 1 to `ones`), `flip()` toggles the flag and sets `ones = size - ones`, and `all`, `one`, `count` just read `ones`: every call is O(1) except `toString`.

**Sorted boundaries** (Range Module, 715): a union of disjoint half-open blocks `[l, r)` is fully described by its sorted boundaries `[l0, r0, l1, r1, ...]`, and the parity of a bisect position tells you where you are. `addRange(l, r)` replaces the boundaries between `bisect_left(ends, l)` and `bisect_right(ends, r)` with `l` (only if l was in a gap) and `r` (only if r was in a gap); `removeRange` is the mirror image.

```text
ends = [10, 14, 16, 20]        tracked: [10, 14) and [16, 20)

  x:                    5     12     15     18     25
  bisect_right(ends,x): 0     1      2      3      4
  inside a block?       no    YES    no     YES    no        odd position = inside
```

### Say it in the interview

> "Let me pin down the operations and how often each is called, and ask whether timestamps only increase and whether a write can correct an earlier one. So operation A needs structure X and operation B needs Y. The dict is the source of truth and the others are indexes; the invariant is that they agree. Helpers like `_expire` and `_evict` keep it true, so each public method is a few calls. Cost per operation is ..., and memory is ..."

For LRU that becomes: "`get` and `put` are both O(1). Finding a key means a dict; recency order with O(1) move-to-front and O(1) remove-oldest means a doubly linked list whose nodes the dict points at. The invariant: the dict and the list hold the same keys. Two helpers, unlink and push-front, make `get` and `put` a few lines each; O(1) time, O(capacity) space." While coding, keep the invariant comment visible in `__init__` and, after each public method, say which helper restored it. If the interviewer allows libraries, `OrderedDict` with `move_to_end` and `popitem(last=False)` is the short version; offer to write the linked list yourself.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| All O'one Data Structure | `design/all_oone_data_structure.py` | doubly linked list of count buckets; a ±1 change moves a key to the neighbouring bucket |
| Data Stream as Disjoint Intervals | `design/data_stream_as_disjoint_intervals.py` | a value is covered, extends one neighbour, bridges two, or starts a singleton: only its two neighbours can change |
| Design Bitset | `design/design_bitset.py` | flip is a lazy flag (seen bit = stored bit XOR flag) plus a maintained count of ones |
| Design Browser History | `design/design_browser_history.py` | list + cursor + logical end; visit overwrites, forward clamps to the end |
| Design HashMap | `design/design_hashmap.py` | buckets of chains at hash % B; double B and rehash when the load factor passes 2 |
| Design Hit Counter | `design/design_hit_counter.py` | deque of (timestamp, count) + running total; pop the front once it is 300 s old |
| Design In-Memory File System | `design/design_in_memory_file_system.py` | trie keyed by path components; a node is a directory (children) or a file (content) |
| Design Movie Rental System | `design/design_movie_rental_system.py` | a heap per movie and one for rentals; lazy deletion with version stamps |
| Design Skiplist | `design/design_skiplist.py` | sorted list with random-height express lanes; record where the search turns down on each level |
| Design Underground System | `design/design_underground_system.py` | two dicts: open journeys by id, and (start, end) → [total time, trips] |
| Dinner Plate Stacks | `design/dinner_plate_stacks.py` | min-heap of indices that may have room, validated lazily; trim empty stacks on the right |
| Insert Delete GetRandom O(1) | `design/insert_delete_getrandom_o1.py` | list + value→index; delete by moving the last value into the hole |
| LFU Cache | `design/lfu_cache.py` | count → OrderedDict buckets + min_freq, which only resets to 1 or steps up by 1 |
| Logger Rate Limiter | `design/logger_rate_limiter.py` | dict message → next allowed timestamp |
| LRU Cache | `design/lru_cache.py` · `practice/simple/24_lru_cache.py` | dict key → node + doubly linked list with sentinels; the node stores its key for eviction |
| Maximum Frequency Stack | `design/maximum_frequency_stack.py` | one stack per frequency; pop from the stack of the max frequency |
| Moving Average from Data Stream | `design/moving_average_from_data_stream.py` | deque of the last `size` values + running sum |
| Online Majority Element In Subarray | `design/online_majority_element_in_subarray.py` | value → sorted positions; random samples verified with two bisects |
| Range Module | `design/range_module.py` | one flat sorted boundary list; an odd bisect position means "inside a block" |
| Range Sum Query 2D - Mutable | `design/range_sum_query_2d_mutable.py` | 2D Fenwick tree; update by the delta, query as 4 prefix rectangles |
| Snapshot Array | `design/snapshot_array.py` | per-index list of (snap_id, value); bisect_right for the last write ≤ snap_id |
| Time Based Key-Value Store | `design/time_based_key_value_store.py` | per-key timestamps appended in order; bisect_right − 1 |

### Self-check

1. The dict already maps key → node. Why must each LRU node also store its key?
<details><summary>Answer</summary>Eviction starts from the list side: it finds the oldest node as <code>tail.prev</code> and must then delete that node's entry from the dict. Without the key inside the node there is no O(1) way to know which dict entry to delete.</details>

2. LRU may insert the new node first and evict afterwards; LFU must evict first. Why the difference?
<details><summary>Answer</summary>In LRU the newcomer is the most recently used item, so it can never be the eviction victim (unless the capacity is 0, where evicting it is correct). In LFU the newcomer has a count of 1, the smallest possible, so if it is inserted first it can be the oldest item on the lowest floor and evict itself.</details>

3. In `RandomizedSet.remove`, what goes wrong if `del pos[val]` runs before `pos[last] = i`?
<details><summary>Answer</summary>When <code>val</code> is the last element, <code>last == val</code>, so <code>pos[last] = i</code> re-creates the entry that was just deleted. The set then believes <code>val</code> is still present (a ghost), and the next <code>insert(val)</code> wrongly returns False.</details>

4. Apply the method: a Leaderboard with `addScore(player, delta)`, `top(K)` (the sum of the K best scores) and `reset(player)`. Which structures, and what does each call cost?
<details><summary>Answer</summary>A dict player → score is the source of truth: <code>addScore</code> and <code>reset</code> are O(1). <code>top(K)</code> is <code>sum(heapq.nlargest(K, scores.values()))</code>: O(n log K), with nothing to keep in sync. If <code>top</code> is called far more often than scores change, also keep the scores in a sorted list: <code>top(K)</code> reads the last K in O(K), and each update pays an O(n) remove and insort.</details>
