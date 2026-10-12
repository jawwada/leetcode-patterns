"""
Decode String (basics: stacks)
Expand every k[text] into text repeated k times; brackets can nest and k can have several digits.
  "3[a2[c]]"  ->  "accaccacc"

Idea: on '[' park the text built so far and the repeat count on a stack, then start fresh.
      On ']' the inner text is finished: pop the parked pair and glue prefix + inner * count.

Pseudocode:
  stack = [], cur = "", k = 0
  for ch in s:
      digit:  k = k * 10 + digit                    # counts can have several digits
      '[':    push (cur, k); cur = ""; k = 0        # park, then start fresh
      ']':    prev, count = pop; cur = prev + cur * count
      letter: cur += ch
  return cur

Time O(output length), space O(output length).
"""


def decode_string(s):
    stack = []                           # (text before '[', its repeat count)
    cur, k = "", 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)         # one more digit of the count
        elif ch == "[":
            stack.append((cur, k))       # park prefix and count
            cur, k = "", 0               # the inner text starts fresh
        elif ch == "]":
            prev, count = stack.pop()
            cur = prev + cur * count     # prefix first, then the repeats
        else:
            cur += ch                    # a plain letter
    return cur


if __name__ == "__main__":
    print(decode_string("3[a2[c]]"))       # accaccacc
    print(decode_string("2[abc]3[cd]ef"))  # abcabccdcdcdef
    print(decode_string("10[a]"))          # aaaaaaaaaa
