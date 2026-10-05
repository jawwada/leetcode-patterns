"""
LRU Cache (LeetCode 146) - Medium-Hard
Area: linked list / design
Key operations: dict lookup, unlink a node, push front after sentinel head, evict tail.prev

Design a cache of fixed capacity with get(key) -> value or -1, and put(key, value); both in O(1). When a
put would exceed the capacity, evict the least recently used key (the one whose last get or put is oldest).
Here solve(capacity, ops) runs a list of ("get", k) / ("put", k, v) operations and returns the get results.
Example: capacity 2, put(1,1) put(2,2) get(1) put(3,3) get(2) put(4,4) get(1) get(3) get(4) -> [1, -1, -1, 3, 4]
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class Node:
    def __init__(self, key=None, val=None):
        self.key, self.val, self.prev, self.next = key, val, None, None


def draw(head):
    out, node = [], head
    while node:
        out.append(f"({node.key}:{node.val})" if node.val is not None else str(node.key))
        node = node.next
    return " <-> ".join(out)


# --- brute force ---
def brute_force(capacity, ops):
    """Keep (key, value) pairs in a plain list, most recent first: every op scans the list for the key and
    shifts the rest to move it to the front, O(capacity) per op. The dict removes the scan, the doubly
    linked list removes the shift."""
    items, results = [], []
    for op in ops:
        key = op[1]
        i = next((i for i, kv in enumerate(items) if kv[0] == key), -1)
        if op[0] == "get":
            if i >= 0:
                items.insert(0, items.pop(i))
            results.append(items[0][1] if i >= 0 else -1)
        else:
            if i >= 0:
                items.pop(i)
            items.insert(0, (key, op[2]))
            if len(items) > capacity:
                items.pop()
    return results


# --- optimal ---
def solve(capacity, ops):
    """dict key -> node, plus the nodes chained in recency order between two sentinels: head side is the
    most recent, tail.prev is the next to evict. Every op is one lookup and O(1) pointer rewrites."""
    head, tail = Node("head"), Node("tail")
    head.next, tail.prev = tail, head
    where, results = {}, []

    def unlink(node):
        node.prev.next, node.next.prev = node.next, node.prev

    def push_front(node):
        node.prev, node.next = head, head.next
        head.next.prev = node
        head.next = node

    for op in ops:
        if op[0] == "get":
            node = where.get(op[1])
            if node:
                unlink(node)
                push_front(node)
                log(f"get {op[1]}: hit, moved to the front")
            results.append(node.val if node else -1)
        else:
            _, key, val = op
            if key in where:
                where[key].val = val
                unlink(where[key])
                log(f"put {key}: key exists, update value and unlink it")
            else:
                where[key] = Node(key, val)
                if len(where) > capacity:
                    victim = tail.prev
                    unlink(victim)
                    del where[victim.key]
                    log(f"put {key}: over capacity, evict ({victim.key}:{victim.val}) from the tail")
            push_front(where[key])
        log(f"{op} -> {results[-1] if op[0] == 'get' else 'ok':>3} | {draw(head)} | keys {sorted(where)}")
    return results


# --- demo ---
def demo():
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2), ("put", 4, 4), ("get", 1), ("get", 3), ("get", 4)]
    return solve(2, ops)


# --- tests ---
def tests():
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2), ("put", 4, 4), ("get", 1), ("get", 3), ("get", 4)]
    assert solve(2, ops) == [1, -1, -1, 3, 4]
    assert solve(1, [("put", 5, 5), ("put", 5, 6), ("get", 5), ("put", 7, 7), ("get", 5), ("get", 7)]) == [6, -1, 7]
    assert solve(2, [("get", 1)]) == [-1]
    assert solve(2, [("put", 1, 1), ("put", 2, 2), ("put", 1, 10), ("put", 3, 3), ("get", 1), ("get", 2)]) == [10, -1]
    assert solve(3, [("put", 1, 1), ("put", 2, 2), ("put", 3, 3), ("get", 1), ("get", 2), ("put", 4, 4), ("get", 3)]) == [1, 2, -1]
    assert solve(2, []) == []
    import random
    random.seed(0)
    for _ in range(200):
        capacity = random.randint(1, 4)
        ops = []
        for _ in range(random.randint(0, 25)):
            k = random.randint(0, 5)
            ops.append(("get", k) if random.random() < 0.4 else ("put", k, random.randint(0, 99)))
        assert solve(capacity, ops) == brute_force(capacity, ops), (capacity, ops)


# --- bugs ---
BUGS = [
    {
        "replace": "                    victim = tail.prev",
        "with":    "                    victim = head.next",
        "fix": "evict from the tail side: the least recently used node is tail.prev",
        "why": "head.next is the most recently used node, so the cache throws away what was just touched; in the example put(3,3) evicts key 1 and get(2) returns 2 instead of -1.",
        "decoys": [
            {"line": "        head.next.prev = node", "change": "should be head.prev = node"},
            {"line": "                    del where[victim.key]", "change": "should delete where[key]"},
            {"line": "            results.append(node.val if node else -1)", "change": "should append None on a miss"},
        ],
    },
    {
        "replace": "                if len(where) > capacity:",
        "with":    "                if len(where) >= capacity:",
        "fix": "evict only when the new key pushes the size past capacity, so compare with >",
        "why": "With >= the cache evicts as soon as it is full, so a capacity-2 cache keeps one entry; put(1), put(2), get(1) gives -1.",
        "decoys": [
            {"line": "        node.prev.next, node.next.prev = node.next, node.prev", "change": "should assign node.prev and node.next instead"},
            {"line": "                where[key] = Node(key, val)", "change": "should store Node(val, key)"},
            {"line": "            push_front(where[key])", "change": "should run only for new keys"},
        ],
    },
    {
        "replace": "                unlink(where[key])",
        "with":    "                continue",
        "fix": "unlink the existing node so push_front can move it to the front",
        "why": "Updating the value without refreshing recency leaves the key at its old position; put(1), put(2), put(1, 10), put(3) then evicts key 1 instead of key 2.",
        "decoys": [
            {"line": "        node.prev, node.next = head, head.next", "change": "should be head.next, head"},
            {"line": "            node = where.get(op[1])", "change": "should use where[op[1]]"},
            {"line": "    head.next, tail.prev = tail, head", "change": "should also set head.prev = tail"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
