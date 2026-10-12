"""
Hash Map with Open Addressing - Linear Probing and Tombstones

Design a hash map without a built-in dict that stores every pair in one array
of slots: put(key, value), get(key) (-1 if missing) and remove(key). With 8
slots, keys 3 and 11 both start at slot 3, so 11 moves on to slot 4:
put(3, 30), put(11, 110), get(11) -> 110.
"""


# --- algorithm ---
EMPTY = None                # never used: a search can stop here
DELETED = "DELETED"         # tombstone: used once, a search must go on


class ProbingHashMap:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0                       # live keys
        self.tombstones = 0                 # DELETED slots
        self.slots = [EMPTY] * capacity     # EMPTY, DELETED or [key, value]

    def find(self, key):
        """Index of key's slot or -1: probe until the key or an EMPTY slot.
        Expected O(1)."""
        index = hash(key) % self.capacity
        while self.slots[index] is not EMPTY:
            slot = self.slots[index]
            if slot != DELETED and slot[0] == key:
                return index
            index = (index + 1) % self.capacity     # taken: try the next slot
        return -1

    def put(self, key, value):
        """Overwrite if present, else fill the first free slot on the path.
        Expected O(1), amortized over the resizes."""
        index = self.find(key)
        if index != -1:
            self.slots[index][1] = value            # already stored: overwrite
            return
        index = hash(key) % self.capacity
        while self.slots[index] is not EMPTY and self.slots[index] != DELETED:
            index = (index + 1) % self.capacity     # skip live pairs
        if self.slots[index] == DELETED:
            self.tombstones -= 1                    # reuse the tombstone
        self.slots[index] = [key, value]
        self.size += 1
        if (self.size + self.tombstones) / self.capacity > 0.5:
            self.resize()

    def get(self, key):
        """Value of key or -1. Expected O(1) while the table is half empty."""
        index = self.find(key)
        if index == -1:
            return -1
        return self.slots[index][1]

    def remove(self, key):
        """Leave a tombstone so that searches step over it. Expected O(1)."""
        index = self.find(key)
        if index != -1:
            self.slots[index] = DELETED
            self.size -= 1
            self.tombstones += 1

    def resize(self):
        """Double the array and re-put the live pairs only. O(n)."""
        old_slots = self.slots
        self.capacity = 2 * self.capacity
        self.slots = [EMPTY] * self.capacity
        self.size = 0
        self.tombstones = 0
        for slot in old_slots:
            if slot is not EMPTY and slot != DELETED:
                self.put(slot[0], slot[1])          # tombstones are dropped


# --- try it ---
table = ProbingHashMap()
table.put(3, 30)
table.put(11, 110)                  # home slot 3 is taken: lands in slot 4
table.put(19, 190)                  # slots 3 and 4 are taken: slot 5
table.put(4, 40)                    # home slot 4 is inside the run: slot 6
table.remove(11)                    # slot 4 becomes a tombstone
print(table.get(19), table.get(11), table.tombstones)   # -> 190 -1 1
table.put(27, 270)                  # reuses the tombstone in slot 4
print(table.slots[4], table.tombstones)                 # -> [27, 270] 0
table.put(12, 120)                  # 5 of 8 slots used: grow to 16
print(table.capacity, table.size, table.get(12))        # -> 16 5 120
