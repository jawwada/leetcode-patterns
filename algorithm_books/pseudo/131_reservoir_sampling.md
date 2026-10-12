---
rank: 131
slug: reservoir_sampling
---

A stream delivers items one at a time, and its length `n` is unknown until it ends. Keep a random sample of `k` items in one pass and `O(k)` memory, so that every item ends up in the sample with the same chance `k / n`. For the stream `10, 20, 30, 40, 50` with `k = 2`, each of the five items must be kept two times in five.

Storing the whole stream and choosing at the end costs `O(n)` memory, which a stream too large to store cannot pay. The reservoir keeps the sample current instead: after `i` items it is a uniform sample of those `i`. The first `k` items fill it. From then on item `i` draws `j` uniformly from `1..i` and enters only if `j ≤ k`, which gives it probability `k / i`, exactly its fair share of the first `i`. The same draw names the slot it overwrites, and that slot is uniform over the `k` slots. A newcomer that loses the draw is simply forgotten.

The proof for `k = 1` is a telescoping product. Item `i` wins its own draw with probability `1 / i`. Each later item `m` takes the single slot with probability `1 / m`, so item `i` survives step `m` with probability `(m - 1) / m`. Its chance of being the final answer is `1/i · i/(i + 1) · (i + 1)/(i + 2) · … · (n - 1)/n`, where every numerator cancels the denominator before it, leaving `1 / n` for every `i`. For a general `k`, the newcomer at step `m` evicts one particular slot with probability `k/m · 1/k = 1/m`, so the same product starts at `k / i`, or at `1` for the first `k` items, and ends at `k / n`.

```text
k = 2, stream 10 20 30 40 50, one run with random.seed(0)
  i   item   chance k/i   j = randint(1, i)   j ≤ k?          reservoir
  1    10        -               -            fill            [10]
  2    20        -               -            fill            [10, 20]
  3    30       2/3              2            ✓ into slot 2   [10, 30]
  4    40       2/4              4            ✗ forgotten     [10, 30]
  5    50       2/5              1            ✓ into slot 1   [50, 30]

item 30 lasts to the end: enters 2/3 · survives 3/4 · survives 4/5 = 2/5
20000 runs with random.seed(1), times each item was kept (expected 8000):
  10 → 8145    20 → 7898    30 → 7904    40 → 7953    50 → 8100
```

```pseudo
FUNCTION ReservoirSample(stream, k)
    reservoir ← empty list
    i ← 0
    FOR EACH item IN stream
        i ← i + 1                       // item is the i-th seen (1-based)
        IF i ≤ k
            reservoir.append(item)      // fill phase
        ELSE
            j ← RandomInt(1, i)         // uniform over 1..i
            IF j ≤ k                    // chance k / i
                reservoir[j - 1] ← item  // evict a uniform slot
    RETURN reservoir
```

Each item costs `O(1)` work, so the pass takes `O(n)` time and `O(k)` memory. Reach for it whenever a uniform choice must come from something walked once or of unknown length: Linked List Random Node is `k = 1` over the nodes, and Random Pick Index is `k = 1` over the positions holding the target, so the `c`-th match replaces the pick with probability `1 / c`. The weighted form, where each rectangle enters with probability equal to its point count over the running total, solves Random Point in Non-overlapping Rectangles in one pass, and the same product telescopes. The classic mistake is an off-by-one in the draw: `randint(1, i - 1)` gives item `i` the chance `k / (i - 1)`, and a 0-based `randint(0, i)` gives `k / (i + 1)`, so late items come out over- or under-represented. The uniformity check in the Python book catches both slips.

*Practice:* LC 382 Linked List Random Node · LC 398 Random Pick Index · LC 497 Random Point in Non-overlapping Rectangles
