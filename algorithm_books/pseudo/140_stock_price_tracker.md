---
rank: 140
slug: stock_price_tracker
---

A feed delivers stock prices as `(timestamp, price)` records, not necessarily in time order, and a later record may correct the price at an earlier timestamp. Design `update(timestamp, price)`, `current()` for the price at the latest timestamp, and `maximum()` and `minimum()` over the current prices of all timestamps. After `update(1, 10)`, `update(2, 5)` and the correction `update(1, 3)`, the current price is `5`, the maximum is `5` and the minimum is `3`: the `10` no longer exists.

A map from timestamp to price, plus the largest timestamp seen, answers `update` and `current` in `O(1)`. The extremes are the hard part. Rescanning the map costs `O(n)` per query, and a plain binary heap has no fast way to do what a correction asks for, which is to delete an arbitrary old price from its middle. The way out is not to delete it at all. Every update pushes a record `(price, timestamp)` into a max-heap and a min-heap and leaves the older records of that timestamp where they are. A record is stale when the map now holds a different price for its timestamp, and since the map is the single source of truth, telling stale from live costs one lookup. A query looks at its heap's top and pops it while it is stale; the first record that agrees with the map is the answer, because every live price has a record in each heap, so anything that outranks the true maximum must be stale.

Picture each heap as a deck in which outdated cards stay put until they surface and are thrown away. Each record is pushed once and popped at most once, so however long one query's cleanup runs, the total work over all calls is bounded by the pushes, which makes every call amortized `O(log n)`. Stale records buried below the top cost memory but never a wrong answer.

```text
price@time is a record; ✗ marks one the map has since corrected
call            prices              max-heap, top first   min-heap, top first
update(1, 10)   {1: 10}             10@1                  10@1
update(2, 5)    {1: 10, 2: 5}       10@1 5@2              5@2 10@1
current() → 5   latest is 2, and prices[2] = 5
maximum() → 10  top 10@1 agrees with prices[1] = 10
update(1, 3)    {1: 3, 2: 5}        10@1✗ 5@2 3@1         3@1 5@2 10@1✗
maximum() → 5   pop 10@1✗, since prices[1] = 3; then top 5@2 agrees
                                    5@2 3@1
minimum() → 3   top 3@1 agrees; 10@1✗ stays buried in the min-heap
update(4, 2)    {1: 3, 2: 5, 4: 2}  5@2 3@1 2@4           2@4 3@1 5@2 10@1✗
current() → 2   latest is 4;  minimum() → 2 at once: top 2@4 agrees
heap sizes 3 and 4: the min-heap still holds the stale 10@1
```

```pseudo
CLASS StockPrice
    FUNCTION Init()
        self.prices ← empty map             // timestamp → its current price
        self.latest ← 0                     // the largest timestamp so far
        self.max_heap ← empty max-heap      // (price, timestamp) records
        self.min_heap ← empty min-heap      // (price, timestamp) records

    FUNCTION Update(timestamp, price)
        self.prices[timestamp] ← price      // older records of it go stale
        IF timestamp > self.latest
            self.latest ← timestamp
        self.max_heap.push((price, timestamp))
        self.min_heap.push((price, timestamp))

    FUNCTION Current()
        RETURN self.prices[self.latest]

    FUNCTION Maximum()
        WHILE true
            (price, timestamp) ← self.max_heap.top()
            IF self.prices[timestamp] = price
                RETURN price                // the record is still true
            self.max_heap.pop()             // stale: corrected since

    FUNCTION Minimum()
        WHILE true
            (price, timestamp) ← self.min_heap.top()
            IF self.prices[timestamp] = price
                RETURN price
            self.min_heap.pop()
```

`update` costs `O(log n)` for its two pushes, `current` costs `O(1)`, and `maximum` and `minimum` cost amortized `O(log n)`, where `n` counts the updates; the heaps hold one record per update, so a storm of corrections to one timestamp bloats them, and rebuilding both from the map with the `O(n)` heapify of #59 whenever they pass twice the number of live prices keeps the memory in check. The sorted-container alternative keeps the current prices in sorted order, as counts per price in Java's `TreeMap`, a balanced search tree, or as a multiset in the third-party Python `SortedList`: an update removes the old price and adds the new one, and the extremes are the two ends, `O(log n)` per call and never a stale entry. Lazy deletion is the template for tracker designs. One map holds the truth, ordered views are allowed to fall behind it, and every read checks its answer against the map: leaderboards and top-k trackers keep score maps with lazy heaps, Design a Number Container System keeps a min-heap of indices per number and discards an index whose number has changed, and the expiring cache of #94 checks every deadline it pops against its map the same way. The classic mistakes are trusting the heap top without the map check, which reports the corrected-away `10` as the maximum, and moving `latest` to every incoming timestamp, which makes `current()` return `3` after the correction `update(1, 3)` instead of `5`.

*Practice:* LC 2034 Stock Price Fluctuation · LC 1244 Design A Leaderboard · LC 2349 Design a Number Container System
