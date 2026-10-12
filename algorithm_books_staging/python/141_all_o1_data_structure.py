"""
All O(1) Data Structure - A Linked List of Count Buckets

Count string keys: inc(key) adds one, dec(key) subtracts one (a key at 0
disappears), and get_max_key() and get_min_key() return a key with the largest
or smallest count, or "" when empty, all in O(1). inc hello twice, inc leet:
get_max_key() -> hello, get_min_key() -> leet.
"""


# --- helpers ---
class Bucket:
    def __init__(self, count):
        self.count = count
        self.keys = set()               # every key with exactly this count
        self.prev = None
        self.next = None


def any_key(keys):
    """Some key of a non-empty set: the first one a loop meets. O(1)."""
    for key in keys:
        return key


def bucket_list(counter):
    """The buckets from head to tail as [count, sorted keys] pairs."""
    result = []
    bucket = counter.head.next
    while bucket is not counter.tail:
        result.append([bucket.count, sorted(bucket.keys)])
        bucket = bucket.next
    return result


# --- algorithm ---
class AllOne:
    """Buckets of keys in increasing count between two sentinels, plus
    key -> bucket. Every operation is O(1)."""

    def __init__(self):
        self.head = Bucket(0)           # sentinel before the smallest count
        self.tail = Bucket(0)           # sentinel after the largest count
        self.head.next = self.tail
        self.tail.prev = self.head
        self.bucket_of = {}             # key -> the bucket that holds it

    def insert_after(self, bucket, count):
        """Splice a new empty bucket for count right after bucket. O(1)."""
        fresh = Bucket(count)
        fresh.prev = bucket
        fresh.next = bucket.next
        bucket.next.prev = fresh
        bucket.next = fresh
        return fresh

    def remove_key(self, bucket, key):
        """Take key out of bucket; unlink the bucket once it is empty. O(1)."""
        bucket.keys.remove(key)
        if len(bucket.keys) == 0:       # empty: unlink the bucket
            bucket.prev.next = bucket.next
            bucket.next.prev = bucket.prev

    def inc(self, key):
        """Move key to the count + 1 bucket just after its own. O(1)."""
        if key in self.bucket_of:
            current = self.bucket_of[key]
        else:
            current = self.head         # a new key comes from count 0
        target = current.next
        if target is self.tail or target.count != current.count + 1:
            target = self.insert_after(current, current.count + 1)
        target.keys.add(key)
        self.bucket_of[key] = target
        if current is not self.head:
            self.remove_key(current, key)   # only after target is linked

    def dec(self, key):
        """Move key to the count - 1 bucket just before its own; at count 0
        the key is gone. O(1)."""
        if key not in self.bucket_of:
            return
        current = self.bucket_of[key]
        if current.count == 1:
            del self.bucket_of[key]     # count 0: the key disappears
        else:
            target = current.prev
            if target is self.head or target.count != current.count - 1:
                target = self.insert_after(current.prev, current.count - 1)
            target.keys.add(key)
            self.bucket_of[key] = target
        self.remove_key(current, key)

    def get_max_key(self):
        """A key of the last bucket, before tail; "" when empty. O(1)."""
        if self.tail.prev is self.head:
            return ""
        return any_key(self.tail.prev.keys)

    def get_min_key(self):
        """A key of the first bucket, after head; "" when empty. O(1)."""
        if self.head.next is self.tail:
            return ""
        return any_key(self.head.next.keys)


# --- try it ---
counter = AllOne()
counter.inc("hello")
counter.inc("hello")
print(counter.get_max_key(), counter.get_min_key())     # -> hello hello
counter.inc("leet")
print(counter.get_max_key(), counter.get_min_key())     # -> hello leet
print(bucket_list(counter))         # -> [[1, ['leet']], [2, ['hello']]]
counter.inc("leet")
print(bucket_list(counter))         # -> [[2, ['hello', 'leet']]]
counter.dec("hello")
print(counter.get_max_key(), counter.get_min_key())     # -> leet hello
counter.dec("hello")                # count 0: hello disappears
counter.dec("leet")
print(bucket_list(counter), counter.get_max_key())  # -> [[1, ['leet']]] leet
counter.dec("leet")
print(repr(counter.get_max_key()), repr(counter.get_min_key()))   # -> '' ''
