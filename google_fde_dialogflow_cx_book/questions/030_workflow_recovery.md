# Q030. Design durable agent workflow recovery

## Scope and success

Resume multi-step investigations or actions after worker failure without duplicating side effects. Define which steps are repeatable, which outputs are durable, and which external outcomes can be queried. Success means recovery preserves the same authorized task and business invariants.

## Architecture and request path

CX creates a task through a backend coordinator. A durable workflow store records step transitions and artifact references. Workers acquire leases, execute eligible steps, and commit results with expected state versions. A recovery process reclaims expired leases and resumes safe work. CX queries the task or receives updates through its channel design.

Model reasoning outputs can be saved as artifacts, but recovery follows explicit step state rather than asking a model to remember where it stopped. External mutations have operation records and reconciliation paths.

## Data and contracts

Store task/step ID, dependency graph, attempt, lease expiry, fencing epoch, input versions, result artifact, operation ID, and terminal status. Each step declares retry and compensation behavior. State updates are conditional so an old worker cannot overwrite newer completion.

## Failure, security, and scale

A worker may continue after losing its lease; fence authoritative writes and use external idempotency where available. Detect stuck tasks, cap retries, and expose operator repair tools. Recheck authorization for newly executed protected steps when policy requires it. Limit active workflows per tenant.

## Trade-off and validation

Fine-grained checkpoints reduce repeated work but increase storage and orchestration overhead. Checkpoint costly or consequential boundaries first. Inject crashes before/after side effects and state commits. Verify operation counts and outcome reconciliation, not just eventual terminal status.

## Interview follow-up answered

**A worker performed an action but crashed before checkpointing.** Consult the durable operation and external status using the same operation reference. Resume with the recorded result or reconcile uncertainty. Blindly rerunning the step is safe only when its side effects have a proven idempotency contract.
