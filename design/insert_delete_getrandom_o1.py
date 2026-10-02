"""
Insert Delete GetRandom O(1) (LeetCode 380)  — Medium
Pattern: Array + index map (swap-with-last delete)

Problem
-------
Implement RandomizedSet with insert(val) -> bool (False if present), remove(val) -> bool
(False if absent) and getRandom() -> a uniformly random element, each in average O(1).
Example: insert(1) True, remove(2) False, insert(2) True, getRandom() in {1,2}, remove(1) True,
insert(2) False, getRandom() == 2.

Brute force
-----------
Keep a plain list. insert scans for duplicates (O(n)), remove scans then pops from the middle
(O(n) scan + O(n) shift), getRandom indexes a random position (O(1)). Space O(n). The wasted
work is the scanning for membership and the shifting of every element after the removed slot
just to keep the list contiguous.

From brute force to optimal
---------------------------
getRandom needs a contiguous array so random.choice is uniform and O(1); membership needs a
hash set. Combine them: a list of values plus dict val -> index. Insert appends and records the
index. Remove is the clever part: the array only needs to stay contiguous, NOT ordered, so
instead of shifting, overwrite the hole with the LAST element, fix that element's index in the
dict, and pop the tail. The tracker remembers each value's slot so deletion never searches,
and it can forget insertion order entirely.

Intuition
---------
An array with "no holes" is all getRandom asks for. Deleting from the middle of an array is
expensive only if you insist on preserving order. Swapping the victim with the last element
and popping the end keeps the array dense in O(1); the dict is updated for the single element
that moved.

Geometric view
--------------
vals: [ 5, 8, 2, 9 ]   idx: {5:0, 8:1, 2:2, 9:3}
remove(8): copy last (9) into slot 1 -> [5, 9, 2, 9], idx[9]=1, pop tail -> [5, 9, 2],
del idx[8]. The array shrinks from the right only; the dict always mirrors it exactly.

Steps
-----
1. insert: if val in idx return False; idx[val] = len(vals); vals.append(val); True.
2. remove: if val not in idx return False; i = idx[val]; last = vals[-1];
   vals[i] = last; idx[last] = i; vals.pop(); del idx[val]; True.
3. getRandom: random.choice(vals).

Complexity: O(1) average time per operation, O(n) space — dict lookup plus one swap and pop.
Pitfalls: removing the last element (swap with itself must still work: update idx[last] BEFORE
          deleting idx[val]); using a set alone (no O(1) uniform random access).
"""
import random


class RandomizedSet:
    def __init__(self):
        self.vals = []        # dense array for O(1) uniform random choice
        self.idx = {}         # val -> position in vals

    def insert(self, val: int) -> bool:
        if val in self.idx:
            return False
        self.idx[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.idx:
            return False
        i, last = self.idx[val], self.vals[-1]
        self.vals[i], self.idx[last] = last, i    # fill the hole with the last element
        self.vals.pop()
        del self.idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)


class BruteForce:
    """Plain list; insert/remove scan for membership and pop from the middle, O(n)."""

    def __init__(self):
        self.vals = []

    def insert(self, val: int) -> bool:
        if val in self.vals:                      # O(n) scan
            return False
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.vals:
            return False
        self.vals.remove(val)                     # O(n) scan + O(n) shift
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)


if __name__ == "__main__":
    s = RandomizedSet()
    assert s.insert(1) is True
    assert s.remove(2) is False
    assert s.insert(2) is True
    assert s.getRandom() in (1, 2)
    assert s.remove(1) is True
    assert s.insert(2) is False
    assert s.getRandom() == 2

    e = RandomizedSet()                  # edge: remove the only element then re-insert
    assert e.insert(7) and e.remove(7) and e.insert(7) and e.getRandom() == 7

    random.seed(2)
    fast, slow = RandomizedSet(), BruteForce()
    for _ in range(1000):
        v = random.randint(0, 20)
        if random.random() < 0.5:
            assert fast.insert(v) == slow.insert(v)
        else:
            assert fast.remove(v) == slow.remove(v)
        assert sorted(fast.vals) == sorted(slow.vals)
        if fast.vals:
            assert fast.getRandom() in slow.vals
    print("ok")
