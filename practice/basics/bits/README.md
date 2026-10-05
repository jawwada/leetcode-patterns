# Bit manipulation

An integer is a row of bits, and a handful of two-operand tricks lets you read, write and count them in constant time. Every trick starts from a mask: `1 << i` is a lone 1 at position i (counted from the right, 0-based), `n - 1` flips the lowest set bit and everything below it, `-n` is `~n + 1`. Python integers have no fixed width and negative numbers behave as if they had infinitely many leading 1s, so 32-bit problems need an explicit `& 0xFFFFFFFF`.

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| `n >> i & 1` read bit i | O(1) | shift the bit down to position 0, then keep only it |
| `n \| (1 << i)` set bit i | O(1) | OR forces a 1, the other bits are untouched |
| `n & ~(1 << i)` clear bit i | O(1) | AND with the complement forces a 0 |
| `n ^ (1 << i)` toggle bit i | O(1) | XOR flips |
| `n & (n - 1)` drop the lowest set bit | O(1) | Kernighan's count loops once per set bit |
| `n & -n` isolate the lowest set bit | O(1) | 0 for n = 0 |
| `n > 0 and n & (n - 1) == 0` power of two | O(1) | the `n > 0` guards against 0 (and negatives) |
| `acc ^= x` over a list | O(n) | pairs cancel: `x ^ x == 0`, `x ^ 0 == x`, order does not matter |
| masks `0 .. (1 << n) - 1` | O(2^n) subsets | bit i set means item i is in |
| `sub = (sub - 1) & mask` | O(2^k) for k set bits | walks every submask of `mask` from `mask` down to 0 |
| `(n & 0xFFFFFFFF) >> k` | O(1) | logical right shift of a 32-bit word; plain `>>` is arithmetic |

## Drawn example: n = 180 = 10110100

```
n          1 0 1 1 0 1 0 0          set bits: 4
n - 1      1 0 1 1 0 0 1 1          the lowest 1 became 0, the zeros below it became 1s
n & (n-1)  1 0 1 1 0 0 0 0          exactly the lowest set bit is gone      (count: 1 of 4)

-n         0 1 0 0 1 1 0 0          ~n + 1: everything above the lowest 1 is flipped
n & -n     0 0 0 0 0 1 0 0          only the lowest set bit survives = 4

1 << 3     0 0 0 0 1 0 0 0          the mask for position 3
n | mask   1 0 1 1 1 1 0 0          set     n & ~mask  1 0 1 1 0 1 0 0   clear (already 0)
n ^ mask   1 0 1 1 1 1 0 0          toggle  n >> 3 & 1 = 0                read
```

## Shifts: arithmetic versus logical

`x << k` multiplies by 2^k. `x >> k` divides by 2^k and **floors**: `41 >> 3 == 5`, `-7 >> 1 == -4`. Python's `>>` is an *arithmetic* shift: the sign bit is copied in from the left, so a negative number stays negative forever (`-1 >> 100 == -1`). A *logical* shift brings in zeros instead; languages with fixed-width unsigned types do it by default (`>>>` in Java/JavaScript). In Python you get it by fixing the width first: `(n & 0xFFFFFFFF) >> k`. The same mask turns a negative into its 32-bit two's-complement pattern, which is also how you print one: `format(-8 & 0xFFFFFFFF, '032b')`.

Precedence trap: `&`, `|` and `^` bind **looser** than `==`, so `n & 1 == 0` means `n & (1 == 0)`, which is always 0. Write `(n & 1) == 0` or `n & 1 == 0` never. Shifts bind tighter than `&`, so `n & 1 << i` is `n & (1 << i)`, and arithmetic binds tighter still, so `sub - 1 & mask` is `(sub - 1) & mask`; the parentheses in this folder are for the reader.

## The identities to say out loud

- "`n & (n - 1)` drops the lowest set bit; `n & -n` keeps only it."
- "A power of two has exactly one set bit: `n > 0 and n & (n - 1) == 0`."
- "XOR cancels pairs, so XOR-ing everything leaves the odd one out."
- "A subset is a mask; bit i says whether item i is in."
- "`(sub - 1) & mask` is the next smaller submask."
- "Python's `>>` keeps the sign; mask to 32 bits for a logical shift."

## Exercises

| File | Drills |
|---|---|
| `01_get_set_clear_toggle_bits.py` | the mask `1 << i` with OR, AND NOT, XOR and shift-and-mask; every result shown as an 8-bit string |
| `02_count_bits_and_lowest_set_bit.py` | Kernighan's `n & (n - 1)` count, `n & -n`, the power-of-two check |
| `03_xor_tricks_single_number_missing_number.py` | LeetCode 136, 268, 260: XOR cancellation, XOR with the indices, splitting two singles by a distinguishing bit |
| `04_bitmask_subset_enumeration.py` | subsets as masks `0 .. 2^n - 1`, testing bit i, walking the submasks of a mask |
| `05_reverse_bits_and_shifts.py` | LeetCode 190: 32 rounds of peel-shift-push; arithmetic versus logical right shift |
