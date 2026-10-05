# Poor Pigs

*LeetCode 458 · Hard · Pattern: Information counting (states per pig, mixed-radix labelling) · Reading time ~8 min*

## The problem

Of buckets buckets of liquid, exactly one is poisonous. A pig that drinks poison dies minutesToDie minutes later; you
have minutesToTest minutes in total and can feed any pigs any buckets at once, wait, then repeat. Return the minimum
number of pigs that guarantees identifying the poisoned bucket.

```text
Example: buckets=4, minutesToDie=15, minutesToTest=15 -> 2;
  buckets=1000, 15, 60 -> 5.
```

## What the problem is really asking

There are `buckets` buckets of liquid and exactly one is poisoned. A pig that drinks poison dies exactly `minutesToDie` minutes later. You have `minutesToTest` minutes in total. In each round you may let any pig drink from any set of buckets (mixing is allowed), then wait `minutesToDie` minutes to see who dies. What is the fewest pigs that *guarantees* identifying the poisoned bucket?

The answer is a small integer. The statement reads like a scheduling or search problem, and that is what makes it hard: people try to design feeding strategies and simulate. The real question is about *information*: how many distinguishable endings can an experiment with `p` pigs have, and is that at least `buckets`?

```text
 buckets = 9, minutesToDie = 15, minutesToTest = 30
   rounds T = 30 // 15 = 2
   [b0][b1][b2][b3][b4][b5][b6][b7][b8]   one is poison
   answer: 2 pigs
```

## Do it by hand first

Start with one round (`T = 1`) and 4 buckets. One pig can drink from some buckets and either dies or not: two outcomes, so it can split 4 buckets into two groups but cannot single one out. Two pigs, each yes/no, give four outcome pairs. Label the buckets in binary and let pig A drink every bucket whose first bit is 1 and pig B every bucket whose second bit is 1:

```text
 T = 1, 4 buckets, 2 pigs
  bucket  bits(A B)  A drinks?  B drinks?   outcome
    0       0 0        no         no        A lives, B lives
    1       0 1        no         yes       A lives, B dies
    2       1 0        yes        no        A dies,  B lives
    3       1 1        yes        yes       A dies,  B dies
 four outcomes, four buckets: each outcome names one bucket
```

Now give the pigs two rounds (`T = 2`) and 9 buckets. A single pig now has *three* possible fates: dies after round 1, dies after round 2, or survives both. Two pigs: `3 * 3 = 9` fate pairs. Nine buckets. It fits exactly — if you can arrange the feeding so each pair of fates points to a different bucket.

What did your hand keep track of? The number of different things that can happen to one pig. That count, not the feeding schedule, is the seed.

## The first honest attempt

Try `p = 0, 1, 2, ...` pigs. For each `p`, enumerate every possible outcome vector — for each pig, "died in round `r`" for `r = 1..T`, or "survived" — with `itertools.product(range(T + 1), repeat=p)`, and count them. Stop at the first `p` whose outcome count is at least `buckets`.

This is correct, but enumerating `(T+1)^p` vectors is exponential in `p`, and for `buckets = 1000` with `T = 4` it builds thousands of tuples just to count them.

Where is the repeated work? Every vector is built only to be counted. The count of a Cartesian product is the product of the factor sizes; listing it is wasted motion.

```text
 enumerate for T = 2, p = 2
   (0,0) (0,1) (0,2)
   (1,0) (1,1) (1,2)      9 tuples built
   (2,0) (2,1) (2,2)
 ...to learn the number 3 * 3 = 9
```

And the deeper question the brute force does not answer: why is "number of outcomes `>= buckets`" the right test at all? That needs two arguments, one for each direction.

## The turning point

**Claim: with `T = minutesToTest // minutesToDie` rounds, each pig ends in one of `T + 1` states, so `p` pigs have `(T+1)^p` outcomes; and `p` pigs suffice if and only if `(T+1)^p >= buckets`.**

**Why each pig has `T + 1` states.** A pig that dies, dies after some specific round. After it dies it is useless, so its whole story is "the round it died in", `1..T`, or "never". That is `T + 1` possibilities. The pigs are independent sensors: one pig's fate does not constrain another's. So `p` pigs have `(T+1)^p` joint outcomes.

**Necessity (lower bound).** Whatever strategy you use, the result you observe at the end is one of those `(T+1)^p` outcome vectors. Each must point to a single bucket, otherwise two buckets produce the same observation and you cannot tell them apart. Two different poisoned buckets therefore need different outcome vectors. So you need at least `buckets` distinct outcomes: `(T+1)^p >= buckets`. This is a pigeonhole argument and holds for *any* clever adaptive scheme.

**Sufficiency (a scheme that meets it).** Number the buckets `0..buckets-1` and write each number in base `T + 1` with `p` digits. Pig `i` is responsible for digit `i`. In round `r` (for `r = 1..T`), pig `i` drinks from every bucket whose digit `i` equals `r`. Buckets whose digit `i` is `0` are never fed to pig `i`.

If the poisoned bucket has digit `i` equal to `d`: when `d = 0`, pig `i` never drinks it and survives; when `d >= 1`, pig `i` drinks it in round `d` and dies after that round, having been perfectly healthy before. So pig `i`'s fate *is* digit `i`. Reading all pigs' fates spells out the bucket's number.

```text
 buckets as a p-dimensional grid of side T+1 (p=2, T=2)
             pig 1 digit (columns) ->
             0       1       2
 pig 0   0  [b0]    [b3]    [b6]
 digit   1  [b1]    [b4]    [b7]
         2  [b2]    [b5]    [b8]
 pig 0 tests ROWS of this picture, pig 1 tests COLUMNS;
 round r = "slice where my digit equals r"
```

So the answer is the smallest `p` with `(T+1)^p >= buckets`: the number of base-`(T+1)` digits needed to write `buckets - 1`. Find it by multiplying in a loop, not with `ceil(log(buckets) / log(T+1))`, because floating-point logs at exact powers (say `125 = 5^3`) can come out as `3.0000000000000004` and round up to the wrong answer.

The mistake to avoid is treating a pig as one bit. With several rounds, *when* it dies carries information; dropping that turns `T + 1` into `2` and overestimates the answer.

## Watch it work

Example: `buckets = 9`, `minutesToDie = 15`, `minutesToTest = 30`. First the counting loop that the solution runs, then the scheme it certifies, with bucket `7` poisoned.

Frame 1 — `states = 30 // 15 + 1 = 3`. Loop: `3^0 = 1 < 9`, `3^1 = 3 < 9`, `3^2 = 9 >= 9`. Answer `2`.

```text
 states = T + 1 = 3
 pigs:      0    1    2
 states^p:  1    3    9   <- first >= 9, return 2
```

Frame 2 — label buckets in base 3 with 2 digits: digit 0 for pig 0, digit 1 for pig 1. Bucket `7 = 2*3 + 1` is `"21"`.

```text
 bucket: 0  1  2  3  4  5  6  7  8
 base3: 00 01 02 10 11 12 20 21 22
          (digit1 digit0)         ^ poison = "21"
```

Frame 3 — round 1. Pig 0 drinks buckets whose digit 0 is 1: `{1, 4, 7}`. Pig 1 drinks those whose digit 1 is 1: `{3, 4, 5}`. Pig 0 drank bucket 7 and dies after round 1; pig 1 survives.

```text
 round 1   pig 0 drinks {1,4,7}  -> DIES  (fate 1)
           pig 1 drinks {3,4,5}  -> lives
 known so far: digit0 = 1, digit1 != 1
```

Frame 4 — round 2. Pig 0 is dead. Pig 1 drinks buckets whose digit 1 is 2: `{6, 7, 8}`. It dies after round 2.

```text
 round 2   pig 0 (dead)           fate 1
           pig 1 drinks {6,7,8} -> DIES  (fate 2)
```

Frame 5 — decode: fates `(pig 1, pig 0) = (2, 1)` is base-3 `"21"` `= 7`. The poisoned bucket is identified.

```text
 fates:   pig1 = 2   pig0 = 1
 bucket = 2 * 3 + 1 = 7      correct
 every bucket 0..8 gives a different fate pair
```

What stayed invariant: after each round, the set of buckets still consistent with what we have observed is a sub-grid where every *dead* pig's digit is fixed and every *living* pig's digit is known not to equal any round already passed. When the rounds are over, every digit is fixed, so the sub-grid is one cell.

## Why it is correct

The loop returns the smallest `p` with `(T+1)^p >= buckets`, since `(T+1)^p` is increasing in `p` (for `T >= 1`).

*No smaller `p` works:* an experiment with `p` pigs ends in one of at most `(T+1)^p` observable outcomes, regardless of the feeding strategy (adaptive or not). If `(T+1)^p < buckets`, two buckets share an outcome by pigeonhole, and when one of those two is poisoned you cannot tell which.

*This `p` works:* the base-`(T+1)` scheme maps each bucket to a distinct digit string, and each pig's fate equals its digit, as argued above. Distinct buckets have distinct digit strings, hence distinct outcomes. The scheme also respects the timing: pig `i` drinks only in rounds `1..T`, each round lasting `minutesToDie`, so `T * minutesToDie <= minutesToTest`.

Edge case: `buckets = 1` needs no test at all, and `(T+1)^0 = 1 >= 1` returns `0`.

## Cost

- **Time:** `O(log buckets)` — the loop runs once per base-`(T+1)` digit, at most about `log2(buckets)` times.
- **Space:** `O(1)`.

The brute force enumerated `(T+1)^p` tuples per candidate `p`, exponential in the answer.

## Variations you will meet

- **Identify one heavier coin with a balance in `w` weighings.** Each weighing has three outcomes (left heavy, right heavy, balanced), so `3^w >= coins`. Same bound, same base-3 labelling.
- **Find one bad item using yes/no group tests (one round).** `T = 1`, two states per tester: `2^p >= n`, i.e. `p = ceil(log2 n)`. This is binary search in disguise, done in parallel.
- **"How many rounds do I need with `p` pigs?"** Invert: the smallest `T` with `(T+1)^p >= buckets`. Same counting, different unknown.
- **Two poisoned buckets.** The outcome count must now be at least `C(buckets, 2)`, and the simple digit scheme fails because two poisoned buckets can mask each other. The lower bound still guides you; constructing a matching scheme is genuinely harder (group-testing designs).

## What to carry forward

For "fewest tests to identify one of `N`", count the outcomes per test, raise to the number of tests, and require at least `N`; label items in that base so each test reads one digit.

The next problem, Max Points on a Line, moves from counting numerals to exact geometry: the job of choosing a canonical label returns, but now the label is a reduced slope that groups collinear points.
