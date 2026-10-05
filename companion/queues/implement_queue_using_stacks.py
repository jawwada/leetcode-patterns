"""
Implement Queue using Stacks (LeetCode 232) - Easy
Chapter: queues
Pattern: Two stacks make a queue (lazy transfer)

Build a first-in-first-out queue with push, pop, peek and empty using only stack operations
(push to top, pop or peek the top, size, is-empty).
Example: push(1); push(2); peek() -> 1; pop() -> 1; empty() -> False.
"""


# --- brute force ---
class BruteForce:
    """One stack with the oldest on top; every push pours everything out and back. push O(n)."""

    def __init__(self):
        self.main = []          # the oldest element sits on top

    def push(self, x):
        helper = []
        while len(self.main) > 0:                   # pour everything out ...
            helper.append(self.main.pop())
        self.main.append(x)                         # x lands at the bottom
        while len(helper) > 0:                      # ... and pour it all back
            self.main.append(helper.pop())

    def pop(self):
        return self.main.pop()

    def peek(self):
        return self.main[-1]

    def empty(self):
        return len(self.main) == 0


# --- optimal ---
class MyQueue:
    """Inbox takes pushes, outbox serves pops; pour only when outbox is dry. Amortised O(1)."""

    def __init__(self):
        self.inbox = []         # newest on top
        self.outbox = []        # oldest on top

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        self.peek()                                 # make sure the outbox holds the front
        return self.outbox.pop()

    def peek(self):
        if len(self.outbox) == 0:                   # pour only when the outbox runs dry
            while len(self.inbox) > 0:
                self.outbox.append(self.inbox.pop())   # reverses the order exactly once
        return self.outbox[-1]

    def empty(self):
        return len(self.inbox) == 0 and len(self.outbox) == 0


# --- try the brute force ---
q = BruteForce()
q.push(1)
q.push(2)
print(q.peek())    # -> 1
print(q.pop())     # -> 1
print(q.empty())   # -> False
print(q.pop())     # -> 2
print(q.empty())   # -> True
e = BruteForce()
e.push(1)
e.push(2)
print(e.pop())     # -> 1
e.push(3)
print(e.pop())     # -> 2
print(e.pop())     # -> 3


# --- try the optimal ---
q = MyQueue()
q.push(1)
q.push(2)
print(q.peek())    # -> 1
print(q.pop())     # -> 1
print(q.empty())   # -> False
print(q.pop())     # -> 2
print(q.empty())   # -> True
e = MyQueue()
e.push(1)
e.push(2)
print(e.pop())     # -> 1
e.push(3)
print(e.pop())     # -> 2
print(e.pop())     # -> 3
