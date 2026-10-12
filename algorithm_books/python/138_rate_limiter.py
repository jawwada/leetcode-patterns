"""
Rate Limiter - Token Bucket and Sliding Log

Decide for each request at time t (in seconds) whether to let it through, so a
client gets at most a fixed rate: with 3 requests per 6 seconds, requests at
times 0, 0, 0, 0, 6 -> allowed, allowed, allowed, rejected, allowed.
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
def allowed_times(limiter, times):
    """Send one request at each time, in order; return the times let through."""
    allowed = []
    for t in times:
        if limiter.allow(t):
            allowed.append(t)
    return allowed


# --- algorithm ---
class TokenBucket:
    """Up to capacity tokens, refilled at rate per second; a request spends
    one. O(1) time per request and O(1) memory."""

    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate                # tokens added per second
        self.tokens = capacity          # start full: a burst may pass
        self.last = 0                   # time of the last refill

    def allow(self, t):
        """Refill for the time since the last call, then spend a token. O(1)."""
        refill = (t - self.last) * self.rate    # earned since the last call
        self.tokens = min(self.capacity, self.tokens + refill)
        self.last = t
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class SlidingLog:
    """The times of the requests allowed in the last window seconds.
    O(1) amortized time per request, O(limit) memory."""

    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.log = deque()              # allowed times, oldest first

    def allow(self, t):
        """Drop expired times; allow if under the limit. O(1) amortized."""
        while len(self.log) > 0 and self.log[0] <= t - self.window:
            self.log.popleft()          # older than the window: expired
        if len(self.log) < self.limit:
            self.log.append(t)
            return True
        return False


# --- try it ---
times = [0, 0, 0, 0, 1, 2, 4, 6, 6, 7]
print(allowed_times(TokenBucket(3, 0.5), times))  # -> [0, 0, 0, 2, 4, 6]
print(allowed_times(SlidingLog(3, 6), times))     # -> [0, 0, 0, 6, 6, 7]
print(allowed_times(SlidingLog(1, 10), [1, 3, 10, 11]))   # -> [1, 11]
