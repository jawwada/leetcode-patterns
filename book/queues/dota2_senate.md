# Dota2 Senate

*LeetCode 649 · Medium · Pattern: Round-robin queues (re-enqueue with index + n) · Reading time ~9 min*

## What the problem is really asking

A string like `"DDRRR"` lists senators in seat order, each from party R (Radiant) or D (Dire). They act one at a time in
seat order, and when the last seat has acted, a new round starts from seat 0. On its turn, a senator who has not been
banned may ban one senator of the other party, who then loses every future turn. (A senator may also declare victory
when only its own party is left.) Everyone plays optimally. Return the winning party.

The answer is one word, but the object behind it is a *turn order that shrinks*: a cyclic line of players in which some
are removed as the rounds go by. Two things make it hard. First, the choice: whom should a senator ban? Second, the
simulation: the rounds wrap around, banned seats must be skipped, and it can take several rounds.

```text
"DDRRR", seats 0..4, n = 5

seat:   0   1   2   3   4
party:  D   D   R   R   R
turn:   1st 2nd 3rd 4th 5th, then seat 0 again ...
R has 3 senators, D has 2. Who wins?  (answer: Dire)
```

## Do it by hand first

Take the tiny case `"RDD"`. Seat 0 (R) acts first. It could ban seat 1 or seat 2. Seat 1 acts next, so if R leaves seat
1 alive, seat 1 will immediately ban R. Banning seat 1 at least removes the most urgent threat. Then seat 2 (D) acts and
bans R. Dire wins.

```text
"RDD":  R0 bans D1 (the next D to act)
        D2 bans R0  -> only D left: Dire
```

The rule your hand discovered: **ban the opponent who would act soonest.** An opponent who acts later is less of a
threat now, and you can always deal with them later, while an opponent who acts next will hurt your side before you get
another turn.

Now try `"DDRRR"` by hand and notice what you keep looking up: "which R acts next after this seat, wrapping around?" and
"which D acts next?". Two lines, each in turn order.

## The first honest attempt

Simulate literally. Keep a `banned` array. Walk the seats round after round; when a live senator at seat `i` acts, scan
forward circularly for the next live opponent and ban them. If the scan comes back to `i` without finding one, `i`'s
party wins.

```text
"DDRRR", round 1, banned seats marked x

seat 0 (D): scan 1(D) 2(R) -> ban 2      D D x R R
seat 1 (D): scan 2(x) 3(R) -> ban 3      D D x x R
seat 2, 3: banned, skip
seat 4 (R): scan 0(D)      -> ban 0      x D x x R
round 2
seat 1 (D): scan 2(x) 3(x) 4(R) -> ban 4
seat 1 again: scan 2 3 4 0 ... all x or D -> Dire
             ^^^^^^^^^^^^^^^^^^^
             the same banned seats are re-walked each scan
```

Each ban needs a scan of up to n seats, and up to n - 1 bans can happen, so O(n^2) time. The waste is the scanning: the
simulation keeps stepping over banned seats and teammates just to answer "who on the other side acts next?".

## The turning point

**Claim: the game is decided entirely by "who acts next on each side", so keep each party's senators in a queue sorted
by when they next act, and resolve the game as a sequence of duels between the two fronts.**

First, the greedy choice, justified: banning the opponent who acts soonest is never worse than banning a later one. If
you ban a later opponent instead, the sooner one gets a turn that the later one would have had anyway, plus a turn
earlier; swapping your ban to the sooner opponent removes a threat without adding any. So every ban targets the other
party's next actor.

Now look at the game only at the moments that matter. The next senator to act is whichever of the two queue fronts has
the earlier turn. That senator bans the other front (the opponent who would act soonest), and then waits for its own
next turn, one full round later. So:

- Pop both fronts, `a` from R and `b` from D.
- The smaller turn time acts. The larger is banned: it is simply not put back.
- The winner rejoins the back of its own queue, stamped with its next turn time.

What is "its next turn time"? Its seat in the next round. If seats are numbered `0 .. n-1` in round one, the same seat in
round two acts at time `i + n`, in round three at `i + 2n`. Re-enqueueing as `i + n` keeps every queue sorted by the
real time each senator acts, even across round boundaries, so comparing two fronts always compares two real turn times.

```text
why + n and not i?   R queue [4], D queue [5]  (5 = seat 0
                                                round 2)
with i:    R4 vs D0 -> D "acts first": WRONG, seat 0's
           round-2 turn comes after seat 4's round-1 turn
with i+n:  R4 vs D5 -> R acts first: right
```

Banned senators never re-enter a queue, so nobody is ever skipped over again. When one queue is empty, the other party
wins.

## Watch it work

`"DDRRR"`, `n = 5`. R queue `[2, 3, 4]`, D queue `[0, 1]`, fronts on the left.

```text
Frame 1: start
  R: [2, 3, 4]
  D: [0, 1]
  fronts: R2 vs D0
```

The two queues are each party's seats in turn order.

```text
Frame 2: duel R2 vs D0 -> 0 < 2, D0 acts, bans R2
  R: [3, 4]
  D: [1, 5]       D0 rejoins as 0 + 5 = 5
```

R2 is popped and gone. D0 goes to the back stamped with its round-two time.

```text
Frame 3: duel R3 vs D1 -> 1 < 3, D1 acts, bans R3
  R: [4]
  D: [5, 6]       D1 rejoins as 1 + 5 = 6
```

Two R senators gone already: Dire's members sit before them in seat order.

```text
Frame 4: duel R4 vs D5 -> 4 < 5, R4 acts, bans D5
  R: [9]          R4 rejoins as 4 + 5 = 9
  D: [6]
```

R4's round-one turn comes before seat 0's round-two turn (time 5), so R wins this duel. Without `+ n`, D's 0 would wrongly
beat R's 4.

```text
Frame 5: duel R9 vs D6 -> 6 < 9, D6 acts, bans R9
  R: []
  D: [11]         D6 rejoins as 6 + 5 = 11
  R is empty -> "Dire"
```

Seat 1 in round two (time 6) acts before seat 4 in round two (time 9). R has no senators left.

At every frame, each queue was sorted by actual turn time, every duel removed exactly one senator for good, and the fronts
were exactly the next actor of each party. The party with more senators lost because it sat later in the order.

## Why it is correct

Two facts carry the argument.

**The greedy ban is optimal.** By the exchange argument above, any strategy that bans a later opponent can be changed
to ban the soonest opponent without hurting the banning side, so we may assume every ban hits the other party's next
actor.

**The queues simulate that game exactly.** Invariant: each queue holds its party's live senators, sorted by their next
turn time, and all those times are later than every turn already taken. Initially true (seats in order). In a duel, the
smaller front time is the next turn in the whole game, because each front is its party's earliest. That senator bans the
other front, which is the soonest opponent, so the greedy rule is followed. The actor's next turn is `n` later, and it is
later than every other time in its own queue: those times are all less than the actor's time plus `n`, since each queue
spans less than one full round of turn times (every senator appears once, at most one round ahead). So appending
`a + n` at the back keeps the queue sorted. The game ends exactly when one party has no senators, which is when its
queue is empty.

## Cost

Time: O(n). Each duel permanently removes one senator, so there are at most n - 1 duels, each O(1) with a deque.
Space: O(n) for the two queues.

The literal simulation is O(n^2) because each ban scans past banned seats.

## Variations you will meet

- **Count bans instead of queues.** A one-queue version keeps a single deque of parties and a "pending bans" counter per
  side: a senator whose party owes a ban is skipped, otherwise it adds a ban against the other side and rejoins. Same
  O(n), same greedy.
- **Find the Winner of the Circular Game (1823).** One queue, fixed step: rotate `k - 1` and pop. The round-robin queue
  without the duel.
- **Task Scheduler (621, Heaps chapter).** Tasks rejoin a queue stamped with the time they may run again, `t + n + 1`,
  the same "stamp the next turn" idea, with a heap choosing among the ready ones.
- **Time Needed to Buy Tickets (2073).** People rejoin the back after each purchase; the queue simulation is fine, and a
  counting shortcut gives O(n) without simulating.

## What to carry forward

A queue is a turn order: the front acts, rejoins at the back, and stamping it with `index + n` keeps several lines
comparable across rounds. This closes the chapter. You have now seen the queue as reversal, rotation, window, ring and
turn order; next it will become the engine of breadth-first search, a queue of places still to explore.
