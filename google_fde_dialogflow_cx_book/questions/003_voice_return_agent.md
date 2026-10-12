# Q003. Design a voice support agent that creates return requests

## Scope and success

Allow callers to identify an order, select an item, check eligibility, and create a return. Assume a telephony provider and an existing return API. Clarify verification policy, supported languages, transfer behavior, and allowable silence. A completed task is one authoritative return associated with the correct customer and item.

## Architecture and request path

The telephony integration connects audio to CX. A Returns flow uses pages for verification, order selection, item, reason, eligibility, confirmation, submission, and result. Webhooks return structured order data and a backend proposal. Confirmation names the exact item and quantity; submission uses the proposal's operation ID.

Use concise prompts, explicit corrections, and keypad input for suitable values where supported. A customer asking a policy question can temporarily enter a knowledge path, then return to the still-valid proposal. The channel performs actual human transfer.

## Data and contracts

Persist proposals, operations, verification references, and transfer packages outside CX. Keep amount and eligibility fields authoritative. A handoff includes completed steps and pending operation status so a human does not repeat a submitted action.

## Failure, security, and scale

Budget recognition, processing, webhook work, and playback together. Downstream deadlines must fit the turn budget including possible webhook retries. Handle dropped calls by reconciling the operation; do not require the original session to survive. Caller ID alone is not adequate proof of identity for protected actions.

## Trade-off and validation

More confirmations increase duration but can reduce consequential recognition errors. Confirm critical values rather than every word. Test noisy audio, accents, interruptions, silence, repeated yes, and yes-with-correction utterances. Track task completion, transfer acceptance, abandonment, and end-to-end latency.

## Interview follow-up answered

**The caller hangs up after submission.** The durable operation continues or reconciles independently. On a later verified interaction, retrieve its status. An authorized notification can deliver the result if the customer chose that channel; the conversation engine does not need to retain the old call.
