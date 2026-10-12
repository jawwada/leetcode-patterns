<a id="hits"></a>

## Hit Counter

**Contract:** `hit(t)` records a hit. `getHits(t)` returns the hits in **`(t - 300, t]`**.
All calls, including reads, have nondecreasing integer timestamps measured in seconds.
Many hits may share a timestamp.

**Q3.** Two hits occur at time 1 and one at time 300. What is `getHits(301)`?
**A.** 3 · **B.** 2 · **C.** 1

**Derive the state:** A deque of individual timestamps works, but a million hits in one second
would occupy a million entries. Store `[timestamp, count]` and a running `total`.

**Invariant:** After cleanup, buckets contain only live seconds and `total` equals their counts' sum.
At time 301, the bucket for time 1 expires **with all of its hits**.

```text
hit(1), hit(1), hit(300):  [[1, 2], [300, 1]]  total = 3
getHits(301):                       [[300, 1]]  total = 1
```

<!-- cell -->

```python
from collections import deque


class HitCounter:
    def __init__(self):
        self.buckets = deque()                 # [timestamp, number of hits]
        self.total = 0

    def _expire(self, t: int) -> None:
        while self.buckets and self.buckets[0][0] <= t - 300:
            _, count = self.buckets.popleft()
            self.total -= count                # Queue and total must change together.

    def hit(self, timestamp: int) -> None:
        self._expire(timestamp)
        if self.buckets and self.buckets[-1][0] == timestamp:
            self.buckets[-1][1] += 1
        else:
            self.buckets.append([timestamp, 1])
        self.total += 1

    def getHits(self, timestamp: int) -> int:
        self._expire(timestamp)                 # Time passes even when no new hit arrives.
        return self.total


hits = HitCounter()
assert hits.getHits(1) == 0
hits.hit(1)
hits.hit(1)
hits.hit(300)
print("At t=300:", hits.getHits(300), list(hits.buckets))
assert hits.getHits(300) == 3
print("At t=301:", hits.getHits(301), list(hits.buckets))
assert hits.getHits(301) == 1
assert hits.getHits(600) == 0

burst = HitCounter()
for _ in range(1000):
    burst.hit(10)
assert len(burst.buckets) == 1
assert burst.getHits(309) == 1000
assert burst.getHits(310) == 0
```

<!-- cell -->

**Cost:** O(1) amortized per operation; at most 300 buckets for integer-second timestamps.
With a configurable window W, space is O(W); one call may expire O(W) buckets.

**Crux:** Cleanup belongs on reads too. If no hits arrive for an hour, the next query must still return 0.
The left boundary is excluded here, so use `<=`, unlike RecentCounter.

**Follow-up:** A circular array of 300 timestamp/count slots also bounds space. Tag each slot
with its timestamp so a slot reused after 300 seconds does not count old hits.

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
elif str(answer).strip().upper() == 'C':
    print("Correct. " + 'At 301 the window is (1, 301]. Both hits at 1 expire, leaving the hit at 300.')
else:
    print("Try again. " + 'At 301 the window is (1, 301]. Both hits at 1 expire, leaving the hit at 300.')
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
