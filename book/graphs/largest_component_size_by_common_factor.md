# Largest Component Size by Common Factor
*LeetCode 952 · Hard · Pattern: Union-Find (disjoint set union) · Reading time ~10 min*

## What the problem is really asking

You get a list of distinct positive integers. Imagine each number as a node, and draw an
edge between two numbers whenever they share a factor larger than 1, that is, whenever
`gcd(a, b) > 1`. Return the size of the largest connected component of that graph.

The answer is one count. What makes it hard is that the graph is never handed to you. It
is implied by arithmetic, and it can be enormous: up to 20,000 numbers means up to 200
million candidate pairs, and the edges can be dense (every even number is joined to every
other even number).

```text
   nums = [4, 6, 15, 35]

   4 --- 6 --- 15 --- 35        4 and 6 share 2
      2     3      5            6 and 15 share 3
                                15 and 35 share 5
   4 and 15? gcd 1, no edge.    one component of size 4
   answer: 4
```

Note that `4` and `35` have nothing in common, yet they are in the same component. The
connection is transitive, through intermediaries. That is exactly what components are.

## Do it by hand first

Take `[20, 50, 9, 63]`. A person does not compute six gcds. They factor each number once
and look for shared primes:

```text
   20 = 2^2 * 5        primes {2, 5}
   50 = 2   * 5^2      primes {2, 5}
    9 = 3^2            primes {3}
   63 = 3^2 * 7        primes {3, 7}

   group by prime:
     2 : 20, 50
     3 : 9, 63
     5 : 20, 50
     7 : 63

   components: {20, 50}  {9, 63}      answer: 2
```

What did your hand keep track of? Not pairs of numbers. It kept, for each **prime**, the
list of numbers that prime divides. Each such list is automatically glued together, and
lists that share a number glue into each other. The primes are acting as meeting points.

## The first honest attempt

Test every pair: if `gcd(nums[i], nums[j]) > 1`, union `i` and `j` in a union-find
forest. At the end, count how many indices share each root and take the maximum.

That is `n(n-1)/2` gcd calls at `O(log max)` each, `O(n^2 log max)` total. For `n = 2*10^4`
it is about 2*10^8 gcds, too slow.

Where is the waste? Look at what each gcd call really computes. To answer "do 20 and 50
share a prime?" it effectively rediscovers the prime structure of 20 and 50. Then "do 20
and 9 share a prime?" rediscovers 20's structure again.

```text
   pairs checked against 20:
     gcd(20, 50) -> learns "20 has 2 or 5" ... yes
     gcd(20,  9) -> learns about 20 again   ... no
     gcd(20, 63) -> learns about 20 again   ... no
                    ^^^^^^^^^^^^^^^^^^^^^
   20's factors {2, 5} never change, but every pair
   containing 20 re-derives them. n-1 times per number.
```

And many unions are redundant even when the gcd is positive. If ten numbers are all even,
the pairwise loop finds 45 edges among them, but nine unions would have been enough.

## The turning point

**Claim: two numbers are adjacent exactly when they share a prime, so the components are
unchanged if we replace every number-number edge with edges from each number to each of
its prime factors.**

Justification. If `gcd(a, b) > 1`, some prime `p` divides both, so `a - p - b` is a path in
the new graph. Conversely, a path in the new graph alternates number, prime, number,
prime..., and each consecutive pair of numbers `a - p - b` shares `p`, so `gcd(a, b) > 1`
and they were adjacent in the original graph. Paths map to paths in both directions, so
the components restricted to the input numbers are identical.

```text
   original (pairwise)          rewritten (through hubs)

   20 ----- 50                  20 ---- [2] ---- 50
                                  \             /
                                   `--- [5] ---'
    9 ----- 63
                                   9 ---- [3] ---- 63
                                                   |
                                                  [7]
```

This changes the cost completely. A number up to `10^5` has at most six distinct prime
factors, so the new graph has at most `6n` edges instead of up to `n^2 / 2`. And we never
need to compare two numbers at all. Each number is factored once, on its own.

Turning the claim into an algorithm:

1. Union-find over a dictionary, so nodes appear lazily. Both numbers and primes are
   nodes. (A number that happens to be prime, like `5`, and the hub `5` share one key.
   That is harmless: the number 5 is divisible by the prime 5 and would be joined to that
   hub anyway.)
2. For each number `x`, factor by trial division: try `p = 2, 3, 4, ...` while
   `p * p <= rem`. When `p` divides `rem`, union `x` with `p` and strip every copy of `p`
   from `rem`. Stripping guarantees that only primes ever divide `rem` at this point,
   because any composite `p` has a smaller prime factor that was already stripped.
3. After the loop, if `rem > 1` it is one leftover prime larger than the square root.
   Union `x` with it too. Forgetting this is the classic bug: in `6`, the factor 3 is only
   found here, because `3 * 3 > 3` ends the loop.
4. Count `find(x)` over the **input numbers only**. Hubs are scaffolding; they must not
   inflate a component's size.

The idea to keep: when "related" means "shares an attribute", do not compare items with
items. Create one node per attribute and connect each item to its attributes. You met this
already in Accounts Merge, where emails were the hubs; here the hubs are primes.

## Watch it work

`nums = [4, 6, 15, 35]`. The solution unions with `parent[find(a)] = find(b)`, so the hub
side becomes the root. Frames show the parent map, with `->` meaning "parent is".

```text
Frame 1   x = 4: p=2 divides -> union(4, 2)
          strip: rem 4 -> 2 -> 1, loop ends
   parent:  4->2   2->2
```
`4` hangs under hub `2`; no leftover since `rem` reached 1.

```text
Frame 2   x = 6: p=2 divides -> union(6, 2), rem = 3
          3 > 1 leftover -> union(6, 3)
          find(6) = 2, so parent[2] = 3
   parent:  4->2  6->2  2->3  3->3
```
The leftover prime 3 was only caught after the loop; hub `2` now sits under hub `3`.

```text
Frame 3   x = 15: p=3 divides -> union(15, 3), rem = 5
          5 > 1 leftover -> union(15, 5)
          find(15) = 3, so parent[3] = 5
   parent:  4->2  6->2  2->3  15->3  3->5  5->5
```
The 2-group and the 3-group are now one tree rooted at hub `5`.

```text
Frame 4   x = 35: p=5 divides -> union(35, 5), rem = 7
          7 > 1 leftover -> union(35, 7)
          find(35) = 5, so parent[5] = 7
   parent:  4->2  6->2  2->3  15->3  3->5
            35->5  5->7  7->7
```
Every node, numbers and hubs, now leads to root `7`.

```text
Frame 5   count roots over nums only
   find(4)=7  find(6)=7  find(15)=7  find(35)=7
   counts: {7: 4}          hubs 2,3,5,7 not counted
   answer: 4
```
Path halving shortened some chains during these finds, but every root is `7`.

Invariant across the frames: the numbers sharing a root are exactly the numbers connected
so far through primes discovered so far. No number was ever compared to another number.

## Why it is correct

The path-mapping argument in "The turning point" shows the hub graph and the gcd graph
have the same components over the input numbers. The algorithm builds exactly the hub
graph: trial division with stripping finds every distinct prime factor of `x` (those up
to `sqrt(x)` in the loop, and at most one larger one as the leftover, since two primes
both above `sqrt(x)` would multiply past `x`). Each such edge is fed to union-find, whose
invariant is that two nodes share a root exactly when the edges seen so far connect them.
After all numbers are processed, the roots are the components of the hub graph, and
counting roots over the inputs alone gives the component sizes the problem defines.

The number `1` has no prime factors, gets no unions, and `find(1)` simply creates it as a
singleton, which is right: `gcd(1, anything) = 1`.

## Cost

- **Time `O(n * sqrt(M) * alpha)`** with `M = max(nums)`: each number is trial-divided up
  to its square root (about 316 steps for `10^5`), and does at most six unions.
- **Space `O(n + P)`**: the parent map holds the numbers plus the distinct primes `P` that
  actually appear.
- **Faster factoring**: precompute a smallest-prime-factor sieve up to `M` in
  `O(M log log M)`; then each number factors in `O(log M)` by repeated division by its
  smallest prime factor, giving `O(M log log M + n log M)` overall.

## Variations you will meet

- **Return the component, not its size.** Same forest; group the inputs by root at the end.
- **Greatest Common Divisor Traversal (LeetCode 2709).** Ask whether *all* indices are in
  one component. Same hub trick, then check that every input has the same root. Watch for
  `1`, which isolates itself unless it is the only element.
- **Edges when two numbers share a divisor `> threshold` (LeetCode 1627).** Hubs become the
  divisors above the threshold; for each `d`, union all its multiples `d, 2d, 3d, ...`. The
  harmonic sum makes this `O(n log n)`.
- **Items sharing any tag or attribute** (users sharing a phone number, documents sharing a
  keyword). Same move: one hub per attribute value, union item to hub.

## What to carry forward

When items connect by "having something in common", union each item to a hub for that
something and count only the real items under each root. The next problem keeps
union-find but adds time: unions that happen at one moment may have to be undone before
the next.
