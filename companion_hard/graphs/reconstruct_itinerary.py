"""
Reconstruct Itinerary (LeetCode 332) - Hard
Chapter: graphs
Pattern: Eulerian path (Hierholzer's DFS)

Tickets [from, to] all belong to one traveller who starts at "JFK". Reconstruct the itinerary
that uses every ticket exactly once; if several exist, return the one that is lexicographically
smallest when read as one string. A valid itinerary is guaranteed to exist.
Example: [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
-> ["JFK","MUC","LHR","SFO","SJC"]
"""


# --- helpers ---
def build_adj(tickets):
    """airport -> list of destinations (one entry per ticket, order not yet fixed)."""
    adj = {}
    for src, dst in tickets:
        if src not in adj:
            adj[src] = []
        adj[src].append(dst)
    return adj


# --- brute force ---
def backtrack(adj, used, path, total):
    """Extend path with any unused ticket, smallest destination first; undo when it dead-ends."""
    if len(path) == total + 1:
        return True                    # every ticket used
    cur = path[-1]
    if cur not in adj:
        return False                   # stranded with tickets left over
    for i in range(len(adj[cur])):
        if used[cur][i]:
            continue
        used[cur][i] = True
        path.append(adj[cur][i])
        if backtrack(adj, used, path, total):
            return True
        path.pop()                     # dead end: undo and try the next destination
        used[cur][i] = False
    return False


def brute_force(tickets):
    """Backtrack over unused tickets in lexical order; the first full path is smallest. O(E!)."""
    adj = build_adj(tickets)
    used = {}
    for src in adj:
        adj[src].sort()                # ascending: try the smallest destination first
        used[src] = [False] * len(adj[src])
    path = ["JFK"]
    backtrack(adj, used, path, len(tickets))
    return path


# --- optimal ---
def visit(adj, airport, route):
    """Hierholzer: use up every ticket out of airport, then record the airport (post-order)."""
    while airport in adj and adj[airport]:
        next_stop = adj[airport].pop()     # smallest remaining destination (list is descending)
        visit(adj, next_stop, route)
    route.append(airport)              # stranded or finished here: this airport goes to the END


def reconstruct_itinerary(tickets):
    """Hierholzer's DFS: fly greedily, record each airport when stuck, then reverse. O(E log E)."""
    adj = build_adj(tickets)
    for src in adj:
        adj[src].sort(reverse=True)    # descending, so pop() from the end yields the smallest
    route = []
    visit(adj, "JFK", route)
    return route[::-1]


# --- try the brute force ---
print(brute_force([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]))
# -> ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']
tickets_b = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
print(brute_force(tickets_b))                     # -> ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO']
tickets_c = [["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]
print(brute_force(tickets_c))                     # -> ['JFK', 'NRT', 'JFK', 'KUL']
print(brute_force([["JFK", "AAA"]]))              # -> ['JFK', 'AAA']


# --- try the optimal ---
print(reconstruct_itinerary([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]))
# -> ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']
tickets_b = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
print(reconstruct_itinerary(tickets_b))           # -> ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO']
tickets_c = [["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]
print(reconstruct_itinerary(tickets_c))           # -> ['JFK', 'NRT', 'JFK', 'KUL']
print(reconstruct_itinerary([["JFK", "AAA"]]))    # -> ['JFK', 'AAA']
