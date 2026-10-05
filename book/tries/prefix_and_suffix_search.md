# Prefix and Suffix Search
*LeetCode 745 · Hard · Pattern: Trie over "suffix#word" rotations, max index stored per node · Reading time ~10 min*

## The problem

WordFilter(words) is built once, and f(pref, suff) returns the largest index i such that words[i] starts with pref and
ends with suff, or -1 if there is none.

```text
Example: words=["apple"] gives f("a","e") = 0 and f("b","") =
  -1.
```

## What the problem is really asking

You are given a word list once, at construction. Then many queries arrive, each `f(pref, suff)`: return the largest index i such that `words[i]` starts with `pref` and ends with `suff`, or −1 if none does. Either string may be empty, and the prefix and suffix may overlap inside the word.

The answer is a single index. The word list never changes, and there can be up to 10^4 queries, so the real goal is to pay once at construction and make each query proportional to the query's length only. What makes it hard is that the constraint has two ends. A trie answers "starts with" beautifully; "ends with" needs a reversed trie; but "both at once, and the largest index" is not a walk in either.

```text
 words: [ape, apple]      index 0: ape   index 1: apple
 f("ap", "e")   -> 1   (both qualify; take larger)
 f("ap", "pe")  -> 0   (only "ape" ends in "pe")
 f("b",  "")    -> -1  (nothing starts with "b")
```

## Do it by hand first

For `f("ap", "pe")`, you would look at each word and check both ends.

```text
 index  word    starts "ap"?  ends "pe"?   both?
 1      apple   yes           no ("le")    no
 0      ape     yes           yes          yes  -> 0
 scan from the back so the first hit is the largest
```

Your hand did two lookups per word, one per end, and combined them. If you had a prefix index (a trie) and a suffix index (a reversed trie), you would get two *sets* of indices, `{0, 1}` and `{0}`, and intersect them. That works, but notice the cost: intersecting sets that may each hold thousands of indices, on every query. What your hand kept track of was a *pair* of conditions. The breakthrough will be to stop treating it as a pair.

## The first honest attempt

Scan from the last index down, return the first word with `startswith(pref) and endswith(suff)`. O(W · L) per query.

```text
 query 1: f("ap","e")   checks apple, ape ...
 query 2: f("ap","x")   checks apple, ape ... again
 query 3: f("ap","e")   checks apple, ape ... AGAIN
            ^^^^
            the same prefix test on the same word,
            once per query, forever
```

The words never change, yet every query re-derives which words start with `ap`. With 10^4 words and 10^4 queries that is 10^8 string comparisons. The two-trie-plus-intersection idea improves the lookups but still pays O(W) per query in the intersection. The waste to kill: anything per query that scales with W.

## The turning point

**Claim: insert, for every word, the strings `suffix + "#" + word` for every suffix (including the empty one); then `f(pref, suff)` is exactly the prefix query `suff + "#" + pref` on that trie.**

Justify it in both directions. Suppose `words[i]` ends with `suff` and starts with `pref`. Then `suff` is one of its suffixes, so the key `suff + "#" + words[i]` was inserted, and since `words[i]` starts with `pref`, that key starts with `suff + "#" + pref`. Conversely, if some inserted key `s + "#" + w` starts with `suff + "#" + pref`, then because `#` occurs exactly once in the key and never in a word, the part before `#` must be exactly `suff` — so `w` ends with `suff` — and the part after must start with `pref`. The separator is what keeps the two halves from bleeding into each other.

```text
 keys for "ape" (index 0)       keys for "apple" (index 1)
   ape#ape                        apple#apple
    pe#ape                         pple#apple
     e#ape                          ple#apple
      #ape   <- empty suffix         le#apple
                                      e#apple
                                       #apple
 query f("ap","pe") = walk "pe#ap"
```

So the pair of conditions collapsed into a single prefix — one walk. That handles "does some word qualify?". For "the largest index", give every node a payload: the largest index of any word whose keys pass through it. Since we insert words in increasing index order, a plain overwrite (`node["$"] = index` at every node on the path) leaves the maximum. The answer is then whatever is written on the node where the walk ends.

The payload must be on *every* node, not just terminal ones, because queries end mid-key: `pe#ap` is a prefix of `pe#ape`, ending one letter short of its terminal.

Two edge cases fall out of the construction rather than needing code. Overlap: `f("apple", "apple")` becomes the walk `apple#apple`, which is literally one of the inserted keys, so the query works even though prefix and suffix cover the same letters. And the separator: any character outside the alphabet works (`#`, or `{`, which is the letter after `z` in ASCII and lets you use a 27-slot array). If you picked a separator that could appear inside a word, the "part before the separator" would no longer be well defined, and the reverse direction of the proof would break.

It is worth pausing on *why* this rewrite is the right move rather than a trick to memorise. A trie can answer exactly one kind of question: "which stored strings start with this?". Whenever a query is not of that shape, ask whether you can change the stored strings so that it is. Here the query had two anchors at opposite ends; rotating each word so its end comes first put both anchors at the front. The next problem uses the same reflex with a simpler rotation: full reversal.

Why include the empty suffix? Because `f("ap", "")` must work, and it becomes the walk `#ap`, which exists only if you inserted the `#word` keys.

## Watch it work

All indices below were read from the solution's trie.

**Frame 1** — insert the 4 keys of `ape` (index 0). Every node created is stamped `0`.

```text
 root
  a0-p0-e0-#0-a0-p0-e0        ape#ape
  p0-e0-#0-a0-p0-e0           pe#ape
  e0-#0-a0-p0-e0              e#ape
  #0-a0-p0-e0                 #ape
```

**Frame 2** — insert the 6 keys of `apple` (index 1). Shared nodes are overwritten to `1`, new nodes are stamped `1`. Shown: the parts the queries will use.

```text
 e1-#1-a1-p1-e0     e#ape shares "e#ap" with e#apple:
             \p1-l1-e1        those nodes now say 1
 p1-e0-#0-a0-p0-e0  pe#ape: only "p" is shared
   \p1 ... \l1 ...  (pple#apple, ple#apple branch off)
 #1-a1-p1-e0        #ape / #apple share "#ap"
          \p1-l1-e1
```

**Frame 3** — `f("ap", "e")`: walk `e # a p`. Every node exists; the last one says `1`.

```text
 walk  e   #   a   p
 index 1   1   1   1   -> answer 1 (apple)
```

**Frame 4** — `f("ap", "pe")`: walk `p e # a p`. The `p` node says 1, but `pe` exists only through `pe#ape`, stamped 0.

```text
 walk  p   e   #   a   p
 index 1   0   0   0   0   -> answer 0 (ape)
```

**Frame 5** — `f("b", "")`: walk `# b`. The `#` node exists (index 1), but it has only an `a` child. The walk falls off.

```text
 walk  #   b
 index 1   MISSING          -> answer -1
```

Across the frames, each node's number was the largest index among words whose keys pass through it, and every query was one walk of length `len(suff) + 1 + len(pref)`.

## Why it is correct

Two invariants after construction.

1. *The node for string q exists iff some word i has a key starting with q* (the standard trie invariant, applied to the keys).
2. *The payload at that node is the maximum such i.* Each key insertion writes its word's index at every node on its path; words are processed in increasing index order, so the last write to any node is from the largest index whose keys pass through it.

By the claim above, the words satisfying `f(pref, suff)` are exactly those with a key starting with `q = suff + "#" + pref`. If none, invariant 1 says the walk falls off and we return −1. Otherwise invariant 2 says the payload is the largest qualifying index. Duplicated words are handled automatically: the later copy overwrites with its larger index.

## Cost

- **Build:** O(W · L²) time and space — each word of length L produces L+1 keys of length up to 2L+1. With L ≤ 7 (the LeetCode limit) this is tiny per word.
- **Query:** O(len(pref) + len(suff)) — one walk, one read.
- **Two-trie alternative:** O(W · L) build, but O(W) per query for the intersection — worse when queries are many.

The trade is deliberate: spend memory quadratic in word length to make each query independent of W.

## Variations you will meet

- **Hash map of all (prefix, suffix) pairs.** For each word, store `map[(p, s)] = i` for every prefix p and suffix s: O(W · L²) entries, O(1) query after building the pair. Same trade, simpler code; equally accepted.
- **Two tries with sorted index lists.** Store each node's indices sorted; walk both tries, then intersect the two lists from the large end. Uses O(W · L) memory, slower queries; better when words are long.
- **Smallest index instead of largest.** Insert in decreasing index order, or write only when the node has no payload yet.
- **Contains-substring queries.** Insert every suffix of every word (a suffix trie); "contains x" becomes "some suffix starts with x".

## What to carry forward

When a query constrains both ends of a word, rewrite the stored strings so the query becomes one prefix (`suffix#word`), and keep the answer in every node along the path. The next problem also needs suffixes, but of a stream that never stops; it gets there by reversing the words and walking the input backwards.
