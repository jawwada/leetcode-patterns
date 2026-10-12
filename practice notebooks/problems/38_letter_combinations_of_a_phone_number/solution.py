"""
Letter Combinations of a Phone Number (LeetCode 17) - Medium
Area: backtracking
Key operations: one recursion level per digit, append a letter, recurse to the next digit, pop on return

Given a string of digits 2-9, return every string the digits could spell on a phone keypad
(2 = abc, 3 = def, 4 = ghi, 5 = jkl, 6 = mno, 7 = pqrs, 8 = tuv, 9 = wxyz), in keypad order.
The empty string gives [].
Example: "23" -> ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
"""
from itertools import product
from typing import List


# --- helpers ---
KEYPAD = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
          "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


# --- brute force ---
def brute_force(digits: str) -> List[str]:
    """Cartesian product of the letter groups, each tuple joined. O(n * 4^n) time, and every partial
    product lives as its own tuple: the optimal keeps ONE shared path and O(n) extra space."""
    if not digits:
        return []
    return ["".join(letters) for letters in product(*(KEYPAD[d] for d in digits))]


# --- optimal ---
def solve(digits: str) -> List[str]:
    """Depth-first over the digits: level i picks one letter of digits[i]; the shared path grows on
    the way down and shrinks on the way up. O(n * 4^n) for the output, O(n) extra space."""
    if not digits:
        return []
    result, path = [], []

    def dfs(i: int) -> None:
        if i == len(digits):
            result.append("".join(path))
            return
        for ch in KEYPAD[digits[i]]:
            path.append(ch)
            dfs(i + 1)
            path.pop()

    dfs(0)
    return result


# --- demo ---
def demo():
    return solve("23")


# --- bugs ---
BUGS = [
    {
        "replace": "        if i == len(digits):",
        "with":    "        if i == len(digits) - 1:",
        "fix": "a leaf is reached once every digit has a letter, at i == len(digits)",
        "why": "Stopping one level early records prefixes of length n - 1, so '23' returns ['a', 'b', 'c'] instead of nine two-letter strings.",
        "decoys": [
            {"line": "            path.append(ch)", "change": "should append digits[i], not the letter"},
            {"line": "    dfs(0)", "change": "should start at dfs(1)"},
            {"line": "    result, path = [], []", "change": "path should start with one placeholder letter"},
        ],
    },
    {
        "replace": "            path.pop()",
        "with":    "            path.pop(0)",
        "fix": "pop from the end: the letter chosen at this level is the last one in the path",
        "why": "Popping the front removes the first digit's letter and leaves this level's letter in place, so after 'ad' the next leaf reads 'de' instead of 'ae'.",
        "decoys": [
            {"line": "            dfs(i + 1)", "change": "should be dfs(i + 2) because this digit is done"},
            {"line": "            result.append(\"\".join(path))", "change": "should append path itself, no join needed"},
            {"line": "        for ch in KEYPAD[digits[i]]:", "change": "should iterate KEYPAD[digits[0]]"},
        ],
    },
    {
        "replace": "        return []",
        "with":    "        return [\"\"]",
        "fix": "the empty input has no combinations: return [], not a list holding the empty string",
        "why": "LeetCode expects [] for '', and [''] claims one combination of zero letters; the empty-input assert fails.",
        "decoys": [
            {"line": "    if not digits:", "change": "should be if len(digits) > 4"},
            {"line": "    return result", "change": "should return sorted(result)"},
            {"line": "        if i == len(digits):", "change": "should be i > len(digits)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
