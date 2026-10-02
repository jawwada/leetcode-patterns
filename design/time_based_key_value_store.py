"""
Time Based Key-Value Store (LeetCode 981)  — Medium
Pattern: Sorted version list + binary search

Problem
-------
Implement TimeMap: set(key, value, timestamp) stores a value for key at that time; get(key,
timestamp) returns the value whose timestamp is the LARGEST one <= timestamp, or "" if none.
All set timestamps are strictly increasing.
Example: set("foo","bar",1); get("foo",1)->"bar"; get("foo",3)->"bar"; set("foo","bar2",4);
get("foo",4)->"bar2"; get("foo",5)->"bar2"; get("foo",0)->"".

Brute force
-----------
dict key -> list of (timestamp, value). set appends. get scans the entire list for the largest
timestamp <= the query. O(1) set, O(n) get, O(n) space. The wasted work is the scan: we look
at every version, including ones far in the future and far in the past, to find one boundary.

From brute force to optimal
---------------------------
Timestamps are inserted strictly increasing, so each key's list is already sorted for free: no
sorting step, no balanced tree. "Largest timestamp <= t" on a sorted list is bisect_right(t) - 1,
an O(log n) binary search. Keep two parallel lists per key (timestamps, values) so bisect works
on plain ints. The tracker remembers every version (the problem asks for history), but it never
needs to re-order anything; the invariant "append keeps it sorted" is what the sortedness
guarantee buys us.

Intuition
---------
Versioned storage is a sorted timeline per key. A query is "snap to the most recent version at
or before time t", which is the classic right-bisect: find where t would go, step back one.

Geometric view
--------------
key "foo":  times  [ 1, 4, 9 ]      get(5): bisect_right -> index 2
            vals   [ a, b, c ]                  ^ step back: index 1 -> "b"
get(0): bisect_right -> 0, nothing to the left -> "".

Steps
-----
1. times[key], vals[key] as parallel lists (defaultdict(list)).
2. set: append timestamp and value (stays sorted by guarantee).
3. get: if key unknown return ""; i = bisect_right(times[key], timestamp);
   return vals[key][i-1] if i > 0 else "".

Complexity: O(1) set, O(log n) get per key with n versions, O(total versions) space —
            a sorted-by-construction list plus one binary search.
Pitfalls: bisect_left vs bisect_right (equal timestamps must match); forgetting the i == 0 case;
          storing (ts, val) tuples and bisecting on them (string comparison on val can bite).
"""
import random
from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    def __init__(self):
        self.times = defaultdict(list)    # key -> ascending timestamps
        self.vals = defaultdict(list)     # key -> values aligned with times

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)  # timestamps strictly increase -> list stays sorted
        self.vals[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.times:
            return ""
        i = bisect_right(self.times[key], timestamp)   # first index with time > timestamp
        return self.vals[key][i - 1] if i else ""


class BruteForce:
    """key -> list of (timestamp, value); get scans every version, O(n)."""

    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        best_t, best_v = -1, ""
        for t, v in self.store.get(key, []):
            if best_t < t <= timestamp:
                best_t, best_v = t, v
        return best_v


if __name__ == "__main__":
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"
    assert tm.get("foo", 0) == ""          # edge: before the first version
    assert tm.get("nope", 7) == ""         # edge: unknown key

    random.seed(6)
    fast, slow = TimeMap(), BruteForce()
    clock = {k: 0 for k in "abc"}
    for _ in range(1500):
        k = random.choice("abc")
        if random.random() < 0.5:
            clock[k] += random.randint(1, 5)
            v = str(random.randint(0, 999))
            fast.set(k, v, clock[k])
            slow.set(k, v, clock[k])
        else:
            q = random.randint(0, clock[k] + 3)
            assert fast.get(k, q) == slow.get(k, q)
    print("ok")
