# Q004. Design a multi-agent customer workflow coordinated through CX

## Scope and success

Handle complex support investigations that need order facts, policy evidence, and technical troubleshooting. Use specialization only where independent tasks justify it. Establish a bounded task graph, an execution deadline, and the actions each worker may perform. Success is a supported recommendation or completed approved action.

## Architecture and request path

CX owns the user-facing conversation and collects the investigation request. A backend coordinator creates a durable job, launches independent read-only workers for order facts and policy retrieval, and combines their typed results. A troubleshooting worker can propose next steps. CX presents clarification or a concrete proposal and uses a flow for consequential confirmation.

Do not let workers converse endlessly with each other. The coordinator enforces dependencies, maximum calls, token budgets, and a stop condition. Each worker sees only its needed context and cannot expand its own authority.

## Data and contracts

Persist job ID, task graph, worker states, artifacts, evidence IDs, deadlines, and operation proposals. Results contain facts, sources, uncertainty, and failure status. A shared artifact store avoids copying entire histories into every prompt. The coordinator rejects results outside the agreed schema.

## Failure, security, and scale

Partial results can produce a qualified answer if missing evidence is explicitly identified. Failed authorization stops the relevant branch. Retry safe reads within budget; mutations use a separate domain service and operation ID. Limit per-customer concurrency to prevent one investigation consuming all capacity.

## Trade-off and validation

Parallel workers can lower wall-clock latency but increase cost and inconsistent conclusions. Compare against one orchestrator with the same tools. Evaluate task correctness, evidence agreement, completion time, tool-call count, and recovery from one failed worker.

## Interview follow-up answered

**Two workers disagree about eligibility.** Preserve both evidence versions, resolve against the authoritative policy/transaction service, and ask for missing facts if needed. Voting among model outputs does not establish a business rule. Record the discrepancy for evaluation and source maintenance.
