# Design Circular Queue

*LeetCode 622 · Medium · Pattern: Ring buffer (circular array with head and count) · Reading time ~8 min*

## The problem

Implement MyCircularQueue(k), a bounded FIFO of capacity k with enQueue(x) and deQueue() returning success, Front()
and Rear() returning -1 when empty, isEmpty() and isFull().

```text
Example: k = 3; enQueue 1, 2, 3 -> True; enQueue(4) -> False;
  Rear() -> 3; isFull() -> True; deQueue() -> True; enQueue(4)
  -> True; Rear() -> 4.
```

## What the problem is really asking

Build `MyCircularQueue(k)`: a FIFO queue that can hold at most `k` values, with `enQueue(x)` and `deQueue()` returning
whether they succeeded, `Front()` and `Rear()` returning the first and last values (or -1 when empty), and `isEmpty()`,
`isFull()`. Every operation should be O(1), and the memory should be a fixed block of `k` slots allocated once.

The answer is a data structure. The hard part is not FIFO itself (a deque does that) but doing FIFO inside a fixed array
without ever moving the data. A queue's front keeps leaving, so the occupied region keeps drifting, and the drift has to
go somewhere.

```text
k = 3: enQueue 1, 2, 3 -> full;  deQueue;  enQueue 4 ?

slots   0   1   2               slots   0   1   2
      [ 1 | 2 | 3 ]   deQueue        [ . | 2 | 3 ]
                      ->              ^ free, at the START
                      where does 4 go, and how do we know
                      that 2 is now the front?
```

## Do it by hand first

Draw three boxes in a circle, like seats around a small round table, numbered 0, 1, 2 clockwise. Seat guests 1, 2, 3 in
seats 0, 1, 2. The first guest leaves: you erase nothing, you just move a paper arrow that says "next to be served" from
seat 0 to seat 1. A new guest 4 arrives. The free seat is seat 0, which is the seat clockwise after the last guest (seat
2), because the table is round.

```text
            seat 0: 4  <- newest
          /          \
  seat 2: 3          seat 1: 2  <- arrow: next served
  (clockwise: 0 -> 1 -> 2 -> 0)
  order of service: 2, 3, 4
```

What did you track? Where the arrow points (the front) and how many guests are seated. Every other fact, such as where
the newest guest sits or where the next one goes, you worked out by counting clockwise from the arrow.

## The first honest attempt

Use a Python list: `append` to enqueue, `pop(0)` to dequeue, `len(items) == k` for full.

```text
deQueue on [1, 2, 3]

before  slot 0  slot 1  slot 2
          1       2       3
after     2       3              <- 2 and 3 each moved
cost: k - 1 moves per deQueue
```

It is correct, but each dequeue costs O(k), because the list must keep its first item at index 0 and shifts every other
item left. The waste is clear in the drawing: k - 1 values are physically moved when the only fact that changed is
*which value counts as first*. (A list also grows and shrinks its memory, which the problem's fixed buffer forbids in
spirit.)

## The turning point

**Claim: a dequeue only changes where the front is, so move an index instead of the data, and treat the array as a
ring so that freed slots at the start are reused.**

Keep three things:

- `buf`, a fixed array of `k` slots.
- `head`, the slot of the front value.
- `count`, how many values are stored.

Everything else is derived. The live values occupy the `count` slots starting at `head` and going "clockwise", that is,
upward with wrap-around from `k - 1` to 0. In code every index is reduced `% k`:

```text
front slot   = head
rear slot    = (head + count - 1) % k
next free    = (head + count) % k

enQueue(x): if count == k: False
            buf[(head + count) % k] = x; count += 1
deQueue():  if count == 0: False
            head = (head + 1) % k;      count -= 1
```

Why `count` and not a `tail` pointer? With `head` and `tail` alone, an empty queue and a full queue look identical:
both have `head == tail`, because the occupied arc has length 0 or length `k`, and on a ring those two arcs start and
end at the same place.

```text
k = 3, head = tail = 1:     empty?          full?
                         [ . | . | . ]   [ 6 | 4 | 5 ]
                               ^ h,t           ^ h,t
           the two pointers alone cannot tell these apart
```

A count of 0 or 3 settles it instantly. (The classic alternative wastes one slot and declares the ring full at `k - 1`
values, so `head == tail` can only mean empty.)

The dequeued value is not erased. It sits in its slot as garbage until a later enqueue overwrites it, and nothing reads
it, because every formula only touches the arc `head .. head + count - 1`.

## Watch it work

`k = 3`. Operations: `enQueue 1, 2, 3`, `enQueue 4`, `deQueue`, `enQueue 4`, `deQueue`, `enQueue 5`, `Front`,
`Rear`. A value in parentheses is stale: still in memory but outside the live arc.

```text
Frame 1: enQueue 1, 2, 3   (slots (0+0)%3, (0+1)%3, (0+2)%3)
slot     0   1   2
       [ 1 | 2 | 3 ]       head 0, count 3 -> full
         ^ head
order: 1 2 3
```

Each value lands at `(head + count) % k` and count grows. The ring is full.

```text
Frame 2: enQueue 4 -> False
slot     0   1   2
       [ 1 | 2 | 3 ]       count == k: refuse, change nothing
         ^ head
```

The full check comes before any write, so nothing is overwritten.

```text
Frame 3: deQueue -> True
slot     0   1   2
       [(1)| 2 | 3 ]       head (0+1)%3 = 1, count 2
             ^ head
order: 2 3
```

Only the label moved. 1 is still in slot 0 but no formula will read it.

```text
Frame 4: enQueue 4 -> True, slot (1 + 2) % 3 = 0
slot     0   1   2
       [ 4 | 2 | 3 ]       head 1, count 3 -> full
             ^ head
order: 2 3 4   (the arc 1 -> 2 -> 0 wraps the seam)
```

The wrap-around: the next free slot is computed past the end and lands at 0, overwriting the stale 1.

```text
Frame 5: deQueue, then enQueue 5 at (2 + 2) % 3 = 1
slot     0   1   2
       [ 4 | 5 | 3 ]       head 2, count 3
                 ^ head
order: 3 4 5   (arc 2 -> 0 -> 1)
```

The head itself has now moved to the last slot; the live arc runs 2, 0, 1.

```text
Frame 6: Front() -> buf[2] = 3
         Rear()  -> buf[(2 + 3 - 1) % 3] = buf[1] = 5
```

Both reads are pure arithmetic on `head` and `count`.

Across all frames the live values were exactly the `count` slots clockwise from `head`, in arrival order. No value was
ever moved after it was written.

## Why it is correct

Invariant: the queue's contents, front to back, are `buf[head], buf[(head+1)%k], ..., buf[(head+count-1)%k]`, and
`0 <= count <= k`.

- Initially `count = 0`: the empty sequence, correct.
- `enQueue` when not full writes to `(head + count) % k`, the slot right after the current back. That slot is outside
  the arc (the arc has fewer than `k` slots), so no live value is overwritten, and the new value becomes the last term of
  the sequence.
- `deQueue` when not empty advances `head` by one and decrements `count`: the sequence loses its first term and keeps
  the rest in order.
- `Front` and `Rear` read the first and last terms of the sequence; `isEmpty` and `isFull` read `count`.

Since enqueues add at the back and dequeues remove from the front, the sequence is always the values in arrival order
minus those dequeued: FIFO.

## Cost

Time: O(1) for every operation, each is a comparison, one array access and an index update.
Space: O(k), the fixed buffer plus two integers.

The list-based brute force is O(k) per dequeue.

## Variations you will meet

- **Waste-a-slot version.** Store `head` and `tail` only, allocate `k + 1` slots, and call the ring full when
  `(tail + 1) % (k + 1) == head`. Same O(1), different bookkeeping; some interviewers expect it.
- **Thread-safe bounded buffer.** The producer/consumer problem: the same ring, plus a lock and conditions for "not full"
  and "not empty". This is what `queue.Queue(maxsize=k)` provides in Python.
- **Overwrite-when-full logs.** Keep the last k events: when full, an enqueue overwrites the oldest and advances `head`.
  Python's `deque(maxlen=k)` does exactly this.
- **Moving Average from Data Stream (346).** A ring of `size` values with a running sum: subtract the value about to be
  overwritten, add the new one.

## What to carry forward

A ring buffer is an arc on a clock face: the front is an index, the back is derived from a count, and `% k` makes the
seam disappear. The next problem lets the front move backwards too, turning the ring into a deque.
