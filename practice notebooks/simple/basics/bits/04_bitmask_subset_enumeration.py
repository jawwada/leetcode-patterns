"""
Bitmask Subset Enumeration (basics: bits)
List every subset of n items using the numbers 0 .. 2^n - 1, and every submask of a mask.
  ['a', 'b', 'c']  ->  [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]

Idea: a subset of n items is an n-bit mask (bit i set = items[i] is in), so counting
      0 .. 2^n - 1 visits every subset once. For submasks, (sub - 1) & mask is the largest
      submask below sub, so the walk goes 1010 -> 1000 -> 0010 -> 0000 (10, 8, 2, 0).

Pseudocode:
  subsets(items):
      for mask in 0 .. 2^n - 1:
          record [items[i] for each i whose bit is set in mask]
  submasks(mask):
      sub = mask
      while sub != 0: record sub; sub = (sub - 1) & mask
      record 0

Time O(n * 2^n) for subsets, O(2^k) for submasks (k = set bits in mask); space O(1) besides the output.
"""


def subsets(items):
    n = len(items)
    result = []
    for mask in range(1 << n):           # 2^n masks, one per subset
        chosen = []
        for i in range(n):
            if (mask >> i) & 1:          # bit i set: items[i] is in
                chosen.append(items[i])
        result.append(chosen)
    return result


def submasks(mask):
    result = []
    sub = mask                           # a mask is its own largest submask
    while sub:
        result.append(sub)
        sub = (sub - 1) & mask           # next smaller submask
    result.append(0)                     # the empty submask ends the walk
    return result


if __name__ == "__main__":
    print(subsets(["a", "b", "c"]))  # [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
    print(submasks(0b1010))          # [10, 8, 2, 0]
    print(submasks(0b111))           # [7, 6, 5, 4, 3, 2, 1, 0]
