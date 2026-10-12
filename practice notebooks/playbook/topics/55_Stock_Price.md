<a id="prices"></a>

## Stock Price Tracker

**Contract:** `update(timestamp, price)` inserts or corrects a price. Updates can arrive out of order.
`current()` returns the price at the **greatest timestamp**. `minimum()` and `maximum()` return
the lowest and highest prices among the current records. Queries occur after at least one update.

**Q9.** Run `update(1, 10)`, `update(2, 5)`, `update(1, 3)`.
What are `(current(), maximum())`? **A.** `(3, 10)` · **B.** `(5, 5)` · **C.** `(3, 5)`

**Derive the state:** A dictionary answers corrections and current price, but finding min/max by
scanning it costs O(n) per query. Add two heaps for extremes. A correction makes older heap
entries potentially invalid; removing an arbitrary heap entry is inconvenient.
Instead, check entries against the dictionary when they reach the top and discard invalid ones.
This is **lazy deletion**.

**Invariant:** `prices[t]` is the authoritative price for t; both heaps contain an entry for every
current `(t, price)` pair, and may also contain obsolete entries. Clean a heap's top before using it.

```text
update(1, 10)   prices = {1: 10}
update(2, 5)    prices = {1: 10, 2: 5}   latest timestamp = 2
update(1, 3)    prices = {1:  3, 2: 5}   latest timestamp stays 2
maximum()      old heap entry (10, 1) disagrees with prices[1] = 3 -> discard
               next valid maximum is 5
```

<!-- cell -->

```python
import heapq


class StockPrice:
    def __init__(self):
        self.prices = {}
        self.latest = None
        self.low = []                          # (price, timestamp)
        self.high = []                         # (-price, timestamp): simulate a max heap

    def update(self, timestamp: int, price: int) -> None:
        self.prices[timestamp] = price
        if self.latest is None or timestamp > self.latest:
            self.latest = timestamp
        heapq.heappush(self.low, (price, timestamp))
        heapq.heappush(self.high, (-price, timestamp))

    def current(self) -> int:
        return self.prices[self.latest]

    def minimum(self) -> int:
        while self.low[0][0] != self.prices[self.low[0][1]]:
            heapq.heappop(self.low)
        return self.low[0][0]

    def maximum(self) -> int:
        while -self.high[0][0] != self.prices[self.high[0][1]]:
            heapq.heappop(self.high)
        return -self.high[0][0]


prices = StockPrice()
prices.update(1, 10)
prices.update(2, 5)
prices.update(1, 3)
print("Current, maximum, minimum:", prices.current(), prices.maximum(), prices.minimum())
assert (prices.current(), prices.maximum(), prices.minimum()) == (5, 5, 3)
prices.update(2, 8)
assert prices.current() == 8                  # A correction to the latest timestamp counts.
assert prices.maximum() == 8
assert prices.minimum() == 3

stale = StockPrice()
for t, p in [(1, 10), (2, 9), (1, 1), (2, 2)]:
    stale.update(t, p)
assert stale.maximum() == 2                  # Must discard TWO obsolete tops: use while.
stale_min = StockPrice()
for t, p in [(1, 1), (2, 2), (1, 10), (2, 9)]:
    stale_min.update(t, p)
assert stale_min.minimum() == 9
```

<!-- cell -->

**Cost:** With U updates so far, `update` costs O(log(U + 1)), `current` O(1), and storage O(U).
A min/max query can remove many obsolete entries, so its worst case is O(U log(U + 1)).
Across U updates and Q queries, total work is O(U log(U + 1) + Q): each entry is pushed once
and popped at most once from each heap. Space is based on **updates**, not just distinct timestamps.

**Crux:** A heap is an index for a particular query. The dictionary determines whether a heap
entry is still correct. Use `while`, since several obsolete entries may be at the top in succession.
Do not set `latest = timestamp` unconditionally: the most recent method call may correct an old time.

**Follow-up:** To control obsolete-entry memory, periodically rebuild heaps from the dictionary
when heap size becomes much larger than the number of live timestamps.

<!-- cell -->

### Check your prediction

Set `answer` to your letter, then run the next cell. The feedback applies to this notebook's question.

<!-- cell -->

```python
answer = None  # Enter "A", "B", or "C".
```

<!-- cell -->

```python
if answer is None:
    print("Choose an answer above, then rerun this cell.")
elif str(answer).strip().upper() == 'B':
    print("Correct. " + 'Timestamp 2 is still latest, with price 5. The obsolete maximum 10 must be discarded.')
else:
    print("Try again. " + 'Timestamp 2 is still latest, with price 5. The obsolete maximum 10 must be discarded.')
```

<!-- cell -->

### Your implementation space

Write the state and invariant first, then implement this API without looking at the solution.

<!-- cell -->

```python
# State:
# Invariant:
# Your implementation:
```
