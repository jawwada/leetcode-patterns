# Number of 1 Bits

*LeetCode 191 · Easy · Pattern: Clear lowest set bit (n & (n - 1)) · Reading time ~5 min*

## What the problem is really asking

You get a 32-bit unsigned integer and must say how many of its 32 columns hold a 1. This count has a name, the Hamming weight or popcount. The answer is a single number between 0 and 32.

Nothing about it is hard to get right. The interesting part is how little work you can do: can the loop run once per 1-bit instead of once per column?

```text
n = 44

col:  5 4 3 2 1 0
      1 0 1 1 0 0
      ^   ^ ^
three lamps on -> answer 3
```

## Do it by hand first

With pen and paper you write 44 in binary, `101100`, and tick each 1 as you see it. Your eye skips the zeros. It jumps from one 1 to the next, and you stop when no 1 is left.

```text
1 0 1 1 0 0
    tick ^      (col 2)  count 1
  tick ^        (col 3)  count 2
tick ^          (col 5)  count 3
nothing left -> 3
```

What your hand kept track of was "the lowest 1 I have not ticked yet". You crossed it out and moved on. That is the seed of the trick: a way to cross out the lowest 1 in one step.

## The first honest attempt

The obvious loop tests every column: for `i` in 0..31, shift `n` right by `i` and check the last bit. It is correct and it is O(32), which is already constant time.

```text
i:   0 1 2 3 4 5 6 7 ... 31
bit: 0 0 1 1 0 1 0 0 ... 0
     x x . . x . x x ... x    x = wasted test on a zero
```

The waste is visible in the drawing: 29 of the 32 tests look at a zero. The loop count is fixed at 32 no matter what the answer is. For a sparse number like 128 (one bit set) we do 32 tests to learn the answer 1.

## The turning point

**Claim: `n & (n - 1)` is `n` with its lowest 1-bit erased and nothing else changed.**

Subtracting 1 from a binary number works like subtracting 1 from 1000 in decimal: you borrow. The borrow travels right to left through the trailing zeros, turning each into a 1, until it reaches the first 1, which pays for it and becomes 0. Every column above that 1 is untouched.

```text
n      = 1 0 1 1 0 0
n - 1  = 1 0 1 0 1 1      borrow stopped at col 2
           same   | flipped
         ----------- AND
result = 1 0 1 0 0 0      col 2 erased
```

Now AND the two rows. Above the borrow point both rows agree, so AND keeps those columns. At the borrow point `n` has 1 and `n - 1` has 0, so AND gives 0. Below it `n` has 0s, so AND gives 0. The result is `n` minus its lowest 1.

That turns the hand method into an algorithm. Erase one 1, count one, repeat until `n` is 0. The loop runs exactly as many times as there are 1-bits.

```python
while n:
    n &= n - 1      # erase the lowest 1
    count += 1
```

## Watch it work

Take `n = 44 = 101100`.

```text
Frame 1   count = 0
  n     = 1 0 1 1 0 0
  n - 1 = 1 0 1 0 1 1
  n & (n-1) = 1 0 1 0 0 0   (40)
```
The 1 in column 2 is erased; `count` becomes 1.

```text
Frame 2   count = 1
  n     = 1 0 1 0 0 0
  n - 1 = 1 0 0 1 1 1
  n & (n-1) = 1 0 0 0 0 0   (32)
```
The borrow runs through three zeros to column 3 and erases it; `count` becomes 2.

```text
Frame 3   count = 2
  n     = 1 0 0 0 0 0
  n - 1 = 0 1 1 1 1 1
  n & (n-1) = 0 0 0 0 0 0   (0)
```
The last 1 goes; `count` becomes 3.

```text
Frame 4   count = 3
  n = 0 0 0 0 0 0   loop condition false
  return 3
```
`n` is 0, so the loop stops after exactly three iterations.

Across the frames, `count + popcount(n)` stayed at 3. Each iteration moved one unit from the right term to the left one, and the bits above the erased one never moved.

## Why it is correct

The invariant is `count + popcount(n) = popcount(original n)`. It holds at the start, when `count = 0`. Each iteration lowers `popcount(n)` by exactly one, because `n & (n - 1)` removes one 1-bit and creates none. It raises `count` by one in the same step. The loop ends when `n = 0`, so `popcount(n) = 0`, and `count` equals the original popcount. It always ends, because each iteration makes `n` strictly smaller.

## Cost

- Time: O(k), where k is the number of 1-bits and k ≤ 32. Each iteration erases one bit.
- Space: O(1), just the counter.

The brute force is O(32). Both are constant, but this version's work tracks the answer, and the same trick drives harder problems.

## Variations you will meet

- **Power of Two** (LeetCode 231): `n > 0 and n & (n - 1) == 0`. A power of two has exactly one 1, so erasing it leaves zero.
- **Hamming Distance** (LeetCode 461): count the columns where `x` and `y` differ, which is `popcount(x ^ y)`. XOR builds the "differs" row and this loop counts it.
- **Using the language builtin**: `n.bit_count()` in Python 3.10+, `Integer.bitCount` in Java, `__builtin_popcount` in C. Say you know them, then show the trick.
- **Negative inputs in Java/C**: a signed right shift copies the sign bit forever, so a shift-based loop never ends. The `n & (n - 1)` loop works on the bit pattern and is safe.

## What to carry forward

`n & (n - 1)` deletes the rightmost 1. The borrow ripples through the zeros and stops at the first 1. The next problem counts bits for every number from 0 to n, and instead of erasing bits it reuses the count already computed for `i >> 1`.
