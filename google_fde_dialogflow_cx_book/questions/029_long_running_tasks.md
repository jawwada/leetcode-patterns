# Q029. Design long-running conversational tasks

## Scope and success

Support tasks such as document analysis or legacy case processing that exceed one conversational turn. Establish acceptance, progress, completion, cancellation, and notification semantics. Success is durable work with an accurate status path even if the customer disconnects.

## Architecture and request path

CX collects required inputs and invokes an acceptance webhook. The backend validates authority, records a job and outbox event, and returns a job reference promptly. Workers perform bounded steps asynchronously. A CX Status flow queries the same job; a custom channel or approved notification can deliver updates.

Separate accepted from completed. A message saying the request was received must not imply that processing succeeded. Route cancellation to a backend operation that checks whether remaining work is cancellable.

## Data and contracts

Persist job ID, principal, input versions, state, step progress, deadline, result reference, and cancellation request. States include QUEUED, RUNNING, SUCCEEDED, FAILED, CANCEL_REQUESTED, and OUTCOME_UNKNOWN where external actions require reconciliation. Progress represents actual milestones, not invented percentages.

## Failure, security, and scale

Use idempotent workers, leases, bounded retries, and dead-letter handling. Customer status requests require ownership checks. Backpressure and per-tenant quotas prevent large jobs starving interactive traffic. Expire abandoned inputs and results according to policy.

## Trade-off and validation

Asynchrony adds state and user-experience complexity but makes long work resilient. Prefer synchronous execution only when the bounded task reliably fits the deadline. Test disconnects, repeated acceptance, worker restarts, stalled tasks, cancellation races, and expired results.

## Interview follow-up answered

**Can the worker send its answer to CX when done?** Choose an explicit supported delivery mechanism. A queue completion event alone does not create an end-user turn. Polling, a channel-controlled event, or an authorized notification must map the result to the correct customer and handle expired sessions.
