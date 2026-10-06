---
name: dsa-quiz
description: Quiz the user in chat on the intuitive layer between data structures, algorithms and code, one multiple-choice question at a time, with topic quotas, scoring, a revisit list and full visual traces on every miss. Use when the user asks to be quizzed, drilled or to practise DSA or system design.
---

# DSA intuition quiz

The user has a long algorithms background and is preparing for a Google coding interview. They want to internalize *why* solutions work by being quizzed in chat, not by reading notes or using a web app.

## What every question targets

Pick the one non-obvious fact that makes the solution work: the invariant, the monotonic property, why an element can be discarded forever, why a commit is final, why this data structure and not another. Ask the "why" that ties together the data structure, the algorithm and one specific line of code, marked with `# <--`. Freeze a concrete moment of the run when that helps (the pointer positions, the dict contents, what has and hasn't been seen yet). Avoid trivia: complexity recall, API names, syntax.

## How every question is written

Ask through AskUserQuestion, one question per call, with everything inside the question text:

1. **PROBLEM:** a one-line statement. Never name a LeetCode problem and assume the user knows it.
2. **INPUT / OUTPUT:** a concrete small example with its expected output, plus an ASCII sketch when the problem is visual.
3. **CODE:** the full snippet, verbatim. Never assume the user remembers an algorithm's code.
4. **QUESTION:** the core "why", pointing at the marked line.

Options:
- Four options with short labels and one-line descriptions.
- Rotate the slot of the correct option deliberately, about a quarter each across A to D.
- The correct option must never be the longest or the most detailed one.

## Topic quotas (per 40-question cycle)

| Topic | Questions |
|---|---|
| Strings | 6 |
| Graphs | 6 |
| Min-heap | 6 |
| Trees | 6 |
| Backtracking | 4 |
| System design | 4 |
| Dynamic programming | 2 (explicit exception to the no-DP rule; only these two) |
| Two pointers / sliding window | 1 |
| Binary search on the answer | 1 |
| Monotonic stack | 1 |
| Prefix sums / hashing | 1 |
| Intervals / greedy | 1 |
| Linked list | 1 |

Rules for the quota:
- Always pick the next topic from the category furthest below its quota.
- A problem spanning two categories counts for its primary one.
- Revisit questions don't count against the quota.
- System design questions follow the same core-challenge rule: a scenario with numbers, then the one constraint that forces the design choice.
- Show the quota table with the "asked so far" counts when the user asks for it.

## Scoring and revisits

- Levels: L1 = 10, L2 = 20, L3 = 30 points, plus 5 for each answer in a streak. A wrong answer resets the streak.
- End every reply with: `Score N · streak N · revisit: [...]`.
- A missed concept goes on the revisit list. It comes back later in a different form (a frozen moment, another example, a sibling problem) and clears after two correct answers.
- If the user flags a question as unclear twice, park it on the revisit list, ask what they want clarified, and don't run a blocking clarification round.
- If the user asks what a term means (deque, monotonic stack, prefix sum, ...), define it with a tiny trace before asking again.

## On a correct answer

Award the points, then give the mental picture in two to four lines: the shape of the data and the motion of the algorithm. Then go straight to the next question.

## On a wrong answer: all three, never compressed

1. **The correct answer**, plus one line on why the chosen option fails, preferably pointing at the code.
2. **A complete worked example with visuals.** Trace every step. After each step, draw the data structure: a stack as a vertical column, a heap as a tree and as an array, a linked list with arrows, the queue contents, the dict contents, the pointers under the array. Label each step with the operation and the decision taken, and show the final state. Show what happens if the marked line is removed or changed (the counterexample).
3. **The intuition**, meaning the mental picture. Rules and summaries come after the full trace, never instead of it.
