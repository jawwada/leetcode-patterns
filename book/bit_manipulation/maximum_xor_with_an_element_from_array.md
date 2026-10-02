# Maximum XOR With an Element From Array

*LeetCode 1707 · Hard · Pattern: Offline queries + binary trie (max XOR) · Reading time ~11 min*

## What the problem is really asking

You get an array `nums` and a list of queries `[x, m]`. For each query, look only at the elements of `nums` that are at most `m`. Among those, find the one whose XOR with `x` is largest, and report that XOR. If no element is at most `m`, report -1. Answers go back in the original query order.

Both lists can hold 10^5 entries, and values are below 10^9 < 2^30, so 30 bits.

There are two separate difficulties tangled together:

1. **Maximising XOR** over a set is not a sort-and-scan problem. The number closest to `x`, the largest number and the smallest number are all unreliable guides. XOR rewards disagreement in high bits, not closeness.
2. **The bound `m`** changes the allowed set from query to query.

```text
nums = [0, 1, 2, 3, 4]
queries = [[3,1], [1,3], [5,6]]

query [5, 6]: allowed {0,1,2,3,4}
  5^0=5  5^1=4  5^2=7  5^3=6  5^4=1   -> 7
answers: [3, 3, 7]
```

## Do it by hand first

Take the query `x = 5 = 101` and the allowed set `{0..4}`. Write them in binary. How would you pick the best partner without trying all five?

```text
x = 1 0 1
     want a partner that is:
     0 in col 2 (to get a 1 there)  -> 000 001 010 011
     1 in col 1                      -> 010 011
     0 in col 0                      -> 010
partner = 010 = 2,  5 ^ 2 = 111 = 7
```

You went column by column from the **top**, and in each column asked: "is there still a candidate that disagrees with `x` here?" If so, you kept only those candidates. A 1 in column 2 is worth 4, more than columns 1 and 0 together (2 + 1 = 3). So winning a high column is always worth losing every lower one.

What your hand kept track of was **the set of candidates that share the chosen top bits**, narrowing one column at a time. A structure that answers "among numbers with these top bits, does any have bit `b` = 1?" in O(1) is a binary trie.

## The first honest attempt

For each query, scan `nums`, skip elements above `m`, and track the max of `x ^ v`.

```text
query [3,1]: scan 0 1 2 3 4  (filter <=1)  try 0,1
query [1,3]: scan 0 1 2 3 4  (filter <=3)  try 0,1,2,3
query [5,6]: scan 0 1 2 3 4  (filter <=6)  try all
             filters are nested: {<=1} c {<=3} c {<=6}
             yet each query re-filters from scratch
```

That is O(n · q) = 10^10. There are two kinds of repeated work.

- **XOR maximisation by enumeration.** Each query tries every allowed element, although a greedy over 30 bits would find the best one.
- **Re-filtering.** The allowed sets for increasing `m` are nested. Each one is a prefix of `nums` once sorted, yet each query rebuilds its set from scratch.

Each kind of waste has its own fix.

## The turning point

**Claim 1: with all numbers stored in a binary trie (top bit first), the max XOR partner of `x` is found by walking down and taking the child opposite to `x`'s bit whenever it exists.**

A binary trie stores each number as a root-to-leaf path. Level `b` corresponds to bit `b`, from bit 29 at the top to bit 0 at the leaves. The left edge means 0 and the right edge means 1. Numbers that share their top bits share the top of their paths. In memory it is just `child[node] = [left, right]` with 0 meaning "absent", since node 0 is the root and never anyone's child.

The greedy walk: at level `b`, let `want = 1 - bit_b(x)`. If `child[node][want]` exists, go there and set bit `b` of the answer. Otherwise take the only existing child and leave bit `b` at 0. That is 30 steps per query, instead of n.

Why greedy is safe: the answer's bit `b` is worth `2^b`, and all lower bits together are worth at most `2^b - 1`. So any partner that makes bit `b` a 1 beats every partner that makes it a 0, whatever happens below. Decide the top bit, never regret it. That is exactly lexicographic maximisation, and the trie offers exactly the lexicographic choice at each node.

**Claim 2: if we answer queries in increasing order of `m` and insert numbers in increasing order, the trie at each query holds exactly the allowed numbers.**

The trie cannot easily "ignore numbers above `m`" during a walk. It can, however, *not contain them yet*. Sort `nums`. Sort the query indices by `m`. Sweep: before answering a query, insert every `nums[i] <= m` not yet inserted. Since `m` only increases, the trie only grows, and each number is inserted once. If nothing has been inserted yet, the answer is -1.

This is the **offline** trick: we are allowed to see all queries up front, so we choose the order that makes the data structure's life easy. We then write each answer back to its original index.

```text
sweep over sorted m:

nums sorted : 0  1  2  3  4
              |--|            m=1: trie = {0,1}
              |--------|      m=3: trie = {0,1,2,3}
              |-----------|   m=6: trie = {0,1,2,3,4}
pointer i only moves right
```

## Watch it work

The real trie has 30 levels, but every value here is below 8, so bits 29..3 are all 0 and form one shared chain from the root. We draw only the bottom three levels, bits 2, 1, 0. Left = 0, right = 1.

```text
Frame 1   sort
  nums = [0,1,2,3,4]
  queries by m: q0 [3,1], q1 [1,3], q2 [5,6]
  ans = [-1,-1,-1]   i = 0   trie empty
```
Sorting turns the per-query filter into a pointer that only moves right.

```text
Frame 2   q0: x=3 (011), m=1   insert 0, 1
        (top)
       0|
        *        bit 2
       0|
        *        bit 1
      0/ \1
      0   1      bit 0 (leaves)
  i = 2
```
Only the paths 000 and 001 exist; 2, 3 and 4 are excluded because they are not yet inserted.

```text
Frame 3   walk x = 0 1 1
  bit2: x=0 want 1 -> absent, take 0  out=000
  bit1: x=1 want 0 -> present         out=010
  bit0: x=1 want 0 -> present         out=011
  ans[q0] = 3   (partner 0)
```
Bit 2 could not be won, so the walk settled for the best lower bits.

```text
Frame 4   q1: x=1 (001), m=3   insert 2, 3
        (top)
       0|
        *          bit 2
      0/  \1
      *    *       bit 1
    0/\1  0/\1
    0  1  2  3     bit 0
  i = 4
```
The 01 branch now exists, which offers a 1 in column 1.

```text
Frame 5   walk x = 0 0 1
  bit2: x=0 want 1 -> absent, take 0  out=000
  bit1: x=0 want 1 -> present         out=010
  bit0: x=1 want 0 -> present         out=011
  ans[q1] = 3   (partner 2)
```
The new branch was used immediately at bit 1.

```text
Frame 6   q2: x=5 (101), m=6   insert 4
           (top)
         0/    \1
         *      *      bit 2
       0/ \1    |0
       *   *    *      bit 1
     0/\1 0/\1  |0
     0  1 2  3  4      bit 0
  i = 5
```
4 adds the first right branch at bit 2.

```text
Frame 7   walk x = 1 0 1
  bit2: x=1 want 0 -> present         out=100
  bit1: x=0 want 1 -> present         out=110
  bit0: x=1 want 0 -> present         out=111
  ans[q2] = 7   (partner 2)
```
Every column was won. Note the partner is 2, not the largest allowed value 4.

```text
Frame 8   write back in original order
  ans = [3, 3, 7]
```
Answers were placed at each query's original index as they were computed.

Throughout, the trie held exactly `{nums[k] : k < i}`, and because queries came in increasing `m`, that set was exactly `{v in nums : v <= m}` at each query. The walk always set the highest bit it could, given the bits already chosen.

## Why it is correct

**The sweep invariant.** When a query with bound `m` is answered, the pointer `i` has advanced past every `nums[k] <= m` (the while loop) and stopped at the first `nums[k] > m`, or the end. Since `nums` is sorted, the inserted set is exactly the allowed set. Since queries are processed in non-decreasing `m`, no later query needs a number removed. If `i = 0`, the allowed set is empty and -1 is correct.

**The greedy walk.** By induction from the top bit: suppose that after deciding bits 29..b+1, the answer's top bits match the best achievable top bits, and `node` is the subtree of all inserted numbers that achieve them. At bit `b`, if some number in the subtree has bit `b` ≠ bit `b` of `x`, then the best achievable answer has bit `b` = 1. Any partner with bit `b` equal to `x`'s loses `2^b`, which the lower bits (worth at most `2^b - 1`) cannot recover. So moving into the `want` child keeps us on an optimal path. If no such number exists, every candidate gives 0 at bit `b`, and the only child holds them all. After bit 0 the path ends at a real inserted number, and the accumulated `out` is its XOR with `x`, the maximum.

**Output order.** Each answer is written to `ans[qi]` using the original index, so sorting the queries never leaks into the output.

## Cost

- Sorting: O(n log n + q log q).
- Insertions: n numbers × 30 levels = O(30 n).
- Queries: q walks × 30 levels = O(30 q).
- Space: up to 30 n + 1 trie nodes, two ints each: O(30 n).

Total: O((n + q) · 30 + n log n + q log q), roughly 6 · 10^6 trie steps for the maximum input.

If queries had to be answered **online** (each one before seeing the next), you would store in each trie node the minimum value in its subtree, and refuse to step into a child whose minimum exceeds `m`. That is the same O(30) per query with no sorting, at the cost of one extra field per node.

## Variations you will meet

- **Maximum XOR of Two Numbers in an Array** (LeetCode 421): no bound, so insert everything and walk every number. That is Claim 1 alone, O(30 n). An alternative builds the answer bit by bit with a prefix hash set.
- **Online bound** (described under Cost): keep a subtree minimum per node, and the walk refuses children whose minimum exceeds `m`.
- **Maximum Genetic Difference Query** (LeetCode 1938): the allowed set is "ancestors of a tree node". DFS the tree, inserting on entry and deleting on exit (keep a count per node), and answer the queries at each node during the DFS. It is the same trie with a different sweep.
- **Count pairs with XOR in a range** (LeetCode 1803): store subtree counts in each node and, while walking against a limit, add up whole subtrees that are guaranteed to be below it.

## What to carry forward

To maximise XOR, walk a binary trie from the top bit and always take the opposite child when it exists, because a high bit outweighs all lower bits together. When each query restricts the set by a threshold, sort the queries offline so the structure only grows. This closes the chapter, and every earlier idea shows up here: bits as columns, XOR as disagreement, numbers as paths of bits, and a greedy decision made one column at a time.
