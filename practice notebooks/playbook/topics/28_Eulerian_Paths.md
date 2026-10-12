## Eulerian Paths

An Eulerian path uses every edge exactly once. Hierholzer's algorithm records a node when it has no remaining outgoing edges, then reverses that finishing order.

<!-- cell -->

Reconstruct Itinerary gives plane tickets `[from, to]`, all used by one traveller who starts at JFK, and asks for the route that uses every ticket exactly once, the smallest in lexical order when several exist: the four tickets below fly JFK, MUC, LHR, SFO, SJC. Backtracking over ticket orders can dead-end deep down and undo a lot.

Hierholzer's algorithm never undoes a flight. Always fly the smallest unused ticket; when you are stuck at an airport, it must be the *end* of what is left, so write it down and back up one step. Airports are written in reverse finishing order, so the route is reversed at the end.

<!-- cell -->

```python
def find_itinerary(tickets):
    graph = defaultdict(list)
    tickets = sorted(tickets, reverse=True)       # INIT: reverse-sorted, so pop() hands out the smallest
    for a, b in tickets:
        graph[a].append(b)
    route, stack = [], ["JFK"]
    while stack:
        while graph[stack[-1]]:                   # keep flying while this airport has unused tickets
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())                 # stuck here: this airport is finished, write it down
    return route[::-1]                            # airports were written in reverse finishing order


print(find_itinerary([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]))   # ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']
print(find_itinerary([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]))                  # ['JFK', 'NRT', 'JFK', 'KUL']
```

<!-- cell -->

**Try it**
- Write each airport down on the way *in* instead (append it when you fly to it, no reverse): the second example becomes `['JFK', 'KUL', 'NRT', 'JFK']`, which needs a KUL → NRT ticket that does not exist.
- Sort ascending instead (drop `reverse=True`): `pop()` now hands out the *largest* destination. For `[["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]` you get `['JFK', 'SFO', 'ATL', 'JFK', 'ATL', 'SFO']`: it uses every ticket, but it is not the smallest route.
- Print `route[-1], stack` each time an airport is written, for the second example: `KUL ['JFK']` comes first. KUL is a dead end, so it must end the trip; the loop through NRT is flown after it and written before the start, so the reversal puts KUL last.
