## Maximum Frequency Stack

Group pushes by the frequency they reach. Pop from the highest frequency, in last-in-first-out order.

<!-- cell -->

Maximum Frequency Stack asks for `push(v)` and a `pop()` that removes and returns the most frequent value, the most recently pushed one on a tie, both in O(1): push 5, 7, 5, 7, 4, 5, and the pops return 5, 7, 5, 4.

Keep `freq[v]`, the truth, one stack per frequency, `group[f]`, holding the values in the order they *reached* f, and `max_freq`. The invariant: a value pushed c times sits once on each floor from 1 to c, so the top of `group[max_freq]` is the most recent of the most frequent values. `push` adds one to `freq[v]`, appends v to that floor and lifts `max_freq` to it. `pop` takes the top of floor `max_freq` and lowers its count; when the floor empties, `max_freq -= 1` is always right, because the floor below still holds the popped value.

<!-- cell -->

### Runnable implementation

Adapted from [`design/maximum_frequency_stack.py`](../../design/maximum_frequency_stack.py).

<!-- cell -->

```python
import random

from collections import Counter, defaultdict

class FreqStack:
    def __init__(self):
        self.freq = defaultdict(int)             # val -> current frequency
        self.group = defaultdict(list)           # frequency -> stack of vals that reached it
        self.maxfreq = 0

    def push(self, val: int) -> None:
        self.freq[val] += 1
        f = self.freq[val]
        self.group[f].append(val)                # val is now the newest at frequency f
        self.maxfreq = max(self.maxfreq, f)

    def pop(self) -> int:
        val = self.group[self.maxfreq].pop()     # most recent among the most frequent
        if not self.group[self.maxfreq]:
            self.maxfreq -= 1                    # group[maxfreq-1] is guaranteed non-empty
        self.freq[val] -= 1
        return val

s = FreqStack()
for value in [5, 7, 5, 7, 4, 5]:
    s.push(value)
answers = [s.pop() for _ in range(4)]
assert answers == [5, 7, 5, 4]
print(answers)
```
