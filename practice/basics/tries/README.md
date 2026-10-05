# Tries

A trie (prefix tree) stores a set of strings as a tree of characters. The root is the empty string; every edge adds one character; a node is the prefix spelled by the path to it. Words that share a prefix share the path, so "apple" and "app" share four nodes. Each node carries two things: a dict `children` from character to child node, and a flag `end` saying that a stored word ends exactly here. The flag is what distinguishes "app is a word" from "app is only a prefix of apple".

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.end = False    # a word ends here
```

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| insert(word) | O(len) | create the missing child at each step, set `end` on the last node |
| search(word) | O(len) | walk the path; True only if the path exists AND the last node has `end` |
| startsWith(prefix) | O(len) | walk the path; True if it exists, the flag does not matter |
| delete(word) | O(len) | clear the flag, then prune upward while the node is empty and ends no word |
| collect words under a prefix | O(len + output) | walk to the prefix node, DFS its subtree, emit at every `end` |
| wildcard search with '.' | O(26^dots * len) worst case | DFS; '.' branches into every child |

All costs depend on the length of the query, never on how many words are stored. That is the whole point.

## Drawn example: insert apple, app, ape ("$" marks a word end)

```
insert "apple"   root -> a -> p -> p -> l -> e$
insert "app"     root -> a -> p -> p$ -> l -> e$        (same path, just a flag on the second p)
insert "ape"     root -> a -> p -> p$ -> l -> e$
                             \-> e$

as a nested dict: {'a': {'p': {'p': {'$': True, 'l': {'e': {'$': True}}}, 'e': {'$': True}}}}

search "app"       walk a, p, p  -> node exists, end flag True   -> True
search "ap"        walk a, p     -> node exists, end flag False  -> False
startsWith "ap"    walk a, p     -> node exists                  -> True
search "apply"     walk a, p, p, l, then no child 'y'            -> False

delete "apple"     clear the flag on e; e is empty and ends no word -> prune
                   l is now empty and ends no word               -> prune
                   second p has no children but ends "app"       -> STOP
                   result: {'a': {'p': {'p': {'$': True}, 'e': {'$': True}}}}
```

## The invariant to say out loud

"Search needs the end flag, startsWith only needs the path." Walking to a node proves the prefix exists; only `node.end` proves a word ends there. When deleting, the mirror rule: "prune a node only if it has no children AND ends no word", and stop climbing the moment one of those holds.

## Exercises

| File | Drills |
|---|---|
| `01_trie_insert_search_prefix.py` | insert creates children and sets the flag; search checks the flag; startsWith does not |
| `02_trie_delete.py` | record the path down, clear the flag, prune upward until a shared or word-ending node |
| `03_autocomplete_collect_words_with_prefix.py` | walk to the prefix node, DFS in sorted child order, output comes out sorted |
| `04_add_and_search_word_with_wildcard.py` (LC 211) | DFS search where '.' tries every child; end flag at the last character |
