## Stacks & Queues

> A **stack** is a pile of unfinished business: whatever you opened last must be finished first, so it sits on top (LIFO). A **queue** is a line: whoever arrived first is served, or expires, first (FIFO). To pick one, ask a single question: *in what order do my pending items get finished?*

**Reach for it when** you see nesting or matching: brackets, `k[...]`, the parentheses of an expression. The same goes for "the most recent unmatched thing", for going back with `..` in a path or with undo, for evaluating an expression, and for a newcomer that only ever meets the nearest survivor, as in a collision. All of those are a **stack**.

When items are handled in arrival order, because the oldest expires first, players take turns or a buffer has a fixed size, that is a **queue**, written with `collections.deque`. The most common queue of all is BFS: "nearest first", "fewest steps" or "level by level" means the frontier is a deque, and that one lives in [Graphs I](#s17).

**In this repo:** `stack/` (10 of its 16 problems; the "next greater" family is in [Monotonic Stack](#s08)) · `queues/` (6 problems) · bank: `practice/simple/13_valid_parentheses.py`, `practice/simple/14_min_stack.py`, `practice/simple/15_evaluate_reverse_polish_notation.py` · basics in `practice/simple/basics/stacks/`: `01_array_stack_and_queue_via_two_stacks.py`, `02_simplify_unix_path.py`, `03_decode_string.py`, `04_basic_calculator_ii.py`, `05_asteroid_collision.py`

### The picture

```text
s = { [ ( ) ] ( }                        the stack after each character (top on the right)

    {   opener: push                     {
    [   opener: push                     { [
    (   opener: push                     { [ (
    )   top is ( : a match, pop          { [
    ]   top is [ : a match, pop          {
    (   opener: push                     { (
    }   top is ( but } needs {           invalid: the innermost open bracket is (
```

```text
stack (LIFO):  [ a  b  c  d ]  <- push and pop here, at the top (d is the most recent)
queue (FIFO):  append -> [ e  d  c  b  a ] -> popleft         (a is the oldest, it leaves first)
```

**Why it is fast:** the brute force for nesting finds an innermost pair like `()`, deletes it, and rescans from the start: O(n²). A stack holds exactly the unfinished items in the order they were opened, so each character is pushed once and popped at most once: O(n).

Queues have the same story. `list.pop(0)` shifts every remaining item, O(n) per call. A `deque` moves nothing, and a ring buffer moves an index instead of the data, so with either one an item leaves the line in O(1).

**Why it is correct:** brackets nest, so a bracket opened later must be closed earlier. The next closer can therefore only match the innermost open bracket, which is the most recent one: the top. A closer that does not match the top can never be matched by anything later, so failing at once is safe.

### From idea to code

**The idea in one sentence:** *walk the input once; push whatever is still unfinished; when an item finishes something, the thing it finishes is on top, so pop it and combine.*

The seven decisions, for a stack first. The **State** is a Python list used as a stack of *unfinished* items, and its **Definition** goes in a comment: `stack = openers not closed yet, innermost on top`. The **Invariant** is that after reading `s[:i]` the stack holds exactly the unfinished items of that prefix, most recent on top. A **Step** pushes an opener or a value; a closer or an operator pops what it finishes, combines, and pushes the result when there is one.

The **Fix** is a `while` loop, needed only when one newcomer can finish several items in a row, as in a collision or a run that vanishes: pop while the newcomer beats the top. **Record** at the pop whenever the pop measures something: the length of a well-formed run in Longest Valid Parentheses, a distance or an area in [Monotonic Stack](#s08). Otherwise the answer is what is left at the end, and an early `return False` records a failure the moment it is certain.

**Init** is `stack = []` and `num = 0`, sometimes with a sentinel: a `-1` barrier under the indices, a trailing `"+"` on the input. **Return** `not stack` for matching, the single value left for evaluation, and the stack itself when the survivors are the answer.

A queue makes the same decisions with the ends swapped. The state is a `deque` in arrival order, defined as `q = pings in [t - 3000, t], oldest at the front`, and the invariant is that it holds exactly the live items. A step appends the new item at the back, the fix pops the front while it has expired, and the record, after the fix, is `len(q)` or the front. Init is `q = deque()`; the return is the size or the front per call, or whoever is left at the end.

One more decision hides inside the state: what goes in one stack entry. The answer is exactly what you will need at the moment it is popped. It is the easiest decision to skip, and the one that makes the rest of the code obvious.

Valid Parentheses (20), which asks whether brackets are properly nested, pushes the opener itself, because the closer must match its type. Evaluate Reverse Polish Notation (150), which evaluates a postfix expression, pushes values, because an operator combines the two newest. Basic Calculator II (227), which evaluates `"3+2*2"` with the usual precedence, pushes signed terms: `+` and `-` wait for the final sum, while `*` and `/` edit the top. Decode String (394), which expands `3[a]` into `aaa`, parks a pair, the text before `[` and the count, because `]` glues prefix + inner × count.

Longest Valid Parentheses (32), which wants the longest well-formed stretch of `(` and `)`, pushes an index on top of a `-1` barrier, because a length is `i - stack[-1]`. Asteroid Collision (735), where the smaller of two colliding asteroids explodes, pushes a survivor, because the newcomer fights the nearest survivor. Min Stack (155), a stack that also answers `getMin` in O(1), pushes the value together with the minimum at or below it, because after a pop the minimum must already be known.

Remove All Adjacent Duplicates in String II (1209), which deletes every run of k equal letters, pushes `[char, run length]`, because a run can grow again after the run above it vanishes. Simplify Path (71), which cleans up a Unix path, pushes a directory name, because `..` undoes the most recent one. If you cannot say what you will need at the pop, solve two pops by hand first.

Two stack templates come first, one that pops to *match* and one that pops to *combine*. Valid Parentheses asks whether a string of `()[]{}` is properly nested: `"{[()]}"` is, `"([)]"` is not. Walk the string. An opener is unfinished business, `stack.append(ch)`. A closer must finish the most recent opener, `stack[-1]`, which you may read only after checking that the stack is not empty; `stack.pop()` finishes it. At the end, `return not stack` asks whether anything is still open.

Evaluate Reverse Polish Notation asks for the value of a postfix expression: `["2", "1", "+", "3", "*"]` is `(2 + 1) * 3 = 9`. Numbers wait on the stack, and an operator combines the two newest, with the right operand coming off first: `b = stack.pop()`, then `a = stack.pop()`, then `a - b`. Order matters in both templates. `is_valid` looks at the top *before* it pops, because the check decides whether the pop is legal, and `eval_rpn` pops `b` before `a`, because the right operand was pushed last.

```python
def is_valid(s):
    partner = {")": "(", "]": "[", "}": "{"}     # closer -> its opener
    stack = []                               # STATE + INIT: openers not closed yet, innermost on top
    for ch in s:
        if ch not in partner:
            stack.append(ch)                 # STEP (opener): one more unfinished bracket
        elif not stack or stack[-1] != partner[ch]:
            return False                     # RECORD: the answer is known now: invalid
        else:
            stack.pop()                      # STEP (closer): it finishes the innermost opener
    return not stack                         # RETURN: valid iff nothing was left open


OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
       "*": lambda a, b: a * b, "/": lambda a, b: int(a / b)}   # int(a / b) truncates toward 0


def eval_rpn(tokens):
    stack = []                               # STATE + INIT: values waiting for an operator
    for tok in tokens:
        if tok in OPS:
            b = stack.pop()                  # the RIGHT operand was pushed last
            a = stack.pop()
            stack.append(OPS[tok](a, b))     # STEP (operator): two waiting values become one
        else:
            stack.append(int(tok))           # STEP (number): it waits; "-3" is a number too
    return stack[-1]                         # RETURN: exactly one value is left


print(is_valid("{[()]}"), is_valid("([)]"), is_valid("(("))                        # True False False
print(eval_rpn(["2", "1", "+", "3", "*"]), eval_rpn(["4", "13", "5", "/", "+"]))   # 9 6
```

**Try it**
- Delete `not stack or` from the `elif` and run `is_valid("]")`: `IndexError`, because the code peeks at the top of an empty stack.
- Replace `return not stack` with `return True` and run `is_valid("((")`: it says `True`, although nothing was ever closed.
- Swap the two pops (pop `a` first) and run `eval_rpn(["6", "3", "-"])`: you get -3 instead of 3, because the operands come off the stack in reverse order.
- Change `int(a / b)` to `a // b` in `OPS` and run `eval_rpn(["7", "-3", "/"])`: -3 instead of -2, because `//` floors and the problem truncates toward zero.

A queue template has the same shape, but items leave from the *other* end: "join the line" is `q.append(x)`, "leave the line" is `q.popleft()`, never `list.pop(0)`, and "the oldest item" is `q[0]`. When items expire in the order they arrived, only the front ever needs checking. The lines then run in the order STEP, FIX, RECORD: join, drop whatever has expired, and measure last, so that only live items are counted.

Number of Recent Calls (933) asks `ping(t)` to count the pings in `[t - 3000, t]`, and `t` only grows: pings at 1, 100, 3001 and 3002 answer 1, 2, 3 and 3, because by 3002 the ping at 1 has expired. Each ping joins at the back, the front leaves while it is older than `t - 3000`, and the answer is the length of what is left. Appending first also means the FIX loop can never empty the deque, because `t` itself never expires, so it needs no `self.q and` guard.

```python
class RecentCounter:                         # 933: how many pings in [t - 3000, t]?
    def __init__(self):
        self.q = deque()                     # STATE + INIT: live pings, oldest at the front

    def ping(self, t):                       # t only grows
        self.q.append(t)                     # STEP: the newest joins at the back
        while self.q[0] < t - 3000:          # FIX: drop expired pings (q never empties: t is in it)
            self.q.popleft()
        return len(self.q)                   # RECORD + RETURN: the window is the deque


counter = RecentCounter()
print([counter.ping(t) for t in [1, 100, 3001, 3002]])   # [1, 2, 3, 3]
```

**Try it**
- Change `<` to `<=` in the `while` and replay `[1, 100, 3001, 3002]`: the third answer becomes 2, because the ping at `t = 1` is exactly 3000 ms old and still belongs to `[1, 3001]`.
- Change the `while` to `if` and ping `[1, 2, 3, 5000]`: the last answer is 3 instead of 1, since only one expired ping can leave per call.
- Replace `3000` with `10` and predict `[1, 5, 11, 12, 30]` before running: `[1, 2, 3, 3, 1]`.

### Watch it work

The stack after every token of `["4", "13", "5", "/", "+"]`, which is `4 + 13 / 5` and evaluates to 6. Notice that `/` takes `13` and `5`, the two most recent values, and never touches the `4` underneath: that is why postfix needs no parentheses.

```python
def trace_rpn(tokens):
    stack = []
    for tok in tokens:
        note = ""
        if tok in OPS:
            b, a = stack.pop(), stack.pop()
            stack.append(OPS[tok](a, b))
            note = f"{a} {tok} {b} = {stack[-1]}"
        else:
            stack.append(int(tok))
        print(f"{tok:>3}   stack = {str(stack):<17} {note}".rstrip())


trace_rpn(["4", "13", "5", "/", "+"])
```

**Try it**
- Run `trace_rpn(["2", "1", "+", "3", "*"])` and predict the stack just before the `*` (it is `[3, 3]`).
- Trace `["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]`: the stack never holds more than 4 values, `6 / -132` truncates to 0, and the result is 22.
- Feed a broken expression, `trace_rpn(["1", "+"])`: the second `pop` raises `IndexError`. A defensive version checks `len(stack) >= 2` before popping.

### Where it goes wrong

1. **Peeking at an empty stack.** A closer with nothing open (`"]"`, `"())"`) makes `stack[-1]` raise `IndexError`. Check `not stack` first, in the same condition.
2. **Forgetting the leftovers.** `"(("` never fails inside the loop. The answer is `not stack`, not `True`.
3. **Counting instead of matching.** `"([)]"` has balanced counts but is invalid. A plain counter is enough only with a single bracket type, as in Minimum Add to Make Parentheses Valid (921), which asks for the fewest brackets to insert: then every stack entry is the same `(` and only the height matters.
4. **Operand order.** The first pop is the *right* operand: `["6", "3", "-"]` is `6 - 3 = 3`, not -3.
5. **Floor instead of truncate.** Python's `//` floors (`7 // -3 == -3`), but these problems truncate toward zero (`int(7 / -3) == -2`). It also bites calculators that store `-3` as a signed term: `"14-3/2"` must be 13, and `-3 // 2` would make it 12.
6. **The last number is never applied.** A calculator applies an operator when the *next* operator arrives, so the final number needs a flush: loop over `s + "+"`. Without the sentinel, `"3+2*2"` gives 5. Testing `i == len(s) - 1` also works, but only in an `if` of its own: chained as an `elif` after the digit test, `"42"` gives 0.
7. **`if` instead of `while` for collisions.** A left-mover can destroy several right-movers in a row: `[1, 2, -5]` must end as `[-5]`, not `[1, -5]`.
8. **`list.pop(0)` as a queue.** Each call shifts every remaining item, so n dequeues cost about n²/2 moves. Use `deque.popleft()`, or a ring buffer that moves `head` instead of the data.
9. **An expiry loop without `q and`.** It is safe in `ping` only because `t` was just appended. A read-only method has no such guarantee. Design Hit Counter (362) asks `getHits(t)` for the hits of the last 300 seconds; [From Idea to Code](#s01) has the base version and [Design Problems](#s24) the follow-up. Write `while q and q[0] <= t - 300`, or a call on an empty counter raises `IndexError`.

### Edge cases to say out loud

Empty input · a lone closer · only openers · the wrong type innermost (`"([)]"`) · a single RPN token · negative numbers (`"-3"` is a number, not an operator) · dividing a negative · multi-digit numbers · a ping exactly 3000 ms old (still counts). The cell checks each of them against the three templates above.

```python
assert is_valid("") is True
assert is_valid("]") is False                         # closer with nothing open
assert is_valid("((") is False                        # leftovers
assert is_valid("([)]") is False                      # counts match, order doesn't
assert eval_rpn(["5"]) == 5
assert eval_rpn(["7", "-3", "/"]) == -2               # "-3" is a number; truncate toward 0
assert eval_rpn(["6", "3", "-"]) == 3                 # a - b, with b popped first
assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
c = RecentCounter()
assert [c.ping(t) for t in [1, 3001, 3002]] == [1, 2, 2]   # t = 1 still counts at 3001
print("edge cases pass")
```

**Try it**
- Predict, then add: `assert is_valid("(]") is False` (the top is `(`, but `]` needs `[`).
- Write the assert for `eval_rpn(["3", "4", "-", "5", "*"])` before running it: `(3 - 4) * 5 = -5`.
- Swap the stack for one counter (+1 on an opener, −1 on a closer, fail below 0) and run `"([)]"`: it passes as valid. That is trap 3 in one line.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Match pairs** | push openers; a closer must equal the top | Valid Parentheses (20) |
| **Stack collapses to a counter** | one bracket type: keep only the height; a `)` at height 0 costs one insertion | Minimum Add to Make Parentheses Valid (921): the fewest brackets to insert |
| **Postfix evaluation** | numbers push; an operator pops two and pushes one | Evaluate Reverse Polish Notation (150) |
| **Precedence** | push signed terms; `*` and `/` edit the top term; the answer is `sum(stack)` | Basic Calculator II (227) |
| **Park and resume** | on an opener, push the current context and start fresh; on a closer, pop it and merge | Decode String (394) |
| **Mark, then rebuild** | a stack of indices of unmatched `(`; drop every marked character | Minimum Remove to Make Valid Parentheses (1249): delete the fewest brackets, in [Strings](#s20) |
| **Undo / go up** | names push, `..` pops (if anything is there), `.` and `""` do nothing | Simplify Path (71) |
| **Collisions** | the newcomer fights the top *while* they collide | Asteroid Collision (735) |
| **Stack of runs** | entry `[char, count]`; k in a row vanish, and the run below may grow again | Remove All Adjacent Duplicates in String II (1209) and I (1047): `"abbaca"` → `"ca"` |
| **Remember the minimum** | each entry stores `(value, min of everything at or below it)` | Min Stack (155) |
| **Queue from two stacks** | inbox takes pushes, outbox serves pops; refill only when the outbox is empty | Implement Queue using Stacks (232) |
| **Stack from one queue** | after each push, rotate the older items behind the new one (`len - 1` times) | Implement Stack using Queues (225): push, pop, top and empty from queue moves only |
| **Ring buffer** | fixed array + `head` + `count`; every index goes through `% k` | Design Circular Queue (622) and Design Circular Deque (641): a bounded queue in a fixed array |
| **Time window** | deque of times; pop the front while it is too old | Number of Recent Calls (933); Design Hit Counter (362) |
| **Round robin** | one queue per side; the earlier front acts and rejoins as `index + n` | Dota2 Senate (649): which party wins a ban war |
| *Second pass:* **Index stack with a barrier** | push indices, seeded with `-1`; after a match the valid run is `i - stack[-1]` | Longest Valid Parentheses (32) |
| *Second pass:* **Collapse at the closer** | push everything; at `)` pop the group's operands, then its operator, and push one result | Parsing a Boolean Expression (1106): evaluate and/or/not groups over `t` and `f` |
| *Second pass:* **Park and resume, with arithmetic** | at `(` park the terms so far and the pending operator; at `)` the group becomes one number | Basic Calculator (224) and Basic Calculator III (772): expressions with parentheses |

The code below covers the five shapes that come up most: precedence, park and resume, collisions and undo, entries that remember, and a queue from two stacks. The ring buffer and the round robin need only their idea.

A ring buffer, as in Design Circular Queue (622), moves a label instead of the data: the items are the `count` slots that start at `head` in a fixed array of k, and every index goes through `% k`. Design Circular Deque (641) adds the front end by stepping `head` back, `(head - 1) % k`, before it writes, and self-check 4 shows why `count` is kept.

The round robin of Dota2 Senate (649) gives each party a queue of turn indices. The earlier front bans the other front and rejoins its own queue as `index + n`, one full round later, so both queues stay in turn order and the party left standing wins.

Precedence comes first because it is Evaluate RPN with the operators in their usual place. Basic Calculator II (227) asks for the value of a string such as `"3+2*2"`, which is 7: `*` and `/` bind before `+` and `-`, and division truncates toward zero, so `" 3/2 "` is 1. An operator cannot be applied when you read it, because its right operand has not been read yet.

So the operator waits *in front of* the current number, in `op`, and is applied when the next operator arrives. `+` and `-` are put off by pushing signed terms, which the end adds up; `*` and `/` bind tighter, so they combine with the term on top at once. The number is read digit by digit, `num = num * 10 + int(ch)`, and a sentinel `"+"` at the end makes the last number get applied too.

```python
def push_term(stack, op, num):               # put num on the stack the way op says
    if op == "+":
        stack.append(num)
    elif op == "-":
        stack.append(-num)                   # the sign is stored with the term
    elif op == "*":
        stack.append(stack.pop() * num)      # binds to the term before it
    else:
        stack.append(int(stack.pop() / num)) # -3 / 2 -> -1 (truncate), not -2


def calculate_ii(s):
    stack, num, op = [], 0, "+"              # STATE + INIT: signed terms; op = the operator in front of num
    for ch in s + "+":                       # the sentinel "+" flushes the last number
        if ch.isdigit():
            num = num * 10 + int(ch)         # one more digit
        elif ch in "+-*/":
            push_term(stack, op, num)        # STEP: num is complete, apply the operator in front of it
            num, op = 0, ch
    return sum(stack)                        # RETURN: the postponed + and - happen here


print(calculate_ii("3+2*2"), calculate_ii(" 3/2 "), calculate_ii("14-3/2"))   # 7 1 13
```

**Try it**
- In `push_term`, change `int(stack.pop() / num)` to `stack.pop() // num` and run `calculate_ii("14-3/2")`: 12 instead of 13, because the term is stored as `-3` and `-3 // 2` floors to -2.
- Delete `+ "+"` from the loop and run `calculate_ii("3+2*2")`: 5 instead of 7. The pending `* 2` is never applied.
- Print `stack` just before the `return` for `"2*3+4*5-6/2"`: `[6, 20, -3]`, one signed term per `+` or `-`, which sum to 23.

Park and resume comes next because the thing on the stack is no longer a value but a whole context. Decode String (394) asks you to expand `k[text]`, which may nest: `"3[a2[c]]"` is `"accaccacc"`. An opening bracket means *save where I am and start fresh*; a closing bracket means *finish the inner part, restore what was saved, and merge*. The stack parks `(text so far, repeat count)` at every `[`, and `cur` is always the text of the innermost open group.

```python
def decode_string(s):
    stack, cur, k = [], "", 0                # STATE + INIT: parked (text before '[', count); cur = open group's text
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)             # "10[a]": counts can have several digits
        elif ch == "[":
            stack.append((cur, k))           # STEP: park, then start fresh inside
            cur, k = "", 0
        elif ch == "]":
            prev, count = stack.pop()        # STEP: resume the parked context
            cur = prev + cur * count
        else:
            cur += ch                        # STEP: a letter extends the open group
    return cur                               # RETURN


print(decode_string("3[a2[c]]"), decode_string("2[abc]3[cd]ef"))   # accaccacc abcabccdcdcdef
```

**Try it**
- Delete the line `cur, k = "", 0` and run `decode_string("a2[b]")`: `aabab` instead of `abb`. The parked prefix `"a"` was also left in the inner text, so it got repeated.
- Change `k = k * 10 + int(ch)` to `k = int(ch)` and run `decode_string("10[a]")`: an empty string, because only the last digit (0) survived.
- Print `stack` right after each push for `"3[a2[c]]"`: `[('', 3)]`, then `[('', 3), ('a', 2)]`. One frame per open bracket.
- Predict `decode_string("2[a]b")` before running: `aab`. Text after a group just extends `cur`.

The next two problems pop for a different reason, to destroy and to undo. Asteroid Collision (735) asks which asteroids survive. The size is the absolute value, the sign is the direction, and when two meet the smaller explodes, both if they are equal: `[5, 10, -5]` ends as `[5, 10]`, `[8, -8]` as `[]`. Only a left-mover arriving after a right-mover can crash, and it meets the most recent survivor first. So it fights the top *while* it keeps winning (FIX), and it is pushed only if it survives (STEP).

Simplify Path (71) asks for the canonical form of a Unix path: `"/a/./b/../../c/"` is `"/c"`. A path is a stack of directory names: a name goes one level down, `..` goes one level up, but never above the root. The same function is in `practice/simple/basics/stacks/02_simplify_unix_path.py`.

```python
def asteroid_collision(asteroids):
    stack = []                               # STATE + INIT: survivors so far, left to right
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:   # FIX: only -> <- collide
            if stack[-1] < -a:
                stack.pop()                  # the top explodes, a flies on
            else:
                if stack[-1] == -a:
                    stack.pop()              # same size: both explode
                alive = False
        if alive:
            stack.append(a)                  # STEP: a survives (for now)
    return stack                             # RETURN: the survivors


def simplify_path(path):
    stack = []                               # STATE + INIT: directory names, the root side at the bottom
    for part in path.split("/"):
        if part == "..":
            if stack:                        # never above the root
                stack.pop()                  # STEP: one level up
        elif part and part != ".":           # "" (from "//") and "." change nothing
            stack.append(part)               # STEP: one level down
    return "/" + "/".join(stack)             # RETURN


print(asteroid_collision([5, 10, -5]), asteroid_collision([8, -8]), asteroid_collision([1, 2, -5]))   # [5, 10] [] [-5]
print(simplify_path("/a/./b/../../c/"), simplify_path("/../"), simplify_path("/home//foo/"))   # /c / /home/foo
```

**Try it**
- Change the `while` in `asteroid_collision` to `if` and run `[1, 2, -5]`: `[1, -5]` instead of `[-5]`. One fight per asteroid is not enough.
- Delete the two lines of the same-size case and run `[8, -8]`: `[8]` instead of `[]`.
- Run `asteroid_collision([-2, -1, 1, 2])`: nothing collides. Left-movers already on the left never meet the right-movers behind them.
- Remove the `if stack:` guard and run `simplify_path("/../")`: `IndexError`, because `..` at the root tries to pop an empty stack.

Entries that remember come next, because here the decision "what goes in one entry" is the whole solution. Min Stack (155) asks for a stack whose `push`, `pop`, `top` and `getMin` all run in O(1): push −2, 0 and −3, and `getMin` is −3; pop, and it is −2 again. Remove All Adjacent Duplicates in String II (1209) asks you to delete every run of k equal neighbours, again and again, until none is left: `"deeedbbcccbdaa"` with k = 3 becomes `"aa"`.

When the pop must know something about what lies *below* the top, store it in the entry. A stack only changes at its top, so the minimum of everything below an entry cannot change while that entry is there: Min Stack stores it next to the value. Remove Adjacent Duplicates II stores a run as `[char, count]`, because when a run of k vanishes, the run underneath can keep growing.

```python
class MinStack:                              # 155
    def __init__(self):
        self.stack = []                      # STATE + INIT: (value, min of this entry and everything below)

    def push(self, x):
        low = min(x, self.stack[-1][1]) if self.stack else x
        self.stack.append((x, low))          # STEP: the entry carries its own minimum

    def pop(self):
        self.stack.pop()                     # the entry below still knows its own minimum

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]


def remove_duplicates(s, k):                 # 1209
    stack = []                               # STATE + INIT: [char, how many in a row]
    for ch in s:
        if stack and stack[-1][0] == ch:
            stack[-1][1] += 1                # STEP: the run on top grows
            if stack[-1][1] == k:
                stack.pop()                  # FIX: k in a row vanish; the run below may grow again
        else:
            stack.append([ch, 1])            # STEP: a new run starts
    return "".join(ch * n for ch, n in stack)    # RETURN


ms = MinStack()
for x in [-2, 0, -3]:
    ms.push(x)
before = ms.getMin()
ms.pop()
print(before, ms.top(), ms.getMin())                                           # -3 0 -2
print(remove_duplicates("deeedbbcccbdaa", 3), remove_duplicates("abbaca", 2))   # aa ca
```

**Try it**
- Print `ms.stack` after the three pushes: `[(-2, -2), (0, -2), (-3, -3)]`. The right column is the running minimum, frozen at each height.
- Build the two-stack version instead: a `mins` stack pushed only when `x < mins[-1]`, popped when the popped value equals `mins[-1]`. Push 0, push 0, pop, then `getMin`: `IndexError`, because the single 0 in `mins` was shared by both pushes. Push when `x <= mins[-1]`.
- Print `stack` after every character of `"deeedbbcccbdaa"` with k = 3: when `ccc` vanishes, the `bb` underneath meets one more `b` and vanishes too, and then `ddd` does the same.
- Make the entry a tuple, `(ch, 1)`: `TypeError` on `stack[-1][1] += 1`, because a tuple can't change. That is why the entry is a list.

A queue from two stacks closes the main path, because it shows that a stack and a queue differ by exactly one reversal. Implement Queue using Stacks (232) asks for a FIFO queue with `push`, `pop`, `peek` and `empty`, built from stack moves only: push 1, push 2, and `peek` is 1. Pouring one stack into another reverses it, which turns "newest on top" into "oldest on top". Pour only when the outbox is empty, so every item is poured once: amortised O(1), which means the cost averaged over all the operations.

```python
class MyQueue:                               # 232
    def __init__(self):
        self.inbox, self.outbox = [], []     # STATE + INIT: inbox newest on top; outbox oldest on top

    def push(self, x):
        self.inbox.append(x)                 # STEP

    def peek(self):
        if not self.outbox:                  # FIX: refill only when empty, or the order breaks
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox[-1]               # RETURN: the oldest item

    def pop(self):
        self.peek()                          # make sure the oldest item is on the outbox top
        return self.outbox.pop()

    def empty(self):
        return not self.inbox and not self.outbox


q = MyQueue()
q.push(1)
q.push(2)
first = q.pop()
q.push(3)                                    # 3 must wait behind 2
print(first, q.pop(), q.pop(), q.empty())    # 1 2 3 True
```

**Try it**
- In `peek`, remove `if not self.outbox:` so it always pours, and replay the lines above: the second `pop` returns 3 instead of 2, because 3 was poured on top of the waiting 2.
- Print `q.inbox, q.outbox` after every call: each item crosses from inbox to outbox exactly once.
- Push 1 to 1000, then pop all 1000: count the appends to `outbox`. There are exactly 1000, so the expensive pour is paid once per item.

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

The full calculator is Decode String's park-and-resume applied to Basic Calculator II. Basic Calculator (224) and Basic Calculator III (772) ask for the value of an expression with parentheses: `"(1+(4+5+2)-3)+(6+8)"` is 23, and `"2*(5+5*2)/3"` is 10. A `(` parks `(terms so far, pending operator)`, and a finished group becomes one number for the outer expression. For 224 alone there is a shortcut: with only `+` and `-`, a parenthesis just flips signs, so a stack of signs is enough.

```python
def calculate(s):                            # + - * / and parentheses (224, 227, 772)
    stack, num, op, saved = [], 0, "+", []   # STATE + INIT: saved = (terms, op) parked at each "("
    for ch in s + "+":                       # the sentinel "+" flushes the last number
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "(":
            saved.append((stack, op))        # STEP: park the outer expression, start fresh
            stack, op = [], "+"
        elif ch in "+-*/)":
            push_term(stack, op, num)        # STEP: num is complete, apply the operator in front of it
            if ch == ")":                    # the group is finished: it becomes one number
                num = sum(stack)
                stack, op = saved.pop()      # resume the outer expression
            else:
                num, op = 0, ch
    return sum(stack)                        # RETURN


print(calculate("(1+(4+5+2)-3)+(6+8)"), calculate("-(2-3)"), calculate("2*(5+5*2)/3"))   # 23 1 10
```

**Try it**
- Print `saved` right after it grows, for `calculate("2*(3+(4-1))")`: first `[([2], '*')]`, then `[([2], '*'), ([3], '+')]`. Each `(` parks one more outer expression. The answer is 12.
- Delete `num = sum(stack)` and run `calculate("2*(3+4)")`: 8 instead of 14. The outer `*` multiplied only the group's last number.
- Predict `calculate("-(3*(2-5))")` before running: `-(3 * -3) = 9`.

### Say it in the interview

Warm-up (Valid Parentheses): "a closer must match the most recent unfinished opener, so I push openers, compare each closer with the top, and the string is valid iff the stack ends empty: O(n)."

The medium version, Decode String:

> "The brute force expands an innermost `k[...]` and rescans, again and again. But a `]` always closes the most recent open `[`, which is last-in-first-out, so one pass with a stack works. At `[` I park the text built so far and the count, and start fresh. At `]` I pop and glue prefix + inner × count. The invariant: `cur` is the innermost open group's text so far, and the stack holds the outer prefixes, innermost on top. Time is proportional to the output; the stack holds one frame per open bracket."

Point at the two pushes and pops while you say the invariant. Likely follow-ups and your answers:

- *Counts with several digits* → `k = k * 10 + int(ch)`, and reset `k` after `[`.
- *Text after a group*, `"2[a]b"` → a letter always extends `cur`, so it just works: `aab`.
- *Recursion instead of a stack* → each `[` calls the decoder for the inner part; the call stack holds the same frames.
- *A stray `]` with nothing open* → check `if not stack` before popping and report invalid input.
- *A calculator instead* → `*` and `/` happen at once, on the top term; `+` and `-` wait for the final sum; `int(a / b)` because Python's `//` floors.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Asteroid Collision | `stack/asteroid_collision.py` · `practice/simple/basics/stacks/05_asteroid_collision.py` | survivors on a stack; a left-mover fights right-moving tops while it keeps winning |
| Basic Calculator | `stack/basic_calculator.py` | only + and −: a parenthesis just flips the signs inside it; keep a stack of context signs |
| Basic Calculator II | `stack/basic_calculator_ii.py` · `practice/simple/basics/stacks/04_basic_calculator_ii.py` | apply the previous operator when the next one arrives; push signed terms, `*` `/` edit the top, then sum |
| Decode String | `stack/decode_string.py` · `practice/simple/basics/stacks/03_decode_string.py` | on `[` park (text, count) and start fresh; on `]` pop and glue prefix + inner × count |
| Design Circular Deque | `queues/design_circular_deque.py` | ring buffer at both ends: insertFront steps head back `(head − 1) % k` before writing |
| Design Circular Queue | `queues/design_circular_queue.py` | fixed array + head + count; tail = (head + count) % k; count tells empty from full |
| Dota2 Senate | `queues/dota2_senate.py` | one queue of turn indices per party; the earlier front bans the other and rejoins as i + n |
| Evaluate Reverse Polish Notation | `stack/evaluate_reverse_polish_notation.py` · `practice/simple/15_evaluate_reverse_polish_notation.py` | numbers wait on a stack; an operator pops the right operand, then the left, and pushes the result |
| Implement Queue using Stacks | `queues/implement_queue_using_stacks.py` · `practice/simple/basics/stacks/01_array_stack_and_queue_via_two_stacks.py` | inbox + outbox; pour only when the outbox is empty, so each item moves once: amortised O(1) |
| Implement Stack using Queues | `queues/implement_stack_using_queues.py` | after each push, rotate the queue len − 1 times so the newest item sits at the front |
| Longest Valid Parentheses | `stack/longest_valid_parentheses.py` | indices on a −1 barrier; after a match, run = i − top; a stray `)` becomes the barrier |
| Min Stack | `stack/min_stack.py` · `practice/simple/14_min_stack.py` | store (value, min so far) in every entry; popping reveals the older minimum for free |
| Minimum Add to Make Parentheses Valid | `stack/minimum_add_to_make_parentheses_valid.py` | one bracket type: the stack is a counter; a `)` at zero costs one insert, leftover opens one each |
| Number of Recent Calls | `queues/number_of_recent_calls.py` | t only grows, so expired pings sit at the front: popleft while q[0] < t − 3000 |
| Parsing a Boolean Expression | `stack/parsing_a_boolean_expression.py` | push everything; on `)` pop letters into a set down to `(`, then apply the operator below it |
| Valid Parentheses | `stack/valid_parentheses.py` · `practice/simple/13_valid_parentheses.py` | push openers; a closer must match the top; valid iff the stack ends empty |

### Self-check

1. Why can't Valid Parentheses be solved with one counter per bracket type?
<details><summary>Answer</summary>Counters forget the order. <code>"([)]"</code> has one of each and balanced counts, but its <code>)</code> arrives while <code>[</code> is the innermost open bracket. A counter is enough only with a single bracket type, because then every stack entry is the same and only the stack's height matters (921).</details>

2. In Basic Calculator II, why is an operator applied when the *next* operator arrives, not when it is read?
<details><summary>Answer</summary>When you read <code>*</code>, its right operand hasn't been read yet. The number is complete only when the next operator (or the sentinel at the end) shows up, so the pending operator waits in <code>op</code> and is applied then.</details>

3. Queue from two stacks: one `pop` can move n items. Why is it still O(1)?
<details><summary>Answer</summary>Amortised: every item is pushed onto the inbox once, moved to the outbox once and popped once, a constant number of stack operations per item. An unlucky single pop does many moves at once, but n operations never do more than a constant times n moves in total.</details>

4. The ring buffer keeps `head` and `count`. What goes wrong with only `head` and `tail`?
<details><summary>Answer</summary><code>head == tail</code> happens both when the queue is empty and when it is full, so you can't tell them apart. Keeping <code>count</code> (or always leaving one slot unused) removes the ambiguity, and the tail is just <code>(head + count) % k</code>.</details>
