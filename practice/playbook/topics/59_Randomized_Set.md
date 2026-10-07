## Insert, Delete, and GetRandom

A dense array supports uniform random choice; a dictionary maps each value to its array index. Deletion swaps the final element into the removed slot so nothing shifts.

<!-- cell -->

Insert Delete GetRandom O(1) comes next because it is the same truth-and-index recipe with a new question, a uniform random pick. `insert(v)` and `remove(v)` return whether anything changed, and `getRandom()` returns a uniformly random stored value, each in O(1) on average: `insert(5)`, `insert(8)`, `insert(2)`, `remove(5)` leaves 8 and 2, and `getRandom()` is one of them.

A dense list answers `getRandom`, since `random.choice` needs no holes, and a dict from value to its index answers membership and says where a value sits. A delete moves the last value into the hole, so the list stays dense and nothing shifts. The invariant is `vals[pos[v]] == v` for every stored v, and the last print removes the only element, which is also the last one.

<!-- cell -->

```python
class RandomizedSet:
    def __init__(self):
        self.vals = []                           # STATE (index): dense list, so random.choice is uniform
        self.pos = {}                            # STATE (truth): value -> its index in vals
        # INVARIANT: vals[pos[v]] == v for every stored v

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)           # STEP
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i, last = self.pos[val], self.vals[-1]
        self.vals[i], self.pos[last] = last, i   # STEP: move the last value into the hole
        self.vals.pop()
        del self.pos[val]                        # AFTER the move: works even when val is the last one
        return True

    def getRandom(self):
        return random.choice(self.vals)          # RETURN


random.seed(0)
rs = RandomizedSet()
print(rs.insert(5), rs.insert(8), rs.insert(2), rs.remove(5), rs.vals, rs.pos)   # True True True True [2, 8] {8: 1, 2: 0}
print(sorted({rs.getRandom() for _ in range(50)}))                              # [2, 8]
one = RandomizedSet()
print(one.insert(7), one.remove(7), one.vals, one.pos)                          # True True [] {}
```

<!-- cell -->

**Try it**
- Move `del self.pos[val]` up, before the line that fills the hole, then remove the only element: `r = RandomizedSet(); r.insert(1); r.remove(1)`. Now `r.pos` is `{1: 0}`, a ghost entry, and `r.insert(1)` returns `False`.
- `Counter(rs.getRandom() for _ in range(3000))`: each of the two values comes up about 1,500 times.
- Delete the line `del self.pos[val]` and rerun: `rs.pos` still lists 5, so `rs.insert(5)` returns `False` although `getRandom` can never return 5. The index (`vals`) and the truth (`pos`) disagree.
