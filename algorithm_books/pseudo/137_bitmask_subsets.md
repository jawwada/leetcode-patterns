---
rank: 137
slug: bitmask_subsets
---

List every subset of an array of n distinct elements, this time without recursion. For `[1, 2, 3]` the eight subsets come out as `[]`, `[1]`, `[2]`, `[1, 2]`, `[3]`, `[1, 3]`, `[2, 3]` and `[1, 2, 3]`.

A subset is n yes-or-no answers, and n yes-or-no answers are an n-bit number. Let bit j of an integer `mask` say whether `nums[j]` is in. Then the integers from 0 to `2^n - 1`, written `(1 << n) - 1`, are exactly the `2^n` subsets, each once, and counting upward in binary walks the whole power set. Decoding a mask is a loop over j that tests `(mask >> j) & 1`, bit j shifted down to position 0. Compared with the backtracking tree of #30 this is flat: no recursion and no path to restore, just two loops, and each subset is an integer that can index an array or key a map.

The same view gives a second, subtler loop, over the submasks of a mask: every subset of a subset. Start from `sub = mask` and step with `sub = (sub - 1) & mask`. Subtracting 1 clears the lowest set bit of sub and sets every bit below it; the AND then throws away the bits that are not in mask, which leaves exactly the next smaller submask. The walk visits all `2^k` submasks of a mask with k set bits, each once and in decreasing order, and the empty submask, 0, is added after the loop stops.

```text
nums = [1, 2, 3]    bit j of the mask says whether nums[j] is in
mask   bit 2 1 0    subset
  0        0 0 0    []
  1        0 0 1    [1]
  2        0 1 0    [2]
  3        0 1 1    [1, 2]
  4        1 0 0    [3]
  5        1 0 1    [1, 3]
  6        1 1 0    [2, 3]
  7        1 1 1    [1, 2, 3]

submasks of 13 = 1101, each step sub ← (sub - 1) & 1101:
1101 → 1100 → 1001 → 1000 → 0101 → 0100 → 0001 → 0000
e.g. 1100 - 1 = 1011, and & 1101 drops bit 1, which is not in the mask: 1001
```

```pseudo
FUNCTION SubsetsByMask(nums)
    n ← len(nums)
    result ← empty list
    FOR mask FROM 0 TO (1 << n) - 1         // 2^n masks, one per subset
        subset ← empty list
        FOR j FROM 0 TO n - 1
            IF (mask >> j) & 1 = 1          // bit j is set: nums[j] is in
                subset.append(nums[j])
        result.append(subset)
    RETURN result

FUNCTION Submasks(mask)
    result ← empty list
    sub ← mask
    WHILE sub > 0
        result.append(sub)
        sub ← (sub - 1) & mask              // borrow, keep only mask's bits
    result.append(0)                        // the empty submask ends the walk
    RETURN result
```

Listing all subsets costs `O(n · 2^n)`, `2^n` masks with n bit tests each, the same as backtracking. Walking the submasks of one mask costs `O(2^k)`, and walking them for every mask of n bits costs `O(3^n)` in total, because each element is outside the mask, in the mask but not the submask, or in both. Signals: n up to about 20, all subsets, a set used as a key, or states that are sets of chosen items. Count Number of Maximum Bitwise-OR Subsets (LC 2044) runs the plain loop; Number of Valid Words for Each Puzzle (LC 1178) turns every word into a 26-bit letter mask and enumerates the submasks of each puzzle's mask. The classic mistake is testing membership with `mask & j`, which looks at the bits of the number j, instead of `(mask >> j) & 1` or `mask & (1 << j)`: `nums[0]` is then never picked, because `mask & 0` is always 0.

*Practice:* LC 78 Subsets · LC 2044 Count Number of Maximum Bitwise-OR Subsets · LC 1178 Number of Valid Words for Each Puzzle
