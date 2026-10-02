"""
Design Bitset (LeetCode 2166)  — Medium
Pattern: Lazy global flip flag + maintained count

Problem
-------
Implement Bitset(size), all bits 0, with fix(idx) set to 1, unfix(idx) set to 0, flip() invert
every bit, all() -> every bit is 1, one() -> at least one bit is 1, count() -> number of 1s,
toString() -> the bits as a string. All but toString should be O(1).
Example: Bitset(5); fix(3); fix(1); flip() -> "10101"; all() False; unfix(0) -> "00101";
flip() -> "11010"; one() True; unfix(0) -> "01010"; count() 2; toString() "01010".

Brute force
-----------
A list of bits. fix/unfix are O(1), but flip walks the whole list inverting each bit, and all,
one and count each walk the whole list again. O(size) for four of the seven operations, O(size)
space. The wasted work is touching every bit to answer questions that could be maintained
incrementally (count) or deferred (flip): flipping twice is a no-op, so eagerly rewriting n
bits for each flip is pure waste.

From brute force to optimal
---------------------------
Two independent observations. First, the number of ones is a single integer that changes by
+1/-1 on fix/unfix and becomes size - ones on flip, so all/one/count are O(1) reads of it.
Second, a flip need not touch any bit: keep a boolean `flipped` and define the logical bit as
physical ^ flipped. fix/unfix read the logical bit, and if it must change, XOR the physical bit
and adjust ones. The tracker remembers the physical bits, one flag and one counter; it never
materialises the flipped array until toString is asked for it.

Intuition
---------
A global flip is a change of viewpoint, not a change of data: "read every bit through an
inverter". Recording the viewpoint in one flag makes flip O(1) and leaves fix/unfix O(1)
because they only need to consult that flag. The count is the only aggregate the queries need,
and it is cheap to keep exact.

Geometric view
--------------
Draw the bits as columns and the flag as a lens over them:
physical:  0 1 0 1 0      flipped = 1      ones = 3
logical :  1 0 1 0 1      (what the user sees: "10101")
unfix(0): logical bit 0 is 1 -> XOR physical[0] -> physical 1 1 0 1 0, logical 0 0 1 0 1, ones 2.
flip():   flipped = 0, ones = 5 - 2 = 3 -> logical now equals physical "11010".

Steps
-----
1. bits = [0]*size; flipped = 0; ones = 0.
2. logical(idx) = bits[idx] ^ flipped.
3. fix: if logical is 0 -> bits[idx] ^= 1; ones += 1. unfix symmetric with ones -= 1.
4. flip: flipped ^= 1; ones = size - ones.
5. all: ones == size; one: ones > 0; count: ones.
6. toString: join "1" if bit ^ flipped else "0" over bits (the only O(size) call).

Complexity: O(1) time per operation except toString O(size), O(size) space —
            a flag and a counter replace full passes.
Pitfalls: fix on an already-set bit must not change the count; forgetting to apply the flag in
          toString; recomputing count = size - count only on flip, not on fix/unfix.
"""
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


class BruteForce:
    """Plain bit list; flip, all, one and count each walk every bit, O(size)."""

    def __init__(self, size: int):
        self.bits = [0] * size

    def fix(self, idx: int) -> None:
        self.bits[idx] = 1

    def unfix(self, idx: int) -> None:
        self.bits[idx] = 0

    def flip(self) -> None:
        self.bits = [1 - b for b in self.bits]       # O(size)

    def all(self) -> bool:
        return all(self.bits)

    def one(self) -> bool:
        return any(self.bits)

    def count(self) -> int:
        return sum(self.bits)

    def toString(self) -> str:
        return "".join(map(str, self.bits))


if __name__ == "__main__":
    b = Bitset(5)
    b.fix(3)
    b.fix(1)
    b.flip()
    assert b.toString() == "10101"
    assert b.all() is False
    b.unfix(0)
    assert b.toString() == "00101"
    b.flip()
    assert b.toString() == "11010"
    assert b.one() is True
    b.unfix(0)
    assert b.toString() == "01010"
    assert b.count() == 2
    assert b.toString() == "01010"

    e = Bitset(1)                              # edge: single bit, double fix, double flip
    e.fix(0)
    e.fix(0)
    assert e.all() and e.count() == 1
    e.flip()
    e.flip()
    assert e.toString() == "1"

    random.seed(10)
    n = 7
    fast, slow = Bitset(n), BruteForce(n)
    for _ in range(2000):
        op = random.choice(["fix", "unfix", "flip", "q"])
        if op == "fix":
            i = random.randrange(n)
            fast.fix(i)
            slow.fix(i)
        elif op == "unfix":
            i = random.randrange(n)
            fast.unfix(i)
            slow.unfix(i)
        elif op == "flip":
            fast.flip()
            slow.flip()
        assert (fast.all(), fast.one(), fast.count(), fast.toString()) == \
               (slow.all(), slow.one(), slow.count(), slow.toString())
    print("ok")
