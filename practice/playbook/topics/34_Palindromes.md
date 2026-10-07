## Palindrome Techniques

A palindrome reads the same in both directions. Expand around a center to find palindromic substrings, or move inward from both ends to check a candidate. The KMP notebook covers the separate prefix-table technique for Shortest Palindrome.

<!-- cell -->

**Palindromes: from the middle, and from the ends.** Longest Palindromic Substring asks for the longest block that reads the same both ways: `"babad"` gives `"bab"`, and `"cbbd"` gives `"bb"`. A palindrome is decided by its center, and growing it one step on each side costs one comparison. So try all 2n − 1 centers, each letter for odd lengths and each gap for even lengths, and stop at the first mismatch, since no wider palindrome can share that center.

Valid Palindrome II asks whether deleting at most one letter makes the string a palindrome: `"abca"` becomes one without its `b` or its `c`, and `"abc"` never does. It walks two pointers inward instead. At the first mismatch one of the two letters must go, so check both leftovers; with punctuation to skip, the walk is in [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers).

<!-- cell -->

```python
def longest_palindrome(s):                   # O(n²) time, O(1) extra space
    best_lo, best_len = 0, 0
    for center in range(len(s)):
        for lo, hi in ((center, center), (center, center + 1)):   # odd and even centers
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1                      # grow while both ends match
                hi += 1
            if hi - lo - 1 > best_len:       # the loop overshot by one on each side
                best_lo, best_len = lo + 1, hi - lo - 1
    return s[best_lo:best_lo + best_len]


def valid_palindrome_ii(s):                  # a palindrome after deleting at most one letter? O(n)
    def is_pal(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo, hi = lo + 1, hi - 1
        return True
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:                   # the first mismatch: one of these two must go
            return is_pal(lo + 1, hi) or is_pal(lo, hi - 1)
        lo, hi = lo + 1, hi - 1
    return True


print(longest_palindrome("babad"), longest_palindrome("cbbd"))   # bab bb
print(valid_palindrome_ii("abca"), valid_palindrome_ii("abc"))   # True False
```

<!-- cell -->

**Try it**
- Keep only the odd center, `for lo, hi in ((center, center),):`, and run `longest_palindrome("cbbd")`: `'c'`. The palindrome `"bb"` has no middle letter, so only a gap can be its center.
- Add `print(center, lo, hi)` after the `while` loop and run `longest_palindrome("aba")`: the line `1 -1 3` shows the loop stopping one step outside `s[0:3]` on both sides.
- Keep only the left skip (`return is_pal(lo + 1, hi)`) and run `valid_palindrome_ii("cbbcc")`: False instead of True. Deleting the `c` at index 3 works; deleting the `b` at index 1 does not.

<!-- cell -->

Palindrome Pairs asks for every pair of different words whose concatenation is a palindrome: in `["abcd", "dcba", "lls", "s", "sssll"]`, `"s" + "lls"` and `"lls" + "sssll"` are two of the four. Cut each word in two. If one half is a palindrome, the other half's reverse must be a whole word, and a dict of reversed words finds it with one lookup: O(n·L²) for n words of length L.

<details><summary>Palindrome Pairs in code</summary>

```py
def palindrome_pairs(words):                 # O(n·L²): n words, L + 1 cuts, O(L) per test
    index = {w[::-1]: i for i, w in enumerate(words)}   # reversed word -> its index
    pairs = []
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):        # w = pre + suf
            pre, suf = w[:cut], w[cut:]
            if pre == pre[::-1] and suf in index and index[suf] != i:
                pairs.append([index[suf], i])    # reverse(suf) + pre + suf
            if cut < len(w) and suf == suf[::-1] and pre in index and index[pre] != i:
                pairs.append([i, index[pre]])    # pre + suf + reverse(pre); cut < len(w) avoids doubles
    return pairs

# palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"])  -> [[1, 0], [0, 1], [3, 2], [2, 4]]
# without "cut < len(w) and", ["abcd", "dcba"] gives every pair twice
```

</details>
