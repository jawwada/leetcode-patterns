"""
Letter Combinations of a Phone Number (LeetCode 17)  — Medium
Pattern: Backtracking over a fixed-depth choice tree (Cartesian product)

Problem
-------
Given a string of digits 2-9, return all letter strings the digits could represent on a phone
keypad (2=abc, 3=def, ..., 7=pqrs, 9=wxyz), in any order. Empty input gives [].
Example: "23" -> ["ad","ae","af","bd","be","bf","cd","ce","cf"].

Brute force
-----------
Build the answer level by level: start with [""], and for each digit replace the list with
every existing string extended by every letter of that digit.
O(n * 4^n) time and O(4^n) space for the live list. The waste: every intermediate level
materialises ALL partial strings as separate objects (3 strings, then 9, then 27, ...), and each
extension copies the whole prefix; the memory high-water mark is the entire last-but-one level
plus the output.

From brute force to optimal
---------------------------
The redundancy is storing every prefix of every answer separately. Observation: the choices form
a tree of depth n with 3 or 4 children per node; a depth-first walk only ever needs the ONE
prefix on the current root-to-node path. A shared path list with append / recurse / pop
produces every leaf with O(1) incremental work and O(n) auxiliary memory instead of O(4^n).
Output size is still 4^n strings, so time is unchanged; the win is the auxiliary space and the
template that extends naturally when some combinations must be skipped.

Intuition
---------
Think of n nested for-loops, one per digit, where n is not known at compile time: recursion is
how you write a variable-depth nested loop. Each recursion level owns one digit and tries each
of its letters.

Geometric view
--------------
A tree of depth n; level i fans out into the letters of digits[i]. Leaves are the answers.
The path list is the pencil line from the root to the current node; it is extended by one
letter on the way down and shortened by one on the way up. There is no pruning in this
problem: every branch is a valid answer, so the tree is walked in full.

Steps
-----
1. If digits is empty return []. Map each digit to its letters.
2. dfs(i): if i == len(digits) record "".join(path) and return.
3. For each letter of digits[i]: append, dfs(i + 1), pop.
4. Call dfs(0), return result.

Complexity: O(n * 4^n) time (4^n leaves, each joined in O(n)), O(n) recursion/path space beyond
the output.
Pitfalls: Returning [""] for empty input instead of []; forgetting that 7 and 9 have four
letters; building strings with + at every level (works, but allocates O(n) per node).
"""
from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        keypad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
                  "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        result: List[str] = []
        path: List[str] = []

        def dfs(i: int) -> None:
            if i == len(digits):                 # one letter chosen per digit: a leaf
                result.append("".join(path))
                return
            for ch in keypad[digits[i]]:
                path.append(ch)
                dfs(i + 1)
                path.pop()

        dfs(0)
        return result


def brute_force(digits: str) -> List[str]:
    if not digits:
        return []
    keypad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
              "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    level = [""]
    for d in digits:
        level = [prefix + ch for prefix in level for ch in keypad[d]]   # whole level materialised
    return level


if __name__ == "__main__":
    s = Solution()
    assert sorted(s.letterCombinations("23")) == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert s.letterCombinations("") == []                      # empty input
    assert s.letterCombinations("2") == ["a", "b", "c"]
    assert len(s.letterCombinations("79")) == 16              # two four-letter keys
    for d in ("23", "", "2", "79", "234"):
        assert sorted(s.letterCombinations(d)) == sorted(brute_force(d)), d
    print("ok")
