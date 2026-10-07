<a id="logs"></a>

## Log Storage System

**Contract:** `put(id, timestamp)` stores a log. `retrieve(start, end, granularity)` returns
the IDs in an inclusive range, comparing timestamps only through the requested granularity.
Timestamps are valid, zero-padded strings: `YYYY:MM:DD:HH:MM:SS`.
Granularity is `Year`, `Month`, `Day`, `Hour`, `Minute`, or `Second`. Insertion may be out of order;
results may be in any order. Different logs can have the same timestamp.

**Q5.** At `Day` granularity, the endpoints are January 2 at 12:00 and January 2 at 12:01.
Is a log from January 2 at 23:59 included? **A.** Yes · **B.** No

**Derive the state:** We need individual log IDs for historical range queries, so we retain the
logs. Fixed-width strings sort chronologically. At day granularity, compare only the first
10 characters: `2026:01:02`. Hours, minutes, and seconds have no effect.

**Invariant:** Every inserted log appears once in `logs`, including logs that share a timestamp.
The simple solution scans on retrieval. That is a valid starting design with an explicit O(n) query cost.

```text
2026:01:02:23:59:59
----------            Day: first 10 characters
-------               Month: first 7 characters
----                  Year: first 4 characters
```

<!-- cell -->

```python
class LogSystem:
    PREFIX_LENGTH = {"Year": 4, "Month": 7, "Day": 10,
                     "Hour": 13, "Minute": 16, "Second": 19}

    def __init__(self):
        self.logs = []                         # Preserve every (id, timestamp) record.

    def put(self, id: int, timestamp: str) -> None:
        self.logs.append((id, timestamp))

    def retrieve(self, start: str, end: str, granularity: str) -> list[int]:
        length = self.PREFIX_LENGTH[granularity]
        low, high = start[:length], end[:length]
        return [id for id, timestamp in self.logs
                if low <= timestamp[:length] <= high]


logs = LogSystem()
logs.put(1, "2026:01:02:23:59:59")            # Deliberately inserted out of order.
logs.put(2, "2026:01:01:08:00:00")
logs.put(3, "2026:01:02:12:00:00")
logs.put(4, "2026:01:02:12:00:00")            # A second log at the same timestamp.
day = logs.retrieve("2026:01:02:12:00:00", "2026:01:02:12:01:00", "Day")
second = logs.retrieve("2026:01:02:12:00:00", "2026:01:02:12:00:00", "Second")
print("Day query:   ", day)                    # [1, 3, 4]
print("Exact second:", second)                 # [3, 4]
assert day == [1, 3, 4]
assert second == [3, 4]
assert logs.retrieve("2025:01:01:00:00:00", "2025:12:31:23:59:59", "Year") == []
assert logs.retrieve("2026:01:01:00:00:00", "2026:01:01:00:00:00", "Month") == [1, 2, 3, 4]
```

<!-- cell -->

**Cost:** O(1) amortized insertion, O(n) retrieval, O(n) stored logs plus O(k) returned IDs.
Timestamp strings have fixed length.

**Crux:** `Logger` decides whether to print a message; `LogSystem` stores events so you can
retrieve them later. Their APIs require different state.

**Follow-up:** With many queries, maintain a timestamp-sorted index and binary-search range
boundaries. A Python sorted list still needs O(n) insertion when entries arrive out of order;
binary search finds the position in O(log n), but shifting entries costs O(n).
A dictionary keyed only by timestamp would overwrite logs sharing that timestamp.

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
elif str(answer).strip().upper() == 'A':
    print("Correct. " + 'Day granularity ignores hour, minute, and second in both bounds and log timestamps.')
else:
    print("Try again. " + 'Day granularity ignores hour, minute, and second in both bounds and log timestamps.')
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
