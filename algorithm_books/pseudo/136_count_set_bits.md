---
rank: 136
slug: count_set_bits
---

Count the 1 bits in the binary form of a non-negative integer, its popcount or Hamming weight. `44` is `101100` in binary, so the answer is `3`.

The obvious loop tests the last bit with `n & 1` (bitwise AND) and shifts right with `n >> 1`, once per bit position: 32 rounds for a 32-bit number, however few ones it holds. Brian Kernighan's trick loops once per set bit instead. Subtracting 1 from n turns its lowest 1 into 0 and every 0 below it into 1, and leaves the higher bits alone; AND-ing that with n keeps the higher bits and wipes the flipped block. So `n & (n - 1)` is n with its lowest set bit cleared, and the number of times it can be applied before n reaches 0 is the number of ones.

Two more facts fall out of the same picture. A power of two has exactly one set bit, so n is a power of two exactly when `n > 0` and `n & (n - 1) = 0`. And `n & -n` keeps only the lowest set bit, because in two's complement `-n` is `NOT n` plus 1, which matches n at that bit and below it and disagrees with n everywhere above. For the counts of every number from 0 to n (LC 338) a one-line recurrence beats running the loop n times: `i >> 1` is i with its last bit dropped, and its count is already known, so `bits[i] = bits[i >> 1] + (i & 1)`.

```text
     n       n - 1    n & (n - 1)   count
  101100    101011      101000        1      n = 44
  101000    100111      100000        2
  100000    011111      000000        3      n is 0: three set bits
n - 1 flips the lowest 1 and every 0 below it; the AND wipes that block

44 = ...00101100, -44 = ...11010100, 44 & -44 = 00000100 = 4

i               1   2   3   4   5
bits[i >> 1]    0   1   1   1   1
i & 1           1   0   1   0   1
bits[i]         1   1   2   1   2      bits for 0..5: [0, 1, 1, 2, 1, 2]
```

```pseudo
FUNCTION CountSetBits(n)
    count ← 0
    WHILE n > 0
        n ← n & (n - 1)                     // the lowest 1 becomes 0
        count ← count + 1
    RETURN count

FUNCTION IsPowerOfTwo(n)
    RETURN n > 0 AND (n & (n - 1)) = 0      // exactly one set bit

FUNCTION CountBitsUpTo(n)
    bits ← array of n + 1 zeros
    FOR i FROM 1 TO n
        bits[i] ← bits[i >> 1] + (i & 1)    // i >> 1 drops i's last bit
    RETURN bits
```

Kernighan's loop runs once per set bit, `O(k)` for k ones and never more than the number of bits, in `O(1)` space; the table for `0..n` takes `O(n)`, one step per number. Signals: popcount, Hamming weight, Hamming distance (LC 461 is the popcount of `x XOR y`), power-of-two tests, and the bitmask loops of #137. Python integers have no fixed width, so a negative number behaves as if it had infinitely many leading ones; when a problem means the 32-bit pattern of a negative number, mask it with `n & 0xFFFFFFFF` first. The classic mistake is dropping `n > 0` from the power-of-two test: `0 & (0 - 1)` is `0 & -1 = 0`, so the bare test calls 0 a power of two.

*Practice:* LC 191 Number of 1 Bits · LC 231 Power of Two · LC 338 Counting Bits · LC 461 Hamming Distance
