"""
Reservoir Sampling - Keep the i-th Item with Probability k / i

Choose k items uniformly at random from a stream of unknown length, in one
pass with O(k) memory, so that every item is kept with the same chance k / n:
stream 10, 20, 30, 40, 50 with k = 2 -> each item kept 2 / 5 of the time.
"""
import random                           # randint(a, b) includes both ends


# --- algorithm ---
def reservoir_sample(stream, k):
    """Keep the first k items; item i then replaces a random slot with
    probability k / i. O(n) time, O(k) space."""
    reservoir = []
    i = 0
    for item in stream:
        i += 1                          # item is the i-th seen (1-based)
        if i <= k:
            reservoir.append(item)      # fill phase
        else:
            j = random.randint(1, i)    # uniform over 1..i
            if j <= k:                  # chance k / i
                reservoir[j - 1] = item  # evict a uniform slot
    return reservoir


def is_uniform(stream, k, trials):
    """Each item should be kept about trials * k / n times. O(trials * n)."""
    counts = {}
    for t in range(trials):
        sample = reservoir_sample(stream, k)
        for item in sample:
            counts[item] = counts.get(item, 0) + 1
    expected = trials * k / len(stream)
    for item in stream:
        if abs(counts.get(item, 0) - expected) > 0.1 * expected:
            return False                # more than 10 percent off
    return True


# --- try it ---
random.seed(7)
print(len(reservoir_sample(range(1000), 10)))           # -> 10
print(reservoir_sample([7, 8, 9], 5))                   # -> [7, 8, 9]
print(is_uniform([10, 20, 30, 40, 50], 2, 20000))       # -> True
print(is_uniform([1, 2, 3, 4, 5, 6, 7, 8], 1, 20000))   # -> True
