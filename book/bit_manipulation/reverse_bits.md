# Reverse Bits

*LeetCode 190 · Easy · Pattern: Bit-by-bit shift and accumulate · Reading time ~5 min*

## What the problem is really asking

Take a 32-bit unsigned integer and mirror its columns. Column 0 goes to column 31, column 1 goes to column 30, and so on. Return the integer that the mirrored pattern spells. The answer is another 32-bit integer.

The only real trap is the width. "Reverse" here means reverse all 32 columns, including the leading zeros, which turn into trailing zeros. Python integers have no fixed width, so you have to impose it yourself.

```text
n = 11
col:   31 ...                        3 2 1 0
in  =  0000000000000000000000000000 1 0 1 1
out =  1 1 0 1 0000000000000000000000000000
       31 30 29 28 ...                     0
       = 3489660928
```

## Do it by hand first

On paper you would write the 32 digits out, then copy them into a new row starting from the right end of the old one. Your finger moves right to left on the input while your pen moves left to right on the output.

```text
input : 0 0 0 ... 0 1 0 1 1
                          <- finger starts here
output: 1 1 0 1 0 0 ... 0
        pen starts here ->
```

You kept track of two positions moving in opposite directions: where you are reading and where you are writing. The seed is that pair of cursors, and on integers both cursors can be shifts.

## The first honest attempt

Turn the number into text: `format(n, '032b')` gives 32 characters, `[::-1]` reverses them, and `int(..., 2)` parses them back. This is correct, and it is O(32).

```text
11 -> "000...01011"   format  (allocate 32 chars)
   -> "11010...000"   reverse (allocate 32 more)
   -> 3489660928      parse   (read 32 chars)
```

The waste is not asymptotic. It is three passes over a text buffer plus string allocations, all to do something the CPU can do on one register with shifts. A common slip is `bin(n)[2:][::-1]`, which forgets the padding.

## The turning point

**Claim: reading the input from the right and writing the output from the left is two shifts per step.**

- Read the lowest bit of the input: `n & 1`. Then discard it: `n >>= 1`. The next bit is now at column 0.
- Write into the output: `result = (result << 1) | bit`. Shifting left opens an empty column 0, and OR drops the bit into it. Every bit written earlier moves one column up.

The first bit read is pushed up once per later step. After 32 steps it has moved 31 times and sits at column 31. In general, the bit read at step `k` (from column `k` of the input) is shifted `31 - k` more times and lands at column `31 - k`. That is exactly the mirror.

Picture a conveyor belt feeding a stack: the input belt moves right and drops its last item, and the output stack pushes everything up to make room at the bottom.

The loop must run **exactly 32 times**, not "until n is 0". When `n` runs out of 1s, the remaining steps still shift `result` left, and that is what moves the early bits up to the top columns.

## Watch it work

`n = 11`. Only the low columns of `n` and `result` are shown; everything not shown is 0.

```text
Frame 1   step 0   read n & 1 = 1
  n      = ...0 1 0 1 1  -> after >>1: ...0 0 1 0 1  (5)
  result = ...0 0 0 0 1                              (1)
```
Bit 0 of the input becomes the only bit of `result`.

```text
Frame 2   step 1   read 1
  n      = ...0 0 0 1 0                              (2)
  result = ...0 0 0 1 1                              (3)
```
`result` shifted left and took the new 1 at column 0.

```text
Frame 3   step 2   read 0
  n      = ...0 0 0 0 1                              (1)
  result = ...0 0 1 1 0                              (6)
```
A 0 entered `result` at the bottom; the earlier bits moved up.

```text
Frame 4   step 3   read 1
  n      = ...0 0 0 0 0                              (0)
  result = ...0 1 1 0 1                              (13)
```
`n` is now 0. A loop that stopped here would return 13, which is wrong.

```text
Frame 5   steps 4..31   read 0 each time (28 more steps)
  result = 1101 followed by 28 zeros   (3489660928)
```
Each of the 28 remaining steps pushes `1101` one column higher, until it fills columns 31..28.

Across the frames, `result` held the bits read so far in reverse order, and `n` held the bits not yet read. Together they always accounted for all 32 original bits.

## Why it is correct

Invariant after `k` steps: `result` holds input bits 0..k-1 mirrored into columns k-1..0 (bit 0 at the top, column k-1), and `n` equals the original shifted right by `k`. Step `k + 1` reads input bit `k` from column 0 of `n`. Shifting `result` left moves every stored bit up one, so bit 0 is now at column k, and the new bit goes in at column 0. The invariant holds with `k + 1`. At `k = 32`, input bit `i` sits at column `31 - i` for every `i`, which is the definition of the reversal.

## Cost

- Time: O(32) = O(1). Exactly 32 iterations of a shift, an AND, an OR and a shift.
- Space: O(1). Two integers.

The constant-time refinement swaps adjacent halves, then quarters, bytes, nibbles, pairs, and single bits, using masks like `0x55555555`.

## Variations you will meet

- **"Called many times"** follow-up: cache the reversal of each byte in a 256-entry table, then reverse a word as four table lookups with the bytes in swapped order.
- **Divide-and-conquer swaps**: `n = (n >> 16) | (n << 16)`, then swap bytes inside each half with `0xFF00FF00` masks, and so on down to single bits. Remember to mask to 32 bits in Python after each left shift.
- **Reverse only the significant bits** (for example, a binary palindrome check): loop `while n` instead of 32 times. Here the early stop is exactly what you want.
- **Java/C signed integers**: use the unsigned shift `>>>` in Java, otherwise the sign bit gets copied in from the left.

## What to carry forward

Read with `n & 1` and `n >>= 1`, write with `(r << 1) | bit`, and run for the full width, because zeros count as columns too. The next problem stops moving bits and starts cancelling them: XOR makes equal numbers vanish.
