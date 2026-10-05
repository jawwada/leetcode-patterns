"""
Random Pick and Reservoir Sampling - Fundamentals
Chapter: fundamentals/math
Key operations: keep the first k, item i replaces slot j = randrange(i + 1) when j < k, k = 1 pick

Choose k items uniformly from a stream of unknown length in one pass and O(k) memory: fill the
reservoir with the first k items, then let item i (0-based) replace slot j = randrange(i + 1) if
j < k. Every item ends up in the reservoir with probability k / n. With k = 1 over the indices that
hold a target value this is LeetCode 398 (Random Pick Index): the m-th match wins with chance 1/m.
Example: reservoir_sample(0..9, 3) -> three of 0..9; random_pick_index([1, 2, 3, 3, 3], 3) -> 2-4
"""
import random


# --- algorithm ---
def reservoir_sample(stream, k, rng):
    """Fill the first k slots; item i replaces slot j = randrange(i + 1) when j < k. O(n), O(k)."""
    reservoir = []
    i = 0
    for item in stream:
        if i < k:
            reservoir.append(item)
        else:
            j = rng.randrange(i + 1)      # item i is the (i + 1)-th seen: chance k / (i + 1)
            if j < k:
                reservoir[j] = item
        i += 1
    return reservoir


def random_pick_index(nums, target, rng):
    """Reservoir of size 1 over the matching indices: the m-th match wins with chance 1/m. O(n)."""
    pick = -1
    seen = 0
    for i in range(len(nums)):
        if nums[i] == target:
            seen += 1
            if rng.randrange(seen) == 0:  # randrange(seen) after the increment: 1st match wins
                pick = i
    return pick


# --- try it ---
rng = random.Random(1)
print(reservoir_sample(list(range(10)), 3, rng))         # -> [5, 7, 6]
print(random_pick_index([1, 2, 3, 3, 3], 3, rng))        # -> 4
print(reservoir_sample([7, 8, 9], 5, rng))               # -> [7, 8, 9]
print(random_pick_index([1, 2, 3], 2, rng))              # -> 1
