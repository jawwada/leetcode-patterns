"""
Consistent Hashing - A Hash Ring with Virtual Nodes

Place keys on servers so that adding or removing a server moves few keys:
servers and keys hash to points on a ring, and a key belongs to the first
server point clockwise from it. 1000 keys, a 4th server joins 3 -> 235 keys
move, all to the new server (hash mod n would move 738).
"""


# --- algorithm ---
RING = 2 ** 32                          # ring positions are 0 .. 2^32 - 1


def ring_hash(text):
    """FNV-1a, then MurmurHash3's finalizer: a 32-bit position that is the
    same in every run (Python's hash() of a string is not). O(len(text))."""
    h = 2166136261                      # FNV-1a offset basis
    for ch in text:
        h = h ^ ord(ch)
        h = (h * 16777619) % RING       # FNV prime, keep 32 bits
    h = h ^ (h >> 16)                   # avalanche: names one letter apart
    h = (h * 2246822507) % RING         # end up far apart on the ring
    h = h ^ (h >> 13)
    h = (h * 3266489909) % RING
    h = h ^ (h >> 16)
    return h


class HashRing:
    """Sorted (position, server) points, several per server; a key belongs
    to the first point clockwise from its hash. Lookup O(log(n * v))."""

    def __init__(self, replicas):
        self.replicas = replicas        # virtual nodes per server
        self.points = []                # (position, server), sorted

    def lower_bound(self, position):
        """First index whose point is at or after position. O(log(n * v))."""
        lo = 0
        hi = len(self.points)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.points[mid][0] < position:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def add_server(self, server):
        """Insert v points, keeping the list sorted. O(v * n * v): each
        insert shifts the list."""
        for i in range(self.replicas):
            position = ring_hash(server + "#" + str(i))
            index = self.lower_bound(position)
            self.points.insert(index, (position, server))

    def remove_server(self, server):
        """Drop every point of the server; its arcs pass clockwise. O(n * v)."""
        kept = []
        for point in self.points:
            if point[1] != server:
                kept.append(point)
        self.points = kept

    def get_server(self, key):
        """The first point clockwise from the key's hash. O(log(n * v))."""
        if len(self.points) == 0:
            return None
        index = self.lower_bound(ring_hash(key))
        if index == len(self.points):
            index = 0                   # past the last point: wrap to the first
        return self.points[index][1]


def ring_owners(ring, keys):
    """The server of every key on the ring, in key order. O(k log(n * v))."""
    owners = []
    for key in keys:
        owners.append(ring.get_server(key))
    return owners


def mod_n_owners(keys, servers):
    """The naive placement to compare: server number hash mod n. O(k)."""
    owners = []
    for key in keys:
        owners.append(servers[ring_hash(key) % len(servers)])
    return owners


def count_moved(before, after):
    """How many keys changed server between two placements. O(k)."""
    moved = 0
    for i in range(len(before)):
        if before[i] != after[i]:
            moved += 1
    return moved


# --- try it ---
keys = []
for i in range(1000):
    keys.append("key" + str(i))
ring = HashRing(100)
ring.add_server("A")
ring.add_server("B")
ring.add_server("C")
before = ring_owners(ring, keys)
ring.add_server("D")
after = ring_owners(ring, keys)
print(count_moved(before, after), after.count("D"))    # -> 235 235
old_mod = mod_n_owners(keys, ["A", "B", "C"])
new_mod = mod_n_owners(keys, ["A", "B", "C", "D"])
print(count_moved(old_mod, new_mod))                   # -> 738
ring.remove_server("D")
print(ring_owners(ring, keys) == before)               # -> True
print(len(ring.points), ring.get_server("key7"))       # -> 300 A
print(HashRing(3).get_server("key7"))                  # -> None
