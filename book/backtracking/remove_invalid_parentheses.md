# Remove Invalid Parentheses
*LeetCode 301 · Hard · Pattern: Backtracking with counted removals and balance pruning · Reading time ~10 min*

## What the problem is really asking

You get a string of `(`, `)` and letters. Delete as **few** parentheses as possible so that
what remains is balanced, and return **every distinct** string you can get that way. Letters
always stay.

So the answer is a set of strings, all of the same length, all valid, each obtained by the
minimum number of deletions. Two requirements pull against each other: "minimum" is an
optimisation, and "all of them" is an enumeration.

```text
  s = ( ) ( ) )         index 0 1 2 3 4
                        the ) at 4 has no partner

  delete 1 char, three ways:
    drop index 1  ->  ( ( ) )     "(())"
    drop index 3  ->  ( ) ( )     "()()"
    drop index 4  ->  ( ) ( )     "()()"   same string again

  answer = ["(())", "()()"]
```

What makes it hard: you do not know in advance which characters are the "bad" ones; the
same string can be fixed in structurally different ways; and different deletions can give
the same result, so duplicates must be collapsed. A careless search either misses answers,
returns non-minimal ones, or explodes in size.

## Do it by hand first

To check if a parenthesis string is valid, you walk left to right with a counter: `(` adds
one, `)` subtracts one, the counter must never go negative, and it must end at zero.

Do that on `()())`:

```text
  char      (   )   (   )   )
  balance   1   0   1   0  -1   <- a ) with nothing open
```

At index 4 the counter would go to -1. That `)` cannot be matched by anything to its left,
and nothing to its right can help it. So at least one `)` must go. Notice that the counter
told you more than "invalid": it told you **how many** of each kind must be deleted. If you
reset the counter instead of letting it go negative and count those resets, you get the
number of unmatched `)`; whatever is left on the counter at the end is the number of
unmatched `(`.

Then by hand you would ask: which `)` should go? Any `)` at or before index 4 will do, as
long as the remaining string still never dips below zero. You tried them one by one.

What you kept track of: the running **balance**, and the **budget** of deletions still
allowed for each kind of bracket. Those two counters become the state of the search.

## The first honest attempt

Try every subset of characters to delete: `2^n` masks. For each, build the remaining string,
validate it, and keep the valid ones; then return the valid strings of maximum length.

```text
  s = ()())   2^5 = 32 deletion masks

  keep all 5         ()())      invalid
  drop {0}           )())       invalid: starts with )
  drop {0,1}         ())        invalid
  drop {0,1,2}       ))         invalid
  ...                every mask that drops index 0
                     but keeps index 1 dies at its
                     first char, yet is built in full
  drop {1,2,3,4}     (          invalid
  drop all           ""         valid but 5 deletions, not 1
```

Cost `O(2^n * n)`. The waste comes in two flavours. Many masks delete far more than needed
(`""` is valid but useless), and they are only discarded at the end when lengths are
compared. Many others go negative at their first or second character, but the rest of the
string is still assembled and scanned.

## The turning point

**Claim: one left-to-right balance pass gives the exact minimum number of `(` to delete
(`left`) and `)` to delete (`right`); the search then only decides which ones, and any
partial string whose balance goes negative or whose budget is exceeded can be cut
immediately.**

Why the counts are exact. Each `)` that would drive the balance negative has no `(` to its
left available to match it; deleting some `)` at or before it is unavoidable, and one
deletion per such event suffices. At the end, `left` unmatched `(` remain, each needing its
own deletion. Neither kind of deletion fixes the other kind of problem, so `left + right` is
both necessary and sufficient. Pass 1 in the code is just:

```python
left = right = 0
for ch in s:
    if ch == "(": left += 1
    elif ch == ")":
        if left: left -= 1
        else: right += 1
```

With the budgets known, the search becomes a walk along the string carrying
`(i, open, left, right, path)`. At each character:

- If it is `(` and `left > 0`, one branch deletes it (`left - 1`).
- If it is `)` and `right > 0`, one branch deletes it (`right - 1`).
- One branch keeps it: `(` raises `open`; a letter changes nothing; `)` lowers `open`
  **only if `open > 0`**. Keeping a `)` with nothing open is pruned on the spot.

At the end of the string, accept `path` only if `open == 0` and both budgets are exactly
zero. Budgets at zero means exactly the minimum was deleted, so every accepted string is
minimal; `open == 0` plus never-negative means it is valid.

The two prunings work on different axes. The budget caps the **depth of deletion**: at most
`left` deletions of `(` and `right` of `)`, so the tree is bounded by
`C(n, left) * C(n, right)` leaves instead of `2^n`. The balance fence cuts **ill-formed
prefixes** at their first bad character. Together, almost every leaf the search reaches is
an answer.

Duplicates remain: deleting the `)` at index 3 or at index 4 of `()())` gives the same
string. The solution collects results in a set. (A sharper version skips deleting a bracket
when the previous character was the same bracket and was kept, which avoids generating the
duplicate at all; the set is simpler and the cost difference is small.)

## Watch it work

`s = "()())"`. Pass 1 gives `left = 0`, `right = 1`. Each frame shows the decision tree so
far (`del` and `keep` edges), the current path in brackets, and the state.

```text
Frame 1   pass 1 and the root
  i       0 1 2 3 4
  s       ( ) ( ) )
  bal     1 0 1 0 -   <- ) at 4 unmatched: right = 1
  i=0 '(' : left = 0, so no delete branch; keep
  state  path "("   open 1  left 0  right 1
```
The budgets say: delete exactly one `)` and no `(`.

```text
Frame 2   i=1 ')' : two branches
         "("
        /    \
   del )      keep )
   right 0    open 0
   "("        "()"
```
The left branch spends the whole budget; from here on it can only keep characters.

```text
Frame 3   follow del: i=2 keep ( open 2, i=3 keep ) open 1
          (no budget to delete), i=4 keep ) open 0
  path  [ ( ( ) ) ]     end: open 0, left 0, right 0
  add "(())"            result = {"(())"}
```
With no budget left, the branch is a straight line; it ends balanced and is accepted.

```text
Frame 4   follow keep at i=1: "()" open 0
          i=2 keep ( -> "()(" open 1
          i=3 ')' :   del ) (right 0)    keep ) open 0
                         |                   |
          i=4 ')' :   keep ) open 0       see Frame 5
  path  [ ( ) ( ) ]     add "()()"   result has 2
```
Deleting the bracket at index 3 and keeping the one at index 4 gives `()()`.

```text
Frame 5   the keep-at-3 branch: path "()()" open 0
          i=4 ')' :   del ) (right 0)   keep ) needs open>0
                        -> "()()"  add       open 0   x
  result = {"(())", "()()"}   set absorbs the repeat
```
Deleting index 4 gives `()()` again, which the set ignores; keeping it is pruned by the
balance fence before it is built.

```text
Frame 6   full tree, 3 leaves reached, 1 branch pruned
  (  ->  del )  ->  ( ) )                  "(())"   OK
     ->  keep ) ->  ( -> del )  -> )        "()()"   OK
                         keep ) -> del )    "()()"   dup
                                   keep )   x open<0
```
Compare with the 32 masks of the brute force: here only 3 leaves exist, all of them valid.

Across the frames, `open` never went below zero on any live branch, and `left + right` plus
the deletions already made always equalled the minimum. Every accepted leaf had both
budgets at exactly zero.

## Why it is correct

**Minimality.** Pass 1 proves at least `left` deletions of `(` and `right` of `)` are
needed, and the search accepts only strings that used exactly those budgets. So every
answer is minimal, and since the true optimum needs those deletions too, minimal answers
exist with these exact counts.

**Validity.** On every live branch the balance is never negative (keeping `)` requires
`open > 0`), and at the leaf it is zero. That is the definition of a valid string.

**Completeness.** Take any valid string reachable with the minimum deletions. Walk it along
`s`: each deleted bracket corresponds to a delete branch, allowed because the budgets are
exact; each kept bracket corresponds to a keep branch, allowed because its prefix balance
is non-negative (it is a prefix of a valid string). So that sequence of choices is a path
in the tree, and its leaf adds the string.

**Distinctness.** The set returns each string once regardless of how many deletion choices
produced it.

## Cost

- **Time `O(2^n)` worst case**, bounded more tightly by `C(n, left) * C(n, right)` leaves,
  each paying `O(n)` to build the path string.
- **Space `O(n)`** recursion depth plus the output set.
- The mask brute force is `O(2^n * n)` and holds every valid string before filtering.

## Variations you will meet

- **Minimum Remove to Make Valid Parentheses (1249): return just one answer.** No search
  needed. Use pass 1 with a stack of indices, delete the unmatched ones, done in `O(n)`.
- **BFS by number of deletions.** Level `k` holds every string with `k` characters removed;
  stop at the first level that contains a valid string. Simpler to reason about, but it
  generates many more strings than the budgeted DFS.
- **Several bracket types.** The balance counter becomes a stack, and the budget pass must
  match types; the search skeleton is unchanged.
- **Longest Valid Parentheses (32).** Same balance counter, but the question is a substring
  length, which is a scan or DP rather than a search.

## What to carry forward

Count before you search: a cheap first pass can fix how many changes are allowed, and then
the search only decides which ones, with a fence (here, balance never below zero) killing
bad prefixes. Next, Expression Add Operators also walks a string left to right building an
expression, but instead of a balance counter it must carry the expression's running value,
and multiplication makes that tricky.
