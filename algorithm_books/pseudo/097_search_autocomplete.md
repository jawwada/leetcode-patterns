---
rank: 97
slug: search_autocomplete
---

Design the suggestion box of a search engine. It starts from a history of past sentences and the number of times each was typed. `input(c)` receives one character and returns the three hottest past sentences that start with everything typed so far, most typed first and ties in ASCII order; `#` ends the sentence, records it as typed once more, and returns an empty list. With the history `i love you` 5, `island` 3, `iroman` 2 and `i love leetcode` 2, typing `i` returns `["i love you", "island", "i love leetcode"]`, and a space next narrows it to `["i love you", "i love leetcode"]`.

The brute force tests every sentence against the typed prefix on every keystroke and sorts the matches, `O(n · L)` per keystroke for the tests alone, with n sentences of length L. A trie (#43) indexes the sentences by prefix instead: each sentence is spelled along a path from the root, the node where it ends remembers the whole sentence, and a separate map holds the counts. The sentences that start with a prefix are exactly those that end in the subtree of that prefix's node. The design keeps a cursor on the node of the text typed so far, from one call to the next, so a keystroke is one step down to a child, never a fresh walk from the root. A DFS below the cursor collects the sentences, and sorting the pairs `(-count, sentence)` ranks by count and breaks ties in the same comparison. That is why `i love leetcode` beats `iroman` at count 2: a space sorts before every letter.

A missing child is a dead end. No past sentence starts with the typed text, and none can start with any longer text, so the cursor becomes null and stays null until `#`. The typed text is still kept, because `#` records it: a fresh path grows into the trie, its count rises by one, and the cursor returns to the root.

```text
trie after the demo; _ is a space and a chain of one-child nodes is one label
root ── i ─┬─ _ ─┬─ love_ ─┬─ you ●        i love you         5
           │     │         └─ leetcode ●   i love leetcode    2
           │     └─ a ●                    i a                2 (typed twice)
           ├─ sland ●                      island             3
           └─ roman ●                      iroman             2

key  cursor     sentences below, by (-count, sentence); | marks the cut at 3
i    i          i love you 5, island 3, i love leetcode 2 | iroman 2
_    i_         i love you 5, i love leetcode 2
a    null       no child a under i_: dead end, [] until the #
#    root       record "i a" with count 1, clear the typed text
i    i          i love you 5, island 3, i love leetcode 2 | iroman 2, i a 1
_    i_         i love you 5, i love leetcode 2, i a 1
a    i_a        i a 1
#    root       record "i a" again: count 2
```

```pseudo
CLASS TrieNode
    FUNCTION Init()
        self.children ← empty map              // character → TrieNode
        self.sentence ← null                   // the sentence that ends here

CLASS AutocompleteSystem
    FUNCTION Init(sentences, times)
        self.root ← new TrieNode()
        self.counts ← empty map                // sentence → times typed
        FOR i FROM 0 TO len(sentences) - 1
            self.Record(sentences[i], times[i])
        self.typed ← ""                        // the sentence typed so far
        self.node ← self.root                  // node of typed; null: dead end

    FUNCTION Record(sentence, times)
        node ← self.root
        FOR EACH ch IN sentence
            IF ch NOT IN node.children
                node.children[ch] ← new TrieNode()
            node ← node.children[ch]
        node.sentence ← sentence               // mark where the sentence ends
        self.counts[sentence] ← self.counts.get(sentence, 0) + times

    FUNCTION Input(c)
        IF c = "#"
            self.Record(self.typed, 1)         // it was typed once more
            self.typed ← ""
            self.node ← self.root
            RETURN empty list
        self.typed ← self.typed + c
        IF self.node = null OR c NOT IN self.node.children
            self.node ← null                   // dead end: stays dead until #
            RETURN empty list
        self.node ← self.node.children[c]      // one step down, no rescan
        RETURN self.TopThree(self.node)

    FUNCTION Collect(node, found)
        IF node.sentence ≠ null
            found.append(node.sentence)
        FOR EACH ch IN node.children
            self.Collect(node.children[ch], found)

    FUNCTION TopThree(node)
        found ← empty list
        self.Collect(node, found)
        ranked ← empty list
        FOR EACH sentence IN found
            ranked.append((-self.counts[sentence], sentence))
        ranked.sort()                          // top count first, then ASCII
        best ← empty list
        FOR i FROM 0 TO min(3, len(ranked)) - 1
            best.append(ranked[i][1])          // keep the sentence
        RETURN best
```

A keystroke costs `O(1)` for the step plus `O(k + m log m)` to collect and rank, for k nodes and m sentences under the cursor (a size-3 heap from #19 trims the ranking to `O(m)`); `#` costs `O(L)`, and the trie holds one node per distinct prefix. The collect is the expensive part, and the trade-off interviewers want to hear is caching the top three at every node. A keystroke then reads three references in `O(1)`, while `#` must update every node on the sentence's path and every node stores three more references. Because counts only grow, each update is an exact merge into a list of three: the recorded sentence is the only one whose rank changes, and it can only climb. Search engines take that side of the trade, computing the suggestions for each prefix offline from query logs and refreshing them in batches. The signals are suggestions as you type and ranked prefix queries. The classic mistake is treating a dead end as a restart: if the cursor falls back to the root, typing `x` and then `i` suggests `i love you` for the text `xi`.

*Practice:* LC 642 Design Search Autocomplete System · LC 1268 Search Suggestions System · LC 208 Implement Trie (Prefix Tree)
