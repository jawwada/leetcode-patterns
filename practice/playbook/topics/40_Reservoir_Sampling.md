## Reservoir Sampling

Keep a uniformly random sample from a stream whose final length is unknown, using only O(k) storage for a sample of size k.

<!-- cell -->

The third recipe is random sampling. Reservoir sampling picks k items uniformly from a stream too long to store: keep the first k, and after that item i, counting from 0, replaces a random member with probability k/(i+1). With k = 1 it is the random pick behind Linked List Random Node, a uniformly random node of a list of unknown length, and Random Pick Index, a random index among the copies of a target value.

Why that is uniform: item i gets in with probability k/(i+1), and each later item j removes it with probability (k/(j+1)) · (1/k) = 1/(j+1), so it survives item j with probability j/(j+1). The product k/(i+1) · (i+1)/(i+2) · ... · (n−1)/n telescopes to k/n. The cell samples 2 of `range(5)` ten thousand times, so each value should be picked about 10 000 · 2/5 = 4000 times.

<!-- cell -->

```python
def reservoir_sample(stream, k):
    sample = []
    for i, x in enumerate(stream):
        if i < k:
            sample.append(x)                   # the first k fill the reservoir
        else:
            j = random.randrange(i + 1)        # a uniform slot in 0..i
            if j < k:                          # happens with probability k / (i + 1)
                sample[j] = x                  # replace a uniformly chosen member
    return sample


random.seed(0)
hits = Counter()
for _ in range(10_000):
    hits.update(reservoir_sample(range(5), 2))
print(sorted(hits.items()))   # [(0, 3990), (1, 3927), (2, 4004), (3, 4035), (4, 4044)]: all near 4000
```

<!-- cell -->

**Try it**
- Change `random.randrange(i + 1)` to `random.randrange(i)` and rerun the cell: values 2, 3 and 4 now show up about 5000 times and 0 and 1 about 2500. Item 2 always gets in, since `j` can only be 0 or 1.
- Use `k = 1` on `range(3)` for 9000 runs: each value about 3000 times. That is random pick.
- `reservoir_sample(range(3), 5)`: `[0, 1, 2]`. With fewer items than k, you simply get them all.
