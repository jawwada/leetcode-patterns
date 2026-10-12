---
rank: 146
slug: bloom_filter
---

A Bloom filter remembers a set without storing its items. `add(item)` records an item, and `might_contain(item)` answers false, which is always right, or true, which is wrong only for a small, tunable share of items that were never added. With 19 bits and 3 hash functions, after adding `cat`, `dog` and `fish`, `might_contain("cat")` is true, `might_contain("owl")` is false, and `might_contain("colt")` is true although `colt` was never added.

A hash set answers exactly but stores every item in full, too much for a billion URLs. When a wrong yes costs only a wasted lookup, a Bloom filter makes do with about 10 bits per item, however large the items. It is an array of m bits, all 0, and k hash functions, each sending an item to one bit. `add` sets the item's k bits to 1 and `might_contain` reads them. A single 0 proves the item was never added, since adding it would have set that bit and bits are never cleared: there are no false negatives. All k bits at 1 only says probably, because other items may have set them.

Two hashes are enough for all k probes, as Kirsch and Mitzenmacher showed: probe i lands on bit `(h1 + i × step) mod m`, with h1 and h2 polynomial string hashes as in Rabin-Karp (#120), bases 31 and 37. The step `1 + h2 mod (m - 1)` is never 0, so with m prime the k probes hit k different bits. Python's `hash()` would be a mistake: it is salted afresh in every process, so a filter saved by one run would be probed at the wrong bits by the next. Picture the array as a strip of lights. Each add switches on k of them, and a query asks whether all k of its own are on. After n adds a bit is still off with probability about `e^(-kn/m)`, so the false-positive rate is about `(1 - e^(-kn/m))^k`. The best `k = (m / n) ln 2` leaves half the lights on, and 10 bits per item with 7 hashes give 0.82 percent.

```text
m = 19 bits, k = 3; probe i sets bit (h1 + i·step) mod 19, step = 1 + h2 mod 18
add "cat"     h1 mod 19 = 13, step  7   →   bits 13,  1,  8
add "dog"     h1 mod 19 =  8, step  9   →   bits  8, 17,  7    shares bit 8
add "fish"    h1 mod 19 = 10, step 13   →   bits 10,  4, 17    shares bit 17

  bit   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18
        0  1  0  0  1  0  0  1  1  0  1  0  0  1  0  0  0  1  0   7 of 19 set

might_contain("cat")    bits 13, 1, 8    read 1 1 1   → true, it was added
might_contain("owl")    bits 2, 17, 13   read 0 1 1   → false: bit 2 is 0
might_contain("colt")   bits 7, 10, 13   read 1 1 1   → true, a false positive:
                        dog set bit 7, fish bit 10 and cat bit 13
```

```pseudo
MOD ← 1000000007                          // a large prime, as in Rabin-Karp

FUNCTION StringHash(word, base)
    h ← 0
    FOR EACH ch IN word
        h ← (h * base + code(ch)) mod MOD
    RETURN h

CLASS BloomFilter
    FUNCTION Init(m, k)
        self.m ← m                        // number of bits, best a prime
        self.k ← k                        // number of hash functions
        self.bits ← array of m zeros

    FUNCTION Positions(item)
        h1 ← StringHash(item, 31)
        h2 ← StringHash(item, 37)         // a second, different hash
        step ← 1 + h2 mod (self.m - 1)    // 1..m-1: the probes always move
        result ← empty list
        FOR i FROM 0 TO self.k - 1
            result.append((h1 + i * step) mod self.m)
        RETURN result

    FUNCTION Add(item)
        FOR EACH p IN self.Positions(item)
            self.bits[p] ← 1

    FUNCTION MightContain(item)
        FOR EACH p IN self.Positions(item)
            IF self.bits[p] = 0
                RETURN false              // adding it would have set this bit
        RETURN true                       // added, or a false positive
```

Each operation costs `O(L)` to hash an item of length L plus `O(k)` bit operations, and the filter stays m bits however many items arrive; a target rate p needs `m = -n ln p / (ln 2)²` bits, about 9.6 per item for 1 percent. The signals are a huge set, a membership check in front of an expensive lookup, and tolerance for a rare false yes: LSM-tree stores such as Bigtable, Cassandra and RocksDB keep a filter per file on disk and skip every file whose filter says no. Guava builds h1 and h2 from the two halves of one 128-bit MurmurHash3, a far stronger hash than these. Bits are shared, so a filter cannot delete; a counting Bloom filter keeps a small counter per position instead. The classic mistake is deleting anyway: clearing the bits of `cat` turns off bit 8, and `dog`, which was added, starts coming back false.

*Practice:* LC 705 Design HashSet · LC 187 Repeated DNA Sequences
