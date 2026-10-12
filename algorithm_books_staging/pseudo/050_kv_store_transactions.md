---
rank: 50
slug: kv_store_transactions
---

Design a key-value store with `set(key, value)`, `get(key)` and `delete(key)`, plus transactions that nest. `begin()` opens a transaction, `rollback()` undoes every change made since the innermost open `begin` and closes that transaction, and `commit()` makes the changes of every open transaction permanent and closes them all. `get` returns `null` for an absent key, and `rollback` and `commit` return `OK`, or `NO TRANSACTION` when none is open. After `set(a, 10)`, `begin()`, `set(a, 20)`, `begin()` and `delete(a)`, the first rollback brings `a` back as `20` and the second as `10`.

The obvious design copies the whole dictionary at every `begin` and puts the copy back on rollback. It is correct, but it costs `O(n)` time and memory per `begin` for a store of `n` keys even when the transaction touches a single key, and every nested level pays again. A transaction only needs to remember what it changed. Keep one live dictionary that always holds the current state, and give each open transaction an undo log: a small map from every key that transaction changed to the value the key had before, with `null` for a key that did not exist. `begin` pushes an empty log onto a stack. Every `set` and `delete` first records the key in the innermost log and only then changes the live dictionary. Only the first change of a key within a level is recorded, because that is the value the level started with; later changes would save values the level itself wrote.

Rollback pops the innermost log and writes each saved value back, deleting the keys that were absent. Each key appears in a log once, so the order of the replay does not matter, and afterwards the live dictionary is exactly what it was at the matching `begin`, the state the outer logs were recorded against. Commit, with the semantics above, throws every log away, because the live dictionary already holds the committed state. Picture the logs as a stack of trays, one per open level, each holding the before-values of the keys its level touched; reads never look at the trays.

```text
operation            data                logs, innermost last
set(a, 10)           {a: 10}             []
begin()              {a: 10}             [{}]
set(a, 20)           {a: 20}             [{a: 10}]
set(b, 30)           {a: 20, b: 30}      [{a: 10, b: null}]
begin()              {a: 20, b: 30}      [{a: 10, b: null}, {}]
delete(a)            {b: 30}             [{a: 10, b: null}, {a: 20}]
set(b, 40)           {b: 40}             [{a: 10, b: null}, {a: 20, b: 30}]
set(b, 45)           {b: 45}             [{a: 10, b: null}, {a: 20, b: 30}]
rollback() → OK      {a: 20, b: 30}      [{a: 10, b: null}]
rollback() → OK      {a: 10}             []
rollback() → NO TRANSACTION
begin(), set(a, 50)  {a: 50}             [{a: 10}]
begin(), set(c, 70)  {a: 50, c: 70}      [{a: 10}, {c: null}]
commit() → OK        {a: 50, c: 70}      []         both levels are permanent
rollback() → NO TRANSACTION
```

```pseudo
CLASS KeyValueStore
    FUNCTION Init()
        self.data ← empty map               // key → value: the live state
        self.logs ← empty stack             // one undo log per open level

    FUNCTION Record(key)
        IF len(self.logs) = 0
            RETURN                          // no transaction: nothing to undo
        log ← self.logs.top()               // the innermost transaction
        IF key NOT IN log                   // only the first change is kept
            log[key] ← self.Get(key)        // null: the key was absent

    FUNCTION Set(key, value)
        self.Record(key)
        self.data[key] ← value

    FUNCTION Get(key)
        IF key IN self.data
            RETURN self.data[key]
        RETURN null

    FUNCTION Delete(key)
        IF key IN self.data
            self.Record(key)
            self.data.remove(key)

    FUNCTION Begin()
        self.logs.push(empty map)

    FUNCTION Rollback()
        IF len(self.logs) = 0
            RETURN "NO TRANSACTION"
        log ← self.logs.pop()               // undo the innermost level only
        FOR EACH key IN log
            IF log[key] = null              // absent before the level began
                IF key IN self.data
                    self.data.remove(key)
            ELSE
                self.data[key] ← log[key]   // the value before the level
        RETURN "OK"

    FUNCTION Commit()
        IF len(self.logs) = 0
            RETURN "NO TRANSACTION"
        self.logs ← empty stack             // nothing can be undone any more
        RETURN "OK"
```

`set`, `get`, `delete`, `begin` and `commit` cost `O(1)`, and `rollback` costs `O(k)` for the `k` keys its level changed; a log holds at most one entry per key, so memory follows the changes, never the size of the store. Since `null` marks an absent key, `null` is never stored as a value. The signals are undo, nested transactions, savepoints and "restore the state as of the last begin". Many databases roll back the same way, from undo records that hold the before-image of each changed row. The mirror design buffers each level's writes in its own map and applies them on commit: rollback becomes a single pop, but every read must search the levels from the innermost outward. If `commit` closed only the innermost level, its log would merge into the parent's, each key the parent lacks moving down so the parent can still undo it. Min Stack (#24) is a small cousin: every entry remembers the minimum below it, so a pop restores the old minimum for free. Snapshot Array (#47) keeps old versions instead of undo records. The classic mistake is recording a key on every change: after `set(b, 40)` and `set(b, 45)` the log would hold `40`, and the rollback would land on `40` instead of `30`. Forgetting to log `null` for a new key is the other one, since rollback then keeps a key the transaction created.

*Practice:* LC 1146 Snapshot Array · LC 981 Time Based Key-Value Store · LC 155 Min Stack
