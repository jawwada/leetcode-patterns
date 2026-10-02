# Remove Duplicates from Sorted Array II
*LeetCode 80 · Medium · Pattern: Slow/fast pointers with look-back · Reading time ~7 min*

## What the problem is really asking

You get a sorted array. Edit it in place so that every value appears at most twice, keep the order, and return the new length `k`. Only the first `k` cells are judged; whatever sits after them is ignored. Extra space must be O(1).

So the answer is an integer plus a rewritten prefix. Two things make it harder than it looks. You may not build a second array, and "at most twice" needs some notion of how many copies of the current value you have already kept, without a counter that grows into a dictionary.

```text
input:   [ 1 | 1 | 1 | 2 | 2 | 3 ]
                   ^
                   third 1: must go

output:  [ 1 | 1 | 2 | 2 | 3 | ? ]    k = 5
          \_________________/
           judged prefix
```

## Do it by hand first

Read the input left to right and copy values onto a new line, refusing any value that would be the third copy in a row.

```text
read   copied so far     decision
 1     1                 keep (first 1)
 1     1 1               keep (second 1)
 1     1 1               refuse: already two 1s
 2     1 1 2             keep
 2     1 1 2 2           keep
 3     1 1 2 2 3         keep
```

How did you decide "already two 1s"? You glanced at the end of the line you were writing and saw two 1s there. You looked at your **output**, not at the input. Because the array is sorted, equal values sit next to each other, so the last two written values are all you need to see. That glance is the seed: a writer that checks its own output two cells back.

## The first honest attempt

Walk the array; whenever the current element equals the two before it, delete it with `del nums[i]`, and do not advance `i` (the next element just slid into position `i`).

That is correct and in place, but each delete shifts the entire tail left by one cell. With many duplicates, say `[1, 1, 1, 1, ..., 1]` of length n, you delete n - 2 times and each delete moves up to n cells: O(n^2).

```text
del at index 2:
  [ 1 | 1 | 1 | 1 | 1 | 2 ]
            x <-- <-- <--     4 cells shift
  [ 1 | 1 | 1 | 1 | 2 ]
del at index 2 again:
            x <-- <--         3 cells shift
  [ 1 | 1 | 1 | 2 ]
the same tail values move again and again
```

The repeated work: the `2` at the end moved one slot per deletion, when its final position (index 2) was knowable the first time it was read.

## The turning point

**Claim: in a sorted array, `nums[read]` would be a third copy exactly when it equals `nums[write - 2]`, the cell two slots back in the output.**

Why: the output prefix `nums[0:write]` is sorted (it is a subsequence of a sorted array) and already obeys "at most two copies". If the new value `x` equals `nums[write - 2]`, then because the prefix is sorted, `nums[write - 1]` lies between them and also equals `x`. So the output already ends with two copies of `x` and a third is forbidden. If `x` differs from `nums[write - 2]`, then the output ends with at most one copy of `x` (the last cell, possibly), and keeping it gives at most two.

That turns deletion inside out. Instead of removing bad elements and shifting the tail, copy good elements forward:

- `write` is the slow pointer: the length of the finished output, and the next free slot.
- `read` is the fast pointer: it visits every input cell once.
- The first two cells are always kept, so both start at 2.

```text
regions:
  [ finished output | junk | unread ]
    0 ...... write-1         read..n-1
             ^
   look-back target: nums[write-2]
```

Why must the look-back target the output and not the input (`nums[read - 2]`)? Because the writer overwrites cells as it goes, and `read - 2` may now hold a value copied there, not the original. With `[1, 1, 1, 2, 2]` the input look-back version keeps the first 2, then compares the second 2 with `nums[2]`, which it just overwrote with a 2, and wrongly drops it. The output prefix is the one region whose contents you trust completely.

## Watch it work

`nums = [1, 1, 1, 2, 2, 3]`. `write = 2`, `read` starts at 2.

Frame 1. `read = 2` sees 1. Look-back `nums[0] = 1`: equal, so this is a third 1. Rejected; `write` stays 2.

```text
  [ 1 | 1 | 1 | 2 | 2 | 3 ]
    ^       w
  w-2       r
  1 == 1 -> reject           write=2
```

Frame 2. `read = 3` sees 2. Look-back `nums[0] = 1`: different. Copy 2 into slot 2; `write = 3`.

```text
  [ 1 | 1 | 2 | 2 | 2 | 3 ]
    ^       ^   r
  w-2   (written)
  2 != 1 -> keep             write=3
```

Frame 3. `read = 4` sees 2. Look-back `nums[1] = 1`: different. Copy 2 into slot 3; `write = 4`.

```text
  [ 1 | 1 | 2 | 2 | 2 | 3 ]
        ^       ^   r
      w-2   (written)
  2 != 1 -> keep             write=4
```

Frame 4. `read = 5` sees 3. Look-back `nums[2] = 2`: different. Copy 3 into slot 4; `write = 5`. Done, return 5.

```text
  [ 1 | 1 | 2 | 2 | 3 | 3 ]
            ^       ^   r
          w-2   (written)
  3 != 2 -> keep             write=5
  \_________________/
   answer, k = 5
```

In every frame the prefix before `write` was sorted and had no value three times, and the look-back only ever read inside that prefix.

## Why it is correct

Invariant after each reader step: `nums[0:write]` equals the "at most two of each" version of `input[0:read+1]`, in order.

Base: after the first two cells, the prefix is those two cells, which trivially has at most two of anything.

Step: the reader brings value `x`. By the claim, `x == nums[write - 2]` exactly when the correct output for `input[0:read+1]` already ends with two copies of `x`, so dropping it keeps the invariant. Otherwise the correct output appends `x`, which is what the copy does. The copy writes to slot `write <= read`, so it never destroys an input cell the reader still needs.

When `read` reaches the end, `nums[0:write]` is the answer for the whole input and `write` is `k`.

## Cost

- Time: O(n). The reader makes n - 2 steps; each does one comparison and at most one write.
- Space: O(1). Two integers.

The delete-based version is O(n^2) time in the worst case because of tail shifting.

## Variations you will meet

- **Remove Duplicates from Sorted Array (LeetCode 26)**: at most one copy. Look back one cell: keep `x` if it differs from `nums[write - 1]`, and start both pointers at 1.
- **At most k copies**: start both pointers at `k` and compare with `nums[write - k]`. The proof is identical, which is why the look-back form is worth learning instead of a "count of the current run" variable.
- **Unsorted input**: the look-back fails because equal values are not adjacent. You need a hash map of counts, and O(n) extra space.
- **Linked list version (LeetCode 82, 83)**: the writer becomes a `prev` node and "copy forward" becomes relinking `prev.next`; the look-back idea maps onto comparing with the last kept node.

## What to carry forward

A slow writer that checks its own output a fixed distance back replaces any counter, as long as the input is sorted so equal values are adjacent. The next problem keeps the reader but adds a second writer growing from the other end, so the array is split into three coloured regions in one pass.
