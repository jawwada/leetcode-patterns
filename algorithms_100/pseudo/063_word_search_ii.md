---
rank: 63
slug: word_search_ii
---

Given a grid of letters and a list of words, return every word that can be spelled along a path of horizontally or vertically adjacent cells, each cell used at most once per word. On the grid with rows `oaan`, `etae`, `ihkr` and `iflv`, of the words `oath`, `pea`, `eat` and `rain`, the answer is `oath` and `eat`.

Running Word Search (#54) once per word repeats work: every search starts again at every cell, and words that share a prefix, like `oat` and `oath`, walk the same cells once each. Put all the words into a trie (#34) instead and search once. The DFS carries a trie node along with the cell, steps onto a neighbor only if the node has a child for that neighbor's letter, and dies the moment its letters stop being a prefix of any word. Each grid path is matched against every word at the same time, a path never grows longer than the longest word, and the number of words no longer multiplies the work.

The node at the end of a word stores the word itself, so a hit is recorded without rebuilding the string, and the word is then cleared, so a second path that spells it adds nothing. After a node's subtree has been searched, a node left with no children is deleted from its parent: every word below it has been found, and later starts skip that branch in one lookup. The trie shrinks as the answer grows. The `#` mark from #54 needs no test of its own here, because `#` is never a child in the trie.

```text
board       trie of the words (● keeps a word)
o a a n     root ─┬─ o ─ a ─ t ─ h ●    oath
e t a e           ├─ p ─ e ─ a ●        pea
i h k r           ├─ e ─ a ─ t ●        eat
i f l v           └─ r ─ a ─ i ─ n ●    rain

start (0,0) o: o → a(0,1) → t(1,1) → h(2,1) ●  record oath, prune o-a-t-h
start (1,0) e: no neighbor is an a, dead after one cell
start (1,3) e: e → a(1,2) → t(1,1) ●  record eat, prune e-a-t
start (2,3) r: no neighbor is an a, dead after one cell
every other start: its letter is not a child of the root (no p on the board)
```

```pseudo
FUNCTION BuildTrie(words)
    root ← new TrieNode()                    // no children yet, word null
    FOR EACH word IN words
        node ← root
        FOR EACH ch IN word
            IF ch NOT IN node.children
                node.children[ch] ← new TrieNode()
            node ← node.children[ch]
        node.word ← word                     // the last node keeps the word
    RETURN root

FUNCTION Dfs(board, row, col, parent, found)
    IF row < 0 OR row ≥ len(board) OR col < 0 OR col ≥ len(board[0])
        RETURN
    ch ← board[row][col]
    IF ch NOT IN parent.children
        RETURN                               // no word goes this way
    node ← parent.children[ch]
    IF node.word ≠ null
        found.append(node.word)
        node.word ← null                     // record each word only once
    board[row][col] ← '#'                    // mark: on the current path
    FOR EACH (d_row, d_col) IN [(1, 0), (-1, 0), (0, 1), (0, -1)]
        Dfs(board, row + d_row, col + d_col, node, found)
    board[row][col] ← ch                     // unmark on the way back
    IF len(node.children) = 0
        parent.children.remove(ch)           // prune: no word left below

FUNCTION FindWords(board, words)
    root ← BuildTrie(words)
    found ← empty list
    FOR row FROM 0 TO len(board) - 1
        FOR col FROM 0 TO len(board[0]) - 1
            Dfs(board, row, col, root, found)
    RETURN found
```

Building the trie costs `O(total letters)`. The search is `O(m · n · 3^L)` in the worst case, for L the longest word, because each start grows paths of at most L cells with at most three ways on after the first step, and that bound does not grow with the number of words; the extra space is the trie plus `O(L)` recursion. Reach for this whenever one grid, or one text, must be searched for many words: the trie merges k searches into one walk that shares every common prefix. The classic mistake, carried over from #54, is returning as soon as a word is found. Here the search must go on, because `oat` and `oath` lie on the same path, and stopping at `oat` loses `oath`.

*Practice:* LC 212 Word Search II · LC 79 Word Search · LC 208 Implement Trie (Prefix Tree)
