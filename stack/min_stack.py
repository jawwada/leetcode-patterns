"""
Min Stack (LeetCode 155)  — Medium
Pattern: Stack with auxiliary state

Problem
-------
Design a stack supporting push, pop, top and getMin, each in O(1) time.
Example: push(-2), push(0), push(-3); getMin() -> -3; pop(); top() -> 0; getMin() -> -2.

Brute force
-----------
A plain list; getMin scans the whole list with min(). push/pop/top are O(1) but getMin is
O(n), O(n) space. The wasted work: every getMin rescans elements whose minimum we already
knew the moment they were pushed -- the minimum of the stack below any element never changes
while that element is on the stack.

From brute force to optimal
---------------------------
The redundancy is recomputing min over a prefix that is frozen. Observation: the elements
beneath position i never change while i is on the stack (stacks only mutate at the top), so
"minimum of everything up to and including i" is a constant that can be computed once at
push time: min(val, previous min). Store it alongside each value. getMin is then the top
entry's stored minimum, and pop automatically restores the previous minimum because the
pairs leave together.

Intuition
---------
Snapshot the running minimum at every level of the stack. Because a stack is only ever
modified at the top, snapshots below the top stay valid, and popping reveals the right
earlier snapshot for free.

Geometric view
--------------
Two parallel columns growing upward: values on the left, "min so far" on the right. The right
column is non-increasing as you go up. Popping removes the top row of both columns at once,
so the right column's top is always the min of the left column.

Steps
-----
1. push(val): cur_min = min(val, stack[-1].min) if non-empty else val; append (val, cur_min).
2. pop(): remove the top pair.
3. top(): return stack[-1].val.
4. getMin(): return stack[-1].min.

Complexity: O(1) time per operation, O(n) space — one extra int per element.
Pitfalls: Keeping a single global min (breaks after pop); a second "min stack" that pushes only
on strict decrease and then mishandles duplicates (push on <=, not <).
"""


class MinStack:
    def __init__(self):
        self.stack = []                          # (value, min of everything at or below it)

    def push(self, val: int) -> None:
        cur_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, cur_min))

    def pop(self) -> None:
        self.stack.pop()                         # the stored min below is still correct

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


class BruteForce:
    def __init__(self):
        self.stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return min(self.stack)                   # O(n) rescan on every call


if __name__ == "__main__":
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2

    dup = MinStack()
    for v in (1, 1, 2):
        dup.push(v)
    dup.pop()
    dup.pop()
    assert dup.getMin() == 1                     # duplicate minimum survives one pop

    fast, slow = MinStack(), BruteForce()
    ops = [("push", 5), ("push", 3), ("push", 7), ("pop",), ("push", 3), ("pop",), ("pop",), ("push", -1)]
    for op in ops:
        for st in (fast, slow):
            getattr(st, op[0])(*op[1:])
        assert fast.top() == slow.top() and fast.getMin() == slow.getMin()
    print("ok")
