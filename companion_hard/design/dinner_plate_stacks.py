"""
Dinner Plate Stacks (LeetCode 1172) - Hard
Chapter: design
Pattern: List of stacks + min-heap of "has room" indices with lazy invalidation

There are infinitely many stacks in a row, each holding at most capacity plates. push(val) places
the plate on the leftmost stack with room, pop() removes from the rightmost non-empty stack, and
popAtStack(i) removes the top of stack i; both pops return -1 when there is nothing to remove.
Example: capacity=2, push 1,2,3,4,5 -> [1,2][3,4][5]; popAtStack(0) -> 2; push(20) lands on
stack 0 -> [1,20][3,4][5]; pop() -> 5.
"""
import heapq                                  # heappush / heappop keep the smallest at index 0


# --- brute force ---
class BruteForce:
    """List of stacks; push scans left to right for the first stack with room. O(k) per push."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.stacks = []

    def push(self, val):
        for stack in self.stacks:             # walks over every full stack, every time
            if len(stack) < self.capacity:
                stack.append(val)
                return
        self.stacks.append([val])

    def pop(self):
        while len(self.stacks) > 0 and len(self.stacks[-1]) == 0:
            self.stacks.pop()                 # skip trailing empty stacks
        if len(self.stacks) == 0:
            return -1
        return self.stacks[-1].pop()

    def popAtStack(self, index):
        if index < len(self.stacks) and len(self.stacks[index]) > 0:
            return self.stacks[index].pop()
        return -1


# --- optimal ---
class DinnerPlates:
    """Min-heap of indices that may have room, checked lazily at the top. O(log n) per op."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.stacks = []                      # the last stack is never empty
        self.open = []                        # min-heap of indices that MAY have room

    def push(self, val):
        while len(self.open) > 0:
            i = self.open[0]
            if i < len(self.stacks) and len(self.stacks[i]) < self.capacity:
                break
            heapq.heappop(self.open)          # stale: that stack was trimmed away or filled up
        if len(self.open) == 0:
            self.stacks.append([])
            heapq.heappush(self.open, len(self.stacks) - 1)
        i = self.open[0]                      # the leftmost stack with room
        self.stacks[i].append(val)
        if len(self.stacks[i]) == self.capacity:
            heapq.heappop(self.open)          # no room left: retire the index

    def pop(self):
        return self.popAtStack(len(self.stacks) - 1)

    def popAtStack(self, index):
        if index < 0 or index >= len(self.stacks) or len(self.stacks[index]) == 0:
            return -1
        val = self.stacks[index].pop()
        heapq.heappush(self.open, index)      # a hole opened here
        while len(self.stacks) > 0 and len(self.stacks[-1]) == 0:
            self.stacks.pop()                 # keep the right edge on a non-empty stack
        return val


# --- try the brute force ---
d = BruteForce(2)
for v in (1, 2, 3, 4, 5):
    d.push(v)                # [1,2] [3,4] [5]
print(d.popAtStack(0))       # -> 2
d.push(20)                   # [1,20] [3,4] [5]
d.push(21)                   # [1,20] [3,4] [5,21]
print(d.popAtStack(0))       # -> 20
print(d.popAtStack(2))       # -> 21
print(d.pop())               # -> 5
print(d.pop())               # -> 4
print(d.pop())               # -> 3
print(d.pop())               # -> 1
print(d.pop())               # -> -1
print(BruteForce(1).popAtStack(5))   # -> -1


# --- try the optimal ---
d = DinnerPlates(2)
for v in (1, 2, 3, 4, 5):
    d.push(v)                # [1,2] [3,4] [5]
print(d.popAtStack(0))       # -> 2
d.push(20)                   # [1,20] [3,4] [5]
d.push(21)                   # [1,20] [3,4] [5,21]
print(d.popAtStack(0))       # -> 20
print(d.popAtStack(2))       # -> 21
print(d.pop())               # -> 5
print(d.pop())               # -> 4
print(d.pop())               # -> 3
print(d.pop())               # -> 1
print(d.pop())               # -> -1
print(DinnerPlates(1).popAtStack(5))   # -> -1
