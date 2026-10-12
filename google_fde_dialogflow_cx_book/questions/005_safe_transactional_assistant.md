# Q005. Design a safe transactional assistant with confirmation

## Scope and success

Support address changes or return creation for verified customers. Define reversible and consequential actions, required verification, and confirmation policy. The invariant is that the executed action matches the authorized customer's confirmed proposal and is not duplicated under retry.

## Architecture and request path

CX gathers values in a flow. The backend validates them and issues a proposal containing action, affected resource, expected version, expiry, and principal binding. CX presents a deterministic confirmation message assembled from those fields. A scoped confirmation route submits the proposal to a domain service.

The domain service rechecks authorization, record version, eligibility, and confirmation requirements, then atomically creates or retrieves the operation. A worker executes external work and reconciles uncertain outcomes. CX reports the operation's actual state.

## Data and contracts

Use Proposal, ConfirmationRecord, Operation, and Outbox tables. Generate operation IDs server-side. Store money as integer minor units with currency. Proposal changes invalidate prior confirmation. For high-impact web actions, an application-issued confirmation nonce or step-up flow can provide stronger evidence than an unconstrained text parameter.

## Failure, security, and scale

Client parameters and generated JSON cannot grant authorization. Use optimistic versions or locks to reject concurrent changes. Duplicate submissions return the existing operation. Unknown provider outcomes trigger status lookup, not a new action. Bound proposal lifetime and keep audit references without storing unnecessary credentials.

## Trade-off and validation

Extra confirmation can add friction; apply it according to action risk and customer policy. Test yes-with-modification, stale versions, expired proposals, two sessions submitting, repeated delivery, and lost responses. Verify invariants directly against the operation database.

## Interview follow-up answered

**Can a low-temperature model guarantee safe execution?** No. Generation settings do not enforce identity, transaction uniqueness, or current eligibility. The backend proposal and operation protocol provides those controls, while the model helps interpret language and explain results.
