"""
Reverse Words in a String (LeetCode 151)  — Medium
Pattern: In-place reverse, then reverse each word

Problem
-------
Given a string with words separated by one or more spaces (possibly leading/trailing), return
the words in reverse order joined by single spaces.
Example: "the sky is blue" -> "blue is sky the"; "  hello world  " -> "world hello";
"a good   example" -> "example good a".

Brute force
-----------
Split on whitespace into a list of words, drop empty tokens, reverse the list, join with single
spaces: " ".join(reversed(s.split())). O(n) time and O(n) space. In Python this is already
optimal and is the answer you state first; the "waste" the interviewer wants you to discuss is
the allocation of a separate word list plus intermediate strings, which matters in a language
with mutable strings where the follow-up is "do it in place with O(1) extra memory".

From brute force to optimal
---------------------------
Reversing the order of words while keeping each word intact can be done with two reversals on
the character array: reverse the entire array (words are now in the right order but each word
is spelled backwards), then reverse each word individually to repair the spelling. Both passes
are in-place two-pointer swaps. Spaces are handled first by a compaction pass: a write pointer
copies characters forward, emitting a space only when the previous written char is not a space,
then trims one trailing space. Three linear passes, O(1) extra memory beyond the array.

Intuition
---------
Reversal composes: reversing the whole and then reversing each part undoes the inner reversal
but keeps the outer one. The character array is treated like a tape that you flip end over end,
then flip each word back so the letters read correctly.

Geometric view
--------------
"  hello world  "  --compact-->  "hello world"
                   --reverse all-->  "dlrow olleh"
                   --reverse words-->  "world hello"
Two pointers L and R meet in the middle for each reversal; the word pass walks start/end
boundaries from left to right.

Steps
-----
1. chars = list(s); compact spaces with read pointer r and write pointer w; trim trailing space.
2. reverse(0, len-1) over the whole array.
3. Walk i from 0; at each space or the end, reverse(start, i-1) and set start = i+1.
4. Join and return.

Complexity: O(n) time, O(n) space in Python for the char list (O(1) extra in a mutable-string
            language) — three linear passes, each character swapped at most twice.
Pitfalls: leaving a trailing space after compaction; forgetting to reverse the last word (loop
          must run to len inclusive); multiple interior spaces collapsing to zero instead of one.
"""


class Solution:
    def reverseWords(self, s: str) -> str:
        chars = list(s)

        def reverse(lo: int, hi: int) -> None:
            while lo < hi:
                chars[lo], chars[hi] = chars[hi], chars[lo]
                lo, hi = lo + 1, hi - 1

        w = 0                                             # 1. compact spaces in place
        for r in range(len(chars)):
            if chars[r] != " " or (w > 0 and chars[w - 1] != " "):
                chars[w] = chars[r]
                w += 1
        if w and chars[w - 1] == " ":
            w -= 1
        del chars[w:]

        reverse(0, len(chars) - 1)                        # 2. reverse the whole tape
        start = 0
        for i in range(len(chars) + 1):                   # 3. reverse each word back
            if i == len(chars) or chars[i] == " ":
                reverse(start, i - 1)
                start = i + 1
        return "".join(chars)


def brute_force(s: str) -> str:
    """Split into words, reverse the list, join; allocates a word list and new strings."""
    return " ".join(reversed(s.split()))


if __name__ == "__main__":
    sol = Solution()
    assert sol.reverseWords("the sky is blue") == "blue is sky the"
    assert sol.reverseWords("  hello world  ") == "world hello"
    assert sol.reverseWords("a good   example") == "example good a"
    assert sol.reverseWords("   ") == ""                   # edge: only spaces
    assert sol.reverseWords("single") == "single"           # edge: one word
    for s in ["the sky is blue", "  hello world  ", "a good   example", "   ", "single", " x "]:
        assert sol.reverseWords(s) == brute_force(s), s
    print("ok")
