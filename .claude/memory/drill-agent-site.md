---
name: drill-agent-site
description: "Self-hosted Flask quiz agent in drill_agent/ (own username/password, Anthropic API key) built Oct 2026 as the web version of the chat drill"
metadata:
  node_type: memory
  type: project
  originSessionId: 692c6852-d402-4a9b-bc81-0a3bf34fcda1
  modified: 2026-10-05T01:39:31.693Z
---

On 2026-10-03 the user asked for the chat quiz to become a separate website with its own username/password login (not claude.ai sign-in) that "improves my leetcode skills" the same way. Built in `drill_agent/` (Flask + SQLite + anthropic SDK, run with the repo's uv venv). Questions are generated live by Claude from `curriculum.py`; trace questions are executed before being shown.

**Why:** User wanted to drill from a browser anywhere. They originally said "uses my cloud profile implicitly signed in", but the Agent SDK docs forbid using claude.ai subscription login for apps, so the site uses an API key stored in `drill_agent/config.json` (git-ignored) and its own login gates access.

On 2026-10-03 the user then said "forget it, save it as an artefact in claude.ai": the live version is the artifact https://claude.ai/artifact/J14FxosCeq7EuwUnMYxHS9 (capabilities sample+db+user, progress in data/users/<id>/progress, seed button for chat progress). The Flask app was deleted from the repo on 2026-10-04 at the user's request (repo clean). A second artifact, System Design Drill, https://claude.ai/artifact/WmPgGzQu26M13qJwtc4mhw, drills distributed systems with MCQs plus Claude-graded short answers (same scoring). User still wants to keep answering DSA questions in chat too.

On 2026-10-04 the user reported option clicks not registering in the DSA artifact; republished as v3 (delegated click handler, on-page error line, selected-state highlight, and a Claude-streamed "Full walkthrough with visuals" that runs automatically on every miss; seed updated to the chat score 345). Scratchpad sources get wiped between sessions, so re-read the artifact URL before editing.

Same day, v4 on the user's request: default mode "Debug a 15-30 line program" (Claude writes a program with exactly one planted bug, options are "line N: fix"; complex model tier; 20/30/40 pts), difficulty selector (auto or fixed level 1-3), "Show answer" button (counts as a miss), and a Scratchpad + Python console side by side. The console runs Pyodide 0.26.4 in a Web Worker from files published next to the page (pyworker.js, pyodide.js, pyodide.asm.js, pyodide.asm.wasm, pyodide-lock.json, and python_stdlib.zip published as python_stdlib.wasm because the host serves no .zip; the worker passes stdLibURL). Whether the viewer's CSP allows WebAssembly was NOT verified; the page shows "could not load the Python runtime" if it is blocked. On later publishes to this URL the runtime files are kept unless passed as null.

v6 (same day): modes are "Debug a program from the bank" (default, no model call; reads `bank.json` published next to the page, see [[practice-bank]]), "Debug a fresh program written by Claude" (reworded code-review prompt after `refused` errors), and "Quick mechanic drill"; a Problem bank browser shows each entry's README/solution with "Debug this", "Code to console", "Traced script to console". Republish after rebuilding the bank with `files: {"bank.json": {"from": "practice/bank.json"}}`.

**How to apply:** Both artifacts are updated by republishing the file to their URL (sources in the session scratchpad; re-read the artifact if lost). Scoring/revisit rules mirror [[drill-quizmaster-format]]. Chat quizzing continues in parallel; the chat revisit list is the source for the artifact's seed button.
