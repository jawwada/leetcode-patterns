# Counting Bits

*LeetCode 338 · Easy · Pattern: Reuse the count of i >> 1 · Reading time ~5 min*

## The problem

Given n, return an array ans of length n + 1 where ans[i] is the number of 1-bits in the binary form of i.

```text
Example: n = 5 -> [0,1,1,2,1,2] for 0, 1, 10, 11, 100, 101.
```

## What the problem is really asking

For every integer `i` from 0 to `n`, report how many 1-bits it has. The answer is a list of `n + 1` small numbers. The previous problem counted bits for one number. Here we count for a whole range, and the question becomes whether the counts can be built from each other instead of computed separately.

```text
n = 5

 i   binary   ones
 0   000      0
 1   001      1
 2   010      1
 3   011      2
 4   100      1
 5   101      2        -> [0, 1, 1, 2, 1, 2]
```

## Do it by hand first

Write 0 to 7 in binary, one under another, and look at them in pairs: 2 and 3, 4 and 5, 6 and 7.

```text
 i   binary          i >> 1   binary
 6   1 1 0            3       1 1
 7   1 1 1            3       1 1
 4   1 0 0            2       1 0
 5   1 0 1            2       1 0
     \___/ \_/
     same   last bit differs
```

The left part of 6 and of 7 is `11`, which is 3 written in binary. The only difference is the last digit. Once you know 3 has two 1s, you know 6 has two (append a 0) and 7 has three (append a 1). Your hand kept track of "the count for the number with the last bit chopped off". That is the seed: a table of earlier answers you can look up.

## The first honest attempt

Count each number from scratch, either by testing 32 columns or with the `n & (n - 1)` loop from the previous problem. That is O(32 · n), or O(n log n) with the faster loop.

```text
popcount(6) = test 1 1 0      -> 2
popcount(7) = test 1 1 1      -> 3
                   ^ ^
           these two columns were counted
           already, when we did popcount(3)
```

The waste: every number's high bits are some smaller number we already counted, and we count them again.

## The turning point

**Claim: `popcount(i) = popcount(i >> 1) + (i & 1)`.**

`i >> 1` is `i` with its last column dropped, so it holds exactly the high bits of `i`. `i & 1` is the dropped column. The 1s of `i` are the 1s of its top part plus possibly the last one, which gives the formula.

And `i >> 1` is smaller than `i` for every `i ≥ 1`. So if we fill the table from left to right, the entry for `i >> 1` is already there when we need it. This is a one-dimensional DP whose transition is a shift.

A tree helps. Make `i >> 1` the parent of `i`. Every number is its parent with one bit appended: a left child appends 0, a right child appends 1. A node's count is its parent's count plus the label of the edge leading to it.

```text
               1 (1)
            0/     \1
          2 (1)    3 (2)
         0/ \1     0/ \1
       4(1) 5(2) 6(2) 7(3)

number (count); edge label = appended bit
```

## Watch it work

`n = 7`, table `bits` starts as `[0, 0, 0, 0, 0, 0, 0, 0]`.

```text
Frame 1   i = 1 = 1     parent 0
  bits: [0, 1, _, _, _, _, _, _]
           ^  bits[0] + 1
```
1 is 0 with a 1 appended, so its count is 0 + 1.

```text
Frame 2   i = 2 = 10, i = 3 = 11   parent 1
  bits: [0, 1, 1, 2, _, _, _, _]
                 ^  ^ bits[1]+0, bits[1]+1
```
Both share parent 1 (count 1); 2 appends a 0, 3 appends a 1.

```text
Frame 3   i = 4 = 100, i = 5 = 101   parent 2
  bits: [0, 1, 1, 2, 1, 2, _, _]
                       ^  ^ bits[2]+0, bits[2]+1
```
Their parent 2 has count 1, which was written in Frame 2.

```text
Frame 4   i = 6 = 110, i = 7 = 111   parent 3
  bits: [0, 1, 1, 2, 1, 2, 2, 3]
                             ^  ^ bits[3]+0, bits[3]+1
```
Parent 3 has count 2; the table is full and is returned.

Throughout, every entry left of `i` was final, and `i >> 1` always pointed into that finished part. Each entry cost one shift, one AND and one add.

## Why it is correct

By induction on `i`. `bits[0] = 0` is right, since 0 has no 1s. Suppose every entry below `i` is correct. Then `bits[i >> 1]` is the true count of `i >> 1`, which is the count of `i`'s bits above column 0. Adding `i & 1` accounts for column 0. So `bits[i]` is correct. The induction is valid because `i >> 1 < i` for every `i ≥ 1`, so we only ever read entries that are already finished.

## Cost

- Time: O(n). Constant work per entry.
- Space: O(1) beyond the output list of size `n + 1`.

The per-number popcount approach is O(n log n). The DP removes the log factor because nothing is ever counted twice.

## Variations you will meet

- **Other recurrences**: `bits[i] = bits[i & (i - 1)] + 1` also works. It drops the lowest 1 instead of the lowest column, so the parent is a smaller number with one fewer 1. Any recurrence that points to a smaller, already-filled index will do.
- **Using the previous power of two**: `bits[i] = 1 + bits[i - highest_power_of_two(i)]`. It is the same idea with the top bit removed, but you have to track the power, which makes it clumsier.
- **Sum of popcounts over 0..n without the list**: count column by column. Column `k` is on in a fixed pattern of blocks of length `2^(k+1)`, so the total has a closed form, O(log n).
- **Interview follow-up "without builtins"**: they want exactly this recurrence, not `bin(i).count("1")`.

## What to carry forward

A number is its half with one bit appended, so its count is the half's count plus that bit. Shifting turns bit problems into DP over smaller numbers. The next problem keeps shifting, but instead of counting bits it moves them, reading from one end of the word and writing to the other.
