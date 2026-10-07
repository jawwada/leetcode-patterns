<a id="average"></a>

## Moving Average

**Contract:** `MovingAverage(size).next(value)` returns the average of the latest `size`
values, or all values received so far if fewer have arrived. `size` is a positive integer.
This is a **count window**; timestamps are irrelevant.

**Q6.** Size is 3, and the only value received is 9. The answer is **A.** 3 · **B.** 9 · **C.** 0.

**Derive the state:** Recomputing the sum each time repeats work. Preserve the running sum,
but also preserve the deque so we know which value to subtract when it leaves.

**Invariant:** `total == sum(window)`, and the window holds at most `size` latest values.

```text
size = 3
[1, 10, 3]  total = 14
append 5, remove 1
[10, 3, 5]  total = 14 + 5 - 1 = 18  -> average 6
```

<!-- cell -->

```python
from collections import deque
from math import isclose


class MovingAverage:
    def __init__(self, size: int):
        if type(size) is not int or size <= 0:
            raise ValueError("size must be a positive integer")
        self.size = size
        self.window = deque()
        self.total = 0

    def next(self, val: int) -> float:
        self.window.append(val)
        self.total += val
        if len(self.window) > self.size:
            self.total -= self.window.popleft()
        return self.total / len(self.window)   # Divide by actual count during warm-up.


average = MovingAverage(3)
answers = [average.next(v) for v in [1, 10, 3, 5]]
print(answers)                               # [1.0, 5.5, 4.666..., 6.0]
assert all(isclose(a, b) for a, b in zip(answers, [1.0, 5.5, 14 / 3, 6.0]))
single = MovingAverage(1)
assert single.next(4) == 4.0
assert single.next(-2) == -2.0
assert MovingAverage(3).next(9) == 9.0
```

<!-- cell -->

**Cost:** O(1) per call, O(size) space. At most one value expires on each call.

**Crux:** A running sum alone is insufficient because we must know the outgoing value.
The deque supplies that value. Dividing by the capacity before the window fills gives the wrong mean.

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
    print("Correct. " + 'Only one value has arrived, so divide 9 by 1, not by the capacity 3.')
else:
    print("Try again. " + 'Only one value has arrived, so divide 9 by 1, not by the capacity 3.')
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
