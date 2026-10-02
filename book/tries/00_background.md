# Tries
*8 problems · Reading time ~16 min*

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

1. **Implement Trie** builds the structure, the end marker, and the walk. Everything later reuses these three things.
2. **Replace Words** uses the walk as a tool rather than an API: one path checks a word against every root at once, and stopping at the first marker gives the shortest.
3. **Add and Search Words** turns the walk into a DFS: a wildcard forks the search, and the trie prunes every fork that cannot match.
4. **Word Search II** moves that DFS onto a grid. The trie becomes a guide that prunes board paths, and it shrinks as words are found so dead branches are never re-walked.
5. **Word Squares** stores a payload in every node (the words passing through it), so a prefix question inside a backtracking search returns its candidates in one walk.
6. **Prefix and Suffix Search** rewrites a two-sided question into a single prefix by inserting `suffix#word` keys, and stores the best index at every node.
7. **Stream of Characters** turns suffix matching into prefix matching with a reversed trie, walked backwards over a buffer bounded by the longest word.
8. **Autocomplete** closes the chapter by combining it all: a persistent cursor that steps one edge per keystroke, per-node frequency maps as payloads, a top-3 selection, and updates that flow down a whole path.
