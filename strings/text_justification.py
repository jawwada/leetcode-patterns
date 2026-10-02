"""
Text Justification (LeetCode 68)  — Hard
Pattern: Greedy line packing

Problem
-------
Pack words greedily into lines of exactly maxWidth characters. Fully justify each line (extra
spaces distributed as evenly as possible, leftover spaces going to the leftmost gaps); the
last line, and any line with a single word, is left-justified and padded with spaces.
Example: words = ["This","is","an","example","of","text","justification."], maxWidth = 16 ->
["This    is    an", "example  of text", "justification.  "].

Brute force
-----------
Pack the same greedy lines, but distribute spaces by simulation: start every gap at one
space, then loop "add one space to the next gap, cycling from the left" until the line
measures maxWidth, re-joining and re-measuring the line after every single space. O(L *
maxWidth^2) time over L lines because each increment rebuilds and measures the line, O(maxWidth)
space. The wasted work: measuring the whole line to decide something that is pure arithmetic.

From brute force to optimal
---------------------------
The redundancy is simulating space distribution one character at a time. Observation: with
`gaps` gaps and `spaces` total spaces to place, every gap gets spaces // gaps and the leftmost
spaces % gaps gaps get one more -- a single divmod replaces the loop. The greedy packing is
itself already optimal for this problem (the statement mandates greedy), so the only
structure needed is a two-index scan: i marks the first word of the line, j is extended while
the next word still fits (current width + 1 + len(next) <= maxWidth). Each word is examined
once, and each output character is written once.

Intuition
---------
Two independent sub-problems: (1) which words go on this line -- greedy, take words while
they fit; (2) how to spread the spare spaces -- arithmetic, divmod with the remainder
favouring the left. Handle the two exceptional cases (single word, last line) with the same
left-justify code.

Geometric view
--------------
A ruler of length maxWidth. Lay words end to end with one space between them; the leftover
length is `spaces`. Cut that leftover into `gaps` equal pieces; the remainder is a handful of
single units dropped into the leftmost gaps one each. The last line is different: words sit
flush left and the ruler's remainder is one trailing block of spaces.

Steps
-----
1. i = 0. While i < len(words): j = i, width = len(words[i]).
2. While j+1 exists and width + 1 + len(words[j+1]) <= maxWidth: j += 1, width += 1 + len.
3. line = words[i..j]. If it is the last line or has one word: " ".join + right-pad.
4. Else spaces = maxWidth - total letters; q, r = divmod(spaces, gaps); gap k gets q + (k < r).
5. i = j + 1. Return the lines.

Complexity: O(total characters) time, O(maxWidth) extra space — each word visited once, each
output char written once.
Pitfalls: Off-by-one on whether the next word fits (count the separating space); a
single-word non-final line must be left-justified, not "fully" justified; the last line gets
exactly one space between words plus trailing padding.
"""
from typing import List


class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        lines, i = [], 0
        while i < len(words):
            j, width = i, len(words[i])                      # pack words[i..j] greedily
            while j + 1 < len(words) and width + 1 + len(words[j + 1]) <= maxWidth:
                j += 1
                width += 1 + len(words[j])
            line = words[i:j + 1]
            gaps = len(line) - 1
            if gaps == 0 or j == len(words) - 1:             # single word or last line
                text = " ".join(line)
                lines.append(text + " " * (maxWidth - len(text)))
            else:
                spaces = maxWidth - sum(map(len, line))
                q, r = divmod(spaces, gaps)                  # leftmost r gaps get one extra
                text = ""
                for k, w in enumerate(line[:-1]):
                    text += w + " " * (q + (k < r))
                lines.append(text + line[-1])
            i = j + 1
        return lines


def brute_force(words: List[str], maxWidth: int) -> List[str]:
    lines, line = [], []
    for w in words + [None]:                                 # None flushes the final line
        if w is None or (line and len(" ".join(line + [w])) > maxWidth):
            if w is None or len(line) == 1:
                text = " ".join(line)
                lines.append(text + " " * (maxWidth - len(text)))
            else:
                gaps, k = [" "] * (len(line) - 1), 0
                while len("".join(line) + "".join(gaps)) < maxWidth:   # one space at a time
                    gaps[k % len(gaps)] += " "
                    k += 1
                lines.append("".join(a + b for a, b in zip(line, gaps)) + line[-1])
            line = []
        if w is not None:
            line.append(w)
    return lines


if __name__ == "__main__":
    s = Solution()
    cases = [
        (["This", "is", "an", "example", "of", "text", "justification."], 16),
        (["What", "must", "be", "acknowledgment", "shall", "be"], 16),
        (["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain", "to", "a",
          "computer.", "Art", "is", "everything", "else", "we", "do"], 20),
        (["a"], 1),
        (["ab", "cd", "ef"], 2),
    ]
    assert s.fullJustify(*cases[0]) == ["This    is    an", "example  of text", "justification.  "]
    assert s.fullJustify(*cases[1]) == ["What   must   be", "acknowledgment  ", "shall be        "]
    assert s.fullJustify(*cases[2]) == [
        "Science  is  what we", "understand      well", "enough to explain to",
        "a  computer.  Art is", "everything  else  we", "do                  ",
    ]
    assert s.fullJustify(["a"], 1) == ["a"]
    for c in cases:
        out = s.fullJustify(*c)
        assert all(len(row) == c[1] for row in out)
        assert out == brute_force(*c)
    print("ok")
