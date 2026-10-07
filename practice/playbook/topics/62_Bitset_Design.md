## Bitset API Design

A lazy flip flag changes the meaning of all stored bits in O(1). Maintain the count of visible ones alongside the underlying bits.

<!-- cell -->

Design Bitset comes next because it settles "who pays" with a single flag. `Bitset(size)` starts as all zeros, with `fix(i)` to set a bit, `unfix(i)` to clear it, `flip()` to invert every bit, and `all()`, `one()` and `count()`, each O(1), plus `toString()`, which may walk the bits: `Bitset(5)`, `fix(3)`, `fix(1)`, `flip()` reads `"10101"`.

Flipping every bit is a change of viewpoint, not of data, so keep the physical `bits`, one `flipped` flag and a count `ones`. The invariant: the bit you see at i is `bits[i] ^ flipped`, and `ones` counts the visible ones. `fix(i)` acts only when the visible bit is 0, toggling `bits[i]` and adding one to `ones`, and `unfix` is its mirror. `flip()` toggles the flag and sets `ones = size - ones`; `all`, `one` and `count` read `ones`, and only `toString` walks the bits.

<!-- cell -->

### Runnable implementation

Adapted from [`design/design_bitset.py`](../../design/design_bitset.py).

<!-- cell -->

```python
import random

class Bitset:
    def __init__(self, size: int):
        self.bits = [0] * size     # physical bits; logical bit = physical ^ flipped
        self.flipped = 0
        self.ones = 0              # count of logical ones

    def _logical(self, idx: int) -> int:
        return self.bits[idx] ^ self.flipped

    def fix(self, idx: int) -> None:
        if not self._logical(idx):
            self.bits[idx] ^= 1
            self.ones += 1

    def unfix(self, idx: int) -> None:
        if self._logical(idx):
            self.bits[idx] ^= 1
            self.ones -= 1

    def flip(self) -> None:
        self.flipped ^= 1                      # O(1): change the lens, not the bits
        self.ones = len(self.bits) - self.ones

    def all(self) -> bool:
        return self.ones == len(self.bits)

    def one(self) -> bool:
        return self.ones > 0

    def count(self) -> int:
        return self.ones

    def toString(self) -> str:
        return "".join("1" if b ^ self.flipped else "0" for b in self.bits)

b = Bitset(5)
b.fix(3)
b.fix(1)
b.flip()
assert b.toString() == "10101"
assert b.count() == 3
assert b.one() and not b.all()
print(b.toString())  # 10101
```
