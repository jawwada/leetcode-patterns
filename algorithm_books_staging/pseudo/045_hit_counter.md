---
rank: 45
slug: hit_counter
---

Design a counter of recent traffic: `hit(timestamp)` records a hit at a time given in whole seconds, and `get_hits(timestamp)` returns how many hits arrived in the past 300 seconds, at times `s` with `timestamp - 300 < s ≤ timestamp`. Calls come in time order, and many hits may share a second. After hits at seconds 1, 2, 2, 3 and 300, `get_hits(300)` is 5 and `get_hits(301)` is 4: the hit at second 1 is now exactly 300 seconds old and has left the window.

The first design to come to mind is the sliding log of the rate limiter (#138), a queue of every hit's time with the expired times dropped from the front. It is `O(1)` amortized per call, but its memory grows with the traffic: a million hits in one second are a million entries, which is LeetCode's follow-up question. The window never needs more than 300 numbers, one count per second, so keep 300 buckets bent into a ring. Second `t` lives in bucket `t mod 300`; the 300 seconds of any window fall into 300 different buckets, and second `t + 300` returns to the bucket of second `t` at the very moment `t` leaves the window.

A reused bucket must never mix two seconds, so each bucket stores the second it counts next to its count. A hit at second `t` goes to bucket `t mod 300`: if the bucket's time is `t` its count goes up by one, and otherwise the bucket is still empty or holds a second at least 300 seconds old, outside every future window, and is reset to `(t, 0)` first. `get_hits` walks all 300 buckets and adds the counts whose age, `timestamp - time`, is under 300; a stale bucket that no hit has reclaimed fails the same test, so nothing is ever cleaned up eagerly. The trace follows the four buckets this sequence touches.

```text
bucket = t mod 300 holds (time, count); buckets 4 to 299 stay (0, 0)
call            bucket 0    bucket 1    bucket 2    bucket 3    returns
hit(1)          (0, 0)      (1, 1)      (0, 0)      (0, 0)
hit(2), hit(2)  (0, 0)      (1, 1)      (2, 2)      (0, 0)
hit(3)          (0, 0)      (1, 1)      (2, 2)      (3, 1)
get_hits(4)       +0          +1          +2          +1         4
hit(300)        (300, 1)    (1, 1)      (2, 2)      (3, 1)
get_hits(300)     +1          +1          +2          +1         5
get_hits(301)     +1        ✗ age 300     +2          +1         4
hit(301)        (300, 1)    (301, 1)    (2, 2)      (3, 1)      bucket 1 reset
get_hits(301)     +1          +1          +2          +1         5
get_hits(600)   ✗ age 300     +1        ✗ age 598   ✗ age 597    1
get_hits(601)   ✗ age 301   ✗ age 300   ✗ age 599   ✗ age 598    0
+c: t - time < 300, count c added     ✗: 300 or more seconds old, skipped
```

```pseudo
CLASS HitCounter
    FUNCTION Init()
        self.window ← 300                      // seconds get_hits looks back
        self.times ← array of self.window zeros     // bucket i: its second
        self.counts ← array of self.window zeros    // bucket i: hits in it

    FUNCTION Hit(timestamp)
        slot ← timestamp mod self.window
        IF self.times[slot] ≠ timestamp        // empty, or 300+ seconds old
            self.times[slot] ← timestamp
            self.counts[slot] ← 0
        self.counts[slot] ← self.counts[slot] + 1

    FUNCTION GetHits(timestamp)
        total ← 0
        FOR slot FROM 0 TO self.window - 1
            IF timestamp - self.times[slot] < self.window    // in the window
                total ← total + self.counts[slot]
        RETURN total
```

`hit` runs in `O(1)` and `get_hits` in `O(300)`, a constant for a fixed window, and the memory is 600 numbers whatever the traffic; a window of `W` seconds needs `O(W)` per query and `O(W)` memory. The price is resolution, and coarser buckets trade more of it for longer windows: 60 one-minute buckets count the last hour with an edge accurate to a minute, the way monitoring systems keep their counters. Counts add, so a fleet of servers can each keep a ring and sum them at query time. Reach for buckets when the question is how many events fell in the last N units of time under heavy traffic; Number of Recent Calls (LC 933) keeps the queue, because its times strictly increase and its queue never holds more than 3001 entries, one per millisecond of the window. The classic mistake is reusing a bucket without zeroing it: the hit at second 301 lands on the leftover hit from second 1, and the last `get_hits(301)` returns 6 instead of 5. Its twin is `≤` in the age test, which still counts the hit at second 1 in the first `get_hits(301)` and returns 5 instead of 4.

*Practice:* LC 362 Design Hit Counter · LC 359 Logger Rate Limiter · LC 933 Number of Recent Calls
