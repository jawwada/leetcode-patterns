"""
Reconstruct Itinerary (LeetCode 332)  — Hard
Pattern: Eulerian path (Hierholzer's DFS)

Problem
-------
Given tickets [from, to], all belonging to one traveller starting at "JFK", reconstruct the
itinerary that uses every ticket exactly once. If several exist, return the one with the
smallest lexical order when read as a single string. A valid itinerary is guaranteed.
Example: [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
-> ["JFK","MUC","LHR","SFO","SJC"].

Brute force
-----------
Backtracking: from the current airport, try each unused ticket in lexical order of
destination, recurse, and undo if the recursion fails to consume every ticket. The first
complete path found is lexically smallest. Worst case explores many dead-end prefixes
that are abandoned deep into the recursion -> exponential time (O(E!) bound-ish), O(E)
space. The wasted work: the search commits to a lexically small edge early, reaches a dead
end, and unwinds and rebuilds huge suffixes.

From brute force to optimal
---------------------------
The problem is an Eulerian path (use every edge once), and a valid one is guaranteed.
Observation (Hierholzer): when a DFS that greedily consumes edges gets stuck at an airport
with no unused outgoing tickets, that airport must be the END of the itinerary (or of a
cycle that can be spliced in). So instead of undoing, record the airport on the way OUT of
the recursion (post-order) and reverse at the end. No backtracking is needed; each edge is
consumed exactly once. Sorting each airport's destinations in reverse and popping from
the end gives lexical order in O(E log E) total.

Intuition
---------
Greedily fly the smallest available destination. When you are stranded (no tickets left
from here), that airport is the last stop of whatever sub-route you are on -- write it
down and back out one step. Because we write airports down only when they are finished,
the written list is the itinerary in reverse.

Geometric view
--------------
Picture airports as dots and tickets as arrows. The DFS path walks arrows, deleting each
as it is used. When it hits a dot with no arrows left, that dot is pinned to the END of
the route and the walk retreats one step, possibly discovering a side loop from there;
that loop gets pinned just before the dead end. Reading the pins backwards gives one
continuous path that covers every arrow.

Steps
-----
1. Build adj: src -> list of destinations sorted in DESCENDING order (so pop() gives the
   smallest).
2. DFS(u): while adj[u] has tickets: DFS(adj[u].pop()); then route.append(u).
3. Start DFS("JFK"); return reversed(route).

Complexity: O(E log E) time, O(E) space — sorting dominates; each ticket popped once; recursion depth up to E.
Pitfalls: appending on the way IN (pre-order) breaks on dead ends; forgetting to reverse;
sorting ascending and popping from the front (O(E) per pop) -- use a deque or reverse sort.
"""
from collections import defaultdict
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        adj = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            adj[src].append(dst)  # descending, so pop() yields the smallest destination
        route = []

        def dfs(airport: str) -> None:
            while adj[airport]:
                dfs(adj[airport].pop())
            route.append(airport)  # post-order: stranded airport goes to the END

        dfs("JFK")
        return route[::-1]


def brute_force(tickets: List[List[str]]) -> List[str]:
    # Backtracking: try unused tickets in lexical order, undo on failure.
    adj = defaultdict(list)
    for src, dst in sorted(tickets):
        adj[src].append(dst)
    used = {src: [False] * len(dsts) for src, dsts in adj.items()}
    path = ["JFK"]

    def backtrack() -> bool:
        if len(path) == len(tickets) + 1:
            return True
        cur = path[-1]
        for i, dst in enumerate(adj[cur]):
            if used[cur][i]:
                continue
            used[cur][i] = True
            path.append(dst)
            if backtrack():
                return True
            path.pop()
            used[cur][i] = False
        return False

    backtrack()
    return path


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]], ["JFK", "MUC", "LHR", "SFO", "SJC"]),
        ([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],
         ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]),
        ([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]], ["JFK", "NRT", "JFK", "KUL"]),  # greedy-smallest dead-ends
        ([["JFK", "AAA"]], ["JFK", "AAA"]),
    )
    for t, want in cases:
        assert brute_force(t) == want
        assert s.findItinerary(t) == want
    print("ok")
