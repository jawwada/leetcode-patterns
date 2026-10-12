"""
Min Stack - Every Entry Remembers the Minimum Below It

Design a stack whose push, pop, top and get_min (the smallest value stored)
all run in O(1); pop, top and get_min are called only on a non-empty stack.
push -2, push 0, push -3, get_min, pop, top, get_min -> -3, 0, -2.
"""


# --- algorithm ---
class MinStack:
    """A stack of pairs (value, minimum of this entry and every entry below)."""

    def __init__(self):
        self.entries = []               # pairs, bottom to top

    def push(self, val):
        """Store val with the smaller of val and the minimum below it. O(1)."""
        current_min = val
        if len(self.entries) > 0:
            below_min = self.entries[-1][1]     # min of everything below
            current_min = min(val, below_min)
        self.entries.append((val, current_min))

    def pop(self):
        """Drop the top pair; the pair below keeps its own minimum. O(1)."""
        self.entries.pop()

    def top(self):
        """The value of the top pair. O(1)."""
        return self.entries[-1][0]

    def get_min(self):
        """The minimum recorded in the top pair. O(1)."""
        return self.entries[-1][1]


# --- try it ---
stack = MinStack()
stack.push(-2)
stack.push(0)
stack.push(-3)
print(stack.get_min(), stack.entries)   # -> -3 [(-2, -2), (0, -2), (-3, -3)]
stack.pop()                             # -3 leaves, and -2 is the min again
print(stack.top(), stack.get_min())     # -> 0 -2
stack.push(-2)                          # a second copy of the minimum
stack.pop()
print(stack.get_min(), stack.entries)   # -> -2 [(-2, -2), (0, -2)]
