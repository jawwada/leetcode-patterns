---
rank: 135
slug: single_number_xor
---

Every element of a non-empty integer array appears exactly twice except one, which appears once; find that one in linear time with constant extra space. In `[4, 1, 2, 1, 2]` the answer is `4`.

Counting with a hash map works but costs `O(n)` space, and sorting to find the element without a twin costs `O(n log n)` time. XOR does it in one pass with one integer, thanks to three facts: `x XOR x = 0`, `x XOR 0 = x`, and XOR is commutative and associative, so the order of the terms does not matter. XOR the whole array together. The terms can be regrouped so that each pair sits side by side, every pair collapses to 0, and the lone element is all that remains. In Python the operator is `^`.

Geometrically, stack the numbers in binary, one per row. XOR works on each bit column separately: a column's result is 1 exactly when it holds an odd number of ones. A pair adds two ones or none to every column, so it never changes a column's parity, and the parities that remain spell out the single number.

```text
               bit 2 1 0   result after the XOR
value 4            1 0 0   100
value 1            0 0 1   101
value 2            0 1 0   111
value 1            0 0 1   110
value 2            0 1 0   100
ones per column    1 2 2   odd, even, even: the single is 100 = 4

missing number in [3, 0, 1], starting from n = 3:
XOR in   i=0  v=3  i=1  v=0  i=2  v=1
result    3    0    1    1    3    2      0, 1 and 3 cancel; 2 is left
```

```pseudo
FUNCTION SingleNumber(nums)
    result ← 0
    FOR EACH value IN nums
        result ← result XOR value          // a pair cancels to 0
    RETURN result

FUNCTION MissingNumber(nums)
    result ← len(nums)                     // index n has no slot of its own
    FOR i FROM 0 TO len(nums) - 1
        result ← result XOR i              // value v cancels against index v
        result ← result XOR nums[i]
    RETURN result
```

One pass, `O(n)` time and `O(1)` space. The same cancellation finds the missing number in an array that holds `0..n` with one value absent (LC 268): XOR every index and every value, starting from n, the one index without a slot; each present value cancels against the index equal to it, wherever it sits, and the missing one has no partner. Find the Difference (LC 389) is the same trick on character codes. When two numbers are single (LC 260), the XOR of everything is `a XOR b`, which is not 0; its lowest set bit (`x & -x`, from #136) is a bit where a and b differ, so splitting the array by that bit puts them in different halves, and XOR-ing each half yields each one. XOR cancels pairs only: when the others appear three times (LC 137), count each bit modulo 3 instead. The classic mistake in Missing Number is starting from 0 instead of n: the result is then the missing value XOR n, so `[3, 0, 1]` gives `1` instead of `2`.

*Practice:* LC 136 Single Number · LC 268 Missing Number · LC 389 Find the Difference · LC 260 Single Number III
