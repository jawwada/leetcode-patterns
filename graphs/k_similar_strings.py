"""
K-Similar Strings (LeetCode 854)  — Hard
Pattern: BFS over states with pruned branching (fix the first mismatch)

Problem
-------
s1 and s2 are anagrams of each other (letters a-f, length <= 20). One move swaps two letters of
s1. Return the smallest number of swaps that turns s1 into s2.
Example: s1="abac", s2="baca" -> 2  (abac -> baac -> baca).

Brute force
-----------
BFS over strings: from each string generate every one of the n(n-1)/2 swaps, enqueue unseen
results, stop when s2 is reached. Correct, but the state space is every permutation reachable,
up to n! / (duplicate letters) strings, each with O(n^2) neighbours: exponential time and space.
The wasted work is exploring swaps that touch already-correct positions or fix nothing, and
exploring the same multiset of mismatches in many different orders.

From brute force to optimal
---------------------------
The redundancy is branching on irrelevant swaps. Observation 1: a position that already matches
never needs to move again, so swaps involving it are pure waste. Observation 2: the first
mismatched index i must be fixed by SOME swap eventually, and swapping is commutative enough
that we can always do that swap first; so from every state branch only on swaps that put the
right letter s2[i] into position i. Observation 3: pick j only where cur[j] == s2[i] and
cur[j] != s2[j], so the swap fixes i and does not break j. The branching factor drops from
O(n^2) to at most the count of one letter (<= n), and the depth is at most n-1. The structure is
still plain BFS with a visited set, but the state tree is now exponentially smaller; a further
prune (prefer j where cur[i] == s2[j], fixing two slots at once) makes it fast on all inputs.

Intuition
---------
Each state is a string; a swap is an edge; BFS layers are swap counts, so the first time s2 is
dequeued we have the minimum. Always repairing the leftmost broken slot never loses optimality:
in any optimal sequence the swap that finally fills slot i can be moved to the front, because
swaps that do not involve slot i commute with it.

Geometric view
--------------
Picture a tree of strings rooted at s1. Each level fixes one more prefix position, so the depth
grows left to right along the string; the branches at a node are the few positions holding the
letter that slot i is waiting for. The brute force is the same tree with every pair of letters
as a branch, which is why it explodes.

Steps
-----
1. queue = [s1], seen = {s1}, swaps = 0.
2. For each string in the current layer: if it equals s2 return swaps.
3. Find the first index i with cur[i] != s2[i].
4. For each j > i with cur[j] == s2[i] and cur[j] != s2[j]: swap, enqueue if unseen.
5. swaps += 1 and continue with the next layer.

Complexity: O(n * k^d) time and space worst case, where k is the pruned branching factor and
            d <= n-1 the swap count — exponential but tiny in practice; each state is O(n) to
            build and hash.
Pitfalls: branching on all swaps (TLE); allowing swaps that break a correct position; using
          DFS without a bound (finds a solution, not the minimum).
"""
import random
from collections import deque


class Solution:
    def kSimilarity(self, s1: str, s2: str) -> int:
        queue = deque([s1])
        seen = {s1}
        swaps = 0
        while queue:
            for _ in range(len(queue)):
                cur = queue.popleft()
                if cur == s2:
                    return swaps
                i = 0
                while cur[i] == s2[i]:           # first mismatch: it must be fixed eventually
                    i += 1
                for j in range(i + 1, len(cur)):
                    if cur[j] == s2[i] and cur[j] != s2[j]:   # fixes i, does not break j
                        nxt = cur[:i] + cur[j] + cur[i + 1:j] + cur[i] + cur[j + 1:]
                        if nxt not in seen:
                            seen.add(nxt)
                            queue.append(nxt)
            swaps += 1
        return -1                                # unreachable for anagrams


def brute_force(s1: str, s2: str) -> int:
    # BFS over ALL swaps: n(n-1)/2 neighbours per state, up to n! states -> exponential.
    n = len(s1)
    queue = deque([(s1, 0)])
    seen = {s1}
    while queue:
        cur, d = queue.popleft()
        if cur == s2:
            return d
        for i in range(n):
            for j in range(i + 1, n):
                lst = list(cur)
                lst[i], lst[j] = lst[j], lst[i]
                nxt = "".join(lst)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, d + 1))
    return -1


if __name__ == "__main__":
    s = Solution()
    assert s.kSimilarity("ab", "ba") == 1
    assert s.kSimilarity("abc", "bca") == 2
    assert s.kSimilarity("abac", "baca") == 2
    assert s.kSimilarity("aabc", "abca") == 2
    assert s.kSimilarity("abcdef", "abcdef") == 0                  # already equal
    assert s.kSimilarity("abcdefabcdefabcdefab", "bcdefabcdefabcdefaba") == 16   # n=20, fast
    assert s.kSimilarity("aabbccddeeff", "ffeeddccbbaa") == 6

    random.seed(5)
    for _ in range(200):
        n = random.randint(1, 7)
        a = [random.choice("abc") for _ in range(n)]
        b = a[:]
        random.shuffle(b)
        assert s.kSimilarity("".join(a), "".join(b)) == brute_force("".join(a), "".join(b))
    print("ok")
