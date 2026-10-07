## Linked Lists

> A linked list is a chain of boxes, each holding a value and **one** arrow to the next box. You can't index into it, walk it backwards or see its length; all you can do is put named fingers on boxes (`prev`, `cur`, `slow`, `fast`) and re-aim arrows. Every algorithm is careful pointer surgery: **give every box you will touch a name, then rewire.**

**Reach for it when** the input is a `ListNode`; the problem says *in place* or *O(1) extra space*; it asks for the **middle**, the **k-th from the end**, a **cycle**, a **merge** or a **reversal**; or an array's values are indices into the same array (then the array *is* a linked list, and Floyd's cycle trick applies).

**In this repo:** `linked_list/` (12 problems) · bank: `practice/simple/21_reverse_linked_list.py`, `practice/simple/22_merge_two_sorted_lists.py`, `practice/simple/23_linked_list_cycle_ii.py`, `practice/simple/25_remove_nth_node_from_end.py` · basics: `practice/simple/basics/linked_lists/` (build/insert/delete, reverse iterative and recursive, middle, Floyd, merge, palindrome, k-group, add two numbers). LRU Cache (a dict plus a doubly linked list) is taught in [Design](#s24).

### The picture

```text
A box holds a value and ONE arrow. A variable is a finger pointing at a box.

  head
   v
  [1]->[2]->[3]->None

Delete 2: put a finger on the box BEFORE it and re-aim that box's arrow past the victim.

  prev
   v
  [1]  [2]->[3]->None          prev.next = prev.next.next
   |         ^                 (nothing points at 2 any more: it is gone)
   +---------+

A dummy box in front gives even the head a box before it:

  [D]->[1]->[2]->None          deleting the head is just dummy.next = dummy.next.next,
                               and the answer is always dummy.next
```

Most steps change more than one arrow. Make it mechanical: draw 3 or 4 boxes before and after **one** step, then type three moves.

```text
  before:  [prev]->[a]->[b]->[after]          after:  [prev]->[b]->[a]->[after]

  1. NAME    every box the step touches:     a, b, after = prev.next, prev.next.next, prev.next.next.next
  2. REWIRE  the changed arrows, any order:  prev.next, b.next, a.next = b, a, after
  3. MOVE    the fingers last:               prev = a

Once every box has a name, no write can lose anything, so the order of the writes stops mattering.
Inserting x after prev is the same recipe: name after = prev.next, then prev.next, x.next = x, after.
```

The fingers can also *measure*, which is how a list answers questions an array answers with an index:

```text
middle: slow moves 1 box, fast moves 2; when fast can't take two more steps, slow is halfway

  [1]->[2]->[3]->[4]->[5]->None
             ^         ^
           slow      fast

n-th from the end (n = 2): open a gap of n + 1 links, then slide both until fast falls off

  [D]->[1]->[2]->[3]->[4]->[5]->None
                  ^               ^
                slow            fast          slow.next (4) is 2nd from the end: skip it
```

Why it is fast (and small): the brute force for almost every list problem is "copy the nodes into a Python list, use indices, rebuild". That is O(n) time but O(n) extra space, and the interviewer will ask you to drop it. Each list technique replaces one array superpower with a pointer trick: *index from the end* becomes a finger trailing by a fixed gap; *the middle* becomes a finger at half speed; *walk backwards* becomes "reverse that half in place"; *have I been here before?* becomes a fast finger lapping a slow one. Fingers only move forward, so each trick is O(n) time and O(1) space.

### From idea to code

**The idea in one sentence:** *name every box a step touches, rewire the arrows, move the fingers last, and put a dummy box in front so the head is never a special case.*

| Decision | Linked-list answer |
|---|---|
| **State**: what must I remember? | a few fingers: `prev`/`cur` to rewire, `tail` to build a new chain, `slow`/`fast` to measure; often a `dummy` box in front of the head |
| **Definition**: what exactly does each variable mean? | say it in a comment: `prev` = head of the already-reversed part, `cur` = first box not processed yet, `tail` = last box of the answer so far |
| **Invariant**: what is true at the end of every step? | everything before `cur` is done and reachable from `prev` (or `dummy`); everything from `cur` on is untouched and reachable from `cur` |
| **Step**: how does one box change the state? | name every box the step touches (`nxt = cur.next`), rewire the arrows, then move the fingers |
| **Record**: when is the answer updated? | building: hang a box on `tail`. Rewiring in place: nothing to record, the structure *is* the answer. Finding: the moment the fingers meet or stop (`slow is fast`, `fast` falls off), then act on that box (return it, skip it) |
| **Init**: starting values | `dummy = ListNode(0, head)`; `prev = None, cur = head` for a reversal; `slow = fast = head` (or `dummy`) for measuring |
| **Return**: what comes back? | `dummy.next` (never `head`: the head may have moved or been deleted), `prev` after a reversal, a box or `None` for a search |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "a box in front of the head" | `dummy = ListNode(0, head)` |
| "name the box I am about to lose" | `nxt = cur.next` |
| "flip this arrow backwards" | `cur.next = prev` |
| "move both fingers on" | `prev, cur = cur, nxt` |
| "skip (delete) the next box" | `prev.next = prev.next.next` |
| "hang a box on the end of the answer" | `tail.next = node` then `tail = tail.next` |
| "can fast take two more steps?" | `while fast and fast.next:` |
| "the same box" (not the same value) | `a is b` |
| "the answer starts after the dummy" | `return dummy.next` |

First the box itself, and two helpers to turn a Python list into a linked list and back:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def build_list(values):                      # [1, 2, 3] -> 1 -> 2 -> 3, returns the head
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head, limit=1000):               # 1 -> 2 -> 3 -> [1, 2, 3]
    out = []
    while head and len(out) < limit:         # the limit stops a walk around a cycle
        out.append(head.val)
        head = head.next
    return out


head = build_list([1, 2, 3])
print(head.val, head.next.val, head.next.next.next)   # 1 2 None
print(to_list(head))                                  # [1, 2, 3]
```

**Try it**
- `build_list([])` returns `None` (an empty list is just "no first box"), and `to_list(None)` is `[]`. Check both.
- Make a cycle by hand: `h = build_list([1, 2, 3]); h.next.next.next = h`, then `to_list(h, 7)` gives `[1, 2, 3, 1, 2, 3, 1]`. Without the limit this walk would never end: remember that when a bug creates a cycle.

Three templates cover most problems: rewire in place (reverse), build a new chain (merge), and fingers that measure (middle, n-th from the end). The tags are the seven decisions, and the **order** of the tagged lines is a decision too: `reverse_list` names `nxt` before the flip (flip first and the rest of the list is lost) and moves the fingers last; `merge_lists` hangs a box on the answer (RECORD) before `tail` steps onto it (STEP); `remove_nth_from_end` acts only after the slide, when `slow` is known to sit just before the victim.

```python
def reverse_list(head):
    prev, cur = None, head                   # STATE + INIT: prev = reversed part, cur = the rest
    while cur:
        nxt = cur.next                       # 1. name the box you would lose
        cur.next = prev                      # 2. STEP: flip one arrow
        prev, cur = cur, nxt                 # 3. move both fingers one box right
    return prev                              # RETURN: the old last box is the new head


def merge_lists(a, b):
    dummy = tail = ListNode()                # STATE + INIT: tail = last box of the answer
    while a and b:
        if a.val <= b.val:                   # the smaller front box goes next
            tail.next, a = a, a.next         # RECORD: hang it on the answer
        else:
            tail.next, b = b, b.next
        tail = tail.next                     # STEP: tail moves onto the box just hung
    tail.next = a or b                       # the leftover is already sorted: hang it whole
    return dummy.next                        # RETURN: skip the dummy


def middle_node(head):
    slow = fast = head                       # STATE + INIT: both fingers on the head
    while fast and fast.next:                # while fast can take two more steps
        slow, fast = slow.next, fast.next.next   # STEP: slow moves 1 box, fast moves 2
    return slow                              # RETURN: the middle (the 2nd middle if even)


def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)                # INIT: a box before the head, so the head can go too
    slow = fast = dummy                      # STATE: two fingers that will stay n + 1 links apart
    for _ in range(n + 1):
        fast = fast.next                     # INIT: open the gap of n + 1 links
    while fast:                              # until fast falls off the end
        slow, fast = slow.next, fast.next    # STEP: both move one box; the gap stays n + 1
    slow.next = slow.next.next               # RECORD: slow stopped just before the victim; skip it
    return dummy.next                        # RETURN: never `head` (it may be gone)


print(to_list(reverse_list(build_list([1, 2, 3, 4, 5]))))                   # [5, 4, 3, 2, 1]
print(to_list(merge_lists(build_list([1, 2, 4]), build_list([1, 3, 4]))))   # [1, 1, 2, 3, 4, 4]
print(middle_node(build_list([1, 2, 3, 4, 5])).val, middle_node(build_list([1, 2, 3, 4])).val)   # 3 3
print(to_list(remove_nth_from_end(build_list([1, 2, 3, 4, 5]), 2)))         # [1, 2, 3, 5]
```

**Try it**
- Swap the first two lines inside `reverse_list`'s loop (flip, *then* name) and reverse `[1, 2, 3, 4, 5]`: you get `[1]`. After the flip, `cur.next` is `None`, so `nxt` named nothing and the rest of the list is lost.
- In `remove_nth_from_end`, change `range(n + 1)` to `range(n)`: `[1, 2, 3, 4, 5], 2` now gives `[1, 2, 3, 4]`. With a gap of n, `slow` stops *on* the 4 instead of before it, so the wrong box is skipped.
- Change `while fast and fast.next:` to `while fast.next:` and call `middle_node(build_list([1, 2, 3, 4]))`: `AttributeError`, because on an even length `fast` itself becomes `None`. Odd lengths still work, which is why this bug survives a quick test.
- Delete `tail.next = a or b` from `merge_lists`: the merge prints `[1, 1, 2, 3, 4]`. The second list's `4` was still waiting when the first list ran out, so it was never hung on the answer.

**Several arrows in one step.** Swap Nodes in Pairs (24) is the three-move recipe from the picture, word for word. Remove Linked List Elements (203) adds the other everyday rule: after a delete, don't move. The finger must look at the *new* `cur.next`, which nobody has checked yet.

```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy                                  # STATE: the box before the next pair
    while prev.next and prev.next.next:
        a, b, after = prev.next, prev.next.next, prev.next.next.next   # 1. name every box you touch
        prev.next, b.next, a.next = b, a, after   # 2. STEP: every box has a name, so any order works
        prev = a                                  # 3. move last: a is now the box before the next pair
    return dummy.next                             # RETURN


def remove_elements(head, val):
    dummy = ListNode(0, head)
    cur = dummy                                   # STATE: the last box we keep
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next              # STEP: delete, and stay: check the new cur.next
        else:
            cur = cur.next                        # keep it, then move on
    return dummy.next                             # RETURN


print(to_list(swap_pairs(build_list([1, 2, 3, 4, 5]))))           # [2, 1, 4, 3, 5]
print(to_list(remove_elements(build_list([1, 2, 6, 3, 6, 6]), 6)))  # [1, 2, 3]
```

**Try it**
- Write the arrows in another order, `a.next, prev.next, b.next = after, b, a`: still `[2, 1, 4, 3, 5]`. With every box named, the order of the writes doesn't matter.
- Now leave `after` unnamed: name only `a, b`, and write `prev.next = b`, then `b.next = a`, then `a.next = b.next` on three lines. First add a step guard (`steps = 0` before the loop; `steps += 1` and `if steps > 20: break` inside), because the loop never ends: on `[1, 2, 3, 4]`, `to_list(swap_pairs(...), 6)` shows `[2, 1, 1, 1, 1, 1]`. `b.next = a` erased the only arrow to 3, so `a.next = b.next` made `a` point at itself.
- In `remove_elements`, move the finger after every step (replace the `if/else` with the delete under an `if`, then an unconditional `cur = cur.next`): removing 2 from `[1, 2, 2, 3]` gives `[1, 2, 3]`, and removing 6 from `[6, 6, 1]` gives `[6, 1]`. The second copy was never checked.
- Remove every value from `[7, 7, 7]`: `[]`. The dummy is the only box left, which is why the loop watches `cur.next` and not `cur`.

**Recursive reversal.** Interviewers sometimes ask for it. Trust the recursion: it reverses everything after `head` and returns the new head (the old last box). At that moment `head` still points at its old next box, which is now the *tail* of the reversed part, so hang `head` behind it:

```text
call on 1:  1 -> 2 -> 3 -> 4      the call on 2 returns 4:  1 -> 2 <- 3 <- 4  (2 is the TAIL)
head.next.next = head             2 points back at 1: 1 <-> 2, a 2-box loop for a moment
head.next = None                  None <- 1 <- 2 <- 3 <- 4, and return 4
```

```python
def reverse_recursive(head):
    if head is None or head.next is None:    # 0 or 1 box: already reversed
        return head
    new_head = reverse_recursive(head.next)  # trust it: everything after head is reversed
    head.next.next = head                    # my old next box is now the tail: hang me after it
    head.next = None                         # I am the new tail
    return new_head                          # the old last box, handed up unchanged


print(to_list(reverse_recursive(build_list([1, 2, 3, 4]))))   # [4, 3, 2, 1]
```

**Try it**
- Print `head.val, new_head.val` just before `return new_head`: you see `3 4`, `2 4`, `1 4`. The same box travels up through every level; only the arrows around `head` change.
- Delete `head.next = None` and rerun: the printed list becomes `[4, 3, 2, 1, 2, 1, 2, 1, ...]` and only stops at `to_list`'s limit. Boxes 1 and 2 now point at each other: a cycle.
- Try `reverse_recursive(build_list(range(10_000)))`: `RecursionError` (Python allows about 1000 nested calls by default). `reverse_list` handles the same list without trouble: prefer the loop unless recursion is asked for.

### Watch it work

The reversal keeps two chains: the reversed part (drawn with arrows pointing left, `prev` is its rightmost box) and the untouched rest (starting at `cur`). Each step moves one box from the right chain to the left one.

```python
def trace_reverse(values):
    prev, cur = None, build_list(values)

    def show(step):
        done = " <- ".join(["None"] + [str(v) for v in reversed(to_list(prev))])
        rest = " -> ".join([str(v) for v in to_list(cur)] + ["None"])
        print(f"step {step}:  {done:<26}|  {rest}")

    show(0)
    step = 0
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
        step += 1
        show(step)


trace_reverse([1, 2, 3, 4])
```

**Try it**
- Run `trace_reverse([7])` and `trace_reverse([])`: one step for one box, and for the empty list only the start line (`prev` stays `None`, which is the right answer).
- On every line the two chains together hold all n boxes, with no box in both. That is the invariant: nothing is ever lost, it only changes sides.
- Change the loop to `while cur.next:` and run `trace_reverse([1, 2, 3])`: the last line still shows `3 -> None` on the right. The last box is never flipped, so you would return `2 -> 1` and lose the 3.

### Where it goes wrong

1. **Losing the rest of the list.** Writing an arrow before naming the box it pointed to: `cur.next = prev` before `nxt = cur.next` turns `[1, 2, 3]` into `[1]`. Fix: name every box the step touches, then rewire, then move.
2. **Returning the old head.** After a reversal `head` is the *tail*: returning it gives `[1]` for `[1, 2, 3]`. Return `prev` (reversal) or `dummy.next` (anything built behind a dummy).
3. **The head without a dummy.** Without the dummy (and without a special case), `remove_nth_from_end` on `[1]` with n = 1 runs `fast` off the end and hits `None.next` (`AttributeError`). A dummy gives every box a box before it; then return `dummy.next`.
4. **Off-by-one fingers.** A loop that only checks `fast.next` crashes on `[1, 2, 3, 4]` (guard with `while fast and fast.next:`); a gap of n instead of n + 1 deletes the wrong box (`[1, 2, 3, 4, 5], 2` → `[1, 2, 3, 4]`).
5. **Values instead of boxes.** Two different boxes can hold the same value. Meeting points and intersections compare boxes: `a is b`, never `a.val == b.val`.
6. **Forgetting to cut.** When you split a list (reorder, merge sort, partition), end the first part with `None`. Reorder `[1, 2, 3, 4]` without the cut and box 3 points at itself: `[1, 4, 2, 3, 3, 3, ...]`. Partition `[2, 1]` around 2 into two dummy chains without `big_tail.next = None`: `[1, 2, 1, 2, ...]`. Palindrome gets away without a cut only because it stops when the reversed half ends.
7. **Advancing after a delete.** After `cur.next = cur.next.next`, nobody has checked the new `cur.next`: move `cur` only when you did not delete. With an unconditional `cur = cur.next`, removing 2 from `[1, 2, 2, 3]` gives `[1, 2, 3]`.
8. **One-line multiple assignment.** Python evaluates the right side first, then assigns the targets left to right. `cur, cur.next, prev = cur.next, prev, cur` sets the `next` of the *new* `cur` and crashes on `[1, 2, 3]` (`AttributeError`); `cur.next, prev, cur = prev, cur, cur.next` works. If unsure, one assignment per line.
9. **Comparing before moving in Floyd.** `slow` and `fast` both start on the head, so `slow is fast` is true before the first step. Move first, then compare.

### Edge cases to say out loud

Empty list (`None`) · one box · two boxes (even length for fast/slow) · remove the head (n = length) · remove the last box (n = 1) · lists of different lengths · duplicate values (compare boxes, not values) · a cycle through the head, or a box pointing at itself.

```python
assert to_list(reverse_list(None)) == [] and to_list(reverse_list(build_list([7]))) == [7]
assert to_list(reverse_recursive(build_list([1, 2]))) == [2, 1]
assert to_list(merge_lists(None, build_list([0]))) == [0]
assert to_list(merge_lists(build_list([5]), build_list([1, 2, 3]))) == [1, 2, 3, 5]
assert middle_node(build_list([1])).val == 1
assert middle_node(build_list([1, 2])).val == 2                        # second middle
assert to_list(remove_nth_from_end(build_list([1]), 1)) == []          # the only box
assert to_list(remove_nth_from_end(build_list([1, 2]), 2)) == [2]      # the head
assert to_list(remove_nth_from_end(build_list([1, 2]), 1)) == [1]      # the last box
assert to_list(swap_pairs(None)) == [] and to_list(swap_pairs(build_list([1]))) == [1]
assert to_list(remove_elements(build_list([6, 6, 1]), 6)) == [1]       # a run at the head
print("edge cases pass")
```

**Try it**
- Predict, then add: `assert middle_node(None) is None` (the `while` never runs, so `slow` is still `None`).
- What does `remove_nth_from_end(build_list([1, 2, 3]), 3)` return? Write the assert first: `[2, 3]`. When n equals the length you remove the head, the case the dummy exists for.
- Change `<=` to `<` in `merge_lists` and rerun: every assert still passes. On ties it only changes *which* of two equal boxes goes first (keeping `<=` keeps the merge stable).

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Several arrows in one step** | name every box, rewire in any order, move the finger last | 24 |
| **Delete while walking** | move the finger only when nothing was deleted; for 82, drop the whole run of duplicates and keep `prev` where it is | 203, 82 |
| **Cycle: is there one, where does it start?** | fast/slow race; after they meet, restart one finger at the head and step both by 1 | 141, 142 |
| **Floyd on an array** | the "next" of index `i` is `nums[i]`; the duplicate value is the cycle entrance | 287 |
| **Fold in half** | middle → cut → reverse the back half → walk both halves together | 234, 143 |
| **Merge sort** | middle (fingers start on a dummy) → cut → sort both halves → merge | 148 |
| **Reverse a block** | reverse with `prev` starting at the box *after* the block, hook the box before it to the new head; in a loop with a look-ahead for k-groups | 92, 25 |
| **Two chains, then join** | one dummy per chain, append each box to its chain, join them and cut the last tail | 86, 328 |
| **Rotate** | count n, close the list into a ring, cut after box n − k % n | 61 |
| **Two lists in lockstep** | one finger per list, step together (merge, add with a carry, line up two tails) | 21, 2, 160 |
| **Copy with extra arrows** | dict old box → new box, then wire `next` and `random` through it | 138 |
| **Recency order with O(1) moves** | dict + doubly linked list with two sentinels ([Design](#s24)) | 146 |

**Cycles (141, 142).** Inside a loop, `fast` gains exactly one box per step on `slow`, so the gap shrinks by one each step and must reach zero: they meet, and `fast` can't jump over `slow` (a speed-3 finger chasing a speed-1 finger round a 4-box loop from 1 apart sees the gap go 1, 3, 1, 3, ... forever). Without a loop, `fast` falls off the end. Phase 2 finds the entrance because **whole laps don't move you**:

```text
 head ------ a boxes ------> E ------ b boxes ------> M        E = entrance, M = where they met
                             ^                        |        c = boxes around the loop
                             +----- c - b boxes ------+

 when they meet, slow has walked a + b and fast 2(a + b); fast's extra a + b steps were whole
 laps, so a + b = k*c. Walk slow a more steps: it has walked a + k*c in total, which ends where
 a steps end, on E. A finger restarted at the head also reaches E after exactly a steps.
```

**Floyd on an array (287):** read index `i` as a box whose arrow points to index `nums[i]`. Values are in `[1, n]`, so no arrow enters index 0: the walk from 0 can never come back to 0, so it must run into a loop. The box where it enters has two incoming arrows, one from the tail and one from the loop's last box. Two arrows into box v means v is stored twice, so the entrance is the duplicate.

```text
 nums  = [1, 3, 4, 2, 2]
 index:   0  1  2  3  4

 0 -> 1 -> 3 -> 2 -> 4           boxes 3 and 4 both point at 2: two arrows enter 2,
                ^    |           so 2 is the duplicate AND the entrance of the loop
                +----+
```

```python
def build_cycle(values, pos):                # the last box links back to index pos (-1: no cycle)
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:                # phase 1: race
        slow, fast = slow.next, fast.next.next
        if slow is fast:                     # met inside the loop (compare boxes, not values)
            break
    if fast is None or fast.next is None:    # the race ended because fast fell off: no cycle
        return None
    finger = head                            # phase 2: from the head and from the meeting point
    while finger is not slow:
        finger, slow = finger.next, slow.next
    return finger                            # the entrance


def find_duplicate(nums):                    # index i points to index nums[i]
    slow = fast = 0                          # 0 is never a target: it starts the tail
    while True:
        slow, fast = nums[slow], nums[nums[fast]]
        if slow == fast:                     # indices, so == is "same box" here
            break
    finger = 0
    while finger != slow:
        finger, slow = nums[finger], nums[slow]
    return finger                            # the box with two incoming arrows


print(detect_cycle(build_cycle([3, 2, 0, -4], 1)).val, detect_cycle(build_cycle([1, 2], -1)))   # 2 None
print(find_duplicate([1, 3, 4, 2, 2]), find_duplicate([3, 1, 3, 4, 2]))                          # 2 3
assert detect_cycle(build_cycle([1], 0)).val == 1                       # a box pointing at itself
assert detect_cycle(build_cycle([1, 2], 0)).val == 1                    # a loop through the head
```

**Try it**
- Return `slow` right after phase 1 (skip phase 2) and rerun the first example: you get `-4`, the box where the race happened to end, not the entrance `2`.
- Check the arithmetic on a bigger rho: in `build_cycle(list(range(10)), 3)` the tail has a = 3 boxes and the loop c = 7. Print `slow.val` after phase 1: `7`, so b = 4 and a + b = 7 is exactly one lap.
- Compare before moving: put the `if slow is fast: break` lines *above* the step line in phase 1. The cell now prints `3` and a `ListNode` instead of `2 None`: the fingers "meet" on the head before taking a single step.
- Predict `find_duplicate([2, 5, 9, 6, 9, 3, 8, 9, 7, 1])` before running (9: it appears three times, so three arrows enter box 9).

**Fold in half (234, 143) and merge sort (148).** Palindrome and Reorder both need "the back half, walked backwards"; you can't walk backwards, but you can *make* the back half run backwards by reversing it in place. Sort List needs two halves to sort and merge. All three start by finding the middle, and the only decision is which middle:

| Fingers start on | Guard | `slow` on `[1, 2, 3, 4]` | `slow` on `[1, 2, 3, 4, 5]` | Use when |
|---|---|---|---|---|
| `head` | `while fast and fast.next` | 3 | 3 | you need the back half's first box (palindrome) |
| a dummy before `head` | `while fast and fast.next` | 2 | 3 | you need the box *before* the back half, to cut it off (reorder, sort) |

Need the box before? Start on the dummy, the same rule as n-th from the end.

```text
 1 -> 2 -> 3 -> 4 -> 5         slow stops on 3, the last box of the first half
 1 -> 2 -> 3     5 -> 4        cut after 3 and reverse the back half
 1 -> 5 -> 2 -> 4 -> 3         zip: one box from the left half, one from the right
```

```python
def reorder_list(head):                      # L0 -> Ln -> L1 -> Ln-1 -> ...  in place
    slow = fast = ListNode(0, head)          # start on a dummy: slow ends BEFORE the back half
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None                         # cut: the halves must not touch
    second = reverse_list(second)            # the back half, now running backwards
    first = head
    while second:                            # the first half is as long or one longer
        n1, n2 = first.next, second.next     # name both rests before rewiring
        first.next, second.next = second, n1
        first, second = n1, n2


def is_palindrome_list(head):
    second = reverse_list(middle_node(head)) # back half reversed (it includes the middle if odd)
    first = head
    while second:                            # the reversed half is never the longer one
        if first.val != second.val:
            return False
        first, second = first.next, second.next
    return True


def sort_list(head):                         # merge sort: middle, cut, sort both halves, merge
    if head is None or head.next is None:
        return head
    slow = fast = ListNode(0, head)          # start on a dummy: slow stops BEFORE the back half
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None                         # cut
    return merge_lists(sort_list(head), sort_list(second))


h = build_list([1, 2, 3, 4, 5]); reorder_list(h); print(to_list(h))      # [1, 5, 2, 4, 3]
h = build_list([1, 2, 3, 4]); reorder_list(h); print(to_list(h))         # [1, 4, 2, 3]
print(is_palindrome_list(build_list([1, 2, 2, 1])), is_palindrome_list(build_list([1, 2])))   # True False
print(to_list(sort_list(build_list([4, 2, 1, 3]))), to_list(sort_list(build_list([-1, 5, 3, 4, 0]))))   # [1, 2, 3, 4] [-1, 0, 3, 4, 5]
```

**Try it**
- Delete the cut `slow.next = None` in `reorder_list` and rerun: both reordered lists now run on until `to_list`'s limit. `to_list(h, 8)` shows `[1, 4, 2, 3, 3, 3, 3, 3]`: box 3 points at itself.
- Split `first.next, second.next = second, n1` into two lines: either order still gives `[1, 5, 2, 4, 3]`, because `n1` and `n2` already name every box. Then drop `n2` and advance with `second = second.next` *after* the rewire: `[1, 5, 2, 3]`. The 4 is lost, because `second.next` was rewired before you read it.
- In `sort_list`, start the fingers on `head` instead of a dummy: `sort_list(build_list([2, 1]))` raises `RecursionError`. `slow` stops on the second box, so the back half is empty and the front half is the whole list again, forever.
- Run `h = build_list([1, 2, 3, 2, 1]); print(is_palindrome_list(h), to_list(h))`: `True [1, 2, 3]`. The check rewired the input; reverse the back half again if the caller needs the list intact.

**Reverse one block (92), then every block (25).** Reversing positions `left..right` is the plain reversal with two extra fingers: `before`, the box before the block, and `after`, the first box after it. Start the reversal with `prev = after`, so the block's new tail already points onward; then hook `before` to the block's new head. Reverse Nodes in k-Group is the same block reversal in a loop, with a look-ahead that stops when fewer than k boxes are left.

```text
 left = 2, right = 4:   D -> 1 -> 2 -> 3 -> 4 -> 5          before = 1, after = 5
                        D -> 1    4 -> 3 -> 2 -> 5          reversed with prev starting at 5
                        D -> 1 -> 4 -> 3 -> 2 -> 5          before.next = 4: hooked in
```

```python
def reverse_block(before, after):            # reverse the boxes strictly between before and after
    prev, cur = after, before.next           # prev = after: the block's new tail points on
    while cur is not after:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    first = before.next                      # the old first box is now the block's tail
    before.next = prev                       # hook the block's new head in
    return first


def reverse_between(head, left, right):      # 92: reverse positions left..right (1-based)
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next                 # the box before the block
    after = before.next
    for _ in range(right - left + 1):
        after = after.next                   # the first box after the block
    reverse_block(before, after)
    return dummy.next


def reverse_k_group(head, k):                # 25: the same block reversal, in a loop
    dummy = ListNode(0, head)
    before = dummy
    while True:
        last = before                        # look ahead: are there k more boxes?
        for _ in range(k):
            last = last.next
            if last is None:
                return dummy.next            # fewer than k left: they stay as they are
        before = reverse_block(before, last.next)   # the block's tail is the next "before"


print(to_list(reverse_between(build_list([1, 2, 3, 4, 5]), 2, 4)))   # [1, 4, 3, 2, 5]
print(to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 2)))      # [2, 1, 4, 3, 5]
print(to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 3)))      # [3, 2, 1, 4, 5]
```

**Try it**
- In `reverse_block`, start with `prev = None` instead of `after`: the 92 example prints `[1, 4, 3, 2]`. Box 2 now points at `None`, so the 5 is cut off.
- `reverse_between(build_list([1, 2, 3]), 1, 3)` reverses everything: `before` is the dummy, so position 1 needs no special case.
- Predict before running: k = 1 returns the list unchanged, k = 5 reverses all of it, k = 6 changes nothing (there is no full block).
- Print `to_list(dummy.next)` right after the `before = reverse_block(...)` line: for k = 2 you see `[2, 1, 3, 4, 5]` and then `[2, 1, 4, 3, 5]`, one finished block per line.

**Two lists in lockstep (2, 160).** One finger per list, moving together. Add Two Numbers is schoolbook addition: the lists store the ones digit first, so walk both, write `total % 10`, carry `total // 10`. Intersection lines up the two tails: after the merge box both lists are the *same* boxes, so once each finger is the same distance from the end, they reach the merge box at the same moment. Count the lengths and skip the longer list's extra prefix, or (below) let each finger walk its own list and then the other one: both then walk A's own part + B's own part + the shared tail. (LCA with parent pointers, 1650, is this same problem: walk up from p and from q, and the two upward paths merge at the LCA.)

```text
 A:      4 -> 1 \                 pa walks 4 1 8 4 5, then B's own part 5 6 1   (8 boxes)
                 8 -> 4 -> 5      pb walks 5 6 1 8 4 5, then A's own part 4 1   (8 boxes)
 B: 5 -> 6 -> 1 /                 so the next step puts both on the shared 8
```

```python
def add_two_numbers(l1, l2):                 # ones digit first: 342 is stored as 2 -> 4 -> 3
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:                 # a leftover carry still makes a box
        total = carry
        if l1:
            total, l1 = total + l1.val, l1.next
        if l2:
            total, l2 = total + l2.val, l2.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)          # RECORD: one new box per column
        tail = tail.next
    return dummy.next


def intersection_node(a, b):
    pa, pb = a, b                            # each finger walks its own list, then the other
    while pa is not pb:                      # boxes, not values
        pa = pa.next if pa else b            # fell off A: continue at the head of B
        pb = pb.next if pb else a
    return pa                                # the shared box, or None (both fell off together)


print(to_list(add_two_numbers(build_list([2, 4, 3]), build_list([5, 6, 4]))))   # [7, 0, 8]  (342 + 465 = 807)
print(to_list(add_two_numbers(build_list([9, 9]), build_list([1]))))             # [0, 0, 1]  (99 + 1 = 100)
shared = build_list([8, 4, 5])
a, b = ListNode(4, ListNode(1, shared)), ListNode(5, ListNode(6, ListNode(1, shared)))
print(intersection_node(a, b).val, intersection_node(build_list([1]), build_list([1])))   # 8 None
```

**Try it**
- Change `while l1 or l2 or carry:` to `while l1 or l2:` and rerun 99 + 1: `[0, 0]`. The final carry never got its box.
- In `intersection_node`, compare values (`while pa.val != pb.val:`) and rerun: `AttributeError` as soon as `pa` falls off A (`None.val`). With `is`, `None` is a legal place to stop, and two boxes that merely hold equal values (the two 1s) never count as the same box.
- Print `pa.val if pa else None, pb.val if pb else None` at the top of the loop, then call `intersection_node(a, b)`: nine lines, ending with `1 1` (two different boxes holding equal values); the next step puts both fingers on the shared 8.
- The counting version lines up the same way: measure both lengths, move the longer list's finger ahead by the difference, then step both until `a is b`. Write it and check that it also gives 8.

**Copy a list with random arrows (138).** A deep copy needs a translator from "a box of the old list" to "its copy". Pass 1 creates a copy of every box and stores the pair in a dict; pass 2 wires each copy's `next` and `random` through that dict. (The O(1)-space version weaves each copy right after its original, `A -> A' -> B -> B'`, so "the copy of X" is simply `X.next`; then it unweaves the two lists.)

```python
class RandomNode:
    def __init__(self, val, next=None, random=None):
        self.val, self.next, self.random = val, next, random


def copy_random_list(head):
    old_to_new = {None: None}                # "points at nothing" translates to nothing
    node = head
    while node:                              # pass 1: one new box per old box
        old_to_new[node] = RandomNode(node.val)
        node = node.next
    node = head
    while node:                              # pass 2: wire the copies through the dict
        old_to_new[node].next = old_to_new[node.next]
        old_to_new[node].random = old_to_new[node.random]
        node = node.next
    return old_to_new[head]


def build_random(pairs):                     # [(val, index the random arrow points to), ...]
    nodes = [RandomNode(v) for v, _ in pairs]
    for i, (_, r) in enumerate(pairs):
        nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
        nodes[i].random = nodes[r] if r is not None else None
    return nodes[0] if nodes else None


def describe(head):                          # [(val, index of the random target), ...]
    boxes = []
    while head:
        boxes.append(head)
        head = head.next
    return [(n.val, None if n.random is None else boxes.index(n.random)) for n in boxes]


orig = build_random([(7, None), (13, 0), (11, 4), (10, 2), (1, 0)])
clone = copy_random_list(orig)
print(describe(clone))                       # [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)]
print(clone is orig, clone.next.random is orig, clone.next.random is clone)   # False False True
```

**Try it**
- Remove the `None: None` entry and rerun: `KeyError: None`, from the first box whose `random` points at nothing.
- In pass 2, write `old_to_new[node].random = node.random` (no translation): `describe(clone)` now fails with `ValueError`, because the copy's random arrows point into the *old* list. A deep copy must never point outside itself.
- In pass 1, store the old box itself (`old_to_new[node] = node`): `describe` looks perfect, but `clone is orig` prints `True`. That is a shallow copy, exactly what the problem forbids.

### Say it in the interview

> "Copying into an array costs O(n) extra space, so I'll rewire the nodes in place. A dummy before the head makes the head an ordinary node. In each step I first name every node I'm about to touch, then change the arrows, then move my pointers. Invariant: everything before `cur` is finished and hangs off the dummy; everything from `cur` on is untouched. One pass: O(n) time, O(1) space. Let me check `[]`, `[1]` and `[1, 2]` by hand."

While coding, point at the naming line ("so I don't lose the rest"), at `return dummy.next` ("the head may have changed"), and for fast/slow say the loop guard out loud ("fast can take two more steps"). Be ready for the follow-ups:

- *Recursive version?* The same rewiring with the call stack as the memory: O(n) stack, and Python stops at about 1000 boxes.
- *Must the input stay intact (palindrome)?* Reverse the back half again before returning.
- *Floyd: why do the fingers meet, and why does phase 2 find the entrance?* The gap closes by exactly one per step, so it can't be skipped; whole laps don't move you, so a steps from the meeting point land where a steps from the head land.
- *Remove the n-th from the end in one pass?* A gap of n + 1 between two fingers that start on the dummy.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Add Two Numbers | `linked_list/add_two_numbers.py` | ones digit first, so add column by column with a carry; loop while either list or the carry remains |
| Copy List with Random Pointer | `linked_list/copy_list_with_random_pointer.py` | dict old box → new box (or weave copies after originals), then wire `next`/`random` through it |
| Find the Duplicate Number | `linked_list/find_the_duplicate_number.py` | read `i → nums[i]` as a list from index 0; the duplicate has two incoming arrows = the cycle entrance (Floyd) |
| Intersection of Two Linked Lists | `linked_list/intersection_of_two_linked_lists.py` | skip the longer list's extra prefix, then walk both until `a is b` |
| Linked List Cycle | `linked_list/linked_list_cycle.py` | fast gains one box per step on slow inside a loop; meeting = cycle, falling off = none |
| Linked List Cycle II | `linked_list/linked_list_cycle_ii.py` · `practice/simple/23_linked_list_cycle_ii.py` | whole laps don't move you: after the meeting, a finger from the head and one from the meeting point meet at the entrance |
| Merge Two Sorted Lists | `linked_list/merge_two_sorted_lists.py` · `practice/simple/22_merge_two_sorted_lists.py` | dummy + tail: always hang the smaller front box; attach the leftover whole |
| Palindrome Linked List | `linked_list/palindrome_linked_list.py` | find the middle, reverse the back half in place, compare the halves |
| Remove Nth Node From End of List | `linked_list/remove_nth_from_end.py` · `practice/simple/25_remove_nth_node_from_end.py` | gap of n + 1 from a dummy: when fast falls off, slow is just before the victim |
| Reorder List | `linked_list/reorder_list.py` | middle (start on a dummy), cut, reverse the back half, zip the two halves |
| Reverse Linked List | `linked_list/reverse_linked_list.py` · `practice/simple/21_reverse_linked_list.py` | name next, flip the arrow, move both fingers; `prev` ends as the new head |
| Reverse Nodes in k-Group | `linked_list/reverse_nodes_in_k_group.py` | look ahead k boxes; reverse with `prev` = the box after the block; hook the box before it to the new head |

### Self-check

1. In Linked List Cycle II, why does a finger restarted at the head meet the other finger exactly at the entrance?
<details><summary>Answer</summary>With a tail of a boxes, a loop of c boxes and a meeting point b boxes into the loop, slow walked a + b and fast 2(a + b). Fast's extra a + b steps were whole laps, so a + b = k·c. Walking a more steps from the meeting point brings slow to a + k·c steps in total, which ends where a steps end: the entrance, where the finger from the head also arrives after a steps.</details>

2. In Remove Linked List Elements, why doesn't `cur` move after a delete?
<details><summary>Answer</summary>The delete pulls a new box into <code>cur.next</code>, and nobody has checked it yet. Moving on would skip it, so a run of equal values (<code>[1, 2, 2, 3]</code>, remove 2) keeps one copy. Move only when you keep the box.</details>

3. In Find the Duplicate Number, why can index 0 never be inside the cycle, and why is the cycle's entrance the duplicate?
<details><summary>Answer</summary>Every value is in [1, n], so no arrow points at index 0: the walk leaves it and never returns, so it is the start of the tail. The entrance is the one box with two incoming arrows (one from the tail, one from inside the loop), and two arrows into box v means two indices hold the value v.</details>
