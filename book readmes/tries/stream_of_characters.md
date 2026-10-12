# Stream of Characters
*LeetCode 1032 · Hard · Pattern: Reversed trie walked backwards over a bounded recent-history buffer · Reading time ~9 min*

## The problem

StreamChecker(words) is fed one character at a time through query(letter), which returns True when some word is a
suffix of everything queried so far.

```text
Example: words=["cd","f","kl"] with the stream a..l returns True
  exactly at d, f and l.
```

## What the problem is really asking

You are given a list of words at construction. Then letters arrive one at a time through `query(letter)`. After each letter, answer: does any word in the list match the *end* of everything received so far? In other words, is some word a suffix of the stream?

Each answer is a boolean, and there can be 4 · 10^4 queries against up to 2000 words of length up to 200. The stream is unbounded. What makes it hard is that the question is about suffixes of a string that keeps growing at its end — the very place a normal trie walk would need to *finish*, not start.

```text
 words: ba, cab
 stream:  c     a     b     a     x
 answer:  F     F     T     T     F
                      ^     ^
                "cab" ends   "ba" ends
```

## Do it by hand first

The third letter arrives: the stream is `cab`. To check for a match, where do your eyes go? Not to the start of the stream. They go to the newest letter, `b`, and read leftwards: `b`, then `a`, then `c`. Any matching word must end in `b`, so you first ask "does any word end in `b`?", then "end in `ab`?", then "end in `cab`?".

```text
 stream:   c  a  b
                 ^ newest
 read leftward:  b -> a -> c
 words ending in   b:  ba? no ("ba" ends in a) cab? yes
 words ending in  ab:  cab
 words ending in cab:  cab   complete -> True
```

Your hand read the stream backwards and narrowed the candidate words letter by letter. That is exactly a trie walk — over the words written backwards. You also never needed to look further back than the length of the longest word, here 3.

## The first honest attempt

Keep the whole stream as a string. On each query, append the letter and check `stream.endswith(w)` for every word. O(W · L) per query, and the stream string grows forever.

```text
 query 'b' : endswith("ba")? endswith("cab")?
 query 'a' : endswith("ba")? endswith("cab")?
 query 'x' : endswith("ba")? endswith("cab")?
             ^^^^^^^^^^^^^^^
             every word, every time, even when
             no word ends in the new letter 'x'
```

Two wastes. First, all W words are checked independently, though most cannot match the newest letter at all, and words sharing endings re-read the same letters. Second, the stream is stored in full even though only its last L characters can ever be part of a match (no word is longer than L).

## The turning point

**Claim: a word is a suffix of the stream iff the stream read backwards from the newest letter starts with the word reversed; so insert every word reversed into a trie and, on each query, walk it while reading the stream backwards.**

This is just the identity "s ends with w ⇔ reverse(s) starts with reverse(w)". Reversal turns the suffix question into a prefix question, and prefix questions are what tries answer. The newest letter is the first letter of the reversed stream, so it is always the first edge taken from the root. That is perfect for a stream: every query starts fresh at the root with the letter that just arrived.

```text
 words      reversed     reversed trie
 ba    ->   ab               (root)
 cab   ->   bac              /    \
                            a      b
                            |      |
                            b*     a
                                   |
                                   c*
```

Why not keep a forward trie and walk it as letters arrive? That is the natural second idea, and it works, but notice what it requires. A match could start at *any* earlier position, so you must keep a set of active pointers — one for every position where a word might have started — and advance all of them on every letter. Each query costs the number of live pointers, up to L, plus the bookkeeping of creating and discarding them. The reversed trie does the same work with no state between queries except the buffer: it simply re-reads the last few letters from scratch each time, starting where every match must end. Re-reading at most L letters is cheap, and it removes a whole class of bugs.

Three details turn this into the full algorithm:

1. **Stop at the first marker.** While walking backwards, as soon as a node has `"$"`, some word has just been completely matched. Return True — do not keep walking hoping for a longer one; one match is enough.
2. **Stop when you fall off.** If the next older letter has no edge, no word ends with the letters read so far, and none can with more. Return False.
3. **Bound the history.** Only the last `max_len` letters can ever be read by a walk, because no trie path is longer than the longest word. Keep them in a `deque` and drop the oldest when it exceeds `max_len`. Space becomes O(L), and the walk is never longer than L.

The invariant: *after k backward steps, the current node is the node for the last k stream letters, reversed* — so it exists iff some word ends with those k letters.

## Watch it work

Words `ba`, `cab`; `max_len = 3`. The deques and answers below are what the solution produces.

**Frame 1** — `query('c')`: buffer `[c]`. Walk from newest: `c` is not a child of the root. Fall off: False.

```text
 buffer: c            walk: root -c-> missing
         ^ newest     -> False
```

**Frame 2** — `query('a')`: buffer `[c, a]`. Walk: `a` exists (node `a`, no marker); next older is `c`, but node `a` has only child `b`. Fall off: False.

```text
 buffer: c a          walk: root -a-> a -c-> missing
           ^          -> False
```

**Frame 3** — `query('b')`: buffer `[c, a, b]`. Walk `b` → `ba` → `bac`, which carries `"$"`: the word `cab` just ended. True.

```text
 buffer: c a b        walk: root -b-> b -a-> ba
             ^                -c-> bac*  -> True
 depth:  3 2 1
```

**Frame 4** — `query('a')`: the buffer would be 4 long, so `c` is dropped: `[a, b, a]`. Walk `a` → `ab`, marked: the word `ba` just ended. True after only 2 steps; the oldest `a` is never read.

```text
 buffer: a b a        dropped: c (len > 3)
             ^        walk: root -a-> a -b-> ab*
                      -> True
```

**Frame 5** — `query('x')`: buffer `[b, a, x]`. `x` is not a child of the root. False immediately — one dict lookup, no matter how many words there are.

```text
 buffer: b a x        walk: root -x-> missing
             ^        -> False
```

Across frames, the buffer never exceeded 3 letters, each walk started at the root with the newest letter, and each walk ended the moment it hit a marker or fell off.

## Why it is correct

The reversed trie satisfies the usual invariant on reversed words: the node for string r exists iff some word, reversed, starts with r — that is, iff some word ends with reverse(r). The node is marked iff reverse(r) is itself a word.

On a query, the walk reads r = last 1 letter, last 2 letters reversed, and so on. If it hits a marked node at depth k, the last k letters of the stream form a word: return True is correct. If it falls off at depth k, no word ends with the last k letters, hence no word of length ≥ k is a suffix; shorter words would have been detected at a marker earlier. If the buffer runs out, every word of length ≤ len(buffer) was checked and none matched. Dropping letters older than `max_len` is safe because no word can reach them. Therefore the answer is True exactly when some word is a suffix of the stream.

## Cost

- **Query:** O(L) where L is the longest word — at most L backward steps, each one dict lookup. Independent of W.
- **Build:** O(total word characters).
- **Space:** O(total word characters + L) — the trie plus a bounded buffer.

Compared with the brute force's O(W · L) per query and unbounded memory, both the W factor and the growing stream are gone.

## Variations you will meet

- **Aho–Corasick.** A forward trie with failure links keeps one pointer that advances one edge per letter: O(1) amortised per query and reports *all* matches. It is the industrial answer; the reversed trie is the interview answer, simpler to write and fast enough for L ≤ 200.
- **Report which word matched, or all of them.** Store the word at its terminal node; to report all, keep walking after the first marker until you fall off.
- **Suffix queries on a fixed set of strings.** Same reversal trick without a buffer — the "ends with" half of Prefix and Suffix Search could be done this way.
- **Longest word that is a suffix.** Do not stop at the first marker; remember the deepest marker seen before falling off.

## What to carry forward

Suffix matching is prefix matching on reversed strings; for a stream, keep only the last L letters and walk the reversed trie from the newest letter backwards. The final problem also follows a stream of keystrokes through a trie, but it keeps a persistent cursor that moves forward and reads ranked answers stored at each node.
