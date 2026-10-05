"""
Insert Delete GetRandom O(1) (LeetCode 380) - Medium
Chapter: design
Pattern: Array + index map (swap-with-last delete)

Implement RandomizedSet with insert(val) -> bool (False if already present), remove(val) -> bool
(False if absent) and get_random() -> a uniformly random element, each in average O(1).
Example: insert(1) True, remove(2) False, insert(2) True, get_random() in {1, 2}, remove(1) True,
insert(2) False, get_random() == 2.
"""
import random   # random.choice picks one element of a list uniformly


# --- brute force ---
class BruteForce:
    """Plain list; insert and remove scan for the value. O(n) per insert and remove."""

    def __init__(self):
        self.vals = []

    def insert(self, val):
        if val in self.vals:              # O(n) scan
            return False
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.vals:
            return False
        self.vals.remove(val)             # O(n) scan, then everything after it shifts left
        return True

    def get_random(self):
        return random.choice(self.vals)


# --- optimal ---
class RandomizedSet:
    """Dense list for random choice + dict val -> index; delete by swapping with the last. O(1)."""

    def __init__(self):
        self.vals = []
        self.index_of = {}

    def insert(self, val):
        if val in self.index_of:
            return False
        self.index_of[val] = len(self.vals)   # it will sit at the end of the list
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.index_of:
            return False
        i = self.index_of[val]
        last = self.vals[-1]
        self.vals[i] = last               # move the last element into the hole
        self.index_of[last] = i
        self.vals.pop()                   # the hole is now at the end: cheap to drop
        del self.index_of[val]
        return True

    def get_random(self):
        return random.choice(self.vals)


# --- try the brute force ---
s = BruteForce()
print(s.insert(1))                  # -> True
print(s.remove(2))                  # -> False
print(s.insert(2))                  # -> True
print(s.get_random() in (1, 2))     # -> True
print(s.remove(1))                  # -> True
print(s.insert(2))                  # -> False
print(s.get_random())               # -> 2


# --- try the optimal ---
s = RandomizedSet()
print(s.insert(1))                  # -> True
print(s.remove(2))                  # -> False
print(s.insert(2))                  # -> True
print(s.get_random() in (1, 2))     # -> True
print(s.remove(1))                  # -> True
print(s.insert(2))                  # -> False
print(s.get_random())               # -> 2
