---
rank: 103
slug: next_permutation
---

Rearrange an array in place into its next permutation in lexicographic order, the next larger arrangement of the same values when they are compared like words in a dictionary; if the array is already the largest arrangement, wrap around to the smallest, the sorted one. Values may repeat. `[1, 3, 5, 4, 2]` becomes `[1, 4, 2, 3, 5]`, and `[3, 2, 1]` wraps to `[1, 2, 3]`.

The brute force lists the permutations in lexicographic order and returns the one after the input, `O(n · n!)`. The insight is to read the array from the right. A suffix that never rises, such as `5, 4, 2`, is already the largest arrangement of its values, so no reordering inside it can make the array larger, and the change has to reach further left. Walk left while each value is at least its right neighbor and stop at the first `nums[i] < nums[i + 1]`. That `i` is the pivot, the rightmost position that can grow, and because of where the walk stopped, everything after it is non-increasing. If the walk runs off the left end, the whole array never rises: it is the last permutation, and reversing it gives the first.

To grow the pivot by as little as possible, swap it with the smallest suffix value that is larger than it; since the suffix never rises, that is the rightmost value larger than the pivot. The swap leaves the suffix non-increasing, because the values left of `j` are at least the old `nums[j]` and the values right of `j` are at most the pivot. With the pivot raised by the minimum, everything after it must be as small as possible, which means sorted order, and reversing a non-increasing run produces exactly that in `O(n)`, with no sort.

```text
5            ●                 the suffix 5 ≥ 4 ≥ 2 never rises, so it
4                ●             is already the largest order of its
3        ●                     values; the pivot 3 is the rightmost
2                    ●         value that can still grow
1    ●
     0   1   2   3   4   index
         ▲   └───────┘
       pivot  suffix

i = 3: 4 ≥ 2, still falling
i = 2: 5 ≥ 4, still falling
i = 1: 3 < 5, pivot found
j = 4: 2 ≤ 3, keep looking
j = 3: 4 > 3, rightmost value larger than the pivot
swap nums[1] and nums[3]   [1, 4, 5, 3, 2]   the suffix still never rises
reverse nums[2..4]         [1, 4, 2, 3, 5]   now it rises: its smallest order
```

```pseudo
FUNCTION NextPermutation(nums)
    i ← len(nums) - 2
    WHILE i ≥ 0 AND nums[i] ≥ nums[i + 1]       // walk past the falling suffix
        i ← i - 1
    IF i ≥ 0                                    // nums[i] is the pivot
        j ← len(nums) - 1
        WHILE nums[j] ≤ nums[i]                 // rightmost larger value
            j ← j - 1
        swap(nums[i], nums[j])
    Reverse(nums, i + 1, len(nums) - 1)         // falling suffix → rising

FUNCTION Reverse(nums, left, right)
    WHILE left < right
        swap(nums[left], nums[right])
        left ← left + 1
        right ← right - 1
```

Two scans from the right and one reversal make it `O(n)` time and `O(1)` space. Reach for it when a problem wants the next arrangement rather than all of them: the next larger number with the same digits is Next Greater Element III, which returns -1 when the digits never rise or the answer overflows 32 bits, and starting from the sorted array and calling it until it wraps lists every distinct permutation exactly once, duplicates included, without the used array of Permutations (#31). Flipping the two value comparisons, `≥` to `≤` and `≤` to `≥`, gives the previous permutation. The classic mistake is a strict comparison where duplicates need equality. Scanning for `j` with `nums[j] < nums[i]` stops on a value equal to the pivot, so `[1, 5, 1]` becomes `[1, 1, 5]`, a smaller permutation, instead of `[5, 1, 1]`; a strict pivot scan picks the equal pair of `[1, 1]` as a pivot, and the search for `j` runs off the left end.

*Practice:* LC 31 Next Permutation · LC 556 Next Greater Element III · LC 47 Permutations II · LC 60 Permutation Sequence
