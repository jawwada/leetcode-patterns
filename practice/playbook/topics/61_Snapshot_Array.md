## Snapshot Array

Store an ordered version history for each array index. A snapshot advances the version number; it does not copy the whole array.

<!-- cell -->

Snapshot Array is the same idea per index. `SnapshotArray(n)` starts as n zeros; `set(i, v)` writes a cell, `snap()` returns the id of the snapshot just taken, counting from 0, and `get(i, snap_id)` returns the cell as it was in that snapshot, and no call may copy the array: after `set(0, 5)`, `snap()` → 0 and `set(0, 6)`, the call `get(0, 0)` is 5.

Give each cell its own history, a list of `(snap_id, value)` pairs that starts as `[(0, 0)]`, and keep one counter `snap_id`, the id of the snapshot still open. The invariant: every history is sorted by id and holds one pair per id at most. So `set` overwrites the last pair when its id is the open one and appends otherwise, `snap` returns the counter and adds one, and `get` is `bisect_right(hist[i], (snap_id, inf))` and one step back, the TimeMap read. Writes are O(1), a read O(log n).

<!-- cell -->

### Runnable implementation

Adapted from [`design/snapshot_array.py`](../../design/snapshot_array.py).

<!-- cell -->

```python
import random

from bisect import bisect_right

class SnapshotArray:
    def __init__(self, length: int):
        self.hist = [[(0, 0)] for _ in range(length)]   # per index: (snap_id, value), ascending
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        h = self.hist[index]
        if h[-1][0] == self.snap_id:
            h[-1] = (self.snap_id, val)       # overwrite: same snapshot, keep one pair
        else:
            h.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        h = self.hist[index]
        i = bisect_right(h, (snap_id, float("inf")))   # first pair written after snap_id
        return h[i - 1][1]

s = SnapshotArray(2)
s.set(0, 5)
first = s.snap()
s.set(0, 6)
assert s.get(0, first) == 5
assert s.get(1, first) == 0
print(s.get(0, first))  # 5
```
