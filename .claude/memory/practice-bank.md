---
name: practice-bank
description: "practice/ folder (started 2026-10-04): 50 traced LeetCode problems + ~80 basics exercises with verified bug variants, built into bank.json for the DSA Drill artifact's debug mode"
metadata:
  node_type: memory
  type: project
  originSessionId: 692c6852-d402-4a9b-bc81-0a3bf34fcda1
  modified: 2026-10-05T01:23:41.150Z
---

On 2026-10-04 the user asked for "50 leetcode algorithms representative of the area, medium / medium-hard, brute force and optimal, a readme for each with intuitive explanation, scripts with print/logger statements", plus basics exercises (stacks, monotonic stacks, heaps, linked lists, backtracking, 5 sorting algorithms, trees, searches, graph algorithms incl. Kruskal/Prim/Dijkstra, strings, tries, and later matrices, math, bits), no DP, "also to artefact". Built as `practice/` with `SPEC.md` (file format), `build_bank.py` (validator + `bank.json` + generated `practice/README.md`), `problems/<nn>_<slug>/{solution.py,README.md}` and `basics/<area>/<nn>_<slug>.py` + area README.

**Why:** The artifact's Claude-written debug questions were being refused (`refused` sample error) and the user wants 15-30 line debugging drills with selectable difficulty. Hand-authored `BUGS` variants in each script are verified by the build (buggy program must fail the tests; expected/actual output recorded), so the artifact's "Debug a program from the bank" mode needs no model call.

**How to apply:** Every script: markers `# --- helpers/brute force/optimal/demo/tests/bugs ---`, `log()` only as standalone statements (stripped for the shown program), `BUGS` entries with exact `replace`/`with` lines and 3 decoys. Validate with `python3 practice/build_bank.py --check <paths>`; full build writes bank.json which is published next to the DSA Drill artifact (see [[drill-agent-site]]). Adding a problem = new folder + run the build + republish the artifact with `files: {"bank.json": "practice/bank.json"}`. Difficulty mapping in the artifact: basics L1 (20 pts), Medium L2 (30), Medium-Hard L3 (40).

On 2026-10-06 the user also asked for `practice/simple/<nn>_<slug>.py` (one per problem: docstring with Idea + Pseudocode, one clean optimal function, small `__main__` demo with `# expected` comments, "without the debugging fluff") and a one-page `practice/CHEATSHEET.md` of Python technique templates. Keep `simple/` free of markers/BUGS/logs; build_bank.py does not scan it.
