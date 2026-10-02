# Logger Rate Limiter

*LeetCode 359 · Easy · Pattern: Hash map of next-allowed timestamps · Reading time ~5 min*

## What the problem is really asking

Messages arrive with timestamps in non-decreasing order. For each one, `shouldPrintMessage(timestamp, message)` answers yes or no: yes if this exact message has not been *printed* in the last 10 seconds. A message printed at time t blocks its copies at t+1 through t+9 and is allowed again at t+10. Each answer is a boolean; the object answering keeps state across calls.

The subtle part is the word *printed*. A rejected call does not reset anything. Only successful prints lay down a new 10-second block.

```text
 time:   1     2     3     8     10    11
 msg:   foo   bar   foo   bar   foo   foo
 print:  T     T     F     F     F     T
         foo blocked over [1, 11) ---->| allowed at 11
```

## Do it by hand first

Imagine you are the logger with a notepad. When "foo" prints at 1, you would not write "foo printed at 1" and later compute. You would write "foo: OK again at 11". When "bar" prints at 2, write "bar: OK again at 12". At time 3, someone asks about foo: glance at the note, 3 < 11, refuse. At 11, 11 >= 11, allow — and overwrite the note with "foo: OK again at 21".

```text
 notepad after t=2       after t=11
 foo -> 11               foo -> 21
 bar -> 12               bar -> 12
```

Your hand kept one number per message: the earliest time it may print again. Every older fact about that message was irrelevant.

## The first honest attempt

Keep a log of every printed (timestamp, message) pair. On each call, scan the whole log for an entry with the same message and `timestamp - t < 10`. If found, refuse; otherwise append and allow.

It is O(n) per call where n is the number of prints so far, and the log grows forever.

```text
 log: (1,foo) (2,bar) (11,foo) (12,bar) (21,foo) ...
 query (25, bar): scan ALL of them
   (1,foo)  wrong message   wasted
   (2,bar)  23 s old        wasted, can never block again
   (11,foo) wrong message   wasted
   ...
```

Two kinds of waste: comparing against other messages, and comparing against prints so old they can never block anything again.

## The turning point

**Claim: whether a message may print now depends only on that message's most recent successful print.**

Justification: an older print of the same message happened earlier than the most recent one, so its block ended earlier too. If the most recent block does not cover `timestamp`, no older block does. So every print except the latest per message is dead information.

That gives the design directly. The operation asks "is this message allowed at time t?" The fact needed is "when is it next allowed?" — one integer per message, looked up by the message. Lookup by key is a hash map. Store `next_ok[message] = t + 10` on each successful print; answer with one comparison. A message never seen gets the default 0, which any timestamp passes.

Storing the *next allowed* time instead of the *last printed* time is a small choice that pays off: the comparison becomes `timestamp >= next_ok`, with no "is it 9 or 10" arithmetic at query time. Put the boundary in the stored value once and it cannot be got wrong per call.

```text
 if timestamp < next_ok.get(message, 0): return False
 next_ok[message] = timestamp + 10
 return True
```

## Watch it work

Calls: (1,foo) (2,bar) (3,foo) (8,bar) (10,foo) (11,foo) (12,bar).

```text
Frame 1  (1, foo) -> True
 next_ok: { foo: 11 }
```
foo was absent (default 0), 1 >= 0, so it prints and stores 1 + 10.

```text
Frame 2  (2, bar) -> True
 next_ok: { foo: 11, bar: 12 }
```
A different key; foo's entry is untouched.

```text
Frame 3  (3, foo) -> False ; (8, bar) -> False
 next_ok: { foo: 11, bar: 12 }    (unchanged)
 3 < 11 blocked     8 < 12 blocked
```
Refusals do not write, so the blocks are not extended.

```text
Frame 4  (10, foo) -> False
 next_ok: { foo: 11, bar: 12 }
 10 < 11   one second short
```
The boundary: 9 seconds after the print is still blocked.

```text
Frame 5  (11, foo) -> True ; (12, bar) -> True
 next_ok: { foo: 21, bar: 22 }
```
Each message reaches its stored time exactly and prints; the notes move forward 10.

Through every frame the map holds exactly one integer per message ever printed, and that integer is 10 more than its latest print time.

## Why it is correct

Invariant: for every message m printed at least once, `next_ok[m]` equals (last print time of m) + 10; for unprinted messages there is no entry. A call returns False only when `timestamp < next_ok[m]`, meaning the last print was fewer than 10 seconds ago — exactly the blocking condition. Otherwise it returns True and records the new print, restoring the invariant. Because only the latest print can block (older blocks end earlier), checking this one value is sufficient.

## Cost

- **Time:** O(1) average per call — one dict lookup and at most one store.
- **Space:** O(m) for m distinct messages ever printed.

## Variations you will meet

- **Unbounded distinct messages.** The map grows forever. Pair it with a queue of (time, message) prints and, on each call, pop entries older than 10 seconds and delete their keys if still current. Memory becomes "messages printed in the last 10 seconds" — the hit counter's queue, next.
- **Out-of-order timestamps.** The "latest print decides" argument breaks; you need per-message sorted print times and a bisect.
- **Allow k prints per window.** One integer is no longer enough; keep a small queue of the last k print times per message (a sliding window per key), or a token bucket: tokens refill at rate k/10 and each print spends one.
- **Distributed rate limiter.** The same map lives in a shared store with atomic compare-and-set; the logic is unchanged.

## What to carry forward

Per-key rate limiting is "remember when this key is allowed again" — one integer in a hash map, overwritten on success. The next problem drops the key and counts all events in a time window, which brings the queue back and makes eviction a loop.
