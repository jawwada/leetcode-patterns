# Design Add and Search Words Data Structure
*LeetCode 211 · Medium · Pattern: Trie with wildcard DFS · Reading time ~7 min*

## The problem

Design WordDictionary with addWord(word) and search(word), where the search pattern may contain '.' matching any
single letter.

```text
Example: add bad, dad, mad; search("pad") -> False;
  search("bad") -> True; search(".ad") -> True; search("b..") ->
  True.
```

## What the problem is really asking

Design a word dictionary with `addWord(word)` and `search(pattern)`. The pattern is made of lowercase letters and dots, and a dot matches any single letter. `search` returns True if some added word has exactly the pattern's length and agrees with it at every non-dot position.

The answer is a boolean, but the interesting object is the *set of words consistent with a pattern*. With no dots this is Implement Trie's `search`. Each dot multiplies the number of possibilities: at a dot, the next letter is unknown, so every letter that some stored word has at that position must be considered.

```text
 added: bed, dad, mad
 search(".ad")  -> True   (dad, mad)
 search("b..")  -> True   (bed)
 search("..x")  -> False
 search("be")   -> False  (prefix of bed, not a word)
```

What makes it hard: the dot defeats hashing (you cannot hash "any letter"), and trying all 26 letters per dot is 26^d lookups.

## Do it by hand first

Match `.ad` against `bed`, `dad`, `mad` written in a column.

```text
 pattern  .  a  d
 bed      b  e       <- 'e' != 'a', drop
 dad      d  a  d    <- survives to the end: match
 mad      m  a  d    (never needed)
```

At the dot you accepted every word; at `a` you dropped `bed`. Now look at this through the trie from the last two chapters. The first position has three distinct letters: `b`, `d`, `m`. The dot says "try each of those". The letter `a` then says "in each branch, follow only `a`". Your hand was keeping a *set of trie nodes still alive*, and the dot is the only thing that makes that set bigger than one.

## The first honest attempt

Store words in a list. `search` compares the pattern to every stored word: equal length, and at each position either the pattern has a dot or the letters are equal.

That is O(N · L) per search. The repeated work: words sharing a prefix are rejected one by one for the same reason.

```text
 pattern "z.."  against 10,000 words starting with 'b'
   bxx: z?b fail
   byy: z?b fail      <- same failed comparison,
   bzz: z?b fail         10,000 times
```

Every word starting with `b` fails at position 0 for the same reason, yet each is visited separately. In a trie, all 10,000 words sit under one `b` edge, and one failed lookup discards them together.

## The turning point

**Claim: on a trie, a literal letter follows at most one edge and a dot follows every edge, so a depth-first search over (node, position) visits only the part of the trie consistent with the pattern.**

Define `dfs(node, i)` = "is there a word in node's subtree that spells `pattern[i:]`?". Then:

- if `i == len(pattern)`: the whole pattern was consumed, so the answer is whether a word ends right here — `"$" in node`;
- if `pattern[i]` is a letter `ch`: the only possible continuation is the edge `ch`; answer `ch in node and dfs(node[ch], i+1)`;
- if `pattern[i]` is a dot: any child works; answer `any(dfs(child, i+1))` over all real children.

```text
 trie for bed, dad, mad          ".ad" as a search tree
       (root)                         root
      /  |   \                    .  / | \
     b   d    m                     b  d  m
     |   |    |                  a  x  |  (skipped:
     e   a    a                        a   any() already
     |   |    |                  d     |   True)
     d*  d*   d*                       d*  -> True
```

Two details make this correct rather than almost-correct. When looping over a dot's children, skip the `"$"` key: it is the end marker (its value is `True`, not a dict), not an edge. And the base case checks `"$"`, not merely "the node exists": `search("be")` reaches the node for `be` but no word ends there.

Why is this fast in practice? Literals dominate real patterns, and each literal is a single dict lookup that either continues one branch or kills it. Only dots branch, and they branch over the children that actually exist — at most 26, usually far fewer. A mismatch prunes a whole subtree of words at once, which is precisely the work the list approach repeated.

The "any" matters too: Python's `any` stops at the first True, so a successful scout ends the search without exploring siblings.

## Watch it work

Words `bed`, `dad`, `mad` (children of the root in insertion order: b, d, m). Running the solution: `.ad` is True, `..x` is False.

**Frame 1** — the trie.

```text
 {"b":{"e":{"d":{"$":T}}},
  "d":{"a":{"d":{"$":T}}},
  "m":{"a":{"d":{"$":T}}}}
```

**Frame 2** — `search(".ad")`, `dfs(root, 0)`: the dot fans out; first scout goes to `b`.

```text
 pattern . a d       depth stack
         ^ i=0       dfs(root,0) '.'
 scout -> b          dfs(b,1)    'a'
 "a" in b? no (only "e")  -> False
```

**Frame 3** — second scout goes to `d`: `a` exists, then `d` exists, then `i == 3` and the node has `"$"`.

```text
 dfs(d,1)   'a' -> node d>a
 dfs(da,2)  'd' -> node d>a>d*
 dfs(dad,3) i==3, "$" present -> True
 any() stops; scout to m never sent
```

**Frame 4** — `search("..x")`: two dots fan out to every depth-2 node, and every one lacks `x`.

```text
 depth 0 '.': b, d, m
 depth 1 '.': be, da, ma
 depth 2 'x': be? no  da? no  ma? no
 every scout falls off -> False
```

Across frames, every `dfs(node, i)` call had `node` = the trie node for some stored prefix of length i that agrees with `pattern[:i]`. Literals never created more than one call; dots created one call per existing child.

## Why it is correct

The invariant: *`dfs(node, i)` is True iff some stored word w has `w[:i]` equal to node's prefix and `w[i:]` matches `pattern[i:]`.* Prove it by induction on the remaining length `len(pattern) - i`.

When nothing remains, the only possible w is the node's prefix itself, and it is a stored word exactly when `"$"` is in the node. Otherwise, any matching w continues with some letter c at position i. If the pattern has a literal, c must equal it, and the only candidate subtree is `node[c]`; if the pattern has a dot, c can be any child, so we must ask every child — and `any` returns True iff one of them succeeds. In both cases the recursive calls are correct by induction, so the combination is. `search` returns `dfs(root, 0)`, which by the invariant is exactly "some stored word matches the whole pattern".

## Cost

- **addWord:** O(L) — standard trie insert.
- **search, no dots:** O(L) — one edge per letter.
- **search, d dots:** worst case O(26^d · L), but never more than the number of trie nodes at the depths visited, so O(total characters) is an absolute bound.
- **Space:** O(total characters) for the trie, plus O(L) recursion depth.

## Variations you will meet

- **Dots only at the end or start.** If dots are known to be trailing, walk the literal prefix and then just check "some word of the right length exists below"; store a set of remaining lengths at each node to answer in O(1).
- **Bucket by length.** Since lengths must match, keeping a separate trie (or list) per word length removes useless branches and is a common speed trick for this exact problem.
- **`*` meaning any run of letters** (wildcard matching). The DFS gains a choice "consume zero letters or one more"; memoise on (node, i) to avoid exponential blow-up.
- **Count matches instead of existence.** Replace `any` with `sum`; you lose the early exit, so cost becomes the full consistent subtree.

## What to carry forward

A trie turns pattern search into a DFS where literals follow one edge and wildcards follow all, and a mismatch prunes a whole subtree of words at once. The next problem keeps this DFS but walks it across a letter grid, where the trie decides which neighbouring cell is worth stepping onto.
