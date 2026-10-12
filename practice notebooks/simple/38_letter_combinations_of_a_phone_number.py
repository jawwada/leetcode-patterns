"""
Letter Combinations of a Phone Number (LeetCode 17)
Return every string the digits 2-9 could spell on a phone keypad.
  digits = "23"  ->  ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]

Idea: one recursion level per digit. At level i, try each letter of digits[i],
      go one level deeper, then take the letter back off. A full-length path is one answer.

Pseudocode:
  if digits is empty: return []
  dfs(i):
      if i == len(digits): record "".join(path)
      for ch in KEYPAD[digits[i]]:
          path.append(ch); dfs(i + 1); path.pop()

Time O(n * 4^n), extra space O(n) for the path.
"""

KEYPAD = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
          "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def letter_combinations(digits):
    if not digits:
        return []
    result, path = [], []

    def dfs(i):
        if i == len(digits):                 # every digit has a letter
            result.append("".join(path))
            return
        for ch in KEYPAD[digits[i]]:
            path.append(ch)                  # choose
            dfs(i + 1)                       # next digit
            path.pop()                       # undo

    dfs(0)
    return result


if __name__ == "__main__":
    print(letter_combinations("23"))  # ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
    print(letter_combinations("7"))   # ['p', 'q', 'r', 's']
    print(letter_combinations(""))    # []
