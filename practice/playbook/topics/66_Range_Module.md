## Range Module

Maintain the sorted endpoints of disjoint half-open intervals. The parity of a bisect position tells whether a point is tracked.

<!-- cell -->

Range Module asks for `addRange(l, r)`, `removeRange(l, r)` and `queryRange(l, r)` over half-open ranges `[l, r)` of real numbers, interleaved in any order, where `queryRange` is true when every point of `[l, r)` is tracked: add `[10, 20)`, remove `[14, 16)`, and `[10, 14)` is tracked while `[13, 15)` is not. Adding and removing cost an O(log n) search plus an O(n) splice of a list, and a query two O(log n) searches.

Keep one flat sorted list `ends = [l0, r0, l1, r1, ...]` of disjoint blocks that never touch; the invariant is that `bisect_right(ends, x)` is odd exactly when x lies inside a block. With `i = bisect_left(ends, l)` and `j = bisect_right(ends, r)`, `addRange` replaces `ends[i:j]` with `l` if `i` is even and `r` if `j` is even, which also merges blocks that touch; `removeRange` replaces the same slice with `l` if `i` is odd and `r` if `j` is odd. `queryRange` is true when `bisect_right(ends, l)` and `bisect_left(ends, r)` are the same odd number.

```text
ends = [10, 14, 16, 20]        tracked: [10, 14) and [16, 20)

  x:                    5     12     15     18     25
  bisect_right(ends,x): 0     1      2      3      4
  inside a block?       no    YES    no     YES    no        odd position = inside
```

<!-- cell -->

### Runnable implementation

Adapted from [`design/range_module.py`](../../design/range_module.py).

<!-- cell -->

```python
import random

from bisect import bisect_left, bisect_right

class RangeModule:
    def __init__(self):
        self.ends = []   # sorted boundaries [l0, r0, l1, r1, ...] of disjoint half-open ranges

    def addRange(self, left: int, right: int) -> None:
        i = bisect_left(self.ends, left)      # left == existing end -> i odd, blocks merge
        j = bisect_right(self.ends, right)    # right == existing start -> j odd, blocks merge
        new = []
        if i % 2 == 0:                        # left falls in a gap: it opens the merged block
            new.append(left)
        if j % 2 == 0:                        # right falls in a gap: it closes the merged block
            new.append(right)
        self.ends[i:j] = new                  # every boundary strictly inside is swallowed

    def queryRange(self, left: int, right: int) -> bool:
        i = bisect_right(self.ends, left)
        j = bisect_left(self.ends, right)
        return i == j and i % 2 == 1          # both ends inside the same tracked block

    def removeRange(self, left: int, right: int) -> None:
        i = bisect_left(self.ends, left)
        j = bisect_right(self.ends, right)
        new = []
        if i % 2 == 1:                        # left was inside a block: that block now ends here
            new.append(left)
        if j % 2 == 1:                        # right was inside a block: a block restarts here
            new.append(right)
        self.ends[i:j] = new

r = RangeModule()
r.addRange(10, 20)
r.removeRange(14, 16)
assert r.queryRange(10, 14)
assert not r.queryRange(13, 15)
assert r.queryRange(16, 20)
print(r.ends)  # [10, 14, 16, 20]
```
