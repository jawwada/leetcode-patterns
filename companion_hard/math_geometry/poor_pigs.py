"""
Poor Pigs (LeetCode 458) - Hard
Chapter: math_geometry
Pattern: Information counting (states per pig, mixed-radix labelling)

Exactly one of `buckets` buckets is poisonous. A pig that drinks poison dies minutes_to_die
minutes later; you have minutes_to_test minutes in total and may feed any pigs any buckets
each round. Return the minimum number of pigs that always finds the poisoned bucket.
Example: buckets = 4, minutes_to_die = 15, minutes_to_test = 15 -> 2; (1000, 15, 60) -> 5.
"""


# --- brute force ---
def all_outcomes(pigs, states):
    """Every list of `pigs` entries, each in 0..states-1 (recursive): states^pigs lists."""
    if pigs == 0:
        return [[]]
    result = []
    for first in range(states):
        for rest in all_outcomes(pigs - 1, states):
            result.append([first] + rest)
    return result


def brute_force(buckets, minutes_to_die, minutes_to_test):
    """Try 0, 1, 2, ... pigs; list every outcome vector until there are enough. O(states^pigs)."""
    rounds = minutes_to_test // minutes_to_die
    pigs = 0
    while True:
        outcomes = all_outcomes(pigs, rounds + 1)  # per pig: dies in round 1..T, or survives
        if len(outcomes) >= buckets:               # one distinct outcome per bucket
            return pigs
        pigs += 1


# --- optimal ---
def poor_pigs(buckets, minutes_to_die, minutes_to_test):
    """Each pig ends in one of T+1 states, so p pigs tell (T+1)^p buckets apart. O(log buckets)."""
    states = minutes_to_test // minutes_to_die + 1     # dies in round 1..T, or survives
    pigs = 0
    while states ** pigs < buckets:                    # each pig is one digit in base `states`
        pigs += 1
    return pigs


# --- try the brute force ---
print(brute_force(4, 15, 15))                      # -> 2
print(brute_force(1000, 15, 60))                   # -> 5
print(brute_force(1, 1, 1))                        # -> 0
print(brute_force(125, 1, 4))                      # -> 3


# --- try the optimal ---
print(poor_pigs(4, 15, 15))                        # -> 2
print(poor_pigs(1000, 15, 60))                     # -> 5
print(poor_pigs(1, 1, 1))                          # -> 0
print(poor_pigs(125, 1, 4))                        # -> 3
