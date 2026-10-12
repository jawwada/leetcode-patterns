---
rank: 100
slug: rate_limiter
---

A rate limiter decides, for each request arriving at time `t`, whether to let it through, so that a client cannot exceed an agreed rate; the two classic designs are the token bucket and the sliding log. With a budget of `3` requests per `6` seconds, four requests at time `0` and one at time `6` come out as allowed, allowed, allowed, rejected, allowed.

The token bucket holds up to `capacity` tokens and gains `rate` tokens per second; a request that finds a whole token spends it and passes, and one that does not is rejected. No timer is needed: each call first credits the tokens earned since the previous call, `(t - last) × rate`, caps the total at `capacity`, and only then decides, so the refill is lazy and the state is two numbers. A full bucket lets a burst of `capacity` requests through at once, and after that requests pass at the refill rate.

The sliding log keeps the times of the requests it allowed during the last `window` seconds in a queue, oldest at the front. A new request first drops every front time `≤ t - window`, which has left the window for good, and passes only if fewer than `limit` remain. Times arrive in order, so the expired ones always sit at the front; each is enqueued once and dequeued at most once, which makes the cost `O(1)` amortized. The log never holds more than `limit` times, so a ring buffer of that size (#76) can replace the queue.

Picture the bucket as a tank refilling at a constant trickle and the log as a frame sliding along the time axis. At the same long-run rate of half a request per second, the bucket spreads requests out after its burst, while the log refuses everything until its first three times slide out of the frame, then admits a fresh burst.

```text
          token bucket: capacity 3,        sliding log: limit 3,
          rate 0.5 per second              window 6 seconds
   t      tokens after refill              log after expiry
   0      3     ✓                          []          ✓
   0      2     ✓                          [0]         ✓
   0      1     ✓                          [0, 0]      ✓
   0      0     ✗                          [0, 0, 0]   ✗
   1      0.5   ✗                          [0, 0, 0]   ✗
   2      1     ✓                          [0, 0, 0]   ✗
   4      1     ✓                          [0, 0, 0]   ✗
   6      1     ✓                          []          ✓   0 ≤ 6 - 6: expired
   6      0     ✗                          [6]         ✓
   7      0.5   ✗                          [6, 6]      ✓
allowed   0 0 0 2 4 6                      0 0 0 6 6 7
          a burst, then a steady trickle   a burst, a wall, a new burst
```

```pseudo
CLASS TokenBucket
    FUNCTION Init(capacity, rate)
        self.capacity ← capacity
        self.rate ← rate                      // tokens added per second
        self.tokens ← capacity                // start full: a burst may pass
        self.last ← 0                         // time of the last refill

    FUNCTION Allow(t)
        refill ← (t - self.last) * self.rate  // earned since the last call
        self.tokens ← min(self.capacity, self.tokens + refill)
        self.last ← t
        IF self.tokens ≥ 1
            self.tokens ← self.tokens - 1
            RETURN true
        RETURN false

CLASS SlidingLog
    FUNCTION Init(limit, window)
        self.limit ← limit
        self.window ← window
        self.log ← empty queue                // allowed times, oldest first

    FUNCTION Allow(t)
        WHILE len(self.log) > 0 AND self.log.front() ≤ t - self.window
            self.log.dequeue()                // older than the window: expired
        IF len(self.log) < self.limit
            self.log.enqueue(t)
            RETURN true
        RETURN false
```

Both limiters cost `O(1)` per request, amortized for the log; the bucket stores two numbers per client and the log up to `limit` times. The trade-off is burst against precision. The bucket is cheap and smooth in the long run but admits up to `capacity + rate × T` requests in a span of `T` seconds, so a short span can beat the nominal rate: five requests pass before time `6` above, where the log lets only three through. The log enforces at most `limit` per window exactly and pays with memory that grows with the limit; a fixed-window counter is cheaper still but lets twice the limit through across a window boundary. The signals are "at most k per window", logger and hit-counter designs, and API throttling, where every client key gets a limiter of its own. The classic mistakes are refilling without the cap, so an idle client banks unlimited tokens, and an off-by-one at the window edge: a time `s` has expired exactly when `s ≤ t - window`.

*Practice:* LC 359 Logger Rate Limiter · LC 362 Design Hit Counter · LC 933 Number of Recent Calls · LC 1396 Design Underground System
