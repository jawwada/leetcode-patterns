<a id="recent"></a>

## Recent Counter

**Contract:** `ping(t)` records a request and returns the number in **`[t - 3000, t]`**,
including the new request. Integer timestamps are strictly increasing; time is in milliseconds.

**Q2.** After `ping(1)`, what does `ping(3001)` return? **A.** 1 · **B.** 2 · **C.** 0

**Derive the state:** An all-history list needs a full scan per query. Since time increases,
expired events form a prefix and can never become relevant again. Keep the live suffix in a deque.

**Invariant:** After `ping(t)`, the deque contains exactly the requests in `[t - 3000, t]`, oldest first.

```text
ping(1):     [1]                  -> 1
ping(100):   [1, 100]             -> 2
ping(3001):  [1, 100, 3001]       -> 3  (1 is exactly on the boundary)
ping(3002):  [100, 3001, 3002]    -> 3  (1 has expired)
```

<!-- cell -->

```python
from collections import deque


class RecentCounter:
    def __init__(self):
        self.window = deque()

    def ping(self, t: int) -> int:
        self.window.append(t)                  # This request always counts.
        while self.window and self.window[0] < t - 3000:
            self.window.popleft()              # Equality is inside this window.
        return len(self.window)


recent = RecentCounter()
answers = []
for t in [1, 100, 3001, 3002]:
    answers.append(recent.ping(t))
    print(f"ping({t:4}) -> {answers[-1]}   window={list(recent.window)}")
assert answers == [1, 2, 3, 3]

edge = RecentCounter()
assert edge.ping(1) == 1
assert edge.ping(3001) == 2
assert edge.ping(6002) == 1                 # Both earlier requests have expired.
```

<!-- cell -->

**Cost:** O(1) amortized per call, O(K) space for K live requests. One call can remove K
expired requests and take O(K), but each request enters once and leaves at most once.
Under the strictly increasing integer-millisecond contract, at most 3001 timestamps fit in the window.

**Crux:** This counter records **every** request. It does not decide whether to allow the request.
Changing `<` to `<=` would incorrectly remove the event exactly 3000 milliseconds old.

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
    print("Correct. " + 'The window is [1, 3001]; both requests are included. RecentCounter expires with <.')
else:
    print("Try again. " + 'The window is [1, 3001]; both requests are included. RecentCounter expires with <.')
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
