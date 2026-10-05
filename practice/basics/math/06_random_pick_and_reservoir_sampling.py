"""
Random Pick and Reservoir Sampling - Basics
Area: math
Key operations: keep the first k, item i replaces slot j = randrange(i + 1) when j < k, k = 1 over matching indices

Choose k items uniformly from a stream of unknown length in one pass and O(k) memory: fill the
reservoir with the first k items, then let item i (0-based) replace slot j = randrange(i + 1) if
j < k. Every item ends up in the reservoir with probability k / n. With k = 1 over the indices that
hold a target value this is LeetCode 398 (Random Pick Index): the m-th match wins with probability 1/m.
Example: reservoir_sample(range(10), 3, Random(1)) -> 3 distinct items of 0..9; random_pick([1, 2, 3, 3, 3], 3, Random(1)) -> 2, 3 or 4
"""
import random
from typing import Iterable, List


# --- brute force ---
def brute_force(stream: Iterable[int], k: int, rng: random.Random) -> List[int]:
    """Materialize the whole stream, then random.sample. O(n) memory and the length must be known."""
    items = list(stream)
    return rng.sample(items, min(k, len(items)))


# --- optimal ---
def reservoir_sample(stream: Iterable[int], k: int, rng: random.Random) -> List[int]:
    """Fill the first k slots, then item i replaces slot j = randrange(i + 1) when j < k. O(n) time, O(k) space."""
    reservoir = []
    for i, x in enumerate(stream):
        if i < k:
            reservoir.append(x)
            continue
        j = rng.randrange(i + 1)
        if j < k:
            reservoir[j] = x
    return reservoir


def random_pick(nums: List[int], target: int, rng: random.Random) -> int:
    """Reservoir of size 1 over the matching indices: the m-th match takes over with probability 1/m. O(n), O(1) space."""
    pick, seen = -1, 0
    for i, x in enumerate(nums):
        if x == target:
            seen += 1
            r = rng.randrange(seen)
            if r == 0:
                pick = i
    return pick


# --- demo ---
def demo():
    rng = random.Random(1)
    return reservoir_sample(range(10), 3, rng), random_pick([1, 2, 3, 3, 3], 3, rng)


# --- bugs ---
BUGS = [
    {
        "replace": "        j = rng.randrange(i + 1)",
        "with":    "        j = rng.randrange(i)",
        "fix": "item i is the (i + 1)-th item seen, so it must enter with probability k / (i + 1): randrange(i + 1)",
        "why": "randrange(i) gives item i probability k / i, which is 1 for the first item after the reservoir is full; the early items are then under-represented (about 600 of 3000 instead of 900).",
        "decoys": [
            {"line": "        if i < k:", "change": "should be i <= k"},
            {"line": "            reservoir[j] = x", "change": "should be reservoir.append(x)"},
            {"line": "        if j < k:", "change": "should be j <= k"},
        ],
    },
    {
        "replace": "            r = rng.randrange(seen)",
        "with":    "            r = rng.randrange(seen + 1)",
        "fix": "the m-th match must take over with probability 1/m: randrange(seen) after seen was incremented",
        "why": "The first match is taken only half the time, so the pick can stay -1, and the later matches get 1/(m + 1) instead of 1/m.",
        "decoys": [
            {"line": "            seen += 1", "change": "should come after the if"},
            {"line": "    pick, seen = -1, 0", "change": "should start seen at 1"},
            {"line": "                pick = i", "change": "should be pick = x"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
