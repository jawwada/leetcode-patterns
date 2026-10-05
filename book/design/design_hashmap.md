# Design HashMap

*LeetCode 706 · Easy · Pattern: Separate chaining with load-factor resizing · Reading time ~6 min*

## The problem

Implement MyHashMap without built-in hash tables: put(key, value), get(key) -> value or -1, remove(key). Keys and
values are non-negative integers up to 10^6.

```text
Example: put(1,1), put(2,2), get(1) -> 1, get(3) -> -1,
  put(2,1), get(2) -> 1, remove(2), get(2) -> -1.
```

## What the problem is really asking

Build `put(key, value)`, `get(key)` (returning -1 if absent) and `remove(key)` without using a built-in dict. Keys and values are non-negative integers. Every tracker so far leaned on a hash map; this problem makes you build one, so that "O(1) average" stops being a phrase and becomes something you can defend.

The hard part is not correctness — a list of pairs is correct — but finding a key without looking at the others.

```text
 put(1,10) put(9,90) put(2,20)
 get(9) -> 90      get(3) -> -1
```

## Do it by hand first

Picture a mailroom with 8 pigeonholes numbered 0–7. A clerk files each letter by the last digit of its key in base 8: key mod 8. Key 1 goes in hole 1, key 9 also in hole 1 (9 mod 8 = 1), key 2 in hole 2. To find key 9, the clerk goes straight to hole 1 and flips through the two letters there.

```text
 hole:  0    1           2      3..7
       [ ]  [1,10]      [2,20]  [ ]
            [9,90]
```

What the clerk's hand tracked was an *address computed from the key*, plus a short pile per address for keys that collide.

## The first honest attempt

One list of [key, value] pairs. `put` scans for the key and updates or appends; `get` scans; `remove` scans and deletes. Each is O(n).

```text
 pairs: [1,10] [9,90] [17,5] [2,20] [3,3] ... [16,16]
 get(16): compare with 1? 9? 17? 2? 3? ... 16. yes
          ^ n comparisons, n-1 of them hopeless
```

The waste: comparing the target against every stored key, when the key itself could have told us where to look.

## The turning point

**Claim: if each key is sent to one of B buckets by `key mod B`, a lookup only needs to scan keys that share its bucket, and keeping n/B bounded keeps that scan O(1) on average.**

Justification: two equal keys always compute the same bucket, so a key is either in its bucket or nowhere. With reasonably spread keys, the n keys divide into B piles of about n/B each.

The structure: an array of B lists ("separate chaining"). Collisions just extend the list. The catch is growth: with B fixed, n/B grows with n and we are back to O(n). So keep the *load factor* n/B below a threshold — this solution uses 2 — by doubling B and re-inserting every pair when it is exceeded. Re-inserting is required because each key's address `key mod B` changes when B changes.

A doubling costs O(n), but it only happens after the number of keys has doubled since the last one. Spread over those inserts, each insert pays O(1) extra: amortised O(1).

## Watch it work

Start with B = 8. Only non-empty buckets are drawn.

```text
Frame 1  put(1,10) put(9,90) put(17,5)
 B=8 size=3
 [1]: [1,10] -> [9,90] -> [17,5]
```
1, 9 and 17 all have remainder 1 mod 8, so they chain in bucket 1.

```text
Frame 2  put(2,20); get(9) -> 90
 B=8 size=4
 [1]: [1,10] -> [9,90] -> [17,5]
 [2]: [2,20]
 get(9): go to bucket 1, scan 2 pairs
```
The lookup never looks at bucket 2.

```text
Frame 3  put(9,99)
 [1]: [1,10] -> [9,99] -> [17,5]     size=4
```
The key exists in its bucket, so the value is overwritten in place; size is unchanged.

```text
Frame 4  put k,k for k = 3..15 except 9
 B=8 size=16      (16 > 2*8? no)
 [0]: [8]   [1]: [1] [9] [17]   [2]: [2] [10]
 [3]: [3] [11]  ...  [7]: [7] [15]
```
Every bucket now holds about two pairs: load factor exactly 2.

```text
Frame 5  put(16,16) -> size 17 > 16: resize
 B=16  every pair re-addressed by key mod 16
 [0]: [16]   [1]: [1,10] -> [17,5]   [2]: [2,20]
 ... [9]: [9,99] ... [15]: [15]
```
Bucket 1's chain splits: 9 moves to bucket 9 because 9 mod 16 = 9.

```text
Frame 6  remove(1); get(1) -> -1; get(17) -> 5
 B=16 size=16
 [1]: [17,5]
```
Removal scans only bucket 1 and pops one pair.

Throughout, every key lives in bucket `key mod B` for the current B, and `size` equals the number of pairs stored.

## Why it is correct

Invariant: each stored key appears exactly once, in bucket `key mod B`. `put` searches only that bucket; if the key is there it updates, so there is never a duplicate; otherwise it appends there. `get` and `remove` search the only bucket the key could occupy. A resize rebuilds every pair at its new address, so the invariant holds for the new B. Because each operation looks in the one bucket that can contain the key, an absent key is correctly reported as -1.

## Cost

- **Time:** O(1) average per operation — chains have about n/B ≤ 2 pairs; O(n) for the occasional resize, O(1) amortised.
- **Space:** O(n + B) — the pairs plus the bucket array, and B never drops below n/2.

Worst case, adversarial keys all landing in one bucket make everything O(n) — the honest caveat.

## Variations you will meet

- **Open addressing.** No chains: on collision, probe the next slot (linear probing). Deletion needs tombstones so later probes do not stop early. Python's own dict works this way.
- **Fixed key range (≤ 10^6).** A direct array of 10^6 + 1 slots with -1 for empty is O(1) worst case. Mention it, then say why it does not generalise.
- **Design HashSet.** Same buckets, no values.
- **Shrinking.** If many removes leave the table sparse, halve B when the load factor drops below 1/8 to reclaim memory.

## What to carry forward

A hash map is "compute where it lives, then look at a few things there", kept fast by resizing before the piles grow. The next problem pairs this map with an array so that a uniformly random element is also O(1).
