---
rank: 24
slug: min_stack
---

Design a stack that supports `push(val)`, `pop()`, `top()` and `get_min()`, which returns the smallest value on the stack, all in `O(1)` time; `pop`, `top` and `get_min` are called only when the stack is not empty. After `push(-2)`, `push(0)` and `push(-3)`, `get_min()` returns -3. After one `pop()`, `top()` returns 0 and `get_min()` returns -2 again.

Scanning the stack inside `get_min` costs `O(n)`, and a single variable holding the minimum breaks on the first pop that removes it: the -3 leaves, the variable still says -3, and nothing remembers that the minimum used to be -2. The way out is a fact about stacks. While an entry sits on the stack, the entries below it never change: all of them were there when it arrived, and none can leave before it does. So the minimum of an entry and everything beneath it is fixed for the entry's whole life, and the entry computes it once, at its push, as the smaller of its own value and the minimum recorded by the entry just below. Each entry is a pair, (value, minimum so far), and `get_min` reads the second half of the top pair.

Read the second column from the bottom up and it is a running minimum, a staircase that only steps down: flat when a larger value arrives, one step lower when a new minimum does. A pop removes the top step and repairs nothing, because the pair it uncovers recorded its minimum when the stack looked exactly as it does now. The minimum that the popped value had hidden comes back on its own, and a second copy of the minimum gets a pair of its own, so it comes and goes without disturbing the first.

```text
after push(-2), push(0), push(-3)             after pop()
          value  min                            value  min
  top → │   -3 │   -3 │ ← get_min = -3
        │    0 │   -2 │                 top → │    0 │   -2 │ ← get_min = -2
        │   -2 │   -2 │                       │   -2 │   -2 │
        └──────┴──────┘                       └──────┴──────┘

operation   how the pair is made          entries, bottom → top       returns
push(-2)    nothing below: min = -2       (-2, -2)
push(0)     min(0, -2) = -2               (-2, -2) (0, -2)
push(-3)    min(-3, -2) = -3              (-2, -2) (0, -2) (-3, -3)
get_min()   read the top pair             (-2, -2) (0, -2) (-3, -3)    -3
pop()       -3 leaves with its record     (-2, -2) (0, -2)
top()       read the top pair             (-2, -2) (0, -2)              0
get_min()   the record below is intact    (-2, -2) (0, -2)             -2
push(-2)    min(-2, -2) = -2              (-2, -2) (0, -2) (-2, -2)
pop()       the copy leaves               (-2, -2) (0, -2)
get_min()   the first -2 still counts     (-2, -2) (0, -2)             -2
```

```pseudo
CLASS MinStack
    FUNCTION Init()
        self.entries ← empty stack          // pairs, bottom to top

    FUNCTION Push(val)
        current_min ← val
        IF len(self.entries) > 0
            below_min ← self.entries.top()[1]     // min of everything below
            current_min ← min(val, below_min)
        self.entries.push((val, current_min))

    FUNCTION Pop()
        self.entries.pop()                  // the pair below keeps its record

    FUNCTION Top()
        RETURN self.entries.top()[0]        // the value half

    FUNCTION GetMin()
        RETURN self.entries.top()[1]        // the minimum half
```

Each operation touches only the top of the stack, so all four run in `O(1)` time, at the price of two numbers per entry, `O(n)` space. Reach for this whenever a stack must also answer a question about everything it holds, such as its minimum, maximum or sum; two min stacks back to back make a queue that reports its minimum too, every operation `O(1)` amortized. The two-stack variant saves space when new minimums are rare: a second stack records a value when it is at most the current minimum, and popping a value equal to the latest record pops the record too. Max Stack mirrors the pairs for `peekMax`, but `popMax` deletes from the middle, which they cannot absorb, so the usual design adds a max-heap beside the stack and deletes lazily, `O(log n)` amortized per call. The classic mistake, in the two-stack variant, is recording only values strictly smaller than the minimum: the demo's second -2 then goes unrecorded, its pop removes the only recorded -2, and `get_min` finds the record stack empty while `[-2, 0]` is still stored.

*Practice:* LC 155 Min Stack · LC 716 Max Stack · LC 232 Implement Queue using Stacks
