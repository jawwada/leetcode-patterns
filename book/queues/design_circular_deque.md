# Design Circular Deque

*LeetCode 641 · Medium · Pattern: Ring buffer (circular array with head and count) · Reading time ~8 min*

## What the problem is really asking

Build `MyCircularDeque(k)`: a double-ended queue of capacity `k` with `insertFront`, `insertLast`, `deleteFront` and
`deleteLast` (each returns whether it succeeded), `getFront` and `getRear` (-1 when empty), `isEmpty` and `isFull`.
Every operation should be O(1) in a fixed buffer of `k` slots.

The answer is a data structure. The previous problem only let the front *shrink*. Now the front can also *grow*: a value
can be inserted before the current first one. In an array that means "before index 0", and that is the whole puzzle.

```text
k = 3 holding 1 2 at slots 0 1       insertFront 3 ?

slot    0   1   2
      [ 1 | 2 | . ]       3 must come before 1, but slot 0
        ^ front           is the first slot of the array
```

## Do it by hand first

Go back to the round table with three seats, numbered clockwise 0, 1, 2. Guests 1 and 2 sit in seats 0 and 1, and the
arrow "front" points at seat 0. Guest 3 must be served *before* guest 1. On a round table that is easy: the seat just
counter-clockwise of seat 0 is seat 2. Seat guest 3 there and move the arrow to seat 2.

```text
            seat 0: 1
          /          \
  seat 2: 3          seat 1: 2
  ^ arrow moved here (one step counter-clockwise)
  order of service, clockwise from the arrow: 3, 1, 2
```

You moved the arrow *first*, then seated the guest where it now points. If you had seated guest 3 at the arrow's old
position, you would have sat on guest 1. Your hand tracked the same two things as before, the arrow and the head count,
and the only new move was turning the arrow the other way.

## The first honest attempt

A Python list: `insert(0, x)` and `pop(0)` for the front, `append` and `pop()` for the back, `len(items) == k` for full.

```text
insertFront 3 on [1, 2]

before  idx 0  idx 1  idx 2
          1      2
after     3      1      2      <- 1 and 2 each shifted right
```

Correct, and back operations are O(1), but every front operation shifts all stored values: O(k). The waste is the same
as in the circular queue, now at the front in both directions: the values do not need to move, only the label "this slot
is the front" does.

## The turning point

**Claim: on a ring, both ends of a deque are just positions, and moving either end in either direction is a `+1` or
`-1` modulo `k`.**

Keep exactly the state from Design Circular Queue: a buffer `buf` of `k` slots, `head` (slot of the front value) and
`count`. The back is still derived as `(head + count - 1) % k`. Now list all four end moves:

```text
insertLast(x):  buf[(head + count) % k] = x;  count += 1
deleteLast():   count -= 1
insertFront(x): head = (head - 1) % k; buf[head] = x; count += 1
deleteFront():  head = (head + 1) % k;  count -= 1
```

The back end moves by changing `count` alone, because the rear is defined relative to `head`. The front end moves by
changing `head` and `count` together: a front insert steps `head` one slot counter-clockwise *and* lengthens the arc, so
the rear stays exactly where it was. Check: rear before is `(head + count - 1) % k`; after, `((head - 1) + (count + 1) -
1) % k`, the same slot.

Two details make or break it:

- **Step, then write.** `head` always points at a live value. Inserting at the front must first move `head` to the free
  slot before it, then write there. Writing first would overwrite the current front.
- **Negative modulo.** In Python, `(0 - 1) % 3` is 2, so the seam wraps cleanly in the backward direction. In C++ or
  Java it is -1, so write `(head - 1 + k) % k`.

As before, `count` is what tells empty (`0`) from full (`k`).

## Watch it work

`k = 3`. Operations: `insertLast 1`, `insertLast 2`, `insertFront 3`, `insertFront 4`, `getRear`, `isFull`,
`deleteLast`, `insertFront 4`, `getFront`, `getRear`. Parentheses mark a stale value outside the live arc.

```text
Frame 1: insertLast 1, insertLast 2
slot     0   1   2
       [ 1 | 2 | . ]       head 0, count 2
         ^ head
order: 1 2
```

Back inserts write at `(head + count) % k` and grow count, exactly as in the circular queue.

```text
Frame 2: insertFront 3 -> True
  head = (0 - 1) % 3 = 2, then buf[2] = 3
slot     0   1   2
       [ 1 | 2 | 3 ]       head 2, count 3 -> full
                 ^ head
order: 3 1 2   (arc 2 -> 0 -> 1)
```

The front stepped backwards across the seam, from slot 0 to slot 2, and only then wrote. The ring is full.

```text
Frame 3: insertFront 4 -> False
         getRear -> buf[(2 + 3 - 1) % 3] = buf[1] = 2
         isFull  -> count == 3 -> True
```

The full check refuses the insert before `head` moves. The rear is still 2, even though it sits in the middle slot of
the array.

```text
Frame 4: deleteLast -> True
slot     0   1   2
       [ 1 |(2)| 3 ]       head 2, count 2
                 ^ head
order: 3 1
```

Deleting the back is a single `count -= 1`; the 2 is left as stale data.

```text
Frame 5: insertFront 4 -> True
  head = (2 - 1) % 3 = 1, then buf[1] = 4
slot     0   1   2
       [ 1 | 4 | 3 ]       head 1, count 3 -> full
             ^ head
order: 4 3 1   (arc 1 -> 2 -> 0)
```

The front stepped back into the slot that the deleted back had freed. The same physical slot was the rear in Frame 3 and
is the front now.

```text
Frame 6: getFront -> buf[1] = 4
         getRear  -> buf[(1 + 3 - 1) % 3] = buf[0] = 1
```

Both reads are arithmetic on `head` and `count`.

Throughout, the live values were the `count` slots running clockwise from `head`; front inserts pulled the arc's start
backwards, back operations moved only its end, and no stored value ever moved.

## Why it is correct

Invariant (unchanged from the circular queue): the deque from front to back is `buf[head], buf[(head+1)%k], ...,
buf[(head+count-1)%k]`, with `0 <= count <= k`. Check each mutation when it is allowed:

- `insertLast` writes the first slot after the arc, which is free because `count < k`, and extends the arc: new last
  term.
- `deleteLast` shortens the arc by one at the end: last term removed, rest unchanged.
- `insertFront` moves `head` to the slot just before the arc, which is free because `count < k`, writes there, and
  extends the arc: new first term, and every old term keeps its slot and its relative order.
- `deleteFront` advances `head` and shortens the arc: first term removed.

The getters read the first and last terms; the predicates read `count`. So the structure is a deque with both ends at
O(1).

## Cost

Time: O(1) for every operation, constant index arithmetic and at most one array write.
Space: O(k) for the buffer and two integers.

The list version costs O(k) for each front insert or delete.

## Variations you will meet

- **Head and tail pointers instead of count.** Some solutions keep `front` and `rear` indices and a wasted slot.
  It works, but you now have four update rules, each with its own off-by-one; head plus count has only two variables to
  get right.
- **Growable deque.** When full, allocate a ring twice as large and copy the arc into it starting at slot 0
  (`head = 0`). Amortised O(1) per insert, the same argument as a dynamic array. This is how Java's `ArrayDeque` works.
- **Design Front Middle Back Queue (1670).** Inserting in the middle breaks the ring idea; the standard answer is two
  deques kept balanced, with the middle at their boundary.
- **Monotonic deque problems.** Sliding Window Maximum needs pops at both ends; in an interview you use
  `collections.deque`, but this ring is what such a deque can look like underneath.

## What to carry forward

On a ring, a deque costs nothing more than a queue: the back moves by `count`, the front moves by stepping `head` and
then writing. The next problem uses queues not as storage but as a turn order, where rejoining the back means "next
round".
