<a id="history"></a>

## Time-Based Key-Value Store

**Contract:** `set(key, value, timestamp)` records a version. `get(key, timestamp)` returns
the value with the greatest stored time **≤ the query time**, or `""` if none exists.
`set` timestamps strictly increase; queries may ask about any earlier time.

**Q8.** Values `"red"` and `"blue"` are stored at times 1 and 4. What does `get(key, 4)` return?
**A.** `"red"` · **B.** `"blue"` · **C.** `""`

**Derive the state:** Keeping only the latest value loses answers to older queries.
Preserve versions in timestamp order. Binary search finds the last timestamp ≤ the query.

**Invariant:** Each key's timestamp list is increasing and aligned with its value list.

```text
times:   [1,     4,      9]
values:  ["red", "blue", "green"]
get(5): bisect_right(times, 5) = 2 -> step left to index 1 -> "blue"
get(4): bisect_right(times, 4) = 2 -> index 1 -> exact match "blue"
get(0): bisect_right(times, 0) = 0 -> no earlier version -> ""
```

<!-- cell -->

```python
from bisect import bisect_right


class TimeMap:
    def __init__(self):
        self.history = {}                      # key -> (timestamps, values)

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.history:
            self.history[key] = ([], [])
        times, values = self.history[key]
        times.append(timestamp)               # Increasing writes keep this sorted.
        values.append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.history:
            return ""
        times, values = self.history[key]
        i = bisect_right(times, timestamp)     # First position strictly after the query.
        return values[i - 1] if i > 0 else ""


versions = TimeMap()
versions.set("color", "red", 1)
versions.set("color", "blue", 4)
versions.set("color", "green", 9)
answers = [versions.get("color", t) for t in [0, 1, 3, 4, 5, 20]]
print(answers)                               # ['', 'red', 'red', 'blue', 'blue', 'green']
assert answers == ["", "red", "red", "blue", "blue", "green"]
assert versions.get("missing", 100) == ""
assert versions.get("color", 1) == "red"     # Old queries remain valid after new writes.
```

<!-- cell -->

**Cost:** O(1) amortized `set`, O(log V) `get` for V versions of the queried key,
O(N) space for N stored versions.

**Crux:** `bisect_right` places the search boundary after equal timestamps. Stepping left
then includes an exact match. If `i == 0`, there is no answer; using `values[-1]` would return
the newest value incorrectly.

**Follow-up:** Out-of-order writes break append-sorted history. Sorted list insertion restores
correctness with O(V) insertion time, or use a suitable ordered index. Unlike expiring counters,
this contract needs old records because queries may move backward in time.

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
    print("Correct. " + 'Time 4 is included by <=. bisect_right steps past the equal time, then we move left.')
else:
    print("Try again. " + 'Time 4 is included by <=. bisect_right steps past the equal time, then we move left.')
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
