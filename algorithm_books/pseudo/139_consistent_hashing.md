---
rank: 139
slug: consistent_hashing
---

A cache or storage cluster spreads keys over servers, and servers come and go. Every client must be able to compute a key's server from the key and the server list alone, and a change to the list should move as few keys as possible, because every moved key is a cache miss or a copy across the network. With 1000 keys on servers A, B and C, a fourth server D should take about a quarter of the keys, the share it will own, and nothing else should move.

The obvious placement, server number `hash(key) mod n`, fails that test badly. When `n` grows to `n + 1` a key stays put only if its hash leaves the same remainder for both, which happens for one hash in `n + 1`, so going from three servers to four moves three keys in four. Consistent hashing puts servers and keys on one circle of `2^32` positions. Each server owns points on the circle, and a key belongs to the first server point clockwise from its own position, wrapping from the top back to 0, so every point owns the arc that ends at it. A new point lands inside some arc and takes over the stretch from the previous point up to itself: the only keys that move are the ones in those stretches, and all of them move to the new server. A removed server's arcs merge into the next points clockwise, and no other key notices.

One point per server leaves the arcs badly uneven: with a single point each, the same hash splits the circle 25, 15 and 60 percent between A, B and C, and D would join with 5. Virtual nodes fix it. Each server hashes `name#0`, `name#1`, … to `v` points, so its share is a sum of `v` small arcs that evens out, and a newcomer takes a little from every server instead of a lot from one neighbor; with 100 points each the shares are 36, 32 and 32 percent. The ring is a sorted list of `(position, server)` pairs, and a lookup is the lower bound of #14 on the positions, where running off the end wraps to index 0. The hash must agree across processes, which rules out Python's `hash()` of a string, salted per run, and FNV-1a alone sends names that differ only in their last character, like `A#1` and `A#2`, to nearby points, so a finalizer scrambles its bits.

```text
2 virtual nodes per server; positions as a percent of the ring, 100 = 0
sorted points:  B 3.9   C 14.5   B 29.7   A 35.2   A 54.8   C 89.9
0 ───B──────C──────────B───A─────────────A─────────────────────────C─────── 100
each point owns the arc that ends at it: C 89.9 owns (54.8, 89.9]
key2 at 6.6:  the first point at or after it is C 14.5        → server C
key1 at 97.7: past the last point, wrap to index 0, B 3.9     → server B

D joins with points at 59.9 and 97.6
0 ───B──────C──────────B───A─────────────A───D─────────────────────C────D── 100
D takes (54.8, 59.9] from C and (89.9, 97.6] from B: 121 of 1000 keys move,
every one of them to D, and no other key changes server
100 virtual nodes each: 235 keys move, all to D; hash mod n moves 738
```

```pseudo
FUNCTION RingHash(text)                 // FNV-1a, then MurmurHash3's finalizer
    h ← 2166136261                      // FNV-1a offset basis
    FOR EACH ch IN text
        h ← h XOR code(ch)
        h ← (h * 16777619) mod RING     // FNV prime; RING = 2^32
    h ← h XOR (h >> 16)                 // avalanche: names one letter apart
    h ← (h * 2246822507) mod RING       // end up far apart on the ring
    h ← h XOR (h >> 13)
    h ← (h * 3266489909) mod RING
    h ← h XOR (h >> 16)
    RETURN h

CLASS HashRing
    FUNCTION Init(replicas)
        self.replicas ← replicas        // virtual nodes per server
        self.points ← empty list        // (position, server), sorted

    FUNCTION LowerBound(position)       // first point at or after position
        lo ← 0
        hi ← len(self.points)
        WHILE lo < hi
            mid ← floor((lo + hi) / 2)
            IF self.points[mid][0] < position
                lo ← mid + 1
            ELSE
                hi ← mid
        RETURN lo

    FUNCTION AddServer(server)
        FOR i FROM 0 TO self.replicas - 1
            position ← RingHash(server + "#" + str(i))
            index ← self.LowerBound(position)
            self.points.insert(index, (position, server))   // stays sorted

    FUNCTION RemoveServer(server)       // its arcs pass to the next points
        kept ← empty list
        FOR EACH point IN self.points
            IF point[1] ≠ server
                kept.append(point)
        self.points ← kept

    FUNCTION GetServer(key)
        IF len(self.points) = 0
            RETURN null
        index ← self.LowerBound(RingHash(key))
        IF index = len(self.points)
            index ← 0                   // past the last point: wrap around
        RETURN self.points[index][1]
```

A lookup hashes the key and binary searches the `n × v` points, `O(log(n × v))`. Adding a server costs `O(v × n × v)` here because each insert shifts the list, `O(v log(n × v))` with a balanced search tree, and the ring holds `O(n × v)` points. The signals are distributed caches, sharded storage, sticky load balancing and any design in which servers join and leave: Amazon's Dynamo, Cassandra and the ketama scheme of memcached clients all place each server on a ring at many points. A server with twice the capacity gets twice the virtual nodes, and replication walks clockwise to the next distinct servers to place the copies. Rendezvous hashing is the ring-free alternative: score every server against the key and take the highest, `O(n)` per lookup. No LeetCode problem asks for a ring; the practice problems drill the hashing underneath. The classic mistakes are forgetting the wrap-around, which misroutes or crashes every key past the last point, and a hash that differs between processes, like Python's `hash()`, or one that clusters, like a base-31 polynomial hash, which puts `A#0` to `A#9` at ten consecutive positions and piles a server's virtual nodes into one spot.

*Practice:* LC 706 Design HashMap · LC 705 Design HashSet · LC 535 Encode and Decode TinyURL
