---
rank: 121
slug: longest_common_prefix
---

Given a list of strings, return the longest string that is a prefix of every one of them, or the empty string if they share none. For `["flower", "flow", "flight"]` the answer is `"fl"`, and for `["dog", "racecar", "car"]` it is `""`.

Stack the strings on top of each other, left-aligned, and read them as columns. The common prefix is the run of columns, from the left, in which every row shows the same character. The vertical scan walks those columns one at a time, takes the character of the first string in the current column and checks every string against it. It stops at the first column where some string holds a different character or has already ended, and returns the first string cut just before that column; if nothing stops it, the first string is a prefix of all the others and is the answer. Because it stops at the first bad column, the scan never reads past the prefix plus one column. Folding the list pairwise instead (the prefix of the first two, then of that and the third) is linear too, but it can spend its time matching long early strings that a short later one cuts down at once.

Two other views are worth knowing. Sorting puts the lexicographically smallest and largest strings at the two ends, and the common prefix of the whole list equals the common prefix of just those two, because any string that sits between them in sorted order must agree with both on that prefix; `min` and `max` find the two ends in linear time, so the sort itself is unnecessary. A trie (#43) built from all the strings turns the answer into the path from the root that never branches and never passes the end of a word, which pays off when many queries ask about one fixed set of strings.

```text
column →      0   1   2   3   4   5
"flower"      f   l   o   w   e   r
"flow"        f   l   o   w
"flight"      f   l   i   g   h   t
              ✓   ✓   ✗
                      ↑ col 2: ch = 'o' from "flower", but "flight" has 'i'
answer: first[0..1] = "fl"     9 comparisons, columns 3 to 5 never touched
```

```pseudo
FUNCTION LongestCommonPrefix(strs)
    IF len(strs) = 0
        RETURN ""
    first ← strs[0]
    FOR col FROM 0 TO len(first) - 1
        ch ← first[col]
        FOR EACH word IN strs
            IF col = len(word) OR word[col] ≠ ch    // word ended, or mismatch
                RETURN first[0..col - 1]
    RETURN first                              // first is a prefix of all
```

The scan reads at most `n` characters in each of `L + 1` columns, where `L` is the length of the answer, so it costs `O(n × (L + 1))`, at most linear in the size of the input, with `O(1)` extra space besides the answer. The signals are a prefix shared by every string, autocomplete (#97), and grouping strings by how they start; when one fixed set is queried many times, build the trie instead. The classic mistake is reading `word[col]` before checking that `word` is long enough: the end of the shortest string is a stopping condition just like a mismatch, which is why the test `col = len(word)` comes first, and it is also what makes a list containing `""` return `""`.

*Practice:* LC 14 Longest Common Prefix · LC 3043 Find the Length of the Longest Common Prefix · LC 2416 Sum of Prefix Scores of Strings
