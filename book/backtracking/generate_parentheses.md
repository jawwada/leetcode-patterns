# Generate Parentheses

*LeetCode 22 · Medium · Pattern: Backtracking with validity-preserving constraints (open/close counts) · Reading time ~7 min*

## The problem

Given n pairs of parentheses, return all strings of n "(" and n ")" that are well-formed.

```text
Example: n=3 -> ["((()))","(()())","(())()","()(())","()()()"].
  Example: n=1 -> ["()"].
```

## What the problem is really asking

Given n, list every string made of n opening and n closing parentheses that is well formed: every ")" closes an earlier unmatched "(", and nothing is left open at the end.

```text
 n = 3  ->  5 strings

   ((()))   (()())   (())()   ()(())   ()()()

 not allowed:
   ())(()   the 3rd char closes nothing (balance -1)
   (((())   only 2 closes: one "(" left open
```

The answer is a list of strings of length 2n. Their number is the n-th Catalan number: 1, 2, 5, 14, 42, ... That grows exponentially, but far slower than the 4^n strings of length 2n over two characters. For n = 5 there are 42 valid strings among 1024 candidates.

The difficulty: validity looks like a property of the whole string ("balanced"), so it seems you must build a string before you can judge it. The trick is to see that it is really a property you can check one character at a time.

## Do it by hand first

Write the n = 2 strings on paper. Most people keep a running count: how many I have opened, how many I have closed.

```text
 char   opened  closed   may I add "("?   may I add ")"?
  (       1       0      yes (1 < 2)      yes (0 < 1)
  ((      2       0      no  (2 = n)      yes (0 < 2)
  (()     2       1      no               yes (1 < 2)
  (())    2       2      done -> record
 back to "(":
  ()      1       1      yes              no  (1 = 1)
  ()(     2       1      no               yes
  ()()    2       2      done -> record
```

Your hand tracked two counters, and every decision was made by comparing them: "(" is allowed while opened < n, ")" is allowed while closed < opened. Not once did it write a string and then check it. Those two counters are the whole state.

## The first honest attempt

Generate every string of length 2n over `(` and `)`, then run the usual balance check on each: walk left to right, +1 for "(", -1 for ")", fail if the balance goes negative, accept if it ends at 0.

```text
 n = 2: all 16 strings of length 4
   ((((  x end 4     ()((  x end 2     )(((  x dips at 1
   ((()  x end 2     ()()  ok          )(()  x dips at 1
   (()(  x end 2     ())(  x dips      ))((  x dips at 1
   (())  ok          ()))  x dips      ...
```

Cost O(n · 4^n): 2^(2n) strings, each checked in O(n). The waste is obvious in the third column: every string starting with ")" is doomed at its very first character, and that is half of all strings. Yet each is generated to full length and then rejected. In general, a prefix that already dips below zero, or that has used more than n "(", can never be completed, and every one of its 2^(remaining) extensions is built anyway.

```text
                     ""
             (/              \)
           "("               ")"   <- dead here, but the brute
          /    \             /  \     force still builds its
        ...    ...        ")("  "))"  8 descendants for n = 2
```

## The turning point

**Claim: a prefix can be extended to a well-formed string of length 2n if and only if opened <= n and closed <= opened; so allowing "(" only when opened < n and ")" only when closed < opened keeps every branch completable, and the tree has no dead ends at all.**

Justify both directions.

*If.* With opened <= n and closed <= opened, append n - opened "(" and then n - closed ")". The balance never drops below zero (it rises first, then falls to exactly 0), so the result is well formed.

*Only if.* If opened > n, there are too many "(" to ever close within length 2n. If closed > opened at some prefix, that prefix contains a ")" that closed nothing, and no suffix fixes a past mistake.

So the two conditions are exactly the "still alive" test, and they are checkable in O(1) from two counters. Turn them into the choice rule:

- add "(" only if `opened < n`;
- add ")" only if `closed < opened`.

Both rules preserve the alive condition, so every node the walk enters is a prefix of at least one answer. The leaves (length 2n) are exactly the answers, Catalan-many, and the walk never visits a dead node.

This is a new kind of pruning. In Combination Sum the cut happened when a child was found to overshoot, and there were still dead ends (a budget of 1 with no candidate of 1). Here the constraint is **validity-preserving**: it is phrased so that it can only ever produce valid prefixes. The best prunes have this shape.

The geometric picture makes it memorable. Draw each "(" as a step up and each ")" as a step down. The rules say: never take more than n up-steps, and never step below the floor.

```text
 (()())                      ())(()
   /\/\    height 2            /\  /\    height 1
  /    \   height 1           --------   floor (0)
 --------  floor (0)             \/      height -1
 a mountain range                ^ 3rd char closes nothing
```

The valid strings are exactly the paths of 2n steps that start and end on the floor and never go underground (Dyck paths). The two counters are "steps up taken" and "steps down taken"; their difference is the current height.

## Watch it work

Example `n = 2`. Sideways tree; each node shows the prefix and `o/c` = opened/closed. Legend: `*` current path, `<-` current node, `x` pruned with the failing test, `?` not visited.

**Frame 1.** From "" (0/0): "(" is allowed. At "(" (1/0): "(" allowed again. At "((" (2/0): "(" is pruned (o = n).

```text
 *"" 0/0
 +-(-> *"(" 1/0
 |     +-(-> *"((" 2/0 <-
 |     |     +-( x  (o=2 not < n=2)
 |     |     +-?
 |     +-?
 +-?
 path="(("  depth 3
```

**Frame 2.** At "((" add ")" (0 < 2): "(()" 2/1, "(" pruned again; add ")" (1 < 2): "(())" 2/2, length 4, record.

```text
 *"" 0/0
 +-(-> *"(" 1/0
 |     +-(-> *"((" 2/0
 |     |     +-( x
 |     |     +-)-> *"(()" 2/1
 |     |           +-( x  (o=2)
 |     |           +-)-> *"(())" 2/2 <- record
 |     +-?
 +-?
 result=["(())"]
```

**Frame 3.** Unwind to "(" (1/0). Add ")" (0 < 1): "()" 1/1. Then "(" (1 < 2): "()(" 2/1.

```text
 *"" 0/0
 +-(-> *"(" 1/0
 |     +-(-> "((" (done)
 |     +-)-> *"()" 1/1
 |           +-(-> *"()(" 2/1 <-
 |           |     +-( x  (o=2)
 |           |     +-?
 |           +-?
 +-?
 path="()("  depth 4
```

**Frame 4.** At "()(" add ")" (1 < 2): "()()" 2/2, record. Back at "()": ")" is pruned (c=1 not < o=1).

```text
 *"" 0/0
 +-(-> *"(" 1/0
 |     +-(-> "((" (done)
 |     +-)-> *"()" 1/1 <-
 |           +-(-> "()(" 2/1
 |           |     +-)-> "()()" 2/2  recorded
 |           +-) x  (c=1 not < o=1)
 +-?
 result=["(())","()()"]
```

**Frame 5.** Unwind to the root. ")" is pruned there too (c=0 not < o=0). Done.

```text
 "" 0/0
 +-(-> "(" 1/0       (done: 2 answers below)
 +-) x  (c=0 not < o=0)
 result=["(())","()()"]   stack empty
```

Every node entered had `closed <= opened <= n`, and every node entered had at least one answer below it: the `x` marks were the only rejections and they were checked before any character was written.

## Why it is correct

*Invariant.* Every call `dfs(opened, closed)` has `closed <= opened <= n` and `path` equal to a prefix with those counts. The root (0, 0) satisfies it; the "(" branch requires `opened < n` and the ")" branch requires `closed < opened`, so both children satisfy it; append/pop keep `path` aligned with the counts.

*Soundness.* A leaf has length 2n with `closed <= opened <= n`, hence opened = closed = n, and every prefix along the way had closed <= opened, which is exactly well-formedness.

*Completeness.* Any well-formed string satisfies the invariant at every prefix, so at each character the corresponding branch's test passes; the walk follows it to the leaf.

*No duplicates.* Different leaves differ at some first character, where one took "(" and the other ")".

## Cost

- **Time: O(4^n / sqrt(n)).** That is Catalan(n) times O(n) per joined string; since there are no dead ends, internal nodes are at most 2n per leaf.
- **Space: O(n)** for the path and 2n + 1 stack frames, beyond the output.

## Variations you will meet

- **Valid Parentheses (LeetCode 20).** The checker, not the generator: the same balance counter, or a stack for several bracket types.
- **Several bracket types.** Generating balanced strings over `()[]{}` needs a stack on the path, not just two counts, because ")" must match the most recent open type; un-choose then also pushes or pops that stack.
- **Remove Invalid Parentheses (later in this chapter).** The string is given and you delete characters; the same balance test prunes, and you first count how many deletions are needed.
- **Count only.** Catalan(n) = C(2n, n) / (n + 1), or a DP over (opened, closed). Once only the count is asked, the (opened, closed) states repeat and DP wins.

## What to carry forward

Phrase the constraint so that it can only produce valid prefixes (here `opened < n` and `closed < opened`), and the tree has no dead ends: every node you enter leads to an answer. The next problem moves backtracking onto a grid, where the path is a trail of cells and "un-choose" means erasing a mark on the board.
