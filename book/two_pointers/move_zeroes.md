# Move Zeroes
*LeetCode 283 · Easy · Pattern: Read/write pointers (stable compaction) · Reading time ~5 min*

## What the problem is really asking

Push every zero to the end of the array, in place, while the non-zero values keep their original order. You return nothing; the array itself is the answer.

Two constraints make it more than a one-liner. "In place" rules out building a new list. "Keep the relative order" rules out sorting and rules out the trick of swapping zeros with the last element. The non-zeros must come out as a stable, compacted prefix.

```text
before: [ 0 | 1 | 0 | 3 | 12 ]
after:  [ 1 | 3 | 12 | 0 | 0 ]
          \_________/  \___/
          same order   zeros
```

## Do it by hand first

Copy the non-zeros onto a fresh line, left to right, and then pad with zeros. For `[0, 1, 0, 3, 12]` you write `1`, then `3`, then `12`, then two zeros.

```text
read:   0   1   0   3   12
            |       |   |
write:      1   3   12  0   0
slot:       0   1   2   3   4
```

Notice what your hand tracked: where the next non-zero goes. The first non-zero goes to slot 0, the second to slot 1, the k-th to slot k-1. One counter. That counter is the writer.

## The first honest attempt

Bubble the zeros rightward: scan the array, and whenever a zero sits just left of a non-zero, swap them. Repeat whole passes until nothing moves. It is in place and stable. It is also O(n^2) in the worst case.

The waste is that a non-zero only hops one slot left per swap. A value with k zeros in front of it gets moved k separate times, even though its final position was known from the start.

```text
[ 0 | 0 | 0 | 7 ]   7 must travel 3 slots
[ 0 | 0 | 7 | 0 ]   swap 1
[ 0 | 7 | 0 | 0 ]   swap 2
[ 7 | 0 | 0 | 0 ]   swap 3
one value, three moves; with n/2 zeros in
front of n/2 values that is n^2/4 swaps
```

## The turning point

**Claim: the k-th non-zero belongs at index k (counting from 0), so it can be sent there in one move.**

Order is preserved and the zeros all go to the tail, so the final array is just the non-zeros in reading order followed by zeros. The k-th non-zero you meet while reading lands in slot k. That is exactly the "next slot" counter from the hand solution.

So keep two indices moving right. The reader `r` visits every cell. The writer `w` is the number of non-zeros placed so far, which is also the slot where the next one goes. When `nums[r]` is non-zero, put it at `w` and advance `w`.

How do you "put it at `w`" in place without losing anything? Swap. The cell at `w` is either the same cell as `r` (no zeros seen yet, the swap is a no-op) or a zero (everything between `w` and `r` is a zero we already passed). Swapping carries that zero forward to `r`. The zeros never need a separate fill-in pass; they ride along in the gap.

```text
regions during the scan:

  [ non-zeros in order | zeros | unread ]
    0 ............ w-1   w..r-1  r .. n-1
```

## Watch it work

`nums = [0, 1, 0, 3, 12]`.

Frame 1. `r = 0` reads a zero. Nothing to place; `w` stays 0.

```text
  [ 0 | 1 | 0 | 3 | 12 ]
    w
    r              w=0
```

Frame 2. `r = 1` reads 1. Swap slots 0 and 1; the zero is carried to slot 1. `w` becomes 1.

```text
  [ 1 | 0 | 0 | 3 | 12 ]
        w
        r          w=1
```

Frame 3. `r = 2` reads a zero. Skip. The gap `w..r` now holds two zeros.

```text
  [ 1 | 0 | 0 | 3 | 12 ]
        w   r      w=1
       \_____/ zeros
```

Frame 4. `r = 3` reads 3. Swap slots 1 and 3. `w` becomes 2.

```text
  [ 1 | 3 | 0 | 0 | 12 ]
            w   r  w=2
```

Frame 5. `r = 4` reads 12. Swap slots 2 and 4. `w` becomes 3, and the scan ends.

```text
  [ 1 | 3 | 12 | 0 | 0 ]
                 w   r  w=3
  \__________/  \_____/
   non-zeros     zeros
```

In every frame the prefix before `w` was the non-zeros seen so far, in order, and the cells from `w` up to `r` were all zeros.

## Why it is correct

Invariant, checked after each reader step: `nums[0:w]` holds the non-zeros among the first `r + 1` cells, in their original order, and `nums[w:r+1]` are all zeros.

It holds trivially before the first step. If the reader sees a zero, it simply joins the zero gap. If the reader sees a non-zero, the swap places it at `w`, directly after the earlier non-zeros, so order is kept, and moves the zero from `w` (or nothing, if `w == r`) to `r`, which keeps the gap all zeros. When `r` reaches the end, the whole array is the non-zero prefix followed by the zero gap.

## Cost

- Time: O(n). The reader takes n steps; each step does at most one swap.
- Space: O(1). Two integers.

An overwrite-then-fill version (copy non-zeros forward, then write zeros from `w` to the end) is also O(n) and O(1). The swap version does it in one pass and performs fewer writes when there are few zeros.

## Variations you will meet

- **Remove Element (LeetCode 27)**: drop every copy of `val` and return the new length. Same reader/writer, but you overwrite instead of swapping, because the dropped values do not have to survive.
- **Remove Duplicates from Sorted Array (LeetCode 26)**: the "keep" test becomes "differs from the last kept value", which looks back into the writer's output. The chapter's Remove Duplicates II generalises this.
- **Move zeros to the front**: run the same scan from right to left with the writer starting at `n - 1`.
- **Order does not matter**: then a converging swap (zero at the left pointer with a non-zero at the right pointer) uses fewer swaps, but it scrambles the non-zeros.

## What to carry forward

A writer that counts "how many I have kept" is also "where the next one goes"; swapping instead of overwriting carries the discarded values along for free. Next, the pointers go back to converging from both ends, but this time they build an output array instead of checking a property.
