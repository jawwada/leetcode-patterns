---
rank: 3
slug: product_of_array_except_self
---

Given an integer array, return an array whose entry `i` is the product of every element except `nums[i]`, without using division. For `[1, 2, 3, 4]` the answer is `[24, 12, 8, 6]`; entry 2, for one, is `1 × 2 × 4 = 8`.

The brute force multiplies the other `n - 1` numbers for every index, `O(n²)` work. Dividing the total product by `nums[i]` looks like a shortcut, but a single zero wrecks it: the total becomes 0, and at the zero's own index the division is by zero. The insight is that "everything except `i`" is two unbroken blocks, the elements left of `i` and the elements right of `i`. So `answer[i]` is a prefix product times a suffix product, and a running product delivers every prefix product in one left-to-right pass and every suffix product in one right-to-left pass.

The output array doubles as the prefix table, which is where the `O(1)` extra space comes from. The first pass writes the running `prefix` into `answer[i]` before multiplying `nums[i]` into `prefix`, so each entry holds exactly the product of the elements strictly to its left. The second pass starts a running `suffix` at the right end, multiplies it into `answer[i]`, and only then absorbs `nums[i]`. Picture two waves crossing the array from opposite ends, each leaving one factor behind at every index. Zeros and negatives need no special case, because nothing is ever divided: a zero simply zeroes every block that contains it, so with one zero every entry except the zero's own is 0, and with two zeros every entry is 0.

```text
nums                    1             2            3            4
left of i               (empty) 1     1            1×2 = 2      1×2×3 = 6
right of i              2×3×4 = 24    3×4 = 12     4            (empty) 1
answer = left × right   24            12           8            6

pass 1, left to right                 pass 2, right to left
 i   answer[i] ← prefix   new prefix    i   answer[i] × suffix   new suffix
 0            1                1        3      6 × 1  = 6             4
 1            1                2        2      2 × 4  = 8            12
 2            2                6        1      1 × 12 = 12           24
 3            6               24        0      1 × 24 = 24           24
answer [1, 1, 2, 6]                   answer [24, 12, 8, 6]
```

```pseudo
FUNCTION ProductExceptSelf(nums)
    n ← len(nums)
    answer ← array of n copies of 1
    prefix ← 1                             // product of nums[0..i-1]
    FOR i FROM 0 TO n - 1
        answer[i] ← prefix                 // everything left of i
        prefix ← prefix * nums[i]          // only now let nums[i] in
    suffix ← 1                             // product of nums[i+1..n-1]
    FOR i FROM n - 1 DOWNTO 0              // right to left
        answer[i] ← answer[i] * suffix     // times everything right of i
        suffix ← suffix * nums[i]
    RETURN answer
```

Two linear passes give `O(n)` time, and besides the output only `prefix` and `suffix` are kept, `O(1)` extra space. Reach for prefix and suffix accumulations whenever the answer at a position combines everything on its left with everything on its right: the same two sweeps build the wall arrays of Trapping Rain Water (#9) and hand out the candies of #111, and with sums in place of products they find the pivot index whose left sum equals its right sum. The classic mistake is multiplying `nums[i]` into `prefix` before writing `answer[i]`, which leaves every element inside its own product: on the example the first pass writes `[1, 2, 6, 24]`, and the answer comes out `[24, 24, 24, 24]`.

*Practice:* LC 238 Product of Array Except Self · LC 724 Find Pivot Index · LC 42 Trapping Rain Water · LC 1352 Product of the Last K Numbers
