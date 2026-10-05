# Number of Recent Calls

*LeetCode 933 · Easy · Pattern: Sliding time window with a deque · Reading time ~6 min*

## The problem

RecentCounter.ping(t) records a request at time t in milliseconds and returns how many requests fall in the inclusive
window [t - 3000, t]. Each call uses a strictly larger t than the previous one.

```text
Example: ping(1) -> 1; ping(100) -> 2; ping(3001) -> 3;
  ping(3002) -> 3, because t = 1 is now older than 3002 - 3000 =
  2.
```

## What the problem is really asking

A `RecentCounter` receives `ping(t)` calls, where `t` is a time in milliseconds and every call's `t` is strictly larger
than the last. Each call must return how many pings, including this one, happened in the inclusive window
`[t - 3000, t]`.

Each answer is a count, but the real object is the *set of pings still inside the window*, which moves with every
call while the history grows.

```text
pings at 1, 100, 3001, 3002          window for t = 3002
                                     [2 ........... 3002]
time:  1    100          3001 3002
       *     *             *    *
       x    [------------------]
       1 < 2: outside        answer: 3
```

## Do it by hand first

Write the pings on a strip of paper as they come: 1, 100, 3001. For the ping at 3002, the window starts at 2. You look at
the leftmost number, 1, and cross it out: too old. Then you look at 100: inside. You stop there, because everything to
its right arrived later and is even newer. Count what is not crossed out: 3.

```text
strip:  [x1] 100  3001  3002
         ^ crossed out once, never looked at again
```

The next ping, at 7000, starts its window at 4000. You cross out 100, 3001, 3002 from the left, stop at 7000, and count
1. You never uncrossed anything. Your hand kept a strip of uncrossed pings and only ever worked at its two ends: new
pings on the right, crossings-out on the left.

## The first honest attempt

Store every timestamp in a list. On each ping, append `t` and count the stored values that are at least `t - 3000`.

```text
ping 3002: scan 1, 100, 3001, 3002          -> 3
ping 7000: scan 1, 100, 3001, 3002, 7000    -> 1
ping 7001: scan 1, 100, 3001, 3002, 7000,   -> 2
           7001
           ^^^^^^^^^^^^^^^^^^^^
           these are rechecked forever, though they can
           never be inside a window again
```

Each ping costs O(n) and the list grows without limit; the repeated work is re-examining timestamps already too old.

## The turning point

**Claim: once a ping falls out of the window, it stays out forever, and the pings that fall out are always the oldest
ones.**

The window's left edge is `t - 3000`, and `t` strictly increases, so the left edge only moves right. A ping older than
the left edge now will be older than every future left edge too. And because pings arrive in time order, the old ones
form a block at the start of the history: if ping `a` is too old and ping `b` arrived before `a`, then `b` is too old as
well.

So the in-window pings are always a contiguous run at the end of the history, and to maintain it you only need two
moves: **append the new ping at the back**, and **pop from the front while the front is older than `t - 3000`**. That is
precisely a FIFO queue. The answer is just the queue's length.

```text
queue (front = oldest)        left edge 4000
[ 100 ][ 3001 ][ 3002 ][ 7000 ]
  pop     pop     pop     stays: 7000 >= 4000
```

The boundary is inclusive: a ping at exactly `t - 3000` counts, so evict only on strict `<`.

## Watch it work

Pings: 1, 100, 3001, 3002, 7000. The queue is drawn front on the left.

```text
Frame 1: ping(1)          left edge = 1 - 3000 = -2999
  append 1                queue [1]
  front 1 >= -2999: stop  return 1
```

Nothing can be too old yet.

```text
Frame 2: ping(100)        left edge = -2900
  append 100              queue [1, 100]
  front 1 >= -2900: stop  return 2
```

One check of the front is enough; there is nothing to evict.

```text
Frame 3: ping(3001)       left edge = 1
  append 3001             queue [1, 100, 3001]
  front 1 >= 1: stop      return 3
```

The inclusive boundary matters: 1 sits exactly on the left edge and stays.

```text
Frame 4: ping(3002)       left edge = 2
  append 3002             queue [1, 100, 3001, 3002]
  front 1 < 2: pop        queue [100, 3001, 3002]
  front 100 >= 2: stop    return 3
```

The first eviction. Ping 1 leaves for good.

```text
Frame 5: ping(7000)       left edge = 4000
  append 7000             queue [100, 3001, 3002, 7000]
  pop 100, 3001, 3002     queue [7000]
  front 7000 >= 4000      return 1
```

One call pops three items, each pushed once and popped once.

In every frame the queue held exactly the pings inside `[t - 3000, t]`, in arrival order, and its length was the
answer.

## Why it is correct

Invariant: after each call, the queue contains exactly the pings with time in `[t - 3000, t]`, oldest at the front.
Suppose it holds after the previous call with time `t'`. The new ping `t` is in its own window, so appending it is
right. Every ping that was in the queue had time at least `t' - 3000`, and the new window's edge `t - 3000` is larger, so
some prefix of the queue may now be too old, and nothing else: the queue is sorted by time, so once the front is inside
the window, everything behind it is too. Popping while `front < t - 3000` removes exactly that prefix. Pings already
evicted earlier are older still, so none of them belongs back in. Hence the queue length is the requested count.

## Cost

Time: O(1) amortised per ping. Each timestamp is appended once and popped at most once, so any sequence of n pings does
at most 2n queue operations, though a single ping may pop many.
Space: O(W), where W is the largest number of pings inside any 3000 ms window. LeetCode caps it at 3001 because times
are distinct integers.

## Variations you will meet

- **Moving Average from Data Stream (346).** The window is "the last k values" instead of "the last 3000 ms", and you
  keep a running sum: add on append, subtract on pop. Same queue.
- **Design Hit Counter (362).** Many hits can share a timestamp and calls may be read without a hit. Store `(time,
  count)` buckets in the queue with a running total, or use a fixed ring of 300 one-second buckets.
- **Out-of-order timestamps.** If `t` could decrease, the front would no longer be the oldest and this argument breaks.
  You would need a sorted structure and binary search (Binary Search chapter) or a heap.

## What to carry forward

When time only moves forward, expiry happens in arrival order, so the oldest item is always the next to leave, exactly
what a queue's front offers. The next problem keeps the queue but removes the unlimited memory: it must live in k fixed
slots.
