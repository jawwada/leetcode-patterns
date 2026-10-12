"""
Key-Value Store with Transactions - A Stack of Undo Logs

Design a key-value store with set, get and delete plus nested transactions:
begin() opens one, rollback() undoes the innermost and commit() makes them all
permanent: set a = 10, begin, set a = 20, rollback -> get a is 10 again.
"""


# --- algorithm ---
class KeyValueStore:
    """The live dict plus a stack of undo logs, one per open transaction.
    set, get, delete, begin and commit O(1); rollback O(changes undone)."""

    def __init__(self):
        self.data = {}              # key -> value: the live state
        self.logs = []              # stack of undo logs, innermost last

    def record(self, key):
        """Log the key's value before its first change in this level. O(1)."""
        if len(self.logs) == 0:
            return                  # no transaction: nothing to undo
        log = self.logs[-1]         # the innermost transaction
        if key not in log:          # only the first change is kept
            log[key] = self.get(key)    # None: the key was absent

    def set(self, key, value):
        """Log the old value, then write the new one. O(1)."""
        self.record(key)
        self.data[key] = value

    def get(self, key):
        """The live value, or None when the key is absent. O(1)."""
        if key in self.data:
            return self.data[key]
        return None

    def delete(self, key):
        """Log the old value, then remove the key. O(1)."""
        if key in self.data:
            self.record(key)
            del self.data[key]

    def begin(self):
        """Open a nested transaction with an empty undo log. O(1)."""
        self.logs.append({})

    def rollback(self):
        """Pop the innermost log, write back its k saved values. O(k)."""
        if len(self.logs) == 0:
            return "NO TRANSACTION"
        log = self.logs.pop()       # undo the innermost level only
        for key in log:
            if log[key] is None:            # absent before the level began
                if key in self.data:
                    del self.data[key]
            else:
                self.data[key] = log[key]   # the value before the level
        return "OK"

    def commit(self):
        """Make every open transaction permanent by dropping the logs. O(1)."""
        if len(self.logs) == 0:
            return "NO TRANSACTION"
        self.logs = []              # nothing can be undone any more
        return "OK"


# --- try it ---
store = KeyValueStore()
store.set("a", 10)
store.begin()
store.set("a", 20)
store.set("b", 30)
store.begin()
store.delete("a")
store.set("b", 40)
store.set("b", 45)              # a second change: the log keeps b: 30
print(store.get("a"), store.get("b"))                     # -> None 45
print(store.rollback(), store.get("a"), store.get("b"))   # -> OK 20 30
print(store.rollback(), store.get("a"), store.get("b"))   # -> OK 10 None
print(store.rollback())                                   # -> NO TRANSACTION
store.begin()
store.set("a", 50)
store.begin()
store.set("c", 70)
print(store.commit(), store.get("a"), store.get("c"))     # -> OK 50 70
print(store.rollback(), store.get("a"))                   # -> NO TRANSACTION 50
