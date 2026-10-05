# Implement Trie (Prefix Tree) (LeetCode 208)

**Area:** tries · **Difficulty:** Medium · **Key operations:** walk one node per character, create the missing child on insert, end flag, prefix walk

## Problem

Design a trie supporting `insert(word)`, `search(word)` (is this exact word stored?) and `startsWith(prefix)` (does some stored word begin with this prefix?). The practice script drives one trie with a list of `(op, string)` pairs and returns the boolean results of the `search` and `startsWith` calls in order.

## Example

```
insert "apple"
search "apple"      -> True
search "app"        -> False   (a prefix of a stored word, not a stored word)
startsWith "app"    -> True
insert "app"
search "app"        -> True
result: [True, False, True, True]
```

## Brute force

Keep the inserted words in a set. `search` is a set lookup; `startsWith(p)` is `any(w.startswith(p) for w in words)`.

O(1) insert and search, but O(N · L) per prefix query over N words of length up to L. The wasted work: words sharing a prefix (`apple`, `apply`, `app`) are compared against the query letter by letter, once per word. The shared letters are re-read N times instead of once.

## From brute force to optimal

Store each shared prefix once. A tree whose edges are labelled with characters does exactly that: the path `a -> p -> p` is shared by every word starting with `app`; `apple` and `apply` only branch after it. Any query then follows at most `len(query)` edges, however many words are stored.

`startsWith` asks "can I walk the whole prefix?". `search` asks the same and additionally "is the node I land on marked as the end of a word?". That end flag is the only thing that separates a stored word from a mere prefix of one. The invariant: the node reached by walking `s` exists iff some inserted word has `s` as a prefix.

## Intuition

A trie is a dictionary of dictionaries keyed by character, with a flag on each node saying "a word ends here". Walking a string is a chain of lookups, one per character; inserting creates the missing links on the way and plants the flag at the end. Picture the words as roads fanning out from a single root: `app`, `apple` and `apply` share the trunk a-p-p and split afterwards. A query is a finger tracing one road. If the finger runs off the map, the answer is False. `startsWith` stops there; `search` also checks for the flag at the final junction.

## Walkthrough

`at p: create child c` means the node spelling `p` had no child `c`, so insert made one. `*` marks an end flag in the picture.

```
insert('apple')
    at '':     create child 'a'   walk to 'a'       end=False
    at 'a':    create child 'p'   walk to 'ap'      end=False
    at 'ap':   create child 'p'   walk to 'app'     end=False
    at 'app':  create child 'l'   walk to 'appl'    end=False
    at 'appl': create child 'e'   walk to 'apple'   end=False
    mark end at 'apple'          trie:  a - p - p - l - e*

search('apple')
    walk a, ap, app, appl, apple   end=True   -> whole word walked and flagged -> True

search('app')
    walk a, ap, app                end=False  -> walked, but no flag at 'app'  -> False

startsWith('app')
    walk a, ap, app                           -> whole prefix walked           -> True

insert('app')
    walk a, ap, app (all exist, nothing created)
    mark end at 'app'            trie:  a - p - p* - l - e*

search('app')
    walk a, ap, app                end=True   -> True

result: [True, False, True, True]
```

Had we asked `startsWith('apl')`: walk `a`, then at `'a'` there is no child `l`, the path breaks, False.

## Steps

1. A node is `children: dict[char -> node]` plus `end: bool`. Start with an empty root.
2. For each operation set `node = root`, `found = True`.
3. For each character: if it is not a child of `node`, then for `insert` create it, otherwise set `found = False` and stop. Step into the child.
4. `insert`: set `node.end = True` on the last node.
5. `search`: result is `found and node.end`. `startsWith`: result is `found`.

## Complexity

Every operation is O(L) for a string of length L, independent of how many words are stored. Space is O(total characters inserted) in the worst case; shared prefixes are stored once.

## Pitfalls

- **`search` without the end flag.** Walking the whole word only proves it is a prefix of a stored word. After inserting only `apple`, `search('app')` must be False.
- **`startsWith` with the end flag.** The symmetric slip turns `startsWith` into `search`: `startsWith('app')` would return False after inserting `apple`.
- **Looking up the character in `root.children` instead of `node.children`.** Every lookup then only sees first letters; worse, inserting `app` after `apple` recreates the child `p` under `a` and silently drops `apple`.
- **Forgetting to reset `node = root` per operation.** The second operation would start walking from wherever the first one ended.
- **Using the children dict itself as the end marker** (e.g. an empty dict means "word ends"). `app` stored inside `apple` has children and would never be found; use an explicit flag.
