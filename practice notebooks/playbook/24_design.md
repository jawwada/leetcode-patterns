## Design Problems: From Requirements to Classes

> A design problem is a contract: a list of operations, each with a price ("O(1)", "O(log n)"). Give every operation a structure that answers its question at that price, write down the one sentence that keeps the structures in sync, and the methods nearly write themselves.

By the end of this section you will take a prompt like *"design a hit counter"*, a class that counts the hits of the last five minutes, and turn it into a working class inside 25 minutes. You will ask the questions that settle the requirements, give every operation a structure that answers it at the asked price, write the invariant that keeps those structures agreeing, and type the methods as calls to two or three small helpers.

Every class here is built by that one procedure, and the section ends with the script for saying it out loud.

**Reach for it when** the prompt says *Design ...* or *Implement a class ...*, describes a **tracker, counter, rate limiter, cache or store**, lists method signatures, or puts a cost on every call ("each in O(1)", "many queries after one construction").

Several design classes live with the structure they are built on. Min Stack, a stack that also reports its minimum in O(1) (`stack/min_stack.py`, `practice/simple/14_min_stack.py`), and `queues/number_of_recent_calls.py`, `queues/design_circular_queue.py`, `queues/design_circular_deque.py` and `queues/implement_queue_using_stacks.py` are in [Stacks & Queues](#s07). MedianFinder, the running median of a stream (`heap/find_median_from_data_stream.py`, `practice/simple/34_find_median_from_data_stream.py`), `heap/design_twitter.py` and `heap/kth_largest_element_in_a_stream.py` are in [Heaps](#s13).

The others sit in three more sections: `intervals/my_calendar_iii.py` in [Intervals & Sweep Line](#s14); `tries/implement_trie_prefix_tree.py`, `tries/design_search_autocomplete_system.py` and `tries/stream_of_characters.py` in [Tries](#s12); and `trees/serialize_and_deserialize_binary_tree.py` in [Trees](#s11).

### The picture

LRU Cache is the showcase, so the picture is drawn for it. `get(key)` returns the value or −1 and `put(key, value)` stores one, both in O(1), and when the cache is full a `put` of a new key evicts the key that was used longest ago. The picture is the whole method on one problem: each operation becomes a question, each question gets a structure, and one sentence ties the structures together.

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

Why it is fast: the brute force keeps one list of `(key, value)` pairs in recency order. Every `get` scans it to find the key, which is O(n), and moving the pair to the front shifts everything behind it, another O(n).

The two structures remove the two costs. The dict removes the scan, because it hands us the node directly. The doubly linked list removes the shift, because a node knows both of its neighbours, so unlinking it is two pointer writes and no other node moves.

### From idea to code

**The idea in one sentence:** *for each operation, ask which question it must answer and pick the structure that answers it at the required price; then write the invariant that keeps all the structures describing the same items.*

The seven decisions of [From Idea to Code](#s01) apply to a class as they apply to a loop: the items are now calls, the state lives in `self`, and every decision has a fixed place. **State** is the structures in `self`, one `# STATE` line in `__init__` for each, with its **Definition** as the comment, and **Init** is what those lines assign. The **Invariant** is the sentence that is true between any two calls, written as the last comment of `__init__`.

A **Step** is what a public method does to the state, and a **Fix** is the private helper that makes the invariant true again, such as `_expire` or `_evict`. **Record** is the running value a write keeps current, a total or a minimum, and **Return** is what each query hands back, including its answer when nothing matches.

The procedure below makes those decisions in the order you work, against a 25-minute clock. Each step leaves something written down, so you hold one decision in your head at a time, and the same procedure builds every class in this section.

1. **Requirements, minutes 0-3.** Ask before you design, and write the answers as the class docstring. Ask whether timestamps only increase, whether two events can share one, whether a write can correct an earlier one, what a query returns when nothing matches, which call is the most frequent, and whether the capacity is bounded and can be 0. Each answer changes a structure, so each is worth its sentence.
2. **Operations and costs, minutes 3-5.** List every public method with the price the prompt puts on it, or the price you propose when it names none. Then turn each into the question it must answer: `get(key)` asks "where is key's entry?", and eviction asks "who is the oldest?".
3. **One structure per question, minutes 5-7.** Pick each structure from the table below by its question and its price, never by the problem's name. One structure, usually a dict, holds the truth, and every other one is an index that answers one question fast. Write them as `# STATE` lines in `__init__`, each with its definition.
4. **The invariant, minutes 7-8.** Write the one sentence that is true between any two calls as the last comment of `__init__`. In a design it almost always reads "the indexes agree with the truth", and every method must leave it true.
5. **Helpers, minutes 8-10.** Name the repairs, `_expire(t)`, `_unlink(node)`, `_evict()`, and give each a one-line contract that says what is true after it runs. A helper is the invariant restored, with a name.
6. **Methods, minutes 10-18.** Write each public method as two or three helper calls, then fill in the helper bodies. After each method, say which helper restored the invariant.
7. **Trace and edge cases, minutes 18-25.** Trace four or five calls on paper, writing down the structures after each. Then say the edge cases out loud: the empty structure, capacity 0 and 1, a missing key, a key written twice, a burst at one timestamp. Close with the cost of each operation and the memory.

| Minutes | You are doing | You have written |
|---|---|---|
| 0-3 | asking the requirement questions | the class docstring |
| 3-7 | operation → question → structure, with costs | `__init__`, one `# STATE` line per structure |
| 7-10 | the invariant and the helper names | the last comment of `__init__`, the helper signatures |
| 10-18 | public methods as helper calls, then the helper bodies | the class |
| 18-25 | a trace of 4-5 calls, the edge cases, the costs | a state table and the closing sentence |

Every design makes one more choice: who pays, the write or the read? Keep the answer current on every write when reads must be O(1): a running total for the mean of the last k values, a count of ones for a bitset that flips, the smallest use count for a cache that evicts its rarest key, the latest timestamp for a price feed.

Leave the cleanup to the reads when writes must stay cheap: a hit counter expires old seconds when someone asks, and a heap drops stale tops when they surface. Say which one you chose; it is the sentence the interviewer is listening for.

Two words carry the method. The **source of truth** is the one structure that is always right, usually a dict: when structures disagree, the truth wins. An **index** is any extra structure kept only so that one question is fast, a heap for "what is the smallest?", a linked list for "who is the oldest?".

An index is updated eagerly, as LRU relinks a node on every use, or checked lazily, as a heap entry that disagrees with the dict is skipped. Either way the invariant is the same sentence, *the indexes agree with the truth*, and every class in this section is this one recipe.

**Lazy deletion** is the second way made precise: nothing leaves the heap at the moment it dies. The dict is corrected, the old heap entry stays behind as a **stale** entry, and whoever reads the heap's top first checks it against the dict and pops it if it disagrees.

Some prices in the table are **amortised**: one call may do a lot of work, such as popping many expired events, but every item is added once and removed at most once, so n calls cost O(n) in total, O(1) per call averaged over the run. The table is the lookup for step 3: find the question, then read off the structure and its price.

| I need to do this fast | The question it answers | Use | Cost |
|---|---|---|---|
| lookup by key, membership | "where is x? have I seen x?" | `dict` / `set` | O(1) |
| count occurrences | "how many x so far?" | `Counter` / `dict` | O(1) per update |
| min or max, with inserts | "what is the smallest now?" | heap ([Heaps](#s13)) | O(log n) |
| min or max, with inserts and arbitrary deletes or corrections | "what is the smallest *live* item?" | heap + lazy deletion (skip stale tops) | O(log n) amortised |
| min or max of a sliding window | "what is the max of the last k?" | monotonic deque ([Sliding Window](#s06)) | O(1) amortised |
| next greater / previous smaller | "who resolves me?" | monotonic stack ([Monotonic Stack](#s08)) | O(1) amortised |
| median of a stream | "what is the middle?" | two heaps | O(log n) |
| events inside a time window | "how many in the last w seconds?" | `deque` + a running total | O(1) amortised |
| first position ≥ x in a sorted list | "where would x go?" | `bisect` ([Binary Search](#s09)) | O(log n) |
| "the value as of time t" | "what was the last write at or before t?" | per-key list of (t, value) + `bisect` | O(log n) |
| a sorted set of disjoint intervals | "which intervals touch x?" | sorted list(s) + `bisect` | O(log n) search, O(n) insert |
| range sum, no updates / with point updates | "what is sum(a[i:j])?" | prefix sums / Fenwick tree ([Prefix Sums](#s04)) | O(1) / O(log n) |
| "are a and b connected?" with merges | "same group?" | union-find | almost O(1) |
| prefix lookups among many words | "which words start with p?" | trie of dicts ([Tries](#s12)) | O(length) |
| add and remove at both ends | "oldest? newest?" | `deque` | O(1) |
| undo, nesting, most recent | "what is the latest unresolved item?" | `list` as a stack | O(1) |
| lookup + order by recency | "which key was used longest ago?" | `dict` + doubly linked list, or `OrderedDict` | O(1) |
| a uniformly random element, with deletes | "pick any stored item" | dense `list` + `dict` value → index (swap with last) | O(1) |
| min or max of counts that change by ±1 | "which key has the smallest count?" | count buckets + a pointer to the min or max count | O(1) |

### Worked example: Stock Price Fluctuation (2034)

The first full run of the method is a problem where the truth changes under its indexes, so you can watch the invariant earn its keep. Stock Price Fluctuation receives a stream of `update(timestamp, price)` records, and a record may correct the price of an earlier timestamp. `current()` returns the price at the latest timestamp, and `maximum()` and `minimum()` return the largest and the smallest price among the current records.

After `update(1, 10)`, `update(2, 5)` and `update(1, 3)`, the current price is 5 and the maximum is 5, because the 10 was corrected away. That example settles the requirements before a line is typed. An update can correct a past timestamp, so a stored price can go stale. Timestamps arrive in any order, so "current" means the largest timestamp seen, not the last call. All four calls are frequent, so none of them may scan: each costs O(log n) at most.

Each operation now names its question and its structure. `update(t, p)` asks what the price at t is now, so a dict `price` from timestamp to latest price is the truth. `current()` asks which timestamp is the latest, so one integer `latest` is kept current on every write.

`maximum()` and `minimum()` ask which live price is the largest and the smallest, so a max-heap of `(-p, t)` and a min-heap of `(p, t)` serve as indexes, with stale entries skipped when they reach the top.

The seven decisions follow from that. The state is `price`, the source of truth, `latest`, and the two heaps `hi` and `lo` as indexes. The definition: `price[t]` is the latest price recorded for t, and a heap entry `(±p, t)` is live exactly when `p == price[t]`. The invariant: every live `(t, price[t])` is in both heaps, any other entry is stale, and reads pop stale tops first; that popping is the fix.

The step, in `update`, overwrites the truth and pushes one entry into each heap, so the old entry for t silently becomes stale. Record is what each method returns, plus the running value kept current on every write, `latest = max(latest, t)`, so `current()` is O(1). Init is an empty dict, `latest = 0` and two empty heaps.

The edge cases to say out loud are a correction of the latest timestamp itself, a correction that moves the maximum, and many corrections of one timestamp, which is a question about memory.

So the class below keeps the dict, the integer and the two heaps. `update` writes the truth and pushes, O(log n), and the one helper `_top` pops stale tops until the top is live, so `maximum` and `minimum` are one call each, O(log n) amortised, because every entry is popped at most once. The prints replay the example and show a stale top leaving the max-heap.

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

Now run the procedure yourself, on a tracker-shaped problem, before reading the tracker family. `RateLimiter(limit, window)` has one method, `allow(user, t)`, which returns whether the request is accepted; it runs on every request, so it should cost O(1) amortised. Each user may have at most `limit` **accepted** requests in any `window` seconds, that is with timestamps in `(t - window, t]`, and refused requests do not count. Calls arrive with non-decreasing `t`.

With `limit = 2` and `window = 10`, user a at times 1, 2, 3 is accepted, accepted, refused, and accepted again at 11, because the request from time 1 has left the window.

Run the method on paper first: what do you remember per user, what can you forget and when, and who pays, the write or the read? Then fill in the class in the cell below and run it. The checker runs that fixed case and 300 random sequences against a brute force.

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
        while q and q[0] <= t - self.window:
            q.popleft()                          # FIX: the read pays for the cleanup
        if len(q) < self.limit:
            q.append(t)                          # STEP: only accepted requests count
            return True
        return False                             # RETURN
```

Each accepted request is appended once and popped once: O(1) amortised per call, O(limit) memory per active user. A user who goes quiet keeps an empty deque; delete it when it empties if memory matters.

</details>

### The tracker family

Most "implement a tracker" questions are small cousins of the worked example, and this is where the procedure starts to pay for itself. A tracker watches a **stream of events**: hits, log lines, values, check-ins, writes. Every one of them comes down to two questions: *what must I remember to answer the queries?* and *what can I forget, and when?*

Time windows come first, because time only moves forward: an event that left the window is gone for good, so forgetting is safe. Logger Rate Limiter asks for `shouldPrintMessage(t, message)` in O(1), true when the same message was not printed in the last 10 seconds: a message printed at 1 is refused at 3 and allowed again at 11. One dict from message to the earliest time it may print again answers it, with no window kept at all.

Moving Average from Data Stream asks for `next(v)` in O(1), the mean of the last `size` values: with `size = 3` the stream 1, 10, 3, 5 answers 1.0, 5.5, 4.67, 6.0. A deque of the last `size` values plus their running sum answers it, and during warm-up the mean divides by the current length.

Design Hit Counter asks for `hit(t)` and `getHits(t)` in O(1) amortised, the number of hits in the last 300 seconds, `(t - 300, t]`, with timestamps that never decrease and any number of hits per second: after hits at 1, 1, 1, 2 and 300, `getHits(300)` is 5 and `getHits(301)` is 2.

It is the follow-up from [From Idea to Code](#s01): a million hits in one second must not mean a million deque entries, so equal timestamps share one `(t, count)` pair, and a running `total` answers `getHits` without counting.

All three classes below answer each call in O(1), the hit counter amortised. In each the write keeps a running value current, and in the hit counter the read also pays for the expiry. The prints replay the three examples, and the last number is the hit counter's deque length, one pair per second still inside the window.

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

Versions over time are the next family, because here nothing is ever forgotten and the question becomes "what was true at time t?". Time Based Key-Value Store asks for `set(key, value, t)` and `get(key, t)`, the value with the largest timestamp at or below t, or `""` when there is none: after `set("foo", "bar", 1)` and `set("foo", "bar2", 4)`, `get("foo", 3)` is `"bar"` and `get("foo", 0)` is `""`.

Ask first whether `set` timestamps only increase. They do, so appending keeps each key's history sorted for free and `set` is O(1). A read is `bisect_right` for the first timestamp after t, then one step back, O(log n). The prints read the history at, between and before its two writes.

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

Snapshot Array is the same idea per index. `SnapshotArray(n)` starts as n zeros; `set(i, v)` writes a cell, `snap()` returns the id of the snapshot just taken, counting from 0, and `get(i, snap_id)` returns the cell as it was in that snapshot, and no call may copy the array: after `set(0, 5)`, `snap()` → 0 and `set(0, 6)`, the call `get(0, 0)` is 5.

Give each cell its own history, a list of `(snap_id, value)` pairs that starts as `[(0, 0)]`, and keep one counter `snap_id`, the id of the snapshot still open. The invariant: every history is sorted by id and holds one pair per id at most. So `set` overwrites the last pair when its id is the open one and appends otherwise, `snap` returns the counter and adds one, and `get` is `bisect_right(hist[i], (snap_id, inf))` and one step back, the TimeMap read. Writes are O(1), a read O(log n).

Some trackers hold two kinds of data with two lifetimes, and each lifetime gets its own structure. Design Underground System asks for `checkIn(id, station, t)`, `checkOut(id, station, t)` and `getAverageTime(start, end)` in O(1), the mean time of the completed trips on a route: trips from Leyton to Waterloo of 12 and 10 minutes average 11.0.

An open journey lives briefly, so it sits in a dict by id until its check-out pops it. A route's statistics live forever but compress to two numbers, so a second dict keyed by `(start, end)` keeps the total time and the trip count current on every check-out, the running sum of MovingAverage, and the average is one division.

Design Browser History splits the same way, with a bound in place of a deletion. `visit(url)` opens a page and clears the forward history, and `back(k)` and `forward(k)` move at most k pages and return the page they land on, each in O(1): from home, after visiting a and then b, `back(1)` is a and `forward(5)` is b.

One list holds the pages, a cursor marks the current one, and clearing the forward history only moves a logical end, `last = cur`. So `visit` overwrites the slot after the cursor, appending when the list ends there, `back(k)` is `max(0, cur - k)` and `forward(k)` is `min(last, cur + k)`: index arithmetic.

### The LRU cache

A cache is the classic design question, and LRU is the method's showcase: two structures, one invariant, three helpers. LRU Cache asks for `get(key)`, the value or −1, and `put(key, value)`, both in O(1); when a `put` of a new key would exceed the capacity, the key whose last `get` or `put` is the oldest is evicted. With capacity 2, `put(1, 1)`, `put(2, 2)`, `get(1)`, `put(3, 3)` evicts key 2, because key 1 was used more recently.

The design, sentence by sentence, is the code. Finding the key's node is `node = self.map.get(key)`. Taking it out of the line is two pointer writes, `node.prev.next, node.next.prev = node.next, node.prev`, which join its neighbours to each other. Putting it at the front, where the newest sits, sets the node's own two pointers first, `node.prev, node.next = self.head, self.head.next`, then `self.head.next.prev = node`, and only then `self.head.next = node`.

The oldest item is `self.tail.prev`. Forgetting it completely means unlinking it and `del self.map[victim.key]`, which is why every node stores its key. "Too full" is `len(self.map) > self.cap`.

`head` and `tail` are **sentinels**, the dummy nodes of [Linked Lists](#s10): they never hold data, so every real node has a neighbour on both sides and no method ever checks for `None`. The empty list is `self.head.next, self.tail.prev = self.tail, self.head`. Each helper below restores the invariant its contract names, and `get` and `put` are a few helper calls each. The prints replay the example, then one more `put` that evicts key 1.

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
- Swap the last two lines of `_push_front` and rerun: the cell prints `1`, then `2` instead of `-1`, then crashes with `KeyError: 1`. After `self.head.next = node`, the line `self.head.next.prev = node` points the node at itself. Swap them back before the trace below: on the broken list its walk never ends.
- Move the two eviction lines above `self._push_front(node)` (evict first, as `practice/simple/24_lru_cache.py` does) and run `LRUCache(0).put(1, 1)`: `AttributeError`. In an empty list `tail.prev` is the head sentinel, whose `prev` is `None`. With capacity ≥ 1 both orders work.
- Predict, then check: `c = LRUCache(2)`, `put(1, 1)`, `put(2, 2)`, `put(1, 10)`, `put(3, 3)`. Key 2 is evicted, because updating key 1 also refreshed it: `c.get(2)` is -1 and `c.get(1)` is 10.

### Watch it work

The invariant is easiest to believe when you can see it. The helper below walks the list from `head` to `tail` and prints the keys from newest to oldest after each call, next to what the call returned. The calls are the example's four, then `get(2)`, an update of key 1 and `get(3)`.

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

### Where it goes wrong

1. **The node does not store its key.** Eviction finds the oldest node as `tail.prev` and must then delete its dict entry, which needs the key. An eviction that skips `del map[key]` leaves a ghost: in `LRUCache(1)`, `put(1, 1)`, `put(2, 2)`, `get(1)` returns 1 instead of −1.
2. **Updating the truth and forgetting an index**, or the other way round. Every helper must leave the invariant true: unlink *and* `del map[key]`, pop the deque *and* subtract from the total. A HitCounter whose `_expire` pops without subtracting answers `getHits(301)` with 2 instead of 1 after hits at 1 and 301.
3. **Pointer order in `_push_front`.** Set the node's own two pointers first, then `head.next.prev = node`, then `head.next = node`; swapping the last two points the node at itself. The LRU example then answers `get(2)` with 2 instead of −1 and crashes on the next `put`.
4. **`put` of an existing key that only updates the value.** A write is a use, so it must refresh the key as well. With capacity 2, `put(1, 1)`, `put(2, 2)`, `put(1, 10)`, `put(3, 3)` must evict key 2; a value-only update evicts key 1, and `get(1)` returns −1 instead of 10.
5. **A running value left stale by a write.** Every write must update `latest` or `total` in the same method, or a read answers from the past. In StockPrice, `latest = t` in place of `max(latest, t)` lets a correction move "now" backwards: after `update(1, 10)`, `update(2, 5)`, `update(1, 3)`, `current()` returns 3 instead of 5.
6. **Trusting a lazily deleted heap top**, or cleaning it with `if` instead of `while`. After the updates (1, 10), (2, 9), (1, 1), (2, 2), a trusted top says the maximum is 10 and a single `if` says 9; the `while` loop gives 2.
7. **Window boundaries.** "The last 300 seconds" is `(t - 300, t]`, so pop while `timestamp <= now - 300`: with `<`, a hit at 1 still counts in `getHits(301)`. A logger's "10 seconds" allows the same message again at exactly `t + 10`, so a message printed at 1 prints again at 11.
8. **`bisect_left` for "as of time t".** Use `bisect_right`, or probe with `(t, inf)`, or an exact match is skipped: with writes at 1 and 4, `bisect_left` makes `get("foo", 1)` return `""` instead of `"bar"`.
9. **Reads that write.** `self.times[key]` on a `defaultdict` inside a query creates an entry for every key ever asked about: after `tm.get("nope", 5)`, `"nope" in tm.times` is True. Read with `.get(key, [])`.
10. **Class-level state and name clashes** ([Python Toolkit](#s02)). `next_ok = {}` in the class body is shared by every Logger, so a fresh logger refuses `"foo"` at time 2 because another one printed it at 1. An attribute named like a method hides the method: `self.next = 0` in `MovingAverage.__init__` makes `avg.next(1)` raise `TypeError`.
11. **Insert-then-evict in LFU Cache**, the variation below that evicts the key with the fewest uses. There the newcomer has the smallest count and can evict itself, so LFU must evict first, while LRU may do either. In `LFUCache(1)`, `put(1, 1)`, `get(1)`, `put(2, 2)` must evict key 1; insert-first evicts the newcomer, and `get(2)` returns −1.
12. **Swap-with-last deletion in the wrong order**, in Insert Delete GetRandom O(1), the set below with O(1) insert, remove and random pick. Write `pos[last] = i` before `del pos[val]`, or removing the last element leaves a ghost: `insert(1)`, `remove(1)`, `insert(1)` returns False.

### Edge cases to say out loud

Capacity 0 and 1 · `get` of a missing key · `put` of an existing key (refresh, no eviction) · an empty structure · a burst of events at one timestamp · a query before the first timestamp · a correction of the latest timestamp · removing the only element, which is also the last one.

The cell asserts each of them on the classes above, and every line is one sentence you would say while coding. The two caches of Variations check their own.

```python
c = LRUCache(1)
c.put(5, 5)
c.put(5, 6)                                      # update an existing key: no eviction
assert c.get(5) == 6 and c.get(7) == -1          # a missing key reads -1
c.put(7, 7)                                      # capacity 1: the only stored key is evicted
assert c.get(5) == -1 and recency(c) == [7]
z = LRUCache(0)                                  # capacity 0: insert, then evict at once
z.put(1, 1)
assert z.get(1) == -1 and z.map == {}
tm0 = TimeMap()
tm0.set("k", "v", 5)
assert tm0.get("missing", 9) == "" and tm0.get("k", 4) == ""   # a missing key; a query before the first write
burst = HitCounter()
for _ in range(5):
    burst.hit(10)                                # a burst at one timestamp shares one pair
assert len(burst.window) == 1 and burst.getHits(309) == 5
assert burst.getHits(310) == 0 and len(burst.window) == 0      # and it expires all at once
sp = StockPrice()
sp.update(5, 7)
sp.update(5, 1)                                  # correct the latest timestamp itself
assert sp.current() == 1 and sp.maximum() == 1 and sp.minimum() == 1
print("edge cases pass")
```

**Try it**
- What should `HitCounter().getHits(5)` return with no hits at all? Predict, then assert it (0).
- A window of one is always the latest value: `m1 = MovingAverage(1)`, then `[m1.next(v) for v in (4, -2)]` is `[4.0, -2.0]`.
- Correct a maximum away: on a fresh `StockPrice`, run `update(1, 9)`, `update(2, 4)`, `update(1, 1)`, then predict `len(sp.hi)` before and after `maximum()`. It is 3, then 2, and the maximum is 4.

### Variations

Every variation is the method again with one different structure, or a different answer to who pays. The table is the overview and a lookup: find the trick, then the problems that use it. The classes after it follow its order, and the first two, LFU Cache and Insert Delete GetRandom O(1), are the designs to know right after LRU.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Count buckets + a minimum pointer** | the truth is key → count; each count has a bucket of keys, oldest first; `min_freq` only resets to 1 or steps up by 1 | LFU Cache (460, below): evict the least frequently used key, ties to the least recently used |
| **Dense list + index map** | a list with no holes answers the random pick; value → index answers membership; delete by moving the last value into the hole | Insert Delete GetRandom O(1) (380, below): insert, remove and a uniform random pick |
| **Heap + lazy deletion** | the dict is the truth; heap entries that disagree with it are skipped when they surface | Stock Price Fluctuation (2034, above); Number Container System (2349): `change(i, x)` fills slot i, `find(x)` is the smallest index holding x; Design a Food Rating System (2353): the best-rated food of a cuisine while ratings change |
| **A heap of free items** | the smallest free seat or id is the heap's top; freeing pushes it back | Seat Reservation Manager (1845): `reserve()` hands out the smallest free seat, `unreserve(s)` gives it back |
| **Counters per line** | row, column and both diagonal sums; a move updates at most 4 counters, a win is a counter reaching ±n | Design Tic-Tac-Toe (348): `move(row, col, player)` returns the winner after the move, or 0 |
| **Deque + set** | the snake's body is a deque (head in, tail out) plus a set for O(1) self-collision checks | Design Snake Game (353): `move(direction)` returns the score, or −1 when the snake hits a wall or itself |
| **Hashing by hand** | an array of short chains at `hash(key) % B`; double B and rehash when chains get long | Design HashMap (706): `put`, `get`, `remove` without built-in hash tables |
| **A cursor and a logical end** | back/forward are index arithmetic; visit overwrites and moves the end | Design Browser History (1472, above) |
| **A snapshot next to each entry** | push (value, min so far) together | Min Stack (155): `push`, `pop`, `top`, `getMin`, all O(1), in [Stacks & Queues](#s07) |
| **Two heaps around the middle** | a max-heap for the low half, a min-heap for the high half, sizes within one | Find Median from Data Stream (295): `addNum`, `findMedian`, in [Heaps](#s13) |
| **A flag and a maintained count** | flip-all toggles one flag; the count of ones is kept current on every write | Design Bitset (2166, below): fix, unfix, flip all and count, each O(1) |
| **Two numbers instead of a log** | tokens left and the time they were counted; each call adds the refill first | a token-bucket rate limiter (below), which allows short bursts |
| **A one-item buffer** | the next item is fetched ahead and kept beside a `done` flag | Peeking Iterator (284): `peek()` without consuming; Flatten Nested List Iterator (341); Zigzag Iterator (281) |
| *Second pass:* **One stack per frequency** | a value pushed c times sits on floors 1..c; pop the top of the highest floor | Maximum Frequency Stack (895, below): pop the most frequent value, the most recent on a tie |
| *Second pass:* **Sorted boundaries + bisect** | intervals stay disjoint and sorted; a change only touches its neighbours | Range Module (715, below): track, untrack and query half-open ranges; Data Stream as Disjoint Intervals (352): `addNum(v)`, `getIntervals()` as merged `[start, end]` pairs |
| *Second pass:* **Count buckets in a linked list** | LRU's list, but each node is a *count* holding a set of keys; ±1 moves a key to the neighbouring bucket | All O'one Data Structure (432): `inc` and `dec` a key's count, `getMaxKey` and `getMinKey`, all O(1) |
| *Second pass:* **Heap of candidates, validated lazily** | a min-heap of indices that may have room; check the top before trusting it | Dinner Plate Stacks (1172): `push` onto the leftmost stack with room, `pop` from the rightmost, `popAtStack(i)` |
| *Second pass:* **Heaps + version stamps** | every state change pushes a fresh entry; stale entries are skipped when they surface | Design Movie Rental System (1912): `search` the five cheapest unrented copies of a movie, `rent`, `drop`, `report` the five cheapest rented |
| *Second pass:* **Trie of dicts** | each path component is an edge; a node is a directory (children) or a file (content) | Design In-Memory File System (588): `ls`, `mkdir`, `addContentToFile`, `readContentFromFile` |
| *Second pass:* **Express lanes** | a sorted linked list plus random-height towers; a search drops a level when it cannot move right | Design Skiplist (1206): `search`, `add`, `erase` in O(log n) expected, no built-in ordered structure |
| *Second pass:* **Positions + random sampling** | value → sorted positions; sample a few indices, verify each with two bisects | Online Majority Element In Subarray (1157): `query(l, r, threshold)`, a value occurring at least `threshold` times in `arr[l..r]`, where `threshold` is more than half its length, or −1 |
| *Second pass:* **Fenwick tree** | point update and prefix sum in O(log n) per axis; a rectangle is 4 prefixes | Range Sum Query 2D - Mutable (308): `update(r, c, v)` and `sumRegion` of a rectangle, interleaved |

LFU Cache comes first because it is the follow-up to LRU: it changes one requirement, and the procedure absorbs it. `get` and `put` stay O(1), every `get` or `put` of a key counts as a use, and when the cache is full the key with the **fewest uses** is evicted, ties going to the least recently used among them. With capacity 2, `put(1, 1)`, `put(2, 2)`, `get(1)`, `put(3, 3)` evicts key 2, which has one use against key 1's two.

Run the method again. `freq_of`, key → count, is the truth; `bucket`, count → an `OrderedDict` of keys, oldest first, is the index that answers "who is the oldest among the rarest?"; one integer `min_freq` says which bucket that is.

The invariant: every key lives in exactly one bucket, `bucket[freq_of[key]]`, and `min_freq` is the smallest non-empty bucket whenever the cache is not empty. One integer can track the minimum because counts only ever go up by one.

The minimum changes in two cases: a brand-new key arrives and `min_freq` becomes 1, or the last key of the minimum bucket moves up and `min_freq` becomes `min_freq + 1`, exactly where that key went. An eviction can empty the lowest floor too, but it only happens right before a new key arrives, so the first case covers it.

```text
counts as floors, each floor a queue (oldest on the left):

freq 1: [2]        freq 2: [1, 3]        min_freq = 1
get(2):   2 climbs to floor 2; floor 1 is now empty and was the min   ->  min_freq = 2
freq 2: [1, 3, 2]                        min_freq = 2
put(4) when full: evict the oldest on the lowest floor (1), THEN 4 enters floor 1   ->  min_freq = 1
freq 1: [4]        freq 2: [3, 2]
```

The class below has two helpers. `_touch` moves a key one floor up and fixes `min_freq` if it emptied the lowest floor; `_evict` pops the oldest key of floor `min_freq`. `put` must evict *before* inserting, because the newcomer, alone on floor 1, would otherwise be its own victim. The prints replay the example, then a tie: keys 1 and 3 both have two uses when key 4 arrives, and the older one leaves.

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
- Delete the two capacity-0 lines at the top of `put` and run `LFUCache(0).put(1, 1)`: `KeyError` again, because the eviction looks for a victim in an empty cache.
- Add `print({f: list(b) for f, b in lfu.bucket.items()}, lfu.min_freq)` after every call and watch keys climb one floor per use.

Insert Delete GetRandom O(1) comes next because it is the same truth-and-index recipe with a new question, a uniform random pick. `insert(v)` and `remove(v)` return whether anything changed, and `getRandom()` returns a uniformly random stored value, each in O(1) on average: `insert(5)`, `insert(8)`, `insert(2)`, `remove(5)` leaves 8 and 2, and `getRandom()` is one of them.

A dense list answers `getRandom`, since `random.choice` needs no holes, and a dict from value to its index answers membership and says where a value sits. A delete moves the last value into the hole, so the list stays dense and nothing shifts. The invariant is `vals[pos[v]] == v` for every stored v, and the last print removes the only element, which is also the last one.

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
one = RandomizedSet()
print(one.insert(7), one.remove(7), one.vals, one.pos)                          # True True [] {}
```

**Try it**
- Move `del self.pos[val]` up, before the line that fills the hole, then remove the only element: `r = RandomizedSet(); r.insert(1); r.remove(1)`. Now `r.pos` is `{1: 0}`, a ghost entry, and `r.insert(1)` returns `False`.
- `Counter(rs.getRandom() for _ in range(3000))`: each of the two values comes up about 1,500 times.
- Delete the line `del self.pos[val]` and rerun: `rs.pos` still lists 5, so `rs.insert(5)` returns `False` although `getRandom` can never return 5. The index (`vals`) and the truth (`pos`) disagree.

Design Bitset comes next because it settles "who pays" with a single flag. `Bitset(size)` starts as all zeros, with `fix(i)` to set a bit, `unfix(i)` to clear it, `flip()` to invert every bit, and `all()`, `one()` and `count()`, each O(1), plus `toString()`, which may walk the bits: `Bitset(5)`, `fix(3)`, `fix(1)`, `flip()` reads `"10101"`.

Flipping every bit is a change of viewpoint, not of data, so keep the physical `bits`, one `flipped` flag and a count `ones`. The invariant: the bit you see at i is `bits[i] ^ flipped`, and `ones` counts the visible ones. `fix(i)` acts only when the visible bit is 0, toggling `bits[i]` and adding one to `ones`, and `unfix` is its mirror. `flip()` toggles the flag and sets `ones = size - ones`; `all`, `one` and `count` read `ones`, and only `toString` walks the bits.

A token bucket comes next because it shows how little state a tracker needs: it is the rate limiter that allows bursts. The bucket holds at most `capacity` tokens and refills at `rate` tokens per second, and `allow(t)` spends one token if there is one, in O(1) time and memory. Instead of remembering requests it keeps two numbers, the tokens left and the time they were last counted, and each call first adds the refill a timer would have added.

With capacity 2 and rate 0.5, three requests at time 0 get yes, yes, no. At time 1 only half a token has dripped in, so no; at time 2 a whole token has, so yes, and the next request at 2 is refused again. By time 6 the bucket has refilled, and the last request passes.

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
- Make it strict: `TokenBucket(capacity=1, rate=0.5)` on the same calls gives `[True, False, False, False, True, False, True]`: capacity 1 allows no burst.

Three follow-ups come up again and again after any tracker. Memory: the Logger's dict keeps every message forever, and a deque of `(t, message)` beside it lets you delete entries older than 10 seconds. O(1)-memory windows: HitCounter's two 300-slot lists, in its Try it above. Concurrency: guard each public method with one `threading.Lock`, so no caller ever sees the truth and an index half-updated.

An iterator with lookahead closes the main path, because it is a design in miniature. Peeking Iterator (284) wraps an ordinary iterator and adds `peek()`, which shows the next item without consuming it, next to `next()` and `hasNext()`, all O(1): over `[1, 2, 3]`, `next()` is 1, `peek()` is 2, and the following `next()` is that same 2.

Keep the next item in a buffer, refilled by `next(self.it)` inside `try / except StopIteration`, plus a separate `done` flag. `hasNext()` returns `not self.done`: a test like `self.buffered is not None` fails when `None` is a real item, and `if self.buffered` fails on 0.

Flatten Nested List Iterator (341) runs `next()` and `hasNext()` over lists nested inside lists, `[[1, 1], 2, [1, 1]]` giving 1, 1, 2, 1, 1, and Zigzag Iterator (281) reads two lists alternately, `[1, 2]` and `[3, 4, 5, 6]` giving 1, 3, 2, 4, 5, 6. Both use the same buffer, and there `hasNext` does the work of finding the next real item.

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Maximum Frequency Stack asks for `push(v)` and a `pop()` that removes and returns the most frequent value, the most recently pushed one on a tie, both in O(1): push 5, 7, 5, 7, 4, 5, and the pops return 5, 7, 5, 4.

Keep `freq[v]`, the truth, one stack per frequency, `group[f]`, holding the values in the order they *reached* f, and `max_freq`. The invariant: a value pushed c times sits once on each floor from 1 to c, so the top of `group[max_freq]` is the most recent of the most frequent values. `push` adds one to `freq[v]`, appends v to that floor and lifts `max_freq` to it. `pop` takes the top of floor `max_freq` and lowers its count; when the floor empties, `max_freq -= 1` is always right, because the floor below still holds the popped value.

Range Module asks for `addRange(l, r)`, `removeRange(l, r)` and `queryRange(l, r)` over half-open ranges `[l, r)` of real numbers, interleaved in any order, where `queryRange` is true when every point of `[l, r)` is tracked: add `[10, 20)`, remove `[14, 16)`, and `[10, 14)` is tracked while `[13, 15)` is not. Adding and removing cost an O(log n) search plus an O(n) splice of a list, and a query two O(log n) searches.

Keep one flat sorted list `ends = [l0, r0, l1, r1, ...]` of disjoint blocks that never touch; the invariant is that `bisect_right(ends, x)` is odd exactly when x lies inside a block. With `i = bisect_left(ends, l)` and `j = bisect_right(ends, r)`, `addRange` replaces `ends[i:j]` with `l` if `i` is even and `r` if `j` is even, which also merges blocks that touch; `removeRange` replaces the same slice with `l` if `i` is odd and `r` if `j` is odd. `queryRange` is true when `bisect_right(ends, l)` and `bisect_left(ends, r)` are the same odd number.

```text
ends = [10, 14, 16, 20]        tracked: [10, 14) and [16, 20)

  x:                    5     12     15     18     25
  bisect_right(ends,x): 0     1      2      3      4
  inside a block?       no    YES    no     YES    no        odd position = inside
```

### Say it in the interview

> "Let me pin down the operations and how often each is called, and ask whether timestamps only increase and whether a write can correct an earlier one. So operation A needs structure X and operation B needs Y. The dict is the source of truth and the others are indexes; the invariant is that they agree. Helpers like `_expire` and `_evict` keep it true, so each public method is a few calls. Cost per operation is ..., and memory is ..."

For LRU that becomes: "`get` and `put` are both O(1). Finding a key means a dict; recency order with O(1) move-to-front and O(1) remove-oldest means a doubly linked list whose nodes the dict points at. The invariant: the dict and the list hold the same keys. Two helpers, unlink and push-front, make `get` and `put` a few lines each; O(1) time, O(capacity) space."

While coding, keep the invariant comment visible in `__init__`, and after each public method say which helper restored it. If the interviewer allows libraries, `OrderedDict` with `move_to_end` and `popitem(last=False)` is the short version; offer to write the linked list yourself.

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
| Maximum Frequency Stack | `design/maximum_frequency_stack.py` | one stack per frequency, a value with count c on floors 1..c; pop the top floor, and max_freq steps down when it empties |
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
