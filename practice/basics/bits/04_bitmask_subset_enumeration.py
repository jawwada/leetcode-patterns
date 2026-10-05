"""
Bitmask Subset Enumeration - Basics
Area: bits
Key operations: masks 0..2^n - 1 are the subsets, mask >> i & 1 tests item i, sub = (sub - 1) & mask walks the submasks

A subset of n items is an n-bit mask: bit i set means items[i] is in. Counting the masks 0..2^n - 1
visits every subset once. To list every subset of a given mask (its submasks), start at the mask and
repeat sub = (sub - 1) & mask: subtracting 1 borrows through the mask's bits only, so each step lands
on the next smaller submask, and the walk ends at 0.
Example: ['a', 'b', 'c'] -> 8 subsets from [] (000) to ['a', 'b', 'c'] (111); submasks of 1010 -> [1010, 1000, 0010, 0000]
"""
from itertools import combinations
from typing import List


# --- brute force ---
def brute_force(items: List[str]) -> List[tuple]:
    """Every combination of every size, via itertools. O(2^n) subsets, no bit tricks."""
    return sorted(c for r in range(len(items) + 1) for c in combinations(items, r))


def brute_submasks(mask: int) -> List[int]:
    """Try every number up to mask and keep those whose bits all lie inside it. O(mask) instead of O(2^k)."""
    return [s for s in range(mask + 1) if s & mask == s]


# --- optimal ---
def subsets(items: List[str]) -> List[List[str]]:
    """Each mask in 0..2^n - 1 is a subset; bit i of the mask says whether items[i] is in. O(2^n * n)."""
    n = len(items)
    out = []
    for mask in range(1 << n):
        chosen = [items[i] for i in range(n) if mask >> i & 1]
        out.append(chosen)
    return out


def submasks(mask: int) -> List[int]:
    """Walk sub = (sub - 1) & mask from mask down to 0: every submask once, in decreasing order. O(2^k) for k set bits."""
    out = []
    sub = mask
    while sub:
        out.append(sub)
        sub = (sub - 1) & mask
    out.append(0)
    return out


# --- demo ---
def demo():
    return subsets(["a", "b", "c"]), submasks(0b1010)


# --- bugs ---
BUGS = [
    {
        "replace": "    for mask in range(1 << n):",
        "with":    "    for mask in range((1 << n) - 1):",
        "fix": "there are 2^n subsets, masks 0 .. 2^n - 1, so iterate range(1 << n)",
        "why": "range already stops before its end, so the all-ones mask (the full set) is never produced: ['a', 'b', 'c'] yields 7 subsets.",
        "decoys": [
            {"line": "        chosen = [items[i] for i in range(n) if mask >> i & 1]", "change": "should test mask >> i & i"},
            {"line": "        out.append(chosen)", "change": "should append mask"},
            {"line": "    sub = mask", "change": "should start at mask - 1"},
        ],
    },
    {
        "replace": "        chosen = [items[i] for i in range(n) if mask >> i & 1]",
        "with":    "        chosen = [items[i] for i in range(n) if mask & i]",
        "fix": "test bit i with mask >> i & 1 (or mask & (1 << i)); i itself is a position, not a mask",
        "why": "mask & i mixes a position with a bit pattern: for ['a', 'b'] mask 1 picks ['b'] and mask 2 picks ['b'] again, so subsets are wrong and repeated.",
        "decoys": [
            {"line": "    for mask in range(1 << n):", "change": "should be range(n << 1)"},
            {"line": "        sub = (sub - 1) & mask", "change": "should be (sub - 1) | mask"},
            {"line": "    out.append(0)", "change": "should append mask"},
        ],
    },
    {
        "replace": "    sub = mask",
        "with":    "    sub = mask - 1",
        "fix": "the walk starts at the mask itself, which is its own largest submask",
        "why": "Starting one below skips the full mask: submasks(0b1010) returns [0b1000, 0b0010, 0] and submasks(0) starts at -1.",
        "decoys": [
            {"line": "    while sub:", "change": "should be while sub > 1"},
            {"line": "        out.append(sub)", "change": "should append sub & mask"},
            {"line": "    n = len(items)", "change": "should be len(items) - 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
