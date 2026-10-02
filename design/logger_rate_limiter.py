"""
Logger Rate Limiter (LeetCode 359)  — Easy
Pattern: Hash map of next-allowed timestamps

Problem
-------
Implement Logger.shouldPrintMessage(timestamp, message) -> bool: a message may be printed only
if the same message was not printed in the previous 10 seconds (so a message printed at t
blocks copies until t + 10 inclusive-exclusive: allowed again at t + 10). Timestamps arrive
in non-decreasing order.
Example: (1,"foo") True, (2,"bar") True, (3,"foo") False, (8,"bar") False, (10,"foo") False,
(11,"foo") True.

Brute force
-----------
Keep a list of every (timestamp, message) that was printed. For each call scan the list for the
same message with timestamp > now - 10. O(n) per call and O(n) space that never shrinks. The
wasted work is scanning entries for OTHER messages and entries so old they could never block
anything again.

From brute force to optimal
---------------------------
The only thing that matters for a message is its most recent print time, and the question
"was it printed in the last 10 s" is a single comparison against that one value. So keep
dict message -> next allowed timestamp: print iff timestamp >= next_ok[message], then set
next_ok[message] = timestamp + 10. O(1) per call. The tracker remembers one integer per
distinct message and forgets all earlier prints. If distinct messages are unbounded, pair the
dict with a queue of (time, message) and evict entries older than 10 s on each call to cap
memory at the number of messages printed in any 10-second window.

Intuition
---------
Rate limiting per key is just "remember when this key is allowed again". A hash map keyed by
the message gives that in O(1); overwriting the value on every successful print keeps it exact.

Geometric view
--------------
Timeline per message: a print at t stamps a closed gate over [t, t+10). Calls landing inside
the gate bounce (False); the first call at or past t+10 passes and lays a new gate.
"foo": |====gate [1,11)====| 11 passes -> |====[11,21)====|

Steps
-----
1. next_ok = {}.
2. On a call: if timestamp < next_ok.get(message, 0): return False.
3. Else next_ok[message] = timestamp + 10; return True.

Complexity: O(1) time per call, O(m) space for m distinct messages — one dict lookup and store.
Pitfalls: off-by-one at the boundary (t + 10 IS allowed); storing the last-printed time and
          comparing with 9 vs 10; letting the dict grow without bound when messages are unique.
"""
import random


class Logger:
    def __init__(self):
        self.next_ok = {}      # message -> earliest timestamp it may print again

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if timestamp < self.next_ok.get(message, 0):
            return False
        self.next_ok[message] = timestamp + 10
        return True


class BruteForce:
    """Keep every printed (timestamp, message); scan the whole log on each call, O(n)."""

    def __init__(self):
        self.printed = []

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        for t, m in self.printed:
            if m == message and timestamp - t < 10:
                return False
        self.printed.append((timestamp, message))
        return True


if __name__ == "__main__":
    lg = Logger()
    assert lg.shouldPrintMessage(1, "foo") is True
    assert lg.shouldPrintMessage(2, "bar") is True
    assert lg.shouldPrintMessage(3, "foo") is False
    assert lg.shouldPrintMessage(8, "bar") is False
    assert lg.shouldPrintMessage(10, "foo") is False
    assert lg.shouldPrintMessage(11, "foo") is True

    e = Logger()                                  # edge: same timestamp twice
    assert e.shouldPrintMessage(0, "x") and not e.shouldPrintMessage(0, "x")

    random.seed(5)
    fast, slow = Logger(), BruteForce()
    t = 0
    for _ in range(2000):
        t += random.choice([0, 1, 1, 3, 12])
        m = random.choice("abcde")
        assert fast.shouldPrintMessage(t, m) == slow.shouldPrintMessage(t, m)
    print("ok")
