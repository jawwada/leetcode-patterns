"""
Accounts Merge (LeetCode 721)  — Medium
Pattern: Union-Find (disjoint set union)

Problem
-------
accounts[i] = [name, email1, email2, ...]. Two accounts belong to the same person if they
share at least one email (names can repeat across different people). Merge them: return
each person's [name, sorted emails...]; output order does not matter.
Example: [["John","a@m","b@m"],["John","b@m","c@m"],["Mary","d@m"]]
-> [["John","a@m","b@m","c@m"],["Mary","d@m"]].

Brute force
-----------
Treat accounts as nodes and connect two accounts if their email sets intersect; find
connected components by DFS. Building the adjacency means comparing every pair of
accounts: O(A^2 * k) with A accounts of up to k emails (set intersection per pair), plus
O(A + E) for the DFS; O(A^2) space for edges. The waste is the all-pairs intersection
test: most pairs share nothing, yet every pair is checked.

From brute force to optimal
---------------------------
The redundancy is pairwise comparison to discover shared emails. Observation: an email is
shared iff it appears in two accounts, which a single hash map email -> first account
index detects in O(1) per email, with no pairwise step. The relation "same person" is
transitive and components only merge, so union-find over account indices is the natural
store: for each email, if it was already seen under account j, union(i, j). Afterwards
group emails by find(root). Total O(N * alpha(A) + N log N) for N total emails (the log
comes from sorting the output emails).

Intuition
---------
Each account starts as its own person. Walk every email; the first time you see an email,
remember which account it came from; the next time, that proves two accounts are the
same person -- union them. At the end, bucket all emails by their account's root and sort
each bucket.

Geometric view
--------------
Draw account indices as dots with self-pointing parent arrows. Every email is a thread
hanging from an account; when a second account grabs the same thread, redirect one root
arrow to the other so the two parent-trees become one. Finally each tree's root collects
all the threads (emails) hanging below it into one sorted list.

Steps
-----
1. parent = list(range(len(accounts))); owner = {} (email -> account index).
2. For account i, each email e: if e in owner: union(i, owner[e]) else owner[e] = i.
3. groups = {find(owner[e]): [emails]} for every email.
4. For each root, output [accounts[root][0]] + sorted(emails).

Complexity: O(N log N) time, O(N) space — N total emails each unioned once; sorting each group dominates.
Pitfalls: using names as keys (different people can share a name); forgetting that emails
within one account must also be grouped even if never shared; returning unsorted emails.
"""
from collections import defaultdict
from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        parent = list(range(len(accounts)))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        owner = {}  # email -> index of the first account that listed it
        for i, acct in enumerate(accounts):
            for email in acct[1:]:
                if email in owner:
                    parent[find(i)] = find(owner[email])  # shared email => same person
                else:
                    owner[email] = i
        groups = defaultdict(list)
        for email, i in owner.items():
            groups[find(i)].append(email)
        return [[accounts[root][0]] + sorted(emails) for root, emails in groups.items()]


def brute_force(accounts: List[List[str]]) -> List[List[str]]:
    # Compare every pair of accounts for a shared email, then DFS the resulting graph.
    n = len(accounts)
    sets = [set(a[1:]) for a in accounts]
    adj = [[j for j in range(n) if j != i and sets[i] & sets[j]] for i in range(n)]
    seen, result = set(), []
    for i in range(n):
        if i in seen:
            continue
        seen.add(i)
        stack, emails = [i], set()
        while stack:
            cur = stack.pop()
            emails |= sets[cur]
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        result.append([accounts[i][0]] + sorted(emails))
    return result


def canon(result: List[List[str]]) -> List[List[str]]:
    return sorted(result)


if __name__ == "__main__":
    s = Solution()
    a1 = [["John", "johnsmith@mail.com", "john_newyork@mail.com"],
          ["John", "johnsmith@mail.com", "john00@mail.com"],
          ["Mary", "mary@mail.com"],
          ["John", "johnnybravo@mail.com"]]
    w1 = [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
          ["Mary", "mary@mail.com"],
          ["John", "johnnybravo@mail.com"]]
    a2 = [["Ann", "a@x"], ["Bob", "b@x"], ["Ann", "c@x"], ["Ann", "a@x", "c@x"]]  # chain-merge through the last
    w2 = [["Ann", "a@x", "c@x"], ["Bob", "b@x"]]
    a3 = [["Solo", "s@x"]]
    for acc, want in ((a1, w1), (a2, w2), (a3, [["Solo", "s@x"]])):
        assert canon(s.accountsMerge(acc)) == canon(want)
        assert canon(brute_force(acc)) == canon(want)
    print("ok")
