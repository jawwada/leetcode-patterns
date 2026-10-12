---
rank: 76
slug: circular_queue
---

Design a first-in, first-out queue of fixed capacity on a single array: `enqueue(value)` and `dequeue()` return `true` or `false` for success, `front()` and `rear()` return the oldest and the newest value or `-1` when the queue is empty, and `is_empty()` and `is_full()` report the state. With capacity 3, after enqueueing 1, 2 and 3 the queue is full and enqueueing 4 fails; after one dequeue the 4 fits, and then `front()` is `2` and `rear()` is `4`.

An array queue that shifts every value left on each dequeue pays `O(n)` per dequeue, and one that only moves its start forward runs off the end of the array while the slots behind it sit empty. The ring buffer bends the array into a circle: slot `capacity - 1` is followed by slot `0`, and every index is taken modulo the capacity. Two numbers describe the whole queue: `head`, the slot of the oldest value, and `count`, how many values are stored. The values fill `count` consecutive slots of the circle starting at `head`, so the next free slot is `tail = (head + count) mod capacity` and the newest value sits just before it. Enqueue writes at the tail and increments `count`. Dequeue steps `head` forward one slot and decrements `count`, leaving the old value behind to be overwritten later. Nothing ever moves.

Storing `count` instead of a second index is the heart of this design. With only `head` and `tail`, an empty queue and a full queue look identical, `head = tail`, as the start and the third enqueue below show; the usual alternatives are exactly this count or one slot left permanently unused.

```text
capacity 3       slot  0    1    2    head  count   tail
start                  ·    ·    ·       0      0      0    empty: head = tail
enqueue 1 → true       1    ·    ·       0      1      1
enqueue 2 → true       1    2    ·       0      2      2
enqueue 3 → true       1    2    3       0      3      0    full: head = tail
enqueue 4 → false      1    2    3       0      3      0    count = capacity
dequeue   → true      (1)   2    3       1      2      0    head steps on
enqueue 4 → true       4    2    3       1      3      1    4 wrapped to slot 0
front = items[1] = 2    rear = items[(1 + 3 - 1) mod 3] = items[0] = 4
· never written    (1) an old value left behind, free to overwrite
```

```pseudo
CLASS CircularQueue
    FUNCTION Init(capacity)
        self.items ← array of capacity zeros
        self.capacity ← capacity
        self.head ← 0                       // slot of the front value
        self.count ← 0                      // how many values are stored

    FUNCTION Enqueue(value)
        IF self.IsFull()
            RETURN false
        tail ← (self.head + self.count) mod self.capacity    // wraps to 0
        self.items[tail] ← value
        self.count ← self.count + 1
        RETURN true

    FUNCTION Dequeue()
        IF self.IsEmpty()
            RETURN false
        self.head ← (self.head + 1) mod self.capacity    // old value stays
        self.count ← self.count - 1
        RETURN true

    FUNCTION Front()
        IF self.IsEmpty()
            RETURN -1
        RETURN self.items[self.head]

    FUNCTION Rear()
        IF self.IsEmpty()
            RETURN -1
        RETURN self.items[(self.head + self.count - 1) mod self.capacity]

    FUNCTION IsEmpty()
        RETURN self.count = 0

    FUNCTION IsFull()
        RETURN self.count = self.capacity
```

Each operation is a constant amount of arithmetic, so all six run in `O(1)` time, and the queue takes `O(capacity)` space allocated once. The signals are a fixed-size buffer, a stream where only the last `k` items matter, such as a moving average, or a request to build a queue or deque without linked nodes. A circular deque adds insertion at the front by stepping `head` backward to `(head - 1 + capacity) mod capacity`, and Java's `ArrayDeque` is a ring buffer of the same kind that grows when it fills. The classic mistake is dropping a modulo: `tail = head + count` runs off the end of the array exactly when the ring should wrap, as in the last enqueue above, where `1 + 2 = 3` must become slot `0`.

*Practice:* LC 622 Design Circular Queue · LC 641 Design Circular Deque · LC 346 Moving Average from Data Stream
