# Q024. Design retrieval reranking

## Scope and success

Improve ordering of a bounded candidate set before answer generation. Assume first-stage hybrid retrieval already applies authorization. Define relevance labels, context budget, deadline, and cost. Success means better evidence coverage in the final prompt without sacrificing required latency.

## Architecture and request path

CX's knowledge webhook requests candidates from lexical/vector search. A reranker scores query-passage pairs or a bounded list. The service selects top evidence while enforcing source diversity and document-version consistency. It can include parent context for passages requiring exceptions or definitions.

Keep an evaluated fallback ordering when the reranker is unavailable. Reranking cannot recover a relevant document never retrieved, so first-stage recall remains independently measured.

## Data and contracts

Candidates contain source/chunk IDs, permitted text, first-stage ranks, and metadata. Results contain new ranks, configuration ID, and safe diagnostics. Labels distinguish direct answer support, related background, contradiction, and irrelevant evidence. Avoid interpreting ranking scores as calibrated factual confidence.

## Failure, security, and scale

Cap candidates and passage length. Batch independent scoring where beneficial, with bounded queue wait. All candidates are authorized before model processing. Preserve query and source instructions as data. If the reranker times out, continue only through an evaluated degraded path and report that condition in telemetry.

## Trade-off and validation

Cross-encoder or model-based reranking can improve relevance but adds serving cost and latency. Cheap heuristics may suffice for exact policy codes. Compare ranking quality, sufficient-evidence rate, answer correctness, and end-to-end cost. Test long passages and conflicting policy versions.

## Interview follow-up answered

**Reranking improves average relevance but removes necessary exceptions.** Add evidence-completeness labels and selection rules that preserve linked exceptions, then evaluate task outcomes. Optimizing a passage ranking metric alone can produce a worse final answer when several passages must be considered together.
