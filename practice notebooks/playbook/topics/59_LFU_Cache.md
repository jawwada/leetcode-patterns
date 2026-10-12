## LFU Cache

Evict the least frequently used key, breaking ties by recency. One ordered bucket per frequency preserves both parts of that rule.

<!-- cell -->

LFU Cache comes first because it is the follow-up to LRU: it changes one requirement, and the procedure absorbs it. `get` and `put` stay O(1), every `get` or `put` of a key counts as a use, and when the cache is full the key with the **fewest uses** is evicted, ties going to the least recently used among them. With capacity 2, `put(1, 1)`, `put(2, 2)`, `get(1)`, `put(3, 3)` evicts key 2, which has one use against key 1's two.

Run the method again. `freq_of`, key → count, is the truth; `bucket`, count → an `OrderedDict` of keys, oldest first, is the index that answers "who is the oldest among the rarest?"; one integer `min_freq` says which bucket that is.

The invariant: every key lives in exactly one bucket, `bucket[freq_of[key]]`, and `min_freq` is the smallest non-empty bucket whenever the cache is not empty. One integer can track the minimum because counts only ever go up by one.

The minimum changes in two cases: a brand-new key arrives and `min_freq` becomes 1, or the last key of the minimum bucket moves up and `min_freq` becomes `min_freq + 1`, exactly where that key went. An eviction can empty the lowest floor too, but it only happens right before a new key arrives, so the first case covers it.

```text
counts as floors, each floor a queue (oldest on the left):

freq 1: [2]        freq 2: [1, 3]        min_freq = 1
get(2):   2 climbs to floor 2; floor 1 is now empty and was the min   ->  min_freq = 2
freq 2: [1, 3, 2]                        min_freq = 2
put(4) when full: evict the oldest on the lowest floor (1), THEN 4 enters floor 1   ->  min_freq = 1
freq 1: [4]        freq 2: [3, 2]
```

The class below has two helpers. `_touch` moves a key one floor up and fixes `min_freq` if it emptied the lowest floor; `_evict` pops the oldest key of floor `min_freq`. `put` must evict *before* inserting, because the newcomer, alone on floor 1, would otherwise be its own victim. The prints replay the example, then a tie: keys 1 and 3 both have two uses when key 4 arrives, and the older one leaves.

<!-- cell -->

```python
class LFUCache:
    """get, put in O(1). When full, evict the least frequently used key; ties -> least recently used."""

    def __init__(self, capacity):
        self.cap = capacity
        self.freq_of = {}                            # STATE (truth): key -> use count
        self.bucket = defaultdict(OrderedDict)       # STATE (index): count -> {key: value}, oldest first
        self.min_freq = 0                            # STATE: the smallest non-empty count
        # INVARIANT: key lives only in bucket[freq_of[key]]; min_freq = smallest non-empty bucket

    def _touch(self, key):                           # contract: one more use of key; returns its value
        f = self.freq_of[key]
        value = self.bucket[f].pop(key)
        if not self.bucket[f]:
            del self.bucket[f]
            if self.min_freq == f:
                self.min_freq = f + 1                # the min floor emptied: key went to f + 1
        self.bucket[f + 1][key] = value              # STEP: newest on its new floor
        self.freq_of[key] = f + 1
        return value

    def _evict(self):                                # FIX: make room, the oldest of the rarest leaves
        victim, _ = self.bucket[self.min_freq].popitem(last=False)
        if not self.bucket[self.min_freq]:
            del self.bucket[self.min_freq]
        del self.freq_of[victim]

    def get(self, key):
        if key not in self.freq_of:
            return -1
        return self._touch(key)                      # RETURN

    def put(self, key, value):
        if self.cap == 0:                            # edge: nothing can ever be stored
            return
        if key in self.freq_of:
            self._touch(key)                         # an update is a use too
            self.bucket[self.freq_of[key]][key] = value
            return
        if len(self.freq_of) == self.cap:
            self._evict()                            # evict FIRST: the newcomer must not be the victim
        self.bucket[1][key] = value                  # STEP: a new key starts on floor 1
        self.freq_of[key] = 1
        self.min_freq = 1                            # RECORD: a new key always has the smallest count


lfu = LFUCache(2)
lfu.put(1, 1)
lfu.put(2, 2)
print(lfu.get(1))                                # 1    (now key 1 has 2 uses, key 2 has 1)
lfu.put(3, 3)                                    # evicts 2, the key with the fewest uses
print(lfu.get(2), lfu.get(3))                    # -1 3
lfu.put(4, 4)                                    # 1 and 3 both have 2 uses; 1 is older -> evicted
print(lfu.get(1), lfu.get(3), lfu.get(4))        # -1 3 4
```

<!-- cell -->

**Try it**
- Insert before evicting: move the eviction below the three insert lines (as `if len(self.freq_of) > self.cap: self._evict()`) and rerun. The last line prints `1 3 -1` instead of `-1 3 4`: the newcomer 4 sat alone on floor 1, so it was evicted instead of key 1.
- Delete `self.min_freq = 1` at the end of `put` and rerun: `KeyError: 'dictionary is empty'` at the first eviction. `min_freq` was still 0, a floor with no keys.
- Delete the two capacity-0 lines at the top of `put` and run `LFUCache(0).put(1, 1)`: `KeyError` again, because the eviction looks for a victim in an empty cache.
- Add `print({f: list(b) for f, b in lfu.bucket.items()}, lfu.min_freq)` after every call and watch keys climb one floor per use.
