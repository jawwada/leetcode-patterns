## Tries

> A trie is a dictionary of dictionaries: each node maps the next letter to a child node, so every word is a path from the root, and words that share a prefix share the path. A lookup costs one step per letter no matter how many words are stored, and one missing letter rules out every word with that prefix at once.

**Reach for it when** there are many words and the questions are about **prefixes** (starts with, autocomplete, the shortest root); when many words must be matched **at the same time** against one board, sentence or stream; or when a search has **wildcards**.

**In this repo:** `tries/` (8 problems) · bank: `practice/simple/31_implement_trie.py` · basics: `practice/simple/basics/tries/` (insert/search/starts-with, delete with pruning, autocomplete, wildcard search).

### The picture

```text
words: app, apple, apply, ape, bat                      * = a word ends here (the end flag)

               (root)
              /      \
             a        b
             |        |
             p        a
           /   \      |
         p*     e*    t*
         |
         l
       /   \
     e*     y*

search("app")         a -> p -> p*          the path exists AND ends on a *   -> True
search("appl")        a -> p -> p -> l      the path exists, but l has no *   -> False (just a prefix)
starts_with("appl")   a -> p -> p -> l      the path exists                   -> True
search("apt")         a -> p -> (no t)      every word starting with "apt" is ruled out in one step
```

Each node is a small object: a dict `children` (letter → node) and a flag `end`. The words never appear as strings; a word is the sequence of letters on the edges from the root to a node with `end = True`.

Why it is fast: the brute force keeps a list of N words and compares the query with each of them: O(N·L) per query (L = word length), re-reading shared prefixes once per word. The trie stores each shared prefix once, so a query walks one path: O(L), whatever N is. The second win is **pruning**: when a letter is missing, the whole subtree (every word with that prefix) is ruled out in one step. That is what makes Word Search II and Stream of Characters fast.

### From idea to code

**The idea in one sentence:** *walk the word down from the root one letter at a time: insert creates missing children, a query follows existing ones and stops at the first missing letter, and the end flag on the last node tells a whole word from a prefix.*

| Decision | Trie answer |
|---|---|
| **State**: what must I remember? | the root node; every node holds `children` (letter → node) and `end` (a word stops here); one finger `node` walks down |
| **Definition**: what exactly does each variable mean? | the node reached by spelling `s` exists ⇔ some inserted word starts with `s`; its `end` ⇔ `s` itself was inserted |
| **Invariant**: what is true at the end of every step? | after reading `word[:i]`, `node` is the node for the prefix `word[:i]` |
| **Step**: how does one letter change the state? | query: `node = node.children.get(ch)` and stop on `None`; insert: create the child if it is missing, then step |
| **Record**: when is the answer updated? | at the last node of an insert: `node.end = True` (or store the word, a count, an index); during a query: note the `end` flags you pass (shortest root, streams) |
| **Init**: starting values | `node = self.root` at the start of every operation |
| **Return**: what comes back? | search: `node is not None and node.end`; starts with: `node is not None`; collect: every word in the subtree below `node` |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "start at the top" | `node = self.root` |
| "follow letter `ch`, if it is there" | `node = node.children.get(ch)` (`None` if not) |
| "make the child if it is missing" | `if ch not in node.children: node.children[ch] = TrieNode()` |
| "a word ends here" | `node.end = True` |
| "a whole word, not just a prefix" | `node is not None and node.end` |
| "every word below this node" | a DFS over `node.children.items()`, adding one letter per level |
| "`.` matches any one letter" | `any(match(child, i + 1) for child in node.children.values())` |
| "rule out every word with this prefix" | `if ch not in node.children: return ...` |

The template. The tags are the seven decisions, and their order matters: `insert` creates a missing child *before* stepping into it, and sets the end flag (RECORD) only after the loop, because only the last node is where the word ends.

```python
class TrieNode:
    def __init__(self):
        self.children = {}                    # STATE: letter -> TrieNode
        self.end = False                      # STATE: a word stops exactly here


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root                      # INIT: every walk starts at the root
        for ch in word:
            if ch not in node.children:       # create the missing child first ...
                node.children[ch] = TrieNode()
            node = node.children[ch]          # STEP: ... then step down to it
        node.end = True                       # RECORD: mark the word's last node

    def _walk(self, s):                       # the node for prefix s, or None
        node = self.root
        for ch in s:
            node = node.children.get(ch)      # STEP: follow one edge
            if node is None:
                return None                   # no word starts with s
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end  # RETURN: a whole word, not just a prefix

    def starts_with(self, prefix):
        return self._walk(prefix) is not None # RETURN: the path exists


trie = Trie()
for w in ["app", "apple", "apply", "ape", "bat"]:
    trie.insert(w)
print(trie.search("app"), trie.search("appl"), trie.starts_with("appl"), trie.search("apt"))   # True False True False
```

**Try it**
- Delete `node.end = True` and rerun: the line prints `False False True False`. `search` now fails for every word (nothing is marked), while `starts_with` still works.
- Insert only `"apple"` into a fresh `Trie()`: `search("app")` is `False` but `starts_with("app")` is `True`. The end flag is the only difference between the two questions.
- Count the nodes: `count = lambda n: 1 + sum(count(c) for c in n.children.values())`, then `count(trie.root)` is 11 (the root plus 10 letters), while the five words have 19 letters in total. Shared prefixes are stored once.
- `trie.insert("")` marks the root itself: afterwards `trie.search("")` is `True`.

### Watch it work

`show` prints the trie as an outline (one letter per line, indented by depth, `*` = end flag). `trace_walk` follows a string down and reports where it stops.

```python
def show(node, depth=0):                      # the trie as an outline, * = a word ends here
    for ch in sorted(node.children):
        child = node.children[ch]
        print("    " * depth + ch + (" *" if child.end else ""))
        show(child, depth + 1)


def trace_walk(trie, s):
    node, steps = trie.root, []
    for ch in s:
        node = node.children.get(ch)
        steps.append(f"{ch} {'ok' if node else 'missing'}")
        if node is None:
            break
    verdict = "no word starts with it" if node is None else ("a word" if node.end else "only a prefix")
    print(f"{s!r:8} {' -> '.join(steps):30} {verdict}")


trie = Trie()
for w in ["app", "apple", "apply", "ape", "bat"]:
    trie.insert(w)
show(trie.root)
for s in ["app", "appl", "apt", "bat"]:
    trace_walk(trie, s)
```

**Try it**
- Add `print(len(node.children))` right after the `if node is None: break` lines and run `trace_walk(trie, "apple")`: 1, 2, 1, 2, 0. Each 2 is a fork where words part ways; 0 means no longer word continues.
- In `show`, drop the `sorted(...)`: under `a p` the `p` branch now comes before `e`, because a dict keeps insertion order and `"app"` was inserted before `"ape"`.
- Run `trie.insert("apt")`, then `show(trie.root)` and `trace_walk(trie, "apt")`: a `t *` appears under `a p`, and `'apt'` is now "a word".

### Where it goes wrong

1. **No end flag.** Without `end`, inserting `"apple"` makes `search("app")` succeed: a path existing only means "some word starts with this".
2. **Walking into the end marker.** In the dict-of-dicts shorthand (`node["$"] = True`), the marker sits among the children, so a DFS over the keys must skip `"$"`, or it tries to walk into `True`.
3. **Wildcard lengths.** A pattern matches only if a word ends exactly where the pattern ends: check `node.end` when `i == len(pattern)`, not "some word continues below".
4. **Stopping too late, or too early.** Replace Words wants the *shortest* root: return at the first `end` on the path. Word Search II must keep walking past a found word, because a longer word can continue from there (`"oat"` and `"oath"`).
5. **Emitting a word twice.** In Word Search II the same word can be spelled along two paths: remove it from its node when found.
6. **Not restoring the board.** Mark a cell as visited before recursing and put its letter back afterwards, or later paths see a corrupted board.
7. **Suffix questions on a forward trie.** "Does some word end at the newest letter of the stream?" needs a trie of *reversed* words, walked from the newest letter backwards.
8. **Deleting too much.** Deleting `"app"` must not remove the nodes `"apple"` still uses: prune a node only if it has no children and ends no word.

### Edge cases to say out loud

The empty string (it marks the root) · a word that is a prefix of another (`app`, `apple`) · inserting the same word twice · a query longer than every word · a pattern of only dots, or a dot at either end · deleting a word that isn't there · characters outside a–z (a dict handles any character).

```python
t = Trie()
assert not t.search("a") and not t.starts_with("a")            # empty trie
t.insert("a")
assert t.search("a") and t.starts_with("") and not t.search("")  # "" is a prefix of every word
t.insert("a")                                                  # a second insert changes nothing
assert len(t.root.children) == 1 and t.search("a")
t.insert("abc")
assert not t.search("ab") and t.starts_with("ab") and not t.starts_with("abcd")
t.insert("Ünï")                                                # any characters: children is a dict
assert t.search("Ünï") and not t.search("Ün")
print("edge cases pass")
```

**Try it**
- Predict, then run: `Trie().starts_with("")` is `True`, even on an empty trie. The walk takes zero steps and ends on the root, which always exists. Decide whether your problem wants that.
- Predict, then add: `t.insert(""); assert t.search("")`. The root itself becomes the end of a word.
- In a fresh trie insert `"apple"`, then `"app"`: `search("app")` flips from `False` to `True`, and the node count (the `count` lambda from the first Try it) stays 6. `"app"` only needed its end flag set.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Wildcard search** | `.` tries every child: a DFS over `(node, index)` that branches only at dots | 211 |
| **Delete** | clear `end`, then prune, bottom-up, the nodes with no children that end no word | basics |
| **Collect / autocomplete** | walk to the prefix's node, then DFS below it collecting words; or keep ranked candidates in every node | 642 |
| **Board backtracking + trie** | the grid DFS walks down the trie in lockstep; a letter that isn't a child prunes the path | 212 |
| **Shortest prefix** | stop at the first `end` on the path | 648 |
| **Suffixes of a stream** | insert words reversed; walk the newest letters backwards | 1032 |
| **Two-sided query** | insert `suffix + "#" + word` for every suffix; every node stores the best index | 745 |
| **Prefix → candidates** | every node lists the words below it; backtracking asks for the prefix of column k | 425 |

**Wildcards (211).** A letter follows exactly one edge; a `.` fans out to every child. That is a DFS over (trie node, position in the pattern), and it only branches at the dots.

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True

    def search(self, pattern):
        def match(node, i):                   # can pattern[i:] be spelled below node?
            if i == len(pattern):
                return node.end               # a word must end exactly here
            ch = pattern[i]
            if ch == ".":
                return any(match(child, i + 1) for child in node.children.values())
            child = node.children.get(ch)
            return child is not None and match(child, i + 1)
        return match(self.root, 0)


d = WordDictionary()
for w in ["bad", "dad", "mad"]:
    d.add_word(w)
print(d.search("pad"), d.search("bad"), d.search(".ad"), d.search("b.."), d.search("b."))   # False True True True False
```

**Try it**
- Change `return node.end` to `return True`: `d.search("b.")` becomes `True` although no two-letter word exists. The pattern ran out in the middle of `"bad"`.
- Put `print(repr(pattern[i:]))` as the first line of `match` and run `d.search(".ad")`: four lines, `'.ad'`, `'ad'`, `'d'`, `''`. `any` stops at the first child that works, so the `d` and `m` branches are never explored.
- Predict before running: `d.search("...")` is `True` and `d.search("....")` is `False`.

**Delete and autocomplete (basics, 642).** Both are a DFS below a node. Delete is bottom-up: each child tells its parent "I am useless now (no children, no word ends here), cut me off". Autocomplete walks down to the prefix's node and collects every word beneath it.

```python
def delete_word(trie, word):                  # returns True if the word was there
    if not trie.search(word):
        return False
    def remove(node, i):                      # returns True if the parent may cut `node` off
        if i == len(word):
            node.end = False                  # the word no longer ends here
        else:
            ch = word[i]
            if remove(node.children[ch], i + 1):
                del node.children[ch]         # prune the useless child
        return not node.children and not node.end
    remove(trie.root, 0)
    return True


def words_with_prefix(trie, prefix):          # every stored word that starts with prefix
    node = trie._walk(prefix)
    if node is None:
        return []
    found = []
    def collect(node, letters):
        if node.end:
            found.append("".join(letters))    # RECORD: a word ends here
        for ch in sorted(node.children):      # sorted children -> the words come out sorted
            letters.append(ch)
            collect(node.children[ch], letters)
            letters.pop()                     # backtrack
    collect(node, list(prefix))
    return found


t = Trie()
for w in ["car", "card", "care", "cat", "dog"]:
    t.insert(w)
print(words_with_prefix(t, "car"), words_with_prefix(t, "x"))   # ['car', 'card', 'care'] []
print(delete_word(t, "car"), words_with_prefix(t, "ca"))        # True ['card', 'care', 'cat']
print(delete_word(t, "cat"), sorted(t.root.children["c"].children["a"].children))   # True ['r']
```

**Try it**
- Then run `delete_word(t, "dog")` and print `sorted(t.root.children)`: `['c']`. The whole d-o-g branch is pruned, because no other word needed it.
- Replace `del node.children[ch]` with `pass` and rerun: `cat` is no longer a word, but `t.starts_with("cat")` is still `True`. A dead branch is left behind.
- `delete_word(t, "ca")` returns `False` and changes nothing: `"ca"` is only a prefix, not a stored word.

**Trie + backtracking on a board (212).** Searching the board once per word repeats the same board paths. Instead, walk the board once and the trie in lockstep: a step to a neighbouring cell is allowed only if its letter is a child of the current trie node, so a dead prefix is dropped after one wrong letter, for every word at once. This cell uses the common shorthand where a node is just a `dict` and the key `"$"` plays the end flag; here `"$"` stores the whole word, so a match can read it directly.

```text
 board        words: oath, pea, eat, rain
 o a a n
 e t a e      o -> a -> t -> h   follows the trie o -> a -> t -> h ($ = "oath"): found
 i h k r      o -> e             no "oe" in the trie: dropped after one step
 i f l v
```

```python
def find_words(board, words):
    root = {}
    for w in words:                           # dict-of-dicts trie; "$" holds the finished word
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    rows, cols, found = len(board), len(board[0]), []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent[ch]
        word = node.pop("$", None)            # RECORD once: popping stops duplicates
        if word is not None:
            found.append(word)
        board[r][c] = "#"                     # visited on this path
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                dfs(nr, nc, node)             # only letters the trie still allows
        board[r][c] = ch                      # un-mark: other paths may use this cell
        if not node:
            del parent[ch]                    # prune a branch with nothing left to find

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root:
                dfs(r, c, root)
    return found


board = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
print(sorted(find_words(board, ["oath", "pea", "eat", "rain"])))   # ['eat', 'oath']
```

**Try it**
- Replace `node.pop("$", None)` with `node.get("$")` and run `find_words([list("aa")], ["a"])`: `['a', 'a']`. Each cell spells the word again; popping reports it once.
- Delete the un-mark line `board[r][c] = ch` and rerun: only `['oath']`. The cells used by `"oath"` stay `"#"`, and `"eat"` needs the same `t`.
- Add `"oat"` to the word list: both `"oat"` and `"oath"` are found. The search keeps going *through* the node where `"oat"` was harvested.
- Delete the two pruning lines at the end of `dfs`: the answer is the same. Pruning only saves time, by stopping later cells from re-walking finished branches.

**Stop at the first end (648), and walk backwards (1032).** Replace Words walks each word down a trie of roots and stops at the first `end` it meets: the first one is the shortest root. Stream of Characters asks "does some word end at the newest letter?", which is a *prefix* question about the stream read backwards: insert every word reversed and walk the recent letters newest-first.

```python
def replace_words(roots, sentence):
    trie = Trie()
    for r in roots:
        trie.insert(r)
    def shortest_root(word):
        node = trie.root
        for i, ch in enumerate(word):
            node = node.children.get(ch)
            if node is None:
                return word                   # no root is a prefix: keep the word
            if node.end:
                return word[:i + 1]           # the FIRST end on the path is the shortest root
        return word
    return " ".join(shortest_root(w) for w in sentence.split())


class StreamChecker:
    def __init__(self, words):
        self.trie, self.longest = Trie(), max(map(len, words))
        for w in words:
            self.trie.insert(w[::-1])         # reversed: the newest letter is matched first
        self.recent = deque()

    def query(self, letter):
        self.recent.append(letter)
        if len(self.recent) > self.longest:
            self.recent.popleft()             # older letters can never be part of a match
        node = self.trie.root
        for ch in reversed(self.recent):      # newest -> oldest
            node = node.children.get(ch)
            if node is None:
                return False
            if node.end:
                return True                   # some word ends at the newest letter
        return False


print(replace_words(["cat", "bat", "rat"], "the cattle was rattled by the battery"))   # the cat was rat by the bat
sc = StreamChecker(["cd", "f", "kl"])
print([ch for ch in "abcdefghijkl" if sc.query(ch)])                                  # ['d', 'f', 'l']
```

**Try it**
- Add the root `"ca"` and predict the first replacement: `"the ca was rat by the bat"`. The shorter root is met first on the path.
- Insert the words forward (`self.trie.insert(w)`) and rerun: only `['f']`. A one-letter word reads the same in both directions; `"cd"` and `"kl"` are now looked for backwards.
- Delete the two `popleft` lines: the answers don't change, and the walk stays short (it can't go deeper than the longest word in the trie). Only the memory now grows with the stream.

**One prefix for two constraints (745), and a trie that feeds backtracking (425).** "Starts with `pref` and ends with `suff`" becomes a single prefix question if you insert, for every suffix of every word, the string `suffix + "#" + word`; every node on the way remembers the latest (largest) index that passed through it. Word Squares uses a trie the other way round: a backtracking search fills the square row by row, and row k must start with column k of the rows above, so the trie answers "which words start with this prefix?".

```text
 "apple" (index 0) is inserted 6 times:  "#apple", "e#apple", "le#apple", "ple#apple", ...
 f(pref = "ap", suff = "le")  ->  walk "le#ap"  ->  the index stored on that node: 0

 word square: row k = column k        w a l l
                                      a r e a       row 2 must start with "le":
                                      l e a d       column 2 of the rows "wall", "area"
                                      l a d y
```

```python
class WordFilter:
    def __init__(self, words):
        self.root = {}
        for index, word in enumerate(words):         # increasing index: a later word overwrites
            for k in range(len(word) + 1):           # every suffix, including the empty one
                node = self.root
                for ch in word[k:] + "#" + word:
                    node = node.setdefault(ch, {})
                    node["$"] = index                # every node on the path knows the best index

    def f(self, pref, suff):
        node = self.root
        for ch in suff + "#" + pref:
            if ch not in node:
                return -1
            node = node[ch]
        return node["$"]


def word_squares(words):
    n = len(words[0])
    root = {"$": list(words)}                        # every node lists the words below it
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {"$": []})
            node["$"].append(w)

    def starting_with(prefix):
        node = root
        for ch in prefix:
            if ch not in node:
                return []
            node = node[ch]
        return node["$"]

    squares, square = [], []
    def fill():
        k = len(square)
        if k == n:
            squares.append(square[:])
            return
        prefix = "".join(row[k] for row in square)   # column k of the rows so far
        for w in starting_with(prefix):
            square.append(w)
            fill()
            square.pop()
    fill()
    return squares


wf = WordFilter(["apple", "ample", "apply"])
print(wf.f("ap", "le"), wf.f("a", "e"), wf.f("b", ""))   # 0 1 -1
squares = word_squares(["area", "lead", "wall", "lady", "ball"])
print(len(squares), [sq[0] for sq in squares])          # 2 ['wall', 'ball']
for row in squares[0]:
    print(" ".join(row))                                # w a l l / a r e a / l e a d / l a d y
```

**Try it**
- `WordFilter(["ab", "ab"]).f("ab", "")` is 1: the later duplicate overwrote the index on every node of its path.
- Skip the empty suffix (`range(len(word))`): `wf.f("ap", "")` becomes -1 although `"apply"` starts with `"ap"`. Every query with `suff = ""` walks `"#..."`, and no key starts with `"#"` any more.
- Print `k, prefix, starting_with(prefix)` right after `prefix` is computed in `fill`: the prefixes `'r'`, `'e'` and `'de'` die at once, because no word starts with them.

### Say it in the interview

> "Checking the query against every word costs O(N·L) per query and re-reads shared prefixes. I'll store the words in a trie: one node per prefix, children in a dict, and an end flag. A query walks one path, O(L), and a missing letter rules out every word with that prefix at once. Space is O(total letters)."

While coding, point at the end flag ("this separates a word from a prefix") and at the early `return` on a missing child ("this is the pruning"). For board or stream problems, say what the trie lets you do *simultaneously*: "every word is checked at once, by one walk".

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Design Add and Search Words Data Structure | `tries/design_add_and_search_words_data_structure.py` | a letter follows one edge, `.` tries every child; match only if a word ends exactly where the pattern ends |
| Design Search Autocomplete System | `tries/design_search_autocomplete_system.py` | a cursor moves one edge per keystroke; each node keeps sentence counts; top 3 by (−count, sentence) |
| Implement Trie (Prefix Tree) | `tries/implement_trie_prefix_tree.py` · `practice/simple/31_implement_trie.py` | dict of children + end flag; search needs the flag, startsWith only the path |
| Prefix and Suffix Search | `tries/prefix_and_suffix_search.py` | insert `suffix#word` for every suffix; nodes store the latest index; query `suff#pref` |
| Replace Words | `tries/replace_words.py` | walk each word down the trie of roots; the first end flag is the shortest root |
| Stream of Characters | `tries/stream_of_characters.py` | trie of reversed words; walk the last L letters newest-first |
| Word Search II | `tries/word_search_ii.py` | the board DFS moves down the trie in lockstep; pop found words, prune empty branches |
| Word Squares | `tries/word_squares.py` | row k must start with column k so far; trie nodes list the words with each prefix |

### Self-check

1. After inserting only `"apple"`, why is `search("app")` false but `starts_with("app")` true?
<details><summary>Answer</summary>Both walks reach the node for "app", because "apple" passes through it. <code>starts_with</code> only needs the path to exist; <code>search</code> also needs the end flag on that node, and only the node for "apple" has it.</details>

2. In Word Search II, why pop the word from its node instead of collecting matches into a set?
<details><summary>Answer</summary>Popping reports each word exactly once, and it lets a branch become empty. Empty branches are then deleted, so later starting cells never re-walk prefixes whose words have all been found. A set would remove the duplicates but keep all that wasted walking.</details>

3. Why does Stream of Characters insert the words reversed?
<details><summary>Answer</summary>The question is whether a word ends at the newest letter, so the word's <em>last</em> letter must be matched first. Reading the stream backwards from the newest letter turns "suffix of the stream" into "prefix of the reversed stream", which a trie of reversed words answers with one walk.</details>

4. Why must WordFilter also insert the empty suffix, `"#" + word`?
<details><summary>Answer</summary>A query with <code>suff = ""</code> walks <code>"#" + pref</code>. That path exists only if some key starts with <code>"#"</code>, which is exactly the empty-suffix key. Without it, every prefix-only query returns -1.</details>
