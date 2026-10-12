---
rank: 43
slug: trie
---

Build a prefix tree with three operations: `insert(word)`; `search(word)`, which asks whether that exact word was inserted; and `starts_with(prefix)`, which asks whether any inserted word begins with the prefix. After inserting `apple`, `app`, `apt` and `bat`, `search("ap")` is false but `starts_with("ap")` is true.

A hash set of the words answers `search` in `O(L)` for a word of length L, but a prefix question would have to compare against all n words, `O(n · L)`. A trie stores the words letter by letter along paths from the root, so words that share a prefix share the path that spells it: `app`, `apple` and `apt` all hang below the single path `a → p`. Each node holds a map from letter to child and one flag, `is_end`, that marks where an inserted word stops. Inserting walks down the letters and creates any missing child on the way; both queries walk down the same way and give up the moment a letter has no child.

The path is the prefix, and the subtree below a node holds every word that starts with it. That makes `starts_with` a pure walk: if the letters can be followed, some inserted word starts with them, because every node lies on the path of a word that was inserted. `search` asks one thing more, that the walk ends on a flagged node, and that flag is the whole difference between a prefix and a word.

```text
root                      ● = is_end, a word stops here
├── a
│   └── p
│       ├── p ●           app
│       │   └── l
│       │       └── e ●   apple
│       └── t ●           apt
└── b
    └── a
        └── t ●           bat

search("app")        a → p → p, flagged        → true
search("ap")         a → p, not flagged        → false
starts_with("ap")    a → p, the path exists    → true
search("apl")        a → p, no child 'l'       → false
```

```pseudo
CLASS TrieNode
    FUNCTION Init()
        self.children ← empty map            // letter → TrieNode
        self.is_end ← false                  // true if a word ends here

CLASS Trie
    FUNCTION Init()
        self.root ← new TrieNode()

    FUNCTION Insert(word)
        node ← self.root
        FOR EACH ch IN word
            IF ch NOT IN node.children
                node.children[ch] ← new TrieNode()
            node ← node.children[ch]
        node.is_end ← true                   // the word stops here

    FUNCTION Walk(prefix)
        node ← self.root
        FOR EACH ch IN prefix
            IF ch NOT IN node.children
                RETURN null                  // the path breaks off
            node ← node.children[ch]
        RETURN node

    FUNCTION Search(word)
        node ← self.Walk(word)
        RETURN node ≠ null AND node.is_end

    FUNCTION StartsWith(prefix)
        RETURN self.Walk(prefix) ≠ null
```

Each operation touches one node per letter, so all three run in `O(L)` no matter how many words are stored, and the trie holds at most one node per inserted letter, `O(total letters)` space. Reach for a trie when a problem asks many questions about the prefixes of a fixed set of strings. Autocomplete (#97) walks to the prefix node, then runs a DFS below it in alphabetical order to collect suggestions (LC 1268); Replace Words swaps each word for the shortest root met on its walk down (LC 648); a grid search for many words at once follows the trie instead of each word in turn (#85). A wildcard `.` that matches any letter (LC 211) turns the walk into a DFS that tries every child at each dot. The classic mistake is a `search` that returns true as soon as the path exists, which finds `ap` in a trie holding only `apple`.

*Practice:* LC 208 Implement Trie (Prefix Tree) · LC 211 Design Add and Search Words Data Structure · LC 1268 Search Suggestions System · LC 648 Replace Words
