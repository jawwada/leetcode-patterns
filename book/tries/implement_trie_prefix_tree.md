# Implement Trie (Prefix Tree)
*LeetCode 208 · Medium · Pattern: Trie (prefix tree) · Reading time ~7 min*

## What the problem is really asking

Build a container of words with three operations: `insert(word)` adds a word, `search(word)` asks "was exactly this word inserted?", and `startsWith(prefix)` asks "was any word inserted that begins with these letters?". The answer to each query is a boolean; the real deliverable is the data structure.

The difficulty is the gap between the two questions. `search` is just set membership, and a hash set does it in O(L). `startsWith` is what a hash set cannot do: a set of words has no idea that `apple` begins with `app` unless you scan every word. The task is to find one structure that answers both in time that depends only on the length of the query.

```text
 insert apple, app, apt

 search("app")      -> True    (inserted)
 search("ap")       -> False   (only a prefix of words)
 startsWith("ap")   -> True    (app, apple, apt start so)
 startsWith("b")    -> False
```

## Do it by hand first

Write the three words in a column and answer `startsWith("ap")` with a pencil.

```text
  a p p l e
  a p p
  a p t
  ^ ^
  |  \_ second letter: p, p, p  -> all still alive
  \____ first letter:  a, a, a  -> all still alive
  after 2 letters at least one word survives -> True
```

You moved down the letters of the query and, at each position, kept the set of words still agreeing with it. But notice what your eye actually did: it did not compare three separate `a`s. It saw one column of `a`s and treated it as one fact. Then one column of `p`s. Only at the third letter do the words disagree (`p` vs `t`), and that is where your attention split.

What your hand kept track of was "the group of words that share what I have read so far". Groups split only where words differ. A tree with one node per group, branching where letters differ, is exactly that bookkeeping made permanent.

## The first honest attempt

Keep a list. `insert` appends. `search(w)` scans the list for an equal string. `startsWith(p)` scans the list calling `word.startswith(p)` on each one.

That is O(1) insert and O(N·L) per query for N words of length up to L. The waste is easy to point at: every word that begins with `ap` re-reads the letters `a` and `p`.

```text
 startsWith("ap") over a list
 apple : a=a? p=p?  -> yes
 app   : a=a? p=p?  -> (already answered, but re-read)
 apt   : a=a? p=p?  -> (re-read again)
         ^^^^^^^^
         the same two comparisons, once per word
```

With ten thousand words starting `ap`, the same two comparisons happen ten thousand times, and the result never changes. The answer to "does anything start with `ap`?" depends on the prefix, not on which word you happen to look at.

## The turning point

**Claim: every query depends only on the prefixes present in the set, so store each distinct prefix once and let a query visit one prefix per character.**

Justification: `startsWith(p)` is literally "is p one of the prefixes of the stored words?". `search(w)` is "is w one of those prefixes, *and* is it a whole word?". Neither needs the words individually; both need the set of prefixes plus one bit per prefix saying "a word ends here".

Now organise those prefixes. Every prefix of length k+1 is a prefix of length k plus one letter. So put the prefixes in a tree: the root is the empty prefix, and each node has one child per letter that extends it into another stored prefix. The prefix `ap` has children `app` and `apt`; `app` has child `appl`. This is the trie, and in Python each node is a dict from letter to child dict:

```text
 trie as a tree             same trie as nested dicts
      (root)                {"a":
        |                     {"p":
        a                       {"p": {"$": True,
        |                              "l": {"e": {"$": True}}},
        p                        "t": {"$": True}}}}
       / \
      p*  t*
      |
      l
      |
      e*
```

With this layout, every operation is a walk down from the root, one letter per step:

- **insert** walks the word, creating any missing child (`setdefault`), and sets `"$"` on the last node.
- **startsWith** walks the prefix; if a letter has no edge, the walk falls off and the answer is False; if it survives, True.
- **search** walks the word the same way and additionally requires `"$"` on the final node.

The end marker is the one subtle part. Without it, `search("app")` after inserting only `apple` would find the node for `app` (it exists, as a step towards `apple`) and wrongly say True. The node existing means "prefix of something"; the marker means "word". Those are different facts and the structure must store both.

Notice what the walk does to the N words: it never names them. At each step it follows one edge, and that one edge stands for every word sharing the prefix so far. Ten thousand `ap` words are checked by two dict lookups.

## Watch it work

Insert `apple`, `app`, `apt`, then query. These frames are the actual dicts the solution builds.

**Frame 1** — insert `apple`: five nodes are created in a chain, the last one marked.

```text
 root>a>p>p>l>e*
 {"a":{"p":{"p":{"l":{"e":{"$":T}}}}}}
 created: a, ap, app, appl, apple
```

**Frame 2** — insert `app`: the walk follows three existing edges, creates nothing, and only adds `"$"` to the node for `app`.

```text
 root>a>p>p*>l>e*
            ^ "$" added here; no new node
 {"a":{"p":{"p":{"l":{...},"$":T}}}}
```

**Frame 3** — insert `apt`: follows `a`, `p`, then `t` is missing under `ap`, so one node is created and marked.

```text
       a
       |
       p ----- t*   <- created
       |
       p*
       |
       l - e*
```

**Frame 4** — `search("app")` walks root>a>p>p and finds `"$"`: True. `search("ap")` walks root>a>p and finds no `"$"`: False.

```text
 query        path       last node   result
 app          a p p      has "$"     True
 ap           a p        no  "$"     False
```

**Frame 5** — `startsWith("ap")` reaches the `ap` node: True. `startsWith("b")` looks for `"b"` in the root, finds no edge, falls off: False.

```text
 (root) --b?--> missing   fell off -> False
 (root) -a-> -p-> node    exists   -> True
```

Across all frames, each node is reached by exactly one path and that path spells its prefix. Inserting never moves or deletes anything; it only adds edges and markers, so earlier answers stay true unless a later insert legitimately makes them true.

## Why it is correct

The invariant: *the node reached by walking s exists iff some inserted word has s as a prefix, and it carries `"$"` iff s itself was inserted.*

It holds for the empty trie: only the root exists (the empty string is a prefix of every word, vacuously fine), and no node is marked. An insert of w creates exactly the nodes for w's prefixes — each of which is now a prefix of an inserted word — and marks exactly the node for w. So both directions of both clauses remain true.

Given the invariant, `startsWith(p)` returns True exactly when the walk for p survives, which is exactly when some inserted word has prefix p. `search(w)` returns True exactly when the node for w exists and is marked, which is exactly when w was inserted.

## Cost

- **Time:** O(L) per insert, search and startsWith — one dict lookup (or creation) per character, independent of how many words are stored.
- **Space:** O(total characters inserted) in the worst case — each character creates at most one node; shared prefixes create none.

## Variations you will meet

- **Delete a word.** Unmark the end node, then walk back up removing nodes that became empty (no children, no marker). Recursion makes this tidy.
- **Count words with a prefix.** Store a counter at every node and increment it along the insert path; `countWordsStartingWith` is then a walk plus one read. This "payload on every node" idea returns in Word Squares and Autocomplete.
- **Node class instead of dicts.** `children = [None] * 26` and `is_end = False` uses less memory per node for a fixed lowercase alphabet and avoids marker collisions; the logic is identical.
- **Maximum XOR pair.** A trie over the 32 bits of each number; greedily walk toward the opposite bit. Same structure, two-letter alphabet.

## What to carry forward

A trie is a dict of dicts where a walk is a chain of lookups; node-exists means "prefix of something", marker means "word". The next problem uses this walk not as an API but as a tool: one walk checks a word against every root at once, and stopping at the first marker gives the shortest.
