# Design Search Autocomplete System
*LeetCode 642 · Hard · Pattern: Trie with per-node frequency map + cursor that follows keystrokes · Reading time ~11 min*

## What the problem is really asking

Build the search box of a website. It starts with a history: `sentences[i]` was typed `times[i]` times. Then the user types one character at a time through `input(c)`:

- if `c` is a normal character, return up to 3 historical sentences that start with everything typed so far in this sentence, ordered by count (highest first), ties broken by plain string order;
- if `c` is `#`, the sentence is finished: add one to its count (creating it if new), reset the typed text, and return `[]`.

Each answer is a short ranked list. The object behind it is "the multiset of sentences under the current prefix", and that prefix only ever grows by one letter until `#` resets it. What makes it hard is doing this per keystroke, fast, while the history keeps changing as users finish sentences.

```text
 history: hello:3  help:2  hi:2  hey:1
 input  typed   suggestions
 'h'    h       hello, help, hi      (help < hi on tie)
 'e'    he      hello, help, hey
 'y'    hey     hey
 '#'    -       []   ("hey" count 1 -> 2)
 'h'    h       hello, help, hey     (now hey ties 2)
```

## Do it by hand first

You are typing `h`. With the history on paper, you would circle every sentence starting with `h`, sort the circled ones by count, and read the top 3. Now type `e`. You would not start over: you would cross out the circled sentences that do not continue with `e` (`hi`). Then `y`: cross out all but `hey`.

```text
 typed "h"   circled: hello3 help2 hi2 hey1
 typed "he"  circled: hello3 help2     hey1   (hi out)
 typed "hey" circled:                  hey1
```

What your hand kept was a *current circled set* that only shrinks while typing and is thrown away on `#`. Each keystroke narrows the previous set by one letter. "Narrow a set of strings by one more prefix letter" is exactly one step down a trie. So the hand's state is a pointer into a trie — a cursor.

## The first honest attempt

Keep a dict `sentence -> count` and the typed string. On each keystroke, scan all S sentences, keep those that start with the typed string, sort by `(-count, sentence)`, return the first 3. On `#`, increment the count.

Cost: O(S · L + S log S) per keystroke. The repeated work is that typing `hey` rescans the whole history three times:

```text
 keystroke 'h':  scan hello help hi hey ... (S items)
 keystroke 'e':  scan hello help hi hey ... (S again)
 keystroke 'y':  scan hello help hi hey ... (S again)
                 but after 'h' only the h-sentences
                 could ever match; after 'e' only he-
```

Each scan re-derives from scratch a set that is just the previous set minus a few sentences.

## The turning point

**Claim: keep a cursor at the trie node for the typed prefix and store, at every node, the counts of all sentences passing through it; then each keystroke is one pointer step plus a top-3 pick from that node's map.**

Justify the two halves.

*The cursor.* The node for `p + c` is the child `c` of the node for `p`. So if we already hold the node for what has been typed, the next keystroke needs one dict lookup, not a walk from the root. If the child does not exist, no historical sentence starts with the typed text — and none will, however many more letters come — so the cursor becomes `None` and stays dead until `#`. That is the chapter's "falling off" image, made persistent.

*The payload.* Holding the node is not enough: to rank its sentences we would have to DFS its subtree, which can be most of the trie after one keystroke. So, as in Word Squares, store the answer's raw material on every node: a map `sentence -> count` for all sentences whose path passes through it. Then the suggestions are the 3 smallest items of the cursor's map under the key `(-count, sentence)`, which `heapq.nsmallest(3, ...)` finds in O(m log 3) for m sentences under the prefix.

```text
 trie with per-node maps (counts before any typing)
 (root)
   |
   h   {hello:3, help:2, hi:2, hey:1}
   |\
   | i {hi:2}
   e   {hello:3, help:2, hey:1}
   |\
   | y {hey:1}
   l   {hello:3, help:2}
   |\
   | p {help:2}
   l   {hello:3}
   |
   o   {hello:3}
```

*Updates.* When `#` arrives, the typed sentence gains one count. Its count is recorded in the map of every node on its path, so the update walks the path from the root and adds 1 at each node — O(L). New sentences create their missing nodes on the way, exactly like trie insert. Then the cursor goes back to the root and the typed buffer is cleared.

Note that the typed text is kept separately from the cursor. When the cursor is dead, the trie no longer remembers what was typed, but `#` still needs the full sentence to insert it.

The invariant: *the map at the node for prefix p holds exactly the current count of every sentence starting with p*, and *the cursor is the node for the typed text, or `None` if no sentence starts with it.*

## Watch it work

History `hello:3, help:2, hi:2, hey:1`; input `h`, `e`, `y`, `#`, `h`. The returned lists and the final map are the solution's actual output.

**Frame 1** — after construction: cursor at root, typed empty. Each node's map is as in the drawing above.

```text
 cursor -> (root)        typed: ""
 h: {hello:3, help:2, hi:2, hey:1}
```

**Frame 2** — `input('h')`: cursor steps to `h`. Ranking its map by (−count, sentence): hello(3), then the tie at 2 is ordered `help` < `hi`, then hey(1).

```text
 cursor -> h             typed: "h"
 ranked: hello3 help2 hi2 | hey1
 return [hello, help, hi]
```

**Frame 3** — `input('e')`: one step to `he`. `hi` is not in this map.

```text
 cursor -> he            typed: "he"
 map: {hello:3, help:2, hey:1}
 return [hello, help, hey]
```

**Frame 4** — `input('y')`: one step to `hey`, whose map has a single entry.

```text
 cursor -> hey           typed: "hey"
 map: {hey:1}
 return [hey]
```

**Frame 5** — `input('#')`: walk `h e y` from the root adding 1 for `hey` at each node; reset.

```text
 h:   hey 1 -> 2
 he:  hey 1 -> 2
 hey: hey 1 -> 2
 cursor -> (root), typed: ""   return []
```

**Frame 6** — `input('h')`: the map at `h` is now `{hello:3, help:2, hi:2, hey:2}`. Three-way tie at 2, broken by string order: help < hey < hi.

```text
 cursor -> h
 ranked: hello3 help2 hey2 | hi2
 return [hello, help, hey]   (hey pushed hi out)
```

Across the frames, every keystroke moved the cursor exactly one edge, every answer was read from one node's map, and the `#` update touched exactly the nodes on the finished sentence's path.

## Why it is correct

**Map invariant.** Construction calls the add routine for each seeded sentence, adding its count to every node on its path; a sentence's path visits exactly the nodes of its prefixes, so the map at the node for p contains exactly the sentences starting with p, with their counts. Each `#` does the same with count 1, preserving it.

**Cursor invariant.** Initially the cursor is the root (the empty prefix). Each keystroke c moves it from the node for `typed` to the node for `typed + c` if it exists; if not, no sentence starts with `typed + c`, and since extending a prefix can only shrink the set, `None` is correct for every later keystroke until `#`. `#` resets to the root and the empty prefix.

Given both, the map at the cursor is exactly the set of historical sentences that start with the typed text, with true counts, and taking the 3 smallest by `(-count, sentence)` is exactly the required ranking. A dead cursor correctly returns `[]`.

## Cost

- **Per keystroke:** O(1) for the cursor step plus O(m log 3) to pick the top 3 among m sentences under the prefix. (If you rebuilt the cursor from the root each time, add O(L).)
- **Per `#`:** O(L) to walk the path and bump counts, where L is the sentence length.
- **Space:** O(S · L²) worst case — each sentence appears in the map of each of its L prefix nodes, and each map entry holds the sentence (up to L characters, though Python shares the string object, so it is closer to O(S · L) references).

The brute force was O(S · L + S log S) per keystroke; the trie version makes the cost depend only on the prefix's own candidates.

## Variations you will meet

- **Cache the top 3 at each node** instead of the full map. Queries become O(1), but updates must re-rank: when a sentence's count rises, it may enter a node's top 3 and push the old third place out (easy), but it can never fall out itself, since counts only increase. With decrements or deletions, you need the full map again.
- **Top k with a large k.** Use `heapq.nsmallest(k, ...)` as is (O(m log k)), or keep a sorted structure per node.
- **Search Suggestions System (LeetCode 1268).** Same keystroke cursor, but the ranking is purely lexicographic and the list is static; sorting the products once and binary-searching each prefix is a trie-free alternative.
- **Delete or decay history.** Counts can go down; the per-node full map handles it directly, and a cached top-k would need recomputation for every node on the path.

## What to carry forward

Autocomplete is a cursor in a trie that steps one edge per keystroke, with ranked raw material stored on every node so each step also delivers the answer; updates flow down the whole path of the finished sentence. This closes the chapter: every move in it — walking a path, falling off to prune, payloads on every node, and rewriting strings so the question becomes a prefix — appears in this one design, and together they let you face any trie problem from a blank page.
