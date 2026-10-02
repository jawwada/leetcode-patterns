# Expression Add Operators
*LeetCode 282 · Hard · Pattern: Backtracking with running value + last operand · Reading time ~10 min*

## What the problem is really asking

You get a string of digits and a target integer. Between any two neighbouring digits you may
put `+`, `-`, `*`, or nothing (nothing glues the digits into a longer number). Return every
expression whose value, with normal precedence (`*` before `+` and `-`), equals the target.
A number may not have a leading zero: `0` alone is fine, `05` is not.

The answer is a list of strings. Our running example:

```text
  num = "232", target = 8

  gap:        2 _ 3 _ 2          each _ is one of  "" + - *
  answers:    2+3*2 = 2+6 = 8
              2*3+2 = 6+2 = 8
```

What makes it hard is not the enumeration: with `n` digits there are `4^(n-1)` ways to fill
the gaps, and we must look at them. The hard part is **evaluating** each candidate cheaply
while respecting precedence. A `*` binds tighter than the `+` or `-` before it, so the value
of a prefix is not something you can simply keep adding to. The other trap is the
leading-zero rule, which is easy to get half right.

## Do it by hand first

Write out the choices for `232` as a tree. First decide how long the first number is: `2`,
`23`, or `232`. Then after `2`, decide the next number (`3` or `32`) and the operator in
front of it, and so on.

Evaluate as you go. After `2+3` you know the value is 5. Now append `*2`. You cannot do
`5 * 2 = 10`; the true value of `2+3*2` is 8. What you actually do in your head is: "the `3`
was the last thing I added; take it back out, and put `3*2 = 6` in instead":

```text
  2+3        value 5     last term added: 3
  2+3*2      value 5 - 3 + 3*2 = 8      last term now: 6
  2+3*2*2    value 8 - 6 + 6*2 = 14     last term now: 12
```

What your head kept track of: the **value so far** and the **last term** (the most recent
chunk that was added or subtracted, which a `*` would extend). Those two numbers are the
seed of the algorithm.

## The first honest attempt

Fill the `n - 1` gaps with every combination of `""`, `+`, `-`, `*`, drop strings with a
leading-zero operand, and evaluate each remaining string from scratch with a precedence
parser (or `eval`). Keep those equal to the target.

```text
  num = "232": 4^2 = 16 strings, each parsed in full

  2+3+2   parse "2", "+", "3", "+", "2"   -> 7
  2+3-2   parse "2", "+", "3", "-", "2"   -> 3
  2+3*2   parse "2", "+", "3", "*", "2"   -> 8
           ^^^^ the prefix "2+3" is re-parsed
                in all three strings
```

Cost `O(4^n * n)`: `4^(n-1)` strings, each `O(n)` to evaluate. The waste is the shared
prefix. Strings that agree on their first `k` characters re-evaluate that prefix
independently. For `n = 10` that is a quarter of a million strings, and every one pays a
full parse at its leaf.

## The turning point

**Claim: carry two numbers down the recursion, `value` (the prefix evaluated with correct
precedence) and `last` (the signed last term of the sum); then appending any operator and
operand is O(1).**

Think of an expression as a **sum of terms**, where each term is a product:

```text
  2 - 3 * 4 + 5   =   (+2) + (-3*4) + (+5)
                       term   term     term
```

`+` and `-` start a new term. `*` extends the current term. So:

- `+x`: a new term `+x`. `value + x`, and `last = x`.
- `-x`: a new term `-x`. `value - x`, and `last = -x`. The sign lives in `last`.
- `*x`: the last term becomes `last * x`. Remove the old last term and add the new one:
  `value - last + last * x`, and `last = last * x`.

```python
dfs(j, expr + "+" + s, value + x, x)
dfs(j, expr + "-" + s, value - x, -x)
dfs(j, expr + "*" + s, value - last + last * x, last * x)
```

Why the sign must be in `last`: take `2-3*4`. After `2-3`, value is `-1`. If `last` were
`3`, the `*4` would compute `-1 - 3 + 12 = 8`, wrong. With `last = -3` it computes
`-1 + 3 - 12 = -10`, which is `2 - 12`. Correct.

Why it extends correctly through chains: `2+3*2*2`. Each `*` replaces the current term with
itself times the new operand, and `value` always equals "everything before the last term"
plus the last term. That identity is the invariant, and each of the three rules preserves
it.

The search itself: `dfs(i, expr, value, last)` stands at digit position `i`. It chooses
where the next operand ends, `j` from `i + 1` to `n`, giving operand `num[i:j]`. If
`i == 0`, there is no operator in front: start with `value = last = operand`. Otherwise
branch three ways with the rules above. At `i == n`, record `expr` if `value == target`.

The leading-zero rule becomes a prune on `j`: if `num[i] == '0'`, only the one-digit
operand `0` is allowed, so the `j` loop **breaks** as soon as the operand has length 2 and
starts with `0`. Every longer operand from that position is cut along with its subtree.

Choosing `j` covers the "nothing" separator: gluing digits is not a fourth operator but a
longer operand. So each node branches on (length of next operand) times (3 operators), and
the tree has exactly the same leaves as the brute force, with O(1) work per edge.

## Watch it work

`num = "232"`, `target = 8`. Each node shows `expr (value, last)`. `x` marks a leaf that
misses the target; `OK` marks a hit.

```text
Frame 1   i = 0: choose the first operand (no operator)
               root
            /   |    \
          "2"  "23"  "232"
         (2,2) (23,23) (232,232)
                        at i=3: 232 != 8   x
```
The whole-string operand is a leaf immediately (the DFS reaches it last) and misses; the
other two branches continue.

```text
Frame 2   under "2" (2,2), operand "3" (j = 2):
      2+3   (2+3, 3)       = (5, 3)
      2-3   (2-3, -3)      = (-1, -3)
      2*3   (2-2+2*3, 6)   = (6, 6)
```
For the first `*`, `value - last` removes the only term, so `2*3` correctly becomes 6.

```text
Frame 3   under 2+3 (5, 3), last operand "2":
      2+3+2   (7, 2)              x
      2+3-2   (3, -2)             x
      2+3*2   (5-3+3*2, 6) = (8,6) OK  -> record
```
The `*` reaches back: it removes the `3` that was added and adds `3*2` instead.

```text
Frame 4   under 2-3 (-1, -3), operand "2":
      2-3+2   (1, 2)                     x
      2-3-2   (-3, -2)                   x
      2-3*2   (-1+3-6, -6) = (-4, -6)    x
```
The negative `last` makes `2-3*2` evaluate to `2-6 = -4`, as precedence demands.

```text
Frame 5   under 2*3 (6, 6), operand "2":
      2*3+2   (8, 2)                     OK -> record
      2*3-2   (4, -2)                    x
      2*3*2   (6-6+12, 12) = (12, 12)    x
```
A chain of `*` keeps one growing term; `+2` starts a fresh one and hits the target.

```text
Frame 6   remaining branches, all miss
      2+32 (34)  2-32 (-30)  2*32 (64)          x x x
      23+2 (25)  23-2 (21)   23*2 (46)          x x x
  result = ["2+3*2", "2*3+2"]   16 leaves, O(1) each
```
Every one of the 16 leaves was reached with its value already computed; nothing was parsed.

Across all frames, `value` equalled the true value of `expr`, and `last` equalled its final
signed term. Each edge did one constant-time update.

## Why it is correct

**Invariant.** At every call, `expr` is a well-formed expression using `num[:i]` with no
leading-zero operands, `value` is its correct value under precedence, and `last` is its
final term with sign, so `value - last` is the value of everything before that term.

**Preservation.** `+x` and `-x` append a new term: the sum grows by `x` or `-x`, and the new
term is `x` or `-x`. `*x` multiplies the final term: the part before it, `value - last`, is
unchanged, and the term becomes `last * x`. The first operand has no operator, so
`value = last = x`. The leading-zero break only removes operands that are illegal.

**Soundness and completeness.** Every legal expression is determined by where each operand
ends and which operator precedes it. The `j` loop tries every legal end and the three
branches every operator, so every legal expression is exactly one root-to-leaf path. At its
leaf the invariant gives its true value, so it is recorded if and only if it hits the
target.

## Cost

- **Time `O(4^n)`.** Each of the `n - 1` gaps takes one of four choices; every edge is O(1)
  arithmetic. Building `expr` strings adds `O(n)` per recorded answer (or per edge if you
  concatenate naively; a shared char buffer avoids that).
- **Space `O(n)`** recursion depth and the current expression, plus the output.
- The brute force is `O(4^n * n)` because each leaf re-parses from scratch.

## Variations you will meet

- **Only `+` and `-` (Target Sum, LeetCode 494).** No precedence issue, so no `last`; and
  because only the value matters, not the expression, it collapses into a subset-sum DP.
- **Allow parentheses or division.** The sum-of-terms view breaks; you are in 24 Game
  territory, where the state is the set of values still to combine, not a left-to-right
  prefix.
- **Basic Calculator II (227).** The same `last` trick, used to evaluate a given expression
  in one pass with a stack of terms instead of searching.
- **Overflow in other languages.** Operands can reach ten digits and products overflow
  32-bit integers; use 64-bit for `value` and `last`. Python does not care.

## What to carry forward

When a search builds something left to right, carry its evaluation incrementally, and when
an operator binds tighter than what came before, also carry the piece it would reach back
into. The next problem, 24 Game, drops left-to-right order entirely: any two numbers may be
combined first, so the state becomes the multiset of values still on the table.
