"""
Generate Parentheses (basics: backtracking)
Return every well-formed string of n pairs of parentheses.
  n = 3  ->  ['((()))', '(()())', '(())()', '()(())', '()()()']

Idea: add one bracket at a time; two counters replace the used[] flags of permutations.
      "(" is allowed while fewer than n are placed, ")" while some "(" is still unmatched,
      so every finished string is valid and nothing has to be filtered out.

Pseudocode:
  backtrack(opened, closed):
      if len(path) == 2n: record "".join(path); return
      if opened < n:      path.append("("); backtrack(opened + 1, closed); path.pop()
      if closed < opened: path.append(")"); backtrack(opened, closed + 1); path.pop()
  backtrack(0, 0)

Time O(n * number of results) (each leaf is valid, O(n) to join it), space O(n) recursion depth.
"""


def generate_parentheses(n):
    result, path = [], []

    def backtrack(opened, closed):
        if len(path) == 2 * n:           # all 2n brackets placed: record
            result.append("".join(path))
            return
        if opened < n:                   # room for another "("
            path.append("(")
            backtrack(opened + 1, closed)
            path.pop()
        if closed < opened:              # an unmatched "(" can be closed
            path.append(")")
            backtrack(opened, closed + 1)
            path.pop()

    backtrack(0, 0)
    return result


if __name__ == "__main__":
    print(generate_parentheses(3))  # ['((()))', '(()())', '(())()', '()(())', '()()()']
    print(generate_parentheses(2))  # ['(())', '()()']
    print(generate_parentheses(1))  # ['()']
