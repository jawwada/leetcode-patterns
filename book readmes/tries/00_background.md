# Tries
*8 problems · Reading time ~24 min*

## The chapter

A trie stores a set of strings as a tree of characters, so every shared prefix is one shared path. This chapter
teaches prefix lookups, wildcard matching down a forking walk, using a trie to prune a backtracking search, rewriting
suffix questions as prefix questions, and storing payloads in nodes so that reaching a node is the answer.

Problems, in reading order:

1. [Implement Trie (Prefix Tree)](implement_trie_prefix_tree.md) · Medium
2. [Replace Words](replace_words.md) · Medium
3. [Design Add and Search Words Data Structure](design_add_and_search_words_data_structure.md) · Medium
4. [Word Search II](word_search_ii.md) · Hard
5. [Word Squares](word_squares.md) · Hard
6. [Prefix and Suffix Search](prefix_and_suffix_search.md) · Hard
7. [Stream of Characters](stream_of_characters.md) · Hard
8. [Design Search Autocomplete System](design_search_autocomplete_system.md) · Hard

## Why this chapter exists

Some questions are not about one string but about a whole dictionary of strings at once. "Is this word in the set?" a hash set answers fine. But "does any stored word start with these letters?", "which stored word is the shortest prefix of this one?", "which words could still be spelled if I extend this path by one more letter?" — a hash set cannot answer those without looking at every key. A trie can, and it answers them in time proportional to the length of the query, not the size of the dictionary.

The chapter's problems fall into five families:

- **Plain prefix lookups** (Implement Trie, Replace Words): store words, then walk one query down one path.
- **Pattern matching with wildcards** (Add and Search Words): the walk forks wherever the pattern says "any letter".
- **Search spaces guided by a trie** (Word Search II, Word Squares): a backtracking search over a grid or a square asks the trie after every step "can anything still match?", and dies early when the answer is no.
- **Rewriting the question into a prefix question** (Prefix and Suffix Search, Stream of Characters): suffixes, or suffix-plus-prefix pairs, are turned into prefixes of cleverly chosen strings so the same walk applies.
- **Tries that carry answers in their nodes** (Word Squares, Prefix and Suffix Search, Autocomplete): each node stores a payload — a list of words, a best index, a frequency map — so reaching the node *is* the answer.

## What it is

Take three words: `app`, `apple`, `apt`. Write them on top of each other and you notice they share their first two letters, and two of them share three. A trie stores that sharing literally: one node per distinct prefix, one edge per character.

```text
            (root)          prefix ""
              |
              a             prefix "a"
              |
              p             prefix "ap"
            /   \
           p*    t*         "app" is a word, "apt" is a word
           |
           l                "appl" (not a word)
           |
           e*               "apple" is a word

   *  = end marker: "a stored word ends at this node"
```

Two facts carry the whole chapter. First, a node does not store its letter in any useful sense; the letter lives on the edge from its parent, and the node *is* a prefix, namely the letters read on the path from the root. Second, a node existing means "some stored word starts with this prefix"; the star means "this exact prefix is itself a stored word". `ap` exists but has no star: it is a prefix of words but not a word.

In Python we do not build node classes. A node is a dict mapping a character to a child dict, and the end marker is a special key, `"$"`, that can never be a real letter. This is the memory layout of the drawing above, exactly as the solution files build it:

```text
root = {
  "a": {                         node for "a"
    "p": {                       node for "ap"
      "p": {                     node for "app"
        "$": True,               <- end marker: "app"
        "l": {                   node for "appl"
          "e": {"$": True}       node for "apple"
        }
      },
      "t": {"$": True}           node for "apt"
    }
  }
}
```

Every `{` is a node; every key that is a letter is an edge; `"$"` is the star. Walking the string `"app"` is the chain of lookups `root["a"]["p"]["p"]`. That one line is the most important thing to be able to picture: **a walk is a chain of dict lookups, one per character.**

Why bother? Count the work. Store `app`, `apple`, `apt` in a list and check whether anything starts with `ap`: you compare `ap` against all three words, re-reading the letters `a`, `p` three times. In the trie, `a` and `p` are stored once and read once. With a thousand words starting with `ap`, the list re-reads `ap` a thousand times; the trie still reads it once. Shared prefixes are stored once and therefore *checked* once. That is the whole saving.

How big does it get? The number of nodes is at most the total number of characters inserted, plus one for the root. It is usually far fewer, because every shared prefix collapses into one path:

```text
 words            total chars    trie nodes (excl. root)
 app,apple,apt    3+5+3 = 11     a,ap,app,appl,apple,apt = 6
 cat,car,cart     3+3+4 = 10     c,ca,cat,car,cart       = 5
 dog,cat          3+3   =  6     d,do,dog,c,ca,cat       = 6
                                 (no sharing: worst case)
```

So space is O(total characters) in the worst case, and the dict overhead per node is the real constant you pay.

## Operations and what they cost

Let L be the length of the string in the operation.

| Operation | Time | Why |
|---|---|---|
| insert(word) | O(L) | one dict lookup or creation per character, then set `"$"` |
| search(word) | O(L) | walk L edges, then check `"$"` at the last node |
| startsWith(prefix) | O(L) | walk L edges; existing at all is the answer |
| walk-until-first-marker | O(L) | stop at the first `"$"` met on the path (shortest stored prefix) |
| wildcard search | O(nodes visited) | each `.` tries every child; bounded by the trie size |
| list all words under a prefix | O(L + subtree size) | walk to the node, then DFS its subtree |
| read payload at a prefix | O(L) | walk, then read what the node stores (index, list, map) |

**Insert** `apt` into a trie holding only `app`. The walk reuses what exists and creates what is missing:

```text
 step  char  at node   action               trie after
 1     a     root      "a" exists, follow   root-a-p-p*
 2     p     "a"       "p" exists, follow   root-a-p-p*
 3     t     "ap"      "t" missing, CREATE  root-a-p-p*
                                                 \-t
 4     end   "apt"     set "$" = True            \-t*
```

In code that is `node = node.setdefault(ch, {})` per character, then `node["$"] = True`.

**Search** and **startsWith** share the same walk and differ only at the last node:

```text
 query           walk                 last node   answer
 search("app")   root>a>p>p           has "$"     True
 search("ap")    root>a>p             no "$"      False
 startsWith("ap")root>a>p             exists      True
 search("apz")   root>a>p> z missing  (fell off)  False
 startsWith("b") root> b missing      (fell off)  False
```

Falling off the tree — a missing edge — answers False for both. Reaching a node answers True for startsWith; search also needs the star.

**Wildcard search** (`.` = any letter) turns the walk into a depth-first search. A literal letter follows one edge; a `.` sends a scout down every edge:

```text
 pattern ".pt" on the trie above
 root --.--> a        only child is "a": one scout
 a    --p--> ap       literal: one edge
 ap   --t--> apt*     literal: one edge, "$" present -> True
```

**List everything under a prefix** is walk-then-DFS: reach the node for `ap`, then visit its whole subtree, collecting every node with a star: `app`, `apple`, `apt`. This costs the size of the subtree, which is why later problems cache the answer at each node instead.

## The invariant

**The node reached by walking a string s from the root exists if and only if some inserted word has s as a prefix; and it carries the end marker if and only if s itself was inserted.**

Every operation preserves this. Insert only creates nodes along the path of the word it inserts (each such node is a prefix of that word, so it is allowed to exist) and only marks the last one. Nothing else adds nodes. The two halves of the invariant are what search and startsWith read.

```text
 LEGAL (words app, apt)        ILLEGAL
     root                          root
      |                             |
      a                             a
      |                             |
      p                             p
     / \                           / \
    p*  t*                        p   t*     <- "app" inserted
                                              but no "$": search
                                              ("app") says False
     root
      |
      a*    <- star on "a", but "a" was never inserted:
              search("a") lies and says True
```

In later problems the invariant grows a third clause about payloads: "the payload at the node for s summarises exactly the words that pass through s" (their indices, their best index, their counts). The trickiest bugs in the hard problems are payloads that were not updated on every node along the path.

## How to picture it

Picture a tree fanning out downward from one root, with the words hanging off it as paths. A query is a finger placed on the root that traces letters downward. Three things can happen to the finger: it runs out of letters while sitting on a node (the prefix exists), it sits on a starred node (a word ends here), or the next letter has no edge and the finger falls off the tree (nothing stored continues this way).

```text
          root
          /  \
         a    b          finger tracing "apx":
         |    |            root -> a -> p -> (no x) FALLS OFF
         p    e*
        / \
       p*  t*
```

Hold onto the falling-off image. In every hard problem in this chapter, "fell off the trie" is the pruning step: the grid path dies, the square row is impossible, the stream has no match, the autocomplete cursor goes dead. The trie's value is not only finding things fast but *knowing early that nothing can be found*.

For the rewritten problems, add a second image: a word can hang from the trie more than once, in different spellings — reversed (stream), or rotated into `suffix#word` (prefix-and-suffix). The trie does not care what the strings mean; you choose strings so that your question becomes "walk this prefix".

## Advanced patterns

The operations above are what a trie *is*. The Hard problems in this chapter are won by what you do *with* it: how you walk it, what you store in it, and which strings you choose to put in it. Seven ideas cover all of them. Each builds on the invariant (a node is a prefix; a node exists only if some stored string continues that way) and turns it into a sharper tool.

### 1. The branching walk: a wildcard turns one path into a pruned DFS

**When it shows up.** A query that is not one exact string but a family of strings: a `.` that matches any letter, a `?`, a set of allowed letters per position, or "words within one edit of this".

**The intuition.** A plain walk follows one edge per character because the query names exactly one letter. A wildcard names many letters, so the walk becomes a depth-first search: at a `.`, send a scout down every child, and at a literal, follow one edge. The reason this is fast is that scouts die the moment their path leaves the trie. Compare it with expanding the pattern first: `...` over 26 letters names 17,576 strings, almost all of which are not prefixes of anything stored. The trie never generates those; it only generates the strings that are *still alive*, because the children of a node are exactly the letters some stored word continues with. The work is bounded by the number of trie nodes at depths reached, never by 26 to the power of the number of dots. Return as soon as any scout reaches a starred node at the end of the pattern, if the question is "does any word match?".

```text
 words bad dad mad cat     pattern "..t"
 depth:   1      2      3
 root -.-> b -.-> ba -t-> missing   scout dies
      -.-> d -.-> da -t-> missing   scout dies
      -.-> m -.-> ma -t-> missing   scout dies
      -.-> c -.-> ca -t-> cat*      -> True
 nodes visited: 10 (root + 9); strings "named": 26*26
```

**Where you'll use it.** Add and Search Words is exactly this. Beyond the chapter, the same branching walk powers "match with at most one mismatch" (Implement Magic Dictionary, LC 676), where the scout carries a budget of one wrong letter.

### 2. The lockstep walk: a trie riding along a search, and shrinking as it wins

**When it shows up.** A search over some other space (a grid, a graph, a sequence of choices) that spells strings as it goes, with *many* target words at once. Searching for each word separately repeats the same board paths once per word.

**The intuition.** Carry a trie pointer alongside the search state, and advance both by the same letter. The invariant is that the trie node always equals the spelling of the current path. That makes the trie a pruning oracle for every word at once: if the next cell's letter is not a child of the current node, no word can be completed through that cell, so the search never steps there. Store the whole word at its terminal node so reaching it hands you the answer. Then add the move that separates a good solution from a time-limit-exceeded one: when a word is found, *remove* it (pop the marker), and on the way back up, delete any node left with no children and no marker. The trie shrinks as words are found, so later starts no longer pay for words already collected; the search gets cheaper the more it succeeds.

```text
 board         words oath pea eat rain
  o a a n
  e t a e      trie before         trie after "oath" found
  i h k r       root                 root
  i f l v       |-o-a-t-h[oath]      |-p-e-a[pea]
                |-p-e-a[pea]         |-e-a-t[eat]
                |-e-a-t[eat]         |-r-a-i-n[rain]
                |-r-a-i-n[rain]
 path for oath: (0,0)o (0,1)a (1,1)t (2,1)h; h, t, a, o
 each left empty on the way back, so the o branch is deleted

 after "eat" is found the e branch goes too: found [oath, eat]
```

**Where you'll use it.** Word Search II is built on it. The same lockstep idea appears in Word Squares (the trie rides along the rows) and in Stream of Characters (the trie rides along the stream, backwards). Beyond the chapter: Concatenated Words (LC 472) walks the trie along one word and restarts at the root every time a marker is hit.

### 3. Forced-prefix backtracking: the trie as a candidate generator

**When it shows up.** A backtracking search where earlier choices pin down the *start* of the next choice: word squares, crossword fills, building a sentence where the next word must begin with something already fixed.

**The intuition.** In an ordinary backtracking problem you try every option at each level and test validity afterwards. Here the constraint is a prefix: after placing rows 0..k-1 of a word square, symmetry says row k must start with the letters already written in column k. So the question at each level is "which words start with this string?", and the trie answers it in one walk. Every word you try is consistent with everything placed so far, and if the walk falls off, the whole subtree of choices is dead before you enumerate any of it. The search never builds a partial answer that needs repair later. The trie is no longer a membership test at the end; it is the generator of the next level's branches.

```text
 words: area lead wall lady ball

 rows placed      column k read down    row k must start with
 w a l l          k=2: l, e        ->   "le"  -> lead
 a r e a
 l e a d          k=3: l, a, d     ->   "lad" -> lady
 l a d y
                  square found: wall area lead lady
                  (and ball area lead lady)
```

**Where you'll use it.** Word Squares. The forced prefix is the trick; the payload in the next pattern is what makes "list the candidates" cheap.

### 4. Payload on every node: make reaching the node *be* the answer

**When it shows up.** The question is not "does something start with p?" but "*which* things, how many, or the best one": all words with this prefix, the largest index, the top 3 by frequency, how many words share this prefix.

**The intuition.** Without help, answering "which words start with p" means walking to the node for p and then searching its whole subtree, which after a short prefix can be most of the trie. Instead, decide what summary of the subtree the query needs and write it on *every* node during insert, since you pass through every node of the word's path anyway. Insert costs stay O(L) plus the update, and every query becomes walk-then-read. The rule that makes it correct: the payload at the node for p must summarise exactly the stored strings that pass through p. So the update must happen on every node of the path, not only at the terminal, because queries stop mid-path. Choose the cheapest payload that answers the query: a count, a max index, a list of indices, a map of counts.

```text
 words app apple apt, payload = number of words through node

 (root)
   a  [3]
   p  [3]
  / \
 p*  t* [1]          query "how many start with ap?"
 [2]                 walk a,p -> read 3. No subtree DFS.
  |
  l  [1]
  e* [1]
```

**Where you'll use it.** Word Squares (list of word indices at each node), Prefix and Suffix Search (largest index at each node; overwriting works because words go in by increasing index), and Autocomplete (a sentence-to-count map at each node). Beyond the chapter, Sum of Prefix Scores of Strings (LC 2416) is the count payload above, summed along each word's path.

### 5. The reversed trie: turning "ends with" into "starts with"

**When it shows up.** Questions about suffixes: "does the stream end with one of these words?", "which words end with this?", matching from the right.

**The intuition.** A trie only answers questions that begin at the start of a string. But `s` ends with `w` exactly when `reverse(s)` starts with `reverse(w)`. So insert every word reversed and read the input backwards. On a stream this is especially clean: every match must end at the letter that just arrived, so every query starts fresh at the root with the newest letter and walks into the past. Two stops keep it cheap: stop at the first marker (some word just ended, answer True) and stop when you fall off (no word ends with what has been read). And since no trie path is longer than the longest word L, only the last L letters can ever be read: keep them in a bounded buffer.

```text
 words cd f kl   reversed trie: root -d-> d -c-> dc*
                                root -f-> f*
                                root -l-> l -k-> lk*
 stream:  a b c d          query('d'):
                ^ newest     root -d-> d -c-> dc*  -> True
          <- walk backwards (never more than L = 2 letters)
```

**Where you'll use it.** Stream of Characters. Beyond the chapter: Short Encoding of Words (LC 820) inserts reversed words and counts leaves, because a word that is a suffix of another disappears inside its path.

### 6. Combined keys: fold two conditions into one prefix

**When it shows up.** A query with two anchors, typically "starts with p *and* ends with s", where neither a forward nor a reversed trie alone can check both.

**The intuition.** The reflex from pattern 5, generalised: if the query does not have the shape "starts with", change what you store until it does. For each word, insert every `suffix + "#" + word`, including the empty suffix. Now the query `(p, s)` is the single prefix walk `s + "#" + p`: the part before `#` must equal `s` exactly (because `#` occurs once and never inside a word), so the word ends with `s`; and the part after starts with `p`, so the word starts with `p`. The separator is what stops the two halves bleeding into each other. Combine it with a payload (pattern 4) and the walk's last node holds the answer. The price is space: a word of length L produces L+1 keys of length up to 2L+1, so O(L^2) characters per word. That is fine when words are short (LeetCode 745 caps them at 7) and the queries are many.

```text
 keys for "apple" (index 0)   query f("ap", "le")
   apple#apple                  walk "le#ap"
    pple#apple                  root-l-e-#-a-p   reached:
     ple#apple                                   payload 0
      le#apple   <- matches
       e#apple
        #apple   <- empty suffix: f("ap","") = walk "#ap"
```

**Where you'll use it.** Prefix and Suffix Search. The alternative two-trie approach (a prefix trie and a suffix trie, each storing index lists, then intersecting) is worth knowing as a fallback when words are long.

### 7. The persistent cursor: a walk that pauses between calls

**When it shows up.** The query string arrives one character at a time across separate calls: autocomplete, type-ahead, a stream where the state must survive between keystrokes.

**The intuition.** The node for `p + c` is child `c` of the node for `p`. So if you keep the node for what has been typed so far, the next keystroke costs one dict lookup, not a fresh walk from the root. The cursor is just the walk's `node` variable promoted to a field of the object. When a keystroke has no edge, the cursor goes dead (`None`) and stays dead until the query ends, because no stored string can start with the typed text however many letters follow. That is "falling off" made permanent. Two things must stay separate: the cursor (where you are in the trie) and the typed buffer (what was typed), because when the cursor is dead the trie cannot tell you what was typed, and the end-of-query update needs the full string. On the terminator, insert the buffer (updating payloads along its path) and reset both.

```text
 stored: hello:3 help:2 hi:2 hey:1

 key  buffer  cursor          suggestions (top 3 at node)
 h    "h"     node h          hello help hi
 e    "he"    node he         hello help hey
 z    "hez"   None (dead)     []
 #    ""      root (reset)    [] ; "hez" inserted, count 1
```

**Where you'll use it.** Design Search Autocomplete System, together with a frequency-map payload (pattern 4). Beyond the chapter, Search Suggestions System (LC 1268) is the same cursor with a sorted list of at most 3 words stored at each node.

## Signals in a problem statement

Point toward a trie:

- "starts with", "prefix", "begins with", "shortest root", "autocomplete", "type-ahead", "suggestions as the user types".
- Many words searched together in one structure: "given a list of words, find all of them in the board".
- A pattern with single-character wildcards (`.` or `?`) against a dictionary.
- "ends with" or "suffix", especially on a stream: reverse the words into a trie.
- Building a string one letter at a time while needing to know whether it can still become a valid word (backtracking that should prune by prefix).
- Total characters around 10^5 to 10^6 and many queries: build once, answer each in O(L).
- Maximum XOR of two numbers: a trie over bits (same structure, alphabet {0,1}).

Counter-signals that point elsewhere:

- Only exact membership: use a `set` — it is simpler and faster.
- Substring anywhere (not prefix or suffix) in one long text: think rolling hash, KMP, or a suffix automaton.
- One pattern, one text: KMP or `str.find`; a trie only pays when there are many patterns.
- Lexicographic ordering of a static list: sorting plus `bisect` gives prefix ranges with no trie at all.

## Python toolbox

Nested dicts are the idiomatic trie. `setdefault` inserts and walks in one call:

```python
trie = {}
for w in words:
    node = trie
    for ch in w:
        node = node.setdefault(ch, {})   # follow or create
    node["$"] = True                     # or = w, or an index
```

A walk that returns None when it falls off:

```python
def walk(s):
    node = trie
    for ch in s:
        node = node.get(ch)
        if node is None:
            return None
    return node
```

Useful pieces: `defaultdict` gives a self-creating trie in one line (`T = lambda: defaultdict(T)`), but then a mere lookup creates nodes, which silently breaks the invariant — prefer `get` and `setdefault`. `heapq.nsmallest(k, items, key=...)` picks the top k from a node's payload without sorting it all. `collections.deque` with a bounded length holds the last L characters of a stream. Python's default recursion limit (1000) is never a problem for word-length recursion, but deep grid DFS on huge boards can approach it.

## Mistakes people make

1. **No end marker.** After inserting only `apple`, `search("app")` returns True. Fix: set `node["$"]` at the last node and check it in search.
2. **Marker collides with a letter.** Using `"*"` when the input may contain `*`. Fix: pick a key outside the alphabet, or use a node class with an `is_end` field.
3. **Iterating over the marker as a child.** A wildcard loop recurses into `node["$"]` (which is `True`, not a dict). Fix: skip the key `"$"` when looping over children.
4. **Lookups that create nodes.** Using `setdefault` or a `defaultdict` in search adds empty branches. Fix: search with `get` / `in`; only insert creates.
5. **Payload only at the terminal node.** A query that stops mid-path finds nothing. Fix: when a query can end anywhere, write the payload at every node along the inserted path.
6. **Not stopping at the first marker** when the question wants the shortest prefix match (Replace Words, Stream). Fix: return as soon as a `"$"` is seen on the walk.
7. **Building the trie forward when the question is about suffixes.** Fix: insert reversed words and walk the input backwards.
8. **Emitting the same word twice** in a grid search when two paths spell it. Fix: remove the word from its node when found (`node.pop("$")`).
9. **Unbounded history** in a stream problem. Fix: keep only the last max-word-length characters.
10. **Forgetting to reset per-query state** (an autocomplete cursor, a typed buffer) when the input says the query is over. Fix: reset both on the terminator.

## The journey ahead

The order follows one thread: the walk from root to node. First you build it, then you use it to stop early, then you let it branch, then you let it ride along another search, and finally you change what is stored so that questions which are not about prefixes become prefix walks.

### Building the walk

**Implement Trie.** The puzzle is small but sharp: why does `search("app")` need anything beyond "the path exists", and why do `search` and `startsWith` share all their code except one check at the end? Answering it gives you the three things every later problem reuses: nested dicts as nodes, the `"$"` end marker, and the walk that returns `None` when it falls off.

**Replace Words.** The naive idea is to test each word against every root with `startswith`, which re-reads the same letters once per root. The new idea is to use the walk as a tool rather than an API: one walk down the word tests it against every root at once, and the first marker met on the way is automatically the shortest root. Stopping early, which was a side detail in Implement Trie, becomes the whole answer here.

### Letting the walk branch

**Add and Search Words.** The tension is the `.`: a walk can only follow one edge, and expanding the pattern into every possible string is hopeless. The answer is pattern 1, the branching walk: a DFS that forks at wildcards and loses each fork the moment it falls off. It is the first time the trie prunes a search instead of just answering a lookup, and that idea runs through the rest of the chapter.

**Word Search II.** Searching the board once per word repeats the same paths thousands of times, so the question is how to look for all the words in one sweep. The DFS from the previous problem moves onto a grid and a trie pointer rides along each board path (pattern 2). The step that lifts it from correct to fast is making the trie shrink: pop each word when found and delete branches that empty out, so the search gets cheaper as it succeeds.

### Storing answers in the nodes

**Word Squares.** At first it looks like a brute-force search over all orderings of words. The observation that cracks it is that symmetry forces the first k letters of row k, so each level of the backtracking needs "all words with this prefix" (pattern 3). To make that query cheap, every node stores the indices of the words passing through it (pattern 4), the first time a node carries more than a marker.

**Prefix and Suffix Search.** Two conditions at opposite ends of a word seem to need two structures and an intersection. The trick is to change the stored strings instead: insert `suffix#word` for every suffix, and the two-sided query becomes one prefix walk (pattern 6). The payload from Word Squares shrinks to a single number, the largest index, written on every node of every key.

### Questions that arrive over time

**Stream of Characters.** Letters arrive one at a time and the question is whether the stream now *ends* with some word. Tracking every position where a match might have started works but is fiddly. Reversing the words (pattern 5) makes every match start at the newest letter, so each query is a fresh walk backwards over a buffer no longer than the longest word.

**Design Search Autocomplete System.** The finale combines nearly everything. A cursor that survives between keystrokes (pattern 7) makes each letter one dict step; a frequency map at every node (pattern 4) makes the ranking a top-3 pick instead of a subtree search; and the `#` terminator inserts the sentence along its whole path, creating nodes like Implement Trie did on day one. If you can build this one from a blank page, every problem before it is a special case.
