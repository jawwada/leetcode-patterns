"""
Time-Based Key-Value Store - Per-Key Timestamp Lists + Binary Search

Keep every version of a key: set(key, value, t) records value at time t (the
times of each key only grow), and get(key, t) returns the value set at the
largest time <= t, or "" if none: set status = draft at 1, review at 4,
live at 9; get status at 5 -> "review".
"""


# --- algorithm ---
class TimeMap:
    """Per key, parallel lists of times and values. set O(1), get O(log n)."""

    def __init__(self):
        self.times = {}             # key -> increasing list of set times
        self.values = {}            # key -> the values, in the same order

    def set(self, key, value, timestamp):
        """Append the version to both lists of the key. O(1) amortized."""
        if key not in self.times:
            self.times[key] = []
            self.values[key] = []
        self.times[key].append(timestamp)   # times only grow: stays sorted
        self.values[key].append(value)

    def get(self, key, timestamp):
        """First time > timestamp, minus one: the last time <= it. O(log n)."""
        if key not in self.times:
            return ""
        times = self.times[key]
        left = 0
        right = len(times)
        while left < right:             # find the first time > timestamp
            mid = (left + right) // 2
            if times[mid] <= timestamp:
                left = mid + 1          # mid is not after timestamp
            else:
                right = mid             # mid is after: maybe the first
        if left == 0:
            return ""                   # every version is newer
        return self.values[key][left - 1]


# --- try it ---
store = TimeMap()
store.set("status", "draft", 1)
store.set("status", "review", 4)
store.set("status", "live", 9)
print(store.get("status", 5), store.get("status", 9))    # -> review live
print(store.get("status", 4), store.get("status", 100))  # -> review live
print(repr(store.get("status", 0)), repr(store.get("owner", 5)))   # -> '' ''
