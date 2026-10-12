"""
Bitmask Subset Enumeration - Every Integer from 0 to 2^n - 1 Is a Subset

List every subset of n distinct elements by counting in binary (bit j of the
mask says whether element j is in), and list every submask of a mask:
[1, 2, 3] -> [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]].
"""


# --- algorithm ---
def subsets_by_mask(nums):
    """Mask m picks nums[j] when bit j of m is set. O(n * 2^n)."""
    n = len(nums)
    result = []
    for mask in range(1 << n):          # 1 << n is 2^n: one mask per subset
        subset = []
        for j in range(n):
            if (mask >> j) & 1:         # bit j is set: nums[j] is in
                subset.append(nums[j])
        result.append(subset)
    return result


def submasks(mask):
    """Every submask of mask, largest first. O(2^k) for k set bits."""
    result = []
    sub = mask
    while sub > 0:
        result.append(sub)
        sub = (sub - 1) & mask          # borrow, then keep only mask's bits
    result.append(0)                    # the empty submask ends the walk
    return result


# --- try it ---
result = subsets_by_mask([1, 2, 3])
print(result)   # -> [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
print(subsets_by_mask([]))              # -> [[]]
print(submasks(13))                     # -> [13, 12, 9, 8, 5, 4, 1, 0]
print(submasks(0))                      # -> [0]
