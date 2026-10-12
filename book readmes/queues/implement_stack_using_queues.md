# Implement Stack using Queues

*LeetCode 225 · Easy · Pattern: Rotate a queue to make a stack · Reading time ~6 min*

## The problem

Build a LIFO stack with push, pop, top and empty using only queue operations (push to back, pop/peek from front, size,
is-empty).

```text
Example: push(1); push(2); top() -> 2; pop() -> 2; empty() ->
  False.
```

## What the problem is really asking

Build a last-in, first-out stack with `push(x)`, `pop()`, `top()` and `empty()`, using only queue operations: append to
the back, remove or read the front, size, is-empty. No reading from the back, no indexing into the middle.

The difficulty mirrors the previous problem: a queue only gives up its *oldest* item, and a stack must give up its
*newest*, which sits at the back, the end you may not read.

```text
push 1, 2, 3 into a queue

front -> [ 1 ][ 2 ][ 3 ] <- back
           ^              ^
     what a queue      what a stack
     lets you take     must return
```

## Do it by hand first

People stand in a single-file line facing a door; only the person at the door can leave. You want the person who joined
last to leave first. The trick a human finds quickly: as soon as someone new joins at the back, everyone ahead of them
walks out the door and rejoins the line behind them, one at a time.

```text
line: 2 1     3 joins:  2 1 3
              2 walks around:  1 3 2
              1 walks around:  3 2 1   <- 3 is at the door
```

After two walk-arounds the newcomer is at the door, and behind them the line reads 2, 1: still newest to oldest. What you
kept track of is how many people were in line before the newcomer, because that is exactly how many must walk around.

## The first honest attempt

Use two queues and do the work when reading. `push` appends to `q1`. To `pop` or `top`, move all but the last item of
`q1` into `q2`, and the item left in `q1` is the newest. Then swap the names.

```text
q1: [1, 2, 3]   top() ?
  move 1, 2 to q2 -> q1 [3], q2 [1, 2]   answer 3
  (top puts 3 back) -> q2 [1, 2, 3], swap names
top() again: move 1, 2 again ... answer 3 again
```

Push is O(1), but every `pop` and `top` is O(n): two `top()` calls in a row move the same n - 1 items twice to find
the same answer.

## The turning point

**Claim: if the queue always holds its items newest-first from front to back, a queue's front *is* a stack's top.**

A queue can read and remove its front in O(1). So arrange things so the newest item is at the front at all times, and
`pop`, `top` and `empty` become one-liners. All the work moves to `push`, where it is done once per item instead of
once per read.

How does `push` put the newcomer at the front? Not by pouring into another queue: pouring a queue into a queue keeps the
order, so unlike stacks there is no reversal to exploit. What a queue *can* do is **rotate**: take the front and append
it to the back. Append `x`, then rotate `n - 1` times, where `n` is the new size. Each rotation sends one older item
around behind `x`, and they go around in their existing order, so after `n - 1` rotations the line reads `x`, then the
old line unchanged.

```text
before: [3, 2, 1]  (newest first)   push 4
append:        [3, 2, 1, 4]
rotate 3 times: [2, 1, 4, 3] -> [1, 4, 3, 2] -> [4, 3, 2, 1]
```

One queue suffices; the brute force's second queue was only a parking lot.

## Watch it work

Operations: `push 1, push 2, push 3, top, pop, push 4, top`. The queue is drawn front on the left.

```text
Frame 1: push 1
  append:   [1]        rotate 0 times
  queue     [1]        front = top = 1
```

Nothing to rotate.

```text
Frame 2: push 2
  append:   [1, 2]
  rotate 1: [2, 1]     front = top = 2
```

One older item walks around behind the newcomer.

```text
Frame 3: push 3
  append:   [2, 1, 3]
  rotate 1: [1, 3, 2]
  rotate 2: [3, 2, 1]  front = top = 3
```

Two rotations; the old items 2, 1 keep their relative order behind 3.

```text
Frame 4: top -> 3, then pop -> 3
  queue     [2, 1]     front = top = 2
```

Both reads are O(1) front operations; after the pop, 2 is already at the front.

```text
Frame 5: push 4, then top
  append:   [2, 1, 4]
  rotate 2: [1, 4, 2] -> [4, 2, 1]
  top -> 4
```

The queue reads newest to oldest again: 4, 2, 1.

After every operation the queue read front to back in exactly the order a stack would pop: newest first.

## Why it is correct

Invariant: between operations, the queue from front to back lists the stack from top to bottom. It holds for the empty
queue. A push appends `x` behind the `n - 1` old items, which are in top-to-bottom order; rotating `n - 1` times moves
each of them, in that same order, from the front to the back, so the queue becomes `x` followed by the old top-to-bottom
order, which is the new stack from top to bottom. A pop removes the front, which is the top, and leaves the rest in
order. `top` reads the front without changing anything. So every pop and top returns the most recently pushed item that
is still present: LIFO.

## Cost

Time: push O(n) because it performs `n - 1` rotations; pop, top and empty O(1).
Space: O(n) for the single queue.

Unlike the two-stack queue, there is no amortised rescue here: pushing n items in a row costs 0 + 1 + ... + (n - 1)
rotations, O(n^2) in total. The brute force has the same total cost, just charged to the reads instead of the pushes.
Choose the version that makes the more frequent operation cheap.

## Variations you will meet

- **Read-heavy vs write-heavy.** If pushes dominate, the brute force (cheap push, expensive pop) is better. Interviewers
  like to ask which one you would pick and why.
- **Two-queue version required.** Some versions insist on two queues: push into the empty one, then drain the other into
  it behind the newcomer. Same cost, same idea.
- **Rotation as a tool.** `deque.rotate(k)` turns a ring of items in O(k). It reappears in circular games such as Find
  the Winner of the Circular Game (1823): rotate `k - 1`, then pop.

## What to carry forward

A queue cannot reverse, but it can rotate; turning the ring after each push keeps the newest item at the exit. The next
problem stops simulating other structures and uses a queue for what it is good at: letting the oldest items expire.
