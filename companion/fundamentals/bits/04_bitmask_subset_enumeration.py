"""
Bitmask Subset Enumeration - Fundamentals
Chapter: fundamentals/bits
Key operations: masks 0..2^n-1 = subsets, mask >> i & 1 tests item i, (sub-1) & mask = next submask

A subset of n items is an n-bit mask: bit i set means items[i] is in. Counting the masks 0..2^n-1
visits every subset once. To list every subset of a given mask (its submasks), start at the mask
and repeat sub = (sub - 1) & mask: subtracting 1 borrows through the mask's bits only, so each
step lands on the next smaller submask, and the walk ends at 0.
Example: [a, b, c] -> 8 subsets from [] (000) to [a, b, c] (111);
         submasks of 1010 -> [1010, 1000, 0010, 0000]
"""


# --- algorithm ---
def subsets_by_bitmask(items):
    """Each mask in 0..2^n - 1 is a subset; bit i says whether items[i] is in. O(2^n * n)."""
    n = len(items)
    out = []
    for mask in range(1 << n):   # 1 << n is 2^n: one mask per subset
        chosen = []
        for i in range(n):
            if (mask >> i) & 1:   # bit i of the mask is set: items[i] is in this subset
                chosen.append(items[i])
        out.append(chosen)
    return out


def submasks(mask):
    """Walk sub = (sub - 1) & mask from mask down to 0: every submask once, decreasing. O(2^k)."""
    out = []
    sub = mask
    while sub:
        out.append(sub)
        sub = (sub - 1) & mask   # the & keeps the borrow inside the mask's own bits
    out.append(0)   # 0 is a submask too; the loop stops before recording it
    return out


# --- try it ---
print(subsets_by_bitmask(["a", "b", "c"]))
# -> [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
print(subsets_by_bitmask(["x"]))      # -> [[], ['x']]
print(subsets_by_bitmask([]))         # -> [[]]
print(submasks(0b1010))               # -> [10, 8, 2, 0]   (1010, 1000, 0010, 0000)
print(submasks(0b111))                # -> [7, 6, 5, 4, 3, 2, 1, 0]
print(submasks(0))                    # -> [0]
