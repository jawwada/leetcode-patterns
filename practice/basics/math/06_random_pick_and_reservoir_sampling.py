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
import sys
import random
from typing import Iterable, List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(stream: Iterable[int], k: int, rng: random.Random) -> List[int]:
    """Materialize the whole stream, then random.sample. O(n) memory and the length must be known."""
    items = list(stream)
    return rng.sample(items, min(k, len(items)))


# --- optimal ---
def reservoir_sample(stream: Iterable[int], k: int, rng: random.Random) -> List[int]:
    """Fill the first k slots, then item i replaces slot j = randrange(i + 1) when j < k. O(n) time, O(k) space."""
    reservoir = []
    log(f"reservoir_sample(k={k}):")
    for i, x in enumerate(stream):
        if i < k:
            reservoir.append(x)
            log(f"  i={i} x={x}: {'fill slot %d' % i:<24} -> {reservoir}")
            continue
        j = rng.randrange(i + 1)
        if j < k:
            reservoir[j] = x
        log(f"  i={i} x={x}: j={j} {'< k, replace slot %d' % j if j < k else '>= k, keep':<20} -> {reservoir}")
    return reservoir


def random_pick(nums: List[int], target: int, rng: random.Random) -> int:
    """Reservoir of size 1 over the matching indices: the m-th match takes over with probability 1/m. O(n), O(1) space."""
    pick, seen = -1, 0
    log(f"random_pick(target={target}):")
    for i, x in enumerate(nums):
        if x == target:
            seen += 1
            r = rng.randrange(seen)
            if r == 0:
                pick = i
            log(f"  match #{seen} at index {i}: drew {r} of 0..{seen - 1} -> {'take over' if r == 0 else 'keep'}, pick = {pick}")
    return pick


# --- demo ---
def demo():
    rng = random.Random(1)
    return reservoir_sample(range(10), 3, rng), random_pick([1, 2, 3, 3, 3], 3, rng)


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # keep the trace to the demo
    rng = random.Random(0)
    assert reservoir_sample([], 3, rng) == []
    assert reservoir_sample([7, 8], 3, rng) == [7, 8]        # fewer items than k: keep them all, in order
    assert reservoir_sample(range(5), 0, rng) == []
    assert random_pick([1, 2, 3], 9, rng) == -1 and random_pick([5], 5, rng) == 0
    for _ in range(50):
        s = reservoir_sample(range(10), 3, rng)
        assert len(s) == 3 and len(set(s)) == 3 and set(s) <= set(range(10)), s
    # every item must land in the reservoir about k/n of the time; the brute force must pass the same check
    trials, k, n = 3000, 3, 10
    expect, tol = trials * k / n, 100                        # 900 +- 100, about 4 standard deviations
    for method in (reservoir_sample, brute_force):
        rng = random.Random(42)
        counts = [0] * n
        for _ in range(trials):
            for x in method(range(n), k, rng):
                counts[x] += 1
        assert all(abs(c - expect) <= tol for c in counts), (method.__name__, counts)
    rng = random.Random(7)
    picks = [0] * 5
    for _ in range(trials):
        p = random_pick([1, 2, 3, 3, 3], 3, rng)
        assert p in (2, 3, 4), p
        picks[p] += 1
    assert all(abs(c - trials / 3) <= tol for c in picks[2:]), picks


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
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
