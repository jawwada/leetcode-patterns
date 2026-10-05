"""
Time Based Key-Value Store (LeetCode 981) - Medium
Chapter: design
Pattern: Sorted version list + binary search

Implement TimeMap: set(key, value, timestamp) stores a value for key at that time, and
get(key, timestamp) returns the value whose timestamp is the largest one <= timestamp, or "" if
none. All timestamps passed to set are strictly increasing.
Example: set("foo","bar",1); get("foo",1) -> "bar"; get("foo",3) -> "bar"; set("foo","bar2",4);
get("foo",4) -> "bar2"; get("foo",5) -> "bar2"; get("foo",0) -> "".
"""


# --- brute force ---
class BruteForce:
    """key -> list of (timestamp, value); get scans every version of the key. O(n) per get."""

    def __init__(self):
        self.store = {}

    def set(self, key, value, timestamp):
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        best_time = -1
        best_value = ""
        for time, value in self.store.get(key, []):
            if time <= timestamp and time > best_time:   # newest version not after timestamp
                best_time = time
                best_value = value
        return best_value


# --- optimal ---
class TimeMap:
    """Timestamps per key arrive sorted; binary search the newest one <= timestamp. O(log n) get."""

    def __init__(self):
        self.times = {}      # key -> ascending list of timestamps
        self.values = {}     # key -> values; values[key][i] was set at times[key][i]

    def set(self, key, value, timestamp):
        if key not in self.times:
            self.times[key] = []
            self.values[key] = []
        self.times[key].append(timestamp)     # strictly increasing, so the list stays sorted
        self.values[key].append(value)

    def get(self, key, timestamp):
        if key not in self.times:
            return ""
        times = self.times[key]
        lo = 0
        hi = len(times)
        while lo < hi:                        # find the first index whose time is > timestamp
            mid = (lo + hi) // 2
            if times[mid] <= timestamp:
                lo = mid + 1
            else:
                hi = mid
        if lo == 0:
            return ""                         # every version is newer than timestamp
        return self.values[key][lo - 1]       # the one just before it is the newest <= timestamp


# --- try the brute force ---
tm = BruteForce()
tm.set("foo", "bar", 1)
print(tm.get("foo", 1))      # -> bar
print(tm.get("foo", 3))      # -> bar
tm.set("foo", "bar2", 4)
print(tm.get("foo", 4))      # -> bar2
print(tm.get("foo", 5))      # -> bar2
print(tm.get("foo", 0))      # -> (empty line)


# --- try the optimal ---
tm = TimeMap()
tm.set("foo", "bar", 1)
print(tm.get("foo", 1))      # -> bar
print(tm.get("foo", 3))      # -> bar
tm.set("foo", "bar2", 4)
print(tm.get("foo", 4))      # -> bar2
print(tm.get("foo", 5))      # -> bar2
print(tm.get("foo", 0))      # -> (empty line)
