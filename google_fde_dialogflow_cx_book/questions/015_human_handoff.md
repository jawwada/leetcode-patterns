# Q015. Design human handoff with structured context

## Scope and success

Transfer customer conversations to support when requested or when automation cannot proceed. Define queue selection, hours, identity requirements, accepted transfer signals, and unavailable-support behavior. Success means the support platform accepts the case or live transfer, with accurate context.

## Architecture and request path

CX enters an Escalation flow, captures the reason and missing details, and calls a handoff backend. That backend builds a typed package, selects an authorized queue, and creates a handoff operation. CX emits the appropriate signal; the channel integration performs the actual transfer and reports acceptance.

Generate a concise issue summary if useful, but attach authoritative fields independently. Pending operations must be prominently identified so support does not resubmit them. Let customers request a human without passing a sentiment threshold.

## Data and contracts

Store handoff ID, conversation reference, verified identity reference, language, queue, completed steps, pending operation, state, and timestamps. Distinguish REQUESTED, ACCEPTED, CONNECTED, FAILED, and CALLBACK_REQUESTED. A generated summary is an annotation, not proof of action completion.

## Failure, security, and scale

Handle queue saturation, closed hours, channel failure, and customer disconnects. Offer an approved callback or case path where available. Restrict context to what the selected team may view. Deduplicate ticket creation and retain durable state across repeated transfer attempts.

## Trade-off and validation

Transferring more context reduces repetition but increases disclosure and cognitive load. Send a short summary plus structured facts and links to authorized records. Measure transfer acceptance, time to human, repeated explanation, resolution, and duplicate actions. Test pending transactions and failed transfers.

## Interview follow-up answered

**CX emitted handoff, but no human joined.** Inspect the channel and support-platform operation; the signal is not proof of a completed transfer. Keep the customer informed, retry within policy using the same handoff operation, and offer the agreed alternative when acceptance cannot be established.
