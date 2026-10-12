"""
Flatten Nested List Iterator - A Stack of List Positions

Iterate over the integers of a nested list, where each item is an integer or
another nested list: next() returns the next integer from left to right and
has_next() says whether one is left. [1, [4, [6]], [], 8] -> 1, 4, 6, 8.
"""


# --- helpers ---
def drain(iterator):
    """Call next() while has_next() is true; return the values in order."""
    values = []
    while iterator.has_next():
        values.append(iterator.next())
    return values


# --- algorithm ---
class NestedIterator:
    """A stack of [list, index] frames, the innermost open list on top."""

    def __init__(self, nested):
        self.stack = []
        self.stack.append([nested, 0])      # frame: a list and its next index

    def has_next(self):
        """Move the top frame onto an integer: pop used-up lists, enter
        sub-lists. O(1) amortized."""
        while len(self.stack) > 0:
            frame = self.stack[-1]
            items = frame[0]
            index = frame[1]
            if index == len(items):
                self.stack.pop()            # this list is used up
            elif isinstance(items[index], list):
                frame[1] = index + 1        # step past the sub-list first
                self.stack.append([items[index], 0])    # then enter it
            else:
                return True                 # the top points at an integer
        return False

    def next(self):
        """Settle on an integer, return it and step past it. O(1) amortized."""
        self.has_next()
        frame = self.stack[-1]
        value = frame[0][frame[1]]
        frame[1] += 1
        return value


# --- try it ---
iterator = NestedIterator([1, [4, [6]], [], 8])
print(iterator.next(), iterator.has_next(), iterator.next())  # -> 1 True 4
print(iterator.next(), iterator.next(), iterator.has_next())  # -> 6 8 False
print(drain(NestedIterator([[1, 1], 2, [1, 1]])))     # -> [1, 1, 2, 1, 1]
print(drain(NestedIterator([[], [[]]])))              # -> []
