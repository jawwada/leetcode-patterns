"""
Array Stack and Queue via Two Stacks - Fundamentals
Chapter: fundamentals/stacks
Key operations: push, pop, peek, drain inbox into outbox only when outbox is empty

A Stack on a Python list (the end is the top) and a Queue made of two stacks: enqueue pushes on
'inbox'; dequeue and peek take from 'outbox', refilling it by draining inbox only when it is empty.
Every element crosses once, so n operations cost O(n) in total (amortized O(1) each).
Example: enqueue 1, 2; peek; dequeue; enqueue 3; dequeue; dequeue; empty -> 1, 1, 2, 3, True
"""


# --- algorithm ---
class Stack:
    def __init__(self):
        self.items = []                     # the end of the list is the top

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()             # removes and returns the top

    def peek(self):
        return self.items[-1]               # looks at the top without removing it

    def empty(self):
        return len(self.items) == 0


class Queue:
    def __init__(self):
        self.inbox = Stack()                # enqueue pushes here
        self.outbox = Stack()               # dequeue and peek take from here

    def enqueue(self, x):
        self.inbox.push(x)

    def refill(self):
        """Move everything from inbox to outbox, which reverses it into queue order."""
        if self.outbox.empty():             # ONLY when outbox is empty, or the order would break
            while not self.inbox.empty():
                self.outbox.push(self.inbox.pop())

    def dequeue(self):
        self.refill()
        return self.outbox.pop()

    def peek(self):
        self.refill()
        return self.outbox.peek()

    def empty(self):
        return self.inbox.empty() and self.outbox.empty()


# --- try it ---
stack = Stack()
stack.push(1)
stack.push(2)
print(stack.peek())        # -> 2
print(stack.pop())         # -> 2
print(stack.pop())         # -> 1
print(stack.empty())       # -> True
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
print(queue.peek())        # -> 1
print(queue.dequeue())     # -> 1
queue.enqueue(3)
print(queue.dequeue())     # -> 2
print(queue.dequeue())     # -> 3
print(queue.empty())       # -> True
