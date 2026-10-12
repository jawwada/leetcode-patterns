# Q014. Design low-latency streaming interactions

## Scope and success

Reduce perceived delay for chat or voice while preserving correct actions and final answers. Distinguish acknowledgment, first useful content, complete response, and business completion. Establish what the chosen channel and CX interface can actually stream.

## Architecture and request path

The channel maintains a streaming connection where supported. CX can deliver queued partial responses before bounded webhook work. The webhook uses deadlines for identity, retrieval, and inference, then returns a validated result. A custom channel can separately support a carefully designed backend streaming experience, but that requires explicit coordination with CX state.

For long tasks, acknowledge acceptance, create a durable operation, and provide a status path. A worker does not automatically inject arbitrary text into a CX session. Choose polling, a channel event, or an authorized notification mechanism.

## Data and contracts

Events need conversation and turn sequence, response type, operation reference, and finality. An acknowledgment says work started; only an authoritative final status says it succeeded. The client handles duplicate events and superseded turns. Persist side effects independently of whether the customer receives the response.

## Failure, security, and scale

Cancel unnecessary read/generation work when superseded, but reconcile accepted mutations. Bound output buffers and apply backpressure to slow clients. Do not stream unvalidated sensitive evidence or unsupported claims merely to improve first-token time. Voice playback cancellation needs channel-specific testing.

## Trade-off and validation

Early output improves responsiveness but can complicate correction and safety checks. Stream low-risk progress messages and evaluate the treatment of generated content separately. Measure first acknowledgment, first useful result, full latency, abandonment, and correctness after interruption.

## Interview follow-up answered

**Can the synchronous webhook stream model tokens directly to CX?** Do not assume it can. Use the documented webhook response contract and supported CX partial-response behavior. Arbitrary token streaming requires a compatible client/backend design with explicit turn ownership, cancellation, and final-result handling.
