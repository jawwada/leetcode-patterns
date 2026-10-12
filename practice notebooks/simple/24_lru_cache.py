"""
LRU Cache (LeetCode 146)
Design a cache with get/put in O(1) that evicts the least recently used key when full.
  cap 2: put(1,1) put(2,2) get(1) put(3,3) get(2)  ->  1, -1   (2 was evicted)

Idea: a dict finds a key's node in O(1); a doubly linked list keeps nodes in
      recency order (front = newest, back = oldest) so moving/removing is O(1).

Pseudocode:
  get(key):  if missing -> -1; else move node to front, return val
  put(key, val):
      if key exists: update val, unlink it
      else: make node; if over capacity -> remove node before tail
      push node to front

Time O(1) per op, space O(capacity).
"""


class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val, self.prev, self.next = key, val, None, None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}                          # key -> node
        self.head, self.tail = Node(), Node()  # sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)                     # move to front = most recent
        self._push_front(node)
        return node.val

    def put(self, key, value):
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._unlink(node)
        else:
            node = self.map[key] = Node(key, value)
            if len(self.map) > self.capacity:  # evict the oldest
                oldest = self.tail.prev
                self._unlink(oldest)
                del self.map[oldest.key]
        self._push_front(node)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1); cache.put(2, 2)
    print(cache.get(1))  # 1
    cache.put(3, 3)      # evicts key 2
    print(cache.get(2))  # -1
    cache.put(4, 4)      # evicts key 1
    print(cache.get(1), cache.get(3), cache.get(4))  # -1 3 4
