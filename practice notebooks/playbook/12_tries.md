## Tries

> A trie is a dictionary of dictionaries: each node maps the next letter to a child node, so every word is a path from the root, and words that share a prefix share the path. A lookup costs one step per letter no matter how many words are stored, and one missing letter rules out every word with that prefix at once.

[Trees](#s11) wrote one recursive function per problem and decided what goes down, what comes up and what is recorded on the side. A trie keeps the tree but writes a letter on every edge, so each node stands for a prefix and is a lookup you can resume one letter later.

**Reach for it when** there are many words and the questions are about **prefixes** (starts with, autocomplete, the shortest root); when many words must be matched **at the same time** against one board, sentence or stream; or when a search has **wildcards**.

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

Each node is a small object: a dict `children` from letter to node, and a flag `end`. The words never appear as strings; a word is the sequence of letters on the edges from the root to a node with `end = True`. A list `[None] * 26` per node is faster to index, but it costs 26 slots per node and handles only a–z, while a dict holds only the letters that occur, from any alphabet.

The brute force keeps a list of N words and compares the query with each of them: O(N·L) per query for words of length L, re-reading every shared prefix once per word. The trie stores each shared prefix once, so a query walks one path: O(L), whatever N is.

The second win is **pruning**: when a letter is missing, the whole subtree, every word with that prefix, is ruled out in one step. Pruning is what makes two later problems fast: Word Search II, which finds many words on one board of letters, and Stream of Characters, which asks after every new letter whether some word has just ended.

A set of words answers exact search in O(L) too, but prefix questions break it: the set would have to store every prefix of every word as its own string. For 1 000 random words of 5 to 12 letters that is 7 042 prefixes holding 41 293 characters, while the trie stores the same 7 042 prefixes as 7 042 one-letter nodes.

A set also hashes the whole prefix again on every query, while a trie node is a resumable lookup: from the node for "app", one dict step reaches "appl". That O(1) extension is what board, stream and autocomplete searches need.

### From idea to code

**The idea in one sentence:** *walk the word down from the root one letter at a time: insert creates missing children, a query follows existing ones and stops at the first missing letter, and the end flag on the last node tells a whole word from a prefix.*

The **State** is a tree of nodes hanging from `root`, each holding `children`, a dict from letter to node, and `end`, a flag for "a word stops here"; one finger, `node`, walks down. The **Definition** ties them together: the node reached by spelling `s` exists exactly when some inserted word starts with `s`, and its `end` is set exactly when `s` itself was inserted. The **Invariant** follows the finger: after reading `word[:i]`, `node` is the node for the prefix `word[:i]`.

A **Step** reads one letter: a query follows `node = node.children.get(ch)` and stops on `None`, and an insert first creates a missing child. The **Record** depends on the job: an insert sets `node.end = True` on the last node, and autocomplete also keeps the top three words on *every* node of the path; a query notes the `end` flags it passes, as the shortest root does. **Init** is `node = self.root`, and the **Return** is `node is not None and node.end` for search, `node is not None` for starts-with.

Implement Trie (208) asks for `insert(word)`, `search(word)` for a whole stored word, and `starts_with(prefix)` for any word that begins with the prefix: after inserting app, apple, apply, ape and bat, `search("app")` is True, `search("appl")` is False and `starts_with("appl")` is True. Both queries share one walk, `_walk`, which returns the node for a prefix or `None`. In `insert` the order is the point: a missing child is created *before* the step into it, and the end flag is set only after the loop, on the word's last node.

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
- Scale it up: `rng = random.Random(0)` and `words = ["".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(5, 12))) for _ in range(1000)]`. The set of every prefix, `{w[:i] for w in words for i in range(1, len(w) + 1)}`, holds 7042 strings with 41293 characters in total; a `Trie()` holding the same words has `count(t.root) - 1 == 7042` one-letter nodes.

### Watch it work

Two small tools make the trie visible. `show` prints it as an outline, one letter per line, indented by depth, with `*` where a word ends. `trace_walk` follows a string down and reports where it stops: on a whole word, on only a prefix, or at a missing letter that rules out every word beginning that way. The cell runs both on the five words of the picture.

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
- Run `trie.insert("ap")` and `show(trie.root)`: the line for the first `p` becomes `p *`, a star on an inner node. A word can end where others continue, which is why `end` is a flag and not "has no children". Then `trace_walk(trie, "")` prints "only a prefix": the empty string reaches the root.
- Run `trie.insert("apt")`, then `show(trie.root)` and `trace_walk(trie, "apt")`: a `t *` appears under `a p`, and `'apt'` is now "a word".

### Where it goes wrong

1. **No end flag.** Without `end`, inserting `"apple"` makes `search("app")` succeed: a path existing only means "some word starts with this".
2. **Walking into the end marker.** In the dict-of-dicts shorthand, `node["$"] = True` puts the marker among the children, so a DFS over `node.items()` reaches `True` and fails: `"$" in True` raises `TypeError: argument of type 'bool' is not iterable`. Skip the `"$"` key.
3. **Wildcard lengths.** A pattern matches only if a word ends exactly where the pattern ends: return `node.end` when `i == len(pattern)`. Returning `True` there makes `"b."` match `"bad"`.
4. **Stopping too late, or too early.** Replace Words replaces each word by its *shortest* root, so return at the first `end` on the path: with the roots `ca` and `cat`, `cattle` becomes `ca`, and a walk that keeps going answers `cat`. Word Search II must keep walking past a found word, because a longer word can continue from there: a search that stops at `"oat"` never finds `"oath"`.
5. **Emitting a word twice.** In Word Search II the same word can be spelled along two paths: on the board `[["a", "a"]]` the word `"a"` is reported twice unless it is removed from its node when found.
6. **Not restoring the board.** Mark a cell as visited before recursing and put its letter back afterwards, or later paths see a corrupted board: on the board of the Word Search II cell, `"eat"` is lost, because `"oath"` left its `t` marked.
7. **Suffix questions on a forward trie.** "Does some word end at the newest letter of the stream?" needs a trie of *reversed* words, walked from the newest letter backwards. A forward trie on `["cd", "f", "kl"]` fires only on `f`.
8. **Deleting too much.** Deleting `"app"` must not remove the nodes `"apple"` still uses: prune a node only if it has no children and ends no word.
9. **One dict shared by every node.** `children = {}` written as a class attribute (or `def __init__(self, children={})`) gives every node the *same* dict: after `insert("ab")`, `search("b")` is `True`, and so is `search("bbbbb")`. Create the dict inside `__init__`: `self.children = {}`.
10. **Reads that write.** With a `defaultdict` trie, `T = lambda: defaultdict(T)`, a read that does `node = node[ch]` creates the path it reads: on a trie holding `"cat"`, one `search("dog")` returns False but leaves d-o-g behind, and from then on `starts_with("dog")` is `True`. Read with `node.get(ch)` or `ch in node`.

### Edge cases to say out loud

The empty string (it marks the root) · a word that is a prefix of another (`app`, `apple`) · inserting the same word twice · a query longer than every word · a pattern of only dots, or a dot at either end · deleting a word that isn't there · characters outside a–z (a dict handles any character). The asserts below put each case to the `Trie` class.

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

Every variation keeps the letter-by-letter walk and changes one thing: how a query moves, what a node stores, or which way the words are read. The table is the lookup; the paragraphs below take the variations in turn, each with the problem it solves.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Wildcard search** | `.` tries every child: a DFS over `(node, index)` that branches only at dots | Design Add and Search Words Data Structure (211: search patterns in which `.` matches any letter) |
| **Delete** | clear `end`, then prune, bottom-up, the nodes with no children that end no word | remove one word and keep the others (basics) |
| **Collect / autocomplete** | walk to the prefix's node, then DFS below it collecting words | every stored word with a given prefix (basics) |
| **Record on every node of the insert path** | each node keeps what queries ending there need: the top 3 words, or sentence counts | Search Suggestions System (1268: the three smallest products after each typed letter), Design Search Autocomplete System (642: the top 3 past sentences for what is typed so far) |
| **Board backtracking + trie** | the grid DFS walks down the trie in lockstep; a letter that isn't a child prunes the path | Word Search II (212: every listed word that can be spelled on the board) |
| **Shortest prefix** | stop at the first `end` on the path | Replace Words (648: replace each word by its shortest root) |
| **Suffixes of a stream** | insert words reversed; walk the newest letters backwards | Stream of Characters (1032: does a word end at the newest letter) |
| **Trie over tokens** | children keyed by path parts or by bits | Design File System (1166: create paths and read their values), Design In-Memory File System (588: `ls`, `mkdir` and files, in [Design Problems](#s24)), Maximum XOR of Two Numbers (421: the largest XOR of a pair, a binary trie described in [Math, Bits & Geometry](#s22)) |
| *Second pass:* **Two-sided query** | insert `suffix + "#" + word` for every suffix; every node stores the best index | Prefix and Suffix Search (745: the largest index of a word with a given prefix and suffix) |
| *Second pass:* **Trie feeding a backtracking search** | every node lists the words that pass through it; the search asks for the words with a prefix | Word Squares (425: words whose rows read the same as their columns) |

Design Add and Search Words Data Structure (211) comes first because it changes only the query. It stores words and searches for patterns in which `.` matches any one letter: after adding bad, dad and mad, `.ad` and `b..` match and `pad` does not.

A letter follows exactly one edge, and a `.` fans out to every child, so the search is a DFS over (trie node, position in the pattern) that branches only at the dots. Each dot multiplies the work by the number of children: the worst case is O(26^d · L) for d dots, and on all 625 four-letter words over a–e, `"...z"` makes 156 calls, 1 + 5 + 25 + 125, before it fails.

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

Delete and autocomplete, two operations from the basics, come next because both are a DFS below a node. Delete is bottom-up: each child tells its parent "I am useless now, with no children and no word ending here, so cut me off". Autocomplete walks down to the prefix's node and collects every word beneath it. In the cell the trie holds car, card, care, cat and dog: the prefix `car` gives car, card and care, and after deleting car, the prefix `ca` gives card, care and cat.

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
            letters.pop()                     # FIX: backtrack
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
- After the cell, run `delete_word(t, "dog")` and print `sorted(t.root.children)`: `['c']`. The whole d-o-g branch is pruned, because no other word needed it.
- Replace `del node.children[ch]` with `pass` and rerun: `cat` is no longer a word, but `t.starts_with("cat")` is still `True`. A dead branch is left behind.
- Run `delete_word(t, "ca")`: `False`, and nothing changes, because `"ca"` is only a prefix, not a stored word.

Search Suggestions System (1268) moves the work from the query to the insert. After each typed letter it returns the three smallest products that start with what was typed: with the products mobile, mouse, moneypot, monitor and mousepad and the word `mouse`, the letters m and mo give mobile, moneypot and monitor. Walking the whole subtree at every keystroke is wasted work, because the answer for a prefix never changes.

So *store it on the node*: insert the products in sorted order, and every node on a product's path keeps the first three products that passed through it. A query is then one dict step per letter. This is the move that transfers: Design Search Autocomplete System (642) stores sentence counts on every node, and in the second pass below Prefix and Suffix Search (745) stores the best index and Word Squares (425) the list of words.

```python
def suggested_products(products, word):
    root = {}
    for p in sorted(products):                    # sorted: the first 3 to pass a node are its 3 smallest
        node = root
        for ch in p:
            node = node.setdefault(ch, {"$": []}) # STEP: walk or create the child
            if len(node["$"]) < 3:
                node["$"].append(p)               # RECORD on every node of the insert path
    out, node = [], root
    for ch in word:
        node = node.get(ch) if node else None     # once the prefix dies, it stays dead
        out.append(node["$"] if node else [])
    return out


products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
for i, suggestions in enumerate(suggested_products(products, "mouse")):
    print("mouse"[:i + 1], suggestions)       # m, mo: mobile moneypot monitor;  mou, mous, mouse: mouse mousepad
```

**Try it**
- Insert the products unsorted (drop `sorted`): the first line becomes `m ['mobile', 'mouse', 'moneypot']`. The first three to pass a node are only the three smallest if they arrive in sorted order.
- Run `suggested_products(["havana"], "tatiana")`: seven empty lists. The first letter already leaves the trie, and the guard keeps the prefix dead for every later letter.
- Replace the guarded step with `node = node.get(ch)` and query `"mxuse"`: `AttributeError: 'NoneType' object has no attribute 'get'`. After `x` the prefix is dead, and a dead prefix must stay dead.
- Write the same function without a trie: sort the products once, then for each prefix take `i = bisect.bisect_left(products, prefix)` and keep the next three that start with the prefix. It prints the same lines in O(log N) per letter with no trie at all, while the trie pays memory up front to answer in O(1) per letter.

Word Search II (212) matches many words at once against one board. It asks which words of a list can be spelled by moving between neighbouring cells, using each cell at most once per word: on the board below, `oath` and `eat` can be spelled, and `pea` and `rain` cannot. Searching the board once per word repeats the same board paths.

```text
 board        words: oath, pea, eat, rain
 o a a n
 e t a e      o -> a -> t -> h   follows the trie o -> a -> t -> h ($ = "oath"): found
 i h k r      o -> e             no "oe" in the trie: dropped after one step
 i f l v
```

Instead, walk the board once and the trie in lockstep: a step to a neighbouring cell is allowed only if its letter is a child of the current trie node, so a dead prefix is dropped after one wrong letter, for every word at once. The worst case is O(R·C·4·3^(L−1)) for words of length L, with 4 directions at the start and 3 after, since a path can't step back onto itself, and the pruning cuts most of it in practice.

This is [Backtracking](#s16) with a trie as the guide. Pick one representation for the interview: the class is clearer, and dict-of-dicts with `"$"` is shorter. This section uses both, and here `"$"` stores the whole word, so a match can read it directly.

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
        board[r][c] = "#"                     # STEP: visited on this path
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                dfs(nr, nc, node)             # only letters the trie still allows
        board[r][c] = ch                      # FIX: un-mark, other paths may use this cell
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

Two more problems change only where the walk stops and which way it reads. Replace Words (648) replaces every word of a sentence by its shortest root from a dictionary: with the roots cat, bat and rat, `the cattle was rattled by the battery` becomes `the cat was rat by the bat`. It walks each word down a trie of roots and stops at the first `end` it meets, because the first one is the shortest root.

Stream of Characters (1032) receives one letter at a time and asks, after each, whether some word ends at the newest letter: for the words cd, f and kl, the stream a to l answers True at d, f and l. That is a *prefix* question about the stream read backwards, so insert every word reversed and walk the recent letters newest-first. The cell writes both.

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

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Prefix and Suffix Search (745) builds a `WordFilter` once and then answers `f(pref, suff)`: the largest index of a word that starts with `pref` and ends with `suff`, or −1. For apple, ample and apply, `f("ap", "le")` is 0. The two constraints become one prefix question if you insert, for every suffix of every word, the string `suffix + "#" + word`, and every node on the way records the latest, largest index that passed through it.

```text
 "apple" (index 0) is inserted 6 times:  "#apple", "e#apple", "le#apple", "ple#apple", ...
 f(pref = "ap", suff = "le")  ->  walk "le#ap"  ->  the index recorded on that node: 0
```

Building costs O(W·L²) time and space for W words of length L: each word is inserted L + 1 times, and each key has up to 2L + 1 letters. Each query is one O(L) walk of `suff + "#" + pref`, and that walk is all `f` does.

```python
class WordFilter:
    def __init__(self, words):
        self.root = {}
        for index, word in enumerate(words):         # increasing index: a later word overwrites
            for k in range(len(word) + 1):           # every suffix, including the empty one
                node = self.root
                for ch in word[k:] + "#" + word:
                    node = node.setdefault(ch, {})
                    node["$"] = index                # RECORD on every node of the insert path

    def f(self, pref, suff):
        node = self.root
        for ch in suff + "#" + pref:
            if ch not in node:
                return -1
            node = node[ch]
        return node["$"]


wf = WordFilter(["apple", "ample", "apply"])
print(wf.f("ap", "le"), wf.f("a", "e"), wf.f("b", ""))   # 0 1 -1
```

**Try it**
- Run `WordFilter(["ab", "ab"]).f("ab", "")`: 1, because the later duplicate overwrote the index on every node of its path.
- Skip the empty suffix (`range(len(word))`): `wf.f("ap", "")` becomes -1 although `"apply"` starts with `"ap"`. Every query with `suff = ""` walks `"#..."`, and no key starts with `"#"` any more.
- Let the prefix and the suffix overlap: `wf.f("appl", "ple")` is 0. The key holds the whole word after the `#`, so shared letters are no problem.

<details><summary>Word Squares (425): a trie that feeds a backtracking search</summary>

Word Squares asks for every square of words, all of one length, that reads the same across and down, so row k must start with column k of the rows above it. A backtracking search fills the square row by row and asks the trie "which words start with this prefix?". Every node records the list of words that pass through it, so the question is one walk. For `["area", "lead", "wall", "lady", "ball"]` the squares are `wall area lead lady` and `ball area lead lady`.

```py
def word_squares(words):
    n, root = len(words[0]), {"$": list(words)}  # every node lists the words below it
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {"$": []})
            node["$"].append(w)
    squares, square = [], []
    def fill():
        if len(square) == n:
            squares.append(square[:])
            return
        node = root
        for ch in (row[len(square)] for row in square):   # column k of the rows so far
            node = node.get(ch)
            if node is None:
                return                                    # no word starts with this prefix
        for w in node["$"]:
            square.append(w)
            fill()
            square.pop()
    fill()
    return squares
```

</details>

### Say it in the interview

> "Comparing the query with every word costs O(N·L) per query. A hash set makes exact search O(L), but not prefix search. A trie stores each shared prefix once: one node per prefix, children in a dict, and an end flag. Insert, search and starts-with are O(L), space is O(total letters), and extending a prefix by one letter is one dict step."

While coding, point at the end flag ("this separates a word from a prefix") and at the early `return` on a missing child ("this is the pruning"). Be ready for the follow-ups:

- *Delete?* Clear the end flag, then prune bottom-up the nodes with no children and no end flag.
- *Top-k suggestions?* Store them on the nodes during insert (1268), or DFS below the prefix's node with a heap.
- *Memory?* A dict per node holds only the letters that occur; `[None] * 26` is faster but costs 26 slots per node and only handles a–z.
- *Word Search II?* O(R·C·4·3^(L−1)) worst case; found words are popped so each is reported once, and empty branches are pruned so they are never walked again.

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

4. Why a trie and not a set of words?
<details><summary>Answer</summary>A set handles exact search, but prefix questions would need every prefix stored as its own string (7 042 strings holding 41 293 characters for 1 000 random words, where the trie has 7 042 one-letter nodes), and every lookup would re-hash the whole prefix. A trie node is a resumable lookup: from the node for a prefix, one dict step extends it by a letter.</details>
