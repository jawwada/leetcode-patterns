# Single Number

*LeetCode 136 · Easy · Pattern: XOR cancellation · Reading time ~5 min*

## The problem

Every element of a non-empty array appears exactly twice except one, which appears once; find that element in linear
time using constant extra space.

```text
Example: [4,1,2,1,2] -> 4. Example: [2,2,1] -> 1.
```

## What the problem is really asking

Every value in the array appears exactly twice, except one value that appears once. Return that loner. The answer is one of the array's values. The difficulty is entirely in the constraints: linear time and constant extra space. A hash set would solve it in one pass, but a hash set grows with the input.

```text
nums = [4, 1, 2, 1, 2]

   4    1    2    1    2
        \____|____/    |
             \_________/
   ^ no partner -> 4
```

## Do it by hand first

On paper you would cross off pairs. Spot a 1, find the other 1, strike both. Same for the 2s. Whatever is left standing is the answer.

```text
 4   1   2   1   2
     x       x        strike the 1s
         x       x    strike the 2s
 4                    survivor
```

Your hand kept track of "which values are still waiting for a partner". That waiting set grows and shrinks. A value enters when first seen and leaves when its twin arrives. The question is whether that set can be squeezed into a single integer.

## The first honest attempt

For each element, scan the array and count its occurrences; return the one whose count is 1. O(n²) time, O(1) space. The O(n)-time fix is a hash set, toggling membership, but that costs O(n) space.

```text
x = 4: scan 4 1 2 1 2 -> count 1   found
x = 1: scan 4 1 2 1 2 -> count 2
x = 2: scan 4 1 2 1 2 -> count 2
...    every scan rediscovers the same pairs
```

The waste in the quadratic version is that the pairing between the two 1s is discovered again on every scan and never stored. The waste in the hash-set version is subtler. We store which values are waiting, but we never need to know which partner matched which. All we need is the final survivor.

## The turning point

**Claim: XOR-ing every element of the array leaves exactly the single number.**

XOR has three properties that make it a "pair eraser":

- `a ^ a = 0`: a value meeting its twin vanishes.
- `a ^ 0 = a`: zero is neutral, so the vanished pairs leave no trace.
- XOR is commutative and associative, so order does not matter. The two 1s do not need to be adjacent; you can reorder the whole expression in your head to put twins side by side.

```text
4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)    regroup freely
= 4 ^   0     ^   0
= 4
```

There is a second, column-level way to see it, and it is the one that generalises. Take any single bit column. A value that appears twice contributes either zero or two 1s to that column, which is an even number either way. So the parity of the column, odd or even, is decided by the loner alone. XOR computes the parity of all 32 columns at once.

The "waiting set" from the hand method has become a single integer. When a value arrives its bits flip in, and when its twin arrives the same bits flip back out.

## Watch it work

`nums = [4, 1, 2, 1, 2]`, accumulator `acc` starts at 0. Columns are bit 2, bit 1, bit 0.

```text
Frame 1   read 4 = 1 0 0
  acc = 0 0 0 ^ 1 0 0 = 1 0 0   (4)
```
4 is waiting; its bit 2 is on in `acc`.

```text
Frame 2   read 1 = 0 0 1
  acc = 1 0 0 ^ 0 0 1 = 1 0 1   (5)
```
1 joins the waiting set; `acc` now encodes {4, 1} mixed together.

```text
Frame 3   read 2 = 0 1 0
  acc = 1 0 1 ^ 0 1 0 = 1 1 1   (7)
```
2 joins; `acc` is 7, which is none of the inputs. The intermediate value need not mean anything.

```text
Frame 4   read 1 = 0 0 1
  acc = 1 1 1 ^ 0 0 1 = 1 1 0   (6)
```
The second 1 flips bit 0 back off: 1 has left the waiting set.

```text
Frame 5   read 2 = 0 1 0
  acc = 1 1 0 ^ 0 1 0 = 1 0 0   (4)
```
The second 2 cancels; only 4's bits remain, so the answer is 4.

At every frame, `acc` equalled the XOR of the values currently waiting for a partner. Middle values like 7 looked meaningless, but the parity of every column stayed honest.

## Why it is correct

Invariant: after reading a prefix of the array, `acc` is the XOR of all values that have appeared an odd number of times in that prefix. Reading `x` toggles whether `x` has appeared an odd number of times, and `acc ^= x` toggles `x` in or out of the XOR. At the end, every paired value has appeared an even number of times, so only the single number remains, and `acc` is exactly that number. Order never matters, because XOR is commutative and associative.

## Cost

- Time: O(n). One XOR per element.
- Space: O(1). One integer, however large the array is.

## Variations you will meet

- **Single Number II** (LeetCode 137: everyone else appears three times): XOR fails, because three copies leave one copy behind. Count each bit column mod 3 instead, or use the two-variable `ones`/`twos` state machine. Same column thinking, different modulus.
- **Single Number III** (LeetCode 260: two loners): XOR everything to get `a ^ b`. Any set bit of that, say `d = x & -x`, is a column where `a` and `b` differ. Split the array by that bit and XOR each half.
- **Negative numbers**: XOR works on the bit pattern, so negatives are fine in Python and in two's-complement languages.
- **Find the Difference** (LeetCode 389): two strings, one has an extra letter. XOR all the character codes of both strings and the extra one survives.

## What to carry forward

XOR is a pair eraser and a column-parity counter, and it does not care about order. The next problem has no explicit pairs, so we manufacture them: XOR the indices against the values, and the missing number is the one without a partner.
