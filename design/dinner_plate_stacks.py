"""
Dinner Plate Stacks (LeetCode 1172)  — Hard
Pattern: List of stacks + min-heap of "has room" indices with lazy invalidation

Problem
-------
Infinitely many stacks in a row, each holding at most capacity plates. push(val) puts the plate
on the LEFTMOST stack with room; pop() removes from the RIGHTMOST non-empty stack; popAtStack(i)
removes the top of stack i. Both pops return -1 when nothing is there.
Example: capacity=2; push 1,2,3,4,5 -> [1,2][3,4][5]; popAtStack(0) -> 2; push(20) lands on
stack 0 -> [1,20][3,4][5]; pop() -> 5.

Brute force
-----------
Keep a list of stacks. push scans from the left for the first stack that is not full; pop walks
back over trailing empty stacks; popAtStack indexes directly. push is O(k) for k stacks, the
pops are O(1) amortised, O(n) space. The wasted work is the push scan: it rewalks every full
stack from index 0 on every push, although a full stack only regains room through popAtStack.

From brute force to optimal
---------------------------
The redundancy is rescanning stacks that are known to be full. Room appears in exactly one way,
popAtStack(i), so record "i may have room" at that moment in a min-heap; push then reads the
smallest such index instead of scanning. Entries go stale in two ways: the stack filled up again
(a later push took the room) or it was trimmed away when the right edge shrank. Rather than
deleting entries eagerly, drop them lazily when they surface at the heap top and fail the check
(index >= len(stacks) or stack is full). The invariant: trailing empty stacks are always removed
after a pop, so pop() is simply popAtStack(len(stacks) - 1). Each heap entry is pushed once and
popped once, so every operation is amortised O(log n).

Intuition
---------
Two edges matter: the leftmost stack with a hole (for push) and the rightmost non-empty stack
(for pop). The right edge is just the end of the list if we trim empties. The left hole is a
min over a set that only changes at popAtStack (hole appears) and push (hole may close), so a
heap with lazy deletion tracks it without ever scanning.

Geometric view
--------------
A row of columns growing to the right. The heap is a set of flags planted on columns that were
dug into from above; push always goes to the leftmost flag, removing it when the column is full
again. pop chips at the rightmost column and knocks down any empty columns at the right end;
flags left standing on knocked-down columns are swept away when they come up for a push.

Steps
-----
1. State: stacks (list of lists), open (min-heap of indices that may have room), cap.
2. push: pop stale heap tops (index out of range or stack full). If heap empty, append a new
   stack and push its index. Append val to stacks[open[0]]; if it is now full, pop that index.
3. popAtStack(i): if i out of range or empty -> -1. Pop the top, push i into the heap, then
   trim empty stacks off the right end.
4. pop(): popAtStack(len(stacks) - 1) (returns -1 when there are no stacks).

Complexity: O(log n) amortised per operation, O(n) space — each heap entry is pushed and popped
            at most once; stacks hold n plates total.
Pitfalls: not trimming trailing empty stacks (pop returns -1 while plates remain to the left);
          trusting heap indices without re-checking (push into a full or vanished stack);
          duplicates in the heap are fine, but only if every top is validated before use.
"""
import random
from heapq import heappop, heappush


class DinnerPlates:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.stacks = []                     # stacks[i] is a list; last one is never empty
        self.open = []                       # min-heap of indices that MAY have room (lazy)

    def push(self, val: int) -> None:
        while self.open:
            i = self.open[0]
            if i < len(self.stacks) and len(self.stacks[i]) < self.cap:
                break
            heappop(self.open)               # stale: that stack was trimmed away or filled up
        if not self.open:
            self.stacks.append([])
            heappush(self.open, len(self.stacks) - 1)
        i = self.open[0]
        self.stacks[i].append(val)
        if len(self.stacks[i]) == self.cap:
            heappop(self.open)               # no room left: retire the index

    def pop(self) -> int:
        return self.popAtStack(len(self.stacks) - 1)

    def popAtStack(self, index: int) -> int:
        if index < 0 or index >= len(self.stacks) or not self.stacks[index]:
            return -1
        val = self.stacks[index].pop()
        heappush(self.open, index)           # a hole opened here
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()                # keep the right edge on a non-empty stack
        return val


class BruteForce:
    """List of stacks; push scans left to right for the first stack with room."""

    def __init__(self, capacity: int):
        self.cap = capacity
        self.stacks = []

    def push(self, val: int) -> None:
        for st in self.stacks:               # O(k) scan over every stack
            if len(st) < self.cap:
                st.append(val)
                return
        self.stacks.append([val])

    def pop(self) -> int:
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        return self.stacks[-1].pop() if self.stacks else -1

    def popAtStack(self, index: int) -> int:
        if index < len(self.stacks) and self.stacks[index]:
            return self.stacks[index].pop()
        return -1


if __name__ == "__main__":
    d = DinnerPlates(2)
    for v in (1, 2, 3, 4, 5):
        d.push(v)                            # [1,2] [3,4] [5]
    assert d.popAtStack(0) == 2              # [1]   [3,4] [5]
    d.push(20)                               # [1,20][3,4] [5]
    d.push(21)                               # [1,20][3,4] [5,21]
    assert d.popAtStack(0) == 20
    assert d.popAtStack(2) == 21
    assert d.pop() == 5
    assert d.pop() == 4
    assert d.pop() == 3
    assert d.pop() == 1
    assert d.pop() == -1                     # everything is gone
    assert DinnerPlates(1).popAtStack(5) == -1

    random.seed(2)
    for cap in (1, 2, 3):
        fast, slow = DinnerPlates(cap), BruteForce(cap)
        for _ in range(500):
            op = random.random()
            if op < 0.5:
                v = random.randint(0, 99)
                fast.push(v)
                slow.push(v)
            elif op < 0.75:
                assert fast.pop() == slow.pop()
            else:
                i = random.randint(0, 6)
                assert fast.popAtStack(i) == slow.popAtStack(i)
    print("ok")
