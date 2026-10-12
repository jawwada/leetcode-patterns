## KMP and the LPS Array

LPS means longest proper prefix that is also a suffix. The same array is often called the prefix function or failure table. KMP uses it to reuse an already matched prefix after a mismatch, instead of comparing those characters again.

<!-- cell -->

The **KMP prefix function** asks, at every position, how much of the start of the string reappears just before it. Longest Happy Prefix asks it once, for the whole string: `"level"` gives `"l"`. `fail[i]` is the length of the longest *border* of `s[:i + 1]`, a prefix that is also a suffix and is *proper*, shorter than the whole string. When the next letter does not extend the current border, fall back to the border of the border, `fail[k - 1]`, instead of starting over:

```text
s = a a b a a a b        fail so far = [0, 1, 0, 1, 2]
i=5 ('a'): extend the border "aa"? its next letter s[2] = 'b' != 'a'
           fall back to the border of "aa", which is "a": s[1] = 'a' == 'a'  ->  "aa", fail[5] = 2
i=6 ('b'): extend "aa": s[2] = 'b' == 'b'  ->  "aab", fail[6] = 3
```

Each fall-back pays for an earlier step forward, so the table costs O(n) and a search O(n + m). Longest Happy Prefix is `fail[-1]`. Shortest Palindrome adds the fewest letters in front of `s`, `"aacecaaa"` → `"aaacecaaa"`, so it needs the longest palindromic *prefix*: the border of `s + "#" + reverse(s)`. `kmp_find` returns every start of a pattern in a text; it glues the two with `"\0"`, a character in neither string, so no border can cross it.

<!-- cell -->

```python
def prefix_function(s):
    fail = [0] * len(s)                      # fail[i] = longest proper border of s[:i + 1]
    for i in range(1, len(s)):
        k = fail[i - 1]                      # the border we hope to extend by s[i]
        while k and s[i] != s[k]:
            k = fail[k - 1]                  # fall back to the next shorter border
        if s[i] == s[k]:
            k += 1
        fail[i] = k
    return fail


def longest_happy_prefix(s):                 # the longest proper prefix that is also a suffix
    return s[:prefix_function(s)[-1]] if s else ""


def shortest_palindrome(s):                  # letters may only be added in front
    keep = prefix_function(s + "#" + s[::-1])[-1]   # the longest palindromic prefix of s
    return s[keep:][::-1] + s


def kmp_find(text, pattern):                 # every start of pattern in text, overlaps too
    m, fail = len(pattern), prefix_function(pattern + "\0" + text)
    return [i - 2 * m for i, k in enumerate(fail) if k == m]


print(prefix_function("aabaaab"))                                      # [0, 1, 0, 1, 2, 2, 3]
print(longest_happy_prefix("ababab"), longest_happy_prefix("level"))   # abab l
print(shortest_palindrome("aacecaaa"), shortest_palindrome("abcd"))    # aaacecaaa dcbabcd
print(kmp_find("aabaaabaab", "aab"))                                   # [0, 4, 7]
```

<!-- cell -->

**Try it**
- Replace `k = fail[k - 1]` with `k = 0` (start over on a mismatch) and rerun: `prefix_function("aabaaab")` is `[0, 1, 0, 1, 2, 1, 0]`. The borders `"aa"` and `"aab"` at the end are missed.
- Remove the `"#"` in `shortest_palindrome` and run it on `"aaba"`: `'aaba'`, which is not a palindrome. The border of `"aabaabaa"` is 5, longer than `s`; the separator caps it at `len(s)`. The right answer is `'abaaba'`.
- Run `kmp_find("aaaa", "aa")`: `[0, 1, 2]`. Overlapping matches are found because a full match keeps its border.
