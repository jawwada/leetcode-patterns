# 24 Game
*LeetCode 679 · Hard · Pattern: Reduce-the-multiset backtracking (combine two values, recurse on the rest) · Reading time ~10 min*

## What the problem is really asking

You hold four cards, each a number from 1 to 9. Using `+`, `-`, `*`, `/` (real division, not
integer) and any parentheses you like, can you make an expression that uses each card
exactly once and equals 24? You may not glue cards into two-digit numbers and there is no
unary minus. Return True or False.

```text
  cards  [4, 1, 8, 7]

  one answer:   (8 - 4) * (7 - 1)  =  4 * 6  = 24
  another:       8 * (7 - 4 * 1)   =  8 * 3  = 24

  cards  [1, 2, 1, 2]  ->  False (nothing reaches 24)
```

The answer is a boolean. What makes it hard is that the expression space has three
independent dimensions: the order of the cards, the three operators, and the shape of the
parentheses. Enumerating them separately means writing out every bracket shape by hand,
and it evaluates the same sub-expressions again and again. There is also a numeric trap:
`[3, 3, 8, 8]` is solvable only as `8 / (3 - 8 / 3)`, which passes through the fraction
`1/3`, so integer arithmetic misses it and float equality fails on it.

## Do it by hand first

How does a person actually play 24? You do not think "which of the five bracket shapes?"
You look at the table, pick two cards, combine them, and look again.

With `[4, 1, 8, 7]`: "4 times 1 is 4, that is useless... well, it gives me `[8, 7, 4]`.
7 minus 4 is 3, and now I have `[8, 3]`. 8 times 3 is 24." Done.

```text
  table states, one merge per step

  [4, 1, 8, 7]      merge 4 and 1 with *   -> 4
  [8, 7, 4]         merge 7 and 4 with -   -> 3
  [8, 3]            merge 8 and 3 with *   -> 24
  [24]              one value left: is it 24?  yes
```

What your hand kept track of: **the numbers still on the table**. Nothing else. The
parentheses never appeared; they are implied by the order in which you merged. That list
of remaining values is the entire state of the search.

## The first honest attempt

Enumerate every full expression: `4! = 24` orderings of the cards, `4^3 = 64` operator
triples, and the 5 ways to parenthesise four operands:

```text
  five shapes for a b c d (each needs its own code):
    ((a b) c) d      (a (b c)) d      (a b) (c d)
    a ((b c) d)      a (b (c d))

  24 orders x 64 operator triples x 5 shapes = 7,680
  expressions, each evaluated from scratch

  repeated work, for example:
    (4 * 1) ...  and  (1 * 4) ...   same value, two trees
    ((4*1)-7)... and (4*1)-(7...)   4*1 evaluated again
```

The input size is fixed, so this is technically O(1), but it is instructive waste. `a + b`
and `b + a` are separate expressions with identical values. Two different shapes that both
start by combining the same pair compute that pair again. And the five shapes are a
hand-written list that does not generalise: with five cards there are 14 shapes, with six
there are 42.

## The turning point

**Claim: every evaluation of an expression over `k` values is a sequence of steps, each of
which takes two values currently on the table and replaces them with one result; so the
search state is just the multiset of remaining values, and the search is "pick two, combine,
recurse on the smaller table".**

Why it holds: evaluate any expression tree bottom-up. At each step some operator node has
two children that are already numbers; it combines them into one. Before that step the
"table" holds the values of the current frontier of the tree, after it the table has one
fewer value. Four cards need exactly three merges to reach one value. Conversely, any
sequence of three merges corresponds to some expression tree: the first merge is a deepest
subtree, and so on. So collapsing the table in every possible way visits every expression,
and the parenthesis shapes fall out automatically from which pair you merge next.

Now the merge itself. For a pair `(a, b)` there are six results, not four, because `-` and
`/` are not commutative:

```text
  a + b     a - b     b - a     a * b     a / b     b / a
                                          (b != 0)  (a != 0)
```

We only iterate pairs with `i < j`, so `b - a` and `b / a` must be listed explicitly; this
is the most common bug. `+` and `*` appear once, which is exactly how the commutative
duplicates of the brute force disappear.

The tree has depth 3:

```text
  level   table size   children per node
  root        4        C(4,2) * 6 = 36
  1           3        C(3,2) * 6 = 18
  2           2        C(2,2) * 6 =  6
  leaves      1        compare with 24

  at most 36 * 18 * 6 = 3,888 leaves
```

The numeric trap is handled with floats and a tolerance. Real division is required, and
values like `8/3` are not exact in binary, so the leaf test is `|x - 24| < 1e-6`. Division
is guarded the same way: skip `a / b` when `|b|` is below the tolerance.

Finally, return True as soon as any branch succeeds. The only case that walks the whole tree
is a hand with no solution.

## Watch it work

Cards `[4, 1, 8, 7]`. Pairs are tried in index order `(0,1), (0,2), ...`, results in the
order `a+b, a-b, b-a, a*b, a/b, b/a`. The new value is appended to the end of the table.

```text
Frame 1   root table [4, 1, 8, 7]
  first pair (4,1): 4+1 = 5  -> table [8, 7, 5]
  first pair (8,7): 8+7 = 15 -> table [5, 15]
  leaves: 5+15=20 x   5-15=-10 x   15-5=10 x ...
```
The DFS dives to depth 3 immediately; the first three leaves all miss 24.

```text
Frame 2   subtree [8, 7, 5] exhausted: 108 leaves, all x
          then 4-1 -> [8, 7, 3]:  108 leaves  x
               1-4 -> [8, 7, -3]: 108 leaves  x
  root
  |- 4+1  x (108)
  |- 4-1  x (108)
  |- 1-4  x (108)
  `- 4*1  -> [8, 7, 4]   <- next
```
324 leaves have failed; every value derived from `4+1`, `4-1`, `1-4` is a dead table.

```text
Frame 3   table [8, 7, 4]
  pair (8,7): 6 merges, 36 leaves     x
  pair (8,4): 6 merges, 36 leaves     x
  pair (7,4): 7+4 = 11 -> [8, 11], 6 leaves  x
              7-4 = 3  -> [8, 3]    <- here
```
Inside `[8, 7, 4]` the first two pairs and the first merge of the third pair all fail.

```text
Frame 4   table [8, 3]
  8+3 = 11  x    8-3 = 5  x    3-8 = -5  x
  8*3 = 24  -> table [24], |24 - 24| < 1e-6   OK
  leaf number 406 of at most 3,888
```
The fourth merge of the last pair reaches 24; True propagates up and the search stops.

```text
Frame 5   reading the merges back as an expression
  [4,1,8,7] --4*1--> [8,7,4] --7-4--> [8,3] --8*3--> [24]
  expression:  8 * (7 - (4 * 1))  = 24
```
The parentheses were never chosen; they are the order of the merges.

For comparison, `[1, 2, 1, 2]` has no answer and the search visits 3,736 leaves (fewer than
3,888 because a few divisions by zero are skipped), then returns False. `[3, 3, 8, 8]`
succeeds at leaf 1,179 via `8 / 3`, then `3 - 8/3 = 1/3`, then `8 / (1/3)`, which in floats
is `23.99999999999999`: an `== 24` test would have said False.

Across all frames, the table always had exactly one value per remaining subexpression, and
its size went down by one per level. Nothing outside the table influenced any decision.

## Why it is correct

**Invariant.** At every call, each value on the table is the value of a disjoint
subexpression over the original cards, and together those subexpressions use each card
exactly once.

**Preservation.** Merging values `a` and `b` with an operator gives the value of the
subexpression `(A op B)`, which uses exactly the cards of `A` and `B`. Replacing the two with
the result keeps the cards disjoint and fully covered.

**Soundness.** A leaf has one value, which by the invariant is the value of a full
expression using every card once. True is returned only if that value is 24 (within
tolerance, which only absorbs float rounding).

**Completeness.** Any valid expression is a binary tree with four leaves. Evaluating it
bottom-up is a sequence of three merges of two current values; at each step the DFS tries
every pair and every one of the six results, including both orders of `-` and `/`, so that
sequence is a path in the search tree.

## Cost

- **Time O(1)** for four cards: at most 3,888 leaves and fewer than 5,000 calls. In general,
  for `n` values the count of leaves grows like `n! * (n-1)! * 6^(n-1) / 2^(n-1)`, which is
  why this only works for tiny `n`.
- **Space O(n)** recursion depth (3 here), plus the small tables.
- The brute force evaluates 7,680 full expressions; the table search is both smaller and
  needs no hand-written shapes.

## Variations you will meet

- **Return the expression, not just True.** Carry a parallel list of strings; when merging
  `a` and `b` into `v`, merge their strings into `"(" + sa + op + sb + ")"`.
- **Arbitrary target and card count.** The same skeleton works; add memoisation keyed on the
  sorted table (as a tuple of exact `Fraction`s) because different merge orders reach the
  same table.
- **Exact arithmetic.** Use `fractions.Fraction` instead of floats; equality is then exact
  and there is no tolerance to tune, at some speed cost.
- **Expression Add Operators (282) contrast.** There the order of digits is fixed and the
  state is a left-to-right prefix; here any pair may merge first, so the state is a
  multiset. Ask: "is order fixed?" to tell which skeleton fits.

## What to carry forward

When parentheses are free, stop enumerating expression shapes and search over the table of
remaining values: pick two, merge with every non-commutative variant, recurse on the smaller
table. The last problem, Robot Room Cleaner, keeps the backtracking skeleton but makes the
undo physical: the robot has to walk back, so you must design how to step out of a branch.
