"""
Random Pick and Reservoir Sampling (basics: math)
Pick k items uniformly from a stream of unknown length in one pass; random_pick is the k = 1 case.
  reservoir_sample(range(10), 3)  ->  3 distinct items, each one kept with probability 3/10

Idea: keep the first k items. Item i (0-based) then draws a random slot j in 0..i and
      replaces reservoir[j] only if j < k, so it gets in with probability k / (i + 1).
      That works out to every item ending up in the sample with probability k / n.

Pseudocode:
  reservoir_sample(stream, k):
      for i, x in stream:
          if i < k: reservoir.append(x)
          else: j = random int in 0..i; if j < k: reservoir[j] = x
  random_pick(nums, target):                   # a reservoir of size 1 over the matches
      seen = 0, pick = -1
      for i, x in nums:
          if x == target:
              seen += 1
              with probability 1 / seen: pick = i    (randrange(seen) == 0)

Time O(n), space O(k) (O(1) for random_pick).
"""
import random


def reservoir_sample(stream, k):
    reservoir = []
    for i, x in enumerate(stream):
        if i < k:                        # the first k items go straight in
            reservoir.append(x)
        else:
            j = random.randrange(i + 1)  # random slot 0..i
            if j < k:                    # true with probability k / (i + 1)
                reservoir[j] = x
    return reservoir


def random_pick(nums, target):
    pick, seen = -1, 0
    for i, x in enumerate(nums):
        if x == target:
            seen += 1                    # this is match number `seen`
            if random.randrange(seen) == 0:  # keep it with probability 1 / seen
                pick = i
    return pick


if __name__ == "__main__":
    random.seed(1)                           # fixed seed, so the output repeats
    print(reservoir_sample(range(10), 3))    # [5, 7, 6]
    print(random_pick([1, 2, 3, 3, 3], 3))   # 4
    print(reservoir_sample(range(3), 5))     # [0, 1, 2]
