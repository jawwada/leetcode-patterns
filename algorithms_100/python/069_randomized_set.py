"""
Insert Delete GetRandom O(1) - Array + Index Map, Swap with Last

Design a set with insert, remove and get_random in average O(1) time each,
where get_random returns every stored value with equal probability:
insert 10, 20, 30, then remove 10 -> values [30, 20].
"""
import random                       # randint(a, b) is uniform on a..b inclusive


# --- algorithm ---
class RandomizedSet:
    """Packed list for random picks, map value -> index for lookups. O(1)."""

    def __init__(self):
        self.values = []            # packed from index 0, no holes
        self.index_of = {}          # value -> its slot in values

    def insert(self, val):
        """Append at the end and remember the slot. O(1)."""
        if val in self.index_of:
            return False
        self.index_of[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val):
        """Move the last value into val's slot, then pop the end. O(1)."""
        if val not in self.index_of:
            return False
        i = self.index_of[val]
        last = self.values[-1]
        self.values[i] = last       # the last value fills the hole
        self.index_of[last] = i     # and learns its new slot
        self.values.pop()           # drop the tail slot
        del self.index_of[val]      # only now: last may be val
        return True

    def get_random(self):
        """Pick a uniform random slot of the packed list. O(1)."""
        i = random.randint(0, len(self.values) - 1)
        return self.values[i]


# --- try it ---
s = RandomizedSet()
s.insert(10)
s.insert(20)
s.insert(30)
print(s.insert(20), s.remove(10), s.remove(10))   # -> False True False
print(s.values, s.index_of)                       # -> [30, 20] {20: 1, 30: 0}
print(s.get_random() in (20, 30))                 # -> True
print(s.remove(20), s.values, s.index_of)         # -> True [30] {30: 0}
