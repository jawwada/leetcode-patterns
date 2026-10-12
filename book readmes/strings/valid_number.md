# Valid Number
*LeetCode 65 · Hard · Pattern: Single-pass state machine with flags · Reading time ~11 min*

## The problem

Return True if the string is a valid number: an optional sign, then an integer or a decimal ("3.", ".5", "3.14"),
optionally followed by 'e'/'E', an optional sign and an integer. No spaces, no inf/nan.

```text
Example: "2e10", "-.9" and "4." are valid; "e3" (no mantissa),
  "99e2.5" (exponent must be an integer) and "." are not.
```

## What the problem is really asking

Decide whether a string is a well-formed number. The grammar is:

```text
 number   :=  [sign] mantissa [ ('e'|'E') [sign] digits ]
 mantissa :=  digits
           |  digits '.' [digits]        "4."  "3.14"
           |  '.' digits                 ".5"
 sign     :=  '+' | '-'
 digits   :=  one or more of 0-9
```

There are no spaces, no `inf`, no hex and no thousands separators. The answer is a boolean. Unlike atoi, you are not allowed to stop early and ignore the rest: every character must belong to the grammar, and the string must end in an accepting position.

What makes it Hard is not the algorithm, which is one pass. It is the number of edge cases that a hand-written chain of `if`s gets wrong. A short list of strings and their verdicts makes the point:

```text
 valid:    "2"  "0089"  "-0.1"  "4."  "-.9"  "2e10"  "3e+7"
           "46.e3"  "-123.456e789"
 invalid:  "e3"  "1e"  "."  "+"  ".e1"  "99e2.5"  "--6"
           "+-1"  "1 "  "4e+.5"  "3.e"
```

Each of the invalid ones is a different rule: a mantissa is required, an exponent needs digits, a lone dot is not a number, the exponent must be an integer, and a sign may appear only at the start or right after `e`.

## Do it by hand first

Check `"-1.5e+7"` with a pencil. You go left to right and keep asking "is this character allowed here?" To answer that, you consult what you have already seen.

```text
 char  question you ask                   answer
  -    at the very start?                 yes -> ok
  1    digits are always ok                ok, "have a digit"
  .    seen a dot already? seen an e?      no, no -> ok
  5    digit                               ok
  e    have a digit before it? seen e?     yes, no -> ok
       (the exponent now needs its OWN digit)
  +    is the previous char e?             yes -> ok
  7    digit                               ok, "have a digit"
 end   does the last part have a digit?    yes -> VALID
```

Your hand carried three facts: **have I seen a digit in the current part**, **have I seen a dot**, **have I seen an e**. For signs it also glanced at the previous character. That is all the memory the grammar needs.

## The first honest attempt

The decomposition people reach for first is to split the string at `e`. The left side must be a decimal and the right side a signed integer. For "decimal", strip a sign, split at `.`, check that each side is all digits or empty, and check that both are not empty. For "signed integer", strip a sign and check that the rest is non-empty digits.

```text
 "-1.5e+7"
   split at e:      "-1.5"        "+7"
   is_dec("-1.5"):  strip sign -> "1.5"
                    split at . -> "1", "5"   digits? yes, yes
   is_int("+7"):    strip sign -> "7"         digits? yes
```

It works, and it is O(n). The repeated work is that the same characters are scanned three or four times: once to find `e`, once to find `.`, and once in each `digits` check, with a slice copied at every step. The deeper cost is the grammar being scattered across helpers. Each helper has its own edge cases (an empty side, a sign alone, a dot alone), and the interactions between them, such as `"+."` or `"4e+.5"`, live in nobody's code. Most wrong submissions for this problem are this structure with one edge case missing.

```text
  - 1 . 5 e + 7
  ^^^^^^^^^^^^^   scan 1: find 'e'
  ^^^^^^^         scan 2: find '.' in left part
    ^ ^           scan 3: digits? on each side
            ^^^   scan 4: is_int on right part
```

## The turning point

**Whether the next character is legal depends only on a handful of facts about what came before, so a single left-to-right pass with a finite state is a complete recogniser.**

The textbook way to see this is to write the deterministic automaton. Each state names "what kind of prefix have I read", and each column is a character class:

```text
             digit   sign    '.'     e/E
 START       INT     SIGN    DOT0    x
 SIGN        INT     x       DOT0    x
 INT*        INT     x       DOT1    E
 DOT0        FRAC    x       x       x      ('.' with no digit)
 DOT1*       FRAC    x       x       E      ('4.')
 FRAC*       FRAC    x       x       E
 E           EXPD    ESIGN   x       x
 ESIGN       EXPD    x       x       x
 EXPD*       EXPD    x       x       x
 * = accepting at end       x = reject immediately
```

The same table drawn as a graph (s = sign, d = digit, e = e/E):

```text
           s           d
  START ------> SIGN ------> (INT) <-+ d
    |  d          |            | |   |
    +-------------|----------->+ +---+
    |             |            |
    | .           | .          | .
    v             v            v
   DOT0 <---------+         (DOT1)
    |                          |
    | d                        | d
    v                          v
  (FRAC) <---------------------+      FRAC loops on d
    |
    | e        (e also leaves INT and DOT1 to E)
    v
    E ----s----> ESIGN
    |              |
    | d            | d
    v              v
  (EXPD) <---------+                  EXPD loops on d

  ( ) = accepting state; any missing edge = reject
```

Nine states is a lot to code as a table in an interview, but looking at the table shows they are not independent. Describe each state by three bits, digit-seen-in-current-part (D), dot-seen (P) and exp-seen (X):

```text
 state    D  P  X
 START    0  0  0      SIGN = START + "previous char was sign"
 INT      1  0  0
 DOT0     0  1  0
 DOT1     1  1  0  <-  DOT1 and FRAC: identical rows, merge
 FRAC     1  1  0  <-
 E        0  0* 1      (* P no longer matters once X is set)
 ESIGN    0  .  1      ESIGN is E plus "previous char was sign"
 EXPD     1  .  1
```

So three booleans plus "what was the previous character" encode every state, and every transition becomes a rule over the flags:

- **digit**: always legal. Set D.
- **sign**: legal only at index 0 or immediately after `e`/`E`. Otherwise reject.
- **'.'**: reject if P or X is set (one dot, and never in the exponent). Otherwise set P.
- **'e'/'E'**: reject if X is set or D is clear (one exponent, and it needs a mantissa with a digit). Otherwise set X and **clear D**, because the exponent part needs its own digit.
- **anything else**: reject.
- **end of string**: accept iff D is set, meaning the current part, mantissa or exponent, is non-empty.

The single most important line is "clear D on e". Without it `"1e"` is accepted. With it, the D flag means "the part I am in has a digit", which is the question the end-of-string check needs answered.

Signs need no flag because their rule is purely local: look one character back. A sign at index 0 is the mantissa sign. A sign after `e` is the exponent sign. A sign anywhere else is junk, and that catches `"--6"`, `"+-1"` and `"1+2"` in one place.

## Watch it work

`s = "-1.5e+7"`. The state after each character is shown as D P X.

**Frame 1.** `-` at index 0 is a sign at the start, so it is legal. No flags change.
```text
 - 1 . 5 e + 7
 ^
 D=0 P=0 X=0        (state SIGN)
```

**Frame 2.** `1` is a digit, so D is set.
```text
 - 1 . 5 e + 7
   ^
 D=1 P=0 X=0        (state INT, accepting)
```

**Frame 3.** `.` with P=0 and X=0 is legal, so P is set.
```text
 - 1 . 5 e + 7
     ^
 D=1 P=1 X=0        (state DOT1, accepting: "-1." is valid)
```

**Frame 4.** `5` sets D (already set). Then `e` arrives with D=1 and X=0, so it is legal. X is set and D is cleared.
```text
 - 1 . 5 e + 7
         ^
 D=0 P=1 X=1        (state E, NOT accepting: "-1.5e" invalid)
```

**Frame 5.** `+` comes right after `e`, so it is legal. `7` sets D.
```text
 - 1 . 5 e + 7
             ^
 D=1 P=1 X=1        (state EXPD)
```

**Frame 6.** End of string with D=1, so it is VALID. For contrast, `"1e2.5"` breaks at the dot:
```text
 1 e 2 . 5
       ^  '.' with X=1 -> reject          return False
 flags before '.': D=1 P=0 X=1
```

**Frame 7.** Two short rejects show the other guards.
```text
 "e3":  e at index 0, D=0          -> reject (no mantissa)
 ".":   '.' ok, P=1; end with D=0  -> False  (no digit)
```

At every step the three flags plus the previous character identified exactly one row of the nine-state table, and the decision about the next character used only that. No character was looked at twice.

## Why it is correct

The argument is that the flag machine is the nine-state automaton, which is the grammar.

1. **The automaton accepts exactly the grammar.** Every path from START to an accepting state spells `[sign] mantissa [e [sign] digits]`. The only way into the exponent is through `e` from INT, DOT1 or FRAC, which are exactly the states whose prefix contains a mantissa digit. The only accepting exponent state is EXPD, which requires at least one digit after `e` and its optional sign. DOT0 is not accepting and has no `e` edge, which rules out `"."` and `".e1"`.

2. **The flags plus the previous character determine the automaton state.** The table above maps each state to a distinct (D, P, X, previous-was-sign-or-e) combination, except DOT1 and FRAC, whose rows are identical, so merging them changes nothing.

3. **Each flag rule is the automaton's row.** A digit is legal from every non-reject state and moves to a state with D=1. A dot is legal only from START, SIGN and INT, which are exactly the states with P=0 and X=0. `e` is legal only from INT, DOT1 and FRAC, exactly the states with D=1 and X=0, and it moves to E, where D=0. A sign is legal only from START (index 0) and E (previous char `e`).

4. **Acceptance.** The accepting states INT, DOT1, FRAC and EXPD are exactly those with D=1. The non-accepting ones (START, SIGN, DOT0, E, ESIGN) all have D=0.

So the one-pass flag scan returns True iff the automaton ends in an accepting state, iff the string matches the grammar.

## Cost

- **Time O(n)**: one pass, O(1) work per character, and it stops at the first reject.
- **Space O(1)**: three booleans and an index.
- The split-and-check version is also O(n) time but O(n) space for slices, and it scans characters several times.

## Variations you will meet

- **Allow surrounding spaces** (the original LeetCode 65 statement did). Strip first, or add LEADING_SPACE and TRAILING_SPACE states. Spaces in the middle must still reject, so trailing spaces lead to a state that accepts nothing but more spaces.
- **"Write it as a table-driven DFA."** Some interviewers want the nine-state table literally. Map each character to a class index, then `state = table[state][cls]`, and check `state in ACCEPT` at the end. It is easier to extend (hex, `inf`, underscores) than the flags.
- **Return the value, not just validity.** Combine with atoi-style accumulation: build the mantissa as an integer plus a count of fractional digits, then the exponent. Real parsers (`strtod`) do this with careful rounding.
- **Regex.** `^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$` is the same automaton written compactly, and a good sanity check to mention. Interviewers usually want the hand-built one.

## What to carry forward

Write the automaton, notice which states are really combinations of a few independent facts, and replace states with flags. The rule people miss is the transition that **resets** a flag: `e` clears "seen digit". The next problem leaves parsing for structure. Instead of flags, a later token cancels an earlier one, and the stack appears.
