"""
Min Stack (LeetCode 155) - Medium
Chapter: stack
Pattern: Stack with auxiliary state

Design a stack that supports push, pop, top and get_min, each in O(1) time.
Example: push(-2), push(0), push(-3); get_min() -> -3; pop(); top() -> 0; get_min() -> -2.
"""


# --- brute force ---
class BruteForce:
    """A plain list; get_min rescans the whole list. push/pop/top O(1), get_min O(n)."""

    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return min(self.stack)                      # O(n) rescan on every call


# --- optimal ---
class MinStack:
    """Each entry stores its value and the min of everything at or below it. All O(1)."""

    def __init__(self):
        self.stack = []         # entries: [value, min of everything at or below it]

    def push(self, val):
        current_min = val
        if len(self.stack) > 0 and self.stack[-1][1] < val:
            current_min = self.stack[-1][1]         # the entries below val never change under it
        self.stack.append([val, current_min])

    def pop(self):
        self.stack.pop()                            # the entry below still holds its correct min

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]


# --- try the brute force ---
ms = BruteForce()
ms.push(-2)
ms.push(0)
ms.push(-3)
print(ms.get_min())   # -> -3
ms.pop()
print(ms.top())       # -> 0
print(ms.get_min())   # -> -2
dup = BruteForce()
dup.push(1)
dup.push(1)
dup.push(2)
dup.pop()
dup.pop()
print(dup.get_min())  # -> 1 (the duplicate minimum survives one pop)


# --- try the optimal ---
ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
print(ms.get_min())   # -> -3
ms.pop()
print(ms.top())       # -> 0
print(ms.get_min())   # -> -2
dup = MinStack()
dup.push(1)
dup.push(1)
dup.push(2)
dup.pop()
dup.pop()
print(dup.get_min())  # -> 1 (the duplicate minimum survives one pop)
