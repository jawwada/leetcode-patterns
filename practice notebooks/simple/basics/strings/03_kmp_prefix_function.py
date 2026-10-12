"""
KMP Prefix Function (basics: strings)
Return every index where pattern starts in text, using the KMP failure table.
  text "aabaaabaab", pattern "aab"  ->  [0, 4, 7]     (failure table of "aab": [0, 1, 0])

Idea: fail[i] = length of the longest proper prefix of pattern[:i + 1] that is also its suffix.
      On a mismatch the matched part is not thrown away: the pattern slides to that border
      (j = fail[j - 1]) while the text index i never moves back.

Pseudocode:
  build_failure(p):
      fail = [0] * m, k = 0
      for i in 1 .. m-1:
          while k > 0 and p[i] != p[k]: k = fail[k - 1]   # fall back to a shorter border
          if p[i] == p[k]: k += 1                         # extend the border
          fail[i] = k

  kmp_search(text, p):
      j = 0                                               # chars of p matched so far
      for i, ch in text:
          while j > 0 and ch != p[j]: j = fail[j - 1]     # slide p, i stays put
          if ch == p[j]: j += 1
          if j == m: record i - m + 1; j = fail[m - 1]    # keep the border: overlaps count

Time O(n + m), space O(m).
"""


def build_failure(pattern):
    fail = [0] * len(pattern)            # fail[0] = 0: a border must be proper
    k = 0                                # length of the border being extended
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = fail[k - 1]              # fall back to a shorter border
        if pattern[i] == pattern[k]:
            k += 1                       # the border grows by one
        fail[i] = k
    return fail


def kmp_search(text, pattern):
    fail = build_failure(pattern)
    hits, j = [], 0                      # j = pattern chars matched right now
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = fail[j - 1]              # slide the pattern, i stays put
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):            # a full match ends at i
            hits.append(i - j + 1)
            j = fail[-1]                 # keep the border so overlaps are found
    return hits


if __name__ == "__main__":
    print(build_failure("aab"))             # [0, 1, 0]
    print(kmp_search("aabaaabaab", "aab"))  # [0, 4, 7]
    print(kmp_search("aaaa", "aa"))         # [0, 1, 2]
