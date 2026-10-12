"""
Cache with Expiring Keys - Lazy Expiry + a Min-Heap of Deadlines

Design a cache whose keys expire: put(key, value, ttl, now) keeps the value
until time now + ttl, get(key, now) returns it only while now is earlier, and
size(now) counts the live keys. After put(b, 2, 3, 1):
get(b, 3), get(b, 4) -> 2, None.
"""
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class TTLCache:
    """Map key -> (value, expire_at) plus a min-heap of (expire_at, key)
    pairs, some of them stale. get O(1), put O(log n)."""

    def __init__(self):
        self.entries = {}           # key -> (value, expire_at)
        self.deadlines = []         # min-heap of (expire_at, key), some stale

    def put(self, key, value, ttl, now):
        """Store until now + ttl; a rewrite replaces the deadline. O(log n)."""
        expire_at = now + ttl
        self.entries[key] = (value, expire_at)
        heapq.heappush(self.deadlines, (expire_at, key))   # old pair goes stale

    def get(self, key, now):
        """The value while now < expire_at; an expired key is removed. O(1)."""
        if key not in self.entries:
            return None
        value, expire_at = self.entries[key]
        if now >= expire_at:
            del self.entries[key]   # lazy expiry: found dead on a read
            return None
        return value

    def purge(self, now):
        """Pop every pair whose time has come; delete keys whose pair is
        current. O(log n) per popped pair."""
        while len(self.deadlines) > 0 and self.deadlines[0][0] <= now:
            expire_at, key = heapq.heappop(self.deadlines)  # earliest first
            if key in self.entries and self.entries[key][1] == expire_at:
                del self.entries[key]   # current pair: the key expired
            # any other pair is stale: the key was rewritten or removed

    def size(self, now):
        """Purge, then count the live keys. O(k log n) for k popped pairs."""
        self.purge(now)
        return len(self.entries)


# --- try it ---
cache = TTLCache()
cache.put("a", 1, 5, 0)             # a lives until 5
cache.put("b", 2, 3, 1)             # b lives until 4
cache.put("c", 3, 10, 2)            # c lives until 12
print(cache.get("b", 3), cache.get("b", 4))     # -> 2 None
cache.put("a", 7, 5, 4)             # rewrite: a lives until 9, (5, a) is stale
print(cache.size(6))                # -> 2
print(cache.get("a", 8), cache.get("a", 9))     # -> 7 None
print(cache.size(11), cache.size(12))           # -> 1 0
