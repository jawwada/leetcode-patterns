<a id="trips"></a>

## Underground System

**Contract:** `checkIn(id, station, t)` begins a journey; `checkOut(id, station, t)` ends it.
`getAverageTime(start, end)` returns the mean duration of all completed trips on that directed route.
Check-ins/check-outs are valid, and queried routes have at least one completed trip.

**Q7.** Completed trips from A to B take 10 and 20 minutes. A third customer is still traveling.
What should the average be? **A.** 10 · **B.** 15 · **C.** We must wait for the third customer.

**Derive the state:** Checkout needs the customer's starting location/time, so use an active-trip map.
Completed trips are only queried for their average, so compress them into `(sum, count)` per route.

**Invariant:** `active` holds exactly unfinished journeys. `stats[(start, end)]` holds the total
duration and count of completed trips for that direction.

```text
checkIn(7, "A", 3):    active[7] = ("A", 3)
checkOut(7, "B", 13):  remove active[7]; stats[("A", "B")] += (10, 1)
```

<!-- cell -->

```python
class UndergroundSystem:
    def __init__(self):
        self.active = {}                       # customer -> (start station, start time)
        self.stats = {}                        # directed route -> [duration sum, trip count]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.active[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start, start_time = self.active.pop(id)
        route = (start, stationName)
        if route not in self.stats:
            self.stats[route] = [0, 0]
        self.stats[route][0] += t - start_time
        self.stats[route][1] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total, count = self.stats[(startStation, endStation)]
        return total / count


trips = UndergroundSystem()
trips.checkIn(1, "A", 0)
trips.checkIn(2, "A", 2)
trips.checkOut(1, "B", 10)                    # Duration 10.
trips.checkOut(2, "B", 22)                    # Duration 20.
trips.checkIn(3, "A", 23)                     # Unfinished; must not change the average.
print("A -> B:", trips.getAverageTime("A", "B"))  # 15.0
assert trips.getAverageTime("A", "B") == 15.0

trips.checkIn(1, "B", 24)                     # The same customer can start another trip.
trips.checkOut(1, "A", 29)
assert trips.getAverageTime("B", "A") == 5.0  # Reverse direction is a different route.
assert trips.getAverageTime("A", "B") == 15.0
trips.checkOut(3, "C", 30)
assert trips.getAverageTime("A", "C") == 7.0  # Same start, different destination.
assert not trips.active
```

<!-- cell -->

**Cost:** O(1) per operation; O(A + R) space for A active customers and R completed-route keys.

**Crux:** `pop(id)` both retrieves the unfinished journey and removes it from active state.
Store totals and counts, not a running average of averages: groups with different trip counts
must have different weights. If the API later asks for the median or individual trips,
`(sum, count)` will no longer be sufficient.

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
    print("Correct. " + 'Only completed journeys count: (10 + 20) / 2 = 15.')
else:
    print("Try again. " + 'Only completed journeys count: (10 + 20) / 2 = 15.')
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
