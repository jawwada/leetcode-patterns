## Queues

A queue serves items in arrival order. Use a deque for O(1) append and popleft. The examples below cover a timestamp queue and implementing a queue with two stacks.

<!-- cell -->

A queue template has the same shape, but items leave from the *other* end: "join the line" is `q.append(x)`, "leave the line" is `q.popleft()`, never `list.pop(0)`, and "the oldest item" is `q[0]`. When items expire in the order they arrived, only the front ever needs checking. The lines then run in the order STEP, FIX, RECORD: join, drop whatever has expired, and measure last, so that only live items are counted.

Number of Recent Calls (933) asks `ping(t)` to count the pings in `[t - 3000, t]`, and `t` only grows: pings at 1, 100, 3001 and 3002 answer 1, 2, 3 and 3, because by 3002 the ping at 1 has expired. Each ping joins at the back, the front leaves while it is older than `t - 3000`, and the answer is the length of what is left. Appending first also means the FIX loop can never empty the deque, because `t` itself never expires, so it needs no `self.q and` guard.

<!-- cell -->

```python
class RecentCounter:                         # 933: how many pings in [t - 3000, t]?
    def __init__(self):
        self.q = deque()                     # STATE + INIT: live pings, oldest at the front

    def ping(self, t):                       # t only grows
        self.q.append(t)                     # STEP: the newest joins at the back
        while self.q[0] < t - 3000:          # FIX: drop expired pings (q never empties: t is in it)
            self.q.popleft()
        return len(self.q)                   # RECORD + RETURN: the window is the deque


counter = RecentCounter()
print([counter.ping(t) for t in [1, 100, 3001, 3002]])   # [1, 2, 3, 3]
```

<!-- cell -->

**Try it**
- Change `<` to `<=` in the `while` and replay `[1, 100, 3001, 3002]`: the third answer becomes 2, because the ping at `t = 1` is exactly 3000 ms old and still belongs to `[1, 3001]`.
- Change the `while` to `if` and ping `[1, 2, 3, 5000]`: the last answer is 3 instead of 1, since only one expired ping can leave per call.
- Replace `3000` with `10` and predict `[1, 5, 11, 12, 30]` before running: `[1, 2, 3, 3, 1]`.

<!-- cell -->

```python
c = RecentCounter()

assert [c.ping(t) for t in [1, 3001, 3002]] == [1, 2, 2]   # t = 1 still counts at 3001
```

<!-- cell -->

A queue from two stacks closes the main path, because it shows that a stack and a queue differ by exactly one reversal. Implement Queue using Stacks (232) asks for a FIFO queue with `push`, `pop`, `peek` and `empty`, built from stack moves only: push 1, push 2, and `peek` is 1. Pouring one stack into another reverses it, which turns "newest on top" into "oldest on top". Pour only when the outbox is empty, so every item is poured once: amortised O(1), which means the cost averaged over all the operations.

<!-- cell -->

```python
class MyQueue:                               # 232
    def __init__(self):
        self.inbox, self.outbox = [], []     # STATE + INIT: inbox newest on top; outbox oldest on top

    def push(self, x):
        self.inbox.append(x)                 # STEP

    def peek(self):
        if not self.outbox:                  # FIX: refill only when empty, or the order breaks
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox[-1]               # RETURN: the oldest item

    def pop(self):
        self.peek()                          # make sure the oldest item is on the outbox top
        return self.outbox.pop()

    def empty(self):
        return not self.inbox and not self.outbox


q = MyQueue()
q.push(1)
q.push(2)
first = q.pop()
q.push(3)                                    # 3 must wait behind 2
print(first, q.pop(), q.pop(), q.empty())    # 1 2 3 True
```

<!-- cell -->

**Try it**
- In `peek`, remove `if not self.outbox:` so it always pours, and replay the lines above: the second `pop` returns 3 instead of 2, because 3 was poured on top of the waiting 2.
- Print `q.inbox, q.outbox` after every call: each item crosses from inbox to outbox exactly once.
- Push 1 to 1000, then pop all 1000: count the appends to `outbox`. There are exactly 1000, so the expensive pour is paid once per item.
