"""
Rabin-Karp Rolling Hash (basics: strings)
Return every index where pattern starts in text, comparing window hashes instead of strings.
  text "abracadabra", pattern "abra"  ->  [0, 7]

Idea: read a window as a base-256 number mod MOD. Sliding it one step is O(1): drop the left
      char (weight BASE^(m-1)), shift by BASE, add the new right char. Different strings can
      share a hash (a collision), so every hash hit is confirmed by comparing the strings.

Pseudocode:
  target = hash(pattern), window = hash(text[:m]), high = BASE^(m-1) % MOD
  for i in 0 .. n-m:
      if window == target and text[i:i+m] == pattern: record i      # verify the hit
      if i + m < n: window = ((window - text[i] * high) * BASE + text[i+m]) % MOD

Time O(n + m) expected, O(n * m) if hashes keep colliding; space O(m).
"""

BASE, MOD = 256, 101                     # tiny MOD on purpose; real code uses a big prime


def poly_hash(s):
    h = 0
    for ch in s:
        h = (h * BASE + ord(ch)) % MOD   # shift one digit left, add the new char
    return h


def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    high = pow(BASE, m - 1, MOD)         # weight of the window's leftmost char
    target, window = poly_hash(pattern), poly_hash(text[:m])
    hits = []
    for i in range(n - m + 1):
        if window == target and text[i:i + m] == pattern:  # hash hit, then verify
            hits.append(i)
        if i + m < n:                    # roll: drop text[i], add text[i + m]
            window = ((window - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
    return hits


if __name__ == "__main__":
    print(rabin_karp("abracadabra", "abra"))       # [0, 7]
    # "abcc" hashes like "abra": at index 0 below the hashes match but the strings don't
    print(poly_hash("abcc") == poly_hash("abra"))  # True
    print(rabin_karp("abccabra", "abra"))          # [4]
