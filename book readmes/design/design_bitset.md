# Design Bitset
*LeetCode 2166 · Medium · Pattern: Lazy global flip flag + maintained count · Reading time ~8 min*

## The problem

Implement Bitset(size) with all bits 0: fix(idx) sets a bit to 1, unfix(idx) sets it to 0, flip() inverts every bit,
all() / one() report whether all / at least one bit is 1, count() returns the number of 1s and toString() returns the
bits as a string. Everything except toString should be O(1).

```text
Example: Bitset(5); fix(3); fix(1); flip() -> '10101'; unfix(0)
  -> '00101'; flip() -> '11010'; unfix(0) -> '01010'; count() ->
  2.
```

## What the problem is really asking

Build a row of `size` bits, all zero, supporting:

- `fix(i)`: make bit i a 1. `unfix(i)`: make bit i a 0.
- `flip()`: invert every bit.
- `all()`, `one()`, `count()`: are all bits 1, is any bit 1, how many are 1.
- `toString()`: the bits as a string.

Everything except `toString` must be O(1). The output of each query is tiny (a bool or a number), but `flip` changes *every* bit, and `all`/`one`/`count` look like they need to see every bit. Up to 100,000 bits and 100,000 calls make O(size) per call too slow.

```text
  Bitset(5): fix(3), fix(1), flip()

  before flip:  0 1 0 1 0     count = 2
  after flip:   1 0 1 0 1     count = 3
                ^ every bit changed, yet count went 2 -> 3
                  without looking at any bit: 5 - 2 = 3
```

## Do it by hand first

Write the five bits on a strip of paper. When asked to flip, you could rewrite all five digits. But a lazier person would just turn the strip over to a side where every 0 is read as 1 and every 1 as 0. Put differently, you keep the digits and change your *glasses*.

```text
  paper:    0 1 0 1 0        glasses: normal
  read as:  0 1 0 1 0

  paper:    0 1 0 1 0        glasses: inverted (after flip)
  read as:  1 0 1 0 1
```

And you keep a running tally in the margin: "ones = 2". When you flip, the tally becomes "5 - 2 = 3". When you fix a bit that was read as 0, the tally goes up by one.

Your hand kept track of three things: the physical digits, which glasses you are wearing, and a tally. Those are the three fields of the data structure.

## The first honest attempt

A plain list of bits. `fix` and `unfix` write one cell, O(1). `flip` rewrites every cell, O(size). `count` sums the list, `all` and `one` scan it, each O(size).

Where is the waste? Two places.

```text
  flip(); flip(); flip(); flip()

  pass 1:  0 1 0 1 0  ->  1 0 1 0 1   5 writes
  pass 2:  1 0 1 0 1  ->  0 1 0 1 0   5 writes, undoing pass 1
  pass 3:  0 1 0 1 0  ->  1 0 1 0 1   5 writes
  pass 4:  1 0 1 0 1  ->  0 1 0 1 0   5 writes, undoing pass 3

  20 writes to end exactly where we started
```

First, consecutive flips cancel, so eager rewriting is pure motion. Second, `count` re-sums bits that we already knew the total of a moment ago; only one bit (or a full flip, with a predictable effect) changed since.

## The turning point

**Claim: a flip never needs to touch a bit, and the number of ones never needs to be recomputed; both can be maintained in O(1) per operation.**

Two independent observations do the work.

*The lens.* Keep a flag `flipped` (0 or 1). Define the *logical* bit, the one the user sees, as `physical[i] XOR flipped`. Then `flip()` just toggles the flag: every logical bit inverts at once because every bit is read through the same lens. No physical bit moves.

*The tally.* Keep `ones`, the number of logical ones. A flip turns every 1 into 0 and every 0 into 1, so the new count is `size - ones`. A `fix(i)` adds one if and only if bit i was logically 0; an `unfix(i)` subtracts one if and only if it was logically 1. With the tally maintained, `count` returns it, `all` checks `ones == size`, and `one` checks `ones > 0`.

The only subtle operation is `fix`/`unfix` while the lens is inverted. You cannot write a literal 1 into the physical array, because it would be read as 0. The rule is: read the logical bit; if it already has the desired value, do nothing (and do not touch the tally); otherwise XOR the physical bit, which flips its logical value under any lens, and adjust the tally.

```text
  flipped = 1,  want logical bit 0 to become 0 (unfix)

  physical:  0      logical = 0 ^ 1 = 1   (needs change)
  physical ^= 1  -> 1   logical = 1 ^ 1 = 0   done, ones -= 1
```

`toString` is the only place that walks the array, applying the lens to every bit, and the problem allows it to be O(size).

## Watch it work

Operations on `Bitset(5)`: `fix(3)`, `fix(1)`, `flip()`, `unfix(0)`, `flip()`, `unfix(0)`.

Frame 1 — after `fix(3)` and `fix(1)`.

```text
  physical: 0 1 0 1 0     flipped = 0   ones = 2
  logical:  0 1 0 1 0
```

Both bits were logically 0, so each was XORed and the tally rose twice.

Frame 2 — `flip()`.

```text
  physical: 0 1 0 1 0     flipped = 1   ones = 5-2 = 3
  logical:  1 0 1 0 1
```

No physical bit changed; the flag flipped and the tally became `size - ones`.

Frame 3 — `unfix(0)`.

```text
  physical: 1 1 0 1 0     flipped = 1   ones = 2
            ^ XORed
  logical:  0 0 1 0 1
```

Logical bit 0 was 1, so the physical bit 0 went 0 -> 1, which reads as 0 under the inverted lens.

Frame 4 — `flip()`.

```text
  physical: 1 1 0 1 0     flipped = 0   ones = 5-2 = 3
  logical:  1 1 0 1 0
```

The lens is back to normal; physical and logical agree again, and the tally is still exact.

Frame 5 — `unfix(0)`, then `count()` returns 2.

```text
  physical: 0 1 0 1 0     flipped = 0   ones = 2
            ^ XORed
  logical:  0 1 0 1 0     toString() = "01010"
```

Logical bit 0 was 1, so it was cleared and the tally dropped to 2.

In every frame, `ones` equalled the number of 1s in the logical row, and the logical row was always `physical XOR flipped`.

## Why it is correct

Invariant: (a) the user-visible bit i equals `bits[i] ^ flipped`; (b) `ones` equals the number of i whose visible bit is 1.

Initially all bits and the flag are 0 and `ones = 0`, so both hold.

- `flip` toggles the flag, so by (a) every visible bit inverts, which is what flip means. The visible ones become the old visible zeros, of which there were `size - ones`; so (b) holds after `ones = size - ones`.
- `fix(i)` reads the visible bit. If it is 1 nothing changes, correctly. If it is 0, toggling `bits[i]` toggles the visible bit (XOR with a fixed flag is a bijection), making it 1, and exactly one visible 1 is added, so `ones += 1` keeps (b). `unfix` is symmetric.
- Queries read `ones` and `size`, which by (b) answer `count`, `all` and `one` directly. `toString` applies (a) to every bit.

## Cost

- Time: O(1) for `fix`, `unfix`, `flip`, `all`, `one`, `count`; O(size) for `toString`, which must output size characters anyway.
- Space: O(size) for the physical bits, plus one flag and one integer.

## Variations you will meet

- **Range flip `flip(l, r)`.** A single global flag no longer suffices; the lens must vary by position. A segment tree with a lazy "flipped" tag per node and a ones-count per node gives O(log n) per range flip and count.
- **Packed bits.** Store bits in 64-bit words (or one Python int) to cut memory 64x; `count` still uses the maintained tally, and the lens is unchanged.
- **Lazy add on an array (`addAll(x)`, `multAll(m)`).** The Fancy Sequence problem generalises the lens to a global affine map `a*v + b`; values written later must be stored through the inverse map, just as `fix` writes through the XOR.
- **Snapshot Array (previous problem).** Also avoids touching untouched cells, but by remembering history rather than by reinterpretation.

## What to carry forward

When an operation changes everything uniformly, change how you *read* the data instead of the data itself, and keep aggregate answers as counters updated by each small change. The next problem, LRU Cache, needs a different kind of O(1) bookkeeping: not a count, but an order of recency that must be updated on every access.
