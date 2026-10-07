---
name: leetcode-playbook
description: "practice/LeetCode_Playbook/ holds 12 category notebooks generated from practice/playbook/NN_slug.md by build.py; idea-to-implementation focus, Try-it after every code cell, one fused voice"
metadata:
  node_type: memory
  type: project
  originSessionId: 25d5bda8-158a-40cb-850a-e870e3d23e3d
  modified: 2026-10-07T00:54:13.959Z
---

On 2026-10-06 the user asked for a notebook that expands `practice/CHEATSHEET.md` into a full, gentle, insight-first guide whose core is "how to turn the idea into an implementation". Built as markdown sources `practice/playbook/NN_slug.md` (00 Start Here, 01 From Idea to Code, 02-25 one technique each, 26 Final Checklists) compiled by `practice/playbook/build.py` into twelve category notebooks in `practice/LeetCode_Playbook/` (the user asked for one notebook per category rather than one huge notebook; `NOTEBOOKS` in build.py maps sections to notebooks, cross-notebook links are rewritten, the A-Z problem finder is in `12_Interview_Day.ipynb`). `build_html.py` renders all notebooks into one reading page for the claude.ai artifact. Jupyter is a dev dependency (`uv run jupyter lab`).

**Why:** The user knows the ideas but freezes when typing; every section answers seven decisions (State, Definition, Invariant, Step, Record, Init, Return) and maps "in words" to "in code". Mid-task the user added: after every code cell, 3-4 "Try it" experiments that teach the main flow and tricky points; then adversarial reviewer agents per section whose advice is fused in with no attribution ("single interface").

**How to apply:** Edit the `.md` sources, never the notebook; rebuild with `uv run python practice/playbook/build.py` and keep its reports at 0 (code cells without **Try it**, topic problems missing from or duplicated across Problem maps, broken `#sNN` links, practice/simple files never referenced). Style rules live in `practice/playbook/README.md`. Related: [[practice-bank]], [[google-interview-prep]].

**Update 2026-10-07:** the active build is now one notebook per topic: sources `practice/playbook/topics/NN_Name.md`, order/filenames in `topics/manifest.json`, 69 notebooks (00 Topic Index … 68 Problem Finder). `15_Segment_Trees` was inserted after Tries (later files renumbered +1). Hand edits to notebooks are lost on rebuild, so move them into the topic `.md`.
