"""
Decode String (LeetCode 394)  — Medium
Pattern: Stack of nested contexts

Problem
-------
Decode a string where k[encoded] means encoded repeated k times; brackets may nest and digits
only appear as repeat counts.
Example: "3[a]2[bc]" -> "aaabcbc"; "3[a2[c]]" -> "accaccacc"; "2[abc]3[cd]ef" -> "abcabccdcdcdef".

Brute force
-----------
Repeatedly locate the first ']' -- the pattern before it (back to the matching '[' and its
count) is an innermost, bracket-free k[...]; expand it into a plain string and splice it back,
then rescan from the start. O(n * output) time because each expansion rebuilds the whole
string and nested groups are re-copied once per nesting level, O(output) space. The wasted
work: text outside the innermost group is copied over and over.

From brute force to optimal
---------------------------
The redundancy is copying unaffected text on every expansion. Observation: an innermost group
can be built on the fly if, upon reaching '[', we park the text built so far together with
the pending count and start a fresh buffer; on ']' we pop that frame, repeat the buffer k
times and append to the parked text. "Park and resume" is a stack of (prefix, count) frames
-- the same thing a recursive-descent parser's call stack would hold. One pass, each output
character written once per nesting level it belongs to.

Intuition
---------
Treat '[' as "call" and ']' as "return". The stack frame saves what you had built and how
many times to repeat what you are about to build. Nesting falls out naturally.

Geometric view
--------------
Columns of frames: each frame is a (prefix, k) pair. Reading "3[a2[c]]": at the first '[' push
("", 3), at the second push ("a", 2). The ']' pops ("a", 2) producing "a" + "c"*2 = "acc";
the next ']' pops ("", 3) producing "acc"*3.

Steps
-----
1. stack = [], cur = "", num = 0.
2. Digit: num = num*10 + digit (counts can be multi-digit).
3. '[': push (cur, num); reset cur = "", num = 0.
4. ']': prev, k = pop; cur = prev + cur*k.
5. Letter: cur += letter. Return cur at the end.

Complexity: O(n + output) time, O(nesting depth + output) space — each char processed once.
Pitfalls: Multi-digit counts like "10[a]"; forgetting to reset num after '['; building
strings via repeated += on long outputs (fine here; use a list for very large outputs).
"""


class Solution:
    def decodeString(self, s: str) -> str:
        stack = []                              # frames: (text before '[', repeat count)
        cur, num = "", 0
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)        # counts may have several digits
            elif ch == "[":
                stack.append((cur, num))        # park the outer context
                cur, num = "", 0
            elif ch == "]":
                prev, k = stack.pop()
                cur = prev + cur * k            # resume the outer context
            else:
                cur += ch
        return cur


def brute_force(s: str) -> str:
    while "[" in s:                                             # one innermost group per pass
        close = s.index("]")                                    # first ']' closes an innermost pair
        open_ = s.rindex("[", 0, close)
        j = open_
        while j > 0 and s[j - 1].isdigit():
            j -= 1
        k = int(s[j:open_])
        s = s[:j] + s[open_ + 1:close] * k + s[close + 1:]      # rebuilds the whole string
    return s


if __name__ == "__main__":
    s = Solution()
    cases = ["3[a]2[bc]", "3[a2[c]]", "2[abc]3[cd]ef", "abc", "10[x]", "2[3[a]b]"]
    assert s.decodeString("3[a]2[bc]") == "aaabcbc"
    assert s.decodeString("3[a2[c]]") == "accaccacc"
    assert s.decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert s.decodeString("10[x]") == "x" * 10
    assert s.decodeString("abc") == "abc"
    for c in cases:
        assert s.decodeString(c) == brute_force(c)
    print("ok")
