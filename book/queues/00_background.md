# Queues and Deques

*6 problems · Reading time ~24 min*

## Why this chapter exists

A stack answers "what is the most recent unfinished thing?". A queue answers the opposite question: "who has been
waiting the longest?". That second question is just as common, and it is the one fairness, time and distance all ask.
A request that arrived first should be served first. A timestamp that is oldest is the first to expire. A cell that was
reached in fewer steps should be expanded before one reached in more. Each time, the answer sits at the *front* of a
line, and new arrivals join the *back*.

The six problems in this chapter fall into three families:

- **Building one discipline from the other.** A queue out of two stacks, and a stack out of one queue (Implement Queue
  using Stacks, Implement Stack using Queues). They force you to understand exactly what FIFO and LIFO promise, and they
  teach the amortised argument you will use for the rest of the book.
- **Time windows and fixed memory.** A queue whose front expires as time moves on (Number of Recent Calls), and a queue
  that must live in a fixed array without ever shifting (Design Circular Queue, Design Circular Deque). Here the queue is
  a sliding window over time, and then a ring of slots with a moving start.
- **Turn order.** A queue as a line of players who act, then rejoin the back for the next round (Dota2 Senate). The queue
  stores *when* each player acts next, and the front is whoever acts soonest.

Beyond these six, queues carry a large part of the rest of the book: monotonic deques for window maxima, cooldown queues
beside heaps, and above all breadth-first search, which is nothing but a queue of places still to explore.

## What it is

### The FIFO queue: first in, first out

A queue is the line at a coffee shop. You join at the back, you are served from the front, and whoever has waited longest
goes next. That rule is called FIFO, first in, first out. A queue has three operations:

- **enqueue(x)**: join the back.
- **dequeue()**: leave from the front, returning that item.
- **peek()**: look at the front without removing it.

```text
             front                     back
dequeue <-   [ A ][ B ][ C ][ D ]   <- enqueue E
               ^
               peek = A

after dequeue (A leaves) and enqueue E:

             [ B ][ C ][ D ][ E ]
               ^ front        ^ back
```

Nobody in the middle ever moves, is read, or is changed. As with a stack, the restriction is the point: a queue is a
list you only touch at its two ends, and each end has one job. The back only grows. The front only shrinks. Read from
front to back, the items are in arrival order, always.

Compare the two disciplines on the same input. Push 1, 2, 3 into each, then take one item out:

```text
              in: 1, 2, 3        take one out

  stack (LIFO)    | 3 | <- top      -> 3  (newest)
                  | 2 |
                  | 1 |

  queue (FIFO)  front [1][2][3] back  -> 1  (oldest)
```

Same items, same arrivals; the only difference is which end the removals come from.

### Why a Python list is a bad queue

A Python list stores its items in one contiguous block of memory, item 0 first. Appending at the end is O(1) amortised,
which is why a list makes a perfect stack. Removing item 0 is not cheap: the list must stay contiguous and start at index
0, so every remaining item shifts one slot to the left to close the gap.

```text
list.pop(0) on [A, B, C, D, E]

before  idx:  0   1   2   3   4
              A   B   C   D   E
              ^ removed
after   idx:  0   1   2   3
              B   C   D   E      <- B, C, D, E each moved
                                    one slot left
cost: n - 1 moves, so O(n) per dequeue, O(n^2) to drain
```

This is not a theoretical worry. Draining a list of 100,000 integers with `pop(0)` took about 0.64 s on a laptop;
draining 200,000 took about 2.6 s, four times as long for twice the items, which is the quadratic signature. The same
drains with a deque took about 2 ms and 3 ms. `insert(0, x)` has the same problem in the other direction: it shifts
everything right. So in Python, never use a list as a queue.

### The deque: a queue open at both ends

`collections.deque` (say "deck", short for double-ended queue) is the right tool. In CPython it stores items in a chain
of fixed-size blocks (64 slots each), linked to their neighbours in both directions, and it keeps a pointer to the first
used slot and the last used slot. Adding or removing at either end touches only an end block: write a slot and move a
pointer, or, when an end block fills up or empties, link in a new block or unlink an old one. Nothing ever shifts.

```text
appendleft(x) ->  [ x ][ A ][ B ][ C ]  <- append(y)
popleft()     <-                        -> pop()

blocks in memory (simplified: 4 slots per block)

 left ptr                                   right ptr
   v                                           v
 [ _ _ x A ] <-> [ B C D E ] <-> [ F G _ _ ]
   ^ free        a full middle      free ^
   slots for     block nobody       slots for
   appendleft    touches            append
```

So a deque supports four O(1) end operations: `append`, `appendleft`, `pop`, `popleft`. The price is the middle:
`d[i]` has to hop from block to block to reach slot `i`, so indexing near the centre of a large deque is O(n), and
inserting into the middle is O(n). A deque is the right structure whenever you only touch the ends. Used with `append`
and `popleft` only, it is a FIFO queue. Used with `append` and `pop` only, it is a stack. Used with all four, it is a
line that people can join or leave at either end, which several patterns below exploit.

### The ring buffer: a queue in a fixed array

Sometimes you are given a fixed amount of memory, `k` slots, and asked to run a queue in it (a network card's packet
buffer, an audio buffer, a log that keeps the last `k` lines). The list approach shifts on every dequeue. The fix is to
stop moving the data and move a *label* instead: keep an index `head` that says which slot is the front, and a `count`
of how many items are stored. A dequeue just advances `head`. The slot the front used to occupy is now free.

But then the queue drifts to the right and falls off the end of the array, while free slots pile up at the start. The
answer is to bend the array into a ring: after slot `k - 1` comes slot 0 again. In code, every index is taken `% k`.

```text
capacity k = 5, head = 3, count = 4
queue (front -> back): A B C D

index      0     1     2     3     4
        +-----+-----+-----+-----+-----+
buf     |  C  |  D  |     |  A  |  B  |
        +-----+-----+-----+-----+-----+
                       ^     ^
          tail = (3+4)%5=2   head = 3 (front)

the same buffer as a ring (clockwise = toward the back)

                 [3] A  <- head
            [2] .      [4] B
              (free)
            [1] D      [0] C
                ^ rear = (3+4-1)%5 = 1
```

Three formulas run the whole structure:

```text
front slot  = head
rear slot   = (head + count - 1) % k
next free   = (head + count) % k

enqueue x : buf[(head+count) % k] = x ; count += 1
dequeue   : head = (head + 1) % k     ; count -= 1
```

Why store `count` rather than a `tail` index? Because with only `head` and `tail`, an empty buffer and a full buffer both
have `head == tail`: the arc has length 0 or length `k`, and the two indices cannot tell you which. A count of 0 or `k`
can. (The other classic fix is to waste one slot and call the buffer full at `k - 1` items.)

### A queue from two stacks

Suppose you only have stacks. Can you build a queue? Pouring one stack into another reverses it: the item that was at the
bottom ends up on top. One reversal turns newest-on-top into oldest-on-top, which is exactly the queue's front.

So keep two stacks with fixed roles. The **inbox** takes every enqueue. The **outbox** serves every dequeue. When the
outbox runs dry, pour the whole inbox into it, once.

```text
enqueue 1, 2, 3           first dequeue: outbox empty,
                          pour inbox into outbox

 inbox   outbox            inbox   outbox
 | 3 |                             | 1 | <- top = oldest
 | 2 |                             | 2 |
 | 1 |                             | 3 |
 -----   -----             -----   -----
                           dequeue -> 1
```

The cost argument is the one from the Stacks chapter, applied to a whole life: each item is pushed onto the inbox once,
popped from the inbox once, pushed onto the outbox once and popped from the outbox once. Four stack operations per item,
for life. A single dequeue can be slow (it may pour n items), but n dequeues cost at most 4n stack operations in total,
so each operation is O(1) *amortised*.

### queue.Queue, in one line

`queue.Queue` is a deque wrapped with a lock so several threads can safely enqueue and dequeue at once; it is for
concurrent programs, and in an interview you use `collections.deque` directly.

### Where this is going

A queue's rule is "oldest first". The Heaps chapter keeps the exact same interface, push, pop, peek, and changes only
the rule: a **priority queue** hands back the *most urgent* item, however recently it arrived. Everything you learn here
about what a queue promises is the baseline that chapter deliberately breaks.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| list `append` / `pop()` | O(1) amortised | the end of a contiguous block, nothing shifts |
| list `pop(0)` / `insert(0, x)` | O(n) | every other item shifts one slot |
| deque `append` / `appendleft` | O(1) | write into an end block, move one pointer |
| deque `pop` / `popleft` | O(1) | clear an end slot, move one pointer |
| deque `d[0]`, `d[-1]` | O(1) | the end pointers point straight at them |
| deque `d[i]` in the middle | O(n) | hops block to block |
| `len(d)` | O(1) | stored as a field |
| ring buffer enqueue / dequeue | O(1) | one write and one index update, all `% k` |
| ring buffer front / rear | O(1) | `head` and `(head + count - 1) % k` |
| two-stack queue enqueue | O(1) | push onto the inbox |
| two-stack queue dequeue / peek | O(1) amortised, O(n) worst | an occasional full pour, at most once per item |
| one-queue stack push | O(n) | rotate the n - 1 older items behind the new one |

Three operations deserve a drawing.

**Ring buffer enqueue across the seam.** The buffer below has a free slot only at index 0. Enqueue does not care: it
computes `(head + count) % k` and lands there.

```text
k = 4, head = 1, count = 3     enqueue E
                               slot = (1 + 3) % 4 = 0

idx    0   1   2   3           idx    0   1   2   3
     +---+---+---+---+              +---+---+---+---+
     |   | B | C | D |              | E | B | C | D |
     +---+---+---+---+              +---+---+---+---+
           ^ head                         ^ head
     count 3                        count 4 (full)
     order: B C D                   order: B C D E
```

**Ring buffer dequeue.** Only `head` moves. The old value stays in its slot as garbage until a later enqueue overwrites
it; that is fine, because no formula ever reads outside the arc `head .. head + count - 1`.

```text
dequeue (B leaves)

idx    0   1   2   3
     +---+---+---+---+
     | E |(B)| C | D |    (B) = stale, outside the arc
     +---+---+---+---+
               ^ head = (1 + 1) % 4 = 2, count 3
     order: C D E
```

**The lazy pour.** The outbox is only refilled when it is empty, never topped up. If it were refilled while it still
held items, the new items would land on top of older ones and leave first.

```text
inbox: 4 5   outbox: 2 3 (2 on top)

WRONG: pour now          RIGHT: wait
outbox: 4 5 2 3          serve 2, then 3 from outbox,
 top -> 4 leaves         then pour: outbox 4 5 (4 on top)
 before 2: FIFO broken   order out: 2 3 4 5
```

## The invariant

Every queue protects one statement: **read from front to back, the items are in arrival order, and the front is the
oldest item still present.** Each concrete layout restates it in its own terms:

- Deque used as a queue: items leave only through `popleft` and arrive only through `append`.
- Ring buffer: the live items are exactly the `count` slots `head, head+1, ..., head+count-1` (all `% k`), in that order.
- Two stacks: every item in the outbox is older than every item in the inbox, the outbox has its oldest item on top,
  and the inbox has its newest on top.

A legal ring and an illegal one, both meant to hold the queue `A B C` (A oldest):

```text
LEGAL: head = 3, count = 3       ILLEGAL: head = 0, count = 3

idx   0   1   2   3              idx   0   1   2   3
    +---+---+---+---+                +---+---+---+---+
    | B | C |   | A |                | B | C |   | A |
    +---+---+---+---+                +---+---+---+---+
                  ^ head               ^ head
arc = slots 3, 0, 1              arc = slots 0, 1, 2
reads A B C : correct            reads B C <free slot>
                                 A is lost, order wrong
```

Both buffers hold the same bytes; only the label differs. The illegal state is what you get if you compute positions
without `% k`, or move `head` the wrong way: the arc covers a free slot and skips a live one.

And for two stacks:

```text
LEGAL                            ILLEGAL (poured too early)
inbox   outbox                   inbox   outbox
| 5 |   | 2 | <- next out                | 4 | <- next out
| 4 |   | 3 |                            | 5 |
                                         | 2 |
outbox all older than inbox              | 3 |
                                         4 leaves before 2
```

## How to picture it

Picture a **conveyor belt** running right to left. Items are dropped on at the right end and taken off at the left end.
Nothing on the belt changes position relative to its neighbours; the belt just carries the line toward the exit.

```text
  exit <- [A][B][C][D] <- entrance
          oldest   newest
```

For the ring buffer, picture a **clock face** with `k` positions and a coloured arc on it. The arc starts at `head` and
runs clockwise for `count` ticks. Enqueue paints one more tick at the arc's clockwise end; dequeue erases the tick at its
start. Both ends only ever move clockwise, chasing each other around the dial, and the seam between `k - 1` and 0 is
invisible.

```text
             [0]*                 k = 8, head = 6, count = 4
       [7]*        [1]*           * = live slot
                                  live: 6, 7, 0, 1
   [6]*                [2]        front at 6 (head)
                                  rear at (6+4-1)%8 = 1
       [5]         [3]            next free (6+4)%8 = 2
             [4]
   clockwise: 0 -> 1 -> 2 -> ... -> 7 -> 0
```

For time windows, picture a **bracket sliding along a number line**. Its right edge sits on "now"; its left edge is
`now - width`. As time moves right, dots fall off the left edge in the order they arrived, which is precisely the order a
queue gives them up.

```text
time:  1   100        3001 3002
       *    *           *    *
           [------- 3001 ms -----]
       ^ fell out: 1 < 3002 - 3000
```

And for the rest of the book, picture a **wave**. Breadth-first search drops a stone in a pond: the queue holds the ring
of the wave currently spreading, everyone at distance `d` before anyone at distance `d + 1`.

## Advanced patterns

The basics give you three layouts (deque, ring, two stacks) and one rule (oldest first). The patterns below are what
the rule turns into when a problem gets harder: modular indexing that runs in both directions, a cost argument that spans
an item's whole life, a queue whose front *expires*, a deque whose back *dominates*, a line of players who rejoin it, and
the queue as the engine of shortest paths. Several of them only pay off in later chapters, and they are here so that when
you meet them you recognise an old friend.

### 1. Ring buffer and modular arithmetic in both directions

**When it shows up.** Fixed capacity, "circular", "bounded buffer", "the last k items", or any time you must avoid
shifting an array but need to add or remove at the start.

**The intuition.** Once the array is a ring, an end of the queue is just an index, and moving that end is just `+ 1` or
`- 1` modulo `k`. The back grows clockwise by increasing `count`. The front can shrink clockwise (`head + 1`) *or grow
counter-clockwise* (`head - 1`), which is what turns the ring into a deque. The key is order of operations: to insert at
the front, first step `head` back, then write, because `head` must always point at a live item. Python's `%` always
returns a value in `0 .. k-1`, even for `-1 % k`, so `(head - 1) % k` wraps cleanly from 0 to `k - 1`; in C++ or Java,
`-1 % k` is `-1`, so write `(head - 1 + k) % k`. Everything else is derived: rear is `(head + count - 1) % k`, and
empty/full come from `count`.

```text
k = 3, queue holds 1 2 at slots 0 1, head = 0

insertFront 3:  head = (0 - 1) % 3 = 2, write slot 2

idx    0   1   2
     +---+---+---+
     | 1 | 2 | 3 |      front -> back: 3 1 2
     +---+---+---+      rear = (2 + 3 - 1) % 3 = 1
               ^ head = 2
```

**Where you'll use it.** Design Circular Queue (one direction) and Design Circular Deque (both). Beyond the chapter:
Moving Average from Data Stream (LeetCode 346) can keep its last `size` values in a ring with a running sum, and the same
`% n` indexing is how you walk a circular array twice in Next Greater Element II.

### 2. The amortised two-stack queue

**When it shows up.** You are given only stacks, or a structure that is easy to maintain as a stack (a running minimum,
a running gcd), and you need queue behaviour. "Implement X using Y" questions, and "min queue" or "sliding window
aggregate" questions where the aggregate cannot be undone.

**The intuition.** Reversal is the bridge between LIFO and FIFO, and reversing is expensive, so do it as rarely as
possible: once per item, at the last moment, and never undo it. The argument that this is O(1) per operation is
*per-item accounting*: follow one item from birth to death and count what it costs. It is pushed to the inbox, popped
from the inbox, pushed to the outbox, popped from the outbox: four operations, no matter how the dequeues are spread
out. A long pour is not a cost spike charged to one dequeue so much as a prepayment for the next many cheap ones. The
deeper use: a stack can carry a ride-along summary (the Min Stack trick), so a queue built from two min stacks reports
the minimum of everything in it in O(1) amortised, with the answer being `min(inbox.min, outbox.min)`. That gives a
sliding-window minimum for any associative summary, even ones a monotonic deque cannot handle.

```text
window minimum via two min stacks (value, min below)

window, oldest first: 4 7 5 | 2 6

inbox (newest on top)     outbox (oldest on top)
| 6 , 2 |                 | 4 , 4 |  <- next to leave
| 2 , 2 |                 | 7 , 5 |
                          | 5 , 5 |
window min = min(2, 4) = 2   (top mins of both stacks)
```

**Where you'll use it.** Implement Queue using Stacks is the pattern in its pure form. Beyond the chapter: the same
accounting justifies every "each element is pushed once and popped at most once" claim, and the two-min-stack queue is
one way to solve Sliding Window Maximum.

### 3. Sliding time window: evict expired items from the front

**When it shows up.** A stream of events with timestamps that never decrease, and a question about "the last W seconds"
or "the last k events": recent calls, hit counters, rate limiters, moving averages.

**The intuition.** If time only moves forward, the window's left edge `now - W` only moves forward too. An event that is
too old now is too old forever. And because events arrived in time order, the old ones are all at the front of the
queue, bunched together. So each new event does two things: append itself at the back, then pop from the front while the
front is out of the window. The queue is then *exactly* the set of in-window events, its length is the count, and a
running sum updated on append and pop gives the total or average. Each event is appended once and popped once, so a
whole stream costs O(n) however the evictions are spread out. The two traps are the boundary (inclusive or exclusive:
read the statement and write `<` or `<=` to match) and assuming the queue is non-empty when the newest event is itself
old enough to be checked.

```text
W = 3000, pings 1, 100, 3001, 3002, then 7000

at 3002: left edge 2       queue: [100, 3001, 3002]  len 3
         1 < 2 popped

at 7000: left edge 4000    pop 100, 3001, 3002
                           queue: [7000]             len 1
```

**Where you'll use it.** Number of Recent Calls. Beyond the chapter: Moving Average from Data Stream (346) and Design
Hit Counter (362), which add a running sum and, for hit counter, bucketing many hits at the same second into one entry.

### 4. Monotonic deque: the front expires, the back is dominated

**When it shows up.** "Maximum (or minimum) of every window of size k", or a window over prefix sums where the best
start must be found fast. You met this in the Sliding Window chapter; here is why it must be a deque.

**The intuition.** The structure has two reasons to remove an item, and they happen at opposite ends. At the **front**,
items leave because they are *too old*: their index has slid out of the window. That is plain queue behaviour, oldest
first. At the **back**, items leave because they are *dominated*: a newcomer that is at least as large and younger will
outlast the old item in every future window, so the old item can never be the maximum again. That is stack behaviour,
newest first, exactly the pop-while loop from the Stacks chapter. Only a deque supports both. The survivors read front to
back in decreasing value and increasing index, so the front is the window maximum. Each index enters once and leaves once
through one of the two doors, so the sweep is O(n).

```text
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3, deque holds indices

i=3 (-3):  front                 back
           [ 1 ][ 2 ][ 3 ]        values 3 -1 -3   max 3
             ^ expires when i = 4 (index 1 <= 4 - 3)

i=4 (5):   5 beats -3, -1, 3 from the back
           [ 4 ]                  values 5         max 5
```

**Where you'll use it.** Beyond the chapter: Sliding Window Maximum (239) is the pattern itself, and Shortest Subarray
with Sum at Least K (862) runs it over prefix sums, where the front leaves because a start has been *used* rather than
because it expired.

### 5. Round-robin: re-enqueue, and stamp the next turn with index + n

**When it shows up.** Players, tasks or processes take turns in a fixed order, round after round, and some of them drop
out: "in order, then repeat", "each round", "circular game", "eliminate".

**The intuition.** A queue is a natural turn order: the front acts, then rejoins at the back, which is exactly "next
round". Drop-outs are free: just do not re-enqueue them, and nobody ever has to skip over them again. When two lines
compete (two parties, two teams), compare their fronts to decide who acts first, and that needs a *time stamp*, not just
an order. Use the player's seat index `i` for round one and re-enqueue as `i + n` for round two, `i + 2n` for round
three. Adding `n` keeps every queue sorted by when its members actually act, across round boundaries, so comparing two
fronts is always comparing two real turn times. The same move with `% n` recovers the seat if you need it.

```text
"DDRRR", n = 5: R queue [2 3 4], D queue [0 1]

duel 1: fronts R2 vs D0 -> D0 acts first, bans R2
        D0 rejoins as 0 + 5 = 5
        R [3 4]   D [1 5]

duel 3: fronts R4 vs D5 -> R4 acts first (round 1 seat
        beats round 2 seat), bans D5; R4 rejoins as 9
```

**Where you'll use it.** Dota2 Senate. Beyond the chapter: Find the Winner of the Circular Game (1823) rotates one queue
`k - 1` times and pops, and Task Scheduler pairs a heap with a cooldown queue whose entries are stamped with the time
they may run again.

### 6. BFS: a queue of frontier layers

**When it shows up.** "Minimum number of steps / moves / minutes", on a grid, a word graph, a state space, where every
move costs the same. Also "everything spreads from several sources at once".

**The intuition.** Breadth-first search explores a graph in rings: first everything one step from the start, then
everything two steps away, and so on. A FIFO queue produces this order automatically. When you pop a cell at distance
`d`, you push its unvisited neighbours at distance `d + 1`, and they go to the *back*, behind every other distance-`d`
cell still waiting. So the queue is always "some cells at distance d, then some at d + 1", never anything else, and the
first time you reach a cell is along a shortest path. To count layers, process the queue in batches of `len(queue)`.
To start from several sources (all rotten oranges, all zeros), put them all in the queue before the loop: they form
layer 0 together, and the wave spreads from all of them at once.

```text
grid (2 = rotten, 1 = fresh, # = empty), distances by BFS

 2 1 1          0 1 2
 1 1 #    ->    1 2 #       queue after popping (1,1):
 # 1 1          # 3 4       [(0,2) d2][(2,1) d3]
                            all d before all d + 1
```

**Where you'll use it.** The Graphs chapter: Rotting Oranges and 01 Matrix (multi-source BFS), Word Ladder (BFS over
an implicit graph of words). The queue is the same `deque` you build here.

### 7. 0-1 BFS: push to the front when a move is free

**When it shows up.** Shortest path where every move costs either 0 or 1: "change the arrow at cost 1, follow it for
free", "break a wall at cost 1".

**The intuition.** Plain BFS works because the queue holds at most two distances, `d` and `d + 1`, front first. A
0-cost move reaches a neighbour at the *same* distance `d` as the cell being expanded, so it belongs ahead of all the
`d + 1` items: push it on the **front** with `appendleft`. A 1-cost move goes to the **back** as usual. The deque stays
sorted by distance, with at most two distinct values in it, so the front is always the cheapest unexpanded cell, which
is the property Dijkstra's algorithm needs, at O(1) per push instead of a heap's O(log n). It is the double-ended deque
earning its keep.

```text
grid: every arrow points right (->), goal bottom-right
 -> -> ->      follow an arrow: cost 0, else cost 1
 -> -> ->

after popping (0,1):
 front                                 back
 [(0,2) d0][(1,0) d1][(1,1) d1]
   ^ free move pushed on the front
answer: dist(1,2) = 1 (one changed arrow)
```

**Where you'll use it.** The Graphs chapter: Minimum Cost to Make at Least One Valid Path in a Grid. Beyond it: any
grid with "remove obstacles at cost 1" (Minimum Obstacle Removal to Reach Corner, 2290).

## Signals in a problem statement

- "First come, first served", "in the order they arrived", "oldest" -> FIFO queue.
- "Circular", "fixed capacity", "bounded buffer", "the last k" -> ring buffer with `head` and `count`.
- "Implement a queue using ...", "implement a stack using ..." -> reversal and rotation; count the cost per item.
- "In the past W milliseconds / seconds", "recent", "hit counter", "rate limit", timestamps that never decrease ->
  sliding time window: append, evict from the front.
- "Maximum / minimum of every window of size k" -> monotonic deque.
- "Round after round", "takes turns", "each player in order", "eliminate" -> round-robin queue, re-enqueue with `+ n`.
- "Minimum number of steps / minutes / moves", unweighted grid or word graph -> BFS with a queue (Graphs chapter).
- Edge costs of only 0 and 1 -> 0-1 BFS with `appendleft` for free moves.
- "Add or remove at both ends" -> deque.

Counter-signals:

- "Most recent", "undo", "matching brackets", "next greater" -> stack, not queue.
- "Most urgent", "smallest so far", "k-th largest", weighted shortest path -> priority queue (heap).
- Random access by position in the middle -> an array or list; a deque's middle is slow.
- Timestamps that can arrive out of order -> the front is no longer the oldest; bucket by time or use a heap.

## Python toolbox

```python
from collections import deque

q = deque()              # FIFO queue
q.append(x)              # enqueue at the back
x = q.popleft()          # dequeue from the front
front, back = q[0], q[-1]  # peek both ends, O(1)
q.appendleft(x); q.pop() # the other two ends
q.rotate(-1)             # move front to back
d = deque(maxlen=3)      # full? append drops the front
if q: ...                # non-empty test
```

A BFS skeleton, layer by layer:

```python
q, seen, d = deque(starts), set(starts), 0
while q:
    for _ in range(len(q)):  # exactly one layer
        u = q.popleft()
        for v in nbrs(u):
            if v not in seen:
                seen.add(v); q.append(v)
    d += 1
```

Quirks worth knowing: `deque(maxlen=k)` silently discards from the opposite end when full, which is handy for "last k
items" but hides overflow if you needed to detect it. Mutating a deque while iterating over it raises a `RuntimeError`.
`(i - 1) % k` is non-negative in Python. `queue.Queue` is for threads and is much slower; do not use it for algorithms.

## Mistakes people make

1. Using `list.pop(0)` as dequeue, turning an O(n) algorithm into O(n^2). Fix: `deque.popleft()`.
2. Ring buffer with only `head` and `tail`, unable to tell empty from full when they are equal. Fix: keep `count`.
3. Computing the rear as `tail - 1` without `% k`, which is `-1` at the seam (Python silently reads the last slot; other
   languages crash). Fix: `(head + count - 1) % k`.
4. Writing before moving `head` in insert-at-front, overwriting the current front. Fix: step `head` back, then write.
5. Pouring the inbox into the outbox while the outbox still has items, which breaks FIFO order. Fix: pour only when the
   outbox is empty.
6. Rotating `n` times instead of `n - 1` after a push in a queue-based stack, which puts the new item back at the end.
   Fix: rotate `len(q) - 1` times.
7. Evicting with `<=` when the window is inclusive (or `<` when it is exclusive). Fix: write the window as an interval
   `[t - W, t]` and translate it literally.
8. Re-enqueueing a round-robin player as `i` instead of `i + n`, so round-two turns compare as if they were round one.
   Fix: stamp with the real next turn time.
9. In BFS, marking a cell visited when it is popped instead of when it is pushed, so it is enqueued many times. Fix:
   mark on push.
10. Quoting "O(1)" for a two-stack dequeue without "amortised". Fix: a single dequeue can pour n items; only the total
    over many operations is linear.

## The journey ahead

The thread through the chapter is one question: where is the front, and what makes it leave? First the front is
something you have to manufacture out of the wrong tool. Then it is the oldest timestamp, leaving because it expired.
Then it is just an index on a ring, and moving it costs nothing. Finally the front is whoever acts next, and leaving
means being knocked out of the game.

### Warm-up: one discipline built from the other

**Implement Queue using Stacks.** You have two stacks and must produce FIFO order. The obvious design pours everything
out and back on every push, and the curious question is why that feels wasteful: pouring twice is a reversal undone.
The new idea is to reverse each item exactly once, lazily, and the lesson that comes with it is amortised cost, measured
over an item's whole life instead of one operation.

**Implement Stack using Queues.** The mirror image, and it is not symmetric. A queue cannot reverse anything by pouring
into another queue, because pouring keeps the order. What it can do is *rotate*: after each push, send the older items
around to the back until the newcomer is at the front. The new idea is that a queue is a ring you can turn, and the
honest cost is O(n) per push, with no amortised escape.

### Time and memory: the front expires, the front is an index

**Number of Recent Calls.** Count the pings in the last 3000 ms. Storing every ping and counting is the trap; it
rereads ancient history forever. Because time only moves forward, expired pings leave from the front in arrival order,
so the queue is exactly the window and its length is the answer. This is the first time the queue *is* the answer
rather than a means to it.

**Design Circular Queue.** Now the queue must live in `k` fixed slots, and the question is how to dequeue without
shifting. Move a label instead of the data: a `head` index and a `count`, with every index taken `% k` so the line wraps
around the seam. The puzzle inside is empty versus full, and `count` is what settles it.

**Design Circular Deque.** The same ring, with both ends movable. The back still grows by `count`; the front now grows
*backwards*, by stepping `head` counter-clockwise before writing. Nothing new is stored, which is the point: one more
formula turns a queue into a deque, and the step-then-write order is the whole difficulty.

### The finale: turn order

**Dota2 Senate.** Senators act in seat order, round after round, each banning an opponent, until one party is left.
Two questions hide in it: whom should each senator ban (the next opponent to act, a greedy choice), and how to simulate
rounds without rescanning banned seats. Two queues of turn times answer the second: compare the fronts, the earlier one
bans the other and rejoins as `i + n`. It closes the chapter because it uses everything at once: the queue as turn
order, the front as "who acts soonest", and a time stamp that makes rounds fit in one ordered line.
