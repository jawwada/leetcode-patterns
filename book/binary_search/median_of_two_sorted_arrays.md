# Median of Two Sorted Arrays

*LeetCode 4 · Hard · Pattern: Binary search on a partition · Reading time ~12 min*

## The problem

Given two sorted arrays nums1 (size m) and nums2 (size n), return the median of their combined sorted order in O(log(m
+ n)).

```text
Example: nums1 = [1,3], nums2 = [2] returns 2.0; nums1 = [1,2],
  nums2 = [3,4] returns 2.5.
```

## What the problem is really asking

We are given two sorted arrays, `nums1` of length `m` and `nums2` of length `n`. We want the median of all `m + n` numbers together: the middle one if the total is odd, or the average of the two middle ones if it is even. The required time is O(log(m + n)), which rules out merging.

The answer is a number, but the thing we really have to find is a **split**: which elements belong to the lower half of the combined data. Once we know the lower half, the median is read off its edge. The difficulty is that the lower half draws from both arrays, and we must decide how many come from each without walking through either one.

```text
A = [1, 18, 21, 24]           (m = 4)
B = [7, 8, 13, 14, 20, 23]    (n = 6)

merged:  1  7  8 13 14 | 18 20 21 23 24
         --- lower 5 ---  --- upper 5 ---
median = (14 + 18) / 2 = 16
```

## Do it by hand first

With two sorted lists on paper, you would probably merge them with two fingers until you have counted off half the elements. Five steps here: 1, 7, 8, 13, 14. Then you look at the next one, 18, and average the two.

```text
A:  1  18  21  24          finger a
    ^
B:  7   8  13  14  20  23  finger b
    ^
take 1(A) 7(B) 8(B) 13(B) 14(B)  -> 5 taken
    now a -> 18, b -> 20; next smallest = 18
lower half = {1} from A + {7,8,13,14} from B
```

Look at what the merge produced in the end: **one number from A and four from B**. Everything else (the order in which you took them) was scaffolding. The final state of your hand was two finger positions whose sum was fixed at 5. That pair of positions, a cut in each array, is what we will search for.

## The first honest attempt

"Merge with two pointers until index `(m + n) // 2`, then read the middle." That is O(m + n) time, and O(1) space if you don't store the merge. It is correct and simple, and it is what most people say first.

```text
step:   1   2   3   4   5
takes:  1   7   8  13  14
        each step compares two heads and advances
        one finger by ONE position
```

The waste is that each comparison moves a cut by one element, although the cuts are linked (their positions always sum to the number taken), so there is really only one free variable, and it is ordered. Searching a one-dimensional ordered choice one step at a time is exactly the linear scan this whole chapter has been replacing with halving.

## The turning point

**Claim: the lower half is a prefix of A of some length `i` plus a prefix of B of length `j = half - i`, where `half = (m + n + 1) // 2`, and the right `i` is found by binary search using only the four values around the two cuts.**

*Why prefixes.* The lower half consists of the `half` smallest elements. Within a sorted array, if an element is among the smallest overall, so is everything before it. So the lower half takes a prefix from each array. Fixing the total `half` means choosing `i` determines `j`.

```text
    A:  a0 ... a(i-1) | a(i) ...         i taken from A
    B:  b0 ... b(j-1) | b(j) ...         j = half - i from B

        Aleft = a(i-1)   Aright = a(i)
        Bleft = b(j-1)   Bright = b(j)
```

*When is a cut correct?* The left side must be all `<=` the right side. Inside each array that holds automatically, because the arrays are sorted. Across arrays only two comparisons matter: `Aleft <= Bright` and `Bleft <= Aright`. Missing values at the ends act as sentinels: `Aleft = -inf` when `i = 0`, `Aright = +inf` when `i = m`, and likewise for B.

*The predicate and why it is monotone.* Name the failure modes.

- `Aleft > Bright` means **too many from A**: an A element on the left is bigger than a B element on the right, so swap it out by decreasing `i`.
- `Bleft > Aright` means **too few from A**: increase `i`.

As `i` grows, `Aleft = A[i-1]` rises (or stays) and `Bright = B[half - i]` falls (or stays), so "too many" is false up to some `i` and true from then on. Symmetrically, "too few" is true up to some `i` and false from then on. Over `i = 0..m` the picture is three blocks:

```text
i          :   0     1     2     3     4
too few?   :   T     F     F     F     F
too many?  :   F     F     T     T     T
verdict    :  go R  STOP  go L  go L  go L
                     ^
          the valid cut sits between the blocks
```

(This is the actual verdict row for our example.) A valid cut always exists, because the true merged lower half is one, and the monotone blocks mean that binary search on `i` steers toward it from either side.

*Search the shorter array.* Keep `A` as the shorter one, so `m <= n`. Then for every `i` in `[0, m]`, `j = half - i` lands in `[0, n]`, so B never needs an index outside itself. That also makes the cost O(log min(m, n)).

*Reading the answer.* If the total is odd, `half` holds one extra element, so the median is `max(Aleft, Bleft)`. If even, it is `(max(Aleft, Bleft) + min(Aright, Bright)) / 2`.

## Watch it work

`A = [1, 18, 21, 24]` (shorter, `m = 4`), `B = [7, 8, 13, 14, 20, 23]` (`n = 6`), `half = (10 + 1) // 2 = 5`. Search `i` in `[0, 4]`.

```text
Frame 1   lo=0  hi=4
  A:  1 18 21 24
  B:  7  8 13 14 20 23
  need 5 on the left; i from A, j = 5 - i from B
```
The search space is the five possible cut positions in A.

```text
Frame 2   lo=0 hi=4  i=2  j=3
  A:  1 18 | 21 24          Aleft=18 Aright=21
  B:  7  8 13 | 14 20 23    Bleft=13 Bright=14
  Aleft 18 > Bright 14  -> too many from A
```
18 cannot be in the lower half while 14 is outside it: `hi = 1`.

```text
Frame 3   lo=0 hi=1  i=0  j=5
  A:  | 1 18 21 24          Aleft=-inf Aright=1
  B:  7  8 13 14 20 | 23    Bleft=20   Bright=23
  Bleft 20 > Aright 1   -> too few from A
```
1 is left out while 20 is in, which is wrong the other way: `lo = 1`.

```text
Frame 4   lo=1 hi=1  i=1  j=4
  A:  1 | 18 21 24          Aleft=1  Aright=18
  B:  7  8 13 14 | 20 23    Bleft=14 Bright=20
  1 <= 20  and  14 <= 18  -> valid cut
```
Both cross-checks pass. The left side is {1, 7, 8, 13, 14}, matching the hand merge.

```text
Frame 5   read the median (total 10, even)
  max(Aleft, Bleft)   = max(1, 14)  = 14
  min(Aright, Bright) = min(18, 20) = 18
  median = (14 + 18) / 2 = 16.0
```
The two values next to the cut are the two middle elements of the merge.

The left side always held exactly 5 elements; only their split between A and B moved. Every `i` above `hi` was known to take too many from A and every `i` below `lo` too few, so the valid cut stayed inside `[lo, hi]`.

## Why it is correct

**Invariant: the valid cut `i*` lies in `[lo, hi]`.** Initially `[0, m]` holds every possible cut. When `Aleft > Bright` at `i`, the "too many" predicate is true at `i`, and by monotonicity at every larger `i`, so none of them is valid and `hi = i - 1` keeps `i*` inside. When `Bleft > Aright`, "too few" is true at `i` and at every smaller `i`, so `lo = i + 1` is safe. The two failures cannot both happen at the same `i`. That would mean `A[i-1] > B[j] >= B[j-1] > A[i]`, contradicting that A is sorted. If neither happens, the cut is valid, every left element is `<=` every right element, and the left side has exactly `half` elements. So the largest left value is the `half`-th smallest overall, and the smallest right value is the next one, which are precisely the median's ingredients. Since a valid cut exists and the interval shrinks every step, we find it.

## Cost

- **Merge:** O(m + n) time, O(1) space if you only count.
- **Binary search on the cut:** O(log min(m, n)) time, since each step halves the range of `i` in the shorter array. **O(1)** space, just four boundary values.

## Variations you will meet

- **K-th smallest of two sorted arrays.** Replace `half` with `k`. The same partition search applies, or use the elimination version: compare `A[k/2 - 1]` with `B[k/2 - 1]` and discard the smaller array's first `k/2`, which is O(log k).
- **Median of k sorted arrays, or of a row-sorted matrix.** The partition trick does not generalise past two arrays. Switch to binary search on the value with a count (`bisect` per row), exactly as in the multiplication table.
- **Streaming median (LeetCode 295).** Data arrives one item at a time, so keep two heaps (a max-heap of the lower half and a min-heap of the upper half), which is the same left/right picture maintained incrementally.
- **Unequal weights or "find the p-th percentile".** Change `half` to the target rank. The cut conditions are unchanged.

## What to carry forward

When the answer is a split of two sorted sequences, search the cut in the shorter one: the other cut is forced, and two cross-comparisons tell you whether to move left, move right, or stop.

This closes the chapter. We started by halving an index range to find a value, learned to halve when the sorted order is broken (rotations, peaks), moved to halving the range of possible answers with a monotone check, and finished by halving the space of partitions. In every case the question is the same: what is the monotone yes/no, and over what ordered space does it live?
